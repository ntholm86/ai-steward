"""Configuration schema for ai-steward.

Every design decision lives here in code:
- Which model family handles which pipeline phase (model-family independence principle)
- llm-harness-proxy integration contract (all LLM calls route through the proxy)
- Scope enforcement (allowed/blocked file globs)
- Safety budget (iteration cap and cost cap)
"""

import warnings
from pathlib import Path
from pydantic import BaseModel, field_validator

# Known lens names for the SCAN phase.
# Built-in lenses correspond to Steps 1–2 in the system prompt; extended lenses
# are injected between Step 2 and Step 3 by _build_system_prompt() in scan.py.
_KNOWN_SCAN_LENSES: frozenset[str] = frozenset({
    "mandate", "examination",          # built-in
    "security", "overburden", "performance", "waste",  # extended
})

# Known lens names for the REFLECT phase.
# Built-in lenses correspond to the three numbered reflection items;
# extended lenses are injected after item 3 by _build_reflect_system_prompt().
_KNOWN_REFLECT_LENSES: frozenset[str] = frozenset({
    "prediction", "model_claim", "blind_spot",          # built-in
    "security", "overburden", "performance", "waste",  # extended
})


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
    reflect_lenses: list[str] = ["prediction", "model_claim", "blind_spot"]  # lenses applied in REFLECT phase; default mirrors current three-item structure
    max_iterations: int = 10
    budget_usd: float = 5.0
    max_tokens_scan: int = 4096     # SCAN phase token budget; 1024 was too small for 5-step reasoning
    max_tokens_implement: int = 4096  # IMPLEMENT phase token budget for full file rewrites
    max_tokens_reflect: int = 400   # REFLECT phase token budget for post-implementation reasoning
    acm_scope_depth: int = 4  # how many parent .acm/ directories to consult (org/workspace/team hierarchies)
    destination_budget_chars: int = 3000  # total character budget for destination.md excerpts in SCAN context
    binary_heuristic_bytes: int = 8192  # first N bytes inspected for NUL byte (binary file detection)
    default_skip_dirs: list[str] = [  # directories skipped when scope.allowed is empty
        ".acm", ".git", ".harness",
        "__pycache__", ".mypy_cache", ".pytest_cache",
        "node_modules", ".venv", "venv", ".tox",
    ]
    sandbox: str = "docker"  # "docker" | "local"
    allow_dirty: bool = False  # skip the clean-tree gate (operator opt-in)
    verify_command: str = "python -m pytest --tb=no -q"  # empty string disables the test gate

    @field_validator("lenses")
    @classmethod
    def lenses_known_names(cls, v: list[str]) -> list[str]:
        unknown = [ln for ln in v if ln not in _KNOWN_SCAN_LENSES]
        if unknown:
            warnings.warn(
                f"Unknown lenses will be silently ignored by SCAN: {unknown}. "
                f"Known lenses: {sorted(_KNOWN_SCAN_LENSES)}",
                UserWarning,
                stacklevel=2,
            )
        return v

    @field_validator("reflect_lenses")
    @classmethod
    def reflect_lenses_known_names(cls, v: list[str]) -> list[str]:
        unknown = [ln for ln in v if ln not in _KNOWN_REFLECT_LENSES]
        if unknown:
            warnings.warn(
                f"Unknown reflect_lenses will be silently ignored by REFLECT: {unknown}. "
                f"Known reflect_lenses: {sorted(_KNOWN_REFLECT_LENSES)}",
                UserWarning,
                stacklevel=2,
            )
        return v

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
