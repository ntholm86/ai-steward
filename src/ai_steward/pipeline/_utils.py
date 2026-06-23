"""Shared utilities for the ai-steward pipeline.

Functions here are tier-0 (no LLM calls) and used by multiple phases.
"""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path


def _load_destination(repo: Path, budget_chars: int = 3000) -> str:
    """Load destination.md (or legacy vision.md), tail-truncated to budget."""
    for name in ("destination.md", "vision.md"):
        dest_file = repo / ".acm" / name
        if dest_file.exists():
            content = dest_file.read_text(encoding="utf-8")
            if len(content) > budget_chars:
                return f"[truncated to last {budget_chars} chars]\n\n" + content[-budget_chars:]
            return content
    return "[No destination.md found]"


def _load_current_retrospect(repo: Path) -> str:
    """Load current retrospect.md if it exists."""
    retro_file = repo / ".acm" / "retrospect.md"
    if not retro_file.exists():
        return "[No retrospect.md found]"
    return retro_file.read_text(encoding="utf-8")


def run_verify_command(cmd: str, repo: Path) -> tuple[bool, int]:
    """Run a configurable verify command. Returns (passed, count).

    If cmd is empty: returns (True, 0) — test gate is disabled.
    count is parsed from pytest-style output when available; 0 otherwise.

    Used by PRE-FLIGHT (baseline) and VERIFY (regression check).
    Tier-0: pure subprocess call, no LLM tokens.
    """
    if not cmd:
        return True, 0
    result = subprocess.run(
        shlex.split(cmd),
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
