# Destination — AI Steward

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

---

## 2026-06-19 — Token efficiency as architectural constraint

### The constraint

AI Steward must be economically viable at continuous operation. Token cost compounds; a system that burns expensive reasoning on every decision becomes unaffordable regardless of capability. **Token efficiency is not an optimization — it is a design constraint that shapes architecture.**

The harness-protocol is the exemplar: it delivers Observable Autonomy (Principle 2) without consuming any tokens. It's a standalone Rust program that intercepts, logs, and chains evidence at the network layer. The agent never calls an LLM to capture the trail — the trail captures itself structurally.

This is the pattern: **push as much as possible from cognitive (token-consuming) operations into structural (tokenless) mechanisms.**

### Evaluation by layer

**Structural integrity layer (harness-protocol)** — Already tokenless. Evidence capture, hash chaining, tamper detection, provider normalization — all happen without LLM calls. This is the gold standard. Cost: zero tokens.

**Execution layer** — Mostly structural. Sandbox execution, test running, diff generation, rollback mechanics, file operations — none of these require reasoning. They require code. The execution layer should be primarily deterministic Python/Rust, calling LLMs only for the specific moments that require language understanding (e.g., "does this diff match the stated intent?"). Cost: minimal tokens, bounded per phase.

**Reasoning layer** — This is where tokens live, and where discipline matters most. Not every decision needs a reasoning model. The hierarchy:

1. **Structural gates (zero tokens):** File exists? Tests pass? Diff size within bounds? Hash chain intact? These are code, not cognition.
2. **Pattern-matched decisions (cheap tokens):** Routine approvals, standard rejections, format compliance. Small models, short prompts, cached responses where valid.
3. **Situated reasoning (expensive tokens):** Novel situations, ambiguous evidence, cross-cutting trade-offs, convergence judgment. This is where frontier models earn their cost — but only here.

The discipline: **escalate up this hierarchy only when the lower tier cannot decide.** Most pipeline cycles should never reach tier 3.

### Model-tier strategy

Not all reasoning requires the same model. The cost difference between tiers is 10-100x.

| Tier | Use case | Model class | Cost |
|------|----------|-------------|------|
| 0 | Structural checks | None (code) | Zero |
| 1 | Routine classification | Small/fast (Haiku, GPT-4o-mini) | Low |
| 2 | Standard reasoning | Mid-tier (Sonnet, GPT-4o) | Medium |
| 3 | Judgment under ambiguity | Frontier (Opus, o3) | High |

Model-family independence (the reasoning integrity requirement) applies at tier 2 and above. At tier 1, the cost of multi-family verification may exceed the value; the harness captures everything regardless, so the evidence exists for later audit if needed.

### What this means for PEA conformance

AI Steward is a case study. It must demonstrate that earned delegation is viable, not just theoretically sound. If the principles only work with unlimited token budget, they're not a governance discipline — they're a luxury.

The claim to validate: **structural mechanisms can replace cognitive work for most of Observable Autonomy, and the remaining cognitive work can be tiered so that expensive reasoning is rare, not routine.**

The Skills Suite demonstrated the principles at the behavioral layer (instructions that direct reasoning). The harness-protocol demonstrated them at the structural layer (capture that doesn't depend on the agent's compliance). AI Steward must demonstrate them at the **operational layer** — a system that runs continuously, earns trust over time, and remains economically sustainable.

### V1 scope: lightweight

Version 1 must be minimal. Not the full three-layer architecture — the smallest thing that demonstrates the concept works and provides real value.

**V1 definition:** A complete autonomous loop that stops before release. The system can analyze → propose → implement → verify → record without human intervention. It does not push or release — the operator reviews and decides whether to accept. This is full autonomy over the improvement cycle, with a human gate before the world changes.

**What v1 includes:**
- Harness-protocol (`C:\git\harness-protocol`, already built, tokenless)
- A single execution loop: analyze → propose → implement → verify → record
- Tier 0 and tier 1 reasoning only — structural gates and cheap models
- Single-model operation (no model-family independence yet)
- One target repo at a time
- Manual operator trigger to start, autonomous until the loop completes
- Stops with a proposal ready for human review — does not push or release

**What v1 defers:**
- Push and release (human reviews before anything goes out)
- Tier 2/3 reasoning (frontier models, situated judgment)
- Model-family independence for reasoning integrity
- Full Skills suite integration (Improve, Retrospect, Probe)
- Self-targeting
- Convergence-based stopping (use fixed iteration limits instead)
- Continuous unattended operation (multiple cycles without operator)

