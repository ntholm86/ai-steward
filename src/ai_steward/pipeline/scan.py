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
import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING

from ai_steward.config import AiStewardConfig
from ai_steward.harness import anthropic_client
from ai_steward.pipeline import _prompts
from ai_steward.pipeline._types import Finding

if TYPE_CHECKING:
    import anthropic

logger = logging.getLogger(__name__)

_BASE_SYSTEM_PROMPT = _prompts.SCAN_SYSTEM


# Additional examination guidance injected per operator-configured lens.
# Keys map to values in config.lenses. 'mandate' and 'examination' are the
# built-in lenses — they map to Steps 1 and 2 in the base prompt (no injection needed).
# All other lens names inject additional examination paragraphs into the system prompt.
_LENS_INSTRUCTIONS: dict[str, str] = {
    "security": (
        "When examining in Step 2, also apply a security lens: identify injection "
        "risks, authentication gaps, authorization bypasses, sensitive data exposure, "
        "and insecure dependencies. Flag any finding from this lens explicitly."
    ),
    "overburden": (
        "When examining in Step 2, also apply an overburden lens: identify components "
        "doing too much — functions or classes with too many responsibilities, modules "
        "with high coupling, or processes that concentrate risk."
    ),
    "performance": (
        "When examining in Step 2, also apply a performance lens: identify O(n²) "
        "operations, blocking I/O, redundant computation, or unnecessary allocations "
        "on hot paths."
    ),
    "waste": (
        "When examining in Step 2, also apply a waste lens: identify dead code, "
        "abstractions with a single consumer, validation that can never fire, or "
        "documentation that restates the obvious without adding meaning."
    ),
}

# Keys that map to base-prompt steps (no additional injection needed)
_BUILTIN_LENSES = frozenset({"mandate", "examination"})


def _build_system_prompt(lenses: list[str]) -> str:
    """Build the SCAN system prompt, injecting guidance for operator-configured lenses.

    'mandate' and 'examination' are built-in lenses that correspond to Steps 1 and 2
    in the base prompt — no injection needed. Any other lens name in `lenses` that
    matches a key in _LENS_INSTRUCTIONS injects additional examination guidance.
    Unknown lens names are silently ignored (forward-compatible).

    The default config ['mandate', 'examination'] produces the base prompt unchanged.
    """
    extras = [
        _LENS_INSTRUCTIONS[lens]
        for lens in lenses
        if lens not in _BUILTIN_LENSES and lens in _LENS_INSTRUCTIONS
    ]
    if not extras:
        return _BASE_SYSTEM_PROMPT

    injection = "\n\n## Additional examination lenses (operator-configured)\n\n" + "\n\n".join(
        f"- {instruction}" for instruction in extras
    )
    # Inject after Step 2 block, before Step 3
    marker = "\n\n## Step 3 — [!DECISION]"
    return _BASE_SYSTEM_PROMPT.replace(marker, injection + marker, 1)

def _extract_json(text: str) -> dict | None:
    """Extract a JSON object from model output that may include prose or code fences.

    Takes the last valid JSON object found — when a model revises its answer,
    the final fence contains the intended response.
    """
    # Strategy 0: look for explicit ```json fences first — these are the
    # canonical output format and must be tried before the generic pattern.
    # The generic pattern's closing `\n``` ` can be mistakenly consumed when
    # two code fences are back-to-back (e.g. ```\ncontent\n```json\n{...}\n```)
    # because `\n``` ` matches the prefix of `\n```json`, leaving `json\n{...}`
    # as non-matching dangling text.
    json_fence_matches = list(re.finditer(r"```json\s*\n(.*?)\n```", text, re.DOTALL))
    for m in reversed(json_fence_matches):
        try:
            return json.loads(m.group(1).strip())
        except (json.JSONDecodeError, ValueError):
            continue

    # Strategy 1: extract from the last markdown code fence (generic)
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


