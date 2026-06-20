"""IMPLEMENT phase — applies a Finding to the target repository.

One Anthropic LLM call (tier 1) via the harness proxy.
The model receives the current file contents and the Finding, and returns
the replacement file contents verbatim.

Token tier: 1 (cheap model — claude-haiku-4-5 or equivalent).
All calls route through llm-harness-proxy. Never call the Anthropic API directly.

See .trail/audit-trail.md (2026-06-19 V1 Pipeline Design) for the
full spec and rationale.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ai_steward.config import AiStewardConfig
from ai_steward.harness import anthropic_client
from ai_steward.pipeline._types import Finding

if TYPE_CHECKING:
    import anthropic


_SYSTEM_PROMPT = """\
You are a code editor. You will receive the current contents of a file and a
description of a change to make.

Return ONLY the complete new file contents — no explanation, no commentary,
no markdown code fences. The response will be written directly to disk.
"""


def implement(
    repo: Path,
    config: AiStewardConfig,
    finding: Finding,
    client: anthropic.Anthropic | None = None,
) -> tuple[bool, str, int, int, int]:
    """Apply *finding* to the target file.

    Args:
        repo: Repository root.
        config: Pipeline configuration.
        finding: The change to apply (produced by SCAN).
        client: Anthropic client. If None, creates one pointing at the harness.
                Pass a mock client in tests to avoid real API calls.

    Returns:
        ``(True, "", original_size_bytes, input_tokens, output_tokens)`` on success.
        ``(False, reason, 0, input_tokens, output_tokens)`` on any failure — file NOT modified.
        Token counts are 0 for failures that occur before the LLM call.
    """
    target = repo / finding.file
    if not target.exists():
        return False, f"target file not found: {finding.file}", 0, 0, 0

    try:
        original_bytes = target.read_bytes()
    except OSError as exc:
        return False, f"could not read {finding.file}: {exc}", 0, 0, 0

    original_size = len(original_bytes)

    try:
        original_text = original_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return False, f"file is not UTF-8: {finding.file}", 0, 0, 0

    if client is None:
        client = anthropic_client(config.harness, harness_root=repo / ".trail")

    user_message = (
        f"File: {finding.file}\n\n"
        f"Current contents:\n{original_text}\n\n"
        f"Change to make: {finding.description}\n"
        f"Details: {finding.proposed_change}\n"
        f"Rationale: {finding.rationale}\n\n"
        "Return the complete new file contents below, nothing else:"
    )

    try:
        response = client.messages.create(
            model=config.models.implement,
            max_tokens=4096,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
    except Exception as exc:  # noqa: BLE001
        return False, f"LLM call failed: {exc}", 0, 0, 0

    # Capture token usage before extracting content
    try:
        _in_tok = int(response.usage.input_tokens)
        _out_tok = int(response.usage.output_tokens)
    except (AttributeError, TypeError, ValueError):
        _in_tok = 0
        _out_tok = 0

    new_content = ""
    for block in response.content:
        if hasattr(block, "text"):
            new_content = block.text
            break

    # Strip markdown code fences if the model ignored the instruction.
    if new_content.lstrip().startswith("```"):
        lines = new_content.lstrip().splitlines()
        inner = lines[1:]
        if inner and inner[-1].strip() == "```":
            inner = inner[:-1]
        new_content = "\n".join(inner)
        if new_content and not new_content.endswith("\n"):
            new_content += "\n"

    if not new_content.strip():
        return False, "model returned empty content", 0, _in_tok, _out_tok

    try:
        target.write_text(new_content, encoding="utf-8")
    except OSError as exc:
        return False, f"could not write {finding.file}: {exc}", 0, _in_tok, _out_tok

    return True, "", original_size, _in_tok, _out_tok
