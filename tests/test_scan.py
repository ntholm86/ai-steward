"""Tests for SCAN phase.

All tests use a mock Anthropic client — no real LLM calls, no anthropic
package required to run the suite.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_steward.config import AiStewardConfig, ModelAssignment, ScopeConfig
from ai_steward.pipeline import Finding
from ai_steward.pipeline.scan import _collect_files, scan

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


def _make_config(tmp_path: Path, scope: ScopeConfig | None = None) -> AiStewardConfig:
    return AiStewardConfig(
        repo=tmp_path,
        models=_V1_MODELS,
        scope=scope or ScopeConfig(),
    )


def _mock_client(response: dict, input_tokens: int = 0, output_tokens: int = 0) -> MagicMock:
    """Mock Anthropic client that returns a fixed JSON response."""
    block = MagicMock()
    block.text = json.dumps(response)
    message = MagicMock()
    message.content = [block]
    message.usage.input_tokens = input_tokens
    message.usage.output_tokens = output_tokens
    client = MagicMock()
    client.messages.create.return_value = message
    return client


# ---------------------------------------------------------------------------
# scan — valid finding
# ---------------------------------------------------------------------------


def test_scan_returns_finding_on_valid_response(tmp_path: Path) -> None:
    (tmp_path / "utils.py").write_text("import os\nimport sys\n\nx = 1\n")
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "Remove unused import os",
        "proposed_change": "import sys\n\nx = 1\n",
        "rationale": "os is not referenced anywhere in the module",
        "risk": "low",
    })

    result = scan(tmp_path, config, client=client)

    assert isinstance(result, Finding)
    assert result.file == "utils.py"
    assert result.risk == "low"
    assert result.blind_spot == ""
    client.messages.create.assert_called_once()


def test_scan_extracts_blind_spot_when_present(tmp_path: Path) -> None:
    (tmp_path / "utils.py").write_text("import os\n\nx = 1\n")
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "Remove unused import os",
        "proposed_change": "Remove the import os line",
        "rationale": "os is not referenced",
        "risk": "low",
        "blind_spot": "Did not examine test files for os usage",
    })

    result = scan(tmp_path, config, client=client)

    assert isinstance(result, Finding)
    assert result.blind_spot == "Did not examine test files for os usage"


# ---------------------------------------------------------------------------
# scan — None paths
# ---------------------------------------------------------------------------


def test_scan_returns_none_when_model_says_nothing(tmp_path: Path) -> None:
    (tmp_path / "clean.py").write_text("x = 1\n")
    config = _make_config(tmp_path)

    result = scan(tmp_path, config, client=_mock_client({"nothing": True}))

    assert result is None


def test_scan_returns_none_on_invalid_json(tmp_path: Path) -> None:
    (tmp_path / "f.py").write_text("x = 1\n")
    config = _make_config(tmp_path)
    block = MagicMock()
    block.text = "sorry, here is my answer in prose"
    message = MagicMock()
    message.content = [block]
    client = MagicMock()
    client.messages.create.return_value = message

    result = scan(tmp_path, config, client=client)

    assert result is None


def test_scan_skips_high_risk_finding(tmp_path: Path) -> None:
    (tmp_path / "core.py").write_text("x = 1\n")
    config = _make_config(tmp_path)

    result = scan(tmp_path, config, client=_mock_client({
        "file": "core.py",
        "description": "Rewrite the module",
        "proposed_change": "# everything rewritten",
        "rationale": "cleaner",
        "risk": "high",
    }))

    assert result is None


def test_scan_returns_none_if_file_not_in_repo(tmp_path: Path) -> None:
    (tmp_path / "real.py").write_text("x = 1\n")
    config = _make_config(tmp_path)

    result = scan(tmp_path, config, client=_mock_client({
        "file": "nonexistent.py",
        "description": "Fix something",
        "proposed_change": "x = 2",
        "rationale": "better",
        "risk": "low",
    }))

    assert result is None


def test_scan_returns_none_if_no_files_in_scope(tmp_path: Path) -> None:
    # No .py files — _collect_files returns empty dict, no LLM call made.
    config = _make_config(tmp_path)
    client = MagicMock()

    result = scan(tmp_path, config, client=client)

    assert result is None
    client.messages.create.assert_not_called()


# ---------------------------------------------------------------------------
# _collect_files
# ---------------------------------------------------------------------------


def test_collect_files_respects_blocked(tmp_path: Path) -> None:
    (tmp_path / "keep.py").write_text("x = 1")
    (tmp_path / "skip.py").write_text("y = 2")
    config = _make_config(
        tmp_path,
        scope=ScopeConfig(allowed=["**/*.py"], blocked=["skip.py"]),
    )

    files = _collect_files(tmp_path, config)

    assert "keep.py" in files
    assert "skip.py" not in files


# ---------------------------------------------------------------------------
# Directed SCAN — Commander's Intent injection
# ---------------------------------------------------------------------------


def test_scan_includes_destination_when_present(tmp_path: Path) -> None:
    """SCAN prompt must include destination content when .trail/destination.md exists."""
    (tmp_path / "utils.py").write_text("import os\nx = 1\n")
    (tmp_path / ".trail").mkdir()
    (tmp_path / ".trail" / "destination.md").write_text(
        "# Destination\nBuild a fast reliable pipeline.", encoding="utf-8"
    )
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "Remove unused import",
        "proposed_change": "Remove the import os line.",
        "rationale": "unused",
        "risk": "low",
    })

    scan(tmp_path, config, client=client)

    call_kwargs = client.messages.create.call_args
    user_content = call_kwargs[1]["messages"][0]["content"]
    assert "Commander's Intent" in user_content
    assert "Build a fast reliable pipeline." in user_content


def test_scan_works_without_destination(tmp_path: Path) -> None:
    """SCAN falls back gracefully when no destination.md exists."""
    (tmp_path / "utils.py").write_text("import os\nx = 1\n")
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "Remove unused import",
        "proposed_change": "Remove import os.",
        "rationale": "unused",
        "risk": "low",
    })

    result = scan(tmp_path, config, client=client)

    assert isinstance(result, Finding)
    call_kwargs = client.messages.create.call_args
    user_content = call_kwargs[1]["messages"][0]["content"]
    assert "Commander's Intent" not in user_content


def test_scan_truncates_long_destination(tmp_path: Path) -> None:
    """Destination takes the tail when over budget — most recent content is preserved."""
    (tmp_path / "utils.py").write_text("x = 1\n")
    (tmp_path / ".trail").mkdir()
    # Old content at start, new content at end — truncation must preserve the end.
    old_content = "OLD: " + "A" * 2000
    new_content = "NEW: latest operator decision"
    long_text = old_content + "B" * 1000 + new_content
    (tmp_path / ".trail" / "destination.md").write_bytes(long_text.encode("utf-8"))
    config = _make_config(tmp_path)
    client = _mock_client({"nothing": True})

    scan(tmp_path, config, client=client)

    call_kwargs = client.messages.create.call_args
    user_content = call_kwargs[1]["messages"][0]["content"]
    assert "truncated for token budget" in user_content
    assert "NEW: latest operator decision" in user_content
    assert "OLD: " + "A" * 2000 not in user_content
