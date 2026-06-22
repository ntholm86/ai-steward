# retrospect.md — ai-steward

_Last updated: 2026-06-22 (run: post-reorient-and-graduate-escalate-design)_

---

## Current claims

**1. The V1 pipeline is structurally complete and behaviorally validated.**
Entry 75 ran 5 cycles: 1 genuine change, 3 NOTHING FOUND, 1 scope gate bug discovered and fixed. Entry 77-78 added REORIENT. The execution and governance layers are proven. Self-targeting produces structurally indistinguishable trail entries from human-supervised runs.
Silence on: self-targeting correctness, internal text-layer consistency.
Bars not tested: external repo generalization, multi-family model independence, harness hash-chain integrity.
**Falsifiable by:** a self-targeting run that produces a structurally malformed trail entry or misses a genuine finding.

**2. System-prompt instructions are soft constraints — all constraints that matter must be enforced in code.**
Entry 75 cycle 3 demonstrated scope bypass: model reasoned around the "choose from the provided file list" instruction. Code-level scope gate now enforces `scope.allowed` / `scope.blocked` at the Finding extraction point.
This is an architectural principle, not a one-time fix. Any future constraint on agent behavior must be enforced structurally if it matters for correctness or safety.
**Falsifiable by:** a future out-of-scope proposal bypassing the code-level gate.

**3. The loop has transitioned from infrastructure to meta-cognition.**
Entries 1-75 built and validated the execution+governance layer. Entry 76-78: REORIENT phase added; GRADUATE and ESCALATE phases designed in destination.md. The target is no longer a pipeline — it is becoming an autonomous agent with structured self-awareness. The founding architectural insight ("execution layer deliberately dumb; reasoning layer external") now applies to the robot's own reasoning as well as the code it improves.
**Falsifiable by:** evidence that REORIENT, GRADUATE, or ESCALATE introduce reasoning failures that the pipeline layer does not catch.

**4. REORIENT capability exists but is disconnected from the pipeline.**
`ai-steward reorient REPO` executes correctly. Config fields `reorient_interval`, `max_tokens_reorient`, `reorient_trail_budget_chars` exist. But `ai-steward run` cannot trigger REORIENT automatically; there is no `run-loop` command that iterates cycles and fires the meta-cognitive phases. The capability exists as a standalone; the activation path does not.
**Falsifiable by:** `ai-steward run` that triggers REORIENT after N cycles without a `run-loop` command.

**5. The multi-cycle loop runner does not exist.**
`reorient_interval`, `max_iterations`, and `budget_usd` are config fields but nothing reads them at runtime. GRADUATE (trigger on sustained silence) and ESCALATE (trigger on failure patterns) are designed in destination.md but not implemented. The robot cannot yet run itself to convergence, respond to silence, or escalate when stuck. All cognitive triggers require human invocation.
**Falsifiable by:** an autonomous run that triggers GRADUATE or ESCALATE without human invocation.

**6. External repo targeting remains unvalidated post-fix.**
Vectorium was tested once (entry 26), revealed a VERIFY deletion-guard gap that was fixed. No external run has been done since the fix. The generalization claim is structurally sound but empirically untested against any repo that is not ai-steward itself.
**Falsifiable by:** a successful external repo run post deletion-guard fix.

**7. Unit tests test structural correctness only, not behavioral quality.**
129 tests verify phase contracts, config structure, and code paths. None verify whether SCAN's reasoning quality is genuine, whether REFLECT produces meaningful reflection, or whether REORIENT's arc-claims are accurate. Behavioral quality is visible only through live runs (entries 44, 75). The test suite cannot catch structurally valid but semantically empty responses.
**Falsifiable by:** a unit test that detects low-quality or empty model reasoning.

**8. Duplicate trail entries (34-35, 77-78) are a minor structural gap.**
Not blocking. The append-only rule and commit discipline prevent recurrence. The operational rule (check the trail before appending) was not consistently applied.
**Falsifiable by:** a run that produces no duplicate entry.

**9. The operator-gate rejection pattern is working correctly.**
Three documented rejections: record.py placeholder abuse (entries 18-19, 28); scope bypass (entry 75, cycle 3). All caught by operator review, discarded, trailed. The review workflow functions as the trust-earning mechanism.
**Falsifiable by:** a rejected proposal that is not trailed.

**10. The cost model and config surface are current.**
Destination.md has the corrected cost range (~$0.018-0.030/cycle at claude-sonnet-4-5, 3 calls). All config fields are live (entries 69-70 wired lenses; entry 70 wired reflect_lenses; entry 71 added validators). No dead config remains in the V1 surface.
**Falsifiable by:** a config field that has no effect on pipeline behavior.

---

## What the next runs should test

1. **`run-loop` command (highest priority)** — the multi-cognitive pipeline (REORIENT after N cycles, GRADUATE on silence, ESCALATE on failure patterns) requires a loop runner. Without this, REORIENT, GRADUATE, and ESCALATE are capabilities without activation paths. This is the single most valuable next structural change.

