"""Shared data types for the ai-steward pipeline phases.

Defining these here breaks the circular import that would otherwise exist
between loop.py (orchestrator) and the phase modules (scan, implement,
record), all of which need Finding as an input or output type.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


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

    status: Literal["proposed", "verify_failed", "nothing_found", "preflight_failed", "implement_failed"]
    finding: Finding | None
    diff: str | None
    trail_entry: str
    preflight_failure: str | None = None
