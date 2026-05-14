# Audit trail

Append-only ledger of autonomous operations on this repo. Newest entries at the bottom.

---

## 2026-05-14 — Architectural clarification: harness-protocol role and dual-use trail

**Trigger:** Operator identified missing architectural points in the vision.

**[!REALIZATION]** The harness-protocol is not just a passive recorder — it is an active transparency evaluator. For every API call, it scores what the model exposed: thinking tokens, tool usage, decision rationale, structured reasoning. Models that don't provide a proper trail are flagged. This makes it a model trustworthiness classifier.

**[!REALIZATION]** The dual-use tension in the trail is real and must be maintained, not resolved:
- Proxy-captured JSONL = evidence (ground truth, independently captured, the agent cannot tamper with it)
- `audit-trail.md` = memory (agent's interpretation, useful but not independently verifiable)
These serve different trust levels. The reasoning layer reads both but weights them differently. If they diverge, the proxy wins.

**[!DECISION]** Harness-protocol stays a standalone application — not built into ai-steward.
Rationale: If internal, ai-steward could modify its own evidence capture. Self-targeting makes this especially dangerous. Structural independence of the capture mechanism is the integrity guarantee — non-negotiable.
Alternatives: Built-in (rejected — breaks integrity guarantee). Hybrid with required dependency (considered — but "required dependency" is the correct framing, not "hybrid").

**[!DECISION]** Harness-protocol must support all model families.
Rationale: ai-steward uses multiple model families across pipeline phases. All API calls must be captured regardless of provider. Different protocols (Anthropic extended thinking, OpenAI reasoning tokens, Gemini thinking mode, models with no reasoning exposure) must be normalized to a common schema.
Alternatives: Anthropic-only (rejected — defeats multi-family independence design).

**[!DECISION]** Scope enforcement: harness-protocol repo is outside ai-steward's autonomous improvement scope by default.
Rationale: The system that captures evidence of ai-steward's actions cannot be autonomously modified by ai-steward. Changes require explicit operator action.
Alternatives: In-scope with operator approval gate (rejected — approval gates can fail; structural exclusion cannot).


**Skill:** Vision v1.3.0
**Trigger:** Operator asked for a Vision run immediately after first vision.md was committed.

### Hunches formed and questions asked

**Hunch 1 — destination is a single demonstration run**
Source: "while you sleep" appeared multiple times; vision called it "the demonstration artifact."
Question asked: "Is the near-term destination one real overnight run with a real release and a real trail you're proud to publish — and everything before that is just getting to that run?"
*Operator response:* No. "While you sleep" is a figure of speech for trusted unsupervised operation, not a specific milestone event. The destination is the system itself, running continuously.
**[!REVERSAL]** Vision corrected: removed "demonstration artifact" framing; replaced with "earned unsupervised operation as normal running state."

**Hunch 2 — Evo is the base, ai-steward wraps and extends it**
Source: Evo is mature, nine-phase pipeline, hash-chained ledger — building from scratch would duplicate months of work.
Question asked: "Is Evo the engine that ai-steward wraps and extends, or are you starting from scratch with Evo as a reference?"
*Operator response:* New solution. Evo tried to solve reasoning itself (inline in the pipeline), and its gates may not be appropriate. Learn from Evo's documentation — take what makes sense, leave what doesn't. Think deeply about the split.
**[!REALIZATION]** The key architectural distinction: Evo tangled reasoning and execution. ai-steward separates them. The execution layer is deliberately dumb. The reasoning layer is architecturally separate and observes/guides from outside. Gates become reasoning decisions, not hard mechanical rules.

**Hunch 3 — public from day one**
Source: All three existing repos (manifesto, skills, harness-protocol) are public; competitive landscape analysis suggests positioning against others.
Question asked: "Is this staying private during build, or public from day one?"
*Operator response:* Private until MVP. The trail is also documentation — when published, it is part of the public argument.

### What the agent now believes

AI Steward is a genuinely new system, not an Evo fork. The execution layer is new, informed by Evo's work, with deliberate architectural separation from the reasoning layer. Gates in ai-steward are reasoning decisions, not mechanical gates. Private until MVP; trail doubles as documentation when published.

### What was rejected

- "The destination is a single demonstration run." The destination is continuous trusted operation.
- "Evo is a dependency." Evo is a learning source. What to take and what to leave requires deliberate analysis of Evo's documentation.

### What is still open

- Which specific parts of Evo's execution layer are worth taking (ledger schema, rollback design, profile system) versus which to redesign. This requires reading Evo's architecture documentation before the first architectural decision is made.
- The multi-model phase assignment design — mentioned in the vision but not yet specified.
