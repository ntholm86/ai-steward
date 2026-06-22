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
        click.echo(f"VERIFY FAILED: {result.acm_entry}", err=True)
        sys.exit(1)
    elif result.status == "implement_failed":
        click.echo(f"IMPLEMENT FAILED: {result.acm_entry}", err=True)
        sys.exit(1)


_CONFIG_TEMPLATE = """\
models:
  analyze: claude-haiku-4-5
  propose: claude-haiku-4-5
  implement: claude-haiku-4-5
  verify: claude-haiku-4-5
  judge: claude-haiku-4-5

verify_command: python -m pytest --tb=no -q  # or: make test, npm test, etc.

# Scope — which files the agent may read and modify.
# Both lists support glob patterns (e.g. "src/**/*.py", "**/*.ts").
# Empty allowed list means all files are in scope.
# blocked is always applied after allowed.
scope:
  allowed:
    - "src/**/*.py"     # restrict to source files; remove to allow all
  blocked:
    - "tests/**"        # never modify tests
    - ".acm/**"         # never modify the evidence trail

# Token budgets — raise if the model truncates output; lower to reduce cost.
max_tokens_scan: 4096       # SCAN: 5-step reasoning needs ~4000; 1024 is too small
max_tokens_implement: 4096  # IMPLEMENT: full file rewrites can be large
max_tokens_reflect: 400     # REFLECT: concise post-cycle reflection

# Safety limits — pipeline stops when either is reached.
max_iterations: 10          # maximum improvement cycles per run
budget_usd: 5.0             # cumulative cost cap in USD

allow_dirty: false          # set true to run on repos with uncommitted changes
"""

_DESTINATION_TEMPLATE = """\
# Destination — {repo_name}

*Write what you want this codebase to become and why.
The agent reads this before every improvement cycle.*

## What this is for

<!-- Describe the purpose of this codebase in 1-3 sentences. -->

## What a good improvement looks like

<!-- What kinds of changes advance the goal? Name at least one quality bar. -->

## Constraints

<!-- Anything the agent must not touch or trade off against. -->
"""


@main.command()
@click.argument("repo", type=click.Path(), default=".")
def init(repo: str) -> None:
    """Scaffold .ai-steward.yaml and .acm/destination.md in REPO."""
    repo_path = Path(repo).resolve()
    config_file = repo_path / ".ai-steward.yaml"
    trail_dir = repo_path / ".acm"
    destination_file = trail_dir / "destination.md"

    if config_file.exists():
        click.echo(
            f".ai-steward.yaml already exists in {repo_path}. "
            "Remove it to re-initialize.",
            err=True,
        )
        sys.exit(1)

    config_file.write_text(_CONFIG_TEMPLATE, encoding="utf-8")

    trail_dir.mkdir(parents=True, exist_ok=True)
    destination_created = not destination_file.exists()
    if destination_created:
        destination_file.write_text(
            _DESTINATION_TEMPLATE.format(repo_name=repo_path.name),
            encoding="utf-8",
        )

    click.echo(f"Initialized ai-steward in {repo_path}")
    click.echo(f"  Created  .ai-steward.yaml      (model configuration)")
    if destination_created:
        click.echo(f"  Created  .acm/destination.md (edit this — it guides every cycle)")
    else:
        click.echo(f"  Skipped  .acm/destination.md (already exists)")
    click.echo("")
    click.echo("Next steps:")
    click.echo("  1. Edit .acm/destination.md — describe what you want the codebase to become")
    click.echo("  2. Set ANTHROPIC_API_KEY")
    click.echo("  3. Start llm-harness-proxy on localhost:8474")
    click.echo(f"  4. Run: ai-steward run {repo_path}")
