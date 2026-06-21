# Learning

Auto-generated from `.trail/audit-trail.md` by the `record.py learning --write` command in the autonomous-agent-skills install.
Do not edit by hand — re-run the command to refresh.

Compact chronological extract of every `[!REALIZATION]` and `[!REVERSAL]` marker. The learning surface — what the loop has actually concluded across runs. Read this before reading `audit-trail.md` in full; reach for `audit-trail.md` only when an item here needs its surrounding context.

## 2026-05-14 — Evo analysis and new project decision

**[!REALIZATION]** ** Evo's self-improvement is metric-driven (benchmark merge rate). It does not know why it improves, whether improvements are genuine, or whether it is optimizing the right thing. The skills layer adds exactly what is missing: Vision (operator intent), Trail (reasoning as it happens), Improve (meta-cognitive loop with silence as valid), Retrospect (arc-level reading), Probe (ARF — tests whether reasoning is genuine).

## 2026-05-14 — Evo analysis and new project decision

**[!REALIZATION]** ** The correct framing of model-family mixing: in most multi-agent systems, models are mixed for task specialization (performance optimization). In ai-steward, model-family independence is a *reasoning integrity mechanism* — the model that proposes a change and the model that judges it come from different families, so the judge cannot share the proposer's blind spots. This is structurally different from performance optimization.

## 2026-05-14 — Vision run: understanding operator intent

**[!REALIZATION]** ** The execution layer is deliberately dumb: executes, verifies, logs. Does not reason. Gates are reasoning decisions made by the reasoning layer, not mechanical rules.

## 2026-05-14 — Vision run: understanding operator intent

**[!REVERSAL]** ** Vision corrected: removed "demonstration artifact" framing; replaced with "earned unsupervised operation as normal running state."

## 2026-05-14 — Architectural clarification: harness-protocol role and dual-use trail

**[!REALIZATION]** ** The harness is not a passive recorder — it is a model trustworthiness classifier. For every API call it scores what the model exposed: thinking tokens, tool usage, decision rationale. Models that do not provide a reasoning trail are flagged. The reasoning layer uses this score to calibrate trust per model per pipeline phase.

## 2026-05-14 — Architectural clarification: harness-protocol role and dual-use trail

**[!REALIZATION]** ** The trail serves two purposes at different trust levels:

## 2026-05-14 — Vision cleanup

**[!REALIZATION]** ** The harness-protocol is not just a passive recorder — it is an active transparency evaluator. For every API call, it scores what the model exposed: thinking tokens, tool usage, decision rationale, structured reasoning. Models that don't provide a proper trail are flagged. This makes it a model trustworthiness classifier.

## 2026-05-14 — Vision cleanup

**[!REALIZATION]** ** The dual-use tension in the trail is real and must be maintained, not resolved:

## 2026-05-14 — Vision cleanup

**[!REALIZATION]** ** The key architectural distinction: Evo tangled reasoning and execution. ai-steward separates them. The execution layer is deliberately dumb. The reasoning layer is architecturally separate and observes/guides from outside. Gates become reasoning decisions, not hard mechanical rules.

## 2026-05-14 — Vision cleanup

**[!REVERSAL]** ** Vision corrected: removed "demonstration artifact" framing; replaced with "earned unsupervised operation as normal running state."

## 2026-05-15 — First retrospect run; launch orientation before first code sprint

**[!REALIZATION]** ** The risk going into the first code sprint is the mirror of harness-protocol's early loop problem. harness iterated on visible features while the core claim was untested. ai-steward's risk is deferring phase assignment and model family decisions until the pipeline "feels ready" — meaning those decisions get made by the code rather than before it. The operational rules in `retrospect.md` are designed to prevent this.

## 2026-05-28 — vision-to-destination-rename

**[!REALIZATION]** :* not fired — no prior realisation in this repo argued for or against the artifact filename.

---

**12 markers — 10 realisations, 2 reversals**
