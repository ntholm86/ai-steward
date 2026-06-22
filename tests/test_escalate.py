"""Tests for the ESCALATE phase."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_steward.config import AiStewardConfig, HarnessConfig, ModelAssignment, ScopeConfig
from ai_steward.pipeline.escalate import (
    _extract_report_content,
    _load_destination,
    _load_failure_context,
    escalate,
    write_report,
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


def _mock_client(report_text: str) -> MagicMock:
    mock_content = MagicMock()
    mock_content.text = report_text
    mock_message = MagicMock()
    mock_message.content = [mock_content]
    mock_message.usage.input_tokens = 100
    mock_message.usage.output_tokens = 50
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


class TestLoadFailureContext:
    def test_loads_trail(self, tmp_path: Path) -> None:
        acm = tmp_path / ".acm"
        acm.mkdir()
        (acm / "audit-trail.md").write_text(
            "## Entry\n\nVERIFY FAILED: tests/test_foo.py", encoding="utf-8"
        )

        result = _load_failure_context(tmp_path)
        assert "VERIFY FAILED" in result

    def test_returns_placeholder_when_missing(self, tmp_path: Path) -> None:
        result = _load_failure_context(tmp_path)
        assert "No audit-trail.md found" in result

    def test_truncates_from_tail(self, tmp_path: Path) -> None:
        acm = tmp_path / ".acm"
        acm.mkdir()
        old = "OLD entry\n" * 20
        new = "NEWEST failure entry\n"
        (acm / "audit-trail.md").write_text(old + new, encoding="utf-8")

        result = _load_failure_context(tmp_path, budget_chars=30)
        assert "NEWEST failure entry" in result
        assert "OLD entry" not in result


# ---------------------------------------------------------------------------
# _extract_report_content tests
# ---------------------------------------------------------------------------


class TestExtractReportContent:
    def test_extracts_markdown_fence(self) -> None:
        raw = "```markdown\n# Report\n\nContent here.\n```"
        result = _extract_report_content(raw)
        assert result == "# Report\n\nContent here."

    def test_extracts_generic_fence(self) -> None:
        raw = "```\n# Report\n\nContent here.\n```"
        result = _extract_report_content(raw)
        assert result == "# Report\n\nContent here."

    def test_falls_back_to_raw_when_no_fence(self) -> None:
        raw = "# Report\n\nContent here."
        result = _extract_report_content(raw)
        assert result == raw

    def test_strips_whitespace(self) -> None:
        raw = "  plain content  "
        result = _extract_report_content(raw)
        assert result == "plain content"


# ---------------------------------------------------------------------------
# escalate() tests
# ---------------------------------------------------------------------------


class TestEscalate:
    def test_returns_tuple_of_three(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)
        client = _mock_client("# Report\n\nTOOLING_BROKEN")

        result = escalate(tmp_path, config, client=client)

        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_returns_report_and_tokens(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)
        client = _mock_client("```markdown\n# Escalation Report\n\nTOOLING_BROKEN\n```")

        content, in_tok, out_tok = escalate(tmp_path, config, client=client)

        assert "Escalation Report" in content
        assert in_tok == 100
        assert out_tok == 50

    def test_passes_current_error_to_prompt(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)
        client = _mock_client("# Report")

        escalate(tmp_path, config, current_error="pytest failed: 3 errors", client=client)

        call_kwargs = client.messages.create.call_args
        user_content = call_kwargs[1]["messages"][0]["content"]
        assert "pytest failed: 3 errors" in user_content

    def test_uses_reorient_model_when_set(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)
        config.models.reorient = "claude-sonnet-4-5"
        client = _mock_client("# Report")

        escalate(tmp_path, config, client=client)

        call_kwargs = client.messages.create.call_args
        assert call_kwargs[1]["model"] == "claude-sonnet-4-5"

    def test_falls_back_to_analyze_model(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)
        config.models.reorient = None
        client = _mock_client("# Report")

        escalate(tmp_path, config, client=client)

        call_kwargs = client.messages.create.call_args
        assert call_kwargs[1]["model"] == "claude-haiku-4-5"

    def test_includes_trigger_in_prompt(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)
        client = _mock_client("# Report")

        escalate(tmp_path, config, trigger="failure_streak_3", client=client)

        call_kwargs = client.messages.create.call_args
        user_content = call_kwargs[1]["messages"][0]["content"]
        assert "failure_streak_3" in user_content


# ---------------------------------------------------------------------------
# write_report() tests
# ---------------------------------------------------------------------------


class TestWriteReport:
    def test_writes_to_acm_dir(self, tmp_path: Path) -> None:
        report_path = write_report(tmp_path, "# Escalation Report\n\nContent.")
        assert report_path == tmp_path / ".acm" / "escalate_report.md"
        assert report_path.exists()

    def test_creates_acm_dir_if_missing(self, tmp_path: Path) -> None:
        assert not (tmp_path / ".acm").exists()
        write_report(tmp_path, "# Report")
        assert (tmp_path / ".acm").exists()

    def test_content_written_correctly(self, tmp_path: Path) -> None:
        content = "# Escalation Report\n\n## Classification: TOOLING_BROKEN"
        write_report(tmp_path, content)
        written = (tmp_path / ".acm" / "escalate_report.md").read_text(encoding="utf-8")
        assert written == content

    def test_overwrites_previous_report(self, tmp_path: Path) -> None:
        (tmp_path / ".acm").mkdir()
        write_report(tmp_path, "first report")
        write_report(tmp_path, "second report")
        written = (tmp_path / ".acm" / "escalate_report.md").read_text(encoding="utf-8")
        assert written == "second report"