**Why this ordering:**
The harness proves Observable Autonomy can be structural. V1 proves the execution loop works end-to-end and that tier 0/1 reasoning is sufficient for routine improvements. The human gate before release is both a safety mechanism and a learning opportunity — every review teaches us where the loop's judgment is good enough and where it isn't.

Only after that foundation exists do we add the expensive reasoning machinery — and we add it incrementally, measuring cost/value as we go. Push/release autonomy is earned by demonstrating that the pre-release loop produces consistently acceptable proposals.

### Open questions

- Where exactly is the tier-escalation boundary? What evidence triggers escalation from tier 1 to tier 2?
- Can convergence checking (Principle 3) be partially structural? E.g., "three consecutive runs with identical output" is a structural signal; "three evaluators found nothing to change" requires cognition.
- What's the token budget per pipeline cycle that keeps continuous operation viable? This needs real numbers from Evo's operational history.
- How do we measure "reasoning quality per token" to know if we're trading off correctly?


---

## 2026-06-20 -- V1 milestone clarification: self-targeting

### Correction to the June 19 V1 definition

The June 19 entry listed "Self-targeting" under **What v1 defers**. This is wrong.

Self-targeting is not a V2 feature -- it is the V1 milestone. The destination has always said: *"AI Steward can target any repository, including its own. Self-targeting is not a special mode -- it is the same pipeline pointed at a different directory."* V1 is not complete until this is demonstrated, not just true in principle.

### What V1 done actually means

V1 is done when ai-steward successfully runs the loop against its own repository:

1. i-steward run c:\git\ai-steward executes
2. The loop reads its own code, proposes one improvement, applies it, verifies it, writes the trail entry, and leaves the change staged
3. The operator reviews the staged diff and decides

That first successful self-targeting cycle is the milestone. Not "57 tests pass." Not "all phases exist."

### What happens after

Once the loop runs on itself once, there is no handoff. The loop continues -- each run proposes the next improvement. The operator reviews and accepts or discards each staged proposal. This is the "taking over" moment: ai-steward improving ai-steward, with the operator as reviewer rather than author.

No special treatment for self-targeting. The same pipeline, the same gates, the same trail. The loop does not know or care that it is modifying its own source code.

### What this means for the remaining work

The gap between "structurally complete" and "V1 done" is operational:

1. pyyaml installed in the ai-steward environment
2. .ai-steward.yaml present in c:\git\ai-steward
3. Harness proxy running at localhost:8474
4. First i-steward run c:\git\ai-steward produces a staged proposal

These are not code problems. They are first-run prerequisites.

### What does NOT change

- V1 still stops before release -- operator reviews every staged change
- V1 still uses tier 0/1 reasoning only
- V1 still uses single-model operation
- Harness-protocol remains outside autonomous scope

---

## 2026-06-20 -- Post-V1: ai-steward as PEA reference implementation

### Confirmed direction

**ai-steward is a proof, not just a tool.** If it works well as a tool but cannot serve as a PEA reference implementation -- because the reasoning layer is opaque or the principles are not demonstrably upheld -- that is a failure, even if developers find it useful. The tool is the proof.

