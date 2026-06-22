"""CLI entry point for ai-steward."""

from __future__ import annotations

import sys
from pathlib import Path

import click
import yaml
from pydantic import ValidationError

from ai_steward.config import AiStewardConfig
from ai_steward.harness import harness_session
from ai_steward.pipeline import run as pipeline_run
from ai_steward.pipeline.reorient import reorient as reorient_phase, write_retrospect
from ai_steward.pipeline.escalate import escalate as escalate_phase, write_report as write_escalate_report
from ai_steward.pipeline.graduate import graduate as graduate_phase, write_proposal as write_graduate_proposal


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
  reflect: claude-haiku-4-5    # optional — defaults to analyze if omitted
  reorient: claude-haiku-4-5  # optional — arc-level reading; defaults to analyze

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
max_tokens_reorient: 8192   # REORIENT: arc-level reading needs large output
max_tokens_graduate: 4096   # GRADUATE: silence classification + proposal
max_tokens_escalate: 2048   # ESCALATE: focused failure diagnosis (smaller budget)

escalate_streak: 3          # auto-ESCALATE after N consecutive failures (0 disables)

# Per-token cost rates for budget_usd enforcement (dollars per 1 million tokens).
# Default matches claude-haiku-4-5 pricing. Update for your model.
# See https://www.anthropic.com/pricing for current rates.
input_cost_per_million_tokens: 0.80
output_cost_per_million_tokens: 4.00

learning_budget_chars: 5000        # chars of learning.md delivered to SCAN (tail-first; 500 was ~1 marker)

lenses:
  - mandate       # Commander's Intent check (destination.md)
  - examination   # Code structure and improvement opportunities
  # Example for security audit: add 'security' to focus on attack surface
  # Example for performance: use ['overburden'] to focus on hot paths only

# Safety limits — pipeline stops when either is reached.
max_iterations: 10          # maximum improvement cycles per run
budget_usd: 5.0             # cumulative cost cap in USD
reorient_interval: 5        # auto-REORIENT every N successful cycles (0 disables)
reorient_trail_budget_chars: 50000  # max chars from audit-trail.md for REORIENT context

allow_dirty: false          # set true to run on repos with uncommitted changes
acm_scope_depth: 4          # ACM scope traversal depth (org/workspace/team/repo hierarchies)
destination_budget_chars: 3000  # character budget for destination.md excerpts in SCAN context

# Input filtering — controls which files enter the SCAN context window.
# binary_heuristic_bytes: first N bytes read to detect binary files (NUL-byte heuristic).
# default_skip_dirs: directories excluded when scope.allowed is empty; explicit scope overrides this.
binary_heuristic_bytes: 8192
default_skip_dirs:
  - ".acm"
  - ".git"
  - ".harness"
  - "__pycache__"
  - ".mypy_cache"
  - ".pytest_cache"
  - "node_modules"
  - ".venv"
  - "venv"
  - ".tox"

sandbox: "docker"           # execution sandbox: "docker" | "local"
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


@main.command()
@click.argument("repo", type=click.Path(exists=True))
def reorient(repo: str) -> None:
    """Run arc-level trail reading and rewrite retrospect.md.

    REORIENT reads the full audit-trail.md, forms arc-claims about the target,
    and rewrites .acm/retrospect.md. This gives the pipeline fresh orientation
    for subsequent SCAN calls.

    Triggers automatically during multi-cycle runs after N successful cycles,
    after NOTHING FOUND, or after VERIFY FAILED. This command runs it manually.
    """
    repo_path = Path(repo).resolve()
    config_file = repo_path / ".ai-steward.yaml"

    if not config_file.exists():
        click.echo(
            f"No .ai-steward.yaml found in {repo_path}\n"
            "Run 'ai-steward init' first.",
            err=True,
        )
        sys.exit(1)

    try:
        data = yaml.safe_load(config_file.read_text(encoding="utf-8")) or {}
        data.pop("repo", None)
        config = AiStewardConfig(repo=repo_path, **data)
    except (ValidationError, yaml.YAMLError) as exc:
        click.echo(f"Invalid .ai-steward.yaml: {exc}", err=True)
        sys.exit(1)

    # Check if audit-trail.md exists
    trail_file = repo_path / ".acm" / "audit-trail.md"
    if not trail_file.exists():
        click.echo(
            f"No .acm/audit-trail.md found in {repo_path}\n"
            "Run at least one improvement cycle first.",
            err=True,
        )
        sys.exit(1)

    click.echo(f"REORIENT: Reading trail and forming arc-claims...")
    with harness_session(repo_path, config.harness):
        content, in_tok, out_tok = reorient_phase(repo_path, config, trigger="manual")
    retro_path = write_retrospect(repo_path, content)

    click.echo(f"REORIENT complete")
    click.echo(f"  Tokens:  {in_tok} in / {out_tok} out")
    click.echo(f"  Wrote:   {retro_path}")
    click.echo("")
    click.echo("The next SCAN will read this fresh orientation.")


