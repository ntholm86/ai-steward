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


# ---------------------------------------------------------------------------
# cycle cost estimation
# ---------------------------------------------------------------------------


def test_cycle_cost_zero_for_nothing_found(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """nothing_found result carries zero cost (no finding, SCAN tokens untracked)."""
    _pass_preflight(monkeypatch)
    monkeypatch.setattr("ai_steward.pipeline.loop.scan", lambda *_a, **_k: None)

    result = run(tmp_path, _reachable_config(tmp_path))

    assert result.status == "nothing_found"
    assert result.cycle_cost_usd == 0.0


def test_cycle_cost_nonzero_for_proposed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """proposed result computes cost from SCAN + IMPLEMENT + REFLECT tokens."""
    _pass_preflight(monkeypatch)
    # SCAN returns 1000 input + 200 output tokens
    finding = Finding(
        file="src/foo.py",
        description="fix",
        proposed_change="x: int",
        rationale="types",
        risk="low",
        input_tokens=1000,
        output_tokens=200,
    )
    monkeypatch.setattr("ai_steward.pipeline.loop.scan", lambda *_a, **_k: finding)
    # IMPLEMENT returns 800 input + 300 output tokens
    monkeypatch.setattr("ai_steward.pipeline.loop.implement", lambda *_a, **_k: (True, "", 100, 800, 300))
    monkeypatch.setattr("ai_steward.pipeline.loop._get_diff", lambda *_a: "diff")
    monkeypatch.setattr("ai_steward.pipeline.loop.verify", lambda *_a, **_k: (True, ""))
    # REFLECT returns 400 input + 100 output tokens
    monkeypatch.setattr("ai_steward.pipeline.loop.reflect", lambda *_a, **_k: ("reflection", 400, 100))
    monkeypatch.setattr("ai_steward.pipeline.loop.record", lambda *_a, **_k: "entry")

    config = _reachable_config(tmp_path)
    result = run(tmp_path, config)

    assert result.status == "proposed"
    # total_in = 1000 + 800 + 400 = 2200; total_out = 200 + 300 + 100 = 600
    # cost = 2200 * 0.80/1e6 + 600 * 4.00/1e6 = 0.00176 + 0.0024 = 0.00416
    expected = 2200 * 0.80 / 1_000_000 + 600 * 4.00 / 1_000_000
    assert abs(result.cycle_cost_usd - expected) < 1e-9

# ---------------------------------------------------------------------------
# Review-branch batching helpers (tier-0, real git in tmp repos)
# ---------------------------------------------------------------------------


def _git(path: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=path, capture_output=True, text=True)


def _git_repo_with_commit(path: Path) -> None:
    _git_init(path)
    (path / "seed.py").write_text("x = 1\n", encoding="utf-8")
    _git(path, "add", "-A")
    _git(path, "commit", "-m", "seed")


def test_start_review_branch_creates_and_switches(tmp_path: Path) -> None:
    from ai_steward.pipeline.loop import _current_branch, _start_review_branch

    _git_repo_with_commit(tmp_path)
    branch = _start_review_branch(tmp_path, "main")

    assert branch is not None
    assert branch.startswith("ai-steward/review/")
    assert _current_branch(tmp_path) == branch
    # Base branch untouched: same commit on both
    assert _git(tmp_path, "rev-parse", "main").stdout == _git(tmp_path, "rev-parse", "HEAD").stdout


def test_commit_proposal_commits_and_leaves_tree_clean(tmp_path: Path) -> None:
    from ai_steward.pipeline.loop import _commit_proposal, _is_git_clean, _start_review_branch

    _git_repo_with_commit(tmp_path)
    _start_review_branch(tmp_path, "main")
    # Simulate a proposal: modify the tracked file and write the trail entry
    (tmp_path / "seed.py").write_text("x = 2\n", encoding="utf-8")
    (tmp_path / ".acm").mkdir()
    (tmp_path / ".acm" / "audit-trail.md").write_text("# trail\n", encoding="utf-8")
    finding = Finding(
        file="seed.py",
        description="Bump x to 2",
        proposed_change="x = 2",
        rationale="test",
        risk="low",
        prediction="passes",
        examination_summary="test",
    )

    assert _commit_proposal(tmp_path, finding, cycle=1) is True
    assert _is_git_clean(tmp_path)
    log = _git(tmp_path, "log", "-1", "--format=%B").stdout
    assert "ai-steward cycle 1: Bump x to 2" in log
    # Proposal file and trail both committed
    committed = _git(tmp_path, "show", "--name-only", "--format=", "HEAD").stdout
    assert "seed.py" in committed
    assert ".acm/audit-trail.md" in committed


def test_switch_back_returns_to_base_with_work_on_review_branch(tmp_path: Path) -> None:
    from ai_steward.pipeline.loop import (
        _commit_proposal,
        _current_branch,
        _start_review_branch,
        _switch_back,
    )

    _git_repo_with_commit(tmp_path)
    review = _start_review_branch(tmp_path, "main")
    assert review is not None
    (tmp_path / "seed.py").write_text("x = 2\n", encoding="utf-8")
    (tmp_path / ".acm").mkdir()
    (tmp_path / ".acm" / "audit-trail.md").write_text("# trail\n", encoding="utf-8")
    finding = Finding(
        file="seed.py", description="d", proposed_change="c",
        rationale="r", risk="low", prediction="p", examination_summary="e",
    )
    _commit_proposal(tmp_path, finding, cycle=1)

    assert _switch_back(tmp_path, "main") is True
    assert _current_branch(tmp_path) == "main"
    # main still has the seed content; the review branch carries the change
    assert (tmp_path / "seed.py").read_text() == "x = 1\n"
    diff = _git(tmp_path, "diff", f"main...{review}", "--", "seed.py").stdout
    assert "+x = 2" in diff


def test_current_branch_none_when_detached(tmp_path: Path) -> None:
    from ai_steward.pipeline.loop import _current_branch

    _git_repo_with_commit(tmp_path)
    sha = _git(tmp_path, "rev-parse", "HEAD").stdout.strip()
    _git(tmp_path, "checkout", sha)
    assert _current_branch(tmp_path) is None
