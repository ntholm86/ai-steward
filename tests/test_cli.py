"""Tests for the ai-steward CLI."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from ai_steward.cli import main
from ai_steward.pipeline._types import Finding, LoopResult


def test_init_creates_config_and_destination(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["init", str(tmp_path)])

    assert result.exit_code == 0, result.output
    config = tmp_path / ".ai-steward.yaml"
    destination = tmp_path / ".acm" / "destination.md"
    assert config.exists()
    assert destination.exists()
    assert "claude-haiku-4-5" in config.read_text()
    assert tmp_path.name in destination.read_text()
    assert "Next steps:" in result.output


def test_init_config_includes_full_tuning_surface(tmp_path: Path) -> None:
    """Generated config must expose all operator-tunable parameters.

    New adopters discover what can be configured from the generated file.
    Parameters added after the initial template (max_tokens_*, budget_usd,
    max_iterations, allow_dirty) must appear so operators don't need to
    read source code to know they exist.
    """
    runner = CliRunner()
    runner.invoke(main, ["init", str(tmp_path)])

    config_text = (tmp_path / ".ai-steward.yaml").read_text()
    for field in ("max_tokens_scan", "max_tokens_implement", "max_tokens_reflect",
                  "max_iterations", "budget_usd", "allow_dirty", "scope",
                  "binary_heuristic_bytes", "default_skip_dirs"):
        assert field in config_text, f"'{field}' missing from init config template"


def test_init_aborts_if_config_already_exists(tmp_path: Path) -> None:
    (tmp_path / ".ai-steward.yaml").write_text("existing", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["init", str(tmp_path)])

    assert result.exit_code == 1
    assert "already exists" in result.output


def test_init_skips_destination_if_already_exists(tmp_path: Path) -> None:
    trail_dir = tmp_path / ".acm"
    trail_dir.mkdir()
    existing = "# My existing destination\n"
    (trail_dir / "destination.md").write_text(existing, encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(main, ["init", str(tmp_path)])

    assert result.exit_code == 0
    assert "Skipped  .acm/destination.md" in result.output
    assert (trail_dir / "destination.md").read_text() == existing


# ---------------------------------------------------------------------------
# run-loop tests
# ---------------------------------------------------------------------------

_MINIMAL_CONFIG = """\
models:
  analyze: claude-haiku-4-5
  propose: claude-haiku-4-5
  implement: claude-haiku-4-5
  verify: claude-haiku-4-5
  judge: claude-haiku-4-5
