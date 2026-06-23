"""Tests for llm-harness-proxy integration.

All tests run without a live harness proxy — testing the integration
contract, not the proxy itself.
"""

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ai_steward.config import HarnessConfig
from ai_steward.harness import anthropic_base_url, anthropic_client, harness_session, is_reachable


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


def test_anthropic_client_raises_outside_harness_session() -> None:
    """anthropic_client() MUST raise if called outside a harness_session() context.

    This is the explicit boundary enforcement: all LLM API calls must be
    harness-captured, no exceptions. The guard fires before any network
    activity — the error is immediate, not after a failed API call.
    """
    os.environ.pop("HARNESS_SESSION_ID", None)
    config = HarnessConfig()
    with pytest.raises(RuntimeError, match="outside a harness_session"):
        anthropic_client(config)


def test_anthropic_client_does_not_raise_inside_harness_session(tmp_path: Path) -> None:
    """anthropic_client() must not raise when HARNESS_SESSION_ID is set."""
    config = HarnessConfig()
    with harness_session(tmp_path, config):
        # We only assert no RuntimeError is raised — not that a live client works.
        try:
            anthropic_client(config)
        except RuntimeError as exc:
            raise AssertionError(f"anthropic_client raised inside harness_session: {exc}") from exc
        except Exception:
            pass  # ImportError, network error, etc — not a boundary violation


def test_harness_session_sets_harness_root(tmp_path: Path) -> None:
    config = HarnessConfig()
    os.environ.pop("HARNESS_ROOT", None)
    with harness_session(tmp_path, config):
        assert os.environ["HARNESS_ROOT"] == str(tmp_path / ".acm")
    assert "HARNESS_ROOT" not in os.environ


def test_harness_session_sets_harness_session_id(tmp_path: Path) -> None:
    config = HarnessConfig()
    os.environ.pop("HARNESS_SESSION_ID", None)
    with harness_session(tmp_path, config) as result:
        sid = os.environ.get("HARNESS_SESSION_ID")
        assert sid is not None, "HARNESS_SESSION_ID must be set during context"
        assert len(sid) == 26, "run_id must be a 26-char ULID"
        assert sid == result["run_id"], "env var and result run_id must match"
    assert "HARNESS_SESSION_ID" not in os.environ


def test_harness_session_restores_previous_value(tmp_path: Path) -> None:
    config = HarnessConfig()
    os.environ["HARNESS_ROOT"] = "/previous/value"
    with harness_session(tmp_path, config):
        assert os.environ["HARNESS_ROOT"] == str(tmp_path / ".acm")
    assert os.environ["HARNESS_ROOT"] == "/previous/value"
    del os.environ["HARNESS_ROOT"]


def test_harness_session_restores_session_id_on_exit(tmp_path: Path) -> None:
    config = HarnessConfig()
    os.environ["HARNESS_SESSION_ID"] = "PREVIOUSSESSIONIDFORTEST00"
    with harness_session(tmp_path, config):
        assert os.environ["HARNESS_SESSION_ID"] != "PREVIOUSSESSIONIDFORTEST00"
    assert os.environ["HARNESS_SESSION_ID"] == "PREVIOUSSESSIONIDFORTEST00"
    del os.environ["HARNESS_SESSION_ID"]


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
    """All .jsonl files created during the context are returned in session_paths."""
    config = HarnessConfig()
    session_id = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    with harness_session(tmp_path, config) as result:
        sessions_dir = tmp_path / ".acm" / "sessions"
        sessions_dir.mkdir(parents=True)
        (sessions_dir / f"{session_id}.jsonl").write_bytes(b'{"v":1}\n')
    assert result["session_paths"] == [f".acm/sessions/{session_id}.jsonl"]


def test_harness_session_captures_all_when_multiple_created(tmp_path: Path) -> None:
    """All new session files are captured in chronological (ULID sort) order."""
    config = HarnessConfig()
    earlier = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    later   = "01BX5ZZKBKACTAV9WEVGEMMVS0"
    with harness_session(tmp_path, config) as result:
        sessions = tmp_path / ".acm" / "sessions"
        sessions.mkdir(parents=True)
        (sessions / f"{earlier}.jsonl").write_bytes(b'{"v":1}\n')
        (sessions / f"{later}.jsonl").write_bytes(b'{"v":1}\n')
    assert result["session_paths"] == [
        f".acm/sessions/{earlier}.jsonl",
        f".acm/sessions/{later}.jsonl",
    ]


def test_harness_session_returns_empty_list_when_no_session_created(tmp_path: Path) -> None:
    """session_paths is an empty list when no new .jsonl files appear."""
    config = HarnessConfig()
    with harness_session(tmp_path, config) as result:
        pass  # harness not running — no session directory created
    assert result["session_paths"] == []


# ---------------------------------------------------------------------------
# X-Harness-Session grouping — one iteration = one file
#
# The proxy routes all calls that share an X-Harness-Session header value to
# the same <sid>.jsonl file.  ai-steward's side of the contract: every
# anthropic_client() call within one harness_session() context must send the
# context's run_id as X-Harness-Session.  When the proxy honours this header,
# one harness_session() == one session file == one pipeline iteration.
#
# Currently the proxy ignores X-Harness-Session and creates one file per LLM
# call.  These tests verify the client-side invariant and document the intended
# one-file-per-iteration shape so the contract is explicit and testable.
# ---------------------------------------------------------------------------


