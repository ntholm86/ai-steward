"""Tests for pipeline PRE-FLIGHT gates.

All gates are tier-0 (no LLM calls). Tests run without a live harness
proxy by using monkeypatch for is_reachable and _baseline_tests.
"""

import subprocess
from pathlib import Path

import pytest

from ai_steward.config import AiStewardConfig, HarnessConfig, ModelAssignment
from ai_steward.pipeline.loop import (
    Finding,
    LoopResult,
    _is_git_clean,
    _is_git_repo,
    preflight,
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


def test_is_git_clean_false_with_untracked(tmp_path: Path) -> None:
    _git_init(tmp_path)
    (tmp_path / "dirty.py").write_text("x = 1")
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


def test_preflight_fails_not_git_repo(tmp_path: Path) -> None:
    config = _reachable_config(tmp_path)
    passed, reason, count = preflight(tmp_path, config)
    assert not passed
    assert "git" in reason.lower()
    assert count == 0


def test_preflight_fails_dirty_tree(tmp_path: Path) -> None:
    _git_init(tmp_path)
    (tmp_path / "dirty.py").write_text("x = 1")
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
    monkeypatch.setattr("ai_steward.pipeline.loop._baseline_tests", lambda _: (False, 0))
    config = _reachable_config(tmp_path)
    passed, reason, count = preflight(tmp_path, config)
    assert not passed
    assert "test" in reason.lower()
    assert count == 0


# ---------------------------------------------------------------------------
# preflight — pass
# ---------------------------------------------------------------------------


def test_preflight_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _git_init(tmp_path)
    monkeypatch.setattr("ai_steward.pipeline.loop.is_reachable", lambda _: True)
    monkeypatch.setattr("ai_steward.pipeline.loop._baseline_tests", lambda _: (True, 13))
    config = _reachable_config(tmp_path)
    passed, reason, count = preflight(tmp_path, config)
    assert passed
    assert reason == ""
    assert count == 13
