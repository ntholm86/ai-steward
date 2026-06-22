"""Tests for the ai-steward CLI."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from ai_steward.cli import main


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
