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
from ai_steward.pipeline.scan import _collect_files, _load_scope_context, scan

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


def test_scan_rejects_blocked_file_proposal(tmp_path: Path) -> None:
    """Model must not be able to propose a file that is in scope.blocked."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "utils.py").write_text("x = 1\n")
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_utils.py").write_text("def test_x(): pass\n")
    config = _make_config(
        tmp_path,
        scope=ScopeConfig(allowed=["src/**/*.py"], blocked=["tests/**"]),
    )

    result = scan(tmp_path, config, client=_mock_client({
        "file": "tests/test_utils.py",
        "description": "Add test coverage",
        "proposed_change": "Add a new test function",
        "rationale": "coverage",
        "risk": "low",
    }))

    assert result is None


def test_scan_rejects_out_of_allowed_scope_proposal(tmp_path: Path) -> None:
    """Model must not be able to propose a file outside scope.allowed."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "utils.py").write_text("x = 1\n")
    (tmp_path / "outside.py").write_text("y = 2\n")
    config = _make_config(
        tmp_path,
        scope=ScopeConfig(allowed=["src/**/*.py"]),
    )

    result = scan(tmp_path, config, client=_mock_client({
        "file": "outside.py",
        "description": "Fix something",
        "proposed_change": "y = 3",
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


# ---------------------------------------------------------------------------
# ORIENT — retrospect.md and learning.md injection
# ---------------------------------------------------------------------------


def test_scan_includes_retrospect_in_context(tmp_path: Path) -> None:
    """retrospect.md content appears in user_content when the file exists."""
    (tmp_path / "utils.py").write_text("x = 1\n")
    (tmp_path / ".acm").mkdir()
    (tmp_path / ".acm" / "retrospect.md").write_text(
        "# retrospect.md\n\nClaim: the loop is working.", encoding="utf-8"
    )
    config = _make_config(tmp_path)
    client = _mock_client({"nothing": True})

    scan(tmp_path, config, client=client)

    user_content = client.messages.create.call_args[1]["messages"][0]["content"]
    assert "Current orientation (retrospect):" in user_content
    assert "Claim: the loop is working." in user_content


def test_scan_includes_learning_in_context(tmp_path: Path) -> None:
    """learning.md tail content appears in user_content when the file exists."""
    (tmp_path / "utils.py").write_text("x = 1\n")
    (tmp_path / ".acm").mkdir()
    (tmp_path / ".acm" / "learning.md").write_text(
        "# Learning\n\n## 2026-06-21\n\n**[!REALIZATION]** The loop converges.", encoding="utf-8"
    )
    config = _make_config(tmp_path)
    client = _mock_client({"nothing": True})

    scan(tmp_path, config, client=client)

    user_content = client.messages.create.call_args[1]["messages"][0]["content"]
    assert "Learning surface" in user_content
    assert "**[!REALIZATION]** The loop converges." in user_content


def test_scan_skips_missing_orient_files(tmp_path: Path) -> None:
    """SCAN succeeds normally when retrospect.md and learning.md are absent."""
    (tmp_path / "utils.py").write_text("x = 1\n")
    config = _make_config(tmp_path)
    client = _mock_client({
        "file": "utils.py",
        "description": "test",
        "proposed_change": "x = 2",
        "rationale": "better",
        "risk": "low",
    })

    result = scan(tmp_path, config, client=client)

    assert isinstance(result, Finding)
    user_content = client.messages.create.call_args[1]["messages"][0]["content"]
    assert "Current orientation" not in user_content
    assert "Learning surface" not in user_content


def test_scan_delivers_operational_rules_beyond_head_window(tmp_path: Path) -> None:
    """Operational rules reach the model even when they fall well past the head window.

    This is the regression test for the 1000-char window bug: retrospect.md in
    production has its '## Active operational rules' section at char 5681. The
    prior head-only extraction silently delivered zero operational rules to SCAN.
    """
    (tmp_path / "utils.py").write_text("x = 1\n")
    (tmp_path / ".acm").mkdir()
    # Rules section far beyond the 2000-char head window
    padding = "Claim: " + ("x" * 50 + "\n") * 40  # ~2400 chars of claims
    retrospect = (
        f"# retrospect\n\n{padding}\n\n"
        f"## Active operational rules\n\n"
        f"- V1 stops before release. Inviolable.\n"
        f"- Harness proxy outside autonomous scope.\n"
    )
    (tmp_path / ".acm" / "retrospect.md").write_text(retrospect, encoding="utf-8")
    config = _make_config(tmp_path)
    client = _mock_client({"nothing": True})

    scan(tmp_path, config, client=client)

    user_content = client.messages.create.call_args[1]["messages"][0]["content"]
    assert "Active operational rules:" in user_content
    assert "V1 stops before release. Inviolable." in user_content
    assert "Current orientation (retrospect):" in user_content  # head still present


def test_scan_head_budget_is_two_thousand_chars(tmp_path: Path) -> None:
    """The head excerpt covers up to 2000 chars (not the old 1000-char limit)."""
    (tmp_path / "utils.py").write_text("x = 1\n")
    (tmp_path / ".acm").mkdir()
    # Write a claim that starts at char ~1100 (beyond the old 1000-char window)
    filler = "A" * 1100
    marker_text = "CLAIM_BEYOND_OLD_LIMIT"
    retrospect = filler + marker_text
    (tmp_path / ".acm" / "retrospect.md").write_text(retrospect, encoding="utf-8")
    config = _make_config(tmp_path)
    client = _mock_client({"nothing": True})

    scan(tmp_path, config, client=client)

    user_content = client.messages.create.call_args[1]["messages"][0]["content"]
    assert marker_text in user_content, "Content at char 1100 must be inside the 2000-char head window"


# ---------------------------------------------------------------------------
# _load_scope_context — parameter variation (scope_depth, budget_chars)
# ---------------------------------------------------------------------------


def test_load_scope_context_scope_depth_limits_traversal(tmp_path: Path) -> None:
    """scope_depth=1 reads only the immediate parent, not the grandparent."""
    workspace = tmp_path / "workspace"
    repo = workspace / "myrepo"
    repo.mkdir(parents=True)

    (tmp_path / ".acm").mkdir()
    (tmp_path / ".acm" / "destination.md").write_text(
        "# Grandparent\nGrandparent goal.", encoding="utf-8"
    )
    (workspace / ".acm").mkdir()
    (workspace / ".acm" / "destination.md").write_text(
        "# Workspace\nWorkspace goal.", encoding="utf-8"
    )

    # scope_depth=1 — only the immediate parent (workspace) is in range
    result_shallow = _load_scope_context(repo, scope_depth=1)
    assert result_shallow is not None
    assert "Workspace goal." in result_shallow
    assert "Grandparent goal." not in result_shallow

    # scope_depth=2 — both levels reached
    result_deep = _load_scope_context(repo, scope_depth=2)
    assert result_deep is not None
    assert "Workspace goal." in result_deep
    assert "Grandparent goal." in result_deep


def test_load_scope_context_budget_chars_controls_truncation(tmp_path: Path) -> None:
    """destination_budget_chars limits how much destination text reaches SCAN."""
    repo = tmp_path
    (repo / ".acm").mkdir()
    # Destination large enough to exceed a small budget (half goes to repo scope)
    long_dest = "## 2026-01-01\n\n" + "A" * 2000
    (repo / ".acm" / "destination.md").write_text(long_dest, encoding="utf-8")

    # budget_chars=200 → repo gets 100 chars; 2015-char dest must be truncated
    result_tight = _load_scope_context(repo, budget_chars=200)
    assert result_tight is not None
    assert "[... destination.md truncated" in result_tight

    # budget_chars=10000 → repo gets 5000 chars; 2015-char dest fits without truncation
    result_wide = _load_scope_context(repo, budget_chars=10000)
    assert result_wide is not None
    assert "[... destination.md truncated" not in result_wide
