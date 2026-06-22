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


_BASE_REFLECT_SYSTEM = """\
You are reviewing the outcome of a software improvement cycle.
Write a concise reflection covering exactly three things:
1. Prediction accuracy: did the stated prediction hold? Note any mismatch.
2. Model claim: one falsifiable statement about what the target is now or is becoming.
3. Blind spot: one specific file or area this cycle did not examine, and why.

Two or three short paragraphs. No headers. No preamble. Write as a trail-entry author.
"""

# Additional reflection guidance injected per operator-configured reflect_lens.
# 'prediction', 'model_claim', and 'blind_spot' are built-in — they map to the three
# numbered items in the base prompt (no injection needed).
_REFLECT_LENS_INSTRUCTIONS: dict[str, str] = {
    "security": (
        "Also briefly note whether the applied change introduced or closed a security risk. "
        "If the blind spot area includes security-sensitive files (auth, input handling, "
        "credentials), name them explicitly."
    ),
    "overburden": (
        "Also briefly note whether the changed component now has fewer or more responsibilities "
        "than before. Is the target converging on simpler, more focused components?"
    ),
    "performance": (
        "Also briefly note any performance implications of the applied change — "
        "better or worse. If the blind spot includes performance-sensitive paths, flag them."
    ),
    "waste": (
        "Also briefly note whether the change removed dead code or unnecessary abstraction, "
        "and whether the blind spot area likely contains similar waste worth a future cycle."
    ),
}

# Built-in reflect_lenses — they correspond to the three numbered items in the base prompt.
_BUILTIN_REFLECT_LENSES = frozenset({"prediction", "model_claim", "blind_spot"})


def _build_reflect_system_prompt(lenses: list[str]) -> str:
    """Build the REFLECT system prompt, injecting guidance for operator-configured lenses.

    'prediction', 'model_claim', and 'blind_spot' are built-in — they correspond to the
    three numbered reflection items in the base prompt. No injection needed for them.
    Any other lens name in `lenses` that matches a key in _REFLECT_LENS_INSTRUCTIONS
    injects additional reflection guidance after the three numbered items.
    Unknown lens names are silently ignored (forward-compatible).

    The default config ['prediction', 'model_claim', 'blind_spot'] returns the base
    prompt unchanged — zero behavior change for existing deployments.
    """
    extras = [
        _REFLECT_LENS_INSTRUCTIONS[lens]
        for lens in lenses
        if lens not in _BUILTIN_REFLECT_LENSES and lens in _REFLECT_LENS_INSTRUCTIONS
    ]
    if not extras:
        return _BASE_REFLECT_SYSTEM

    injection = "\n\nAdditional reflection lenses (operator-configured):\n" + "\n".join(
        f"- {instruction}" for instruction in extras
    )
    # Inject after the three numbered items, before the closing style instructions
    marker = "\n\nTwo or three short paragraphs."
    return _BASE_REFLECT_SYSTEM.replace(marker, injection + marker, 1)


def reflect(
    repo: Path,
    config: AiStewardConfig,
    finding: Finding,
    diff: str,
    client: "anthropic.Anthropic | None" = None,
) -> tuple[str, int, int]:
    """Run the REFLECT phase after VERIFY passes.

    Args:
        repo: Repository root.
        config: Pipeline configuration.
        finding: The applied Finding (carries prediction and blind_spot from SCAN).
        diff: The applied diff (output of ``git diff HEAD -- <file>``).
        client: Anthropic client. If None, creates one pointing at the harness.
                Pass a mock client in tests to avoid real API calls.

    Returns:
        Tuple of (reflection_text, input_tokens, output_tokens).
        On any failure returns ("", 0, 0) — never raises.
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
            system=_build_reflect_system_prompt(config.reflect_lenses),
            messages=[{"role": "user", "content": user_content}],
        )
        try:
            _in_tok = int(message.usage.input_tokens)
            _out_tok = int(message.usage.output_tokens)
        except (AttributeError, TypeError, ValueError):
            _in_tok = 0
            _out_tok = 0
        block = message.content[0] if message.content else None
        if block is None:
            return "", _in_tok, _out_tok
        text = getattr(block, "text", "") or ""
        return text.strip(), _in_tok, _out_tok
    except Exception:
        return "", 0, 0
