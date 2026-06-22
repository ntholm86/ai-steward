"""Tests for RECORD phase."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from ai_steward.config import AiStewardConfig, ModelAssignment
from ai_steward.pipeline import Finding
from ai_steward.pipeline.record import record

from ai_steward.pipeline.record import (
    _FALLBACK_PRICING,
    _MODEL_PRICING,
    _model_cost_per_token,
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
    assert not (tmp_path / ".acm").exists()
    record(tmp_path, _make_config(tmp_path), _make_finding(), diff="")
    assert (tmp_path / ".acm").is_dir()


def test_record_creates_audit_trail_file(tmp_path: Path) -> None:
    record(tmp_path, _make_config(tmp_path), _make_finding(), diff="")
    assert (tmp_path / ".acm" / "audit-trail.md").is_file()


def test_record_appends_not_overwrites(tmp_path: Path) -> None:
    trail_dir = tmp_path / ".acm"
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

    trail_content = (tmp_path / ".acm" / "audit-trail.md").read_text(encoding="utf-8")
    assert entry in trail_content


def test_record_entry_includes_reflection_when_present(tmp_path: Path) -> None:
    finding = _make_finding()
    finding.reflection = "The prediction held. The codebase is cleaner."
    entry = record(tmp_path, _make_config(tmp_path), finding, diff="")

    assert "**Reflection:**" in entry
    assert finding.reflection in entry


def test_record_entry_omits_reflection_section_when_empty(tmp_path: Path) -> None:
    finding = _make_finding()
    finding.reflection = ""
    entry = record(tmp_path, _make_config(tmp_path), finding, diff="")

    assert "**Reflection:**" not in entry


def test_record_entry_lists_all_harness_session_paths(tmp_path: Path) -> None:
    paths = [".acm/sessions/01ARZ.jsonl", ".acm/sessions/01BXZ.jsonl", ".acm/sessions/01CXZ.jsonl"]
    entry = record(tmp_path, _make_config(tmp_path), _make_finding(), diff="",
                   harness_session_paths=paths)

    assert "**Harness sessions:**" in entry
    for p in paths:
        assert p in entry


def test_record_entry_shows_not_captured_when_no_sessions(tmp_path: Path) -> None:
    entry = record(tmp_path, _make_config(tmp_path), _make_finding(), diff="",
                   harness_session_paths=None)

    assert "not captured" in entry


# ---------------------------------------------------------------------------
# Pricing: _model_cost_per_token contract tests
# ---------------------------------------------------------------------------


def test_model_cost_per_token_exact_match() -> None:
    """Exact base-name IDs resolve to their table entry."""
    for key, pricing in _MODEL_PRICING.items():
        assert _model_cost_per_token(key) == pricing


def test_model_cost_per_token_date_versioned_haiku() -> None:
    """Date-versioned haiku ID resolves to haiku pricing, not the fallback."""
    result = _model_cost_per_token("claude-haiku-4-5-20251001")
    assert result == _MODEL_PRICING["claude-haiku-4-5"]


def test_model_cost_per_token_date_versioned_sonnet_not_haiku_fallback() -> None:
    """Date-versioned sonnet ID resolves to sonnet pricing — not haiku fallback.

    This is the primary regression guard: before the prefix-matching fix,
    'claude-sonnet-4-5-20250514' fell through to FALLBACK_PRICING (haiku),
    underreporting sonnet cycle costs by 3.75x.
    """
    result = _model_cost_per_token("claude-sonnet-4-5-20250514")
    assert result == _MODEL_PRICING["claude-sonnet-4-5"]
    assert result != _FALLBACK_PRICING, "sonnet must not resolve to haiku fallback"


def test_model_cost_per_token_unknown_falls_back() -> None:
    """Unrecognised model IDs fall through to the haiku baseline."""
    assert _model_cost_per_token("claude-model-99-0") == _FALLBACK_PRICING


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
