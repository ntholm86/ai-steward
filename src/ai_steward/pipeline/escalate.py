"""ESCALATE phase — failure pattern classification and operator escalation.

When the loop records N consecutive failure cycles (VERIFY FAILED or IMPLEMENT FAILED),
ESCALATE reads the destination and recent trail to classify the failure pattern:
TOOLING_BROKEN, PIPELINE_BOTTLENECK, DESTINATION_UNREACHABLE, or CONTEXT_INSUFFICIENT.
It writes .acm/escalate_report.md for operator review and the loop stops cleanly.

This is the robot's structural equivalent of recognising "I keep failing for the same
reason — a human needs to make a decision I can't."

Token tier: 1 (focused failure context, no retrospect needed — recent trail has the
evidence; retrospect adds no cognitive yield for concrete failure diagnosis).
All calls route through llm-harness-proxy. Never call the Anthropic API directly.

Triggers:
- Failure streak in run-loop (N consecutive VERIFY FAILED or IMPLEMENT FAILED)
- Manual via future `ai-steward escalate` command

Called from cli.py run-loop, not from single-cycle run().
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

from ai_steward.config import AiStewardConfig
from ai_steward.harness import anthropic_client
from ai_steward.pipeline import _prompts
from ai_steward.pipeline._utils import _load_destination

if TYPE_CHECKING:
    import anthropic

logger = logging.getLogger(__name__)

_FAILURE_TRAIL_BUDGET = 8000  # chars — smaller than GRADUATE; failure messages are dense, not long


def _load_failure_context(repo: Path, budget_chars: int = _FAILURE_TRAIL_BUDGET) -> str:
    """Load recent trail entries focused on the failure pattern.

    Takes the tail of audit-trail.md — the failure streak is in recent history.
    Smaller budget than GRADUATE: failure messages are dense, not long.
    """
    trail_file = repo / ".acm" / "audit-trail.md"
    if not trail_file.exists():
        return "[No audit-trail.md found]"
    content = trail_file.read_text(encoding="utf-8")
    if len(content) > budget_chars:
        return f"[truncated to last {budget_chars} chars]\n\n" + content[-budget_chars:]
    return content


def _extract_report_content(response_text: str) -> str:
    """Extract the report content from the model's response.

    The model is instructed to return only markdown in a code fence.
    Extract it; fall back to raw response if no fence found.
    """
    if "```markdown" in response_text:
        start = response_text.find("```markdown") + len("```markdown")
        end = response_text.find("```", start)
        if end > start:
            return response_text[start:end].strip()

    if "```" in response_text:
        start = response_text.find("```") + 3
        newline = response_text.find("\n", start)
        if newline > start:
            start = newline + 1
        end = response_text.find("```", start)
        if end > start:
            return response_text[start:end].strip()

    return response_text.strip()


def escalate(
    repo: Path,
    config: AiStewardConfig,
    trigger: str = "failure_streak",
    current_error: str = "",
    client: "anthropic.Anthropic | None" = None,
) -> tuple[str, int, int]:
    """Run the ESCALATE phase — classify the failure pattern and escalate to operator.

    Args:
        repo: Repository root.
        config: Pipeline configuration.
        trigger: What triggered this call (e.g., "failure_streak_3").
        current_error: Most recent error message from the failing cycle.
        client: Anthropic client (injected for testing).

    Returns:
        (report_content, input_tokens, output_tokens)
        report_content is the new content for .acm/escalate_report.md
    """
    logger.info("ESCALATE phase starting (trigger: %s)", trigger)

    if client is None:
        client = anthropic_client(config.harness)

    destination = _load_destination(repo, config.destination_budget_chars)
    failure_context = _load_failure_context(repo)
    today = date.today().isoformat()

    user_content = f"""## Destination (operator-held)

{destination}

## Recent trail (last {_FAILURE_TRAIL_BUDGET} chars — look for the failure pattern)

{failure_context}

## Current error (most recent failure)

{current_error or "[No error message provided]"}

## Your task

Today is {today}. Trigger: {trigger}.
Classify the failure pattern and produce an escalation report for the operator.
"""

    model = config.models.reorient or config.models.analyze
    response = client.messages.create(
        model=model,
        max_tokens=config.max_tokens_escalate,
        system=_prompts.ESCALATE_SYSTEM,
        messages=[{"role": "user", "content": user_content}],
    )
    in_tok = response.usage.input_tokens
    out_tok = response.usage.output_tokens
    raw = "".join(getattr(block, "text", "") for block in response.content)
    report_content = _extract_report_content(raw)
    return report_content, in_tok, out_tok


def write_report(repo: Path, content: str) -> Path:
    """Write the escalation report to .acm/escalate_report.md.

    Overwrites any previous report — current assessment supersedes old ones.
    History of failures lives in audit-trail.md (append-only).
    """
    acm_dir = repo / ".acm"
    acm_dir.mkdir(exist_ok=True)
    report_path = acm_dir / "escalate_report.md"
    report_path.write_text(content, encoding="utf-8")
    logger.info("Escalation report written to %s", report_path)
    return report_path
