"""Configuration schema for ai-steward.

Every design decision lives here in code:
- Which model family handles which pipeline phase (model-family independence principle)
- llm-harness-proxy integration contract (all LLM calls route through the proxy)
- Scope enforcement (allowed/blocked file globs)
- Safety budget (iteration cap and cost cap)
"""

from pathlib import Path
from pydantic import BaseModel, field_validator


class HarnessConfig(BaseModel):
    """Connection config for llm-harness-proxy (port 8474 by default)."""

    endpoint: str = "http://localhost:8474"

    @field_validator("endpoint")
    @classmethod
    def no_trailing_slash(cls, v: str) -> str:
        return v.rstrip("/")


class ModelAssignment(BaseModel):
    """Which model/provider handles which pipeline phase.

    Specify as provider-native model identifiers — llm-harness-proxy routes them to the
    correct backend based on the endpoint path chosen by the execution layer.

    V1 (single-model): assign the same model to all phases. This is valid and expected.
    The token-efficiency constraint (destination 2026-06-19) means V1 uses only tier 0/1
    reasoning; a single cheap model (e.g. claude-haiku-4-5) across all phases is correct.

        analyze: "claude-haiku-4-5"
        propose: "claude-haiku-4-5"
        implement: "claude-haiku-4-5"
        verify: "claude-haiku-4-5"
        judge: "claude-haiku-4-5"

    V2 (model-family independence): PROPOSE and VERIFY use different families so the
    judge cannot share the proposer's blind spots. JUDGE should use a third family.
    No validator enforces this in V1; that constraint is V2 work.

        analyze: "claude-haiku-4-5"      # fast, cheap analysis
        propose: "claude-opus-4-5"        # high-quality proposal
        implement: "claude-sonnet-4-5"    # balanced implementation
        verify: "gpt-4o"                  # adversarial — different family from propose
        judge: "gemini-2.5-pro"           # third-family gate
    """

    analyze: str
    propose: str
    implement: str
    verify: str
    judge: str


class ScopeConfig(BaseModel):
    """Controls which files the execution layer may read and write."""

    allowed: list[str] = []  # glob patterns; empty means all files
    blocked: list[str] = []  # glob patterns; always applied after allowed


class AiStewardConfig(BaseModel):
    """Top-level configuration loaded from .ai-steward.yaml in the target repo."""

    repo: Path
    harness: HarnessConfig = HarnessConfig()
    models: ModelAssignment
    scope: ScopeConfig = ScopeConfig()
    lenses: list[str] = ['mandate', 'examination']
    max_iterations: int = 10
    budget_usd: float = 5.0
    max_tokens_scan: int = 4096     # SCAN phase token budget; 1024 was too small for 5-step reasoning
    max_tokens_implement: int = 4096  # IMPLEMENT phase token budget for full file rewrites
    max_tokens_reflect: int = 400   # REFLECT phase token budget for post-implementation reasoning
    sandbox: str = "docker"  # "docker" | "local"
    allow_dirty: bool = False  # skip the clean-tree gate (operator opt-in)
    verify_command: str = "python -m pytest --tb=no -q"  # empty string disables the test gate

    @field_validator("repo")
    @classmethod
    def repo_must_exist(cls, v: Path) -> Path:
        if not v.exists():
            raise ValueError(f"repo path does not exist: {v}")
        return v.resolve()

    @field_validator("sandbox")
    @classmethod
    def valid_sandbox(cls, v: str) -> str:
        if v not in ("docker", "local"):
            raise ValueError(f"sandbox must be 'docker' or 'local', got: {v!r}")
        return v
