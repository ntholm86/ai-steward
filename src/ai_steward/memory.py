"""Where a repository's ACM memory lives.

A work repository is *bound* to a scope in a shared memory repository when
exactly one ``<memory>/repositories/<id>/repository.json`` lists one of the
repository's root commits. Memory repositories are found through a registry
file (``ACM_MEMORIES_FILE``, default ``~/.acm/memories``): one absolute path
per line, each a directory containing an ``.acm-root`` file.

An unbound repository keeps using its legacy in-repo ``<repo>/.acm`` folder.
An ambiguous binding (several scopes claim the repository) raises
:class:`MemoryResolutionError` -- the scope is never guessed.

In bound mode ai-steward only writes files into the memory working tree; it
never runs git against the memory repository.
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

_TRAIL_FILE = "audit-trail.md"
_AGENT_LINE = "ai-steward (autonomous engine; the model is recorded under Harness sessions)"

_warned: set[str] = set()


class MemoryResolutionError(RuntimeError):
    """The repository cannot be mapped to exactly one memory scope."""


@dataclass(frozen=True)
class MemoryScope:
    dir: Path
    bound: bool
    memory_root: Path | None


def clear_cache() -> None:
    """Forget already-emitted warnings (resolution itself is never cached)."""
    _warned.clear()


def _warn(message: str) -> None:
    if message not in _warned:
        _warned.add(message)
        logger.warning(message)


def _registry_path() -> Path:
    env = os.environ.get("ACM_MEMORIES_FILE")
    return Path(env).expanduser() if env else Path.home() / ".acm" / "memories"


def _root_commits(repo: Path) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-list", "--max-parents=0", "HEAD"],
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return set()
    if result.returncode != 0:
        return set()
    return {line.strip().lower() for line in result.stdout.splitlines() if line.strip()}


def _registered_memories() -> list[Path]:
    registry = _registry_path()
    try:
        lines = registry.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    memories: list[Path] = []
    seen: set[Path] = set()
    for raw in lines:
        entry = raw.strip()
        if not entry or entry.startswith("#"):
            continue
        memory = Path(entry).expanduser()
        if not memory.is_absolute():
            _warn(f"ignoring memory registry entry that is not an absolute path: {entry}")
            continue
        if not (memory / ".acm-root").is_file():
            _warn(f"ignoring registered memory {memory}: missing or has no .acm-root")
            continue
        real = memory.resolve()
        if real not in seen:
            seen.add(real)
            memories.append(memory)
    return memories


def _binding_roots(binding: Path) -> set[str] | None:
    try:
        data = json.loads(binding.read_text(encoding="utf-8"))
        roots = data["root_commits"]
        if not isinstance(roots, list):
            raise TypeError("root_commits is not a list")
        return {str(c).strip().lower() for c in roots}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        _warn(f"ignoring unreadable binding {binding}: {exc}")
        return None


def resolve_scope(repo: Path) -> MemoryScope:
    """Resolve the memory scope for ``repo`` (bound scope dir, else legacy ``.acm``)."""
    legacy = MemoryScope(repo / ".acm", False, None)
    memories = _registered_memories()
    bindings: list[tuple[Path, Path]] = []  # (repository.json, memory root)
    for memory in memories:
        for binding in sorted((memory / "repositories").glob("*/repository.json")):
            bindings.append((binding, memory))
    if not bindings:
        return legacy

    commits = _root_commits(repo)
    if not commits:
        return legacy

    matches: list[tuple[Path, Path]] = []
    for binding, memory in bindings:
        roots = _binding_roots(binding)
        if roots is None or not (commits & roots):
            continue
        if not binding.parent.resolve().is_relative_to(memory.resolve()):
            _warn(f"ignoring binding {binding}: scope resolves outside its memory repository")
            continue
        matches.append((binding, memory))

    if not matches:
        return legacy
    if len(matches) > 1:
        sources = "; ".join(str(binding) for binding, _ in matches)
        raise MemoryResolutionError(
            f"{len(matches)} memory bindings match {repo} (same root commit): {sources}. "
            "Remove the duplicate binding; ai-steward will not guess."
        )
    binding, memory = matches[0]
    return MemoryScope(binding.parent, True, memory)


def acm_dir(repo: Path) -> Path:
    """Directory holding the repository's memory files (scope dir, or legacy ``.acm``)."""
    return resolve_scope(repo).dir


def trail_location(repo: Path) -> str:
    """Human-readable description of where the trail is read from."""
    scope = resolve_scope(repo)
    if not scope.bound:
        return str(scope.dir / _TRAIL_FILE)
    return f"{scope.dir / _TRAIL_FILE} or {scope.dir / 'records' / '*.md'}"


def _trail_files(scope: MemoryScope) -> list[Path]:
    files: list[Path] = []
    legacy = scope.dir / _TRAIL_FILE
    if legacy.is_file():
        files.append(legacy)
    if scope.bound:
        records = scope.dir / "records"
        if records.is_dir():
            files.extend(sorted(p for p in records.glob("*.md") if p.is_file()))
    return files


def trail_exists(repo: Path) -> bool:
    return bool(_trail_files(resolve_scope(repo)))


def read_trail(repo: Path) -> str:
    """Full trail text: legacy ``audit-trail.md`` first, then bound ``records/*.md`` in name order."""
    parts = [p.read_text(encoding="utf-8") for p in _trail_files(resolve_scope(repo))]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return "\n\n---\n\n".join(part.strip() for part in parts) + "\n"


def _clean_slug(slug: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", slug.lower())).strip("-") or "record"


def _record_content(entry: str, stem: str, moment: datetime) -> str:
    body = entry.removeprefix("\n---\n\n").lstrip("\n")
    header = (
        f"- record: {stem}\n"
        f"- time: {moment.strftime('%Y-%m-%dT%H.%M.%SZ')}\n"
        "- scope: repository\n"
        f"- agent: {_AGENT_LINE}\n"
    )
    lines = body.split("\n")
    for index, line in enumerate(lines):
        if line.startswith("## "):
            return "\n".join(lines[: index + 1]) + "\n" + header + "\n".join(lines[index + 1 :])
    return header + "\n" + body


def write_trail_entry(repo: Path, entry: str, slug: str) -> Path:
    """Add one trail entry; returns the file written to.

    Legacy: append to ``.acm/audit-trail.md``. Bound: create a new
    ``records/<UTC timestamp>-<slug>.md`` that never overwrites an existing file.
    """
    scope = resolve_scope(repo)
    scope.dir.mkdir(parents=True, exist_ok=True)
    if not scope.bound:
        trail_file = scope.dir / _TRAIL_FILE
        with trail_file.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(entry)
        return trail_file

    records = scope.dir / "records"
    records.mkdir(parents=True, exist_ok=True)
    moment = datetime.now(timezone.utc)
    base = f"{moment.strftime('%Y%m%dT%H%M%SZ')}-{_clean_slug(slug)}"
    attempt = 1
    while True:
        stem = base if attempt == 1 else f"{base}-{attempt}"
        target = records / f"{stem}.md"
        try:
            with target.open("x", encoding="utf-8", newline="\n") as fh:
                fh.write(_record_content(entry, stem, moment))
        except FileExistsError:
            attempt += 1
            continue
        return target
