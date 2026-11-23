"""Shared utilities for the ai-steward pipeline.

Functions here are tier-0 (no LLM calls) and used by multiple phases.
"""

from __future__ import annotations

import re
import shlex
import subprocess
from pathlib import Path

from ai_steward.memory import acm_dir, resolve_scope

_BOUNDED_GOAL_START = "<!-- current-goal: complete -->"
_BOUNDED_GOAL_END = "<!-- goal-history -->"


def _extract_bounded_goal(text: str) -> str | None:
    """Extract the bounded current mandate from a goal.md, if marked.

    When a goal contains the exact markers
    <!-- current-goal: complete --> and <!-- goal-history -->
    in that order, the content between them is the operator-confirmed current
    mandate (the skills-suite bounded-read convention). That bounded section
    is small and authoritative; the dated history below the end marker is
    provenance, not active instruction -- tail-truncation into it would
    deliver superseded sections and miss the mandate entirely.
    """
    start = text.find(_BOUNDED_GOAL_START)
    if start < 0:
        return None
    end = text.find(_BOUNDED_GOAL_END, start)
    if end < 0:
        return None
    return text[start + len(_BOUNDED_GOAL_START) : end].strip()


def _truncate_goal(text: str, char_limit: int) -> str:
    """Truncate a goal.md to char_limit, starting at the nearest section
    heading boundary so the receiving phase gets a complete, labelled section
    rather than a mid-sentence fragment.

    If the file carries the bounded-mandate markers, the bounded section is
    returned whole when it fits the budget, else head-truncated to it -- the
    mandate is the content phases must see; the history tail is not.
    """
    bounded = _extract_bounded_goal(text)
    if bounded is not None:
        if len(bounded) <= char_limit:
            return bounded
        return (
            "[... bounded current goal truncated to budget ...]\n\n"
            + bounded[:char_limit]
        )
    if len(text) <= char_limit:
        return text
    cutoff = len(text) - char_limit
    match = re.search(r"^## \d{4}-\d{2}-\d{2}", text[cutoff:], re.MULTILINE)
    tail = text[cutoff + match.start() :] if match else text[-char_limit:]
    return "[... goal.md truncated for token budget ...]\n\n" + tail


def _load_goal(repo: Path, budget_chars: int = 3000) -> str:
    """Load goal.md (or legacy vision.md), truncated to budget.

    Bounded-marker files deliver the current mandate; unmarked files keep the
    historical tail + section-boundary behavior.

    A bound repository whose memory root also holds a goal.md gets both:
    the memory-wide mandate first (it outranks the repository goal),
    then the repository goal, each with half the budget.
    """
    scope = resolve_scope(repo)
    repo_text: str | None = None
    for name in ("goal.md", "vision.md"):
        dest_file = scope.dir / name
        if dest_file.exists():
            repo_text = dest_file.read_text(encoding="utf-8")
            break

    memory_text: str | None = None
    if scope.bound and scope.memory_root is not None:
        memory_file = scope.memory_root / "goal.md"
        if memory_file.is_file():
            memory_text = memory_file.read_text(encoding="utf-8")

    if memory_text is None:
        if repo_text is None:
            return "[No goal.md found]"
        return _truncate_goal(repo_text, budget_chars)

    half = budget_chars // 2
    sections = [f"### Higher-scope mandate (memory):\n\n{_truncate_goal(memory_text, half)}"]
    if repo_text is not None:
        sections.append(f"### Repo-scope mandate:\n\n{_truncate_goal(repo_text, half)}")
    return "\n\n---\n\n".join(sections)


def _load_current_orientation(repo: Path) -> str:
    """Load the current learning.md (the synthesis REORIENT writes) if it exists."""
    orientation_file = acm_dir(repo) / "learning.md"
    if not orientation_file.exists():
        return "[No learning.md found]"
    return orientation_file.read_text(encoding="utf-8")


def _load_learning(repo: Path, budget_chars: int = 20000) -> str:
    """Load generated/trail-markers.md — the pre-extracted [!REALIZATION]/[!REVERSAL] surface.

    trail-markers.md is the compact chronological digest of every marker across the
    full trail. It is the pre-digested pattern surface: reading it alongside
    the raw trail gives the model both the extracted conclusions and their
    original context. Budget takes the tail (newest markers last).
    """
    learning_file = acm_dir(repo) / "generated" / "trail-markers.md"
    if not learning_file.exists():
        return "[No generated/trail-markers.md found — run record.py markers --write to generate it]"
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
