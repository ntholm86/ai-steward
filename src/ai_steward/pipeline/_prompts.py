"""LLM prompt templates — loaded from versioned .md files in prompts/.

Same public API pattern as evo's core/_prompts.py.
Templates live in src/ai_steward/pipeline/prompts/*.md for clean diffs and versioning.
"""

from pathlib import Path

_PROMPT_DIR = Path(__file__).parent / "prompts"


def _load(name: str) -> str:
    """Load a prompt template from the prompts/ directory."""
    return (_PROMPT_DIR / f"{name}.md").read_text(encoding="utf-8").rstrip("\n")


# ---------------------------------------------------------------------------
# Public constants — one per LLM phase
# ---------------------------------------------------------------------------

SCAN_SYSTEM = _load("scan_system")
REFLECT_SYSTEM = _load("reflect_system")
IMPLEMENT_SYSTEM = _load("implement_system")
