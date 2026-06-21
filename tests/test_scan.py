"""Tests for SCAN phase.

All tests use a mock Anthropic client — no real LLM calls, no anthropic
package required to run the suite.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_steward.config import AiStewardConfig, ModelAssignment, ScopeConfig
from ai_steward.pipeline import Finding
from ai_steward.pipeline.scan import _collect_files, scan

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_V1_MODELS = ModelAssignment(
    analyze="claude-haiku-4-5",
    propose="claude-haiku-4-5",
    implement="claude-haiku-4-5",
    verify="claude-haiku-4-5",
    judge="claude-haiku-4-5",
)


def _make_config(tmp_path: Path, scope: ScopeConfig | None = None) -> AiStewardConfig:
    return AiStewardConfig(
        repo=tmp_path,
        models=_V1_MODELS,
        scope=scope or ScopeConfig(),
    )


def _mock_client(response: dict, input_tokens: int = 0, output_tokens: int = 0) -> MagicMock:
    """Mock Anthropic client that returns a fixed JSON response."""
    block = MagicMock()
    block.text = json.dumps(response)
    message = MagicMock()
    message.content = [block]
    message.usage.input_tokens = input_tokens
    message.usage.output_tokens = output_tokens
    client = MagicMock()
    client.messages.create.return_value = message
    return client


# ---------------------------------------------------------------------------
# scan — valid finding
# ---------------------------------------------------------------------------


def test_scan_returns_finding_on_valid_response(tmp_path: Path) -> None:
    (tmp_path / "utils.py").write_text("import os\nimport sys\n\nx = 1\n")
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "Remove unused import os",
        "proposed_change": "import sys\n\nx = 1\n",
        "rationale": "os is not referenced anywhere in the module",
        "risk": "low",
    })

    result = scan(tmp_path, config, client=client)

    assert isinstance(result, Finding)
    assert result.file == "utils.py"
    assert result.risk == "low"
    assert result.blind_spot == ""
    client.messages.create.assert_called_once()


def test_scan_extracts_blind_spot_when_present(tmp_path: Path) -> None:
    (tmp_path / "utils.py").write_text("import os\n\nx = 1\n")
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "Remove unused import os",
        "proposed_change": "Remove the import os line",
        "rationale": "os is not referenced",
        "risk": "low",
        "blind_spot": "Did not examine test files for os usage",
    })

    result = scan(tmp_path, config, client=client)

    assert isinstance(result, Finding)
    assert result.blind_spot == "Did not examine test files for os usage"


# ---------------------------------------------------------------------------
# scan — None paths
# ---------------------------------------------------------------------------


def test_scan_returns_none_when_model_says_nothing(tmp_path: Path) -> None:
    (tmp_path / "clean.py").write_text("x = 1\n")
    config = _make_config(tmp_path)

    result = scan(tmp_path, config, client=_mock_client({"nothing": True}))

    assert result is None


def test_scan_returns_none_on_invalid_json(tmp_path: Path) -> None:
    (tmp_path / "f.py").write_text("x = 1\n")
    config = _make_config(tmp_path)
    block = MagicMock()
    block.text = "sorry, here is my answer in prose"
    message = MagicMock()
    message.content = [block]
    client = MagicMock()
    client.messages.create.return_value = message

    result = scan(tmp_path, config, client=client)

    assert result is None


def test_scan_skips_high_risk_finding(tmp_path: Path) -> None:
    (tmp_path / "core.py").write_text("x = 1\n")
    config = _make_config(tmp_path)

    result = scan(tmp_path, config, client=_mock_client({
        "file": "core.py",
        "description": "Rewrite the module",
        "proposed_change": "# everything rewritten",
        "rationale": "cleaner",
        "risk": "high",
    }))

    assert result is None


def test_scan_returns_none_if_file_not_in_repo(tmp_path: Path) -> None:
    (tmp_path / "real.py").write_text("x = 1\n")
    config = _make_config(tmp_path)

    result = scan(tmp_path, config, client=_mock_client({
        "file": "nonexistent.py",
        "description": "Fix something",
        "proposed_change": "x = 2",
        "rationale": "better",
        "risk": "low",
    }))

    assert result is None


def test_scan_returns_none_if_no_files_in_scope(tmp_path: Path) -> None:
    # No .py files — _collect_files returns empty dict, no LLM call made.
    config = _make_config(tmp_path)
    client = MagicMock()

    result = scan(tmp_path, config, client=client)

    assert result is None
    client.messages.create.assert_not_called()


# ---------------------------------------------------------------------------
# _collect_files
# ---------------------------------------------------------------------------


def test_collect_files_respects_blocked(tmp_path: Path) -> None:
    (tmp_path / "keep.py").write_text("x = 1")
    (tmp_path / "skip.py").write_text("y = 2")
    config = _make_config(
        tmp_path,
        scope=ScopeConfig(allowed=["**/*.py"], blocked=["skip.py"]),
    )

    files = _collect_files(tmp_path, config)

    assert "keep.py" in files
    assert "skip.py" not in files


# ---------------------------------------------------------------------------
# Directed SCAN — Commander's Intent injection
# ---------------------------------------------------------------------------


def test_scan_includes_destination_when_present(tmp_path: Path) -> None:
    """SCAN prompt must include destination content when .acm/destination.md exists."""
    (tmp_path / "utils.py").write_text("import os\nx = 1\n")
    (tmp_path / ".acm").mkdir()
    (tmp_path / ".acm" / "destination.md").write_text(
        "# Destination\nBuild a fast reliable pipeline.", encoding="utf-8"
    )
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "Remove unused import",
        "proposed_change": "Remove the import os line.",
        "rationale": "unused",
        "risk": "low",
    })

    scan(tmp_path, config, client=client)

    call_kwargs = client.messages.create.call_args
    user_content = call_kwargs[1]["messages"][0]["content"]
    assert "Commander's Intent" in user_content
    assert "Build a fast reliable pipeline." in user_content


def test_scan_works_without_destination(tmp_path: Path) -> None:
    """SCAN falls back gracefully when no destination.md exists."""
    (tmp_path / "utils.py").write_text("import os\nx = 1\n")
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "Remove unused import",
        "proposed_change": "Remove import os.",
        "rationale": "unused",
        "risk": "low",
    })

    result = scan(tmp_path, config, client=client)

    assert isinstance(result, Finding)
    call_kwargs = client.messages.create.call_args
    user_content = call_kwargs[1]["messages"][0]["content"]
    assert "Commander's Intent" not in user_content


def test_scan_truncates_long_destination(tmp_path: Path) -> None:
    """Destination takes the tail when over budget — most recent content is preserved."""
    (tmp_path / "utils.py").write_text("x = 1\n")
    (tmp_path / ".acm").mkdir()
    # Old content at start, new content at end — truncation must preserve the end.
    old_content = "OLD: " + "A" * 2000
    new_content = "NEW: latest operator decision"
    long_text = old_content + "B" * 1000 + new_content
    (tmp_path / ".acm" / "destination.md").write_bytes(long_text.encode("utf-8"))
    config = _make_config(tmp_path)
    client = _mock_client({"nothing": True})

    scan(tmp_path, config, client=client)

    call_kwargs = client.messages.create.call_args
    user_content = call_kwargs[1]["messages"][0]["content"]
    assert "truncated for token budget" in user_content
    assert "NEW: latest operator decision" in user_content
    assert "OLD: " + "A" * 2000 not in user_content


def test_scan_truncation_starts_at_section_boundary(tmp_path: Path) -> None:
    """When destination has dated sections, truncation starts at the nearest heading."""
    (tmp_path / "utils.py").write_text("x = 1\n")
    (tmp_path / ".acm").mkdir()
    # Old section must be long enough that total > 3000 and cutoff lands before new heading.
    old_section = "## 2026-05-14 — Old section\n\n" + "A" * 3500 + "\n\n"
    new_section = "## 2026-06-20 — New section\n\nLatest operator decision.\n"
    long_text = old_section + new_section
    (tmp_path / ".acm" / "destination.md").write_bytes(long_text.encode("utf-8"))
    config = _make_config(tmp_path)
    client = _mock_client({"nothing": True})

    scan(tmp_path, config, client=client)

    call_kwargs = client.messages.create.call_args
    user_content = call_kwargs[1]["messages"][0]["content"]
    assert "## 2026-06-20 — New section" in user_content
    assert "Latest operator decision." in user_content
    # Must not start mid-sentence inside the old section
    assert "## 2026-05-14 — Old section" not in user_content


# ---------------------------------------------------------------------------
# _load_scope_context — parent-scope traversal (ACM §4.2)
# ---------------------------------------------------------------------------


def test_scan_includes_parent_scope_destination(tmp_path: Path) -> None:
    """Parent .acm/destination.md is included in the SCAN prompt as higher-scope mandate."""
    repo = tmp_path / "myrepo"
    repo.mkdir()
    (repo / "utils.py").write_text("x = 1\n")
    (repo / ".acm").mkdir()
    (repo / ".acm" / "destination.md").write_text("# Repo dest\nRepo goal.", encoding="utf-8")
    # Parent scope (workspace level)
    (tmp_path / ".acm").mkdir()
    (tmp_path / ".acm" / "destination.md").write_text(
        "# Workspace dest\nWorkspace goal.", encoding="utf-8"
    )
    config = _make_config(repo)
    client = _mock_client({
        "file": "utils.py",
        "description": "test",
        "proposed_change": "x = 2",
        "rationale": "test",
        "risk": "low",
    })

    scan(repo, config, client=client)

    user_content = client.messages.create.call_args[1]["messages"][0]["content"]
    assert "Workspace goal." in user_content
    assert "Repo goal." in user_content
    assert "Higher-scope mandate" in user_content


def test_scan_stops_at_acm_root_marker(tmp_path: Path) -> None:
    """Traversal stops at .acm-root marker; destination above it is NOT included."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    repo = workspace / "myrepo"
    repo.mkdir()
    (repo / "utils.py").write_text("x = 1\n")
    # Repo scope
    (repo / ".acm").mkdir()
    (repo / ".acm" / "destination.md").write_text("# Repo\nRepo goal.", encoding="utf-8")
    # Workspace scope with .acm-root marker → ceiling here
    (workspace / ".acm").mkdir()
    (workspace / ".acm" / "destination.md").write_text(
        "# Workspace\nWorkspace goal.", encoding="utf-8"
    )
    (workspace / ".acm-root").write_text("")  # ceiling marker
    # Above the ceiling — must NOT be read
    (tmp_path / ".acm").mkdir()
    (tmp_path / ".acm" / "destination.md").write_text(
        "# Org\nOrg goal MUST NOT APPEAR.", encoding="utf-8"
    )
    config = _make_config(repo)
    client = _mock_client({
        "file": "utils.py",
        "description": "test",
        "proposed_change": "x = 2",
        "rationale": "test",
        "risk": "low",
    })

    scan(repo, config, client=client)

    user_content = client.messages.create.call_args[1]["messages"][0]["content"]
    assert "Workspace goal." in user_content
    assert "Repo goal." in user_content
    assert "Org goal MUST NOT APPEAR." not in user_content


