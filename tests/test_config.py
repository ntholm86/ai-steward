"""Tests for AiStewardConfig validation."""

import pytest
from pathlib import Path
from ai_steward.config import AiStewardConfig, ModelAssignment, HarnessConfig, ScopeConfig


MINIMAL_MODELS = ModelAssignment(
    analyze="claude-haiku-4-5",
    propose="claude-opus-4-5",
    implement="claude-sonnet-4-5",
    verify="gpt-4o",
    judge="gemini-2.5-pro",
)


def test_config_loads_with_valid_repo(tmp_path: Path) -> None:
    cfg = AiStewardConfig(repo=tmp_path, models=MINIMAL_MODELS)
    assert cfg.repo == tmp_path


def test_repo_must_exist() -> None:
    with pytest.raises(ValueError, match="does not exist"):
        AiStewardConfig(repo=Path("/nonexistent/path"), models=MINIMAL_MODELS)


def test_harness_endpoint_strips_trailing_slash() -> None:
    h = HarnessConfig(endpoint="http://localhost:8474/")
    assert h.endpoint == "http://localhost:8474"


def test_sandbox_rejects_unknown_value(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="sandbox must be"):
        AiStewardConfig(repo=tmp_path, models=MINIMAL_MODELS, sandbox="podman")


def test_sandbox_accepts_local(tmp_path: Path) -> None:
    cfg = AiStewardConfig(repo=tmp_path, models=MINIMAL_MODELS, sandbox="local")
    assert cfg.sandbox == "local"


def test_model_assignment_all_fields_required() -> None:
    with pytest.raises(ValueError):
        ModelAssignment(analyze="x", propose="y")  # missing implement, verify, judge


def test_scope_defaults_empty(tmp_path: Path) -> None:
    cfg = AiStewardConfig(repo=tmp_path, models=MINIMAL_MODELS)
    assert cfg.scope.allowed == []
    assert cfg.scope.blocked == []


def test_lenses_warns_on_unknown_name(tmp_path: Path) -> None:
    """Unknown lens name triggers UserWarning but the value is preserved."""
    with pytest.warns(UserWarning, match="Unknown lenses"):
        cfg = AiStewardConfig(repo=tmp_path, models=MINIMAL_MODELS, lenses=["mandate", "typo_lens"])
    assert cfg.lenses == ["mandate", "typo_lens"]


def test_reflect_lenses_warns_on_unknown_name(tmp_path: Path) -> None:
    """Unknown reflect_lens name triggers UserWarning but the value is preserved."""
    with pytest.warns(UserWarning, match="Unknown reflect_lenses"):
        cfg = AiStewardConfig(repo=tmp_path, models=MINIMAL_MODELS, reflect_lenses=["prediction", "unknown"])
    assert cfg.reflect_lenses == ["prediction", "unknown"]


def test_lenses_known_custom_no_warning(tmp_path: Path) -> None:
    """Known custom lenses (e.g. 'security') do not trigger a warning."""
    import warnings as _warnings
    with _warnings.catch_warnings():
        _warnings.simplefilter("error")
        cfg = AiStewardConfig(
            repo=tmp_path,
            models=MINIMAL_MODELS,
            lenses=["mandate", "examination", "security"],
        )
    assert "security" in cfg.lenses