def _load_scope_context(
    repo: Path,
    scope_depth: int = 4,
    budget_chars: int = 3000,
) -> str | None:
    """Load Commander's Intent from all applicable ACM scopes (ACM §4).

    Traverses parent directories from repo upward, collecting every
    .acm/destination.md found. Stop conditions (ACM §4.2):
      1. Filesystem root reached (hard stop, always applies)
      2. .acm-root marker file found in a directory: read that directory's
         .acm/destination.md if present, then stop (operator-declared ceiling)
      3. Implementation ceiling: scope_depth levels (operator-configurable via
         acm_scope_depth in .ai-steward.yaml; default 4 = session→repo→workspace→org)

    Higher scopes are listed first and take precedence.

    Total budget: budget_chars chars (operator-configurable via destination_budget_chars
    in .ai-steward.yaml; default 3000 ≈ 750 tokens). Split evenly: half for higher
    scopes, half for repo scope.

    Returns None if no destination.md exists at any scope.
    """
    # Collect all applicable destinations, outermost first
    parents: list[tuple[str, str]] = []  # (label, text)
    current = repo.parent
    repo_root = Path(repo.anchor)
    for _ in range(scope_depth):
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
    half = budget_chars // 2
    if parents:
        per_scope = max(300, half // len(parents))
        # Reverse so outermost (highest authority) is first
        for label, text in reversed(parents):
            truncated = _truncate_destination(text, per_scope)
            sections.append(f"### Higher-scope mandate ({label}):\n\n{truncated}")

    # Repo scope: up to half the total budget
    if repo_text is not None:
        truncated = _truncate_destination(repo_text, half)
        sections.append(f"### Repo-scope mandate:\n\n{truncated}")

    return "\n\n---\n\n".join(sections)


def _load_orient_context(repo: Path) -> str | None:
    """Load repo-scoped ORIENT context: retrospect.md and learning.md.

    retrospect.md is extracted in two guaranteed parts:

    1. Arc-claims head — up to 2000 chars from the top of the file.
       Claims are listed first in retrospect.md, so the head captures
       current arc-state.

    2. Operational rules — the full "## Active operational rules" section,
       extracted by header name and always appended as a separate subsection.
       Rules live at the END of retrospect.md.  In the current file they
       begin at char 5681.  The previous 1000-char head window delivered
       NONE of them — the model was operating without its operational
       constraints in every SCAN call.  Explicit header-targeted extraction
       makes delivery invariant to file length.

    learning.md carries chronological [!REALIZATION]/[!REVERSAL] markers;
    the tail is most relevant (most recent markers last).

    Budget: retrospect head ≤ 2000 chars; operational rules ≤ 3000 chars;
    learning tail ≤ 500 chars.  Returns None if neither file exists.
    """
    _RULES_MARKER = "## Active operational rules"
    sections: list[str] = []

    retrospect = repo / ".acm" / "retrospect.md"
    if retrospect.is_file():
        try:
            text = retrospect.read_text(encoding="utf-8", errors="ignore")
            # 1. Arc-claims: head of file.
            head = text[:2000] + "\n[... truncated ...]" if len(text) > 2000 else text
            sections.append(f"### Current orientation (retrospect):\n\n{head}")
            # 2. Operational rules: always extracted by section header.
            rules_idx = text.find(_RULES_MARKER)
            if rules_idx >= 0:
                rules_text = text[rules_idx:]
                if len(rules_text) > 3000:
                    rules_text = rules_text[:3000] + "\n[... truncated ...]"
                sections.append(f"### Active operational rules:\n\n{rules_text}")
        except OSError:
            pass

    learning = repo / ".acm" / "learning.md"
    if learning.is_file():
        try:
            text = learning.read_text(encoding="utf-8", errors="ignore")
            excerpt = "[... truncated ...]\n" + text[-500:] if len(text) > 500 else text
            sections.append(f"### Learning surface (recent markers):\n\n{excerpt}")
        except OSError:
            pass

    return "\n\n---\n\n".join(sections) if sections else None


_BINARY_HEURISTIC_BYTES = 8192

# Directories excluded when using the default scope (**/*).
# Operators who set scope.allowed explicitly are fully in control.
_DEFAULT_SKIP_DIRS = frozenset({
    ".acm", ".git", ".harness",
    "__pycache__", ".mypy_cache", ".pytest_cache",
    "node_modules", ".venv", "venv", ".tox",
})


def _is_binary(path: Path, byte_limit: int = _BINARY_HEURISTIC_BYTES) -> bool:
    """Return True if path appears to be a binary file.

    Uses the NUL-byte heuristic (same as git): if the first byte_limit bytes
    contain a NUL byte the file is treated as binary and excluded from SCAN
    context. byte_limit is operator-configurable via binary_heuristic_bytes.
    """
    try:
        chunk = path.read_bytes()[:byte_limit]
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
            if not config.scope.allowed and _is_binary(path, config.binary_heuristic_bytes):
                continue
            skip_dirs = frozenset(config.default_skip_dirs)
            if not config.scope.allowed and any(
                part in skip_dirs
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

    destination = _load_scope_context(
        repo,
        scope_depth=config.acm_scope_depth,
        budget_chars=config.destination_budget_chars,
    )
    orient = _load_orient_context(repo)

    parts: list[str] = []
    if destination:
        parts.append(
            f"Commander's Intent (operator destination — higher scope governs):\n\n{destination}"
        )
    if orient:
        parts.append(orient)
    parts.append(
        f"Repository files:\n\n{file_list}\n\n"
        + ("Identify one improvement that advances the stated destination."
           if destination else "Identify one improvement.")
    )
    user_content = "\n\n---\n\n".join(parts)

    message = client.messages.create(
        model=config.models.analyze,
        max_tokens=config.max_tokens_scan,
        system=_build_system_prompt(config.lenses),
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

    # Scope enforcement: reject proposals for files outside the configured scope.
    # The system prompt tells the model to only propose files from the provided file
    # list, but the model can reason its way around that instruction. This is the
    # structural gate — not a hint.
    if any(target.match(b) for b in config.scope.blocked):
        logger.warning("SCAN proposed blocked file %s — rejected by scope", file_path)
        return None
    if config.scope.allowed and not any(target.match(p) for p in config.scope.allowed):
        logger.warning("SCAN proposed out-of-scope file %s — rejected by scope", file_path)
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
        prediction=data.get("prediction", ""),
        examination_summary=data.get("examination_summary", ""),
        description=data["description"],
        proposed_change=data["proposed_change"],
        rationale=data["rationale"],
        risk=data["risk"],
        input_tokens=_in_tok,
        output_tokens=_out_tok,
        blind_spot=data.get("blind_spot", ""),
    )