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


def _load_current_orientation(repo: Path) -> str:
    """Load current orientation.md if it exists."""
    orientation_file = repo / ".acm" / "orientation.md"
    if not orientation_file.exists():
        return "[No orientation.md found]"
    return orientation_file.read_text(encoding="utf-8")


def _load_learning(repo: Path, budget_chars: int = 20000) -> str:
    """Load learning.md — the pre-extracted [!REALIZATION]/[!REVERSAL] surface.

    learning.md is the compact chronological digest of every marker across the
    full trail. It is the pre-digested pattern surface: reading it alongside
    the raw trail gives the model both the extracted conclusions and their
    original context. Budget takes the tail (newest markers last).
    """
    learning_file = repo / ".acm" / "learning.md"
    if not learning_file.exists():
        return "[No learning.md found — run record.py learning --write to generate it]"
    content = learning_file.read_text(encoding="utf-8")
    if len(content) > budget_chars:
        return f"[truncated to last {budget_chars} chars]\n\n" + content[-budget_chars:]
    return content


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
