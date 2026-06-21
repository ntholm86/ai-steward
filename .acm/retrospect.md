# retrospect.md — ai-steward

_Last updated: 2026-06-21 (run: post-prediction-field)_

---

## Current claims

**1. The mandate gate is now a hard structural filter, not background context.**
The 5-step SCAN protocol closes the off-mandate gap. One run proven; pattern not yet established.
**Falsifiable by:** a SCAN run that produces an off-mandate proposal despite the 5-step prompt.

**2. V1 proof is complete. Multi-cycle convergence is the critical untested claim.**
External targeting (vectorium), self-targeting, and mandate-gated SCAN are all demonstrated.
Multi-cycle convergence — does the loop stop cleanly when SCAN returns nothing_found N times? — has never been tested. More single cycles produce no new proof on this claim.
**Falsifiable by:** a multi-cycle run that fails to stop, or stops before the mandate is satisfied.

**3. The cost model in destination’s Current State section is obsolete.**
"~$0.002 per cycle (haiku)" contradicts actual ~$0.03/cycle under claude-sonnet-4-5 + 5-step protocol.
**Falsifiable by:** a cycle under the current prompt that consistently costs ≤$0.003.

**4. RECORD’s structural errors are partially fixed; two remain.**
The prediction field fix (improve iteration, entry 37) corrected the most visible error: `**Prediction:**` now carries the model’s Step 4 falsifiable statement instead of the proposed_change description. Two structural errors remain:
- `*Expected outcome:* {finding.rationale}` still uses rationale (why we’re doing this) as an outcome statement (what will happen). These are semantically distinct; the current code conflates them.
- No Reflection (second LLM call synthesizing VERIFY outcome against prediction), no trigger evaluation, no Candidate Next Moves in autonomous trail entries. Every autonomous cycle still produces a trail entry that does not meet the trail-skill standard.
**Falsifiable by:** an autonomous trail entry that contains genuine Reflection, trigger evaluation, and Candidate Next Moves.

**5. The improve–retrospect cadence is steering correctly.**
The retrospect (entry 36) identified RECORD as the largest gap. The improve iteration (entry 37) selected the prediction field fix — not ORIENT (top-ranked candidate) — because the incorrect Prediction section was a present structural harm vs. ORIENT’s future benefit. This judgment call is arc-visible and auditable: future Retrospect runs can check whether this prioritization held up.
**Falsifiable by:** showing the prediction field fix produced no benefit, or that ORIENT would have been higher-leverage.

**6. A duplicate trail entry exists (entries 34–35).**
"scan-reasoning-quality + V1-milestone-confirmed" appears twice. The trail-skill duplicate detection gap remains unaddressed. Not a blocking issue; a structural cleanliness gap.

**7. The shared .acm/ evidence layer is an achieved structural fact; ORIENT is the remaining integration step.**
Both skills and the autonomous pipeline write to the same trail. Until ORIENT is implemented, the retrospect.md and learning.md we write are invisible to the autonomous pipeline’s SCAN context.
**Falsifiable by:** a SCAN run that receives retrospect.md content in its context window.

**8. The config surface is defined before implementation. Risk: aspirational drift.**
`max_cost_per_cycle_usd`, memory, retrospect, reasoning, escalation controls are captured in destination.md. None implemented. This is the third session where these are "defined but pending." The risk of aspirational drift increases with each session that passes without implementation.
**Falsifiable by:** showing these fields in `config.py` and `.ai-steward.yaml`.

---

## What the next runs should test

1. **ORIENT phase** — extend `_load_scope_context()` to also load `retrospect.md` and `learning.md`. Until this is done, the retrospect we just wrote is invisible to autonomous SCAN runs. This is the highest-leverage next move: it closes the loop between human-supervised retrospect and autonomous pipeline reasoning.

2. **Fix `*Expected outcome:*` semantic error in `_build_entry()`** — replace `finding.rationale` (the why) with a distinct outcome description, or remove the redundant line now that `finding.prediction` carries the Step 4 statement. Small, surgical, closes the second RECORD structural error.

3. **Cost model correction in destination** — update Current State from "$0.002 (haiku)" to actual ~$0.03/cycle. A destination that contradicts operation confuses future operators.

4. **Multi-cycle convergence test** — run ai-steward against an external repo in a loop until nothing_found fires twice consecutively. Until demonstrated, "Convergence Is Silence" is a principle, not a proven property.

5. **Config surface: add `max_cost_per_cycle_usd` to `AiStewardConfig`** — first config field from the defined surface to be implemented. A useful forcing function: implementing one concrete field will expose whether the design decisions in the destination entry hold up.

---

## Active operational rules

- **V1 stops before release.** Operator reviews every staged diff. Inviolable.
- **llm-harness-proxy is outside ai-steward’s autonomous scope.** Structural exclusion.
- **Execution layer must remain separate from reasoning layer.** Phases execute; skills reason.
- **ACM §4.2 stop conditions govern scope traversal.** Filesystem root, `.acm-root` marker, 4-level cap.
- **Trail entries are required for all `scan.py` changes.** No scan.py change without a trail entry in the same session.
- **Test SCAN prompt changes with a live run before declaring them correct.** Live run is the gate for prompt changes.
- **Before appending a trail entry, check if the most recent entry already covers the current session.** Entries 34–35 duplicate; this rule prevents recurrence.
- **The cost model in destination must be updated when operating parameters change materially.** Current State "$0.002" is obsolete; update is pending.
- **Use Python (not PowerShell) for all .acm/ file reads and writes.** PowerShell 5.1 silently mojibake-corrupts UTF-8 content and re-injects BOM.
- **When two structural errors exist in the same function, fix the more visible one first, then record the second as a known gap.** The prediction fix was correct to precede the Expected outcome fix.

---

## Loop-effectiveness notes

The improve–retrospect–improve cycle is working as designed: retrospect surfaces arc-level gaps; improve selects one fix; retrospect updates orientation. The two-entry arc since the last retrospect is short but shows clean loop behavior.

The loop’s attention distribution remains asymmetric: SCAN has received most autonomous improvement effort; RECORD has received one fix (prediction field) and still has two structural errors. ORIENT has received zero implementation work despite being the integration mechanism between the human-supervised and autonomous evidence layers.

**Quality bars tested so far:** mandate alignment (SCAN), trail entry structural correctness (partially). **Bars not tested:** whether autonomous proposals are accepted by operators at a meaningful rate, whether the harness ledger is tamper-evident, whether multi-cycle runs converge.
