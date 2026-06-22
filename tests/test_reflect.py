"""Tests for REFLECT phase."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_steward.config import AiStewardConfig, ModelAssignment
from ai_steward.pipeline._types import Finding
from ai_steward.pipeline.reflect import reflect

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


def _mock_client(text: str) -> MagicMock:
    """Build a mock Anthropic client that returns `text` as the message content."""
    block = MagicMock()
    block.text = text
    message = MagicMock()
    message.content = [block]
    client = MagicMock()
    client.messages.create.return_value = message
    return client


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_reflect_returns_string(tmp_path: Path) -> None:
    client = _mock_client("The prediction held. The target is cleaner. test_utils.py not examined.")
    result = reflect(tmp_path, _make_config(tmp_path), _make_finding(), diff="- import os", client=client)
    assert isinstance(result, str)
    assert len(result) > 0


def test_reflect_strips_whitespace(tmp_path: Path) -> None:
    client = _mock_client("  \n\nReflection text.\n\n  ")
    result = reflect(tmp_path, _make_config(tmp_path), _make_finding(), diff="", client=client)
    assert result == "Reflection text."


def test_reflect_returns_empty_on_api_error(tmp_path: Path) -> None:
    client = MagicMock()
    client.messages.create.side_effect = Exception("API error")
    result = reflect(tmp_path, _make_config(tmp_path), _make_finding(), diff="", client=client)
    assert result == ""


def test_reflect_returns_empty_on_empty_content(tmp_path: Path) -> None:
    message = MagicMock()
    message.content = []
    client = MagicMock()
    client.messages.create.return_value = message
    result = reflect(tmp_path, _make_config(tmp_path), _make_finding(), diff="", client=client)
    assert result == ""


def test_reflect_prompt_contains_prediction_and_diff(tmp_path: Path) -> None:
    client = _mock_client("ok")
    finding = _make_finding()
    reflect(tmp_path, _make_config(tmp_path), finding, diff="- import os\n+ # removed", client=client)

    call_kwargs = client.messages.create.call_args
    user_msg = call_kwargs.kwargs["messages"][0]["content"]
    assert finding.prediction in user_msg
    assert "- import os" in user_msg