def test_anthropic_client_sends_run_id_as_x_harness_session(tmp_path: Path) -> None:
    """anthropic_client() must send X-Harness-Session equal to the context run_id."""
    config = HarnessConfig()
    with patch("anthropic.Anthropic") as mock_cls:
        mock_cls.return_value = MagicMock()
        with harness_session(tmp_path, config) as ctx:
            run_id = ctx["run_id"]
            anthropic_client(config, harness_root=tmp_path / ".acm")

    http_client = mock_cls.call_args.kwargs["http_client"]
    assert http_client.headers.get("x-harness-session") == run_id


def test_anthropic_client_sends_x_harness_root_from_env_without_explicit_param(
    tmp_path: Path,
) -> None:
    """X-Harness-Root is sent automatically from the HARNESS_ROOT env var.

    A call to anthropic_client(config) with no harness_root argument must still
    send X-Harness-Root — making it impossible to accidentally omit the header.
    harness_session() sets HARNESS_ROOT unconditionally; this test confirms the
    client picks it up without any explicit parameter at the call site.
    """
    config = HarnessConfig()
    with patch("anthropic.Anthropic") as mock_cls:
        mock_cls.return_value = MagicMock()
        with harness_session(tmp_path, config):
            expected_root = os.environ["HARNESS_ROOT"]
            anthropic_client(config)  # no harness_root argument

    http_client = mock_cls.call_args.kwargs["http_client"]
    assert http_client.headers.get("x-harness-root") == expected_root


def test_anthropic_client_explicit_harness_root_overrides_env(tmp_path: Path) -> None:
    """Explicit harness_root= wins over the env var (override still works)."""
    config = HarnessConfig()
    override = tmp_path / "custom" / "root"
    with patch("anthropic.Anthropic") as mock_cls:
        mock_cls.return_value = MagicMock()
        with harness_session(tmp_path, config):
            anthropic_client(config, harness_root=override)

    http_client = mock_cls.call_args.kwargs["http_client"]
    assert http_client.headers.get("x-harness-root") == str(override)


def test_all_lm_calls_in_one_iteration_share_x_harness_session(tmp_path: Path) -> None:
    """All anthropic_client() calls within one harness_session() send the same
    X-Harness-Session — the client precondition for one iteration = one file.

    SCAN, IMPLEMENT, and REFLECT each call anthropic_client().  They must all
    send the same grouping token so the proxy can route them into one file.
    """
    config = HarnessConfig()
    with patch("anthropic.Anthropic") as mock_cls:
        mock_cls.return_value = MagicMock()
        with harness_session(tmp_path, config) as ctx:
            run_id = ctx["run_id"]
            anthropic_client(config, harness_root=tmp_path / ".acm")  # SCAN
            anthropic_client(config, harness_root=tmp_path / ".acm")  # IMPLEMENT
            anthropic_client(config, harness_root=tmp_path / ".acm")  # REFLECT

    assert mock_cls.call_count == 3
    session_ids = [
        call.kwargs["http_client"].headers.get("x-harness-session")
        for call in mock_cls.call_args_list
    ]
    assert session_ids == [run_id, run_id, run_id], (
        f"All LLM calls in one iteration must share X-Harness-Session={run_id!r}. "
        f"Got: {session_ids!r}"
    )


def test_one_session_file_per_iteration_when_proxy_groups_by_run_id(tmp_path: Path) -> None:
    """When the proxy honours X-Harness-Session, one harness_session() = one .jsonl file.

    The proxy writes all calls sharing the same X-Harness-Session to
    <run_id>.jsonl.  harness_session() must report exactly one session_path
    for the iteration, not one per LLM call.

    All entries in that file share the same sid (SPEC §8.2: one file per session).
    """
    config = HarnessConfig()
    with harness_session(tmp_path, config) as ctx:
        run_id = ctx["run_id"]
        sessions_dir = tmp_path / ".acm" / "sessions"
        sessions_dir.mkdir(parents=True)
        # Simulate proxy grouping all 3 calls (SCAN+IMPLEMENT+REFLECT) into one file.
        entries = [{"sid": run_id, "seq": i, "v": 1} for i in range(3)]
        (sessions_dir / f"{run_id}.jsonl").write_text(
            "\n".join(json.dumps(e) for e in entries) + "\n",
            encoding="utf-8",
        )

    assert len(ctx["session_paths"]) == 1, (
        f"One iteration must produce exactly one session file. "
        f"Got {len(ctx['session_paths'])}: {ctx['session_paths']!r}"
    )
    assert ctx["session_paths"][0] == f".acm/sessions/{run_id}.jsonl"

    # All entries in the file share the same sid — SPEC §8.2 conformance.
    lines = (tmp_path / ".acm" / "sessions" / f"{run_id}.jsonl").read_text("utf-8").splitlines()
    unique_sids = {json.loads(l)["sid"] for l in lines if l.strip()}
    assert unique_sids == {run_id}, (
        f"Session file must contain only entries with sid={run_id!r}. Found: {unique_sids!r}"
    )
