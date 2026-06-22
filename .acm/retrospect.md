# retrospect.md — ai-steward

_Last updated: 2026-06-22 (run: post-governance-layer-completion)_

---

## Current claims

**1. The mandate gate is live-validated, not just structurally implemented.**
The 5-step SCAN protocol has been tested in live runs (entries 44, 49). The mandate gate works under operational conditions: a NOTHING FOUND that correctly deferred an off-mandate finding, a genuine mandate-aligned proposal accepted by the operator. The gate is empirically demonstrated, not just specified.
**Falsifiable by:** a SCAN run that produces an off-mandate proposal despite the 5-step prompt.

**2. Multi-cycle convergence is the critical untested architectural claim.**
The loop has never been run until it self-silences. Convergence Is Silence is named in every destination section but has never been demonstrated in practice. With governance infrastructure now structurally complete (entries 36–52), multi-cycle testing is no longer blocked — it is the next necessary validation. A principle stated but untested is an aspiration, not a claim.
**Falsifiable by:** a multi-cycle run that fails to stop cleanly, or continues past all genuine findings.

**3. Single-cycle pipeline structural parity with human trail entries is complete.**
All single-cycle fields are now structurally correct: Prediction (entry 37), Lenses/examination_summary (entry 42), Blind spot, Reflection (entry 47), Trigger evaluations (entry 47), Token counts, Cycle cost (entry 46), Harness session links (entry 50). The autonomous trail entry is structurally indistinguishable from a human-supervised trail skill entry for the single-cycle case.
Silence on: structural completeness for the single-cycle case. Bars not tested: multi-cycle compounding behavior, whether Candidate Next Moves from autonomous entries are useful to operators, across-trail trigger accuracy over time.
**Falsifiable by:** an autonomous trail entry structurally missing a field that a human-supervised entry would include.

**4. ORIENT context now delivers both arc-claims and operational rules — but was silently broken from day one.**
[!REVERSAL of prior claim 4] The prior retrospect stated "ORIENT is implemented; the autonomous pipeline now reads from the same evidence layer." This was false. The 1000-char head window delivered 12% of retrospect.md — claims #1–2 (partial) and nothing else. Operational rules begin at char 5681. Every SCAN call from entry 40 through entry 51 executed without operational constraints.
Fixed in entry 52: head window raised to 2000 chars, `## Active operational rules` extracted by section header unconditionally. Both are now contract-tested.
**Falsifiable by:** a SCAN context inspection showing operational rules absent from the model's input.

**5. Unit tests alone are insufficient for prompt and token-budget changes; live runs are required.**
The max_tokens=1024 bug (entry 44) passed all 81 unit tests but failed immediately in the first live run. The 5-step reasoning protocol consumed 3977 chars before JSON was emitted, exceeding the budget. Unit tests structurally cannot test "is the model's output long enough to fit in the budget?" — this requires live model calls.
**Falsifiable by:** a prompt or token-budget change that passes unit tests but fails live.

**6. The cost model in destination.md is stale.**
`record.py` uses model-keyed pricing (entry 46) and produces accurate per-entry costs. But `destination.md` still says "~$0.002 per cycle (haiku, 2 LLM calls)." The validated cost under the current configuration (claude-sonnet-4-5, 3 LLM calls: SCAN + IMPLEMENT + REFLECT) is ~$0.027–0.030/cycle. The code is correct; the destination document is not.
**Falsifiable by:** a destination.md that still shows "$0.002" without qualification.

**7. Duplicate trail entries 34–35 are unaddressed.**
Not blocking. Structural cleanliness gap only. The operational rule (check before appending) has been in place since entry 35.

**8. The operator-gate rejection pattern is working correctly.**
One proposal discarded by operator review (record.py [!REVERSAL] placeholder abuse). The rejection is evidence the review workflow functions — the pipeline produced a wrong proposal, the operator caught it, the trail records it.
**Falsifiable by:** a rejected proposal that is not recorded in the trail.

**9. Three consecutive fixes shared a single root cause: no contract tests verifying inputs reach their consumers.**
Entry 50 (harness): session files not verified to be all captured. Entry 51 (CONFIG_TEMPLATE): operator-tunable fields not verified to be in the generated template. Entry 52 (ORIENT): operational rules not verified to be in SCAN context. Each fix added exactly one contract test. The pattern is now mitigated for these three points. Other injection points (e.g., destination.md's tail truncation behavior, learning.md's tail budget) have not been contract-tested.
**Falsifiable by:** discovery of another injection point that lacks a contract test verifying delivery.

**10. The governance infrastructure is structurally complete; the target's weight now lies in behavioral validation.**
Entries 36–52 (17 iterations over two days) built the governance layer: SCAN reasoning quality, RECORD fields, ORIENT context, REFLECT phase, harness coverage, CONFIG surface. The loop has spent this entire arc building the infrastructure that was supposed to be a means to an end. The end — "finds genuine improvements, applies them, verifies them" — has been tested in only ~3 live runs, all single-cycle. The governance infrastructure is a complete instrument. It has not been played.
**Falsifiable by:** a multi-cycle run on a non-trivial target that completes without operator intervention and produces accepted proposals.

