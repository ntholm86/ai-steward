"""RECORD phase — tier 0, no LLM call.

Appends an audit trail entry to <target_repo>/.trail/audit-trail.md
and stages the changed file (git add) for operator review.

Called after VERIFY has confirmed the change is safe to stage.
The operator reviews the staged diff and commits or discards.

See .trail/audit-trail.md (2026-06-19 V1 Pipeline Design) for the
full spec and rationale.
"""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

from ai_steward.config import AiStewardConfig
from ai_steward.pipeline._types import Finding

# claude-haiku-4-5 pricing (V1 model — update if model changes)
_INPUT_COST_PER_TOKEN = 0.80 / 1_000_000   # $0.80 / MTok
_OUTPUT_COST_PER_TOKEN = 4.00 / 1_000_000  # $4.00 / MTok


def record(
    repo: Path,
    config: AiStewardConfig,
    finding: Finding,
    diff: str,
) -> str:
    """Append a trail entry and stage the changed file.

    Args:
        repo: Repository root.
        config: Pipeline configuration (reserved for future use in V2).
        finding: The change that was applied by IMPLEMENT.
        diff: Output of ``git diff HEAD -- <file>`` captured before staging.

    Returns:
        The trail entry string that was appended.
    """
    entry = _build_entry(finding, diff)
    _append_to_trail(repo, entry)
    _stage_file(repo, finding.file)
    return entry


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_entry(finding: Finding, diff: str) -> str:
    today = date.today().isoformat()
    scan_cost = (
        finding.input_tokens * _INPUT_COST_PER_TOKEN
        + finding.output_tokens * _OUTPUT_COST_PER_TOKEN
    )
    impl_cost = (
        finding.impl_input_tokens * _INPUT_COST_PER_TOKEN
        + finding.impl_output_tokens * _OUTPUT_COST_PER_TOKEN
    )
    cycle_cost = scan_cost + impl_cost
    return (
        f"\n---\n\n"
        f"## {today} \u2014 ai-steward: {finding.description}\n\n"
        f"**File:** {finding.file}  \n"
        f"**Risk:** {finding.risk}  \n"
        f"**Rationale:** {finding.rationale}\n\n"
        f"**Tokens:** "
        f"SCAN {finding.input_tokens}/{finding.output_tokens} "
        f"\u2014 IMPL {finding.impl_input_tokens}/{finding.impl_output_tokens} "
        f"\u2014 cycle est. ${cycle_cost:.5f} USD  \n\n"
        f"**Proposed change:**\n```\n{finding.proposed_change}\n```\n\n"
        f"**Diff:**\n```diff\n{diff}\n```\n\n"
        f"*Staged for operator review. Not committed.*\n"
    )


def _append_to_trail(repo: Path, entry: str) -> None:
    trail_dir = repo / ".trail"
    trail_dir.mkdir(exist_ok=True)
    trail_file = trail_dir / "audit-trail.md"
    with trail_file.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(entry)


def _stage_file(repo: Path, rel_path: str) -> None:
    """Stage the changed file. Silent on failure — operator will notice on review."""
    subprocess.run(
        ["git", "add", "--", rel_path],
        cwd=repo,
        capture_output=True,
    )