def test_scan_returns_none_when_change_already_exists(tmp_path: Path) -> None:
    """already_exists_check quotes text found in the file → false-positive rejected."""
    (tmp_path / "utils.py").write_text("def handle(x):\n    if x is None:\n        return 0\n    return x\n")
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "Add None guard in handle()",
        "proposed_change": "Add `if x is None: return 0` at the top of handle()",
        "rationale": "prevents crash on None input",
        "risk": "low",
        "already_exists_check": "if x is None:",
    })

    result = scan(tmp_path, config, client=client)

    assert result is None


def test_scan_proceeds_when_already_exists_check_is_not_found(tmp_path: Path) -> None:
    """already_exists_check = 'not found' → proposal is genuine, proceeds normally."""
    (tmp_path / "utils.py").write_text("def handle(x):\n    return x\n")
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "Add None guard in handle()",
        "proposed_change": "Add `if x is None: return 0` at the top of handle()",
        "rationale": "prevents crash on None input",
        "risk": "low",
        "already_exists_check": "not found",
    })

    result = scan(tmp_path, config, client=client)

    assert isinstance(result, Finding)


# ---------------------------------------------------------------------------
# _collect_files — default scope (technology-agnostic)
# ---------------------------------------------------------------------------


def test_collect_files_default_scope_includes_non_python_text_files(tmp_path: Path) -> None:
    """Default scope **/* collects any text file, not just .py."""
    (tmp_path / "README.md").write_text("# Hello\n")
    (tmp_path / "package.json").write_text('{"name": "x"}\n')
    config = _make_config(tmp_path)  # no explicit scope

    files = _collect_files(tmp_path, config)

    assert "README.md" in files
    assert "package.json" in files


def test_collect_files_default_scope_excludes_binary_files(tmp_path: Path) -> None:
    """Default scope skips binary files (NUL-byte heuristic)."""
    (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00")
    (tmp_path / "notes.txt").write_text("plain text\n")
    config = _make_config(tmp_path)  # no explicit scope

    files = _collect_files(tmp_path, config)

    assert "image.png" not in files
    assert "notes.txt" in files
