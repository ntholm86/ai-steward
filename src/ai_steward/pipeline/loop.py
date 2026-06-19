"""V1 pipeline orchestrator for ai-steward.

One cycle: PRE-FLIGHT → SCAN → IMPLEMENT → VERIFY → RECORD
Stops before release: the staged change waits for operator review.

Full phase specification, gate conditions, and data types are in:
  .trail/audit-trail.md  (entry: 2026-06-19 — V1 pipeline design)
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from ai_steward.config import AiStewardConfig
from ai_steward.harness import is_reachable


@dataclass
class Finding:
    """Output of the SCAN phase: one improvement worth making."""

    file: str
    description: str
    proposed_change: str
    rationale: str
    risk: Literal["low", "medium", "high"]


@dataclass
class LoopResult:
    """Outcome of one complete pipeline cycle."""

    status: Literal["proposed", "verify_failed", "nothing_found", "preflight_failed"]
    finding: Finding | None
    diff: str | None
    trail_entry: str
    preflight_failure: str | None = None


# ---------------------------------------------------------------------------
# Internal helpers (tier-0, no LLM calls)
# ---------------------------------------------------------------------------


def _is_git_repo(repo: Path) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=repo,
        capture_output=True,
    )
    return result.returncode == 0


def _is_git_clean(repo: Path) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == ""


def _baseline_tests(repo: Path) -> tuple[bool, int]:
    """Run the test suite. Returns (all_passed, pass_count)."""
    result = subprocess.run(
        ["python", "-m", "pytest", "--tb=no", "-q"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    count = 0
    for line in result.stdout.splitlines():
        if " passed" in line:
            for part in line.split():
                if part.isdigit():
                    count = int(part)
                    break
    return result.returncode == 0, count


# ---------------------------------------------------------------------------
# PRE-FLIGHT (tier 0 — all gates must pass before first LLM call)
# ---------------------------------------------------------------------------


def preflight(repo: Path, config: AiStewardConfig) -> tuple[bool, str, int]:
    """Run all tier-0 gates.

    Returns (passed, failure_reason, baseline_test_count).
    baseline_test_count is 0 when any gate fails before the test run.
    """
    if not repo.exists():
        return False, f"repo path does not exist: {repo}", 0

    if not _is_git_repo(repo):
        return False, f"not a git repository: {repo}", 0

    if not _is_git_clean(repo):
        return False, "working tree has uncommitted changes", 0

    if not is_reachable(config.harness):
        return False, f"harness proxy unreachable at {config.harness.endpoint}", 0

    passed, count = _baseline_tests(repo)
    if not passed:
        return False, "baseline tests failed — repo must be green before evolution", 0

    return True, "", count


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------


def run(repo: Path, config: AiStewardConfig) -> LoopResult:
    """Run one V1 pipeline cycle.

    PRE-FLIGHT is fully implemented.
    SCAN, IMPLEMENT, VERIFY, RECORD are built in subsequent iterations.
    """
    passed, reason, _baseline = preflight(repo, config)
    if not passed:
        return LoopResult(
            status="preflight_failed",
            finding=None,
            diff=None,
            trail_entry=f"PRE-FLIGHT FAILED: {reason}",
            preflight_failure=reason,
        )

    # SCAN → IMPLEMENT → VERIFY → RECORD
    # (see .trail/audit-trail.md 2026-06-19 for full spec)
    raise NotImplementedError("SCAN phase not yet implemented")
