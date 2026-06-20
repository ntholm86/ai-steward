"""CLI entry point for ai-steward."""

from __future__ import annotations

import sys
from pathlib import Path

import click
import yaml
from pydantic import ValidationError

from ai_steward.config import AiStewardConfig
from ai_steward.pipeline import run as pipeline_run


@click.group()
@click.version_option()
def main() -> None:
    """ai-steward: autonomous software evolution."""


@main.command()
@click.argument("repo", type=click.Path(exists=True))
def run(repo: str) -> None:
    """Run one evolution cycle against REPO."""
    repo_path = Path(repo).resolve()
    config_file = repo_path / ".ai-steward.yaml"

    if not config_file.exists():
        click.echo(
            f"No .ai-steward.yaml found in {repo_path}\n"
            "Create one to configure the pipeline. Minimum required:\n\n"
            "  models:\n"
            "    analyze: claude-haiku-4-5\n"
            "    propose: claude-haiku-4-5\n"
            "    implement: claude-haiku-4-5\n"
            "    verify: claude-haiku-4-5\n"
            "    judge: claude-haiku-4-5\n",
            err=True,
        )
        sys.exit(1)

    try:
        data = yaml.safe_load(config_file.read_text(encoding="utf-8")) or {}
        data.pop("repo", None)  # repo comes from the CLI arg, not the config file
        config = AiStewardConfig(repo=repo_path, **data)
    except (ValidationError, yaml.YAMLError) as exc:
        click.echo(f"Invalid .ai-steward.yaml: {exc}", err=True)
        sys.exit(1)

    result = pipeline_run(repo_path, config)

    if result.status == "proposed":
        assert result.finding is not None
        f = result.finding
        click.echo(
            f"PROPOSED\n"
            f"  File:   {f.file}\n"
            f"  Change: {f.description}\n"
            f"  Risk:   {f.risk}\n\n"
            f"Staged for review. Inspect with:\n"
            f"  git -C {repo_path} diff --cached"
        )
    elif result.status == "nothing_found":
        click.echo("NOTHING FOUND — no actionable improvement identified.")
    elif result.status == "preflight_failed":
        click.echo(f"PREFLIGHT FAILED: {result.preflight_failure}", err=True)
        sys.exit(1)
    elif result.status == "verify_failed":
        click.echo(f"VERIFY FAILED: {result.trail_entry}", err=True)
        sys.exit(1)
    elif result.status == "implement_failed":
        click.echo(f"IMPLEMENT FAILED: {result.trail_entry}", err=True)
        sys.exit(1)
