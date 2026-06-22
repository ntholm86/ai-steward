# retrospect.md — ai-steward

_Last updated: 2026-06-22 (run: post-multi-cycle-convergence)_

---

## Current claims

**1. Multi-cycle convergence is validated.**
Entry 75 ran 5 cycles against ai-steward itself. Result: 1 genuine change (reflect model field), then 3 consecutive NOTHING FOUND (cycles 2, 4, 5). Cycle 3 was VERIFY FAILED due to scope gate bug — which the run discovered and fixed. The "Convergence Is Silence" principle is now empirically demonstrated, not just stated.
Silence on: self-targeting convergence. Bar tested: internal text-layer correctness for `src/**/*.py`. Bars not tested: external repo convergence, workspace-level mandate conflicts, custom lens behavior in production.
**Falsifiable by:** a multi-cycle run that fails to stop cleanly after exhausting genuine findings.

**2. System-prompt instructions are soft constraints — all constraints that matter must be enforced in code.**
Cycle 3 of the convergence run exposed this: SCAN proposed `tests/test_scan.py` (blocked by `scope.blocked: [tests/**]`) by reasoning around the file-list instruction. The prompt said "choose from the provided file list" — the model ignored it. Fix: added code-level scope enforcement in `scan.py` (lines 445–453). Two new tests.
This generalizes the "trust but verify" principle to LLM pipelines: the model will follow instructions most of the time, but the pipeline must be structurally correct even when it doesn't.
**Falsifiable by:** an out-of-scope proposal that bypasses the code-level gate.

**3. ORIENT context now delivers both arc-claims and operational rules.**
Entry 52 fixed a silent failure: the prior 1000-char head window delivered only 12% of retrospect.md, missing all operational rules. Now: 2000-char head window + unconditional `## Active operational rules` section extraction. Contract-tested.
**Falsifiable by:** a SCAN context inspection showing operational rules absent from the model's input.

**4. Single-cycle pipeline structural parity with human trail entries is complete.**
All required fields: Prediction (entry 37), Lenses/examination_summary (entry 42), Blind spot, Reflection (entry 47), Trigger evaluations (entry 47), Token counts, Cycle cost (entry 46), Harness session links (entry 50). 112 tests. Autonomous trail entries are structurally indistinguishable from human-supervised ones.
**Falsifiable by:** an autonomous trail entry structurally missing a field that a human-supervised entry would include.

**5. Unit tests alone are insufficient for prompt and token-budget changes; live runs are required.**
Entry 44: max_tokens=1024 passed 81 unit tests but failed immediately in live run. Entry 75: scope bypass passed all tests but failed in live multi-cycle run. Unit tests structurally cannot test "does the model actually obey the prompt under operational conditions?"
**Falsifiable by:** a prompt change that passes unit tests and live runs without issue.

**6. The cost model in destination.md is current.**
Entry 72 appended the correction: actual validated cost ~$0.027–0.030/cycle at claude-sonnet-4-5 + 3-call pipeline. The prior claim #6 from the last retrospect is now falsified — destination.md no longer shows "$0.002" without qualification.
**Falsifiable by:** destination.md showing outdated cost figures without correction annotation.

**7. Duplicate trail entries 34–35 remain unaddressed.**
Not blocking. Structural cleanliness gap only. The operational rule (check before appending) prevents recurrence.

**8. The operator-gate rejection pattern is working correctly.**
Two documented rejections: record.py `[!REVERSAL]` placeholder abuse (entries 18–19, 28), and the cycle-3 scope bypass (entry 75). Both caught by operator review, discarded, and trailed. The review workflow functions.
**Falsifiable by:** a rejected proposal not recorded in the trail.

**9. The V2 cost optimization (dedicated reflect model) is structurally enabled.**
Entry 74 added `reflect: str | None = None` to ModelAssignment with backward-compatible defaulting to `analyze`. Operators can now assign a cheaper model (e.g. haiku) to REFLECT without changing SCAN's model. The destination's named optimization is no longer blocked.
**Falsifiable by:** a config that sets `reflect: claude-haiku-4-5` failing to use haiku for REFLECT.

**10. The governance infrastructure is structurally complete.**
Entries 36–75 (40 iterations over 4 days) built and validated: SCAN reasoning quality, RECORD fields, ORIENT context, REFLECT phase, harness coverage, CONFIG surface, scope enforcement. With the multi-cycle convergence validation, the infrastructure has been played, not just built.
**Falsifiable by:** discovery of a missing structural component required for V1 operation.

