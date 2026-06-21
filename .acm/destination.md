# Destination â€” AI Steward

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

**Purpose 1 â€” Proof:** ai-steward is a reference implementation of the Principles of Earned Autonomy. It demonstrates that autonomous delegation can be structurally trustworthy â€” not through promises, but through Observable Autonomy (harness-captured evidence), Commander's Intent (operator-written destination), and Convergence Is Silence (stop when done, not when tired).

**Purpose 2 â€” Tool:** ai-steward must be genuinely useful and widely adoptable. The workflow is simple: write a destination â†’ run the loop â†’ review staged changes â†’ commit. It works on any codebase. Adoption depends on cost-efficiency being *provable* â€” not claimed, measured.

Both purposes are essential. A proof that nobody uses proves nothing. A tool that violates the principles is just another black box.

### The architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  OPERATOR                                               â”‚
â”‚  - Writes .acm/destination.md (Commander's Intent)    â”‚
â”‚  - Reviews staged diffs                                 â”‚
â”‚  - Commits or discards                                  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â”‚
                          â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  PIPELINE (ai-steward)                                  â”‚
â”‚  PRE-FLIGHT â†’ SCAN â†’ IMPLEMENT â†’ VERIFY â†’ RECORD        â”‚
â”‚  - Tier 0: structural checks (zero tokens)              â”‚
â”‚  - Tier 1: cheap models (haiku) for routine work        â”‚
â”‚  - Tier 2+: deferred until V1 proves the baseline       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â”‚
                          â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  HARNESS (localhost:8474)                               â”‚
â”‚  - Intercepts all LLM API calls                         â”‚
â”‚  - Writes .acm/sessions/*.jsonl BEFORE response       â”‚
â”‚  - Hash-chained, tamper-evident                         â”‚
â”‚  - The agent cannot fabricate evidence                  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
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
1. `ai-steward run c:\git\pea\ai-steward` executes
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
- Multi-family verification (proposer â‰  judge)
- Push/release autonomy (earned after N accepted proposals)

---

# Historical Record

*The sections below preserve the evolution of this destination. Newest entries win on conflicts.*

---

## 2026-05-14 â€” First articulation

### What this is

AI Steward is an autonomous software evolution engine with a reasoning layer.

It runs continuously without the operator present. It finds improvements, implements them, verifies them, and releases them â€” in the operator's name. The operator can trust this because every action is logged, every decision is reasoned, and the reasoning is independently verified.

This is **earned delegation**: the system earns the right to act unsupervised by building a verifiable record over time.

### The three layers

**Execution layer** (new â€” informed by Evo, not derived from it)

Closed-loop pipeline: analyze â†’ propose â†’ implement â†’ verify â†’ decide â†’ release â†’ record. The execution layer does not reason â€” it executes, verifies, and logs. Reasoning is the job of the reasoning layer.

What to take from Evo: hash-chained proof ledger, rollback, multi-language profiles, sandbox execution, proposal queues.

What to leave: Evo's inline LLM reasoning scattered through ANALYZE and PROPOSE, the lessons journal, the fitness gate as a hard rule, the embedded Kaizen auditor. In Evo, reasoning and execution are mixed. In ai-steward they are separate.

Gates are reasoning decisions, not hard rules. The execution layer presents evidence; the reasoning layer decides whether to accept, reject, or escalate.

**Reasoning layer** (from the Skills suite)

- destination: persistent operator intent across sessions
- Trail: decisions and reasoning recorded as they happen
- Improve: meta-cognitive improvement loop; silence is a valid outcome
- Retrospect: reads the full arc â€” is the loop improving the right thing?
- Probe: tests whether reasoning is genuine or pattern-matched

Different model families handle different pipeline phases. Model-family independence is a reasoning integrity mechanism â€” the model that proposes a change and the model that judges it come from different families, so the judge cannot share the proposer's blind spots.

**Structural integrity layer** (harness-protocol â€” standalone, separate from ai-steward)

Intercepts all API calls ai-steward makes â€” any model, any family, any key â€” and writes the raw stream before the model's response is processed.

The harness must be a separate application. If it were internal, ai-steward could modify its own evidence capture, especially when targeting itself. The capture mechanism must be independent of the thing being captured.

The harness supports all model families. Different providers have different protocols (Anthropic thinking blocks, OpenAI reasoning tokens, Gemini thinking mode, models with no reasoning exposure). The harness normalizes these to a common schema.

The harness scores model transparency per call:
- Thinking tokens / reasoning trace present?
- Tool usage recorded?
- Decision rationale structured?

Models that do not provide a reasoning trail are flagged. The reasoning layer uses this score to calibrate trust in each model's output per pipeline phase.

Two trail types, two trust levels:
- Proxy-captured JSONL: evidence â€” raw, independent, the agent cannot modify it
- `audit-trail.md`: memory â€” the agent's record of decisions and reasoning

If they diverge, the proxy wins. The reasoning layer reads both but weights them differently.

The harness-protocol repo is outside ai-steward's autonomous scope. Changes to it require explicit operator action.

### Target model

AI Steward can target any repository, including its own. Self-targeting is not a special mode â€” it is the same pipeline pointed at a different directory. Scope enforcement, proof trail, and probe verification apply identically.

### Competitive position

Execution pipelines will be common. The reasoning layer is the differentiator â€” specifically:
- The separation of action integrity (what was done) from reasoning integrity (why, and whether the reasoning was genuine)
- Model-family independence as a structural reasoning guarantee, not a performance choice
- A convergence stopping criterion: the system stops when independent evaluators agree, not when it runs out of ideas

### Visibility

Private until MVP. The trail and vision are also documentation â€” when published, they are part of the public record, not just internal notes.

### Principles

1. **Commander's Intent** â€” what + why, never how
2. **Observable Autonomy** â€” autonomy without evidence is abdication
3. **Convergence Is Silence** â€” stop when convergence is genuinely earned

Full statement: [Principles of Earned Autonomy](https://github.com/ntholm86/principles-of-earned-autonomy)

---

## 2026-06-19 â€” Token efficiency as architectural constraint

### The constraint

AI Steward must be economically viable at continuous operation. Token cost compounds; a system that burns expensive reasoning on every decision becomes unaffordable regardless of capability. **Token efficiency is not an optimization â€” it is a design constraint that shapes architecture.**

The harness-protocol is the exemplar: it delivers Observable Autonomy (Principle 2) without consuming any tokens. It's a standalone Rust program that intercepts, logs, and chains evidence at the network layer. The agent never calls an LLM to capture the trail â€” the trail captures itself structurally.

This is the pattern: **push as much as possible from cognitive (token-consuming) operations into structural (tokenless) mechanisms.**

### Evaluation by layer

**Structural integrity layer (harness-protocol)** â€” Already tokenless. Evidence capture, hash chaining, tamper detection, provider normalization â€” all happen without LLM calls. This is the gold standard. Cost: zero tokens.

**Execution layer** â€” Mostly structural. Sandbox execution, test running, diff generation, rollback mechanics, file operations â€” none of these require reasoning. They require code. The execution layer should be primarily deterministic Python/Rust, calling LLMs only for the specific moments that require language understanding (e.g., "does this diff match the stated intent?"). Cost: minimal tokens, bounded per phase.

**Reasoning layer** â€” This is where tokens live, and where discipline matters most. Not every decision needs a reasoning model. The hierarchy:

1. **Structural gates (zero tokens):** File exists? Tests pass? Diff size within bounds? Hash chain intact? These are code, not cognition.
2. **Pattern-matched decisions (cheap tokens):** Routine approvals, standard rejections, format compliance. Small models, short prompts, cached responses where valid.
3. **Situated reasoning (expensive tokens):** Novel situations, ambiguous evidence, cross-cutting trade-offs, convergence judgment. This is where frontier models earn their cost â€” but only here.

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

AI Steward is a case study. It must demonstrate that earned delegation is viable, not just theoretically sound. If the principles only work with unlimited token budget, they're not a governance discipline â€” they're a luxury.

The claim to validate: **structural mechanisms can replace cognitive work for most of Observable Autonomy, and the remaining cognitive work can be tiered so that expensive reasoning is rare, not routine.**

The Skills Suite demonstrated the principles at the behavioral layer (instructions that direct reasoning). The harness-protocol demonstrated them at the structural layer (capture that doesn't depend on the agent's compliance). AI Steward must demonstrate them at the **operational layer** â€” a system that runs continuously, earns trust over time, and remains economically sustainable.

### V1 scope: lightweight

Version 1 must be minimal. Not the full three-layer architecture â€” the smallest thing that demonstrates the concept works and provides real value.

**V1 definition:** A complete autonomous loop that stops before release. The system can analyze â†’ propose â†’ implement â†’ verify â†’ record without human intervention. It does not push or release â€” the operator reviews and decides whether to accept. This is full autonomy over the improvement cycle, with a human gate before the world changes.

**What v1 includes:**
- Harness-protocol (`C:\git\harness-protocol`, already built, tokenless)
- A single execution loop: analyze â†’ propose â†’ implement â†’ verify â†’ record
- Tier 0 and tier 1 reasoning only â€” structural gates and cheap models
- Single-model operation (no model-family independence yet)
- One target repo at a time
- Manual operator trigger to start, autonomous until the loop completes
- Stops with a proposal ready for human review â€” does not push or release

**What v1 defers:**
- Push and release (human reviews before anything goes out)
- Tier 2/3 reasoning (frontier models, situated judgment)
- Model-family independence for reasoning integrity
- Full Skills suite integration (Improve, Retrospect, Probe)
- Self-targeting
- Convergence-based stopping (use fixed iteration limits instead)
- Continuous unattended operation (multiple cycles without operator)

**Why this ordering:**
The harness proves Observable Autonomy can be structural. V1 proves the execution loop works end-to-end and that tier 0/1 reasoning is sufficient for routine improvements. The human gate before release is both a safety mechanism and a learning opportunity â€” every review teaches us where the loop's judgment is good enough and where it isn't.

Only after that foundation exists do we add the expensive reasoning machinery â€” and we add it incrementally, measuring cost/value as we go. Push/release autonomy is earned by demonstrating that the pre-release loop produces consistently acceptable proposals.

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

The TRAIL skill is a behavioral convention â€” it asks the LLM to append to a markdown file. The LLM is an unreliable narrator of itself. This is a structural problem that cannot be solved with better instructions.

The harness-protocol is the structural solution. It intercepts LLM API traffic and writes a hash-chained ledger before the response is released. The LLM cannot fabricate, omit, or modify entries. Trail integrity becomes a technical guarantee, not a discipline.

### What this means for ai-steward

ai-steward uses Anthropic API keys routed through the harness at localhost:8474. The harness already captures every LLM call to `.harness/sessions/*.jsonl`. The structural trail exists.

The memory model must be redesigned around this fact:

- **The LLM reads from the memory directory.** Destination, orientation, recent context.
- **The LLM does NOT write the authoritative trail.** The harness does.
- **Derived artifacts (orientation, recent) are computed from the harness ledger.**

### One directory, one standard: .pea/

Three systems need context memory:

1. The skill suite (currently .acm/)
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

- `destination.yaml` â€” Operator. Never the LLM.
- `sessions/*.jsonl` â€” Harness-protocol. Never the LLM.
- `orientation.yaml` â€” LLM (retrospect), but derived from sessions/ which LLM did not author.

**The compatibility path:**

ai-steward defines `.pea/` as the standard. The skill suite migrates from `.acm/` to reading/writing `.pea/`. The harness-protocol migrates from `.harness/` to `.pea/sessions/`. One directory, one standard, structural integrity.

### How this maps to the three principles

**Principle 1 (Commander's Intent):** The operator authors `destination.yaml`. The LLM interprets it but does not self-author its instructions.

**Principle 2 (Observable Autonomy):** The harness captures the authoritative record. The LLM cannot be the sole narrator of its own actions. Capture is structural, not behavioral.

**Principle 3 (Convergence Is Silence):** Retrospect reads the harness ledger (which the LLM did not author) and produces orientation. The judgment of what the arc means comes from reading evidence the LLM could not fabricate.

### Relation to AAS-1 proposals

The Agent Audit Trail standard (AAS-1) is defining the schema for autonomous agent records. Two open proposals on the working group:

1. Provenance (Â§6.9) should capture reasoning traces â€” the harness already captures this in the `reason` field.
2. Reproducibility (Â§6.10) for non-deterministic models â€” reasoning reproducibility, not output-identical reproduction.

ai-steward and the harness-protocol are reference implementations of what AAS-1 is standardizing. Alignment between the .pea/ standard and AAS-1 is a goal.

---

## 2026-06-20 -- Scope expansion: cross-project memory model convergence

### The full scope of work

The `.pea/` unification is not just ai-steward work. It requires coordinated changes across three projects:

1. **ai-steward** â€” reads destination + derives context from sessions/ â€” the consumer
2. **harness-protocol** â€” writes to `.pea/sessions/` instead of `.harness/sessions/` â€” the producer
3. **skill suite** â€” migrates from `.acm/` to `.pea/` â€” the legacy system

### What has NOT converged

The memory model schema is not yet defined. The token budget constraints are stated (~200 destination, ~150 orientation, ~300 recent) but the actual YAML/JSONL structure that achieves those budgets under real usage has not been designed.

**Open design questions:**

- What fields in `destination.yaml`? How do we compress the skill suite's free-form prose into structured data that fits in ~200 tokens?
- How does `orientation.yaml` get derived from `sessions/*.jsonl`? What's the summarization strategy?
- What is "recent context"? Last N entries? Last N tokens? Entries from the last M hours? How is it computed from the harness ledger?
- How does the harness know to write to `.pea/sessions/`? Is it HARNESS_ROOT pointing to `.pea/`? A new config option?
- What migration path for existing `.acm/` and `.harness/` directories?

### The convergence path

The memory model standard will be defined through ai-steward development. The pattern:

1. **ai-steward implements first.** Design choices are made, tested against real usage, refined.
2. **The standard crystallizes.** Once ai-steward proves the model works cost-efficiently, it becomes the standard.
3. **harness-protocol aligns.** Config option or default change to write to `.pea/sessions/`.
4. **skill suite aligns.** Instructions updated to read/write `.pea/` instead of `.acm/`.

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

The directory holds **context memory** â€” the working memory an agent reads at the start of a run and the evidence trail the harness writes during execution. The name should say that.

### The standardization insight

The schema should not be defined in ai-steward's documentation. It should live in **its own repository** â€” a formal schema definition that:

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

## 2026-06-20 -- Decision: .acm/ is the standard

The naming discussion is closed. `.acm/` is the standard directory name.

**Rationale:** The skill suite already uses `.acm/`. It works. Changing the name for theoretical purity adds migration cost with no practical benefit. The standard can evolve in the future if needed, but the current convention is the starting point.

**What this means:**

1. ai-steward uses `.acm/` (not `.pea/`, not `.context/`)
2. harness-protocol writes to `.acm/sessions/` (not `.harness/`)
3. skill suite continues as-is
4. Schema repo (if created) defines the `.acm/` structure

The prior discussion about naming was premature optimization. Ship with what works.


---

## 2026-06-20 -- Cost-efficiency as a first-class measurement goal

### The missing axis

ai-steward makes real API calls with real cost. Claims about improvement mean nothing without the cost side of the ledger. "V2 is better than V1" is an assertion; "V2 achieves the same improvement quality at 40% lower token cost" is evidence.

Cost-efficiency must be a declared measurement dimension alongside improvement quality â€” not an afterthought.

### What to measure

- **Tokens per improvement cycle** â€” SCAN + IMPLEMENT + VERIFY call counts, prompt tokens, completion tokens, total cost in USD. Captured by the harness ledger already; needs surfacing.
- **Cost per accepted improvement** â€” improvements that reach a passing VERIFY are the unit of value. Cost = total tokens spent in the cycle that produced the accepted improvement.
- **Cost trend over iterations** â€” if the architecture improves, cost per accepted improvement should decrease or quality should increase at equal cost. Flat or rising cost with flat quality is a signal the loop is not converging.

### ROI definition

ROI = quality of accepted improvements / total token cost

"Quality" is measured by the harness trail (accepted by VERIFY, not reverted). "Cost" is measured by the ledger. Both sides are auditable structural evidence â€” not self-reported.

### Why this matters for the skills

The skill suite runs in Copilot Chat (Copilot token budget, no direct cost visibility) and in AI-steward cycles (paid API calls, full cost visibility). The discipline is the same in both contexts:

- A skill that requires 10 LLM calls to do what 1 call should do is a structural waste, not a style choice.
- Token budget constraints in skill prompts (~200 tokens for destination, ~150 for orientation) are cost constraints, not just window constraints.
- Improvements to prompt efficiency are as valuable as improvements to output quality.

### Implementation direction

1. **Harness ledger already captures token counts** â€” no new data needed.
2. **Surface cost per cycle** â€” ai-steward run output should report: total tokens, estimated USD cost, tokens per phase.
3. **Record cost in trail entries** â€” each improve iteration's trail entry should include the token cost of that cycle.
4. **Track trend** â€” retrospect.md should include a cost-trend claim when enough data exists.
5. **Establish a baseline** â€” the first N runs establish the baseline cost per accepted improvement. Future architectural changes are evaluated against it.

### What counts as improvement

An architectural change that reduces cost-per-accepted-improvement by X% is evidence of improvement â€” independently of whether the output "feels better." This is the same structural-evidence discipline the manifesto applies to reasoning fidelity: eliminate subjective claims, replace with auditable measurement.


---

## 2026-06-20 -- Self-targeting gate and development principles

### Self-targeting is a milestone, not a mode

ai-steward can target any repository, including its own. But self-targeting before the system earns it produces a demonstration of compliance, not a demonstration of Observable Autonomy. For ai-steward to serve as a PEA integration exemplar, two structural preconditions must hold before the first self-targeting run:

**Precondition 1 -- P2 (Observable Autonomy) is structurally complete**

The two-tier trust model must be functional end-to-end:
- Harness sessions land in `.acm/sessions/` (co-located with `audit-trail.md`) -- done.
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

- Path validation in SCAN rejects `..` and absolute paths by structure â€” the code cannot construct an out-of-scope path, not merely refuses to when asked.
- The harness writes evidence before releasing the response â€” the response cannot reach the caller without the ledger entry existing. Observable Autonomy is structural, not behavioral.
- Token cost is captured from the API response, not self-reported â€” the agent cannot misstate its own cost.
- Session path is discovered by before/after directory scan, not passed from the LLM call â€” the agent cannot fabricate a session reference.

If a bug requires the system to be "working correctly" to prevent it, the design is not defensive enough. The question to ask: *can this fail silently?* If yes, add a structural constraint that makes silent failure impossible.

This principle supersedes "add a test." Tests verify behavior; structure prevents misbehavior. Both are needed, but structure comes first.

---

## 2026-06-20 -- Decision: Reasoning layer structural equivalence

*Closes the open question from the self-targeting gate section.*

**Question:** "Reasoning layer as good as the skillset" â€” does this mean SCAN should produce a trail entry that looks like an improve skill entry (lenses, predictions, `[!DECISION]` markers), or does it mean the *outcomes* are equivalently sound?

**Decision from destination:** Structural equivalence. The destination says:

- "every decision is reasoned, and the reasoning is independently verified"
- "Trail: decisions and reasoning recorded as they happen"
- "The separation of action integrity (what was done) from reasoning integrity (why, and whether the reasoning was genuine)"

The skill suite trail format (lenses, predictions, `[!DECISION]`, `[!REALIZATION]`, `[!REVERSAL]`) is the established pattern for visible reasoning. If ai-steward is the PEA exemplar, and P2 requires the reasoning to be visible, then the trail entries must show the reasoning structure â€” not just the outcomes.

**Implication:** SCAN must produce trail entries that include:
- Which lenses were applied and what each revealed
- A pre-commit prediction of what the change will achieve
- A named blind spot this run did not examine
- `[!DECISION]` marker on the chosen finding
- `[!REVERSAL]` if the prediction was wrong â€” added by the operator in a subsequent run when VERIFY evidence is available. **Never a placeholder. Never emitted by the pipeline.**

**[DONE â€” 2026-06-20]** `record.py` now produces entries with this structure from the Finding + context already available. No new LLM calls required. The format is stable. Do not refactor `_build_entry` â€” it is intentional.

### Canonical trail entry format (authoritative)

Each pipeline-generated entry contains exactly these sections, in this order:

```
## YYYY-MM-DD â€” ai-steward: <description>

**[!DECISION]** Proposed: <description>
*Rationale:* <rationale>
*Risk:* <risk>

**Prediction:** <proposed_change>
*Expected outcome:* <rationale>

**Lenses applied:**
- *Commander's Intent:* ...
- *Code examination:* ...

**Blind spot:** <blind_spot or 'Not identified for this run.'>

**File:** `<file>`
**Tokens:** SCAN in/out â€” IMPL in/out â€” cycle est. $X.XXXXX USD
**Harness session:** `<path>`

**Diff:**
` ` `diff
...
` ` `

*Staged for operator review. Not committed.*
```

**`[!REVERSAL]` rule:** This marker appears in audit-trail.md only when a prediction was demonstrably wrong â€” appended by the operator after VERIFY evidence is available. It is never emitted by the pipeline as a structural placeholder. Any proposal that adds a `[!REVERSAL]` placeholder section to `_build_entry` violates this rule and must be rejected.


---

## 2026-06-20 â€” Expanded destination: universal autonomous improvement engine

### The identity correction

ai-steward is not a code improvement tool.

It is a **universal autonomous improvement engine**. The target is anything an LLM can read and
reason about: a Python codebase, a Rust library, a Node.js project, a book manuscript, a research
paper, a song, a legal document, a product strategy. Code projects are the most obvious initial
use case â€” not the boundary.

This matters for positioning: ai-steward's proof is not "we can autonomously improve Python code."
It is "any artifact that can be expressed as text can be autonomously improved under Observable
Autonomy discipline." That proof is much stronger.

### The minimal assumption set

The only things ai-steward truly requires:

1. **A readable artifact** â€” something the LLM can examine (files, text, any content)
2. **A way to apply a change** â€” write back to a file, patch a document, modify any artifact
3. **A way to review the change** â€” the operator sees what changed and accepts or rejects it
4. **A trail** â€” RECORD always runs; the harness always captures; the ledger always appends

Everything else is operator-declared:
- **Test runner:** erify_command in .ai-steward.yaml â€” or empty for no verification
- **File scope:** scope.allowed glob patterns â€” **/*.py, **/*.md, **/*.ts, **/*
- **LLM:** configurable per phase, swappable per purpose
- **Version control:** git if present, file-backup diff if not, operator review either way

### Git is a capability, not a requirement

Git provides diff, rollback, and staging. These are valuable but not structurally required.
For non-git targets:
- Diff = compare the file before and after IMPLEMENT
- Rollback = restore from the pre-IMPLEMENT backup copy
- Staging = show the operator the before/after and let them decide

The trail recording (RECORD phase, harness sessions) requires no git at all.

PRE-FLIGHT's "git clean" gate becomes optional â€” it applies when git is present, is bypassed when
it is not.

### The LLM is configurable per purpose

Different domains benefit from different models:
- Code: a cheap fast coding-optimised model
- Creative writing, songs: a model strong on language and creativity
- Legal/compliance: a model trained on legal reasoning
- Music notation: a model that understands music theory

The pipeline does not know or care which model handles which phase. The operator declares it.
The harness captures it regardless.

### Open questions for V2 architecture

These are deliberately unresolved â€” they shape whether the next iteration is incremental or
architectural:

1. **Review mechanism abstraction.** Git staging is one review path. A "show before/after diff"
   in a terminal is another. A web UI diff is a third. Should the review mechanism be a pluggable
   backend, or is git-or-nothing the V2 scope?

2. **Non-file targets.** "Create a song from scratch" is a generation task, not an improvement
   task. Does ai-steward expand to cover generation (start from nothing) or stay focused on
   iterative improvement of existing artifacts?

3. **Verification for non-code targets.** For a book manuscript, what does VERIFY mean?
   Word-count bounds (already structural)? Readability score? Grammar check? Or just: operator
   sees the diff and decides? The operator-review-as-verification model may be sufficient for V2.

### Quality bar (2026-06-20)

The question ai-steward must be able to answer yes to:

> "Can I point this at a song manuscript, write a destination, and get a disciplined,
> traceable improvement cycle with a tamper-evident trail â€” without touching Python or git?"

If the answer is no, the universal claim is not yet true.


---

## 2026-06-20 â€” Clarification: git as anchor, not constraint

### The git model (corrected)

Git is **assumed but not required to be pre-existing**. The invariant is:

> The git repository root is always the anchor for .acm/.

ai-steward provides git if needed:
- If the target directory is already a git repo: use it as-is.
- If git is installed but the target is not a git repo: git init it.
  ai-steward derives the repo name from the directory name (or makes one cheap LLM call
  to suggest a meaningful name from the content). The operator can rename later.
- If git is not installed: fail PRE-FLIGHT with a clear message: install git.

Git is not a dependency the operator must arrange. It is infrastructure ai-steward sets up.
This means .acm/ always has a canonical home, rollback always works, and the diff is
always a git diff â€” regardless of whether the target was "a Python repo" or "a folder of
song lyrics the user just created."

### What this changes

PRE-FLIGHT stops being a gate that says "you must bring a git repo." It becomes:
1. Is git installed? If not: fail with instructions.
2. Is the target a git repo? If not: git init it.
3. Is the working tree clean? Apply only if git was pre-existing (a fresh init is always clean).
4. Verify command (if configured): run it. If empty: skip.

The "git clean" gate applies to pre-existing repos only. A freshly-init'd repo is always clean.

### The target is unbounded

The target of ai-steward is not defined by file type, language, or domain.
It is defined by: **anything the LLM can read and reason about**.

Song lyrics, legal documents, a Python codebase, a Rust library, a book manuscript,
a marketing strategy, a research paper. The LLM is swappable per purpose.
ai-steward provides the discipline layer â€” proposal, application, verification, trail.
What gets improved is the operator's choice.

The only structural requirements:
1. Git is available (ai-steward will init if needed)
2. The target consists of files (ai-steward reads them; IMPLEMENT writes them back)
3. The operator writes a .acm/destination.md (or ai-steward scaffolds one via init)

### What this does NOT change

- The trail anchor is always the git root. .acm/ lives there. Always.
- RECORD always runs. The harness always captures. Observable Autonomy applies to every domain.
- The operator always reviews the staged diff. Trust is earned one accepted proposal at a time.
- The harness (llm-harness-proxy) is still outside the agent. The guarantee is structural.

---

## 2026-06-20 â€” V2 architecture: full memory model pipeline

### The core problem with V1 SCAN

V1 pipeline: PRE-FLIGHT â†’ SCAN â†’ IMPLEMENT â†’ VERIFY â†’ RECORD.

SCAN reads destination.md as a hint and then scans files for "something worth improving."
This produces noise when the destination is thin. A poor destination equals wasted cycles.
The pipeline was blind to its own work queue.

**"ai-steward should never work towards blindness."**

### The memory model must be in the pipeline, not outside it

The destination skill, retrospect, and the improve skill are currently human-invoked tools
that feed the pipeline. In V2, they ARE phases of the pipeline. The pipeline embodies the
full memory model: Destination â†’ Retrospect â†’ SCAN (guided) â†’ IMPLEMENT â†’ VERIFY â†’ RECORD.

### Destination gate (Phase 0 â€” before any code is touched)

Three cases:
1. **No destination / thin destination** â€” the pipeline pauses. It reads raw context from
   `.acm/` (docs, notes, specs, anything the operator dropped there), synthesizes inferences,
   and asks the operator the minimum questions needed to produce a quality destination.md.
   Only when destination.md is accurate does the pipeline proceed.

2. **Stale destination** â€” detected when operator-added raw docs predate the last
   destination update, or when the operator signals drift. Pipeline re-runs destination
   derivation for the changed sections.

3. **Quality destination** â€” proceed.

The primary onboarding path: **operator drops raw context into `.acm/` â†’ ai-steward
derives destination.md â†’ asks clarifying questions â†’ destination confirmed â†’ work begins.**
This replaces "manually write destination.md before running."

The pipeline must never start a SCAN cycle without a quality destination.
The `ai-steward init` command is the stub of this; the full version derives from
whatever context is available.

### Retrospect gate (Phase 1 â€” work queue management)

Retrospect produces the **prioritized work queue** â€” the ranked list of next-highest-leverage
items. SCAN is guided by this queue, not by free-ranging file inspection.

The work queue is a **persistent, lazy cache**. Retrospect runs only when the cache is invalid:

- **Cold start** â€” no prior retrospect has run (`.acm/retrospect.md` absent or empty)
- **Queue exhausted** â€” all items from the last retrospect have been completed
- **Destination changed** â€” the operator updated destination.md, invalidating the prior queue

Between these events, the pipeline consumes queue items one by one without re-running
retrospect. Retrospect is expensive (full arc-read); it must not run redundantly.

When retrospect re-runs and produces an empty queue: **Convergence Is Silence** is declared.
The loop stops. The operator is informed. This is a success state, not a failure.

### The full state machine

```
Destination gate
    â”œâ”€ thin/missing â†’ derive from raw docs + questions â†’ loop back
    â””â”€ quality âœ“
         â†“
Retrospect gate
    â”œâ”€ stale/empty/changed â†’ run retrospect â†’ work queue
    â”‚       â””â”€ queue empty â†’ SILENCE (convergence declared, loop stops)
    â””â”€ valid queue âœ“
         â†“
SCAN (guided by work queue top item)
    â””â”€ IMPLEMENT â†’ VERIFY â†’ RECORD â†’ mark item done
         â†“
    Work queue empty? â†’ back to Retrospect gate
    Destination changed? â†’ back to Destination gate
    Otherwise â†’ next queue item
```

### What does NOT change

- The harness captures every LLM call. Observable Autonomy applies to Destination and
  Retrospect phases too â€” their reasoning is captured, not just SCAN/IMPLEMENT.
- The operator always reviews staged diffs. Trust is earned one accepted proposal at a time.
- RECORD always runs when a proposal is staged.
- The target is still unbounded â€” anything the LLM can read.
- The trail anchor is always the git root.

---

## 2026-06-20 â€” V2 architecture: simplified (supersedes verbose flowchart above)

*KISS / DRY / YAGNI / Solve by design. Newest section wins on conflicts.*

### Three rules

```
1. No destination  â†’  define destination. Nothing else runs.
2. No todos        â†’  run retrospect (destination required). Nothing else runs.
3. Todos exist     â†’  run improve loop. One item per cycle.
```

That is the complete pipeline logic. The structure enforces the behaviour.

### Destination derivation (Rule 1)

If `.acm/destination.md` is absent or thin:
- Read all raw context the operator dropped into `.acm/` (docs, notes, specs, anything)
- Form sourced inferences
- Ask the minimum questions needed to produce an accurate destination
- Write destination.md. Only then proceed.

The operator never needs to write destination.md manually.
Dropping context and answering questions is the full onboarding path.

### Retrospect as work queue (Rule 2)

Retrospect runs only when the work queue is invalid:
- Cold start (never run)
- Queue exhausted (all items done)
- Destination changed

It produces a ranked list of next-highest-leverage items.
SCAN executes the top item. The queue persists between cycles.

### Convergence check

When retrospect finds nothing â†’ run once more with Opus before declaring silence.
Cheap models may declare convergence too early. One expensive verification is worth it.
After Opus confirms nothing remains: loop stops. This is a success state.

### Model cost strategy

| Phase | Model | Rationale |
|-------|-------|-----------|
| Destination derivation | Sonnet | Reasoning quality needed |
| Retrospect (work queue) | Sonnet | Arc-read quality matters |
| SCAN + IMPLEMENT | Sonnet | Good quality, reasonable cost |
| Convergence verification | Opus | Rare, high-stakes, worth paying |
| Structural gates (VERIFY) | Haiku / none | No LLM needed for syntax/tests |

---

## Current State (updated 2026-06-21)

### V1 is complete

V1 was closed on 2026-06-20. Self-targeting proved the mechanism. CI enforces `mypy src/` and `pytest` on every push/PR. 66 tests pass. 13 source files are mypy-clean. P1 (Commander's Intent) and P2 (Observable Autonomy) are both structurally complete.

Measured cost: **~$0.018/cycle** on claude-haiku-4-5 (2 LLM calls). Orders of magnitude cheaper than a Claude Sonnet conversation for code-level work.

### The division of labour

ai-steward and the skills suite serve different roles. They are complementary, not competing:

| Work type | Tool | Why |
|-----------|------|-----|
| Code improvements to any repo | ai-steward | Cheap (~$0.018/cycle), harness-captured, structural guarantee |
| Cross-repo architecture, vision | Skills (human conversation) | Requires judgment that cannot be delegated yet |
| Publication review, theory | publication-rigour-review skill | Requires deep reasoning over literature |

The key difference: the skills depend on the LLM following instructions correctly (behavioral). ai-steward's evidence is captured by the harness *before the agent can respond* -- structural, not behavioral. One is a trust claim; the other is a structural guarantee.

### V2 direction -- external targeting and the pea workspace

The next proof layer is generalisation. V1 proved the loop works on one repo (self-targeting). V2 proves it works on any repo.

**Primary targets (in order):**
1. `c:\git\pea\agent-context-memory` -- the ACM spec. Small, no tests yet, well-bounded destination.
2. `c:\git\pea\manifesto` -- theory docs. Prose improvements, reference consistency.
3. Any pea workspace repo with `.acm/destination.md` and `.ai-steward.yaml`.

**Before running external targeting:**
- Harness must be running from new location: `c:\git\pea\llm-harness-proxy\`
- Target repo must have `.ai-steward.yaml` (run `ai-steward init <path>` if not)
- Target repo must have `.acm/destination.md` authored by operator

**What V2 must prove:**
- `audit-trail.md` lands in the *target* repo's `.acm/`, not ai-steward's
- Harness session lands in the *target* repo's `.acm/sessions/`
- Loop stops (Convergence Is Silence) when there is genuinely nothing to improve
- Actual cost per accepted proposal on a non-trivial external target

### Infrastructure (updated 2026-06-21)

- **Harness:** `c:\git\pea\llm-harness-proxy\` (moved from `c:\git\llm-harness-proxy\`)
- **ai-steward:** `c:\git\pea\ai-steward\` (moved from `c:\git\ai-steward\`)
- **Workspace ACM:** `c:\git\pea\.acm\` governs all pea workspace repos

---

## Current State (updated 2026-06-21)

### V1 is complete

V1 was closed on 2026-06-20. Self-targeting proved the mechanism. CI enforces mypy and pytest on every push/PR. 66 tests pass. 13 source files are mypy-clean. P1 (Commander's Intent) and P2 (Observable Autonomy) are both structurally complete.

Measured cost: ~0.018 USD/cycle on claude-haiku-4-5 (2 LLM calls). Orders of magnitude cheaper than a Claude Sonnet conversation for code-level work.

### The division of labour

ai-steward and the skills suite serve different roles. They are complementary, not competing.

Code improvements to any repo: ai-steward -- cheap, harness-captured, structural guarantee.
Cross-repo architecture and vision: Skills (human conversation) -- requires judgment that cannot be delegated yet.
Publication review and theory: publication-rigour-review skill -- requires deep reasoning over literature.

The key difference: the skills depend on the LLM following instructions correctly (behavioral). ai-steward's evidence is captured by the harness before the agent can respond -- structural, not behavioral. One is a trust claim; the other is a structural guarantee.

### V2 direction -- external targeting and the pea workspace

The next proof layer is generalisation. V1 proved the loop works on one repo (self-targeting). V2 proves it works on any repo.

Primary targets in order:
1. c:\git\pea\agent-context-memory -- the ACM spec. Small, no tests yet, well-bounded destination.
2. c:\git\pea\manifesto -- theory docs. Prose improvements, reference consistency.
3. Any pea workspace repo with .acm/destination.md and .ai-steward.yaml.

Before running external targeting:
- Harness must be running from new location: c:\git\pea\llm-harness-proxy\
- Target repo must have .ai-steward.yaml (run 'ai-steward init <path>' if not)
- Target repo must have .acm/destination.md authored by operator

What V2 must prove:
- audit-trail.md lands in the target repo's .acm/, not ai-steward's
- Harness session lands in the target repo's .acm/sessions/
- Loop stops (Convergence Is Silence) when there is genuinely nothing to improve
- Actual cost per accepted proposal on a non-trivial external target

### Infrastructure (updated 2026-06-21)

- Harness: c:\git\pea\llm-harness-proxy\ (moved from c:\git\llm-harness-proxy\)
- ai-steward: c:\git\pea\ai-steward\ (moved from c:\git\ai-steward\)
- Workspace ACM: c:\git\pea\.acm\ governs all pea workspace repos


---

## Current State (updated 2026-06-21)

### V1 is complete

V1 was closed on 2026-06-20. Self-targeting proved the mechanism. CI enforces mypy and pytest on every push/PR. 66 tests pass. 13 source files are mypy-clean. P1 (Commander's Intent) and P2 (Observable Autonomy) are both structurally complete.

Measured cost: ~0.018 USD/cycle on claude-haiku-4-5 (2 LLM calls). Orders of magnitude cheaper than a Claude Sonnet conversation for code-level work.

### The division of labour

ai-steward and the skills suite serve different roles. They are complementary, not competing:

- **Code improvements to any repo:** ai-steward -- cheap (~0.018 USD/cycle), harness-captured, structural guarantee
- **Cross-repo architecture, vision:** Skills (human conversation) -- requires judgment that cannot be delegated yet
- **Publication review, theory:** publication-rigour-review skill -- requires deep reasoning over literature

The key difference: the skills depend on the LLM following instructions correctly (behavioral). ai-steward's evidence is captured by the harness before the agent can respond -- structural, not behavioral. One is a trust claim; the other is a structural guarantee.

### V2 direction -- external targeting and the pea workspace

The next proof layer is generalisation. V1 proved the loop works on one repo (self-targeting). V2 proves it works on any repo.

**Primary targets (in order):**
1. c:\git\pea\agent-context-memory -- the ACM spec. Small, no tests yet, well-bounded destination.
2. c:\git\pea\manifesto -- theory docs. Prose improvements, reference consistency.
3. Any pea workspace repo with .acm/destination.md and .ai-steward.yaml.

**Before running external targeting:**
- Harness must be running from new location: c:\git\pea\llm-harness-proxy\
- Target repo must have .ai-steward.yaml (run ai-steward init <path> if not)
- Target repo must have .acm/destination.md authored by operator

**What V2 must prove:**
- audit-trail.md lands in the target repo's .acm/, not ai-steward's
- Harness session lands in the target repo's .acm/sessions/
- Loop stops (Convergence Is Silence) when there is genuinely nothing to improve
- Actual cost per accepted proposal on a non-trivial external target

### Infrastructure (updated 2026-06-21)

- **Harness:** c:\git\pea\llm-harness-proxy\ (moved from c:\git\llm-harness-proxy\)
- **ai-steward:** c:\git\pea\ai-steward\ (moved from c:\git\ai-steward\)
- **Workspace ACM:** c:\git\pea\.acm\ governs all pea workspace repos

---

## 2026-06-21 — Reasoning quality is non-negotiable (clarification over cost framing)

*Layered over the cost model in the consolidated 2026-06-20 section. This governs when there is tension.*

### The separation that was missing

The destination has stated `~$0.002 per improvement cycle` and `improvements are evaluated against cost-per-accepted-proposal`. This is a **measurement target**, not a reasoning filter. The model was reading it as a gate: "is this change worth the cost of a cycle?" That is wrong.

**Cost governs two things only:**
1. **Model selection** — use cheap models (haiku) for routine reasoning; escalate when the model genuinely cannot decide.
2. **Proposal scope** — propose small, focused, low-risk changes that fit in a single cycle. Not big rewrites.

**Cost does not govern:**
- Whether to reason fully
- Whether a valid proposal is "worth" acting on
- How deep to examine the code

### Reasoning quality is the floor

The reasoning protocol — Mandate check → Examination → [!DECISION] with rejected alternative → Prediction → Blind spot — is executed completely on every cycle, regardless of model tier or cycle cost. This is the same governance architecture as the skillset. The caliber is the same. The cost buys a cheaper model, not shallower reasoning.

If a model cannot reason to this standard at haiku tier, that is a **tier escalation signal**, not a reason to skip steps.

### What "cost with quality" actually means

- Reason fully, at the skillset standard
- Propose the smallest change that genuinely serves the mandate
- Use the cheapest model that can meet the reasoning standard
- Measure the actual cost; use that data to improve model selection

The `~$0.002` target was aspirational for haiku + routine changes. It is not a constraint on proposal acceptance. A well-reasoned proposal that costs $0.03 and gets accepted is better than a shallow one that costs $0.002 and gets discarded.

---

## 2026-06-21 — Cost ceiling raised to $1.00 per cycle

*Supersedes the $0.002 target in the consolidated 2026-06-20 section and the $0.018 measured figure.*

**Budget ceiling: $1.00 per improvement cycle.**

The $0.002 target was written when cost was the primary concern. It was too low — it caused the model to treat cycle cost as a proposal filter, self-rejecting valid improvements on the grounds that they "didn't justify a cycle." That is the wrong behaviour.

The correct constraint: each cycle may cost up to $1.00. Within that ceiling, use the cheapest model that reasons to the required quality standard. Measure and record actual cost per cycle. Optimise from data, not from aspirational targets.

Cost is measured. Quality is the gate.

---

## 2026-06-21 — Cognitive architecture target: skillset parity

*This section defines what ai-steward must become. It supersedes any prior framing where "reasoning quality" was treated as a prompt concern. This is an architectural target.*

---

### The gap

The skillset (Improve + Retrospect + Trail) is a complete cognitive loop. ai-steward is currently half of it.

ai-steward has: mandate gate, 5-step pre-proposal reasoning, harness capture, trail record.
ai-steward is missing: memory reading, examination lenses, first-read challenge, reflection, autonomous retrospect, learning surface.

Every SCAN run today starts cold — no memory of what prior cycles found, concluded, or reversed. The skillset never starts cold. This is the root quality gap.

---

### The target cognitive architecture

Four phases must be built, matching the skillset's Improve → Retrospect → Trail loop:

---

**Phase 1 — ORIENT (before SCAN)**

Before proposing anything, SCAN must read the memory layer in this order (ACM §4 scope traversal applies to all):

1. `destination.md` — mandate. What the operator wants. Highest authority. (Already done.)
2. `retrospect.md` — current orientation. What is true about this codebase right now. Arc-level claims from prior cycles.
3. `learning.md` — compact learning surface. Every `[!REALIZATION]` and `[!REVERSAL]` across all history, chronological. Read this before the trail — it is what the loop has actually concluded.
4. `audit-trail.md` — full history. Read only when a specific prior decision needs its context.

SCAN without retrospect.md and learning.md is examination without memory. It will re-find the same things, propose what was already tried, and miss patterns only visible across the arc.

*Implementation: extend `_load_scope_context()` to load retrospect.md and learning.md alongside destination.md. Inject as "Current orientation" and "Prior learnings" sections.*

---

**Phase 2 — SCAN with examination lenses (replaces flat "Step 2 — Examination")**

The skillset's Improve skill uses four named lenses — not a checklist, but vocabulary for structured thinking. SCAN must use the same lenses:

- **Purpose** — does the target do what the destination says it should? Gap between stated goal and actual behaviour? This lens runs first.
- **Inconsistency** — where does the target contradict itself? Mixed conventions, asymmetric handling of similar cases.
- **Overburden** — where is one component doing too much? The most overburdened file is the highest-risk change target.
- **Waste** — what carries no value? Dead code, never-fired validation, abstractions with one consumer.

Add lenses as the target warrants. Name every lens applied and what it revealed — including "nothing actionable."

Then: **Challenge the first read.** Ask explicitly:
- What am I not seeing?
- Am I anchored to the obvious finding and missing a subtler, more important one?
- Is the structure itself wrong, such that no incremental fix will help? (Kaikaku question — if yes, argue for redesign, do not propose incremental patches.)

*Implementation: restructure the SCAN system prompt Steps 2–3 to use these lenses and the Kaikaku challenge.*

---

**Phase 3 — RECORD with Reflection**

Currently RECORD writes what happened. It must also write what was learned.

After VERIFY confirms the change, RECORD must add:

- **Reflection** — updated model of the target as a falsifiable claim a future run could disagree with. Not "what I did" — "what I now believe is true about this codebase."
- **Across-trail trigger evaluation** (mandatory, not skippable):
  - Recurring finding-class: has this type of finding appeared before? If yes — [!REALIZATION].
  - About to declare silence: is the loop reaching a natural end? Is the silence earned?
  - Prior [!REALIZATION] contradicted: does this run's outcome change a prior conclusion?
  - Operator explicitly asked: was there a direct operator question this run answers?
- **[!REALIZATION]** when something discovered changes understanding.
- **[!REVERSAL]** when a plan from this cycle or a prior cycle was changed — both kinds count.
- **Candidate Next Moves** — ranked list of what the next run should look at, from this iteration's blind spots and open questions.

*Implementation: pass VERIFY outcome back to RECORD; add a second LLM call in RECORD for reflection synthesis.*

---

**Phase 4 — Autonomous RETROSPECT**

The skillset's Retrospect skill reads the full trail and synthesizes arc-level claims into `retrospect.md`. ai-steward must do this autonomously.

Trigger conditions (any one fires it):
- After every N accepted proposals (N=5 is a reasonable start)
- When SCAN returns `{"nothing": true}` for two consecutive cycles (convergence signal)
- On operator demand: `ai-steward retrospect <repo>`

What it does:
1. Regenerate `learning.md` and `history.md` from `audit-trail.md`
2. Read the full arc
3. Form falsifiable arc-level claims about the target
4. Write updated `retrospect.md`
5. Trail the retrospect run itself

Once Retrospect runs, the next SCAN has a current orientation to read. The feedback loop is closed.

*Implementation: new `retrospect.py` pipeline phase + `ai-steward retrospect` CLI command.*

---

### What "same caliber" means

The skillset is caliber. ai-steward is the same caliber when:

1. SCAN never starts cold — it always reads memory before reasoning
2. Examination uses named lenses and challenges its first read
3. RECORD produces Reflection + Candidate Next Moves + trigger evaluation
4. Retrospect runs autonomously and keeps orientation current
5. `learning.md` is regenerated after every accepted proposal
6. The trail is readable at three resolutions: Digest (outcome/delta), Indexed ([!MARKERS]), Full (sessions/)

This is not about prompt quality. It is the same cognitive loop — compressed to run autonomously within the $1.00/cycle ceiling, using the cheapest model that meets the reasoning standard.

---

### Build order

1. **ORIENT** — feed retrospect.md + learning.md into SCAN. Highest leverage, ~20 lines. Immediate quality improvement.
2. **SCAN lenses + Kaikaku** — restructure examination step with named lenses and first-read challenge. Prompt change only.
3. **RECORD Reflection** — add reflection synthesis after VERIFY. Requires passing outcome back to RECORD.
4. **Retrospect command** — `ai-steward retrospect`. Closes the feedback loop.
5. **Auto-trigger Retrospect** — fire on convergence signal or after N accepted proposals.

Each step is independent and shippable. Do not wait for all five before running.

---

## 2026-06-21 — Cost ceiling is provisional, not principled

*Correction to the $1.00/cycle figure set earlier today.*

The $1.00 ceiling is arbitrary. It was set reactively to remove the $0.002 floor that was causing the model to self-censor, not derived from any measurement or reasoning about what a cycle should cost.

**The principled position:**

There is no target cost. There is a cost constraint method:

1. Use the cheapest model that reasons to the required quality standard.
2. Measure actual cost per cycle. Record it in every trail entry (already done).
3. When N accepted proposals have been collected, read the data: what did accepted proposals actually cost? What did rejected ones cost? What is the cost-per-accepted-proposal trend?
4. From that data, set a principled ceiling.

$1.00/cycle is a temporary operational upper bound — a circuit breaker to prevent runaway cost while the system is being built. It is not a quality signal, not a target, and not evidence of anything. It will be replaced by a data-derived figure once enough cycles have run.

**Until then:** cost is measured and recorded. Quality is the gate. The model tier is the variable that gets optimised from evidence, not assumed from the start.

---

## 2026-06-21 — Configuration surface: operator controls that will emerge

*The .ai-steward.yaml is the operator's governance interface. Model-per-phase was the first signal. More controls will surface as the cognitive architecture is built. This section defines them.*

---

### What already exists in config.py

```yaml
models:
  analyze: claude-sonnet-4-5      # per-phase model assignment
  propose: claude-sonnet-4-5
  implement: claude-sonnet-4-5
  verify: claude-haiku-4-5
  judge: claude-opus-4-5

harness:
  endpoint: "http://localhost:8474"

scope:
  allowed: ["src/**/*.py"]        # file glob whitelist
  blocked: ["tests/**", ".acm/**"]

budget_usd: 5.0                   # total session budget (all cycles combined)
max_iterations: 1                 # cycle cap per run
sandbox: local                    # execution environment
allow_dirty: false                # require clean working tree
verify_command: "python -m pytest --tb=no -q"
```

**Note:** `budget_usd` is the total session budget. It is not a per-cycle ceiling. These are different controls.

---

### Controls that will surface

**Cost controls (clarify and extend the existing budget_usd):**

```yaml
budget_usd: 5.0                   # total spend across all cycles in this session
max_cost_per_cycle_usd: 1.0       # circuit breaker per individual cycle
                                  # provisional; replace with data-derived figure
```

`max_cost_per_cycle_usd` is the per-cycle ceiling the user sets based on their budget and task size. $0.50 for a quick pass on a small repo, $2.00 for deep reasoning on a large one. The operator knows their budget; the system should respect it without assuming a universal number.

---

**Memory controls (from ORIENT phase):**

```yaml
memory:
  read_retrospect: true           # load .acm/retrospect.md into SCAN context
  read_learning: true             # load .acm/learning.md into SCAN context
  context_chars: 3000             # total char budget for all memory sections
  scope_levels: 4                 # how many parent directories to traverse (ACM §4.2)
```

Some operators target repos with no retrospect or learning history. Memory reading should default on but be disableable. Context budget controls token cost for memory injection.

---

**Retrospect controls (from autonomous Retrospect phase):**

```yaml
retrospect:
  auto: true                      # run retrospect automatically when triggered
  trigger_every_n_accepted: 5     # after N accepted proposals
  trigger_on_convergence: true    # when SCAN returns nothing twice in a row
```

Operators running ai-steward in a tight loop may want frequent retrospects. Others running single cycles may want none. Both are valid.

---

**Reasoning controls (from SCAN lenses and RECORD Reflection):**

```yaml
reasoning:
  lenses: [purpose, inconsistency, overburden, waste]   # active examination lenses
  kaikaku_check: true             # include "is the structure itself wrong?" challenge
  reflection: true                # RECORD writes a reflection after VERIFY
  candidate_next_moves: true      # RECORD writes ranked next moves
  trigger_evaluation: true        # RECORD runs across-trail trigger check
```

Different tasks warrant different lenses. A security audit might add `security` to the lens list. A performance pass might use `overburden` only. These should not be hardcoded.

---

**Tier escalation controls:**

```yaml
escalation:
  enabled: false                  # V1: off. V2: enables automatic model promotion
  on: [verify_fail, nothing_found_twice]
  max_model: claude-opus-4-5      # ceiling model for escalation
```

When the cheap model fails verification or cannot find anything actionable, escalate to a stronger model before giving up. The ceiling prevents runaway cost.

---

### The pattern

The .ai-steward.yaml config is the operator's governance interface. Every decision that depends on:
- the operator's budget
- the operator's risk tolerance
- the size and type of the target repo
- the operator's quality bar

…should be a config parameter, not a hardcoded constant.

Model-per-phase was the first signal of this pattern. `max_cost_per_cycle_usd` is the second. Memory, retrospect, reasoning depth, and escalation will follow as the cognitive architecture phases are implemented.

**Design rule:** when implementing a new cognitive phase, identify its operator-facing controls first. Add them to `AiStewardConfig` and the YAML schema before writing the implementation. The config is the contract.
