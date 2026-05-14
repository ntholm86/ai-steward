# Vision — AI Steward

*Operator-held destination. Append or layer new insights; never destructively overwrite.*

---

## 2026-05-14 — First articulation

### What this is

AI Steward is an autonomous software evolution engine with a reasoning layer.

It runs continuously without the operator present. It finds improvements, implements them, verifies them, and releases them — in the operator's name. The operator can trust this because every action is logged, every decision is reasoned, and the reasoning is independently verified.

This is **earned delegation**: the system earns the right to act unsupervised by building a verifiable record over time.

### The three layers

**Execution layer** (new — informed by Evo, not derived from it)

Closed-loop pipeline: analyze → propose → implement → verify → decide → release → record. The execution layer does not reason — it executes, verifies, and logs. Reasoning is the job of the reasoning layer.

What to take from Evo: hash-chained proof ledger, rollback, multi-language profiles, sandbox execution, proposal queues.

What to leave: Evo's inline LLM reasoning scattered through ANALYZE and PROPOSE, the lessons journal, the fitness gate as a hard rule, the embedded Kaizen auditor. In Evo, reasoning and execution are mixed. In ai-steward they are separate.

Gates are reasoning decisions, not hard rules. The execution layer presents evidence; the reasoning layer decides whether to accept, reject, or escalate.

**Reasoning layer** (from the Skills suite)

- Vision: persistent operator intent across sessions
- Trail: decisions and reasoning recorded as they happen
- Improve: meta-cognitive improvement loop; silence is a valid outcome
- Retrospect: reads the full arc — is the loop improving the right thing?
- Probe: tests whether reasoning is genuine or pattern-matched

Different model families handle different pipeline phases. Model-family independence is a reasoning integrity mechanism — the model that proposes a change and the model that judges it come from different families, so the judge cannot share the proposer's blind spots.

**Structural integrity layer** (harness-protocol — standalone, separate from ai-steward)

Intercepts all API calls ai-steward makes — any model, any family, any key — and writes the raw stream before the model's response is processed.

The harness must be a separate application. If it were internal, ai-steward could modify its own evidence capture, especially when targeting itself. The capture mechanism must be independent of the thing being captured.

The harness supports all model families. Different providers have different protocols (Anthropic thinking blocks, OpenAI reasoning tokens, Gemini thinking mode, models with no reasoning exposure). The harness normalizes these to a common schema.

The harness scores model transparency per call:
- Thinking tokens / reasoning trace present?
- Tool usage recorded?
- Decision rationale structured?

Models that do not provide a reasoning trail are flagged. The reasoning layer uses this score to calibrate trust in each model's output per pipeline phase.

Two trail types, two trust levels:
- Proxy-captured JSONL: evidence — raw, independent, the agent cannot modify it
- `audit-trail.md`: memory — the agent's record of decisions and reasoning

If they diverge, the proxy wins. The reasoning layer reads both but weights them differently.

The harness-protocol repo is outside ai-steward's autonomous scope. Changes to it require explicit operator action.

### Target model

AI Steward can target any repository, including its own. Self-targeting is not a special mode — it is the same pipeline pointed at a different directory. Scope enforcement, proof trail, and probe verification apply identically.

### Competitive position

Execution pipelines will be common. The reasoning layer is the differentiator — specifically:
- The separation of action integrity (what was done) from reasoning integrity (why, and whether the reasoning was genuine)
- Model-family independence as a structural reasoning guarantee, not a performance choice
- A convergence stopping criterion: the system stops when independent evaluators agree, not when it runs out of ideas

### Visibility

Private until MVP. The trail and vision are also documentation — when published, they are part of the public record, not just internal notes.

### Principles

1. **Commander's Intent** — what + why, never how
2. **Observable Autonomy** — autonomy without evidence is abdication
3. **Convergence Is Silence** — stop when convergence is genuinely earned

Full statement: [Principles of Earned Autonomy](https://github.com/ntholm86/principles-of-earned-autonomy)

