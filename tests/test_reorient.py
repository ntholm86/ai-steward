"""Tests for the REORIENT phase."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_steward.config import AiStewardConfig, HarnessConfig, ModelAssignment, ScopeConfig
from ai_steward.pipeline._utils import _load_current_retrospect, _load_destination, _load_learning
from ai_steward.pipeline.reorient import (
    _extract_retrospect_content,
    _load_audit_trail,
    reorient,
    write_retrospect,
)


@pytest.fixture
def sample_config(tmp_path: Path) -> AiStewardConfig:
    """Create a minimal config for testing."""
    return AiStewardConfig(
        repo=tmp_path,
        harness=HarnessConfig(),
        models=ModelAssignment(
            analyze="test-model",
            propose="test-model",
            implement="test-model",
            verify="test-model",
            judge="test-model",
        ),
        scope=ScopeConfig(),
    )


def _mock_client(response_text: str) -> MagicMock:
    """Create a mock Anthropic client returning the given text."""
    mock = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=response_text)]
    mock_message.usage.input_tokens = 1000
    mock_message.usage.output_tokens = 500
    mock.messages.create.return_value = mock_message
    return mock


class TestLoadDestination:
    def test_loads_destination_md(self, tmp_path: Path) -> None:
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        dest = acm_dir / "destination.md"
        dest.write_text("# Destination\n\nThis is the goal.", encoding="utf-8")

        result = _load_destination(tmp_path, budget_chars=1000)
        assert "This is the goal" in result

    def test_falls_back_to_vision_md(self, tmp_path: Path) -> None:
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        vision = acm_dir / "vision.md"
        vision.write_text("# Vision\n\nLegacy content.", encoding="utf-8")

        result = _load_destination(tmp_path, budget_chars=1000)
        assert "Legacy content" in result

    def test_truncates_large_files(self, tmp_path: Path) -> None:
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        dest = acm_dir / "destination.md"
        dest.write_text("A" * 5000, encoding="utf-8")

        result = _load_destination(tmp_path, budget_chars=1000)
        assert "truncated" in result
        assert len(result) < 1100  # budget + prefix

    def test_returns_placeholder_when_missing(self, tmp_path: Path) -> None:
        result = _load_destination(tmp_path, budget_chars=1000)
        assert "No destination.md found" in result


class TestLoadAuditTrail:
    def test_loads_full_trail(self, tmp_path: Path) -> None:
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        trail = acm_dir / "audit-trail.md"
        trail.write_text("# Audit trail\n\n## Entry 1\n\nContent here.", encoding="utf-8")

        result = _load_audit_trail(tmp_path, budget_chars=50000)
        assert "Entry 1" in result

    def test_truncates_large_trails(self, tmp_path: Path) -> None:
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        trail = acm_dir / "audit-trail.md"
        trail.write_text("B" * 100000, encoding="utf-8")

        result = _load_audit_trail(tmp_path, budget_chars=10000)
        assert "truncated" in result
        assert len(result) < 10100

    def test_returns_placeholder_when_missing(self, tmp_path: Path) -> None:
        result = _load_audit_trail(tmp_path, budget_chars=50000)
        assert "No audit-trail.md found" in result


class TestLoadCurrentRetrospect:
    def test_loads_existing_retrospect(self, tmp_path: Path) -> None:
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        retro = acm_dir / "retrospect.md"
        retro.write_text("# retrospect.md\n\n## Claims\n\n1. Test claim.", encoding="utf-8")

        result = _load_current_retrospect(tmp_path)
        assert "Test claim" in result

    def test_returns_placeholder_when_missing(self, tmp_path: Path) -> None:
        result = _load_current_retrospect(tmp_path)
        assert "No retrospect.md found" in result


class TestLoadLearning:
    def test_loads_learning_md(self, tmp_path: Path) -> None:
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        (acm_dir / "learning.md").write_text(
            "# Learning\n\n**[!REALIZATION]** System prompts are soft constraints.",
            encoding="utf-8",
        )

        result = _load_learning(tmp_path)
        assert "soft constraints" in result

    def test_returns_placeholder_when_missing(self, tmp_path: Path) -> None:
        result = _load_learning(tmp_path)
        assert "No learning.md found" in result

    def test_truncates_from_tail(self, tmp_path: Path) -> None:
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        old_entry = "OLD content\n" * 10
        new_entry = "NEW content\n"
        (acm_dir / "learning.md").write_text(old_entry + new_entry, encoding="utf-8")

        result = _load_learning(tmp_path, budget_chars=20)
        assert "NEW content" in result
        assert "OLD content" not in result

    def test_reorient_includes_learning_in_user_content(self, tmp_path: Path) -> None:
        """REORIENT passes learning.md content to the model."""
        acm = tmp_path / ".acm"
        acm.mkdir()
        (acm / "audit-trail.md").write_text("# Trail\n", encoding="utf-8")
        (acm / "learning.md").write_text(
            "# Learning\n\n**[!REALIZATION]** Never truncate from the head.",
            encoding="utf-8",
        )
        config = AiStewardConfig(
            repo=tmp_path,
            models=ModelAssignment(
                analyze="claude-haiku-4-5",
                propose="claude-haiku-4-5",
                implement="claude-haiku-4-5",
                verify="claude-haiku-4-5",
                judge="claude-haiku-4-5",
            ),
        )
        mock_content = MagicMock()
        mock_content.text = "# retrospect.md\n\n## Current claims\n\n1. Claim."
        mock_message = MagicMock()
        mock_message.content = [mock_content]
        mock_message.usage.input_tokens = 100
        mock_message.usage.output_tokens = 50
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_message

        reorient(tmp_path, config, trigger="test", client=mock_client)

        user_content = mock_client.messages.create.call_args[1]["messages"][0]["content"]
        assert "Learning surface" in user_content
        assert "Never truncate from the head" in user_content


class TestExtractRetrospectContent:
    def test_extracts_from_markdown_fence(self) -> None:
        response = """Here's the retrospect:

```markdown
# retrospect.md — test

Content here.
```

That's the output."""
        result = _extract_retrospect_content(response)
        assert result.startswith("# retrospect.md")
        assert "Content here" in result
        assert "That's the output" not in result

    def test_extracts_from_generic_fence(self) -> None:
        response = """```
# retrospect.md — test

Content here.
```"""
        result = _extract_retrospect_content(response)
        assert "Content here" in result

    def test_returns_raw_when_no_fence(self) -> None:
        response = "# retrospect.md — test\n\nContent here."
        result = _extract_retrospect_content(response)
        assert result == response


class TestReorient:
    def test_calls_model_with_context(
        self, tmp_path: Path, sample_config: AiStewardConfig
    ) -> None:
        # Set up files
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        (acm_dir / "destination.md").write_text("# Goal\nBe awesome.", encoding="utf-8")
        (acm_dir / "audit-trail.md").write_text("# Trail\n## Entry 1", encoding="utf-8")

        mock = _mock_client("```markdown\n# retrospect.md — test\n\nNew claims.\n```")

        content, in_tok, out_tok = reorient(tmp_path, sample_config, "test", client=mock)

        assert "New claims" in content
        assert in_tok == 1000
        assert out_tok == 500
        mock.messages.create.assert_called_once()

    def test_uses_configured_model(
        self, tmp_path: Path, sample_config: AiStewardConfig
    ) -> None:
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        (acm_dir / "audit-trail.md").write_text("# Trail", encoding="utf-8")

        # Set a specific reorient model
        sample_config.models.reorient = "special-reorient-model"

        mock = _mock_client("# retrospect.md\n\nContent.")
        reorient(tmp_path, sample_config, "test", client=mock)

        call_kwargs = mock.messages.create.call_args.kwargs
        assert call_kwargs["model"] == "special-reorient-model"


class TestWriteRetrospect:
    def test_writes_file(self, tmp_path: Path) -> None:
        content = "# retrospect.md — test\n\nContent here."
        path = write_retrospect(tmp_path, content)

        assert path.exists()
        assert path.read_text(encoding="utf-8") == content

    def test_creates_acm_directory(self, tmp_path: Path) -> None:
        content = "# retrospect.md — test\n\nContent here."
        write_retrospect(tmp_path, content)

        assert (tmp_path / ".acm").is_dir()

    def test_overwrites_existing(self, tmp_path: Path) -> None:
        acm_dir = tmp_path / ".acm"
        acm_dir.mkdir()
        retro = acm_dir / "retrospect.md"
        retro.write_text("Old content", encoding="utf-8")

        write_retrospect(tmp_path, "New content")

        assert retro.read_text(encoding="utf-8") == "New content"
