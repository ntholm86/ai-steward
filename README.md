# ai-steward

An autonomous code improvement loop with structural accountability.

**Purpose 1 — Proof:** A reference implementation of [Principles of Earned Autonomy](https://github.com/ntholm86/manifesto). Demonstrates that autonomous delegation can be structurally trustworthy — not through promises, but through Observable Autonomy (harness-captured LLM evidence), Operator's Intent (operator-written destination), and Convergence Is Silence (stop when done, not when tired).

**Purpose 2 — Tool:** Genuinely useful. Write a destination → run the loop → review the staged diff → commit or discard. Works on any codebase. Cost is measured, not claimed (~$0.15–0.20/cycle on claude-sonnet-4-5; haiku is the V2 cost target).

## How it works

```
┌──────────────────────────────────┐
│  OPERATOR                        │
│  .acm/destination.md           │  ← Operator's Intent: what + why
│  Reviews staged diffs            │
│  Commits or discards             │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  PIPELINE                        │
│  PRE-FLIGHT → SCAN → IMPLEMENT   │
│           → VERIFY → RECORD      │
│                                  │
│  • PRE-FLIGHT: git clean, tests  │  ← zero LLM tokens
│  • SCAN: read files + dest → LLM │  ← one cheap model call
│  • IMPLEMENT: apply change → LLM │  ← one cheap model call
│  • VERIFY: syntax, size, tests   │  ← zero LLM tokens
│  • RECORD: append trail entry    │  ← zero LLM tokens
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  HARNESS (localhost:8474)        │
│  Intercepts all LLM API calls    │
│  Writes .acm/sessions/*.jsonl  │  ← BEFORE response is processed
│  Hash-chained, tamper-evident    │  ← agent cannot fabricate evidence
└──────────────────────────────────┘
```

Every cycle produces two records in the target repo's `.acm/` directory:
- `audit-trail.md` — the agent's reasoning (what it proposed and why)
- `sessions/<ulid>.jsonl` — the harness-captured LLM evidence (independent, unmodifiable)

The agent cannot claim it did something it did not do.

## Quickstart

**Prerequisites:** Python 3.12+, [llm-harness-proxy](https://github.com/ntholm86/llm-harness-proxy) running on `localhost:8474`, `ANTHROPIC_API_KEY` set.

```bash
pip install -e ".[dev]"
```

**In your target repo**, create `.ai-steward.yaml`:

```yaml
models:
  analyze: claude-haiku-4-5
  propose: claude-haiku-4-5
  implement: claude-haiku-4-5
  verify: claude-haiku-4-5
  judge: claude-haiku-4-5
```

And `.acm/destination.md` — write what you want the codebase to become and why:

```markdown
# Destination — my-project

What this is for and what a good improvement looks like.
The agent reads this before every SCAN. Be honest about trade-offs.
```

**Run:**

```bash
ai-steward run /path/to/your/repo
```

The loop proposes one change, applies it, verifies tests pass, and stages the diff. You inspect and commit or discard.

## V1 status — ACHIEVED (GRADUATE classification, 2026-06-22)

- Self-targeting proven: ai-steward runs against its own repository; convergence confirmed by consecutive NOTHING FOUND cycles
- Meta-cognitive layer implemented and auto-triggered: REORIENT, GRADUATE, ESCALATE
- Observable Autonomy structural: harness sessions co-located with trail in `.acm/`
- Operator's Intent structural: SCAN reads `.acm/destination.md` before every proposal
- 187 tests, mypy-clean, CI on GitHub Actions
- Cost baseline: ~$0.15–0.20/cycle (SCAN + IMPLEMENT + REFLECT, claude-sonnet-4-5)

**V2 (in progress)** — four closing conditions, from the GRADUATE-generated proposal: live multi-cycle run with REORIENT firing; external repo run post deletion-guard fix; cost-cap enforcement validated live; compounding-error detection across N≥3 cycles.

## Observable Autonomy

The harness proxy writes the session ledger **before** the LLM response is processed. The agent cannot selectively omit calls, retroactively modify evidence, or claim a reasoning path it did not take. The trail entry (agent-authored) and the JSONL session (harness-captured) are co-located but distinct — two trust levels, one directory.

```
.acm/
  audit-trail.md          ← agent's claim about what happened
  sessions/
    01KV....jsonl         ← independent proof of what the LLM was asked and answered
```

## Development

```bash
pip install -e ".[dev]"
pytest          # 187 tests
mypy src/       # type-check
```

CI runs both on push via `.github/workflows/ci.yml`.
