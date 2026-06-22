"""Tests for REFLECT phase."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_steward.config import AiStewardConfig, ModelAssignment
from ai_steward.pipeline._types import Finding
from ai_steward.pipeline.reflect import (
    _BASE_REFLECT_SYSTEM,
    _build_reflect_system_prompt,
    reflect,
)

_V1_MODELS = ModelAssignment(
    analyze="claude-haiku-4-5",
    propose="claude-haiku-4-5",
    implement="claude-haiku-4-5",
    verify="claude-haiku-4-5",
    judge="claude-haiku-4-5",
)


def _make_config(tmp_path: Path) -> AiStewardConfig:
    return AiStewardConfig(repo=tmp_path, models=_V1_MODELS)


def _make_finding() -> Finding:
    return Finding(
        file="utils.py",
        description="Remove unused import",
        proposed_change="Delete line 3",
        rationale="os is not referenced",
        risk="low",
        prediction="The import will be gone; no runtime behaviour changes.",
        blind_spot="tests/test_utils.py — not examined for import coverage.",
    )


def _mock_client(text: str, in_tok: int = 10, out_tok: int = 5) -> MagicMock:
    """Build a mock Anthropic client that returns `text` as the message content."""
    block = MagicMock()
    block.text = text
    usage = MagicMock()
    usage.input_tokens = in_tok
    usage.output_tokens = out_tok
    message = MagicMock()
    message.content = [block]
    message.usage = usage
    client = MagicMock()
    client.messages.create.return_value = message
    return client


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_reflect_returns_string(tmp_path: Path) -> None:
    client = _mock_client("The prediction held. The target is cleaner. test_utils.py not examined.")
    text, _, _ = reflect(tmp_path, _make_config(tmp_path), _make_finding(), diff="- import os", client=client)
    assert isinstance(text, str)
    assert len(text) > 0


def test_reflect_strips_whitespace(tmp_path: Path) -> None:
    client = _mock_client("  \n\nReflection text.\n\n  ")
    text, _, _ = reflect(tmp_path, _make_config(tmp_path), _make_finding(), diff="", client=client)
    assert text == "Reflection text."


def test_reflect_returns_empty_on_api_error(tmp_path: Path) -> None:
    client = MagicMock()
    client.messages.create.side_effect = Exception("API error")
    text, in_tok, out_tok = reflect(tmp_path, _make_config(tmp_path), _make_finding(), diff="", client=client)
    assert text == ""
    assert in_tok == 0
    assert out_tok == 0


def test_reflect_returns_empty_on_empty_content(tmp_path: Path) -> None:
    message = MagicMock()
    message.content = []
    client = MagicMock()
    client.messages.create.return_value = message
    text, _, _ = reflect(tmp_path, _make_config(tmp_path), _make_finding(), diff="", client=client)
    assert text == ""


def test_reflect_returns_token_counts(tmp_path: Path) -> None:
    """reflect() returns (text, input_tokens, output_tokens) — token cost is measurable."""
    client = _mock_client("The prediction held.", in_tok=123, out_tok=45)
    _, in_tok, out_tok = reflect(tmp_path, _make_config(tmp_path), _make_finding(), diff="", client=client)
    assert in_tok == 123
    assert out_tok == 45


def test_reflect_prompt_contains_prediction_and_diff(tmp_path: Path) -> None:
    client = _mock_client("ok")
    finding = _make_finding()
    reflect(tmp_path, _make_config(tmp_path), finding, diff="- import os\n+ # removed", client=client)

    call_kwargs = client.messages.create.call_args
    user_msg = call_kwargs.kwargs["messages"][0]["content"]
    assert finding.prediction in user_msg
    assert "- import os" in user_msg


# ---------------------------------------------------------------------------
# _build_reflect_system_prompt tests
# ---------------------------------------------------------------------------


def test_build_reflect_system_prompt_default_is_base() -> None:
    """Default reflect_lenses ['prediction', 'model_claim', 'blind_spot'] -> base prompt unchanged."""
    result = _build_reflect_system_prompt(["prediction", "model_claim", "blind_spot"])
    assert result == _BASE_REFLECT_SYSTEM


def test_build_reflect_system_prompt_security_lens_injected() -> None:
    """Adding 'security' to reflect_lenses injects security reflection guidance."""
    result = _build_reflect_system_prompt(["prediction", "model_claim", "blind_spot", "security"])
    assert "security" in result.lower()
    assert "Additional reflection lenses" in result
    # Three numbered items must still be present
    assert "1. Prediction accuracy" in result
    assert "3. Blind spot" in result


def test_build_reflect_system_prompt_unknown_lens_ignored() -> None:
    """Unknown lens names are silently ignored — forward-compatible."""
    result = _build_reflect_system_prompt(["prediction", "model_claim", "blind_spot", "nonexistent_lens"])
    assert result == _BASE_REFLECT_SYSTEM