max_iterations: 10
reorient_interval: 0
"""


def _make_finding() -> Finding:
    return Finding(
        file="src/foo.py",
        description="Add missing type annotation",
        proposed_change="def foo(x: int) -> None:",
        rationale="Improves type safety",
        risk="low",
        prediction="Tests pass",
        examination_summary="Found unannotated parameter",
    )


def test_run_loop_converges_on_nothing_found(tmp_path: Path) -> None:
    """Two consecutive NOTHING FOUND stops the loop cleanly."""
    (tmp_path / ".ai-steward.yaml").write_text(_MINIMAL_CONFIG, encoding="utf-8")
    nothing_found = LoopResult(
        status="nothing_found", finding=None, diff=None, acm_entry="SCAN: no finding"
    )
    runner = CliRunner()
    with patch("ai_steward.cli.pipeline_run", return_value=nothing_found), \
         patch("ai_steward.cli.graduate_phase", return_value=("proposal", 10, 5)), \
         patch("ai_steward.cli.write_graduate_proposal", return_value=tmp_path / ".acm" / "graduate_proposal.md"):
        result = runner.invoke(main, ["run-loop", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "Convergence" in result.output
    assert "NOTHING FOUND" in result.output


def test_run_loop_respects_max_iterations(tmp_path: Path) -> None:
    """Loop stops when max_iterations is reached without convergence."""
    config_text = _MINIMAL_CONFIG.replace("max_iterations: 10", "max_iterations: 3")
    (tmp_path / ".ai-steward.yaml").write_text(config_text, encoding="utf-8")
    proposed = LoopResult(
        status="proposed",
        finding=_make_finding(),
        diff="--- a\n+++ b\n",
        acm_entry="entry",
    )
    runner = CliRunner()
    with patch("ai_steward.cli.pipeline_run", return_value=proposed) as mock_run:
        result = runner.invoke(main, ["run-loop", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert mock_run.call_count == 3
    assert "Max iterations (3)" in result.output


def test_run_loop_exits_on_preflight_failed(tmp_path: Path) -> None:
    """Preflight failure causes exit code 1."""
    (tmp_path / ".ai-steward.yaml").write_text(_MINIMAL_CONFIG, encoding="utf-8")
    failed = LoopResult(
        status="preflight_failed",
        finding=None,
        diff=None,
        acm_entry="",
        preflight_failure="git is not installed",
    )
    runner = CliRunner()
    with patch("ai_steward.cli.pipeline_run", return_value=failed):
        result = runner.invoke(main, ["run-loop", str(tmp_path)])

    assert result.exit_code == 1
    assert "PREFLIGHT FAILED" in result.output


def test_run_loop_triggers_reorient_at_interval(tmp_path: Path) -> None:
    """REORIENT fires after reorient_interval successful cycles."""
    config_text = _MINIMAL_CONFIG.replace("reorient_interval: 0", "reorient_interval: 2")
    (tmp_path / ".ai-steward.yaml").write_text(config_text, encoding="utf-8")
    # Create audit-trail.md so the reorient trigger fires
    acm_dir = tmp_path / ".acm"
    acm_dir.mkdir()
    (acm_dir / "audit-trail.md").write_text("# Trail\n", encoding="utf-8")

    proposed = LoopResult(
        status="proposed",
        finding=_make_finding(),
        diff="--- a\n+++ b\n",
        acm_entry="entry",
    )
    nothing_found = LoopResult(
        status="nothing_found", finding=None, diff=None, acm_entry=""
    )
    # 2 proposed → REORIENT fires → 2 nothing_found → convergence → GRADUATE fires
    side_effects = [proposed, proposed, nothing_found, nothing_found]
    runner = CliRunner()
    with patch("ai_steward.cli.pipeline_run", side_effect=side_effects), \
         patch("ai_steward.cli.reorient_phase", return_value=("arc claims", 100, 50)) as mock_reorient, \
         patch("ai_steward.cli.write_retrospect", return_value=acm_dir / "retrospect.md"), \
         patch("ai_steward.cli.graduate_phase", return_value=("proposal", 200, 80)), \
         patch("ai_steward.cli.write_graduate_proposal", return_value=acm_dir / "graduate_proposal.md"):
        result = runner.invoke(main, ["run-loop", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert mock_reorient.call_count == 1
    assert "REORIENT" in result.output


def test_run_loop_escalates_on_failure_streak(tmp_path: Path) -> None:
    """Three consecutive failures trigger ESCALATE and stop the loop."""
    config_text = _MINIMAL_CONFIG + "escalate_streak: 3\n"
    (tmp_path / ".ai-steward.yaml").write_text(config_text, encoding="utf-8")
    acm_dir = tmp_path / ".acm"
    acm_dir.mkdir()
    (acm_dir / "audit-trail.md").write_text("# Trail\n", encoding="utf-8")

    verify_failed = LoopResult(
        status="verify_failed",
        finding=_make_finding(),
        diff="--- a\n+++ b\n",
        acm_entry="VERIFY FAILED: 3 test errors",
    )
    runner = CliRunner()
    with patch("ai_steward.cli.pipeline_run", return_value=verify_failed), \
         patch("ai_steward.cli.escalate_phase", return_value=("report", 100, 40)) as mock_escalate, \
         patch("ai_steward.cli.write_escalate_report", return_value=acm_dir / "escalate_report.md"):
        result = runner.invoke(main, ["run-loop", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert mock_escalate.call_count == 1
    assert "ESCALATE" in result.output


def test_run_loop_shows_allow_dirty_warning_when_false(tmp_path: Path) -> None:
    """Startup warning appears when allow_dirty is false (the default)."""
    (tmp_path / ".ai-steward.yaml").write_text(_MINIMAL_CONFIG, encoding="utf-8")
    nothing_found = LoopResult(
        status="nothing_found", finding=None, diff=None, acm_entry=""
    )
    runner = CliRunner()
    with patch("ai_steward.cli.pipeline_run", return_value=nothing_found), \
         patch("ai_steward.cli.graduate_phase", return_value=("proposal", 10, 5)), \
         patch("ai_steward.cli.write_graduate_proposal", return_value=tmp_path / ".acm" / "graduate_proposal.md"):
        result = runner.invoke(main, ["run-loop", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "allow_dirty" in result.output


def test_run_loop_no_allow_dirty_warning_when_true(tmp_path: Path) -> None:
    """No startup warning when allow_dirty is explicitly true."""
    config_text = _MINIMAL_CONFIG + "allow_dirty: true\n"
    (tmp_path / ".ai-steward.yaml").write_text(config_text, encoding="utf-8")
    nothing_found = LoopResult(
        status="nothing_found", finding=None, diff=None, acm_entry=""
    )
    runner = CliRunner()
    with patch("ai_steward.cli.pipeline_run", return_value=nothing_found), \
         patch("ai_steward.cli.graduate_phase", return_value=("proposal", 10, 5)), \
         patch("ai_steward.cli.write_graduate_proposal", return_value=tmp_path / ".acm" / "graduate_proposal.md"):
        result = runner.invoke(main, ["run-loop", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "allow_dirty" not in result.output
