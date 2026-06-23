# orientation.md — ai-steward

_Last updated: 2026-06-23 (run: post-destination-consolidation)_

---

## Current claims

**1. V1 is ACHIEVED.**
GRADUATE classified V1 as ACHIEVED on 2026-06-22 after two consecutive NOTHING FOUND cycles. The self-targeting milestone passed: ai-steward runs against its own repository, proposes improvements, applies them, verifies them, and records the trail. 187 tests. All phases wired. The structural proof holds.
**Falsifiable by:** a self-targeting run that produces a structurally malformed trail entry or misses a genuine finding that prior entries did not already address.

**2. One run = one session file (verified live).**
Session 01KVS6HP18E5TN0RD8M53YAWWS.jsonl contains SCAN (seq=0), IMPLEMENT (seq=1), REFLECT (seq=2) — three hash-chained entries in a single file. The X-Harness-Session grouping works. All LLM calls inside one harness_session() context land in one .acm/sessions/<sid>.jsonl.
**Falsifiable by:** a run that produces multiple session files for a single cycle, or entries with mismatched sid values.

**3. HARNESS_ROOT is structurally impossible to omit.**
harness_session() sets HARNESS_ROOT in the environment before yielding. anthropic_client() reads it automatically. No call site passes it explicitly — the context manager guarantees the header. The class-2 bug (calling anthropic_client without harness_root) is impossible by design since commit d6b597c.
**Falsifiable by:** a session file appearing outside .acm/sessions/ in a properly-wrapped run.

**4. Scope gate is code-level, not prompt-level.**
Both _parse_finding() and _collect_files() use Path.full_match() on repo-relative paths to enforce scope.allowed and scope.blocked. System-prompt instructions are soft constraints the model can reason around (demonstrated entry 75 cycle 3). The code gate is the structural boundary.
**Falsifiable by:** an out-of-scope proposal bypassing the code-level gate.

**5. Meta-cognitive phases are implemented and wired.**
REORIENT (every N successes), GRADUATE (2 consecutive NOTHING FOUND), ESCALATE (N consecutive failures) — all implemented, unit-tested, and triggered automatically by run-loop. run-loop also enforces budget_usd at runtime (stops loop when exceeded). The activation path exists.
**Falsifiable by:** a run-loop invocation that reaches a trigger condition without firing the corresponding phase, or exceeds budget without stopping.

**6. Graduate system prompt declares learning.md as 4th input.**
graduate.py loads learning.md (pre-extracted [!REALIZATION]/[!REVERSAL] markers). graduate_system.md now explicitly lists it as input #3 and provides usage guidance: treat as primary pattern evidence, cite by slug, do not double-count with raw trail.
**Falsifiable by:** GRADUATE producing a proposal that re-derives a learning.md pattern from raw trail without citing the learning entry.

**7. External repo targeting remains unvalidated post-fix.**
Vectorium was tested once (entry 26), revealed a VERIFY deletion-guard gap that was fixed. No external run has been done since the fix. The generalization claim is structurally sound but empirically untested.
**Falsifiable by:** a successful external repo run post deletion-guard fix.

**8. Unit tests verify structural correctness, not behavioral quality.**
187 tests verify phase contracts, config structure, and code paths. None verify whether SCAN reasoning is genuine, REFLECT reflection is meaningful, or REORIENT arc-claims are accurate. Behavioral quality is visible only through live runs.
**Falsifiable by:** a unit test that detects low-quality or empty model reasoning.

**9. Cost model is current: ~.15-0.20 per cycle.**
claude-sonnet-4-5, 3 LLM calls (SCAN + IMPLEMENT + REFLECT). Every trail entry records tokens and estimated USD. Haiku at .002/cycle is the V2 cost target once behavioral quality is validated at sonnet level.
**Falsifiable by:** a cycle that costs significantly outside this range under the same config.

**10. Destination consolidated 2026-06-23.**
V1 ACHIEVED declared. V2 destination adopted from graduate_proposal.md: four conditions (live multi-cycle, external repo, cost-cap enforcement, compounding-error detection). Historical record preserved below the consolidated section.
**Falsifiable by:** a SCAN run that reads destination.md and acts on stale V1 claims.

---

## What V2 needs to close

1. **Live multi-cycle run** — run-loop completes with REORIENT firing, GRADUATE or ESCALATE firing, retrospect rewrite validated.

2. **External repo run** — post-deletion-guard fix; generalization proven beyond self-targeting.

3. **Cost-cap enforcement live** — loop stops on budget_usd, not just max_iterations. (Code exists; needs live validation.)

4. **Compounding-error detection** — N>=3 cycle run; stale claim at cycle N does not corrupt SCAN reasoning at cycle N+1.

---

## Active operational rules

1. **System-prompt instructions are soft constraints.** Any behavioral constraint that matters for correctness or safety MUST be enforced in code, not just in the prompt. (Entry 75 cycle 3.)

2. **Live runs are required to validate prompt and token-budget changes.** Unit tests cannot verify model reasoning quality under operational conditions.

3. **Truncate destination.md from the tail, not the head.** The file is append-only; newest content is at the bottom. Use [-N:] slices.

4. **Never accept convergence without an arc-read.** Single-cycle silence is not structural silence. Run retrospect before declaring the destination closed.

5. **Do not modify .acm/destination.md from within the autonomous pipeline.** Operator-held artifact. Autonomous phases may read it, not write it.

6. **Check the trail before appending.** Verify no duplicate slug before writing a new entry.

7. **Code changes that add new context to LLM prompts require two commits.** One for the code (what data is delivered), one for the system prompt (how the model should interpret it). These are structurally coupled but not in the same file.

8. **Path.match() is unreliable for multi-level glob patterns.** Use Path.full_match() on repo-relative paths for scope enforcement. (Entries 80-81.)

---

## Loop-effectiveness notes

The loop is functioning at all three layers: execution (phases), governance (harness capture), and meta-cognition (REORIENT/GRADUATE/ESCALATE).

V1 ACHIEVED. The transition from V1 to V2 is behavioral validation: proving the structure generalizes under operational conditions without human cycle-by-cycle supervision.

**What this retrospect cannot yet validate:**
- Multi-cycle compounding error patterns (requires N>=3 cycle run)
- External repo generalization (requires vectorium or similar)
- REORIENT arc-claim accuracy under long-running loops

The next retrospect should run after V2 condition #1 (live multi-cycle) completes.
