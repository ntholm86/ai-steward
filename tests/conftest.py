"""Shared fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_steward import memory


@pytest.fixture(autouse=True)
def _isolated_memory_registry(tmp_path_factory: pytest.TempPathFactory, monkeypatch: pytest.MonkeyPatch) -> None:
    """Point the memory registry at a missing file so a developer's real one never leaks in."""
    missing = tmp_path_factory.mktemp("acm-registry") / "no-such-memories-file"
    monkeypatch.setenv("ACM_MEMORIES_FILE", str(missing))
    memory.clear_cache()
