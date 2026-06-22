"""Tests for pipeline PRE-FLIGHT gates.

All gates are tier-0 (no LLM calls). Tests run without a live harness
proxy by using monkeypatch for is_reachable and run_tests.
"""

import os
import subprocess
from pathlib import Path

import pytest

from ai_steward.config import AiStewardConfig, HarnessConfig, ModelAssignment
from ai_steward.pipeline import Finding, LoopResult
from ai_steward.pipeline.loop import (
    _is_git_clean,
    _is_git_repo,
    preflight,
    run,
)

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


def _git_init(path: Path) -> None:
    subprocess.run(["git", "init", "-b", "main"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, capture_output=True)


def _reachable_config(tmp_path: Path) -> AiStewardConfig:
    """Config with an explicitly unreachable harness — use monkeypatch to override."""
    return AiStewardConfig(
        repo=tmp_path,
        models=_V1_MODELS,
        harness=HarnessConfig(endpoint="http://127.0.0.1:19999"),
    )


# ---------------------------------------------------------------------------
# _is_git_repo
# ---------------------------------------------------------------------------


def test_is_git_repo_true(tmp_path: Path) -> None:
    _git_init(tmp_path)
    assert _is_git_repo(tmp_path) is True


def test_is_git_repo_false(tmp_path: Path) -> None:
    assert _is_git_repo(tmp_path) is False


# ---------------------------------------------------------------------------
# _is_git_clean
# ---------------------------------------------------------------------------


def test_is_git_clean_empty_repo(tmp_path: Path) -> None:
    _git_init(tmp_path)
    assert _is_git_clean(tmp_path) is True


def test_is_git_clean_ignores_untracked(tmp_path: Path) -> None:
    _git_init(tmp_path)
    (tmp_path / "untracked.py").write_text("x = 1")
    # Untracked files are not committed changes — must not block the pipeline.
    assert _is_git_clean(tmp_path) is True


def test_is_git_clean_false_with_modified_tracked(tmp_path: Path) -> None:
    _git_init(tmp_path)
    f = tmp_path / "tracked.py"
    f.write_bytes(b"x = 1\n")
    subprocess.run(["git", "add", "tracked.py"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    f.write_bytes(b"x = 2\n")
    assert _is_git_clean(tmp_path) is False


# ---------------------------------------------------------------------------
# preflight — failure gates (in order)
# ---------------------------------------------------------------------------


def test_preflight_fails_path_not_exist(tmp_path: Path) -> None:
    nonexistent = tmp_path / "no_such_dir"
    config = _reachable_config(tmp_path)
    passed, reason, count = preflight(nonexistent, config)
    assert not passed
    assert "does not exist" in reason
    assert count == 0


def test_preflight_auto_inits_git_if_not_repo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # No git repo — preflight should auto-init and then pass all remaining gates.
    monkeypatch.setattr("ai_steward.pipeline.loop.is_reachable", lambda _: True)
    monkeypatch.setattr("ai_steward.pipeline.loop.run_verify_command", lambda cmd, repo: (True, 0))
    config = _reachable_config(tmp_path)
    passed, reason, count = preflight(tmp_path, config)
    assert passed
    assert (tmp_path / ".git").exists()  # git was provisioned


def test_preflight_fails_dirty_tree(tmp_path: Path) -> None:
    _git_init(tmp_path)
    # A tracked file with uncommitted modifications makes the tree dirty.
    f = tmp_path / "tracked.py"
    f.write_bytes(b"x = 1\n")
    subprocess.run(["git", "add", "tracked.py"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    f.write_bytes(b"x = 2\n")
    config = _reachable_config(tmp_path)
    passed, reason, count = preflight(tmp_path, config)
    assert not passed
    assert "uncommitted" in reason
    assert count == 0


def test_preflight_fails_harness_unreachable(tmp_path: Path) -> None:
    _git_init(tmp_path)
    # Port 19999 is explicitly unreachable — no monkeypatch needed.
    config = _reachable_config(tmp_path)
    passed, reason, count = preflight(tmp_path, config)
    assert not passed
    assert "harness" in reason.lower()
    assert count == 0


def test_preflight_fails_baseline_tests(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _git_init(tmp_path)
    monkeypatch.setattr("ai_steward.pipeline.loop.is_reachable", lambda _: True)
    monkeypatch.setattr("ai_steward.pipeline.loop.run_verify_command", lambda cmd, repo: (False, 0))
    config = _reachable_config(tmp_path)
    passed, reason, count = preflight(tmp_path, config)
    assert not passed
    assert "verify" in reason.lower() or "green" in reason.lower()
    assert count == 0


# ---------------------------------------------------------------------------
# preflight — pass
# ---------------------------------------------------------------------------


def test_preflight_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _git_init(tmp_path)
    monkeypatch.setattr("ai_steward.pipeline.loop.is_reachable", lambda _: True)
    monkeypatch.setattr("ai_steward.pipeline.loop.run_verify_command", lambda cmd, repo: (True, 13))
    config = _reachable_config(tmp_path)
    passed, reason, count = preflight(tmp_path, config)
    assert passed
    assert reason == ""
    assert count == 13


def test_preflight_dirty_tree_passes_when_allow_dirty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _git_init(tmp_path)
    (tmp_path / "wip.py").write_text("x = 1")  # dirty working tree
    config = AiStewardConfig(
        repo=tmp_path,
        models=_V1_MODELS,
        harness=HarnessConfig(endpoint="http://127.0.0.1:19999"),
        allow_dirty=True,
    )
    monkeypatch.setattr("ai_steward.pipeline.loop.is_reachable", lambda _: True)
    monkeypatch.setattr("ai_steward.pipeline.loop.run_verify_command", lambda cmd, repo: (True, 5))

    passed, reason, count = preflight(tmp_path, config)

    assert passed
    assert reason == ""
    assert count == 5


# ---------------------------------------------------------------------------
# run() — full pipeline (all phases mocked to isolate loop logic)
# ---------------------------------------------------------------------------

import contextlib

import ai_steward.harness

_FINDING = Finding(
    file="f.py",
    description="Remove unused import",
    proposed_change="x = 1\n",
    rationale="unused",
    risk="low",
)


def _pass_preflight(monkeypatch: pytest.MonkeyPatch, baseline: int = 5) -> None:
    monkeypatch.setattr("ai_steward.pipeline.loop._is_git_repo", lambda _r: True)
    monkeypatch.setattr("ai_steward.pipeline.loop._is_git_clean", lambda _r: True)
    monkeypatch.setattr("ai_steward.pipeline.loop.run_verify_command", lambda cmd, repo: (True, baseline))
    monkeypatch.setattr("ai_steward.pipeline.loop.is_reachable", lambda _c: True)
    monkeypatch.setattr(ai_steward.harness, "harness_session", lambda *_a: contextlib.nullcontext())


def test_run_nothing_found(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _pass_preflight(monkeypatch)
    monkeypatch.setattr("ai_steward.pipeline.loop.scan", lambda *_a, **_k: None)
    monkeypatch.setattr("ai_steward.pipeline.loop._get_diff", lambda *_a: "")

    result = run(tmp_path, _reachable_config(tmp_path))

    assert result.status == "nothing_found"
    assert result.finding is None


def test_run_implement_failed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _pass_preflight(monkeypatch)
    monkeypatch.setattr("ai_steward.pipeline.loop.scan", lambda *_a, **_k: _FINDING)
    monkeypatch.setattr("ai_steward.pipeline.loop.implement", lambda *_a, **_k: (False, "model returned empty content", 0, 0, 0))
    monkeypatch.setattr("ai_steward.pipeline.loop._get_diff", lambda *_a: "")

    result = run(tmp_path, _reachable_config(tmp_path))

    assert result.status == "implement_failed"
    assert result.finding is _FINDING


def test_run_verify_failed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _pass_preflight(monkeypatch)
    monkeypatch.setattr("ai_steward.pipeline.loop.scan", lambda *_a, **_k: _FINDING)
    monkeypatch.setattr("ai_steward.pipeline.loop.implement", lambda *_a, **_k: (True, "", 100, 0, 0))
    monkeypatch.setattr("ai_steward.pipeline.loop._get_diff", lambda *_a: "diff text")
    monkeypatch.setattr("ai_steward.pipeline.loop.verify", lambda *_a, **_k: (False, "syntax error"))

    result = run(tmp_path, _reachable_config(tmp_path))

    assert result.status == "verify_failed"
    assert result.diff == "diff text"


def test_run_proposed_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _pass_preflight(monkeypatch)
    monkeypatch.setattr("ai_steward.pipeline.loop.scan", lambda *_a, **_k: _FINDING)
    monkeypatch.setattr("ai_steward.pipeline.loop.implement", lambda *_a, **_k: (True, "", 100, 0, 0))
    monkeypatch.setattr("ai_steward.pipeline.loop._get_diff", lambda *_a: "diff text")
    monkeypatch.setattr("ai_steward.pipeline.loop.verify", lambda *_a, **_k: (True, ""))
    monkeypatch.setattr("ai_steward.pipeline.loop.reflect", lambda *_a, **_k: ("reflection text", 0, 0))
    monkeypatch.setattr("ai_steward.pipeline.loop.record", lambda *_a, **_k: "trail entry")

    result = run(tmp_path, _reachable_config(tmp_path))

    assert result.status == "proposed"
    assert result.finding is _FINDING
    assert result.diff == "diff text"
    assert result.acm_entry == "trail entry"
