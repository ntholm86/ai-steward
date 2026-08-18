# orientation.md — ai-steward

_Last updated: 2026-08-18 (mini-orient, Improve skill — 3 entries since 2026-07-04 header; not a full REORIENT arc-read)_

---

## Mini-orient addendum — 2026-08-18 (window: destination-reconciliation-shared-mandate, scan-bounded-destination-delivery, bounded-destination-utils-path)

**Arc-claims (falsifiable):**

1. **The destination reconciliation immediately produced the code change it was meant to enable.** Within the same session: the mandate was layered on (entry 1), then a concrete contradiction it created was found and fixed (entries 2-3) — tail-truncation delivering the superseded 2026-06-22 symmetry amendment as SCAN's entire mandate, verified by live-file simulation. The new destination was load-bearing within hours, not aspirational.
   **Falsifiable by:** a future entry showing SCAN or a meta-cognitive phase still receiving stale mandate text after df205ad.

2. **Destination-delivery is now a structurally closed class — one shared extraction path — but the fault line is upstream, not in this repo.** All four LLM phases read destination.md through `_truncate_destination()` in `_utils.py`. The residual risk is that the destination *format* evolves in the skills suite (where the bounded-marker convention was born) while the delivery code lives here; the next break will arrive the same way today's did — silently, one side of the convention only.
   **Falsifiable by:** a third destination-delivery entry appearing after df205ad; if so, treat as shape-shifting and route the format-coupling question to Destination, per the 2026-08-18 entry's own across-trail judgment.

3. **V2 is now unblocked on the "loop reads the wrong thing" axis and blocked only operationally.** The 2026-07-04 claim 3 (11 entries of V2-avoidance) should now be re-judged against the current mandate: the harness (localhost:8474) was unreachable today, so conditions #1 and #2 had an external blocker, not an avoidance signal. The avoidance hypothesis is only testable once the harness is up and a run is available.
   **Falsifiable by:** harness available + a subsequent entry still choosing consolidation over a V2 condition.

**Watch for:** whether the reconciled destination's "Self-knowledge duties" section changes SCAN's behavior in the first live run — it is the first destination content written *to* the loop about *the loop*, and its effect (or absence) is direct evidence about how much destination text shapes proposals.

**Not updated:** "Current claims" (1-10) and "Active operational rules" remain the last full REORIENT output. Claims 7 (external repo unvalidated) and 8 (tests verify structure, not behavior) are unaffected by this window. Claim 1 (V1 ACHIEVED) stands. The counting window for the next mini-orient starts from this header.

---

## Mini-orient addendum — 2026-07-04 (auditonomy skill, window: entries 2-11 since 2026-06-23 header)

**Arc-claims (falsifiable):**

1. **The post-consolidation window (entries 1-9, all dated 2026-06-23) was consolidation, not new capability.** Three DRY loader extractions (`_load_destination`, `_load_current_retrospect`, `_load_learning` → `_utils.py`), a terminology rename completed across prompt files, and one substantive addition (learning.md wired into GRADUATE + its system prompt). No new phase or pipeline capability shipped in this window.
   **Falsifiable by:** a future entry in the next window that adds a new phase/capability rather than consolidating an existing one.

2. **Trail hygiene lagged code hygiene in this window.** Code stayed disciplined throughout (187→189 tests, all green, mypy clean at every entry checked). But: two back-to-back identical `retrospect-to-orientation-rename` entries appeared (2026-06-23) with no `[!REVERSAL]` or explanation, and went unflagged for 2+ subsequent entries; separately, the mini-orient itself was due at entry #5 and #10 of this window and was not run either time (this pass is the catch-up).
   **Falsifiable by:** the duplicate entry being corrected or explained in a later pass, or a future mini-orient trigger being honored on schedule without operator prompting.

3. **V2 made zero forward progress across this entire 11-entry window.** All four of destination.md's V2 conditions (live multi-cycle, external repo run, cost-cap live validation, compounding-error detection) are untouched. Every entry in the window's own "Candidate Next Moves" repeatedly named "external repo validation" or "live multi-cycle run" as a top candidate, and every following entry chose something else instead (DRY extraction, prompt sync, README accuracy, orient-budget wiring).
   **Falsifiable by:** an external-repo or multi-cycle run entry appearing in the next window.

**Watch for:** if a 12th consecutive entry since 2026-06-23 still hasn't touched a V2 condition, that is no longer "reasonable sequencing" — it is avoidance, and should be named as such rather than quietly continued past.

**Not updated:** the "Current claims" (1-10) and "Active operational rules" sections below are the last full REORIENT output and are left as-is — this addendum is additive, per this mini-orient's deliberately narrow read window (last ~10 entries, not the full trail).

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
