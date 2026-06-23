"""GRADUATE phase — silence classification and destination revision.

When the loop converges (SCAN returns NOTHING FOUND for N consecutive cycles),
GRADUATE reads the destination, retrospect, and recent trail to classify the
silence: ACHIEVED, STALE, STUCK, or PREMATURE. It then produces a proposal
written to .acm/graduate_proposal.md for operator review.

This is the robot's structural equivalent of the human noticing "this goal is
done, time to move on" or "the approach is exhausted."

Token tier: 2 (needs destination + retrospect + recent trail context).
All calls route through llm-harness-proxy. Never call the Anthropic API directly.

Triggers:
- Convergence signal in run-loop (2 consecutive NOTHING FOUND)
- Manual via future `ai-steward graduate` command

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
from ai_steward.pipeline._utils import _load_current_retrospect, _load_destination, _load_learning

if TYPE_CHECKING:
    import anthropic

logger = logging.getLogger(__name__)

_RECENT_TRAIL_BUDGET = 15000  # chars of recent trail entries delivered to GRADUATE


def _load_recent_trail(repo: Path, budget_chars: int = _RECENT_TRAIL_BUDGET) -> str:
    """Load the most recent entries from audit-trail.md.

    Takes the tail of the file — the most recent entries are most relevant
    for understanding the convergence pattern.
    """
    trail_file = repo / ".acm" / "audit-trail.md"
    if not trail_file.exists():
        return "[No audit-trail.md found]"
    content = trail_file.read_text(encoding="utf-8")
    if len(content) > budget_chars:
        return f"[truncated to last {budget_chars} chars]\n\n" + content[-budget_chars:]
    return content


def _extract_proposal_content(response_text: str) -> str:
    """Extract the proposal content from the model's response.

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


def graduate(
    repo: Path,
    config: AiStewardConfig,
    trigger: str = "convergence",
    client: "anthropic.Anthropic | None" = None,
) -> tuple[str, int, int]:
    """Run the GRADUATE phase — classify convergence and propose next destination.

    Args:
        repo: Repository root.
        config: Pipeline configuration.
        trigger: What triggered this graduate call (e.g., "nothing_found_streak_2").
        client: Anthropic client (injected for testing).

    Returns:
        (proposal_content, input_tokens, output_tokens)
        proposal_content is the new content for .acm/graduate_proposal.md
    """
    logger.info("GRADUATE phase starting (trigger: %s)", trigger)

    if client is None:
        client = anthropic_client(config.harness)

    destination = _load_destination(repo, config.destination_budget_chars)
    retrospect = _load_current_retrospect(repo)
    learning = _load_learning(repo)
    recent_trail = _load_recent_trail(repo)
    today = date.today().isoformat()

    user_content = f"""## Destination (operator-held)

{destination}

---

## Current retrospect.md

{retrospect}

---

## Learning surface (pre-extracted [!REALIZATION]/[!REVERSAL] markers)

{learning}

---

## Recent audit trail (most recent entries)

{recent_trail}

---

Today's date: {today}
Trigger: {trigger}
Target name: {repo.name}
"""

    logger.debug("GRADUATE user content length: %d chars", len(user_content))

    model = config.models.reorient or config.models.analyze
    message = client.messages.create(
        model=model,
        max_tokens=config.max_tokens_graduate,
        system=_prompts.GRADUATE_SYSTEM,
        messages=[{"role": "user", "content": user_content}],
    )

    block = message.content[0] if message.content else None
    response_text = getattr(block, "text", "") or "" if block else ""
    proposal_content = _extract_proposal_content(response_text)

    input_tokens = getattr(message.usage, "input_tokens", 0)
    output_tokens = getattr(message.usage, "output_tokens", 0)

    logger.info(
        "GRADUATE complete: %d in / %d out tokens", input_tokens, output_tokens
    )
    return proposal_content, input_tokens, output_tokens


def write_proposal(repo: Path, content: str) -> Path:
    """Write graduate proposal to .acm/graduate_proposal.md.

    Overwrites any previous proposal — the current proposal is always the
    most recent convergence assessment. History lives in audit-trail.md.
    """
    acm_dir = repo / ".acm"
    acm_dir.mkdir(parents=True, exist_ok=True)
    proposal_path = acm_dir / "graduate_proposal.md"
    proposal_path.write_text(content + "\n", encoding="utf-8")
    logger.info("GRADUATE proposal written to %s", proposal_path)
    return proposal_path