---

## What the next runs should test

1. **External repo targeting** — the pipeline has only been tested against itself. The vectorium run (entry 26) exposed the deletion-guard gap; the fix has not been re-validated. Run against a TypeScript or mixed-language repo to test the binary heuristic, skip-dirs, and custom verify_command paths.

2. **Workspace-level destination conflicts** — cycle 3 showed SCAN reading the workspace-level `.acm/destination.md` and using it to justify test-coverage proposals that hit the blocked scope. If workspace-level mandates systematically steer toward blocked targets, the pipeline wastes tokens. Examine whether this is happening.

3. **Custom lens behavior in production** — entries 69–71 wired `lenses` and `reflect_lenses` config fields. Never live-tested with non-default lens sets. Run with a custom lens configuration to validate the prompt wiring.

4. **Harness ledger hash-chain integrity** — structural mechanism exists but has never been exercised end-to-end. Verify that a session JSONL tampered after capture is detected.

5. **Haiku-for-REFLECT cost measurement** — now that `reflect:` is a separate field, measure actual cost difference: `reflect: claude-haiku-4-5` vs. inheriting sonnet. Document whether the quality tradeoff is acceptable.

---

## Active operational rules

- **V1 stops before release.** Operator reviews every staged diff. Inviolable.
- **llm-harness-proxy is outside ai-steward's autonomous scope.** Structural exclusion.
- **Execution layer must remain separate from reasoning layer.** Phases execute; skills reason.
- **ACM §4.2 stop conditions govern scope traversal.** Filesystem root, `.acm-root` marker, 4-level cap.
- **Trail entries required for all scan.py changes.** No scan.py change without a trail entry in the same session.
- **Test SCAN prompt changes with a live run before declaring correct.** Unit tests cannot detect token-budget overruns (entry 44) or prompt-bypass behaviors (entry 75).
- **Before appending a trail entry, check for duplicate.** Entries 34–35 show the cost of skipping.
- **Use Python (not PowerShell) for all `.acm/` file reads and writes.** PowerShell 5.1 mojibakes UTF-8.
- **Write contract tests when adding new pipeline context injections.** Entries 50–52 established this pattern.
- **Bound every silence claim.** Name which quality bar and which surfaces.
- **Do not place `[!REVERSAL]` as a placeholder for future data.** It marks actual reversals only.
- **System-prompt instructions are soft constraints — enforce in code.** Entry 75: the model bypassed the scope constraint by reasoning around it. Any behavioral constraint that matters for correctness must be structurally enforced.

---

## Loop-effectiveness notes

**What changed since the prior retrospect (post-governance-layer-completion):**
- Multi-cycle convergence run completed (entry 75): 5 cycles, 1 change, 3 NOTHING FOUND, 1 bug discovered and fixed
- Scope gate bug found and closed (code-level enforcement in scan.py)
- V2 cost optimization structurally enabled (reflect model field)
- Cost model correction applied (entry 72)
- 97 → 112 tests

**What the loop has been challenged on and passed:**
- Multi-cycle convergence: validated (cycles 2, 4, 5 = stable silence)
- Scope bypass: discovered and closed within the same run
- ORIENT context delivery: corrected (entry 52), contract-tested

**What the loop has NOT been challenged on:**
- External repo targeting: vectorium run was pre-deletion-guard; post-fix validation pending
- Workspace-level mandate steering: observed but not examined for systematic waste
- Custom lens configurations: structurally wired but never live-tested
- Harness hash-chain integrity: mechanism exists, never exercised
- Haiku-for-REFLECT quality tradeoff: structurally enabled but not measured

**What kind of finding would this loop structurally miss?**
1. Failures requiring external context the loop doesn't have (e.g., actual user adoption feedback)
2. Cross-repo coordination issues (the loop targets one repo at a time)
3. Subtle quality degradation under cheaper model configurations (the loop tests correctness, not quality)

**Loop-effectiveness verdict:**
The loop is functioning correctly. The multi-cycle run found a genuine bug (scope gate), applied a genuine improvement (reflect field), and then converged cleanly. The governance infrastructure has been validated under operational conditions. The next challenge is breadth: external repos, custom configurations, and the quality tradeoffs enabled by V2 cost optimizations.
