"""REORIENT phase — arc-level reading of the improvement trail.

Reads the full audit-trail.md, forms arc-claims, and rewrites learning.md.
This is the robot's equivalent of the human-driven Learn skill.

Token tier: 2 (needs large context for full trail reading).
All calls route through llm-harness-proxy. Never call the Anthropic API directly.

Triggers:
- After N successful cycles (configurable: reorient_interval)
- After NOTHING FOUND (before declaring convergence)
- After VERIFY FAILED (something went wrong, reassess)
- Manual via `ai-steward reorient` command

Called from cli.py multi-cycle mode, not from single-cycle run().
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

from ai_steward.config import AiStewardConfig
from ai_steward.harness import anthropic_client
from ai_steward.memory import acm_dir, read_trail, trail_exists, trail_location
from ai_steward.pipeline import _prompts
from ai_steward.pipeline._utils import _load_current_orientation, _load_destination, _load_learning

if TYPE_CHECKING:
    import anthropic

logger = logging.getLogger(__name__)


def _load_audit_trail(repo: Path, budget_chars: int = 50000) -> str:
    """Load the full audit trail (audit-trail.md and bound records/), truncated to budget if necessary."""
    if not trail_exists(repo):
        return f"[No audit-trail.md found (checked {trail_location(repo)})]"
    content = read_trail(repo)
    if len(content) > budget_chars:
        # Take the most recent entries (end of file)
        return f"[truncated to last {budget_chars} chars]\n\n" + content[-budget_chars:]
    return content


def _extract_orientation_content(response_text: str) -> str:
    """Extract the learning.md content from the model's response.

    The model is instructed to return only markdown in a code fence.
    Extract it; fall back to raw response if no fence found.
    """
    # Look for markdown code fence
    if "```markdown" in response_text:
        start = response_text.find("```markdown") + len("```markdown")
        end = response_text.find("```", start)
        if end > start:
            return response_text[start:end].strip()

    # Look for generic code fence
    if "```" in response_text:
        start = response_text.find("```") + 3
        # Skip language tag if present
        newline = response_text.find("\n", start)
        if newline > start:
            start = newline + 1
        end = response_text.find("```", start)
        if end > start:
            return response_text[start:end].strip()

    # No fence found — use raw response
    return response_text.strip()


def reorient(
    repo: Path,
    config: AiStewardConfig,
    trigger: str,
    client: "anthropic.Anthropic | None" = None,
) -> tuple[str, int, int]:
    """Run the REORIENT phase — arc-level trail reading.

    Args:
        repo: Repository root.
        config: Pipeline configuration.
        trigger: What triggered this reorient (e.g., "nothing_found", "interval_5", "manual").
        client: Anthropic client (injected for testing).

    Returns:
        (orientation_content, input_tokens, output_tokens)
        orientation_content is the new content for learning.md in the memory scope
    """
    logger.info("REORIENT phase starting (trigger: %s)", trigger)

    if client is None:
        client = anthropic_client(config.harness)

    # Build context
    destination = _load_destination(repo, config.destination_budget_chars)
    audit_trail = _load_audit_trail(repo, config.reorient_trail_budget_chars)
    current_orientation = _load_current_orientation(repo)
    learning = _load_learning(repo)
    today = date.today().isoformat()

    user_content = f"""## Destination (operator-held)

{destination}

---

## Current learning.md

{current_orientation}

---

## Learning surface (pre-extracted [!REALIZATION]/[!REVERSAL] markers)

{learning}

---

## Full audit-trail.md

{audit_trail}

---

Today's date: {today}
Trigger: {trigger}
Target name: {repo.name}
"""

    logger.debug("REORIENT user content length: %d chars", len(user_content))

    model = config.models.reorient or config.models.analyze
    message = client.messages.create(
        model=model,
        max_tokens=config.max_tokens_reorient,
        system=_prompts.REORIENT_SYSTEM,
        messages=[{"role": "user", "content": user_content}],
    )

    block = message.content[0] if message.content else None
    response_text = getattr(block, "text", "") or "" if block else ""
    orientation_content = _extract_orientation_content(response_text)

    # Extract token counts
    input_tokens = getattr(message.usage, "input_tokens", 0)
    output_tokens = getattr(message.usage, "output_tokens", 0)

    logger.info(
        "REORIENT complete: %d input tokens, %d output tokens",
        input_tokens,
        output_tokens,
    )

    return orientation_content, input_tokens, output_tokens


def write_orientation(repo: Path, content: str) -> Path:
    """Write the new learning.md content to disk.

    Creates the memory directory (bound scope dir, or legacy .acm/) if it
    doesn't exist. Returns the path to the written file.
    """
    memory_dir = acm_dir(repo)
    memory_dir.mkdir(parents=True, exist_ok=True)

    orientation_file = memory_dir / "learning.md"
    orientation_file.write_text(content, encoding="utf-8")

    logger.info("Wrote %s (%d chars)", orientation_file, len(content))
    return orientation_file
