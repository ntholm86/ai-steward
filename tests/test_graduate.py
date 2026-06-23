"""Tests for the GRADUATE phase."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_steward.config import AiStewardConfig, HarnessConfig, ModelAssignment, ScopeConfig
from ai_steward.pipeline._utils import _load_destination
from ai_steward.pipeline.graduate import (
    _extract_proposal_content,
    _load_current_retrospect,
    _load_recent_trail,
    graduate,
    write_proposal,
)


def _make_config(repo: Path) -> AiStewardConfig:
    return AiStewardConfig(
        repo=repo,
        models=ModelAssignment(
            analyze="claude-haiku-4-5",
            propose="claude-haiku-4-5",
            implement="claude-haiku-4-5",
            verify="claude-haiku-4-5",
            judge="claude-haiku-4-5",
        ),
    )


def _mock_client(proposal_text: str) -> MagicMock:
    mock_content = MagicMock()
    mock_content.text = proposal_text
    mock_message = MagicMock()
    mock_message.content = [mock_content]
    mock_message.usage.input_tokens = 200
    mock_message.usage.output_tokens = 80
    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message
    return mock_client


# ---------------------------------------------------------------------------
# Loader tests
# ---------------------------------------------------------------------------


class TestLoadDestination:
    def test_loads_destination_md(self, tmp_path: Path) -> None:
        acm = tmp_path / ".acm"
        acm.mkdir()
        (acm / "destination.md").write_text("# Destination\n\nGoal: improve.", encoding="utf-8")

        result = _load_destination(tmp_path)
        assert "Goal: improve" in result

    def test_returns_placeholder_when_missing(self, tmp_path: Path) -> None:
        result = _load_destination(tmp_path)
        assert "No destination.md found" in result

    def test_truncates_from_tail(self, tmp_path: Path) -> None:
        acm = tmp_path / ".acm"
        acm.mkdir()
        old = "OLD content\n" * 10
        new = "NEW content\n"
        (acm / "destination.md").write_text(old + new, encoding="utf-8")

        result = _load_destination(tmp_path, budget_chars=20)
        assert "NEW content" in result
        assert "OLD content" not in result


class TestLoadCurrentRetrospect:
    def test_loads_retrospect(self, tmp_path: Path) -> None:
        acm = tmp_path / ".acm"
        acm.mkdir()
        (acm / "retrospect.md").write_text("# retrospect\n\n1. Claim.", encoding="utf-8")

        result = _load_current_retrospect(tmp_path)
        assert "Claim." in result

    def test_returns_placeholder_when_missing(self, tmp_path: Path) -> None:
        result = _load_current_retrospect(tmp_path)
        assert "No retrospect.md found" in result


class TestLoadRecentTrail:
    def test_loads_trail(self, tmp_path: Path) -> None:
        acm = tmp_path / ".acm"
        acm.mkdir()
        (acm / "audit-trail.md").write_text("## Entry 1\n\nSome text.", encoding="utf-8")

        result = _load_recent_trail(tmp_path)
        assert "Entry 1" in result

    def test_returns_placeholder_when_missing(self, tmp_path: Path) -> None:
        result = _load_recent_trail(tmp_path)
        assert "No audit-trail.md found" in result

    def test_truncates_from_tail(self, tmp_path: Path) -> None:
        acm = tmp_path / ".acm"
        acm.mkdir()
        old = "OLD entry\n" * 20
        new = "NEWEST entry\n"
        (acm / "audit-trail.md").write_text(old + new, encoding="utf-8")

        result = _load_recent_trail(tmp_path, budget_chars=20)
        assert "NEWEST entry" in result
        assert "OLD entry" not in result


# ---------------------------------------------------------------------------
# _extract_proposal_content tests
# ---------------------------------------------------------------------------


class TestExtractProposalContent:
    def test_extracts_from_markdown_fence(self) -> None:
        response = "Here it is:\n\n```markdown\n# Proposal\n\nContent.\n```\n\nDone."
        result = _extract_proposal_content(response)
        assert result.startswith("# Proposal")
        assert "Done." not in result

    def test_extracts_from_generic_fence(self) -> None:
        response = "```\n# Proposal\n\nContent.\n```"
        result = _extract_proposal_content(response)
        assert "# Proposal" in result

    def test_falls_back_to_raw(self) -> None:
        response = "# Proposal\n\nNo fence here."
        result = _extract_proposal_content(response)
        assert "No fence here" in result


# ---------------------------------------------------------------------------
# graduate() tests
# ---------------------------------------------------------------------------


class TestGraduate:
    def test_calls_model_with_destination_and_trail(self, tmp_path: Path) -> None:
        acm = tmp_path / ".acm"
        acm.mkdir()
        (acm / "destination.md").write_text("# Dest\n\nGoal.", encoding="utf-8")
        (acm / "audit-trail.md").write_text("## Entry\n\nNOTHING FOUND.", encoding="utf-8")

        config = _make_config(tmp_path)
        proposal_text = "```markdown\n# Graduate Proposal\n\n## Classification: ACHIEVED\n```"
        client = _mock_client(proposal_text)

        content, in_tok, out_tok = graduate(tmp_path, config, trigger="test", client=client)

        assert client.messages.create.called
        user_content = client.messages.create.call_args[1]["messages"][0]["content"]
        assert "Goal." in user_content
        assert "NOTHING FOUND." in user_content
        assert in_tok == 200
        assert out_tok == 80

    def test_returns_extracted_proposal(self, tmp_path: Path) -> None:
        acm = tmp_path / ".acm"
        acm.mkdir()
        (acm / "audit-trail.md").write_text("# Trail\n", encoding="utf-8")

        config = _make_config(tmp_path)
        proposal_text = "```markdown\n# Graduate Proposal\n\n## Classification: STALE\n```"
        client = _mock_client(proposal_text)

        content, _, _ = graduate(tmp_path, config, trigger="test", client=client)

        assert "Classification: STALE" in content

    def test_handles_empty_response(self, tmp_path: Path) -> None:
        acm = tmp_path / ".acm"
        acm.mkdir()
        (acm / "audit-trail.md").write_text("# Trail\n", encoding="utf-8")

        config = _make_config(tmp_path)
        mock_message = MagicMock()
        mock_message.content = []
        mock_message.usage.input_tokens = 0
        mock_message.usage.output_tokens = 0
        client = MagicMock()
        client.messages.create.return_value = mock_message

        content, in_tok, out_tok = graduate(tmp_path, config, trigger="test", client=client)

        assert content == ""
        assert in_tok == 0
        assert out_tok == 0


# ---------------------------------------------------------------------------
# write_proposal tests
# ---------------------------------------------------------------------------


class TestWriteProposal:
    def test_writes_proposal_file(self, tmp_path: Path) -> None:
        content = "# Graduate Proposal\n\n## Classification: ACHIEVED"
        path = write_proposal(tmp_path, content)

        assert path.name == "graduate_proposal.md"
        assert path.exists()
        assert "Classification: ACHIEVED" in path.read_text(encoding="utf-8")

    def test_creates_acm_dir_if_missing(self, tmp_path: Path) -> None:
        content = "# Proposal"
        path = write_proposal(tmp_path, content)
        assert path.parent.name == ".acm"
        assert path.parent.exists()

    def test_overwrites_previous_proposal(self, tmp_path: Path) -> None:
        write_proposal(tmp_path, "First proposal")
        write_proposal(tmp_path, "Second proposal")

        content = (tmp_path / ".acm" / "graduate_proposal.md").read_text(encoding="utf-8")
        assert "Second proposal" in content
        assert "First" not in content
