"""Tests for ACM memory binding (shared memory repository vs legacy in-repo .acm)."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest
from click.testing import CliRunner

from ai_steward import memory
from ai_steward.cli import main
from ai_steward.config import HarnessConfig
from ai_steward.harness import harness_session
from ai_steward.memory import (
    MemoryResolutionError,
    acm_dir,
    read_trail,
    resolve_scope,
    trail_exists,
    write_trail_entry,
)
from ai_steward.pipeline import Finding
from ai_steward.pipeline._utils import _load_destination
from ai_steward.pipeline.loop import _commit_proposal
from ai_steward.pipeline.record import _build_entry, _trail_slug, record
from ai_steward.pipeline.scan import _load_scope_context

_IDENTITY = ["-c", "user.name=t", "-c", "user.email=t@example.com"]


def _git(path: Path, *args: str) -> str:
    result = subprocess.run(["git", *_IDENTITY, *args], cwd=path, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _git_repo(path: Path, content: str = "x = 1\n") -> str:
    """Create a git repo with one commit; return its root commit."""
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q")
    (path / "seed.py").write_text(content, encoding="utf-8")
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", f"seed {path.name}")
    return _git(path, "rev-list", "--max-parents=0", "HEAD")


def _make_memory(root: Path, bindings: dict[str, str]) -> Path:
    """Create a memory repository root with one binding per (id -> root commit)."""
    root.mkdir(parents=True, exist_ok=True)
    (root / ".acm-root").write_text("", encoding="utf-8")
    for repo_id, commit in bindings.items():
        scope = root / "repositories" / repo_id
        scope.mkdir(parents=True)
        (scope / "repository.json").write_text(json.dumps({"root_commits": [commit]}), encoding="utf-8")
    return root


def _register(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *memories: Path) -> None:
    registry = tmp_path / "registry"
    registry.write_text("\n\n".join(str(m) for m in memories) + "\n", encoding="utf-8")
    monkeypatch.setenv("ACM_MEMORIES_FILE", str(registry))


@pytest.fixture
def bound(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path, Path]:
    """(work repo, memory root, scope dir) with the repo bound to repositories/x."""
    repo = tmp_path / "work"
    commit = _git_repo(repo)
    mem = _make_memory(tmp_path / "mem", {"x": commit})
    _register(tmp_path, monkeypatch, mem)
    return repo, mem, mem / "repositories" / "x"


def _finding() -> Finding:
    return Finding(
        file="seed.py",
        description="Bump x to 2!",
        proposed_change="x = 2",
        rationale="test",
        risk="low",
        prediction="passes",
        examination_summary="test",
    )


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------


def test_unbound_repo_uses_legacy_acm(tmp_path: Path) -> None:
    scope = resolve_scope(tmp_path)
    assert (scope.dir, scope.bound, scope.memory_root) == (tmp_path / ".acm", False, None)
    assert acm_dir(tmp_path) == tmp_path / ".acm"


def test_git_repo_without_matching_binding_is_unbound(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = tmp_path / "work"
    _git_repo(repo)
    other = _git_repo(tmp_path / "other", content="y = 1\n")
    _register(tmp_path, monkeypatch, _make_memory(tmp_path / "mem", {"y": other}))
    assert resolve_scope(repo).bound is False


def test_repo_is_bound_by_root_commit(bound: tuple[Path, Path, Path]) -> None:
    repo, mem, scope_dir = bound
    scope = resolve_scope(repo)
    assert scope.bound is True
    assert scope.dir == scope_dir
    assert scope.memory_root == mem
    assert acm_dir(repo) == scope_dir


def test_ambiguous_binding_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = tmp_path / "work"
    commit = _git_repo(repo)
    mem = _make_memory(tmp_path / "mem", {"a": commit, "b": commit})
    _register(tmp_path, monkeypatch, mem)
    with pytest.raises(MemoryResolutionError, match="2 memory bindings"):
        resolve_scope(repo)


def test_invalid_registry_entries_and_bindings_are_ignored(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    repo = tmp_path / "work"
    commit = _git_repo(repo)
    mem = _make_memory(tmp_path / "mem", {"x": commit})
    (mem / "repositories" / "broken").mkdir()
    (mem / "repositories" / "broken" / "repository.json").write_text("{not json", encoding="utf-8")
    no_root = tmp_path / "not-a-memory"
    no_root.mkdir()
    _register(tmp_path, monkeypatch, tmp_path / "missing", no_root, mem)

    with caplog.at_level("WARNING", logger="ai_steward.memory"):
        scope = resolve_scope(repo)

    assert scope.bound is True and scope.dir == mem / "repositories" / "x"
    assert "no .acm-root" in caplog.text
    assert "unreadable binding" in caplog.text


def test_ambiguity_aborts_cli_command(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = tmp_path / "work"
    commit = _git_repo(repo)
    _register(tmp_path, monkeypatch, _make_memory(tmp_path / "mem", {"a": commit, "b": commit}))
    result = CliRunner().invoke(main, ["run", str(repo)])
    assert result.exit_code != 0
    assert "2 memory bindings" in result.output


# ---------------------------------------------------------------------------
# Trail reads and writes
# ---------------------------------------------------------------------------


def test_read_trail_empty_when_nothing(tmp_path: Path) -> None:
    assert read_trail(tmp_path) == ""
    assert trail_exists(tmp_path) is False


def test_read_trail_legacy_reads_file_verbatim(tmp_path: Path) -> None:
    (tmp_path / ".acm").mkdir()
    (tmp_path / ".acm" / "audit-trail.md").write_text("# trail\n\nentry\n", encoding="utf-8")
    assert trail_exists(tmp_path) is True
    assert read_trail(tmp_path) == "# trail\n\nentry\n"


def test_read_trail_bound_legacy_file_then_records_in_name_order(bound: tuple[Path, Path, Path]) -> None:
    repo, _, scope_dir = bound
    (scope_dir / "audit-trail.md").write_text("LEGACY", encoding="utf-8")
    records = scope_dir / "records"
    records.mkdir()
    (records / "20260102T000000Z-b.md").write_text("SECOND", encoding="utf-8")
    (records / "20260101T000000Z-a.md").write_text("FIRST", encoding="utf-8")
    (records / "notes.txt").write_text("IGNORED", encoding="utf-8")

    text = read_trail(repo)

    assert trail_exists(repo) is True
    assert [text.index(s) for s in ("LEGACY", "FIRST", "SECOND")] == sorted(
        text.index(s) for s in ("LEGACY", "FIRST", "SECOND")
    )
    assert "IGNORED" not in text


def test_read_trail_bound_records_only(bound: tuple[Path, Path, Path]) -> None:
    repo, _, scope_dir = bound
    assert trail_exists(repo) is False
    (scope_dir / "records").mkdir()
    (scope_dir / "records" / "2026-05.md").write_text("SEALED", encoding="utf-8")
    assert read_trail(repo) == "SEALED"


def test_legacy_record_still_appends(tmp_path: Path) -> None:
    write_trail_entry(tmp_path, "\n---\n\n## one\n", "ai-steward-x")
    write_trail_entry(tmp_path, "\n---\n\n## two\n", "ai-steward-x")
    assert (tmp_path / ".acm" / "audit-trail.md").read_text(encoding="utf-8") == "\n---\n\n## one\n\n---\n\n## two\n"
    assert not (tmp_path / ".acm" / "records").exists()


def test_bound_record_creates_new_file_with_header(bound: tuple[Path, Path, Path]) -> None:
    repo, _, scope_dir = bound
    entry = _build_entry(_finding(), "diff")

    target = write_trail_entry(repo, entry, _trail_slug(_finding()))

    assert target.parent == scope_dir / "records"
    assert target.name.endswith("Z-ai-steward-bump-x-to-2.md")
    assert not (scope_dir / "audit-trail.md").exists()
    content = target.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert lines[0].startswith("## ")
    assert lines[1] == f"- record: {target.stem}"
    assert lines[2].startswith("- time: ") and lines[2].endswith("Z") and "." in lines[2]
    assert lines[3] == "- scope: repository"
    assert lines[4].startswith("- agent: ai-steward (autonomous engine")
    assert not content.startswith("\n---")
    assert "**[!DECISION]**" in content


def test_bound_record_never_overwrites(bound: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch) -> None:
    repo, _, scope_dir = bound

    class _FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):  # type: ignore[override]
            return datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)

    monkeypatch.setattr(memory, "datetime", _FixedDatetime)

    first = write_trail_entry(repo, "\n---\n\n## one\n", "ai-steward-same")
    second = write_trail_entry(repo, "\n---\n\n## two\n", "ai-steward-same")
    third = write_trail_entry(repo, "\n---\n\n## three\n", "ai-steward-same")

    assert first.name == "20260102T030405Z-ai-steward-same.md"
    assert second.name == "20260102T030405Z-ai-steward-same-2.md"
    assert third.name == "20260102T030405Z-ai-steward-same-3.md"
    assert "## one" in first.read_text(encoding="utf-8")
    assert "- time: 2026-01-02T03.04.05Z" in second.read_text(encoding="utf-8")
    assert len(list((scope_dir / "records").iterdir())) == 3


def test_record_in_bound_mode_writes_record_file(bound: tuple[Path, Path, Path]) -> None:
    from ai_steward.config import AiStewardConfig, ModelAssignment

    repo, _, scope_dir = bound
    models = ModelAssignment(
        analyze="claude-haiku-4-5", propose="claude-haiku-4-5", implement="claude-haiku-4-5",
        verify="claude-haiku-4-5", judge="claude-haiku-4-5",
    )
    record(repo, AiStewardConfig(repo=repo, models=models), _finding(), diff="")
    assert len(list((scope_dir / "records").glob("*.md"))) == 1
    assert not (repo / ".acm").exists()


def test_trail_slug_is_bounded_and_clean() -> None:
    finding = _finding()
    finding.description = "Ünïcode & Symbols: " + "very long " * 20
    slug = _trail_slug(finding)
    assert slug.startswith("ai-steward-")
    assert len(slug) <= len("ai-steward-") + 40
    assert slug == slug.lower() and all(c.isalnum() or c == "-" for c in slug)
    assert not slug.endswith("-")


# ---------------------------------------------------------------------------
# Destination chain
# ---------------------------------------------------------------------------


def test_bound_destination_chain_is_memory_then_scope_without_parents(
    bound: tuple[Path, Path, Path], tmp_path: Path
) -> None:
    repo, mem, scope_dir = bound
    (mem / "destination.md").write_text("MEMORY MANDATE", encoding="utf-8")
    (scope_dir / "destination.md").write_text("REPO MANDATE", encoding="utf-8")
    (tmp_path / ".acm").mkdir()
    (tmp_path / ".acm" / "destination.md").write_text("PARENT DIR MANDATE", encoding="utf-8")

    context = _load_scope_context(repo)

    assert context is not None
    assert "Higher-scope mandate (memory)" in context
    assert context.index("MEMORY MANDATE") < context.index("REPO MANDATE")
    assert "Repo-scope mandate" in context
    assert "PARENT DIR MANDATE" not in context

    loaded = _load_destination(repo)
    assert loaded.index("MEMORY MANDATE") < loaded.index("REPO MANDATE")


def test_bound_destination_scope_only(bound: tuple[Path, Path, Path]) -> None:
    repo, _, scope_dir = bound
    (scope_dir / "destination.md").write_text("REPO MANDATE", encoding="utf-8")
    assert _load_destination(repo) == "REPO MANDATE"
    context = _load_scope_context(repo)
    assert context is not None and "REPO MANDATE" in context and "Higher-scope" not in context


# ---------------------------------------------------------------------------
# Harness and loop integration
# ---------------------------------------------------------------------------


def test_harness_session_root_and_session_paths_when_bound(bound: tuple[Path, Path, Path]) -> None:
    repo, _, scope_dir = bound
    os.environ.pop("HARNESS_ROOT", None)
    session_id = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    with harness_session(repo, HarnessConfig()) as result:
        assert os.environ["HARNESS_ROOT"] == str(scope_dir)
        sessions = scope_dir / "sessions"
        sessions.mkdir()
        (sessions / f"{session_id}.jsonl").write_bytes(b'{"v":1}\n')
    assert result["session_paths"] == [str(sessions / f"{session_id}.jsonl")]
    assert "HARNESS_ROOT" not in os.environ


def test_commit_proposal_does_not_touch_memory_when_bound(
    bound: tuple[Path, Path, Path], tmp_path: Path
) -> None:
    repo, mem, scope_dir = bound
    _git(mem, "init", "-q")
    (mem / "README.md").write_text("memory", encoding="utf-8")
    _git(mem, "add", "-A")
    _git(mem, "commit", "-q", "-m", "memory seed")
    memory_head = _git(mem, "rev-parse", "HEAD")

    (repo / "seed.py").write_text("x = 2\n", encoding="utf-8")
    (scope_dir / "records").mkdir()
    (scope_dir / "records" / "20260101T000000Z-ai-steward-x.md").write_text("## r\n", encoding="utf-8")
    (scope_dir / "sessions").mkdir()
    (scope_dir / "sessions" / "01ARZ.jsonl").write_text("{}\n", encoding="utf-8")

    assert _commit_proposal(repo, _finding(), cycle=1) is True

    assert _git(mem, "rev-parse", "HEAD") == memory_head
    assert _git(mem, "diff", "--cached", "--name-only") == ""
    assert "repositories/" in _git(mem, "status", "--porcelain", "-uall").replace("\\", "/")
    committed = _git(repo, "show", "--name-only", "--format=", "HEAD")
    assert committed == "seed.py"
    message = _git(repo, "log", "-1", "--format=%B")
    assert str(scope_dir) in message
    assert "shared memory repository" in message and "uncommitted" in message
    assert ".acm/audit-trail.md (this commit)" not in message


def test_commit_proposal_legacy_still_stages_acm(tmp_path: Path) -> None:
    repo = tmp_path / "legacy"
    _git_repo(repo)
    (repo / "seed.py").write_text("x = 2\n", encoding="utf-8")
    (repo / ".acm").mkdir()
    (repo / ".acm" / "audit-trail.md").write_text("# trail\n", encoding="utf-8")

    assert _commit_proposal(repo, _finding(), cycle=1) is True

    committed = _git(repo, "show", "--name-only", "--format=", "HEAD")
    assert ".acm/audit-trail.md" in committed
    assert ".acm/audit-trail.md (this commit)" in _git(repo, "log", "-1", "--format=%B")


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------


def test_init_scaffolds_destination_into_scope_when_bound(bound: tuple[Path, Path, Path]) -> None:
    repo, _, scope_dir = bound
    result = CliRunner().invoke(main, ["init", str(repo)])
    assert result.exit_code == 0, result.output
    assert (scope_dir / "destination.md").is_file()
    assert not (repo / ".acm").exists()
    assert str(scope_dir / "destination.md") in result.output
