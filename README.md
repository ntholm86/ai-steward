# ai-steward

An autonomous code improvement loop with structural accountability.

**Purpose 1 - Proof:** A reference implementation of [Principles of Earned Autonomy (PEA)](https://github.com/ntholm86/principles-of-earned-autonomy). It demonstrates that autonomous delegation can be structurally trustworthy through Observable Autonomy, captured by [Agent Evidence Proxy (AEP)](https://github.com/ntholm86/agent-evidence-proxy); Operator's Intent, held in the goal; and Convergence Is Silence, which stops when work is done.

**Purpose 2 - Tool:** Write a goal, run the loop, review the staged diff, then commit or discard. It works on any codebase. Cost is measured, not claimed (~$0.15 to $0.20 per cycle on claude-sonnet-4-5; Haiku is the V2 cost target).

## How it works

```
┌──────────────────────────────────┐
│  OPERATOR                        │
│  Memory: goal.md        │  ← Operator's Intent: what + why
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
│  Writes evidence/*.jsonl         │  ← BEFORE response is processed
│  Hash-chained, tamper-evident    │  ← agent cannot fabricate evidence
└──────────────────────────────────┘
```

Every cycle produces two records in the target repo's memory directory (see [Where memory lives](#where-memory-lives)):
- `audit-trail.md` — the agent's reasoning (what it proposed and why)
- `evidence/<ulid>.jsonl` — the harness-captured LLM evidence (independent, unmodifiable)

The agent cannot claim it did something it did not do.

## Where memory lives

`.acm/` in the diagram above stands for the repository's memory directory:

- **Bound repository:** when the repository is bound to a scope in a shared memory repository, memory is found there. Memory repositories are listed in the registry `~/.acm/memories` (or the file named by `ACM_MEMORIES_FILE`), one absolute path per line, each containing an `.acm-root` file. A repository is bound when exactly one `<memory>/repositories/<id>/repository.json` lists one of its root commits in `root_commits`. Zero matches means unbound; several matches abort with an error — the scope is never guessed. In bound mode the trail is the optional legacy `audit-trail.md` plus `records/` (one create-only file per cycle), `goal.md` may be preceded by a memory-wide `goal.md`, and no parent directories are searched. ai-steward only writes files into the memory working tree; it never commits to the memory repository.
- **Unbound repository (legacy):** memory is the in-repo `.acm/` folder, exactly as before, and `run-loop` commits it with each review-branch commit.

## Quickstart

**Prerequisites:** Python 3.12+, [agent-evidence-proxy](https://github.com/ntholm86/agent-evidence-proxy) running on `localhost:8474`, `ANTHROPIC_API_KEY` set. Start the proxy with `HARNESS_ROOT` set to the memory scope's `evidence/` folder (`.acm/evidence` for a legacy repo); the proxy alone decides where evidence is written, ai-steward only sends a session id.

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

And `goal.md` in the repository's memory (`.acm/goal.md` for a legacy repo, or the bound scope of the shared memory repository; `ai-steward init` creates it in the right place) — write what you want the codebase to become and why:

```markdown
# Goal — my-project

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
- Observable Autonomy structural: harness sessions co-located with the trail in the repository's memory (`.acm/` or its bound scope)
- Operator's Intent structural: SCAN reads the memory's `goal.md` before every proposal
- 187 tests, mypy-clean, CI on GitHub Actions
- Cost baseline: ~$0.15–0.20/cycle (SCAN + IMPLEMENT + REFLECT, claude-sonnet-4-5)

**V2 (in progress)** — four closing conditions, from the GRADUATE-generated proposal: live multi-cycle run with REORIENT firing; external repo run post deletion-guard fix; cost-cap enforcement validated live; compounding-error detection across N≥3 cycles.

## Observable Autonomy

The harness proxy writes the session ledger **before** the LLM response is processed. The agent cannot selectively omit calls, retroactively modify evidence, or claim a reasoning path it did not take. The trail entry (agent-authored) and the JSONL session (harness-captured) are co-located but distinct — two trust levels, one directory.

```
.acm/                     ← legacy in-repo memory (bound repos: <memory>/repositories/<id>/)
  audit-trail.md          ← agent's claim about what happened (bound: records/<timestamp>-<slug>.md)
  evidence/
    01KV....jsonl         ← independent proof of what the LLM was asked and answered
```

## Development

```bash
pip install -e ".[dev]"
pytest          # 187 tests
mypy src/       # type-check
```

CI runs both on push via `.github/workflows/ci.yml`.

---

Author: [Nils Wendelboe Holmager](https://nilsholmager.com/) · [Project context and connected work](https://nilsholmager.com/research/ai-steward/)
