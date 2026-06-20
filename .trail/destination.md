# Destination — AI Steward

*Operator-held destination. Append or layer new insights; never destructively overwrite.*

---

## Current State (consolidated 2026-06-20)

### What ai-steward is

An autonomous software improvement engine that:
1. **Reads** the operator's destination (what + why)
2. **Proposes** one improvement per cycle
3. **Applies** the change
4. **Verifies** tests still pass
5. **Stages** the result for human review

The operator commits or discards. Trust is earned one accepted proposal at a time.

### Dual purpose

**Purpose 1 — Proof:** ai-steward is a reference implementation of the Principles of Earned Autonomy. It demonstrates that autonomous delegation can be structurally trustworthy — not through promises, but through Observable Autonomy (harness-captured evidence), Commander's Intent (operator-written destination), and Convergence Is Silence (stop when done, not when tired).

**Purpose 2 — Tool:** ai-steward must be genuinely useful and widely adoptable. The workflow is simple: write a destination → run the loop → review staged changes → commit. It works on any codebase. Adoption depends on cost-efficiency being *provable* — not claimed, measured.

Both purposes are essential. A proof that nobody uses proves nothing. A tool that violates the principles is just another black box.

### The architecture

```
┌─────────────────────────────────────────────────────────┐
│  OPERATOR                                               │
│  - Writes .trail/destination.md (Commander's Intent)    │
│  - Reviews staged diffs                                 │
│  - Commits or discards                                  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  PIPELINE (ai-steward)                                  │
│  PRE-FLIGHT → SCAN → IMPLEMENT → VERIFY → RECORD        │
│  - Tier 0: structural checks (zero tokens)              │
│  - Tier 1: cheap models (haiku) for routine work        │
│  - Tier 2+: deferred until V1 proves the baseline       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  HARNESS (localhost:8474)                               │
│  - Intercepts all LLM API calls                         │
│  - Writes .trail/sessions/*.jsonl BEFORE response       │
│  - Hash-chained, tamper-evident                         │
│  - The agent cannot fabricate evidence                  │
└─────────────────────────────────────────────────────────┘
```

### Cost model

V1 target: **~$0.002 per improvement cycle** (haiku, 2 LLM calls).

Every trail entry records:
- SCAN tokens (input/output)
- IMPLEMENT tokens (input/output)
- Estimated cycle cost in USD
- Link to harness session (independent evidence)

Efficiency is measured, not claimed. Improvements are evaluated against cost-per-accepted-proposal.

### V1 milestone

V1 is done when ai-steward successfully runs the loop against **its own repository**:
1. `ai-steward run c:\git\ai-steward` executes
2. The loop proposes one improvement, applies it, verifies it, records the trail
3. The operator reviews and commits

Self-targeting is the validation gate. If it can improve itself under its own discipline, the proof holds.

### Development principles

- **KISS:** Each phase does exactly one thing.
- **YAGNI:** V2 features ship after V1 data proves they're needed.
- **DRY:** Shared logic extracted (e.g., `_load_destination()`).
- **Solve by design:** Structure prevents misbehavior; tests verify behavior.

### What remains for V1

1. **P1 compliance:** SCAN must produce trail entries with visible reasoning (lenses, predictions, `[!DECISION]`). This is a `record.py` change.
2. **Self-targeting gate:** Both P1 (reasoning quality) and P2 (harness capture) must be structurally complete before self-targeting runs are merged to main.

### Post-V1 direction

