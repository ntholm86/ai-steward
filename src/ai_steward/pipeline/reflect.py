"""REFLECT phase — one Anthropic LLM call via harness.

Synthesizes the VERIFY outcome against the SCAN prediction, producing
a structured reflection section for the audit trail entry.

Token tier: 1 (cheap model — same as SCAN by default).
All calls route through llm-harness-proxy. Never call the Anthropic API directly.

The reflection covers three things:
1. Whether the prediction held (based on verify result and diff)
2. A falsifiable model-claim about what the target is now or is becoming
3. A specific blind spot this cycle did not examine

Called from loop.py after VERIFY passes and before RECORD.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ai_steward.config import AiStewardConfig
from ai_steward.harness import anthropic_client
from ai_steward.pipeline._types import Finding

if TYPE_CHECKING:
    import anthropic


_REFLECT_SYSTEM = """\
You are reviewing the outcome of a software improvement cycle.
Write a concise reflection covering exactly three things:
1. Prediction accuracy: did the stated prediction hold? Note any mismatch.
2. Model claim: one falsifiable statement about what the target is now or is becoming.
3. Blind spot: one specific file or area this cycle did not examine, and why.

Two or three short paragraphs. No headers. No preamble. Write as a trail-entry author.
"""


def reflect(
    repo: Path,
    config: AiStewardConfig,
    finding: Finding,
    diff: str,
    client: "anthropic.Anthropic | None" = None,
) -> str:
    """Run the REFLECT phase after VERIFY passes.

    Args:
        repo: Repository root.
        config: Pipeline configuration.
        finding: The applied Finding (carries prediction and blind_spot from SCAN).
        diff: The applied diff (output of ``git diff HEAD -- <file>``).
        client: Anthropic client. If None, creates one pointing at the harness.
                Pass a mock client in tests to avoid real API calls.

    Returns:
        Prose reflection string. Empty string on any failure — never raises.
    """
    if client is None:
        import anthropic as _anthropic

        client = anthropic_client(config.harness, harness_root=repo / ".acm")

    prediction = finding.prediction or finding.proposed_change
    user_content = (
        f"Prediction made before the change:\n{prediction}\n\n"
        f"Change applied:\n```diff\n{diff}\n```\n\n"
        f"Verification: PASSED. "
        f"SCAN blind spot named: {finding.blind_spot or 'not identified'}."
    )

    try:
        message = client.messages.create(
            model=config.models.analyze,
            max_tokens=config.max_tokens_reflect,
            system=_REFLECT_SYSTEM,
            messages=[{"role": "user", "content": user_content}],
        )
        block = message.content[0] if message.content else None
        if block is None:
            return ""
        text = getattr(block, "text", "") or ""
        return text.strip()
    except Exception:
        return ""
