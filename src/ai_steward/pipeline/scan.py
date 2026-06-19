"""SCAN phase — one Anthropic LLM call via harness.

Combines ANALYZE and PROPOSE: asks the model to identify one improvement
AND describe the specific change in a single prompt. Returns a Finding,
or None if nothing actionable was found.

Token tier: 1 (cheap model — claude-haiku-4-5 or equivalent).
All calls route through harness-protocol. Never call the Anthropic API directly.

See .trail/audit-trail.md (2026-06-19 V1 Pipeline Design) for the
full prompt rationale and gate conditions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from ai_steward.config import AiStewardConfig
from ai_steward.harness import anthropic_base_url
from ai_steward.pipeline.loop import Finding

if TYPE_CHECKING:
    import anthropic


_SYSTEM_PROMPT = """\
You are a software improvement assistant examining a repository.
Identify ONE high-value improvement and describe it precisely.

Respond with a JSON object only — no prose, no markdown fences, no explanation:
{
  "file": "<repo-relative path to the file to change>",
  "description": "<what the improvement is, one sentence>",
  "proposed_change": "<the new content or specific replacement — not a diff>",
  "rationale": "<why this change earns its maintenance cost>",
  "risk": "<low | medium | high>"
}

If you find nothing worth changing, respond with exactly: {"nothing": true}

Rules:
- Only suggest low or medium risk changes.
- The file must be in the provided file list.
- Be specific: "Remove unused import os from utils.py" not "clean up imports".
- proposed_change must be the actual replacement content, ready to write.
"""


def _collect_files(repo: Path, config: AiStewardConfig) -> dict[str, str]:
    """Read files within scope for the SCAN context window.

    Returns {relative_path: content}. Respects scope.allowed and
    scope.blocked glob patterns. Defaults to **/*.py if allowed is empty.
    """
    patterns = config.scope.allowed if config.scope.allowed else ["**/*.py"]
    blocked = config.scope.blocked

    files: dict[str, str] = {}
    for pattern in patterns:
        for path in sorted(repo.glob(pattern)):
            if not path.is_file():
                continue
            rel = str(path.relative_to(repo))
            if any(path.match(b) for b in blocked):
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
        import anthropic as _anthropic

        client = _anthropic.Anthropic(
            base_url=anthropic_base_url(config.harness),
        )

    files = _collect_files(repo, config)
    if not files:
        return None

    file_list = "\n\n".join(
        f"=== {rel} ===\n{content}" for rel, content in files.items()
    )

    message = client.messages.create(
        model=config.models.analyze,
        max_tokens=1024,
        system=_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Repository files:\n\n{file_list}\n\nIdentify one improvement.",
            }
        ],
    )

    # Extract text from response
    text = ""
    for block in message.content:
        if hasattr(block, "text"):
            text = block.text.strip()
            break

    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None

    if data.get("nothing"):
        return None

    # Validate required fields present
    required = {"file", "description", "proposed_change", "rationale", "risk"}
    if not required.issubset(data.keys()):
        return None

    # V1 gate: skip high-risk findings
    if data["risk"] == "high":
        return None

    # Validate the file actually exists
    target = repo / data["file"]
    if not target.is_file():
        return None

    return Finding(
        file=data["file"],
        description=data["description"],
        proposed_change=data["proposed_change"],
        rationale=data["rationale"],
        risk=data["risk"],
    )
