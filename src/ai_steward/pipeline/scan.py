"""SCAN phase — one Anthropic LLM call via harness.

Combines ANALYZE and PROPOSE: asks the model to identify one improvement
AND describe the specific change in a single prompt. Returns a Finding,
or None if nothing actionable was found.

Token tier: 1 (cheap model — claude-haiku-4-5 or equivalent).
All calls route through llm-harness-proxy. Never call the Anthropic API directly.

See .acm/audit-trail.md (2026-06-19 V1 Pipeline Design) for the
full prompt rationale and gate conditions.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

from ai_steward.config import AiStewardConfig
from ai_steward.harness import anthropic_client
from ai_steward.pipeline._types import Finding

if TYPE_CHECKING:
    import anthropic


_SYSTEM_PROMPT = """\
You are a software improvement assistant examining a repository.
Identify ONE high-value improvement and describe it precisely.

Respond with a JSON object only — no prose, no markdown fences, no explanation:
{
  "file": "<repo-relative path to the file to change>",
  "description": "<what the improvement is, one sentence>",
  "proposed_change": "<precise description of the exact change — what to add, remove, or replace and where, in one or two sentences. Do NOT include file contents.>",
  "rationale": "<why this change earns its maintenance cost>",
  "risk": "<low | medium | high>",
  "blind_spot": "<one area or file you did not examine and why — be specific>",
  "already_exists_check": "<paste the exact line(s) from the target file that prove this change is already implemented; write 'not found' if the change is not yet there>"
}

If you find nothing worth changing, respond with exactly: {"nothing": true}

Rules:
- Only suggest low or medium risk changes.
- The file must be in the provided file list.
- Be specific: "Remove unused import os from utils.py" not "clean up imports".
- proposed_change must describe the change, not reproduce file contents.
- IMPORTANT: Before proposing, read the target file and verify the change is not already implemented.
  If you find evidence it already exists, respond with {"nothing": true}.
"""

def _extract_json(text: str) -> dict | None:
    """Extract a JSON object from model output that may include prose or code fences.

    Takes the last valid JSON object found — when a model revises its answer,
    the final fence contains the intended response.
    """
    # Strategy 1: extract from the last markdown code fence
    fence_matches = list(re.finditer(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL))
    for m in reversed(fence_matches):
        try:
            return json.loads(m.group(1).strip())
        except (json.JSONDecodeError, ValueError):
            continue

    # Strategy 2: direct parse (model returned raw JSON as instructed)
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        pass

    # Strategy 3: extract outermost { ... } (handles trailing prose)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except (json.JSONDecodeError, ValueError):
            pass

    return None


def _truncate_destination(text: str, char_limit: int) -> str:
    """Truncate a destination.md to char_limit, starting at the nearest section
    heading boundary so SCAN receives a complete, labelled section rather than
    a mid-sentence fragment.
    """
    if len(text) <= char_limit:
        return text
    cutoff = len(text) - char_limit
    match = re.search(r"^## \d{4}-\d{2}-\d{2}", text[cutoff:], re.MULTILINE)
    tail = text[cutoff + match.start() :] if match else text[-char_limit:]
    return "[... destination.md truncated for token budget ...]\n\n" + tail


def _load_scope_context(repo: Path) -> str | None:
    """Load Commander's Intent from all applicable ACM scopes (ACM §4).

    Traverses parent directories from repo upward, collecting every
    .acm/destination.md found. Stop conditions (ACM §4.2):
      1. Filesystem root reached (hard stop, always applies)
      2. .acm-root marker file found in a directory: read that directory's
         .acm/destination.md if present, then stop (operator-declared ceiling)
      3. Implementation ceiling: 4 levels (session→repo→workspace→org)

    Higher scopes are listed first and take precedence.

    Total budget: ~3000 chars (~750 tokens). Split as:
      - Higher scopes (workspace/org): up to 1500 chars total
      - Repo scope: up to 1500 chars

    Returns None if no destination.md exists at any scope.
    """
    # Collect all applicable destinations, outermost first
    parents: list[tuple[str, str]] = []  # (label, text)
    current = repo.parent
    repo_root = Path(repo.anchor)
    for _ in range(4):
        if current == repo_root:
            break
        dest = current / ".acm" / "destination.md"
        if dest.is_file():
            try:
                text = dest.read_text(encoding="utf-8", errors="ignore")
                # Label by relative relationship to repo
                try:
                    rel = current.relative_to(repo.parent)
                    label = str(rel) if str(rel) != "." else "workspace"
                except ValueError:
                    label = current.name or "parent"
                parents.append((label, text))
            except OSError:
                pass
        # Stop at operator-declared scope ceiling (.acm-root marker)
        if (current / ".acm-root").exists():
            break
        current = current.parent

    # Repo-level destination
    repo_dest = repo / ".acm" / "destination.md"
    repo_text: str | None = None
    if repo_dest.is_file():
        try:
            repo_text = repo_dest.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            pass

    if not parents and repo_text is None:
        return None

    sections: list[str] = []

    # Higher scopes: allocate up to 1500 chars total, divided evenly
    if parents:
        per_scope = max(300, 1500 // len(parents))
        # Reverse so outermost (highest authority) is first
        for label, text in reversed(parents):
            truncated = _truncate_destination(text, per_scope)
            sections.append(f"### Higher-scope mandate ({label}):\n\n{truncated}")

    # Repo scope: up to 1500 chars
    if repo_text is not None:
        truncated = _truncate_destination(repo_text, 1500)
        sections.append(f"### Repo-scope mandate:\n\n{truncated}")

    return "\n\n---\n\n".join(sections)


_BINARY_HEURISTIC_BYTES = 8192

# Directories excluded when using the default scope (**/*).
# Operators who set scope.allowed explicitly are fully in control.
_DEFAULT_SKIP_DIRS = frozenset({
    ".acm", ".git", ".harness",
    "__pycache__", ".mypy_cache", ".pytest_cache",
    "node_modules", ".venv", "venv", ".tox",
})


def _is_binary(path: Path) -> bool:
    """Return True if path appears to be a binary file.

    Uses the NUL-byte heuristic (same as git): if the first 8 KB contains
    a NUL byte the file is treated as binary and excluded from SCAN context.
    """
    try:
        chunk = path.read_bytes()[:_BINARY_HEURISTIC_BYTES]
        return b"\x00" in chunk
    except OSError:
        return True  # unreadable — treat as binary


def _collect_files(repo: Path, config: AiStewardConfig) -> dict[str, str]:
    """Read files within scope for the SCAN context window.

    Returns {relative_path: content}. Respects scope.allowed and
    scope.blocked glob patterns. Defaults to **/* (all text files) if
    allowed is empty; binary files are excluded via NUL-byte heuristic.
    """
    patterns = config.scope.allowed if config.scope.allowed else ["**/*"]
    blocked = config.scope.blocked

    files: dict[str, str] = {}
    for pattern in patterns:
        for path in sorted(repo.glob(pattern)):
            if not path.is_file():
                continue
            rel = str(path.relative_to(repo))
            if any(path.match(b) for b in blocked):
                continue
            if not config.scope.allowed and _is_binary(path):
                continue
            if not config.scope.allowed and any(
                part in _DEFAULT_SKIP_DIRS
                for part in path.relative_to(repo).parts
            ):
                continue
            try:
                files[rel] = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
    return files