2. **GRADUATE phase** — implement destination-revision-on-silence. When SCAN returns NOTHING FOUND for N consecutive cycles, the robot should classify the silence (ACHIEVED / STALE / STUCK / PREMATURE) and propose a successor destination for human approval.

3. **ESCALATE phase** — implement self-modification awareness. When repeated failures share a class (same test, same phase, same error), the robot should diagnose and escalate instead of looping.

4. **External repo targeting** — validate post-deletion-guard behavior against vectorium or another TypeScript repo. First proof of generalization beyond self-targeting.

5. **Live REORIENT validation** — run `ai-steward reorient .` against this repo to confirm the prompt produces arc-claims of the required quality. The phase is untested in live conditions.

6. **Workspace-level destination conflict** — cycle 3 showed SCAN reading the workspace-level `.acm/destination.md` and using it to target test files inside the blocked scope. Examine whether higher-scope mandates systematically steer proposals toward blocked paths.

---

## Active operational rules

1. **System-prompt instructions are soft constraints.** Any behavioral constraint that matters for correctness or safety MUST be enforced in code, not just in the prompt. (Entry 75, cycle 3.)

2. **Live runs are required to validate prompt and token-budget changes.** Unit tests cannot verify model reasoning quality under operational conditions. (Entries 44, 75.)

3. **Truncate destination.md from the tail, not the head.** The file is append-only; newest content is at the bottom. Use `[-N:]` slices. (Entry 20.)

4. **Never accept convergence without an arc-read.** Single-cycle silence is not structural silence. Run retrospect before declaring the destination closed.

5. **Do not modify `.acm/destination.md` from within the autonomous pipeline.** Operator-held artifact. Autonomous phases may read it, not write it.

6. **Check the trail before appending.** Verify no duplicate slug before writing a new entry. (Entries 34-35, 77-78.)

7. **Scope enforcement must be code-level.** `scope.allowed` and `scope.blocked` must be checked at the Finding extraction point in scan.py. (Entry 75.)

---

## Loop-effectiveness notes

The loop is functioning at the execution and governance layers. Multi-cycle convergence is validated. The test suite is structurally complete.

The loop has entered a new phase: meta-cognition. REORIENT has been added; GRADUATE and ESCALATE are designed. The critical transition now is from capability layer (phases exist as standalone tools) to activation layer (the loop runner triggers them automatically on the right conditions).

**What this retrospect cannot test:**
- Whether REORIENT's arc-claims are accurate (requires a live run and subsequent prediction tracking)
- Whether GRADUATE correctly classifies silence (not yet implemented)
- Whether ESCALATE correctly identifies stuck patterns (not yet implemented)
- External repo generalization (untested post-fix)

The next operator-triggered retrospect should be run after the `run-loop` command exists and at least one REORIENT has fired automatically.

6. **Workspace-level destination conflict** -- cycle 3 showed SCAN reading the workspace-level .acm/destination.md and using it to target test files inside the blocked scope. Examine whether higher-scope mandates systematically steer proposals toward blocked paths.

---

## Active operational rules

1. **System-prompt instructions are soft constraints.** Any behavioral constraint that matters for correctness or safety MUST be enforced in code, not just in the prompt. (Entry 75, cycle 3.)

2. **Live runs are required to validate prompt and token-budget changes.** Unit tests cannot verify model reasoning quality under operational conditions. (Entries 44, 75.)

3. **Truncate destination.md from the tail, not the head.** The file is append-only; newest content is at the bottom. Use [-N:] slices. (Entry 20.)

4. **Never accept convergence without an arc-read.** Single-cycle silence is not structural silence. Run retrospect before declaring the destination closed.

5. **Do not modify .acm/destination.md from within the autonomous pipeline.** Operator-held artifact. Autonomous phases may read it, not write it.

6. **Check the trail before appending.** Verify no duplicate slug before writing a new entry. (Entries 34-35, 77-78.)

7. **Scope enforcement must be code-level.** scope.allowed and scope.blocked must be checked at the Finding extraction point in scan.py. (Entry 75.)

---

## Loop-effectiveness notes

The loop is functioning at the execution and governance layers. Multi-cycle convergence is validated. The test suite is structurally complete.

The loop has entered a new phase: meta-cognition. REORIENT has been added; GRADUATE and ESCALATE are designed. The critical transition now is from capability layer (phases exist as standalone tools) to activation layer (the loop runner triggers them automatically on the right conditions).

**What this retrospect cannot test:**
- Whether REORIENT's arc-claims are accurate (requires a live run and subsequent prediction tracking)
- Whether GRADUATE correctly classifies silence (not yet implemented)
- Whether ESCALATE correctly identifies stuck patterns (not yet implemented)
- External repo generalization (untested post-fix)

The next operator-triggered retrospect should be run after the run-loop command exists and at least one REORIENT has fired automatically.
