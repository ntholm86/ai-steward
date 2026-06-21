# retrospect.md — ai-steward

_Last updated: 2026-06-21 (run: post-v1-milestone-config-surface)_

---

## Current claims

**1. The mandate gate is now a hard structural filter, not background context.**
The token-budget cycle (autonomous run, 2026-06-21) exposed the gap: a model without an explicit mandate check produces proposals consistent with the codebase but unrelated to the destination. The new 5-step SCAN protocol closes this with Step 1 as a mandatory gate — the model must quote an exact destination sentence or return `{"nothing": true}`. The first run under the new protocol self-rejected correctly (NOTHING FOUND). One run proves the gate fires; it does not yet prove the gate holds under repeated pressure.
**Falsifiable by:** a SCAN run that produces an off-mandate proposal despite the 5-step prompt.

**2. V1 proof is complete. The convergence gap is the next critical untested claim.**
External targeting (vectorium, TypeScript), self-targeting (ai-steward), and mandate-gated SCAN are all demonstrated. What has never been tested: multi-cycle convergence — does the loop stop cleanly when SCAN returns nothing_found across N consecutive runs? Running more single cycles produces no new evidence on this claim. The proof requires a loop, not another pass.
**Falsifiable by:** a multi-cycle run that fails to stop, or that stops prematurely before the mandate is satisfied.

**3. The cost model in the destination’s Current State section is now obsolete.**
The V1 target was “~$0.002 per improvement cycle (haiku, 2 LLM calls).” The actual operating cost under claude-sonnet-4-5 with the 5-step reasoning protocol is ~$0.03/cycle — roughly 15×. The destination explicitly approved trading cost for quality, but the Current State section still declares the $0.002 target. This discrepancy between declared cost model and actual operation is a source of confusion for any operator reading the destination.
**Falsifiable by:** a cycle under the current prompt that consistently costs ≤$0.003.

**4. The RECORD phase is the largest gap between destination and implementation.**
The destination defines: Reflection (second LLM call synthesizing outcomes), across-trail trigger evaluation, and Candidate Next Moves appended to autonomous trail entries. None of these exist in `record.py`. SCAN received intensive attention this session; RECORD has been untouched since initial implementation. An autonomous improvement cycle cannot produce a trail entry that looks like the trail skill’s output until RECORD is rebuilt. The gap grows with every SCAN improvement.
**Falsifiable by:** showing an autonomous trail entry that contains Reflection, trigger evaluation, and Candidate Next Moves.

**5. A duplicate trail entry was created this session.**
“scan-reasoning-quality + V1-milestone-confirmed” appears twice at the end of the trail (entries 34 and 35, both dated 2026-06-21). Both are structurally identical. This reveals that the Trail skill has no duplicate detection gate — it cannot check whether the most recent entry already covers the current session before appending. The duplicate does not corrupt the trail (it is append-only) but inflates the entry count and creates ambiguity in future arc-reads.
**Falsifiable by:** showing the two final entries have distinct content.

**6. The shared .acm/ evidence layer is an achieved structural fact, not a goal.**
Both skills (human-supervised) and ai-steward (autonomous) write to the same `audit-trail.md`, governed by the same `destination.md`. The ORIENT phase — feeding `retrospect.md` and `learning.md` into SCAN — will close the loop: the autonomous pipeline reads the same synthesis the human sessions produce. The integration architecture is complete conceptually; ORIENT implementation is the remaining step.
**Falsifiable by:** showing a SCAN run that receives retrospect.md content in its context.

**7. The config surface is defined before it needs to exist.**
`max_cost_per_cycle_usd`, memory, retrospect, reasoning, and escalation parameters are captured in destination.md (2026-06-21 entry). None implemented. This is the correct order — design-in before bolt-on — consistent with the destination’s “solve by design” principle. The risk is that destination entries without implementation become aspirational clutter if not implemented within 2–3 sessions.
**Falsifiable by:** showing these config fields in `config.py` and `.ai-steward.yaml`.