def scan(
    repo: Path,
    config: AiStewardConfig,
    client: anthropic.Anthropic | None = None,
) -> Finding | None:
    """Run the SCAN phase.

    Args:
        repo: Repository root.
        config: Pipeline configuration.
        client: Anthropic client. If None, creates one pointing at the harness.
                Pass a mock client in tests to avoid real API calls.

    Returns:
        A Finding if one actionable improvement was identified, None otherwise.
    """
    if client is None:
        client = anthropic_client(config.harness, harness_root=repo / ".acm")

    files = _collect_files(repo, config)
    if not files:
        return None

    file_list = "\n\n".join(
        f"=== {rel} ===\n{content}" for rel, content in files.items()
    )

    destination = _load_scope_context(repo)
    if destination:
        user_content = (
            f"Commander's Intent (operator destination — higher scope governs):\n\n{destination}\n\n"
            f"---\n\nRepository files:\n\n{file_list}\n\n"
            "Identify one improvement that advances the stated destination."
        )
    else:
        user_content = f"Repository files:\n\n{file_list}\n\nIdentify one improvement."

    message = client.messages.create(
        model=config.models.analyze,
        max_tokens=1024,
        system=_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": user_content,
            }
        ],
    )

    # Capture token usage before extracting text
    try:
        _in_tok = int(message.usage.input_tokens)
        _out_tok = int(message.usage.output_tokens)
    except (AttributeError, TypeError, ValueError):
        _in_tok = 0
        _out_tok = 0

    # Extract text from response
    text = ""
    for block in message.content:
        if hasattr(block, "text"):
            text = block.text.strip()
            break

    data = _extract_json(text)
    if data is None:
        return None

    if data.get("nothing"):
        return None

    # Validate required fields present
    required = {"file", "description", "proposed_change", "rationale", "risk"}
    if not required.issubset(data.keys()):
        return None

    # Validate the file path to reject directory traversal and absolute paths
    file_path = data["file"]
    if ".." in file_path or file_path.startswith("/") or ":" in file_path:
        return None

    # V1 gate: skip high-risk findings
    if data["risk"] == "high":
        return None

    # Validate the file actually exists
    target = repo / file_path
    if not target.is_file():
        return None

    # Guard: reject if the model's own check confirms the change is already implemented.
    # The model is asked to quote the specific line(s) that prove existence; if the
    # quoted text is actually found in the file, the proposal is a false-positive.
    already_check = data.get("already_exists_check", "not found").strip()
    if already_check.lower() != "not found" and len(already_check) >= 10:
        target_content = target.read_text(encoding="utf-8", errors="ignore")
        if already_check.lower() in target_content.lower():
            return None

    return Finding(
        file=file_path,
        description=data["description"],
        proposed_change=data["proposed_change"],
        rationale=data["rationale"],
        risk=data["risk"],
        input_tokens=_in_tok,
        output_tokens=_out_tok,
        blind_spot=data.get("blind_spot", ""),
    )