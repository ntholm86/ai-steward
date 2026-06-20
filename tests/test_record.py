"""Tests for RECORD phase."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from ai_steward.config import AiStewardConfig, ModelAssignment
from ai_steward.pipeline import Finding
from ai_steward.pipeline.record import record

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


# ---------------------------------------------------------------------------
# Trail creation
# ---------------------------------------------------------------------------


def test_record_creates_trail_directory(tmp_path: Path) -> None:
    assert not (tmp_path / ".trail").exists()
    record(tmp_path, _make_config(tmp_path), _make_finding(), diff="")
    assert (tmp_path / ".trail").is_dir()


def test_record_creates_audit_trail_file(tmp_path: Path) -> None:
    record(tmp_path, _make_config(tmp_path), _make_finding(), diff="")
    assert (tmp_path / ".trail" / "audit-trail.md").is_file()


def test_record_appends_not_overwrites(tmp_path: Path) -> None:
    trail_dir = tmp_path / ".trail"
    trail_dir.mkdir()
    trail_file = trail_dir / "audit-trail.md"
    existing = "# Pre-existing trail\n\nOld entry here.\n"
    trail_file.write_text(existing, encoding="utf-8")

    record(tmp_path, _make_config(tmp_path), _make_finding(), diff="")

    content = trail_file.read_text(encoding="utf-8")
    assert content.startswith(existing), "existing trail content was overwritten"


# ---------------------------------------------------------------------------
# Entry content
# ---------------------------------------------------------------------------


def test_record_entry_contains_finding_fields(tmp_path: Path) -> None:
    finding = _make_finding()
    entry = record(tmp_path, _make_config(tmp_path), finding, diff="")

    assert finding.file in entry
    assert finding.description in entry
    assert finding.risk in entry
    assert finding.rationale in entry


def test_record_entry_contains_diff(tmp_path: Path) -> None:
    diff_text = "- import os\n+ # os removed\n"
    entry = record(tmp_path, _make_config(tmp_path), _make_finding(), diff=diff_text)

    assert diff_text in entry


def test_record_returns_entry_string_matching_file(tmp_path: Path) -> None:
    entry = record(tmp_path, _make_config(tmp_path), _make_finding(), diff="test diff")

    trail_content = (tmp_path / ".trail" / "audit-trail.md").read_text(encoding="utf-8")
    assert entry in trail_content


# ---------------------------------------------------------------------------
# Git staging
# ---------------------------------------------------------------------------


@pytest.fixture()
def git_repo(tmp_path: Path) -> Path:
    """Minimal git repo with one committed file, then the file modified."""
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=tmp_path,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=tmp_path,
        capture_output=True,
    )
    target = tmp_path / "utils.py"
    target.write_text("import os\nx = 1\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "initial"], cwd=tmp_path, capture_output=True
    )
    # Simulate what IMPLEMENT wrote
    target.write_text("x = 1\n", encoding="utf-8")
    return tmp_path


def test_record_stages_changed_file(git_repo: Path) -> None:
    record(git_repo, _make_config(git_repo), _make_finding(), diff="-import os\n x=1\n")

    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=git_repo,
        capture_output=True,
        text=True,
    )
    assert "utils.py" in result.stdout
