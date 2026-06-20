"""V1 pipeline orchestrator for ai-steward.

One cycle: PRE-FLIGHT → SCAN → IMPLEMENT → VERIFY → RECORD
Stops before release: the staged change waits for operator review.

Full phase specification, gate conditions, and data types are in:
  .trail/audit-trail.md  (entry: 2026-06-19 — V1 pipeline design)
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from ai_steward.config import AiStewardConfig
from ai_steward.harness import harness_session, is_reachable
from ai_steward.pipeline._types import Finding, LoopResult
from ai_steward.pipeline._utils import run_verify_command
from ai_steward.pipeline.implement import implement
from ai_steward.pipeline.record import record
from ai_steward.pipeline.scan import scan
from ai_steward.pipeline.verify import verify


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
            trail_entry=f"PRE-FLIGHT FAILED: {reason}",
            preflight_failure=reason,
        )

    with harness_session(repo, config.harness) as harness_ctx:
        finding = scan(repo, config)
        if finding is None:
            return LoopResult(
                status="nothing_found",
                finding=None,
                diff=None,
                trail_entry="SCAN: no actionable improvement found",
            )

        ok, reason, original_size, impl_in_tok, impl_out_tok = implement(repo, config, finding)
        if not ok:
            return LoopResult(
                status="implement_failed",
                finding=finding,
                diff=None,
                trail_entry=f"IMPLEMENT FAILED: {reason}",
            )
        finding.impl_input_tokens = impl_in_tok
        finding.impl_output_tokens = impl_out_tok

    # Extract session path populated by harness_session's finally block.
    # harness_ctx is None when the session is mocked (tests) — handled gracefully.
    harness_session_path = harness_ctx["session_path"] if isinstance(harness_ctx, dict) else None

    # VERIFY and RECORD are tier-0 — outside the harness LLM context.
    diff = _get_diff(repo, finding.file)
    changed_file = repo / finding.file
    ok, reason = verify(repo, config, changed_file, original_size, baseline_count)
    if not ok:
        return LoopResult(
            status="verify_failed",
            finding=finding,
            diff=diff,
            trail_entry=f"VERIFY FAILED: {reason}",
        )

    trail_entry = record(repo, config, finding, diff, harness_session_path=harness_session_path)

    return LoopResult(
        status="proposed",
        finding=finding,
        diff=diff,
        trail_entry=trail_entry,
        harness_session_path=harness_session_path,
    )