- Retrospect (arc-level orientation from harness ledger)
- ARF probe (operator-triggered reasoning fidelity check)
- Tier escalation (when cheap models can't decide)
- Multi-family verification (proposer ≠ judge)
- Push/release autonomy (earned after N accepted proposals)

---

# Historical Record

*The sections below preserve the evolution of this destination. Newest entries win on conflicts.*

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

---

## 2026-06-20 -- Scope expansion: cross-project memory model convergence

### The full scope of work

The `.pea/` unification is not just ai-steward work. It requires coordinated changes across three projects:

1. **ai-steward** — reads destination + derives context from sessions/ — the consumer
2. **harness-protocol** — writes to `.pea/sessions/` instead of `.harness/sessions/` — the producer
3. **skill suite** — migrates from `.trail/` to `.pea/` — the legacy system

### What has NOT converged

The memory model schema is not yet defined. The token budget constraints are stated (~200 destination, ~150 orientation, ~300 recent) but the actual YAML/JSONL structure that achieves those budgets under real usage has not been designed.

**Open design questions:**

- What fields in `destination.yaml`? How do we compress the skill suite's free-form prose into structured data that fits in ~200 tokens?
- How does `orientation.yaml` get derived from `sessions/*.jsonl`? What's the summarization strategy?
- What is "recent context"? Last N entries? Last N tokens? Entries from the last M hours? How is it computed from the harness ledger?
- How does the harness know to write to `.pea/sessions/`? Is it HARNESS_ROOT pointing to `.pea/`? A new config option?
- What migration path for existing `.trail/` and `.harness/` directories?

### The convergence path

The memory model standard will be defined through ai-steward development. The pattern:

1. **ai-steward implements first.** Design choices are made, tested against real usage, refined.
2. **The standard crystallizes.** Once ai-steward proves the model works cost-efficiently, it becomes the standard.
3. **harness-protocol aligns.** Config option or default change to write to `.pea/sessions/`.
4. **skill suite aligns.** Instructions updated to read/write `.pea/` instead of `.trail/`.

ai-steward is the proving ground. The other projects align to what works.

### What this means for the work ahead

The next milestone is not "implement directed SCAN." It is:

**Define the `.pea/` memory model schema such that:**

- destination.yaml fits in ~200 tokens and captures Commander's Intent
- orientation.yaml fits in ~150 tokens and captures current arc orientation
- recent context derivation from sessions/ fits in ~300 tokens
- The schema is implementable in ai-steward, adoptable by harness and skills

This is design work before implementation. The schema must converge before the code does.

---

## 2026-06-20 -- Correction: Context Memory is a standard, not a project artifact

### The naming problem

`.pea/` names the directory after the Principles of Earned Autonomy project. That's backwards. A common standard should be named for **what it is**, not **where it came from**.

The directory holds **context memory** — the working memory an agent reads at the start of a run and the evidence trail the harness writes during execution. The name should say that.

### The standardization insight

The schema should not be defined in ai-steward's documentation. It should live in **its own repository** — a formal schema definition that:

- Declares the directory structure
- Declares file formats (YAML, JSONL)
- Declares field schemas with validation rules
- Declares token budget constraints
- Is versioned independently

ai-steward, harness-protocol, and the skill suite all **reference and conform to** this standard. They are consumers of the schema, not authors of it.

### What this means

1. **New repository needed:** A "context-memory" or similarly named repo that defines the standard. This is the authoritative schema source.

2. **Directory name TBD:** Not `.pea/`. Something that describes function: `.context/`, `.memory/`, `.agent-context/`, or similar. The name will be decided when the schema repo is created.

3. **Relationship clarified:**
   - The schema repo defines the standard
   - ai-steward is an early implementer (may influence schema design)
   - harness-protocol produces data conforming to the schema
   - skill suite consumes and produces data conforming to the schema

4. **ai-steward's role shifts:** From "defines the standard" to "implements the standard and provides feedback on whether the schema works under real usage."

### What does NOT change

- The token budget constraints (~200 destination, ~150 orientation, ~300 recent)
- The principle that harness writes the authoritative trail, not the LLM
- The principle that schema design precedes implementation
- The convergence order (ai-steward implements first, proves it works, others align)

### Open questions for the schema repo

- What directory name? (Must describe function, not origin)
- What file format for the schema definition? (JSON Schema? YAML schema? Prose + examples?)
- What versioning scheme?
- How do conforming implementations declare which schema version they target?

---

## 2026-06-20 -- Decision: .trail/ is the standard

The naming discussion is closed. `.trail/` is the standard directory name.

**Rationale:** The skill suite already uses `.trail/`. It works. Changing the name for theoretical purity adds migration cost with no practical benefit. The standard can evolve in the future if needed, but the current convention is the starting point.

**What this means:**

1. ai-steward uses `.trail/` (not `.pea/`, not `.context/`)
2. harness-protocol writes to `.trail/sessions/` (not `.harness/`)
3. skill suite continues as-is
4. Schema repo (if created) defines the `.trail/` structure

The prior discussion about naming was premature optimization. Ship with what works.


---

## 2026-06-20 -- Cost-efficiency as a first-class measurement goal

### The missing axis

ai-steward makes real API calls with real cost. Claims about improvement mean nothing without the cost side of the ledger. "V2 is better than V1" is an assertion; "V2 achieves the same improvement quality at 40% lower token cost" is evidence.

Cost-efficiency must be a declared measurement dimension alongside improvement quality — not an afterthought.

### What to measure

- **Tokens per improvement cycle** — SCAN + IMPLEMENT + VERIFY call counts, prompt tokens, completion tokens, total cost in USD. Captured by the harness ledger already; needs surfacing.
- **Cost per accepted improvement** — improvements that reach a passing VERIFY are the unit of value. Cost = total tokens spent in the cycle that produced the accepted improvement.
- **Cost trend over iterations** — if the architecture improves, cost per accepted improvement should decrease or quality should increase at equal cost. Flat or rising cost with flat quality is a signal the loop is not converging.

### ROI definition

ROI = quality of accepted improvements / total token cost

"Quality" is measured by the harness trail (accepted by VERIFY, not reverted). "Cost" is measured by the ledger. Both sides are auditable structural evidence — not self-reported.

### Why this matters for the skills

The skill suite runs in Copilot Chat (Copilot token budget, no direct cost visibility) and in AI-steward cycles (paid API calls, full cost visibility). The discipline is the same in both contexts:

- A skill that requires 10 LLM calls to do what 1 call should do is a structural waste, not a style choice.
- Token budget constraints in skill prompts (~200 tokens for destination, ~150 for orientation) are cost constraints, not just window constraints.
- Improvements to prompt efficiency are as valuable as improvements to output quality.

### Implementation direction

1. **Harness ledger already captures token counts** — no new data needed.
2. **Surface cost per cycle** — ai-steward run output should report: total tokens, estimated USD cost, tokens per phase.
3. **Record cost in trail entries** — each improve iteration's trail entry should include the token cost of that cycle.
4. **Track trend** — retrospect.md should include a cost-trend claim when enough data exists.
5. **Establish a baseline** — the first N runs establish the baseline cost per accepted improvement. Future architectural changes are evaluated against it.

### What counts as improvement

An architectural change that reduces cost-per-accepted-improvement by X% is evidence of improvement — independently of whether the output "feels better." This is the same structural-evidence discipline the manifesto applies to reasoning fidelity: eliminate subjective claims, replace with auditable measurement.


---

## 2026-06-20 -- Self-targeting gate and development principles

### Self-targeting is a milestone, not a mode

ai-steward can target any repository, including its own. But self-targeting before the system earns it produces a demonstration of compliance, not a demonstration of Observable Autonomy. For ai-steward to serve as a PEA integration exemplar, two structural preconditions must hold before the first self-targeting run:

**Precondition 1 -- P2 (Observable Autonomy) is structurally complete**

The two-tier trust model must be functional end-to-end:
- Harness sessions land in `.trail/sessions/` (co-located with `audit-trail.md`) -- done.
- Every trail entry references the harness session by path -- done.
- The link is verifiable: the referenced JSONL exists independently and cannot be modified by the agent.

What is NOT yet done: the trail entry is still self-reported reasoning. The harness proves the *call happened*, but the *reasoning in the trail entry* is the agent's own account of what it decided and why. For full P2, the reasoning trace must either come from the harness (structural capture) or be independently verifiable. This is an open design question.

**Precondition 2 -- P1 (Commander's Intent) + reasoning quality**

The pipeline's reasoning layer must be at least as rigorous as the skill suite:
- SCAN must apply structured reasoning: lenses, pre-commit prediction, blind spot identification
- SCAN must make the reasoning visible in the trail entry -- not just the JSON finding
- IMPLEMENT must also receive the destination (Commander's Intent is currently SCAN-only)
- The operator must be able to read a pipeline trail entry and verify that the reasoning was sound, not just that the change was applied

*Open question:* "Reasoning layer as good as the skillset" -- does this mean SCAN should produce a trail entry that looks like an improve skill entry (lenses, [!DECISION], [!REALIZATION])? Or does it mean the *outcomes* should be equivalently sound? The implementation differs. Operator clarification needed before building.

**The gate rule:** Do not merge a self-targeting run into the main trail until both preconditions are met. Runs before the gate are experiments, not evidence.

---

### Development principles: KISS, YAGNI, DRY

These are structural constraints on how ai-steward itself is built -- not general advice.

**KISS (Keep It Simple):** Each pipeline phase does exactly one thing. SCAN identifies one improvement. IMPLEMENT applies one change. VERIFY checks one invariant set. Complexity that serves multiple purposes belongs in configuration, not in phase logic. If a phase needs to do two things, that is a signal to split it, not to add a branch.

**YAGNI (You Aren't Gonna Need It):** V2 features do not ship before V1 is proven. The tier-escalation boundary, multi-family model verification, concurrent runs, proposal queues -- these are not built until V1 has established a baseline of cost-per-accepted-improvement and shown where the bottleneck actually is. Building V2 infrastructure before V1 data exists is speculation, not engineering.

**DRY (Don't Repeat Yourself):** Prompt construction logic, file collection, trail appending -- these are not duplicated across phases. If two phases do the same thing, it is extracted. The `_load_destination()` function is the model: one place, used by any phase that needs it.

These principles apply to the pipeline code. They do not apply to trail entries and destination sections -- prose that appears to repeat is often reinforcing, not duplicating.

---

### The cost-quality operating point

ai-steward must operate on the **cost-efficiency frontier** -- the Pareto-optimal balance where:

- Reducing cost further would degrade improvement quality below the acceptance threshold
- Improving quality further would not justify the additional cost per accepted improvement

This applies on two axes simultaneously:

**Reasoning quality axis:** Model and tier selection. A cheaper model (haiku) reasons faster and costs less but produces lower-quality proposals. A more expensive model (sonnet, opus) reasons better but costs more per cycle. The right operating point is not the cheapest model -- it is the model where additional cost would not materially improve proposal acceptance rate. This is empirically determined, not assumed.

**Output quality axis:** Context and prompt design. More context (larger destination excerpt, more file content) produces better-targeted proposals but costs more tokens. Less context is cheaper but produces less directed proposals. The right operating point is not maximum context -- it is the context window where additional tokens produce diminishing returns on proposal quality.

**The constraint:** Architecture decisions are evaluated against cost-efficiency, not either axis alone. A change that improves proposal quality but doubles cycle cost is not an improvement unless the quality gain is proportionally demonstrated. A change that halves cycle cost but degrades acceptance rate is not an improvement either.

**How to find the frontier:** Run baseline N cycles at current settings. Measure cost-per-accepted-improvement. Then vary one parameter (model, context window, prompt design) and measure the delta. The frontier is where the delta in quality matches the delta in cost. This requires the cost measurement infrastructure already in place.

**The operating principle:** Start cheap (V1 is haiku, 2 calls, ~.002/cycle). Move toward the frontier as data accumulates. Never move away from it on instinct alone.


---

## 2026-06-20 -- Development principle: Solve by design

The best design makes the bug impossible. Catching errors at runtime is defense in depth; preventing them by construction is defense in kind.

**What this means for ai-steward:**

- Path validation in SCAN rejects `..` and absolute paths by structure — the code cannot construct an out-of-scope path, not merely refuses to when asked.
- The harness writes evidence before releasing the response — the response cannot reach the caller without the ledger entry existing. Observable Autonomy is structural, not behavioral.
- Token cost is captured from the API response, not self-reported — the agent cannot misstate its own cost.
- Session path is discovered by before/after directory scan, not passed from the LLM call — the agent cannot fabricate a session reference.

If a bug requires the system to be "working correctly" to prevent it, the design is not defensive enough. The question to ask: *can this fail silently?* If yes, add a structural constraint that makes silent failure impossible.

This principle supersedes "add a test." Tests verify behavior; structure prevents misbehavior. Both are needed, but structure comes first.

---

## 2026-06-20 -- Decision: Reasoning layer structural equivalence

*Closes the open question from the self-targeting gate section.*

**Question:** "Reasoning layer as good as the skillset" — does this mean SCAN should produce a trail entry that looks like an improve skill entry (lenses, predictions, `[!DECISION]` markers), or does it mean the *outcomes* are equivalently sound?

**Decision from destination:** Structural equivalence. The destination says:

- "every decision is reasoned, and the reasoning is independently verified"
- "Trail: decisions and reasoning recorded as they happen"
- "The separation of action integrity (what was done) from reasoning integrity (why, and whether the reasoning was genuine)"

The skill suite trail format (lenses, predictions, `[!DECISION]`, `[!REALIZATION]`, `[!REVERSAL]`) is the established pattern for visible reasoning. If ai-steward is the PEA exemplar, and P2 requires the reasoning to be visible, then the trail entries must show the reasoning structure — not just the outcomes.

**Implication:** SCAN must produce trail entries that include:
- Which lenses were applied and what each revealed
- A pre-commit prediction of what the change will achieve
- A named blind spot this run did not examine
- `[!DECISION]` marker on the chosen finding
- `[!REVERSAL]` if the prediction was wrong (captured in the next run when VERIFY data is available)

This is a significant expansion of SCAN's responsibilities. Currently SCAN returns a JSON blob; to meet this requirement it must return (or the trail entry must synthesize) structured reasoning in the same format as an improve skill entry.

**What this does NOT mean:** The prompt sent to the model need not change. The *capture* of the reasoning must change. The model's raw output (JSON finding) plus the context (destination, files examined, lenses applied) must be recorded in the trail entry with the same structure as improve skill entries. This is a record.py change, not a scan.py change — the reasoning is already implicit in what was examined and what was proposed; the change is making it explicit in the trail.

**Next step:** Refactor `record.py` to produce improve-skill-style trail entries from the Finding + context already available. No new LLM calls required; this is structural capture of reasoning that is already happening.