---

## What the next runs should test

1. **Multi-cycle convergence (highest priority).** Run ai-steward against an external repo in a loop until SCAN returns nothing_found twice consecutively. Verify the loop stops without operator intervention. This is the central proof gap. Until it is tested, the “Convergence Is Silence” principle is stated but undemonstrated.

2. **Cost model correction.** Update the Current State section of destination.md to reflect actual ~$0.03/cycle cost under the sonnet-4-5 + 5-step protocol. The discrepancy with the $0.002 target should be acknowledged, not silently contradicted.

3. **RECORD reflection.** Implement the Reflection call in `record.py` — second LLM call that synthesizes VERIFY outcome against the prediction, flags mismatches, and appends Candidate Next Moves. This closes the feedback loop in the autonomous pipeline.

4. **ORIENT phase.** Extend `_load_scope_context()` in `scan.py` to also load `retrospect.md` and `learning.md`. The shared evidence layer only produces benefit when the autonomous pipeline reads from it.

5. **Harness ledger integrity.** Verify hash-chain replay on the `.acm/sessions/*.jsonl` files using the harness-protocol spec. The JSONL files exist and are being written; whether they are correctly hash-chained per SPEC §8 has never been tested.

6. **Config surface implementation.** Add `max_cost_per_cycle_usd` and the first memory control fields (`memory.read_retrospect`, `memory.context_chars`) to `AiStewardConfig` and the YAML schema. Implement before ORIENT so ORIENT has its config hooks.

7. **Duplicate entry cleanup.** Append a correction note to the trail acknowledging the duplicate. Do not rewrite in place.

---

## Active operational rules

- **V1 stops before release.** Operator reviews every staged diff. Inviolable.
- **llm-harness-proxy is outside ai-steward’s autonomous scope.** Structural exclusion — changes there require a separate session.
- **Execution layer must remain separate from reasoning layer.** Phases execute; skills reason.
- **ACM §4.2 stop conditions govern scope traversal.** Filesystem root, `.acm-root` marker, 4-level cap.
- **Trail entries are required for all `scan.py` changes.** Any `scan.py` change without a trail entry in the same session is a governance gap.
- **Test SCAN prompt changes with a live run before declaring them correct.** The token-budget tag was committed before being discovered as off-mandate. Live run is the gate for prompt changes.
- **Before appending a trail entry, check if the most recent entry already covers the current session.** The duplicate entry (entries 34–35) was created because Trail ran twice on the same session. Check the most recent entry’s date and subject before appending.
- **The cost model in destination.md must be updated when operating parameters change materially.** A cost target that is 15× off actual operation misleads operators. Update on the same session that changes the model or prompt depth.
- **Do not use PowerShell Set-Content or Get-Content for `.acm/` files.** PowerShell 5.1 silently mojibake-corrupts UTF-8 content (em-dashes, arrows, box-drawing chars) and re-injects BOM. Use Python with `encoding='utf-8'` for all reads and writes to `.acm/` files.

---

## Loop-effectiveness notes

The loop has been heavily concentrated on SCAN quality (steps 1–5 in the pipeline). This is appropriate — SCAN is the intelligence layer, and the mandate gate was a genuine structural gap. However:

- **RECORD has received zero autonomous improvements.** The loop has never turned its attention to its own output format. The trail entries it produces do not match the trail skill standard — no Reflection, no trigger evaluation, no Candidate Next Moves. SCAN and RECORD are equally important; the asymmetry is a structural blind spot.

- **Convergence has not been tested.** The “Convergence Is Silence” principle is named in every destination entry but has never been empirically demonstrated. If the loop produces busy-work proposals indefinitely on a stable target, the principle fails in practice.

- **The quality bar tested so far:** internal mandate alignment (does SCAN propose things consistent with destination?). Bars not tested: whether proposals are accepted by operators at a meaningful rate, whether the audit-trail entries are independently auditable, whether the harness ledger is actually tamper-evident.
