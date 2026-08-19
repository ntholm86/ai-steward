"""V1 pipeline orchestrator for ai-steward.

One cycle: PRE-FLIGHT → SCAN → IMPLEMENT → VERIFY → RECORD
Stops before release: the staged change waits for operator review.

Full phase specification, gate conditions, and data types are in:
  .acm/audit-trail.md  (entry: 2026-06-19 — V1 pipeline design)
"""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path

from ai_steward.config import AiStewardConfig
from ai_steward.harness import harness_session, is_reachable
from ai_steward.pipeline._types import Finding, LoopResult
from ai_steward.pipeline._utils import run_verify_command
from ai_steward.pipeline.implement import implement
from ai_steward.pipeline.record import record
from ai_steward.pipeline.reflect import reflect
from ai_steward.pipeline.scan import scan
from ai_steward.pipeline.verify import verify

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal helpers (tier-0, no LLM calls)
# ---------------------------------------------------------------------------


def _is_git_installed() -> bool:
    """Check if git is available on the system."""
    result = subprocess.run(
        ["git", "--version"],
        capture_output=True,
    )
    return result.returncode == 0


def _is_git_repo(repo: Path) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=repo,
        capture_output=True,
    )
    return result.returncode == 0


def _git_auto_init(repo: Path) -> bool:
    """Initialise a git repo with an initial commit.

    Used by PRE-FLIGHT when the target directory has no git history.
    Sets a minimal git identity so the commit succeeds in any environment.
    Returns True if all steps succeeded, False if git is unavailable.
    """
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "ai-steward",
        "GIT_AUTHOR_EMAIL": "ai-steward@local",
        "GIT_COMMITTER_NAME": "ai-steward",
        "GIT_COMMITTER_EMAIL": "ai-steward@local",
    }
    for cmd in [
        ["git", "init"],
        ["git", "add", "-A"],
        ["git", "commit", "--allow-empty", "-m", "initial commit (provisioned by ai-steward)"],
    ]:
        result = subprocess.run(cmd, cwd=repo, capture_output=True, env=env)
        if result.returncode != 0:
            return False
    return True


def _is_git_clean(repo: Path) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == ""


# ---------------------------------------------------------------------------
# Review-branch batching (tier-0)
#
# The loop's autonomy model: proposals are committed to a per-run review
# branch so the tree returns to clean and the next cycle can start. The
# operator reviews the whole batch (one branch diff) and merges or discards.
# main is never touched by the loop itself. This replaces the old behavior
# where a staged proposal left the tree dirty and PRE-FLIGHT halted the loop
# after a single cycle.
# ---------------------------------------------------------------------------

_REVIEW_AUTHOR_ENV = {
    "GIT_AUTHOR_NAME": "ai-steward",
    "GIT_AUTHOR_EMAIL": "ai-steward@local",
    "GIT_COMMITTER_NAME": "ai-steward",
    "GIT_COMMITTER_EMAIL": "ai-steward@local",
}


