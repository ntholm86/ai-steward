"""Tests for llm-harness-proxy integration.

All tests run without a live harness proxy — testing the integration
contract, not the proxy itself.
"""

import os
from pathlib import Path

import pytest

from ai_steward.config import HarnessConfig
from ai_steward.harness import anthropic_base_url, harness_session, is_reachable


def test_is_reachable_returns_false_when_nothing_listening() -> None:
    # Port 19999 is almost certainly unused; connection must fail cleanly.
    config = HarnessConfig(endpoint="http://127.0.0.1:19999")
    assert is_reachable(config) is False


def test_anthropic_base_url_returns_endpoint() -> None:
    config = HarnessConfig(endpoint="http://localhost:8474")
    assert anthropic_base_url(config) == "http://localhost:8474"


def test_anthropic_base_url_strips_trailing_slash() -> None:
    # HarnessConfig validator strips the slash; base_url must be clean.
    config = HarnessConfig(endpoint="http://localhost:8474/")
    assert anthropic_base_url(config) == "http://localhost:8474"


def test_harness_session_sets_harness_root(tmp_path: Path) -> None:
    config = HarnessConfig()
    os.environ.pop("HARNESS_ROOT", None)
    with harness_session(tmp_path, config):
        assert os.environ["HARNESS_ROOT"] == str(tmp_path / ".trail")
    assert "HARNESS_ROOT" not in os.environ


def test_harness_session_restores_previous_value(tmp_path: Path) -> None:
    config = HarnessConfig()
    os.environ["HARNESS_ROOT"] = "/previous/value"
    with harness_session(tmp_path, config):
        assert os.environ["HARNESS_ROOT"] == str(tmp_path / ".trail")
    assert os.environ["HARNESS_ROOT"] == "/previous/value"
    del os.environ["HARNESS_ROOT"]


def test_harness_session_restores_on_exception(tmp_path: Path) -> None:
    config = HarnessConfig()
    os.environ.pop("HARNESS_ROOT", None)
    with pytest.raises(RuntimeError):
        with harness_session(tmp_path, config):
            raise RuntimeError("pipeline failed")
    assert "HARNESS_ROOT" not in os.environ


# ---------------------------------------------------------------------------
# Session discovery
# ---------------------------------------------------------------------------


def test_harness_session_discovers_new_session(tmp_path: Path) -> None:
    """A session .jsonl file created during the context is returned as session_path."""
    config = HarnessConfig()
    session_id = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    with harness_session(tmp_path, config) as result:
        sessions_dir = tmp_path / ".trail" / "sessions"
        sessions_dir.mkdir(parents=True)
        (sessions_dir / f"{session_id}.jsonl").write_bytes(b'{"v":1}\n')
    assert result["session_path"] == f".trail/sessions/{session_id}.jsonl"


def test_harness_session_picks_latest_when_multiple_created(tmp_path: Path) -> None:
    """When multiple sessions are created, the latest ULID is chosen."""
    config = HarnessConfig()
    earlier = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    later   = "01BX5ZZKBKACTAV9WEVGEMMVS0"
    with harness_session(tmp_path, config) as result:
        sessions = tmp_path / ".trail" / "sessions"
        sessions.mkdir(parents=True)
        (sessions / f"{earlier}.jsonl").write_bytes(b'{"v":1}\n')
        (sessions / f"{later}.jsonl").write_bytes(b'{"v":1}\n')
    assert result["session_path"] == f".trail/sessions/{later}.jsonl"


def test_harness_session_returns_none_when_no_session_created(tmp_path: Path) -> None:
    """session_path is None when no new session directory appears."""
    config = HarnessConfig()
    with harness_session(tmp_path, config) as result:
        pass  # harness not running — no session directory created
    assert result["session_path"] is None
