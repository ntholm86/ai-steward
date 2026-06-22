# retrospect.md — ai-steward

_Last updated: 2026-06-22 (run: post-record-field-alignment)_

---

## Current claims

**1. The mandate gate is live-validated, not just structurally implemented.**
The 5-step SCAN protocol has been tested in a live run (entry 43). The first run returned NOTHING FOUND due to a max_tokens bug (the model was proposing the fix for the bug that silenced it). The second run produced a genuine, mandate-aligned proposal (`verify_command` visible in init template) accepted by the operator. The mandate gate works under operational conditions.
**Falsifiable by:** a SCAN run that produces an off-mandate proposal despite the 5-step prompt.

**2. V1 proof is complete. Multi-cycle convergence is the critical untested claim.**
External targeting (vectorium), self-targeting, and mandate-gated SCAN demonstrated. Multi-cycle convergence has never been tested — the loop has never been run until it self-silences. A principle named in every destination section but never demonstrated is an aspiration, not a claim.
**Falsifiable by:** a multi-cycle run that fails to stop cleanly, or runs beyond necessity.

**3. `_build_entry()` field-level correctness is complete for the single-cycle case.**
Six improvements since the last retrospect (entries 40–46) completed the alignment: ORIENT context injection, Expected outcome line removed, examination_summary added, max_tokens configurable, trailing-newline guard, model-keyed pricing. The taxonomy of remaining work has shifted: Prediction, Lenses, Blind spot, Token counts, and Cycle cost are now structurally correct. The remaining gap is Reflection (second LLM call after VERIFY), across-trail trigger evaluation, and Candidate Next Moves — which require architectural changes, not field additions.
**Falsifiable by:** an autonomous trail entry containing genuine Reflection and Candidate Next Moves.

**4. ORIENT is implemented. The autonomous pipeline now reads from the same evidence layer as human-supervised sessions.**
`_load_orient_context()` in `scan.py` reads `.acm/retrospect.md` (first 1000 chars) and `.acm/learning.md` (last 500 chars) into SCAN context. The three-layer context model is complete: destination (multi-scope, section-boundary-aware) + orient (arc-derived state) + files (target code). Every retrospect we write is now consumed by the next autonomous cycle.
**Falsifiable by:** a SCAN run where the model's context does not contain retrospect.md content.

**5. Unit tests alone are not sufficient; live runs are required for prompt and token-budget changes.**
The max_tokens=1024 bug passed all 81 unit tests but was exposed immediately in the first live run. The 5-step reasoning protocol consumed 3977 chars before the JSON was emitted, exceeding the budget. The model was proposing the fix for the exact bug that silenced it — the loop found its own failure mode. V1 test suite coverage is high but structurally cannot cover "is the model's output long enough to fit in the token budget?"
**Falsifiable by:** another prompt or token-budget change that passes unit tests but fails live.

**6. The cost model in destination's Current State section is still stale.**
`record.py` now uses model-keyed pricing (entry 46). But `destination.md` still says "~$0.002 per cycle (haiku)." The code is correct; the documentation is not. The actual validated cost is ~$0.027/cycle at claude-sonnet-4-5 with the 5-step protocol (SCAN 16663 tokens, $0.02683 in entry 43). Note: model-keyed pricing makes future entries accurate regardless of which model runs.
**Falsifiable by:** a destination.md that still shows "$0.002" after this retrospect run.

**7. A duplicate trail entry exists (entries 34–35). Still unaddressed.**
Not blocking; structural cleanliness gap only. The operational rule (check before appending) is now in place.

**8. The operator-gate rejection pattern is working correctly.**
One proposal was discarded by operator review in this arc (record.py [!REVERSAL] placeholder abuse, entry after verify-deletion-guard). The rejection is evidence the review workflow functions — the pipeline produced a wrong proposal, the operator caught it, the trail records it. This is the system working as designed.
**Falsifiable by:** a rejected proposal that is not recorded in the trail.

---

## What the next runs should test

1. **Reflection call architecture** — design and implement the second LLM call in `record.py` that synthesizes VERIFY outcome against the prediction. This is the next class of work. The taxonomy shifted at entry 46: no more field-level gaps to fix; the next improvement is architectural.

2. **Multi-cycle convergence test** — run `ai-steward run` in a loop on a target until SCAN returns `nothing_found`. Demonstrates "Convergence Is Silence" as evidence, not aspiration.

3. **Cost model correction in destination** — append to `destination.md`: actual cycle cost is ~$0.027 under claude-sonnet-4-5 + 5-step protocol. The code is correct; the document is not.

4. **Model ID variant matching in pricing table** — `claude-sonnet-4-5-20250514` would fall through to haiku fallback. A `startswith` match in `_model_cost_per_token()` would be more robust.

5. **Orient context budget tuning** — current retrospect.md is large; 1000 chars covers only the header and first 1–2 claims. The operational rules section likely falls outside the window. A live SCAN inspection would confirm what the model actually receives.

6. **External repo targeting** — vectorium run exposed a VERIFY gap (bulk deletion, size guard asymmetric — fixed by verify-deletion-guard). Rerun against vectorium with the symmetric gate to confirm fix holds under real conditions.

---

## Active operational rules

- **V1 stops before release.** Operator reviews every staged diff. Inviolable.
- **llm-harness-proxy is outside ai-steward's autonomous scope.** Structural exclusion.
- **Execution layer must remain separate from reasoning layer.** Phases execute; skills reason.
- **ACM §4.2 stop conditions govern scope traversal.** Filesystem root, `.acm-root` marker, 4-level cap.
- **Trail entries required for all `scan.py` changes.** No scan.py change without a trail entry in the same session.
- **Test SCAN prompt changes with a live run before declaring them correct.** Unit tests cannot detect token-budget overruns.
- **Before appending a trail entry, check for duplicate.** Entries 34–35 show the cost of skipping this check.
- **Update cost model in destination when operating parameters change materially.** Code corrected (entry 46); destination still needs updating.
- **Use Python (not PowerShell) for all .acm/ file reads and writes.** PowerShell 5.1 silently corrupts UTF-8.
- **Sequence RECORD fixes by effort: 2-line fixes first, significant refactoring second.** Proven effective: entries 41, 42, 46 sequenced correctly.
- **Bound every silence claim.** Silence on `_build_entry()` field-level correctness for the single-cycle case. Bars not tested: Reflection, across-trail trigger evaluation, Candidate Next Moves, multi-cycle behavior.

---

## Loop-effectiveness notes

The loop has been focused and effective since the last retrospect. Six improvements landed (entries 40–46) without a failed commit (one within-iteration [!REVERSAL] on a test assertion in entry 40, one operator-gate rejection on a wrong proposal — both expected and healthy). The operator-gate is steering well: ORIENT was held at the gate for two consecutive retrospects, then implemented cleanly when the gate opened.

**What the loop has never been challenged on:**
- Multi-cycle convergence (the loop's defining claim — never demonstrated)
- Reflection quality (the second LLM call — not yet implemented)
- External repo reliability after VERIFY fix (vectorium was attempted; the deletion-guard fix has not been retested against it)
- Harness ledger hash-chain integrity (structural mechanism exists, never exercised end-to-end)

**What kind of finding would this loop structurally miss?**
Any failure mode that only surfaces across multiple cycles. The loop has been run one cycle at a time. If the orient context carries a stale claim that steers the model toward a wrong proposal in cycle N+1, that compounding-error pattern is invisible in single-cycle testing.
