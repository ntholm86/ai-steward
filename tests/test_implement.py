"""Tests for IMPLEMENT phase.

All tests use a mock Anthropic client — no real LLM calls, no anthropic
package required to run the suite.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_steward.config import AiStewardConfig, ModelAssignment
from ai_steward.pipeline import Finding
from ai_steward.pipeline.implement import implement

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_V1_MODELS = ModelAssignment(
    analyze="claude-haiku-4-5",
    propose="claude-haiku-4-5",
    implement="claude-haiku-4-5",
    verify="claude-haiku-4-5",
    judge="claude-haiku-4-5",
)


def _make_config(tmp_path: Path) -> AiStewardConfig:
    return AiStewardConfig(repo=tmp_path, models=_V1_MODELS)


def _make_finding(file: str = "utils.py") -> Finding:
    return Finding(
        file=file,
        description="Remove unused import os",
        proposed_change="import sys\n\nx = 1\n",
        rationale="os is not referenced",
        risk="low",
    )


def _mock_client(response_text: str, input_tokens: int = 0, output_tokens: int = 0) -> MagicMock:
    """Mock Anthropic client that returns a fixed text response."""
    block = MagicMock()
    block.text = response_text
    message = MagicMock()
    message.content = [block]
    message.usage.input_tokens = input_tokens
    message.usage.output_tokens = output_tokens
    client = MagicMock()
    client.messages.create.return_value = message
    return client


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_implement_writes_content_and_returns_true(tmp_path: Path) -> None:
    (tmp_path / "utils.py").write_text("import os\nimport sys\n\nx = 1\n")
    config = _make_config(tmp_path)
    new_content = "import sys\n\nx = 1\n"
    client = _mock_client(new_content)

    ok, *_ = implement(tmp_path, config, _make_finding(), client=client)

    assert ok is True
    assert (tmp_path / "utils.py").read_text(encoding="utf-8") == new_content


def test_implement_returns_original_size_bytes(tmp_path: Path) -> None:
    # Write bytes explicitly to avoid Windows CRLF expansion changing the size.
    original = b"import os\nimport sys\n\nx = 1\n"
    (tmp_path / "utils.py").write_bytes(original)
    config = _make_config(tmp_path)
    client = _mock_client("import sys\n\nx = 1\n")

    _, _, original_size, *_ = implement(tmp_path, config, _make_finding(), client=client)

    assert original_size == len(original)


def test_implement_strips_markdown_fences(tmp_path: Path) -> None:
    (tmp_path / "utils.py").write_text("import os\nx = 1\n")
    config = _make_config(tmp_path)
    client = _mock_client("```python\nimport sys\nx = 1\n```")

    ok, *_ = implement(tmp_path, config, _make_finding(), client=client)

    assert ok is True
    written = (tmp_path / "utils.py").read_text(encoding="utf-8")
    assert "```" not in written
    assert "import sys" in written


def test_implement_returns_false_if_file_missing(tmp_path: Path) -> None:
    config = _make_config(tmp_path)
    finding = _make_finding(file="no_such_file.py")
    client = _mock_client("x = 1\n")

    ok, reason, size, *_ = implement(tmp_path, config, finding, client=client)

    assert ok is False
    assert "not found" in reason
    assert size == 0


def test_implement_returns_false_on_empty_response(tmp_path: Path) -> None:
    original = "x = 1\n"
    (tmp_path / "utils.py").write_text(original)
    config = _make_config(tmp_path)
    client = _mock_client("   ")

    ok, reason, size, *_ = implement(tmp_path, config, _make_finding(), client=client)

    assert ok is False
    assert "empty" in reason
    assert size == 0
    assert (tmp_path / "utils.py").read_text(encoding="utf-8") == original


def test_implement_returns_false_on_llm_exception(tmp_path: Path) -> None:
    original = "x = 1\n"
    (tmp_path / "utils.py").write_text(original)
    config = _make_config(tmp_path)
    client = MagicMock()
    client.messages.create.side_effect = RuntimeError("connection refused")

    ok, reason, size, *_ = implement(tmp_path, config, _make_finding(), client=client)

    assert ok is False
    assert "LLM call failed" in reason
    assert size == 0
    assert (tmp_path / "utils.py").read_text(encoding="utf-8") == original


def test_implement_returns_false_for_non_utf8_file(tmp_path: Path) -> None:
    (tmp_path / "data.bin").write_bytes(b"\xff\xfe\x00binary_data")
    config = _make_config(tmp_path)
    finding = _make_finding(file="data.bin")
    client = _mock_client("new content\n")

    ok, reason, size, *_ = implement(tmp_path, config, finding, client=client)

    assert ok is False
    assert "UTF-8" in reason
    assert size == 0
