"""VERIFY phase — tier 0, no LLM call.

Runs after IMPLEMENT has applied a change. All checks are structural:
  1. Python syntax check (V1: Python files only)
  2. Diff size guard (modified file must stay within 50 %–200 % of original byte size)
  3. Test suite must pass with count ≥ baseline

On any failure: rolls back the file to HEAD and returns (False, reason).
On pass: returns (True, "").

See .trail/audit-trail.md (2026-06-19 V1 Pipeline Design) for the
full spec and rationale.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from ai_steward.config import AiStewardConfig
from ai_steward.pipeline._utils import run_verify_command
from ai_steward.rollback import rollback_file


# Test-running logic extracted to _utils.py (DRY principle)


def verify(
    repo: Path,
    config: AiStewardConfig,
    changed_file: Path,
    original_size_bytes: int,
    baseline_count: int,
) -> tuple[bool, str]:
    """Verify a change is safe to stage.

    Args:
        repo: Repository root.
        config: Pipeline configuration (unused in V1 verify, reserved for V2).
        changed_file: Absolute path to the file that was modified.
        original_size_bytes: Byte size of the file before IMPLEMENT ran.
        baseline_count: Number of passing tests recorded in PRE-FLIGHT.

    Returns:
        (True, "") on pass.
        (False, reason) on failure — file is rolled back to HEAD before returning.
    """
    # Gate 1: Python syntax check
    if changed_file.suffix == ".py":
        try:
            source = changed_file.read_text(encoding="utf-8")
            compile(source, str(changed_file), "exec")
        except SyntaxError as exc:
            rollback_file(repo, changed_file)
            return False, f"syntax error in {changed_file.name}: {exc}"

    # Gate 2: Diff size guard — modified file must stay within 50 %–200 % of original.
    # Upper bound catches whole-file rewrites; lower bound catches bulk deletion.
    new_size = changed_file.stat().st_size
    if new_size > original_size_bytes * 2:
        rollback_file(repo, changed_file)
        return (
            False,
            f"{changed_file.name} grew from {original_size_bytes}B to {new_size}B "
            f"(exceeds 2× limit — likely a whole-file rewrite)",
        )
    if original_size_bytes > 0 and new_size < original_size_bytes * 0.5:
        rollback_file(repo, changed_file)
        return (
            False,
            f"{changed_file.name} shrank from {original_size_bytes}B to {new_size}B "
            f"(below 50 % of original — likely bulk deletion)",
        )

    # Gate 3: Verify command (skipped when verify_command is empty)
    if config.verify_command:
        passed, count = run_verify_command(config.verify_command, repo)
        if not passed or count < baseline_count:
            rollback_file(repo, changed_file)
            return (
                False,
                f"verify command failed or test count dropped "
                f"(baseline {baseline_count}, now {count})",
            )

    return True, ""
