"""RECORD phase — tier 0, no LLM call.

Appends an audit trail entry to <target_repo>/.acm/audit-trail.md
and stages the changed file (git add) for operator review.

Called after VERIFY has confirmed the change is safe to stage.
The operator reviews the staged diff and commits or discards.

See .acm/audit-trail.md (2026-06-19 V1 Pipeline Design) for the
full spec and rationale.
"""

from __future__ import annotations

import logging
import subprocess
from datetime import date
from pathlib import Path

from ai_steward.config import AiStewardConfig
from ai_steward.pipeline._types import Finding

logger = logging.getLogger(__name__)

# Pricing table (USD / token) for known Anthropic models.
# Source: https://www.anthropic.com/pricing — update when pricing changes.
# Unknown models fall back to haiku-4-5 as a conservative baseline estimate.
# Keys are base model names without date suffixes — _model_cost_per_token()
# matches by prefix so that date-versioned IDs (e.g. claude-haiku-4-5-20251001)
# resolve to the correct base tier.
_MODEL_PRICING: dict[str, tuple[float, float]] = {
    "claude-haiku-4-5":   (0.80 / 1_000_000,  4.00 / 1_000_000),
    "claude-sonnet-4-5":  (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-sonnet-4-6":  (3.00 / 1_000_000, 15.00 / 1_000_000),
    "claude-opus-4-5":    (15.00 / 1_000_000, 75.00 / 1_000_000),
}
_FALLBACK_PRICING: tuple[float, float] = (0.80 / 1_000_000, 4.00 / 1_000_000)


def _model_cost_per_token(model: str) -> tuple[float, float]:
    """Return (input_cost_per_token, output_cost_per_token) for a model.

    Matches by prefix so that date-versioned IDs such as
    ``claude-haiku-4-5-20251001`` resolve to the correct base-model tier.
    Unknown models fall back to the haiku-4-5 baseline.
    """
    for key, pricing in _MODEL_PRICING.items():
        if model == key or model.startswith(key + "-"):
            return pricing
    return _FALLBACK_PRICING


def _estimate_cycle_cost(config: AiStewardConfig, finding: Finding) -> float:
    """Estimate total cycle cost using model-appropriate pricing.

    Covers all three LLM phases: SCAN, IMPLEMENT, and REFLECT.
    REFLECT uses models.analyze (same model as SCAN).
    """
    scan_in, scan_out = _model_cost_per_token(config.models.analyze)
    impl_in, impl_out = _model_cost_per_token(config.models.implement)
    return (
        finding.input_tokens * scan_in
        + finding.output_tokens * scan_out
        + finding.impl_input_tokens * impl_in
        + finding.impl_output_tokens * impl_out
        + finding.reflect_input_tokens * scan_in   # REFLECT uses models.analyze
        + finding.reflect_output_tokens * scan_out
    )


def record(
    repo: Path,
    config: AiStewardConfig,
    finding: Finding,
    diff: str,
    harness_session_paths: list[str] | None = None,
) -> str:
    """Append a trail entry and stage the changed file.

    Args:
        repo: Repository root.
        config: Pipeline configuration — used for model-appropriate cost estimation.
        finding: The change that was applied by IMPLEMENT.
        diff: Output of ``git diff HEAD -- <file>`` captured before staging.
        harness_session_paths: Repo-relative paths to all harness session files
            created during this pipeline run (SCAN + IMPLEMENT + REFLECT), or
            None / empty when the harness was not running.

    Returns:
        The trail entry string that was appended.
    """
    cycle_cost_usd = _estimate_cycle_cost(config, finding)
    entry = _build_entry(finding, diff, harness_session_paths, cycle_cost_usd=cycle_cost_usd)
    _append_to_trail(repo, entry)
    _stage_file(repo, finding.file)
    return entry


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_entry(
    finding: Finding,
    diff: str,
    harness_session_paths: list[str] | None = None,
    cycle_cost_usd: float = 0.0,
) -> str:
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
    cycle_cost = cycle_cost_usd
    if harness_session_paths:
        session_line = ", ".join(f"`{p}`" for p in harness_session_paths)
    else:
        session_line = "not captured (harness not running or no calls made)"
    return (
        f"\n---\n\n"
        f"## {today} \u2014 ai-steward: {finding.description}\n\n"
        f"**[!DECISION]** Proposed: {finding.description}  \n"
        f"*Rationale:* {finding.rationale}  \n"
        f"*Risk:* {finding.risk}\n\n"
        f"**Prediction:** {finding.prediction or finding.proposed_change}  \n\n"
        f"**Lenses applied:**\n"
        + (
            finding.examination_summary + "\n\n"
            if finding.examination_summary
            else (
                f"- *Commander\u2019s Intent:* Operator destination (`.acm/destination.md`) "
                f"loaded \u2014 improvement selected against stated direction.\n"
                f"- *Code examination:* Repository files within scope scanned for structural improvements.\n\n"
            )
        )
        + f"**Blind spot:** {finding.blind_spot or 'Not identified for this run.'}\n\n"
        + (
            f"**Reflection:**\n{finding.reflection}\n\n"
            if finding.reflection
            else ""
        )
        + f"**File:** `{finding.file}`  \n"
        f"**Tokens:** "
        f"SCAN {finding.input_tokens}/{finding.output_tokens} "
        f"\u2014 IMPL {finding.impl_input_tokens}/{finding.impl_output_tokens} "
        f"\u2014 REFLECT {finding.reflect_input_tokens}/{finding.reflect_output_tokens} "
        f"\u2014 cycle est. ${cycle_cost:.5f} USD  \n"
        f"**Harness sessions:** {session_line}  \n\n"
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