**The three principles are architectural constraints.** An undirected SCAN violates Principle 1 (Commander's Intent). V1 achieved operational self-targeting, but is incomplete against the principles. Principle 1 compliance -- directed SCAN that reads the operator's destination -- is the real next milestone.

**ARF probe is operator-triggered.** `ai-steward probe` when the operator wants to verify reasoning quality. Not automatic, not every-N-cycles.

### The cost-efficient memory model

The skill suite memory model (destination.md, retrospect.md, audit-trail.md as unbounded prose) was designed during the token bonanza. It is not cost-efficient enough to become the standard.

ai-steward will define the new standard. The skill suite will align to it later.

**Design principles:**

1. **Structured over prose.** YAML/JSONL with defined schema, not free-form markdown. Structured data can be selectively loaded and validated.

2. **Hard token budgets per artifact.** Enforced at write time. An artifact that exceeds its budget is invalid.

3. **Separation of working memory from audit memory.** The full trail exists for retrospect and external audit, but is NOT loaded into SCAN context.

4. **Sliding window for recent context.** Last N entries, not the full history.

**Proposed structure:**

::

  .ai-steward/
      destination.yaml      # Operator's WHAT and WHY. Max ~200 tokens.
      orientation.yaml      # Current arc orientation (retrospect output). Max ~150 tokens.
      recent.jsonl          # Sliding window of last N trail entries. Max ~300 tokens.
      trail.jsonl           # Full audit trail. Append-only. NOT loaded into SCAN.

SCAN loads destination + orientation + recent = ~650 tokens of memory context.
The full trail is for retrospect and audit, not for every cycle.

**Compatibility path:**

ai-steward defines forward compatibility. The skill suite adopts the new standard when it is proven. Verbose markdown becomes a generated view or is deprecated. ai-steward does not implement backward compatibility to the old format.

### The git gate stays

The loop does not push. It does not release. It cannot act on its own judgment past the staged diff. Every proposal requires the operator's hand on the commit.

This is not a temporary safety measure. It is permanent trust infrastructure. One proposal, one diff, one decision. Trust is earned incrementally. The ledger of accepted proposals IS the evidence that the AI's judgment is reliable.

### What this means for the next work

1. **Design the memory schema** -- YAML/JSONL structure for destination, orientation, recent. Define fields, constraints, token budgets.

2. **Implement directed SCAN** -- SCAN reads destination and orientation, proposes improvements that advance the operator's stated direction.

3. **Implement retrospect** -- Reads full trail, produces orientation.yaml summary. Runs on operator trigger or after N accepted commits.

4. **Implement probe** -- ARF probe per ARF-SPEC.md. Operator-triggered. Reports pass/fail with evidence.

The ordering is: (1) schema, (2) directed SCAN, (3) retrospect, (4) probe. Each builds on the previous.

---

## 2026-06-20 -- Unification: .pea/ as the common standard

### The architectural correction

The TRAIL skill is a behavioral convention — it asks the LLM to append to a markdown file. The LLM is an unreliable narrator of itself. This is a structural problem that cannot be solved with better instructions.

The harness-protocol is the structural solution. It intercepts LLM API traffic and writes a hash-chained ledger before the response is released. The LLM cannot fabricate, omit, or modify entries. Trail integrity becomes a technical guarantee, not a discipline.

### What this means for ai-steward

ai-steward uses Anthropic API keys routed through the harness at localhost:8474. The harness already captures every LLM call to `.harness/sessions/*.jsonl`. The structural trail exists.

The memory model must be redesigned around this fact:

- **The LLM reads from the memory directory.** Destination, orientation, recent context.
- **The LLM does NOT write the authoritative trail.** The harness does.
- **Derived artifacts (orientation, recent) are computed from the harness ledger.**

### One directory, one standard: .pea/

Three systems need context memory:

1. The skill suite (currently .trail/)
2. The harness-protocol (currently .harness/)
3. ai-steward (was going to be .ai-steward/)

These should be ONE directory with ONE standard.

::

  .pea/
      destination.yaml     # Operator-written. Commander's Intent.
      orientation.yaml     # Derived from ledger by retrospect.
      sessions/            # Written by harness-protocol. Hash-chained.
          *.jsonl          # The LLM does NOT write here.
      (derived views)      # recent context computed from sessions/

**Who writes what:**

- `destination.yaml` — Operator. Never the LLM.
- `sessions/*.jsonl` — Harness-protocol. Never the LLM.
- `orientation.yaml` — LLM (retrospect), but derived from sessions/ which LLM did not author.

**The compatibility path:**

ai-steward defines `.pea/` as the standard. The skill suite migrates from `.trail/` to reading/writing `.pea/`. The harness-protocol migrates from `.harness/` to `.pea/sessions/`. One directory, one standard, structural integrity.

### How this maps to the three principles

**Principle 1 (Commander's Intent):** The operator authors `destination.yaml`. The LLM interprets it but does not self-author its instructions.

**Principle 2 (Observable Autonomy):** The harness captures the authoritative record. The LLM cannot be the sole narrator of its own actions. Capture is structural, not behavioral.

**Principle 3 (Convergence Is Silence):** Retrospect reads the harness ledger (which the LLM did not author) and produces orientation. The judgment of what the arc means comes from reading evidence the LLM could not fabricate.

### Relation to AAS-1 proposals

The Agent Audit Trail standard (AAS-1) is defining the schema for autonomous agent records. Two open proposals on the working group:

1. Provenance (§6.9) should capture reasoning traces — the harness already captures this in the `reason` field.
2. Reproducibility (§6.10) for non-deterministic models — reasoning reproducibility, not output-identical reproduction.

ai-steward and the harness-protocol are reference implementations of what AAS-1 is standardizing. Alignment between the .pea/ standard and AAS-1 is a goal.