---

## What the next runs should test

1. **Multi-cycle convergence** — run `ai-steward run` in a loop until SCAN returns `nothing_found` on a real target. This is the highest-leverage test remaining: it simultaneously validates "Convergence Is Silence," exercises the orient context with accumulating context from prior cycles, and tests compounding behavior that single-cycle testing cannot reach. All governance blockers are cleared.

2. **Cost model correction in destination.md** — append actual validated cost (~$0.027–0.030/cycle at claude-sonnet-4-5 + 3-call pipeline). 2-line append. Stale documentation undermines the "efficiency is measured, not claimed" destination principle.

3. **Model ID variant matching in `_model_cost_per_token()`** — model IDs like `claude-sonnet-4-5-20250514` fall through to the haiku fallback. A `startswith` prefix match would be more robust. Low-effort, high-correctness.

4. **Add `scope` to `_CONFIG_TEMPLATE`** — the scope section (allowed/blocked paths) is the first thing operators need after basic configuration. Currently absent from `ai-steward init` output. Named blind spot since entry 51.

5. **P1 compliance completion** — destination says "SCAN must produce trail entries with visible reasoning." P1 is now structurally implemented but has only been live-validated twice. Verify it holds across multiple proposals of varying complexity.

6. **External repo reliability** — vectorium run exposed a VERIFY gap (bulk deletion, fixed by deletion-guard). The fix has not been re-tested against vectorium. Rerun to confirm.

---

## Active operational rules

- **V1 stops before release.** Operator reviews every staged diff. Inviolable.
- **llm-harness-proxy is outside ai-steward's autonomous scope.** Structural exclusion. Do not propose changes to the proxy binary or its SPEC.
- **Execution layer must remain separate from reasoning layer.** Phases execute; skills reason.
- **ACM §4.2 stop conditions govern scope traversal.** Filesystem root, `.acm-root` marker, 4-level cap.
- **Trail entries required for all `scan.py` changes.** No scan.py change without a trail entry in the same session.
- **Test SCAN prompt changes with a live run before declaring them correct.** Unit tests cannot detect token-budget overruns. The max_tokens=1024 failure (entry 44) established this rule empirically.
- **Before appending a trail entry, check for duplicate.** Entries 34–35 show the cost of skipping this check.
- **Update cost model in destination when operating parameters change materially.** Destination.md still says "$0.002" — this rule applies now.
- **Use Python (not PowerShell) for all `.acm/` file reads and writes.** PowerShell 5.1 silently corrupts UTF-8 (mojibake on em-dash U+2014).
- **Write contract tests when adding new pipeline context injections.** Entries 50–52 all lacked contract tests on delivery; each fix added one. The pattern: if you add a feature that injects data into a consumer, write a test verifying the consumer receives it.
- **Bound every silence claim.** Name which quality bar the silence applies to and which surfaces are in scope. Unbounded silence claims ("the target is in good shape") have been overturned within the same day in the manifesto arc.
- **Do not place `[!REVERSAL]` as a placeholder for future data.** It marks actual reversals in the current session only. (Operator gate caught this in entries 18–19, 28.)

---

## Loop-effectiveness notes

The loop has been focused and effective since the last retrospect. Six improvements landed (entries 47–52) without a failed commit (one within-iteration [!REVERSAL] on a test count in entry 47 — expected noise). The operator-gate is steering correctly.

**What the loop has been exclusively focused on since entry 36:**
The governance layer of ai-steward itself. SCAN quality, RECORD fields, ORIENT context, REFLECT phase, harness coverage, CONFIG surface. This was necessary — the governance layer had to be structurally sound before it could be trusted to run autonomously. It is now structurally sound.

**What the loop has never been challenged on:**
- Multi-cycle convergence: never demonstrated; the loop's defining claim
- Behavioral correctness at scale: 3 live runs total, all single-cycle
- External repo reliability post-deletion-guard: vectorium was tested once, fix not re-validated
- Harness ledger hash-chain integrity: structural mechanism exists, never exercised end-to-end
- Compounding error detection: if ORIENT carries a stale claim that steers cycle N+1 wrong, that failure mode is invisible in single-cycle testing — and was structurally suppressed for entries 40–51 because the operational rules never reached the SCAN model

**What kind of finding would this loop structurally miss?**
Any failure mode requiring two cycles to manifest. The orient context fix (entry 52) is the leading example: the loop could not diagnose its own orientation failure by running one cycle. The retrospect saw it because the retrospect reads the full arc. This class of failure — "the instrument used to detect the problem is also the instrument that's broken" — is only catchable at the arc level.

**Loop-effectiveness verdict:**
The governance infrastructure is complete. Continued single-cycle self-targeting has near-zero expected value. The next session should be a multi-cycle run on a non-trivial target. If the loop is functioning correctly, it will find genuine improvements, apply them cleanly, and stop when there is nothing left. If it is not, the multi-cycle run will surface the failure mode.
