"""Shared utilities for the ai-steward pipeline.

Functions here are tier-0 (no LLM calls) and used by multiple phases.
"""

from __future__ import annotations

import re
import shlex
import subprocess
from pathlib import Path

_BOUNDED_DESTINATION_START = "<!-- current-destination: complete -->"
_BOUNDED_DESTINATION_END = "<!-- destination-history -->"


def _extract_bounded_destination(text: str) -> str | None:
    """Extract the bounded current mandate from a destination.md, if marked.

    When a destination contains the exact markers
    <!-- current-destination: complete --> and <!-- destination-history -->
    in that order, the content between them is the operator-confirmed current
    mandate (the skills-suite bounded-read convention). That bounded section
    is small and authoritative; the dated history below the end marker is
    provenance, not active instruction -- tail-truncation into it would
    deliver superseded sections and miss the mandate entirely.
    """
    start = text.find(_BOUNDED_DESTINATION_START)
    if start < 0:
        return None
    end = text.find(_BOUNDED_DESTINATION_END, start)
    if end < 0:
        return None
    return text[start + len(_BOUNDED_DESTINATION_START) : end].strip()


def _truncate_destination(text: str, char_limit: int) -> str:
    """Truncate a destination.md to char_limit, starting at the nearest section
    heading boundary so the receiving phase gets a complete, labelled section
    rather than a mid-sentence fragment.

    If the file carries the bounded-mandate markers, the bounded section is
    returned whole when it fits the budget, else head-truncated to it -- the
    mandate is the content phases must see; the history tail is not.
    """
    bounded = _extract_bounded_destination(text)
    if bounded is not None:
        if len(bounded) <= char_limit:
            return bounded
        return (
            "[... bounded current destination truncated to budget ...]\n\n"
            + bounded[:char_limit]
        )
    if len(text) <= char_limit:
        return text
    cutoff = len(text) - char_limit
    match = re.search(r"^## \d{4}-\d{2}-\d{2}", text[cutoff:], re.MULTILINE)
    tail = text[cutoff + match.start() :] if match else text[-char_limit:]
    return "[... destination.md truncated for token budget ...]\n\n" + tail


def _load_destination(repo: Path, budget_chars: int = 3000) -> str:
    """Load destination.md (or legacy vision.md), truncated to budget.

    Bounded-marker files deliver the current mandate; unmarked files keep the
    historical tail + section-boundary behavior.
    """
    for name in ("destination.md", "vision.md"):
        dest_file = repo / ".acm" / name
        if dest_file.exists():
            content = dest_file.read_text(encoding="utf-8")
            return _truncate_destination(content, budget_chars)
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
