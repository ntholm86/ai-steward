# Vision — AI Steward

*Operator-held destination. Append or layer new insights; never destructively overwrite.*

---

## 2026-05-14 — First articulation

### What this is

AI Steward is an autonomous software evolution engine with a reasoning layer — the system that makes earned delegation real.

It is not an AI coding tool. It is not an agent that waits to be asked. It is a system that runs, improves, releases, and understands itself — continuously — with the operator's structural consent.

The operator sleeps. AI Steward acts in their name. This is only possible because:

1. Every action is tamper-evidently logged (the operator can reconstruct what happened)
2. Every decision is reasoned, not just executed (the operator can see why)
3. The reasoning is tested for fidelity — not just recorded (pattern-matching cannot impersonate genuine reasoning undetected)
4. Operator intent is anchored and persistent across sessions (the system knows what it is for)
5. Convergence is earned by independent agreement, not declared by the system itself

This is **earned delegation**: authority granted because trust was built, not assumed.

### What it is not

- It is not automation. A cron job acts in your name without your knowledge. AI Steward acts in your name with structural consent — every decision is observable and challengeable.
- It is not recursive self-improvement as a risk. It is recursive self-improvement made governable: bounded by scope, anchored to vision, tested for reasoning fidelity, and stopped when convergence is genuinely earned.
- It is not another multi-agent framework. Model-family diversity here is a *reasoning integrity mechanism*, not a performance optimization. The model that proposes a change and the model that judges whether it is Pareto-dominant come from different families — structural independence, not just architectural variety.

### The three layers

**Execution layer** (new — informed by Evo, not derived from it)
Closed-loop pipeline. The execution layer is deliberately dumb: it executes, verifies, and logs. It does not reason. Reasoning is the job of the reasoning layer, not the pipeline.

What to take from Evo: hash-chained proof ledger, rollback mechanism, multi-language profiles, sandbox execution model, proposal queues.

What to leave behind: Evo's inline reasoning — the LLM scattered through ANALYZE, PROPOSE, the lessons journal, the fitness gate as a reasoning shortcut, the Kaizen auditor embedded in the pipeline. In Evo, reasoning and execution are tangled. In ai-steward they are architecturally separate.

Gates also change: Evo's Pareto gate is mechanical ("any metric regression → reject"). In ai-steward, gates are reasoning decisions made by the reasoning layer — with context, nuance, and a trail. The execution layer presents the evidence; the reasoning layer decides.

**Reasoning layer** (from the Skills suite)
The memory model that makes the execution layer governable:
- Vision: persistent operator intent across sessions
- Trail: reasoning recorded as it happens, not summarized after
- Improve: meta-cognitive loop with silence as a valid outcome
- Retrospect: arc-level reading — is the loop looking at the right thing?
- Probe: ARF testing — is the reasoning genuine or pattern-matched?

**Structural integrity layer** (harness-protocol — standalone, not built into ai-steward)

The proxy intercepts ALL API calls ai-steward makes — to any model, any family, any key — and writes them AS-IS before the model's response is processed. This is structural evidence, not an agent self-report.

The harness-protocol is a separate application by necessity. If it were internal to ai-steward, ai-steward could modify its own evidence capture — especially dangerous given that ai-steward targets itself. Structural independence of the capture mechanism from the thing being captured is the integrity guarantee. It cannot be negotiated away.

**The harness must support all model families.** Different providers have different response protocols — Anthropic extended thinking blocks, OpenAI reasoning tokens, Gemini thinking mode, and models that expose nothing at all. The harness normalizes these into a common schema and captures whatever the model exposes.

**The harness surfaces model transparency.** For every API call, it evaluates what the model actually provided:
- Thinking tokens / reasoning trace present?
- Tool usage recorded?
- Decision rationale structured?
- Response matches the reasoning exposed?

Models that do not provide a proper reasoning trail are flagged. This makes the harness a **model trustworthiness classifier** — not just a recorder. The reasoning layer uses this signal to calibrate how much weight to give each model's output in each pipeline phase. A model with a low transparency score should only be used where its output is independently verified by a higher-transparency model.

**The dual-use of the trail:** The proxy-captured JSONL is evidence (ground truth, independently captured, tamper-evident by the agent). The `audit-trail.md` is memory (the agent's interpretation of events). They serve different trust levels. If they diverge, the proxy wins. The reasoning layer reads both but treats them differently.

**Scope enforcement:** The harness-protocol repo is outside ai-steward's autonomous improvement scope by default. Changes to it require explicit operator action — they do not go through the autonomous loop.

### The moat

Anyone can build an execution pipeline. AI is here; Evo-style engines will be common within months.

The moat is the reasoning layer — specifically the clarity about *what it does*:

- It is not "add memory to an agent"
- It is the difference between *action integrity* (what was done is logged) and *reasoning integrity* (why it was done, and whether the reasoning was genuine)
- It uses model-family independence as a structural guarantee of reasoning fidelity
- It has a stopping criterion: convergence is earned when independent evaluators agree, not when the system runs out of ideas

That framing is not obvious. Most people building in this space cannot see it clearly. That is the advantage.

### End state

AI Steward runs without the operator at the computer. It finds real improvements, implements them, verifies them, releases them — in the operator's name. Not as a one-time demonstration. Continuously, as normal operation.

"While you sleep" is a figure of speech for earned unsupervised operation — not a specific milestone event. The destination is the system itself, running trustworthily. Trust is built run by run through the trail, not declared at a launch moment.

### Target model

AI Steward can target **any repository** — including its own.

This is not an edge case. It is the point. A system that can improve any codebase but cannot improve itself is a tool. A system that can improve itself, with the same reasoning layer and audit trail it applies to everything else, is an agent that earns delegation.

The self-targeting case is the hardest and the most important:
- The scope enforcement that prevents the engine from modifying what it shouldn't must apply to itself
- The proof trail for self-modifications must be indistinguishable in structure from trails for external targets
- The Probe layer must be able to test whether self-improvement reasoning is genuine — not just whether self-improvement happened
- The hash-chained ledger means self-modifications cannot be silently undone or rewritten

Self-targeting is not a special mode. It is the same pipeline pointed at a different directory.

### Visibility

Private until MVP. The trail and vision are also documentation — when published, they are part of the public argument, not just internal records.

### Principles

The three principles from the manifesto hold unchanged:

1. **Commander's Intent** — what + why, never how
2. **Observable Autonomy** — autonomy without evidence is abdication
3. **Convergence Is Silence** — the system stops when convergence is genuinely earned

Full statement: [Principles of Earned Autonomy](https://github.com/ntholm86/principles-of-earned-autonomy)