@main.command("run-loop")
@click.argument("repo", type=click.Path(exists=True))
def run_loop(repo: str) -> None:
    """Run the loop until convergence (Convergence Is Silence).

    Iterates improvement cycles up to max_iterations. Triggers REORIENT
    every reorient_interval successful cycles. Stops cleanly on two
    consecutive NOTHING FOUND (convergence signal).
    """
    repo_path = Path(repo).resolve()
    config_file = repo_path / ".ai-steward.yaml"

    if not config_file.exists():
        click.echo(
            f"No .ai-steward.yaml found in {repo_path}\n"
            "Run 'ai-steward init' first.",
            err=True,
        )
        sys.exit(1)

    try:
        data = yaml.safe_load(config_file.read_text(encoding="utf-8")) or {}
        data.pop("repo", None)
        config = AiStewardConfig(repo=repo_path, **data)
    except (ValidationError, yaml.YAMLError) as exc:
        click.echo(f"Invalid .ai-steward.yaml: {exc}", err=True)
        sys.exit(1)

    nothing_found_streak = 0
    failure_streak = 0
    successful_cycles = 0
    total_cost_usd = 0.0

    if not config.allow_dirty:
        click.echo(
            "Note: allow_dirty is false — each PROPOSED cycle stages changes in git.\n"
            "      PRE-FLIGHT requires a clean tree, so the loop pauses when a change is pending.\n"
            "      Commit or discard staged changes to continue, or set allow_dirty: true to skip this gate."
        )

    for cycle in range(1, config.max_iterations + 1):
        click.echo(f"\nCycle {cycle}/{config.max_iterations}")
        result = pipeline_run(repo_path, config)

        if result.status == "preflight_failed":
            click.echo(f"PREFLIGHT FAILED: {result.preflight_failure}", err=True)
            sys.exit(1)
        elif result.status == "proposed":
            assert result.finding is not None
            nothing_found_streak = 0
            failure_streak = 0
            successful_cycles += 1
            click.echo(
                f"  PROPOSED: {result.finding.description}\n"
                f"  Staged for review."
            )
            # REORIENT trigger — fires when Nth successful cycle completes
            if (
                config.reorient_interval > 0
                and successful_cycles % config.reorient_interval == 0
            ):
                trail_file = repo_path / ".acm" / "audit-trail.md"
                if trail_file.exists():
                    click.echo(
                        f"\nREORIENT: {successful_cycles} successful cycles"
                        " — re-reading trail..."
                    )
                    with harness_session(repo_path, config.harness):
                        content, in_tok, out_tok = reorient_phase(
                            repo_path, config, trigger="auto"
                        )
                    write_retrospect(repo_path, content)
                    click.echo(f"REORIENT complete ({in_tok} in / {out_tok} out)")
        elif result.status == "nothing_found":
            nothing_found_streak += 1
            failure_streak = 0
            click.echo(f"  NOTHING FOUND (streak: {nothing_found_streak})")
            if nothing_found_streak >= 2:
                click.echo(
                    "\nConvergence: 2 consecutive NOTHING FOUND."
                )
                # GRADUATE phase — classify the silence and propose next destination
                trail_file = repo_path / ".acm" / "audit-trail.md"
                if trail_file.exists():
                    click.echo("GRADUATE: classifying silence — reading destination and trail...")
                    with harness_session(repo_path, config.harness):
                        proposal, g_in_tok, g_out_tok = graduate_phase(
                            repo_path, config, trigger=f"nothing_found_streak_{nothing_found_streak}"
                        )
                    proposal_path = write_graduate_proposal(repo_path, proposal)
                    click.echo(
                        f"GRADUATE complete ({g_in_tok} in / {g_out_tok} out)\n"
                        f"  Proposal: {proposal_path}\n"
                        f"  Review the proposal and decide: update destination, change scope, or continue."
                    )
                else:
                    click.echo("Loop complete.")
                return
        elif result.status in ("verify_failed", "implement_failed"):
            nothing_found_streak = 0
            failure_streak += 1
            click.echo(f"  {result.status.upper()}: {result.acm_entry} (failure streak: {failure_streak})")
            if config.escalate_streak > 0 and failure_streak >= config.escalate_streak:
                trail_file = repo_path / ".acm" / "audit-trail.md"
                if trail_file.exists():
                    click.echo(
                        f"\nESCALATE: {failure_streak} consecutive failures"
                        " — classifying failure pattern..."
                    )
                    with harness_session(repo_path, config.harness):
                        report, e_in_tok, e_out_tok = escalate_phase(
                            repo_path, config,
                            trigger=f"failure_streak_{failure_streak}",
                            current_error=result.acm_entry,
                        )
                    report_path = write_escalate_report(repo_path, report)
                    click.echo(
                        f"ESCALATE complete ({e_in_tok} in / {e_out_tok} out)\n"
                        f"  Report: {report_path}\n"
                        f"  Review the report and decide: fix tooling, adjust config, or update destination."
                    )
                else:
                    click.echo("Escalation limit reached. Check errors above.")
                return

        total_cost_usd += result.cycle_cost_usd
        if config.budget_usd > 0 and total_cost_usd >= config.budget_usd:
            click.echo(
                f"\nBudget limit reached: ${total_cost_usd:.4f} spent"
                f" >= ${config.budget_usd:.2f} limit. Stopping."
            )
            return

    click.echo(f"\nMax iterations ({config.max_iterations}) reached."
               f" Total cost: ${total_cost_usd:.4f}.")
