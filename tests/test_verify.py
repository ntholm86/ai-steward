"""Tests for VERIFY phase and rollback utility."""

import subprocess
from pathlib import Path

import pytest

from ai_steward.config import AiStewardConfig, HarnessConfig, ModelAssignment
from ai_steward.pipeline.verify import verify
from ai_steward.rollback import rollback_file

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


def _git_repo_with_file(tmp_path: Path, filename: str, content: str) -> Path:
    """Create a git repo, write a file, commit it, return the file path."""
    subprocess.run(["git", "init", "-b", "main"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=tmp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "T"], cwd=tmp_path, capture_output=True)
    f = tmp_path / filename
    f.write_text(content, encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True, capture_output=True)
    return f


# ---------------------------------------------------------------------------
# rollback_file
# ---------------------------------------------------------------------------


def test_rollback_restores_committed_content(tmp_path: Path) -> None:
    f = _git_repo_with_file(tmp_path, "foo.py", "x = 1\n")
    f.write_text("x = MODIFIED\n", encoding="utf-8")
    assert f.read_text() == "x = MODIFIED\n"
    rollback_file(tmp_path, f)
    assert f.read_text() == "x = 1\n"


def test_rollback_works_with_relative_path(tmp_path: Path) -> None:
    f = _git_repo_with_file(tmp_path, "bar.py", "y = 2\n")
    f.write_text("y = CHANGED\n", encoding="utf-8")
    rollback_file(tmp_path, Path("bar.py"))  # relative path
    assert f.read_text() == "y = 2\n"


# ---------------------------------------------------------------------------
# verify — failure paths (all should rollback the file)
# ---------------------------------------------------------------------------


def test_verify_fails_syntax_error_and_rolls_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = _git_repo_with_file(tmp_path, "mod.py", "x = 1\n")
    original_size = f.stat().st_size
    f.write_text("def broken(\n", encoding="utf-8")  # syntax error
    monkeypatch.setattr("ai_steward.pipeline.verify.run_tests", lambda _: (True, 5))
    config = _make_config(tmp_path)

    passed, reason = verify(tmp_path, config, f, original_size, 5)

    assert not passed
    assert "syntax" in reason.lower()
    assert f.read_text() == "x = 1\n"  # rolled back


def test_verify_fails_file_too_large_and_rolls_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = _git_repo_with_file(tmp_path, "mod.py", "x = 1\n")
    original_size = f.stat().st_size
    f.write_text("x = 1\n" * 1000, encoding="utf-8")  # way bigger than 2×
    monkeypatch.setattr("ai_steward.pipeline.verify.run_tests", lambda _: (True, 5))
    config = _make_config(tmp_path)

    passed, reason = verify(tmp_path, config, f, original_size, 5)

    assert not passed
    assert "2×" in reason or "limit" in reason
    assert f.read_text() == "x = 1\n"  # rolled back


def test_verify_fails_tests_fail_and_rolls_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = _git_repo_with_file(tmp_path, "mod.py", "x = 1\n")
    original_size = f.stat().st_size
    f.write_text("x = 2\n", encoding="utf-8")
    monkeypatch.setattr("ai_steward.pipeline.verify.run_tests", lambda _: (False, 0))
    config = _make_config(tmp_path)

    passed, reason = verify(tmp_path, config, f, original_size, 5)

    assert not passed
    assert "test" in reason.lower()
    assert f.read_text() == "x = 1\n"  # rolled back


def test_verify_fails_when_test_count_drops(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = _git_repo_with_file(tmp_path, "mod.py", "x = 1\n")
    original_size = f.stat().st_size
    f.write_text("x = 2\n", encoding="utf-8")
    # pytest exits 0 but fewer tests pass (some were deleted)
    monkeypatch.setattr("ai_steward.pipeline.verify.run_tests", lambda _: (True, 3))
    config = _make_config(tmp_path)

    passed, reason = verify(tmp_path, config, f, original_size, baseline_count=5)

    assert not passed
    assert "baseline" in reason or "3" in reason


# ---------------------------------------------------------------------------
# verify — pass
# ---------------------------------------------------------------------------


def test_verify_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    f = _git_repo_with_file(tmp_path, "mod.py", "x = 1\n")
    original_size = f.stat().st_size
    f.write_text("x = 2\n", encoding="utf-8")  # same size — stays within 2× guard
    monkeypatch.setattr("ai_steward.pipeline.verify.run_tests", lambda _: (True, 7))
    config = _make_config(tmp_path)

    passed, reason = verify(tmp_path, config, f, original_size, baseline_count=7)

    assert passed
    assert reason == ""
    assert f.read_text() == "x = 2\n"  # not rolled back


def test_verify_skips_syntax_check_for_non_python(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    f = _git_repo_with_file(tmp_path, "notes.md", "# hello\n")
    original_size = f.stat().st_size
    f.write_text("# world\n", encoding="utf-8")  # same size — no syntax gate for .md
    monkeypatch.setattr("ai_steward.pipeline.verify.run_tests", lambda _: (True, 3))
    config = _make_config(tmp_path)

    passed, reason = verify(tmp_path, config, f, original_size, baseline_count=3)

    assert passed  # no syntax check for .md
