"""RECORD phase — tier 0, no LLM call.

Appends an audit trail entry to <target_repo>/.acm/audit-trail.md
and stages the changed file (git add) for operator review.

Called after VERIFY has confirmed the change is safe to stage.
The operator reviews the staged diff and commits or discards.

See .acm/audit-trail.md (2026-06-19 V1 Pipeline Design) for the
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
    harness_session_path: str | None = None,
) -> str:
    """Append a trail entry and stage the changed file.

    Args:
        repo: Repository root.
        config: Pipeline configuration (reserved for future use in V2).
        finding: The change that was applied by IMPLEMENT.
        diff: Output of ``git diff HEAD -- <file>`` captured before staging.
        harness_session_path: Repo-relative path to the harness session
            directory (e.g. ``.acm/sessions/01J.../``), or None if the
            harness session path could not be determined.

    Returns:
        The trail entry string that was appended.
    """
    entry = _build_entry(finding, diff, harness_session_path)
    _append_to_trail(repo, entry)
    _stage_file(repo, finding.file)
    return entry


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_entry(finding: Finding, diff: str, harness_session_path: str | None = None) -> str:
    """Build a structured trail entry from a Finding.

    The format is intentional and stable — do not refactor to add structural
    placeholders. In particular:

    - ``[!REVERSAL]`` must NEVER appear as a placeholder in this output.
      It belongs in audit-trail.md only when an operator appends it after a
      prediction is demonstrably wrong. The pipeline does not emit it.
    - The sections (DECISION, Prediction, Lenses, Blind spot, Tokens, Diff)
      are already the canonical improve-skill entry format. No restructuring
      is needed.

    See ``.acm/destination.md`` (Canonical trail entry format) for the
    authoritative spec.
    """
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
    session_line = (
        harness_session_path
        if harness_session_path
        else "not captured (harness not running or no calls made)"
    )
    return (
        f"\n---\n\n"
        f"## {today} \u2014 ai-steward: {finding.description}\n\n"
        f"**[!DECISION]** Proposed: {finding.description}  \n"
        f"*Rationale:* {finding.rationale}  \n"
        f"*Risk:* {finding.risk}\n\n"
        f"**Prediction:** {finding.prediction or finding.proposed_change}  \n\n"
        f"**Lenses applied:**\n"
        f"- *Commander\u2019s Intent:* Operator destination (`.acm/destination.md`) "
        f"loaded \u2014 improvement selected against stated direction.\n"
        f"- *Code examination:* Repository files within scope scanned for structural improvements.\n\n"
        f"**Blind spot:** {finding.blind_spot or 'Not identified for this run.'}\n\n"
        f"**File:** `{finding.file}`  \n"
        f"**Tokens:** "
        f"SCAN {finding.input_tokens}/{finding.output_tokens} "
        f"\u2014 IMPL {finding.impl_input_tokens}/{finding.impl_output_tokens} "
        f"\u2014 cycle est. ${cycle_cost:.5f} USD  \n"
        f"**Harness session:** `{session_line}`  \n\n"
        f"**Diff:**\n```diff\n{diff}\n```\n\n"
        f"*Staged for operator review. Not committed.*\n"
    )


def _append_to_trail(repo: Path, entry: str) -> None:
    trail_dir = repo / ".acm"
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