def _current_branch(repo: Path) -> str | None:
    """Current branch name, or None when HEAD is detached."""
    result = subprocess.run(
        ["git", "symbolic-ref", "--quiet", "--short", "HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _start_review_branch(repo: Path, base_branch: str) -> str | None:
    """Create and switch to a fresh review branch off the current HEAD.

    Branch name is unique per run: ai-steward/review/YYYYMMDD-HHMMSS.
    Returns the branch name, or None if creation/switch failed (callers
    must treat None as: continue on the base branch, old behavior).
    """
    from datetime import datetime, timezone

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    branch = f"ai-steward/review/{stamp}"
    result = subprocess.run(
        ["git", "switch", "-c", branch],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return branch


def _commit_proposal(repo: Path, finding: "Finding", cycle: int) -> bool:
    """Stage and commit the pending proposal on the current branch.

    Commits the proposal's target file plus the .acm trail artifacts the
    cycle produced, so branch diff = complete record of the loop's work.
    The commit message links the finding to its trail evidence.
    Returns True on success.
    """
    env = {**os.environ, **_REVIEW_AUTHOR_ENV}
    # Stage the proposal's target file; stage .acm artifacts only when present
    # (a repo without .acm must not fail the add — git errors on missing paths).
    add = subprocess.run(
        ["git", "add", "--", finding.file],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if add.returncode != 0:
        return False
    if (repo / ".acm").is_dir():
        subprocess.run(
            ["git", "add", "--", ".acm"],
            cwd=repo,
            capture_output=True,
            text=True,
        )
    message = (
        f"ai-steward cycle {cycle}: {finding.description}\n\n"
        f"File: {finding.file}\n"
        f"Risk: {finding.risk}\n"
        f"Prediction: {finding.prediction}\n\n"
        "Evidence: .acm/audit-trail.md (this commit) + .acm/sessions/ "
        "(hash-chained harness capture)."
    )
    commit = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=repo,
        capture_output=True,
        text=True,
        env=env,
    )
    return commit.returncode == 0


def _switch_back(repo: Path, branch: str) -> bool:
    """Return to the base branch, leaving review commits on the review branch."""
    result = subprocess.run(
        ["git", "switch", branch],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


# Test-running logic extracted to _utils.py (DRY principle)


def _estimate_cycle_cost(finding: "Finding", config: "AiStewardConfig") -> float:
    """Estimate LLM cost for one cycle from Finding token counts.

    Sums SCAN + IMPLEMENT + REFLECT tokens (input and output separately).
    nothing_found cycles return 0 because their SCAN tokens are not stored
    on Finding (finding is None in that case) — a known V1 undercount.
    """
    total_in = (
        finding.input_tokens
        + finding.impl_input_tokens
        + finding.reflect_input_tokens
    )
    total_out = (
        finding.output_tokens
        + finding.impl_output_tokens
        + finding.reflect_output_tokens
    )
    return (
        total_in * config.input_cost_per_million_tokens / 1_000_000
        + total_out * config.output_cost_per_million_tokens / 1_000_000
    )


# Test-running logic extracted to _utils.py (DRY principle)


def _get_diff(repo: Path, rel_path: str) -> str:
    """Capture unstaged diff of a file vs HEAD."""
    result = subprocess.run(
        ["git", "diff", "HEAD", "--", rel_path],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    return result.stdout


# ---------------------------------------------------------------------------
# PRE-FLIGHT (tier 0 — all gates must pass before first LLM call)
# ---------------------------------------------------------------------------


def preflight(repo: Path, config: AiStewardConfig) -> tuple[bool, str, int]:
    """Run all tier-0 gates.

    Returns (passed, failure_reason, baseline_test_count).
    baseline_test_count is 0 when any gate fails before the test run.
    """
    if not _is_git_installed():
        return False, "git is not installed — install git to proceed", 0

    if not repo.exists():
        return False, f"repo path does not exist: {repo}", 0

    if not _is_git_repo(repo):
        if not _git_auto_init(repo):
            return False, "not a git repository and git init failed — is git installed?", 0

    if not _is_git_clean(repo) and not config.allow_dirty:
        return False, "working tree has uncommitted changes", 0

    if not is_reachable(config.harness):
        return False, f"harness proxy unreachable at {config.harness.endpoint}", 0

    passed, count = run_verify_command(config.verify_command, repo)
    if not passed:
        return False, "baseline verify command failed — repo must be green before evolution", 0

    return True, "", count


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------


def run(repo: Path, config: AiStewardConfig) -> LoopResult:
    """Run one V1 pipeline cycle.

    PRE-FLIGHT → SCAN → IMPLEMENT → VERIFY → RECORD
    Stops before release: the staged change waits for operator review.
    """
    passed, reason, baseline_count = preflight(repo, config)
    if not passed:
        return LoopResult(
            status="preflight_failed",
            finding=None,
            diff=None,
            acm_entry=f"PRE-FLIGHT FAILED: {reason}",
            preflight_failure=reason,
        )

    with harness_session(repo, config.harness) as harness_ctx:
        finding = scan(repo, config)
        if finding is None:
            return LoopResult(
                status="nothing_found",
                finding=None,
                diff=None,
                acm_entry="SCAN: no actionable improvement found",
            )

        ok, reason, original_size, impl_in_tok, impl_out_tok = implement(repo, config, finding)
        finding.impl_input_tokens = impl_in_tok
        finding.impl_output_tokens = impl_out_tok
        if not ok:
            return LoopResult(
                status="implement_failed",
                finding=finding,
                diff=None,
                acm_entry=f"IMPLEMENT FAILED: {reason}",
                cycle_cost_usd=_estimate_cycle_cost(finding, config),
            )

        diff = _get_diff(repo, finding.file)
        changed_file = repo / finding.file
        ok, reason = verify(repo, config, changed_file, original_size, baseline_count)
        if not ok:
            return LoopResult(
                status="verify_failed",
                finding=finding,
                diff=diff,
                acm_entry=f"VERIFY FAILED: {reason}",
                cycle_cost_usd=_estimate_cycle_cost(finding, config),
            )

        # REFLECT is an LLM call — inside the harness context so its session
        # is captured alongside SCAN and IMPLEMENT.
        reflection, refl_in_tok, refl_out_tok = reflect(repo, config, finding, diff)
        finding.reflection = reflection
        finding.reflect_input_tokens = refl_in_tok
        finding.reflect_output_tokens = refl_out_tok

    # session_paths populated in harness_session’s finally block — contains
    # all .jsonl files created during this run (SCAN + IMPLEMENT + REFLECT).
    # harness_ctx is None when the session is mocked (tests) — handled gracefully.
    harness_session_paths = (
        harness_ctx.get("session_paths", []) if isinstance(harness_ctx, dict) else []
    )

    acm_entry = record(repo, config, finding, diff, harness_session_paths=harness_session_paths)

    return LoopResult(
        status="proposed",
        finding=finding,
        diff=diff,
        acm_entry=acm_entry,
        harness_session_paths=harness_session_paths,
        cycle_cost_usd=_estimate_cycle_cost(finding, config),
    )