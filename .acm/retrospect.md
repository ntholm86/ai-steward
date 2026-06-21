# retrospect.md — ai-steward

_Last updated: 2026-06-21 (run: pre-orient-implementation)_

---

## Current claims

**1. The mandate gate is now a hard structural filter, not background context.**
The 5-step SCAN protocol closes the off-mandate gap. One run proven; pattern not yet established.
**Falsifiable by:** a SCAN run that produces an off-mandate proposal despite the 5-step prompt.

**2. V1 proof is complete. Multi-cycle convergence is the critical untested claim.**
External targeting (vectorium), self-targeting, and mandate-gated SCAN demonstrated. Multi-cycle convergence has never been tested. More single cycles produce no new proof.
**Falsifiable by:** a multi-cycle run that fails to stop cleanly.

**3. The cost model in destination’s Current State section is obsolete.**
"~$0.002 per cycle (haiku)" contradicts actual ~$0.03/cycle under claude-sonnet-4-5 + 5-step protocol.
**Falsifiable by:** a cycle under the current prompt that consistently costs ≤$0.003.

**4. RECORD’s structural errors are partially fixed; two remain.**
Prediction field (entry 37) fixed the most visible error. Remaining:
- `*Expected outcome:* {finding.rationale}` uses rationale, not an outcome — 2-line fix, zero-risk
- No Reflection, no trigger evaluation, no Candidate Next Moves in autonomous trail entries — significant work (second LLM call + record.py refactoring)
**Falsifiable by:** an autonomous trail entry containing genuine Reflection, trigger evaluation, and Candidate Next Moves.

**5. The improve–retrospect cadence is steering correctly but is stalled at the operator-gate.**
Two consecutive retrospects (entries 36 and 38) have identified ORIENT as the next move with no improve iteration between them. The arc is not thrashing — the claims are stable. The loop is waiting at the gate. This is the expected V1 behavior (operator reviews before every action) but it means ORIENT has been declared the top priority twice without implementation.
**Falsifiable by:** an ORIENT implementation (entry 39 or later) that proves the gate moved correctly.

**6. A duplicate trail entry exists (entries 34–35). Still unaddressed.**
Not blocking; a structural cleanliness gap.

**7. The shared .acm/ evidence layer is a structural fact; ORIENT is the integration step.**
Until ORIENT is implemented, retrospect.md and learning.md are invisible to the autonomous SCAN context. Every retrospect run adds value that the pipeline cannot yet consume.
**Falsifiable by:** a SCAN run that receives retrospect.md content in its context window.

**8. Config surface: aspirational drift risk increasing.**
Three consecutive sessions where `max_cost_per_cycle_usd` and related fields are "defined but pending." Risk is low while ORIENT is the focus, but the window for clean design-in is finite.

---

## ORIENT implementation brief

When the next improve iteration runs on ORIENT, this is the precise spec:

**What:** Extend `_load_scope_context()` in `scan.py` to also load `.acm/retrospect.md` and `.acm/learning.md` from the repo being scanned, and inject them into the SCAN context window.

**Where:** `scan.py` — `_load_scope_context()` currently reads only `destination.md` at each scope level. Add a second pass that reads `retrospect.md` and `learning.md` from the repo root (not parent scopes — these are repo-scoped artifacts).

**How — context budget:**
- Current total budget: ~3000 chars (1500 higher scopes + 1500 repo destination)
- Add: retrospect up to 1000 chars (arc-claims + active operational rules — most relevant sections)
- Add: learning up to 500 chars (most recent [!REALIZATION] and [!REVERSAL] markers)
- Total new budget: ~4500 chars. Still well within typical context windows.

**Label in user_content:** After the destination section, before the file list:
```
### Current orientation (retrospect):
<truncated retrospect.md>

### Learning surface (recent markers):
<truncated learning.md>
```

**Gate:** If retrospect.md or learning.md does not exist, skip gracefully — not an error.

**Tests to add:**
- `test_scan_includes_retrospect_in_context`: create `.acm/retrospect.md` in tmp_path, verify the mock client receives it in user_content
- `test_scan_includes_learning_in_context`: same for learning.md
- `test_scan_skips_missing_orient_files`: no retrospect.md or learning.md — scan succeeds without them

**Prediction:** After ORIENT, a self-targeting SCAN run will receive the arc-claims and operational rules from the retrospect we just wrote. The "test SCAN prompt changes live" rule and the "Expected outcome uses rationale" known gap will be in the model’s context. Proposals will be informed by the loop’s own history.

---

## What the next runs should test

1. **ORIENT implementation** — implement the brief above. This is the single highest-leverage next move; every retrospect since entry 36 has pointed here.

2. **Fix `*Expected outcome:*` semantic error** — 2-line fix in `_build_entry()`. Can be bundled with ORIENT or done immediately after.

3. **Multi-cycle convergence test** — run the loop until nothing_found fires twice. Demonstrates the principle rather than stating it.

4. **Cost model correction in destination** — update Current State from "$0.002 (haiku)" to ~$0.03/cycle.

---

## Active operational rules

- **V1 stops before release.** Operator reviews every staged diff. Inviolable.
- **llm-harness-proxy is outside ai-steward’s autonomous scope.** Structural exclusion.
- **Execution layer must remain separate from reasoning layer.** Phases execute; skills reason.
- **ACM §4.2 stop conditions govern scope traversal.** Filesystem root, `.acm-root` marker, 4-level cap.
- **Trail entries required for all `scan.py` changes.** No scan.py change without a trail entry in the same session.
- **Test SCAN prompt changes with a live run before declaring them correct.**
- **Before appending a trail entry, check for duplicate.** Entries 34–35 show the cost of skipping this check.
- **Update cost model in destination when operating parameters change materially.**
- **Use Python (not PowerShell) for all .acm/ file reads and writes.** PowerShell 5.1 silently corrupts UTF-8.
- **Sequence RECORD fixes by effort: 2-line fixes first, significant refactoring second.**
