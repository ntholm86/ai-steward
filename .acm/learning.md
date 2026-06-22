# Learning

Auto-generated from `.acm/audit-trail.md` by the `record.py learning --write` command in the autonomous-agent-skills install.
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

## 2026-06-19 — Post-destination-refinement retrospect

**[!REALIZATION]** ** The founding decisions (harness as tokenless capture, dumb execution layer, separation of execution from reasoning) are structurally aligned with the new token-efficiency constraint. The founding vision *enables* token efficiency; the June refinement *requires* it.

## 2026-06-19 — Post-destination-refinement retrospect

**[!REALIZATION]** ** The existing code (config.py) encodes the full vision — five-phase model assignment with model-family independence — while V1 explicitly says "single-model operation." This is a concrete gap. Either the config needs simplification, or V1 inherits scaffolding it said it would defer.

## 2026-06-19 — Post-destination-refinement retrospect

**[!REALIZATION]** ** The deepest uncertainty: can the autonomous loop produce acceptable proposals without tier 2/3 reasoning? The destination asserts tier 0/1 is sufficient for routine improvements. V1 is the test. If it fails, the token-efficiency constraint conflicts with the earned-delegation destination.

## 2026-06-19 — Improve: config.py docstring correction (V1 / V2 framing)

**[!REALIZATION]** `:* not fired.

## 2026-06-19 — Improve: V1 pipeline design

**[!REALIZATION]** `:* not fired — design is consistent with all founding realizations.

## 2026-06-19 — Improve: harness.py — structural Observable Autonomy

**[!REALIZATION]** `:* not fired.

## 2026-06-19 — Improve: pipeline loop skeleton + PRE-FLIGHT gates

**[!REALIZATION]** `:* not fired.

## 2026-06-19 — Improve: VERIFY phase + rollback utility

**[!REALIZATION]** :* not fired.

## 2026-06-19 — Improve: VERIFY phase + rollback utility

**[!REVERSAL]** ** Prediction partially failed — 2 test bugs. Both pass-path tests triggered the 2x size guard inadvertently (6-byte original, 19-byte modified = 3x). The verify.py code was correct. Fixed by using same-size file content. Three runs to get to green (initial fail, stale assertion, pass).

## 2026-06-19 — Improve: SCAN phase

**[!REALIZATION]** below.

## 2026-06-19 — Improve: SCAN phase

**[!REALIZATION]** :* not fired.

## 2026-06-19 — Improve: SCAN phase

**[!REALIZATION]** ** CRLF is a recurring test-infrastructure hazard in this codebase. Every test that writes a file with `write_text` and then compares byte sizes will produce a CRLF mismatch on Windows. The pattern to remember: when byte size matters, use `write_bytes(content.encode("utf-8"))` to control exact on-disk layout. This will fire again in any test that exercises VERIFY's 2x size gate with newly-written test files.

## 2026-06-19 — Improve: SCAN phase

**[!REALIZATION]** :* not fired.

## 2026-06-19 — Improve: SCAN phase

**[!REALIZATION]** ** Finding and LoopResult belong in `pipeline/_types.py`. The circular import that forced lazy phase imports in run() is a structural smell. V2 refactor target: move Finding and LoopResult to _types.py, update all phase modules and tests to import from there, restore top-level imports in loop.py.

## 2026-06-19 — Improve: SCAN phase

**[!REALIZATION]** :* not fired.

## 2026-06-19 — Improve: SCAN phase

**[!REALIZATION]** :* not fired.

## 2026-06-19 — Improve: SCAN phase

**[!REALIZATION]** s that aged well:**

## 2026-06-19 — Improve: SCAN phase

**[!REALIZATION]** arc-level (new -- surfaces from arc-read not visible in any iteration):**

## 2026-06-19 — Improve: SCAN phase

**[!REVERSAL]** ** test_implement_returns_original_size_bytes initially used `write_text(original)` and asserted `len(original.encode("utf-8"))`. On Windows, `write_text` emits CRLF, inflating the on-disk size by 4 bytes (32 vs 28). Fixed by using `write_bytes(original.encode("utf-8"))` to control exact byte layout. Same CRLF class as verify tests -- this is now the third occurrence in one session.

## 2026-06-19 — Improve: SCAN phase

**[!REVERSAL]** , multiple [!REALIZATION])

## 2026-06-19 — Improve: SCAN phase

**[!REVERSAL]** markers across 15 entries. Prediction accuracy: high -- most held exactly. One class of mistake repeated 3 times (CRLF/byte-size on Windows), documented and mitigated.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** (arc-level):** The founding hypothesis — "structural guarantees replace social contracts" — validated under operational contact. This is the most important confirmation in the arc. The hypothesis is no longer theoretical.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** (arc-level):** The next gap is not more code. SCAN works but is undirected. The architectural constraint now is schema design for .pea/ memory model before directed SCAN implementation.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** ** The destination.md truncation direction is inverted. The file is append-only (oldest content at top, newest at bottom). Truncating with [:3000] delivers the founding vision from May — correct framing, but the most recent operator decisions (post-V1 direction, .trail/ decision) are cut. The fix is [-3000:] to take the tail. Low-cost correction; high impact on SCAN quality.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** :* not fired.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** -flagged truncation direction defect.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** from the directed SCAN iteration explicitly named this: 	ext[:3000] delivers the founding vision (oldest content); 	ext[-3000:] delivers the most recent operator decisions. The destination.md is append-only. Newest entries are at the bottom. This is a one-line fix with high SCAN quality impact.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** :* not fired — this change RESOLVES the [!REALIZATION] from the prior entry.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** :* not fired — this change RESOLVES the [!REALIZATION] ("Finding and LoopResult belong in pipeline/_types.py") from the loop-wiring entry.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** (arc-level):** The retrospect.md was materially stale. .pea/ references throughout; _types.py marked as outstanding debt; directed SCAN described as "not implemented." The prior retrospect was one day old but three commits behind. Retrospect runs after substantive implementation work should be mandatory, not optional.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** :* not fired.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** :* not fired.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** :* not fired.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** ** The dual purpose (proof + tool) was always implicit but never stated. The consolidation didn't change direction; it made the direction visible. Every decision since May 14 served both purposes.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** ** The remaining P1 gap is structural, not cognitive. SCAN reasons (harness proves it). But the reasoning is NOT visible in the audit-trail.md entry. The destination says "every decision is reasoned, and the reasoning is independently verified." The harness proves reasoning happened; the trail entry should show what it was.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** ** Cost tracking is complete but there's no baseline yet. The ~$ .002/cycle from the first run is the baseline. Future changes evaluated against it.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** :* not fired -- this resolves the P1 gap identified in retrospect.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** :* not fired -- this resolves the placeholder introduced last iteration.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** ** P1 (Commander's Intent + reasoning visibility) is now structurally complete. Both P2 (harness capture) and P1 were listed as preconditions for merging self-targeting runs. Both are now met. The self-targeting gate is open.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** :* not fired.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REALIZATION]** :* not fired.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REVERSAL]** markers across 17 entries. High prediction accuracy. CRLF class documented and mitigated.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REVERSAL]** ** The top-level import promotion broke 3 tests. With lazy imports, monkeypatching scan_mod.scan worked because run() called

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REVERSAL]** fix.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REVERSAL]** ** Prediction of 61/61 on first attempt failed: 7 test_implement.py tests unpacked the return as 3-tuples (`ok, _, _` and `ok, reason, size`). They all raised `ValueError: too many values to unpack`. I missed that test_implement.py calls implement() directly — test_loop.py uses monkeypatched lambdas (which I did update), but test_implement.py unpacks the real return. Fixed by updating all 7 unpackings to use `*_` for the extra values: `ok, *_`, `ok, reason, size, *_`, `_, _, original_size, *_`. 61/61 after fix.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REVERSAL]** ** Prediction of 61/61 on first attempt failed: test_harness.py had two tests asserting `str(tmp_path / ".harness")` that needed updating to `str(tmp_path / ".trail")`. Caught immediately, fixed in same iteration. This is the same pattern as the previous implement-tuple reversal: tests that directly test the changed contract need updating; tests that mock out the whole function do not.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REVERSAL]** fired for the second consecutive iteration (test assertions on changed return contracts). Pattern: when changing a contract that has direct test coverage, those tests need updating. Not a structural problem -- honest coverage catching real changes. Not fired as "recurring problem," fired as "pattern documented."

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REVERSAL]** ` markers across 20+ entries. High prediction accuracy. Recurring class (test assertions on changed contracts) documented and mitigated.

## 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

**[!REVERSAL]** ** Initial test data was ~2585 chars total -- below the 3000-char threshold -- so truncation never fired and both section headings appeared in the output. Fixed by increasing old_section padding from "A" * 2500 to "A" * 3500 (total ~3587 chars). Same class of mistake as the CRLF test failures: test data that does not actually trigger the code path under test.

## 2026-06-20 — ai-steward: Refactor _build_entry to capture reasoning structure (lenses, predictions, blind spots) in improve-skill-style format to meet structural equivalence requirement from destination 2026-06-20.

**[!REVERSAL]** ** placeholder section for capturing prediction mismatches in future runs, and reorganize the entry so the blind_spot field is prominent as a named decision gate rather than a trailing afterthought.

## 2026-06-20 — ai-steward: Refactor _build_entry to capture reasoning structure (lenses, predictions, blind spots) in improve-skill-style format to meet structural equivalence requirement from destination 2026-06-20.

**[!REVERSAL]** ** Prediction Mismatch Gate:  \n"

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20.

**[!REALIZATION]** (arc-level):** The AI keeps proposing the same wrong fix to `record.py`. The destination says "improve-skill-style entries" without defining them. This creates an attractor loop: every self-targeting run reads the destination, concludes record.py needs restructuring, and produces a proposal with hardcoded `[!REVERSAL]` placeholders. Either define the format concretely or accept the current format as sufficient.

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20.

**[!REVERSAL]** ` marker stub for future VERIFY data binding, and formats the prediction/rationale structure to match the skill-suite pattern (lenses, predictions, decision marker, blind spot) rather than the current lightweight summary format.

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20.

**[!REVERSAL]** ` markers when VERIFY data becomes available in future runs; the current record.py has no mechanism to query prior session data or link reversals across cycles.

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20.

**[!REVERSAL]** ** *stub — VERIFY binding pending*\n"

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20.

**[!REVERSAL]** ` placeholder error)

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20.

**[!REVERSAL]** ` in the `_types.py` refactor (monkeypatch timing). Honest handling.

## 2026-06-20 — DRY extraction: run_tests to _utils.py

**[!REALIZATION]** ** `loop.py` has `_baseline_tests()` and `verify.py` has `_run_tests()` — identical implementations with different names. Naming difference masked semantic identity during prior sessions. This is exactly the kind of duplication the destination calls out: "DRY: Shared logic extracted."

## 2026-06-20 — Fix implement() return type annotation

**[!REALIZATION]** ** `implement()` has `-> tuple[bool, str, int]` annotation but actually returns `tuple[bool, str, int, int, int]`. The two token-count return values (`input_tokens`, `output_tokens`) were added during P2 token-tracking work without updating the annotation or docstring. Tests used `*_` star-unpacking so nothing broke at runtime, but a type checker flags this. Loop.py correctly unpacks all 5 values — the mismatch is purely in the signature.

## 2026-06-20 — Make codebase mypy-clean

**[!REALIZATION]** ** harness.py had the same missing TYPE_CHECKING/anthropic guard that scan.py and implement.py already have. cli.py accessed

## 2026-06-20 — Make codebase mypy-clean

**[!REALIZATION]** (macro -- recurring-class trigger FIRED):** Last three iterations were all annotation/type discipline fixes (DRY test-runner, wrong 3->5-tuple annotation, missing TYPE_CHECKING + null guard). All root-caused to the P2 token-tracking implementation pass landing quickly without a type-check gate. The code is now clean; the structural fix is adding mypy to CI so the next rapid implementation pass cannot leave the same gap silently.

## 2026-06-20 — Retrospect: post-CI-closure

**[!REALIZATION]** (arc-level):** Self-targeting has hit diminishing returns. Two consecutive sessions (P1/P2 closure + this CI session) found nothing functional to improve in ai-steward's own codebase. The loop is ready to prove generalisation by running against external repos.

## 2026-06-20 — Retrospect: post-CI-closure

**[!REVERSAL]** markers across the full session (one from _types.py refactor, one from implement-tuple test unpacking). Honest, within expected noise.

## 2026-06-20 — First external-repo run: vectorium (TypeScript) — VERIFY gap discovered

**[!REALIZATION]** VERIFY has no meaningful guards for non-Python repos.**

## 2026-06-20 — First external-repo run: vectorium (TypeScript) — VERIFY gap discovered

**[!REALIZATION]** SCAN and IMPLEMENT have different failure modes on large files.**

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern.

**[!REVERSAL]** markers when VERIFY data contradicts predictions.

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern.

**[!REVERSAL]** placeholder section for future verification data—transforming the trail entry from outcome-focused to reasoning-focused per the 2026-06-20 decision on structural equivalence.

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern.

**[!REVERSAL]** markers when VERIFY data contradicts predictions.

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern.

**[!REVERSAL]** ** *(Reserved for VERIFY phase)*  \n"

## 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern.

**[!REVERSAL]** placeholder is explicitly prohibited by operational rules — it marks actual reversals, never reserved sections; (2) removes trailing newline at EOF (regression). The refactoring itself is cosmetic with no leverage. This is the attractor loop documented in retrospect.md firing and the operator gate holding. Evidence that the review-then-commit workflow functions correctly.

## 2026-06-20 — fix-scan-false-positive-already-exists-check

**[!REALIZATION]** : not fired.

## 2026-06-20 — feat-ai-steward-init-command

**[!REALIZATION]** : not fired.

## 2026-06-20 — feat-configurable-verify-command

**[!REALIZATION]** :* not fired.

## 2026-06-20 — feat-configurable-verify-command

**[!REALIZATION]** :* not fired.

## 2026-06-20 — feat-configurable-verify-command

**[!REVERSAL]** ** First run: 2 pre-existing tests failed. `**/*` collected `.trail/destination.md` as a file, causing its raw content to appear twice in the SCAN prompt (once from `_load_destination()`, once from `_collect_files()`). Fix: add `_DEFAULT_SKIP_DIRS` to exclude `.trail/` and other system dirs when using the default scope. Fixed in same iteration.

## 2026-06-20 — feat-configurable-verify-command

**[!REVERSAL]** fired again — test relying on directory isolation broke when scope was widened. Class: "test isolation assumptions break when collection scope widens." Documented. Mitigated by `_DEFAULT_SKIP_DIRS`.

## 2026-06-21 — scan-reasoning-quality + V1-milestone-confirmed

**[!REALIZATION]** The first run under the improved prompt returning NOTHING FOUND is not a failure — it is a quality gate working. The previous run with the flat prompt produced a speculative off-mandate proposal in seconds. The new prompt produced genuine mandate-aligned examination followed by an honest rejection. The quality bar is structurally higher now.

## 2026-06-21 — scan-reasoning-quality + V1-milestone-confirmed

**[!REALIZATION]** The skills (GitHub Copilot, trail) and ai-steward both write to the same .acm/audit-trail.md. This is the shared evidence layer: human-supervised sessions write trail-skill-format entries; the autonomous pipeline writes RECORD-phase-format entries. Both are governed by the same destination.md and both read from the same .acm/ context. Unified governance, two classes of author.

## 2026-06-21 — scan-reasoning-quality + V1-milestone-confirmed

**[!REALIZATION]** contradicted: No.

## 2026-06-21 — scan-reasoning-quality + V1-milestone-confirmed

**[!REALIZATION]** The first run under the improved prompt returning NOTHING FOUND is not a failure — it is a quality gate working. The previous flat prompt produced a speculative off-mandate proposal instantly. The new prompt produced genuine mandate-aligned examination followed by an honest rejection.

## 2026-06-21 — scan-reasoning-quality + V1-milestone-confirmed

**[!REALIZATION]** The skills (GitHub Copilot, trail skill) and ai-steward both write to the same `.acm/audit-trail.md`. This is the shared evidence layer: human-supervised sessions write trail-skill-format entries; the autonomous pipeline writes RECORD-phase-format entries. Both are governed by the same `destination.md` and both read from the same `.acm/` context. Unified governance, two classes of author.

## 2026-06-21 — scan-reasoning-quality + V1-milestone-confirmed

**[!REALIZATION]** contradicted: No.

## 2026-06-21 — Retrospect: post-v1-milestone-config-surface

**[!REALIZATION]** SCAN has received exclusive autonomous attention. RECORD has received zero. These phases are equally critical — SCAN generates the proposal, RECORD closes the feedback loop. The asymmetry means every cycle currently produces a trail entry that does not meet the trail skill standard. This is the loop's structural blind spot.

## 2026-06-21 — Retrospect: post-v1-milestone-config-surface

**[!REALIZATION]** "Convergence Is Silence" is named in every destination section but has never been demonstrated. A principle stated but untested is an aspiration, not a claim. The convergence test is the session that turns this into evidence.

## 2026-06-21 — feat: capture prediction field from SCAN JSON into Finding and trail entry

**[!REALIZATION]** :* not fired — the realization that RECORD is the largest gap is confirmed, not contradicted.

## 2026-06-21 — Retrospect: post-prediction-field

**[!REALIZATION]** The improve–retrospect cycle is producing compounding orientation: each retrospect updates the arc-claims from the prior one, creating a narrowing funnel. After two iterations, the next move is unambiguous: ORIENT (retrospect.md + learning.md into SCAN context). Every other candidate depends on it or is lower-leverage. The loop is converging on a decision, not thrashing.

## 2026-06-21 — Retrospect: post-prediction-field

**[!REALIZATION]** The two structural errors remaining in RECORD (_Expected outcome_ and the missing Reflection/trigger/CNM) are not equivalent in effort or value. The Expected outcome fix is 2-line, zero-risk. The Reflection/trigger/CNM fix requires a second LLM call and significant record.py refactoring. They should be sequenced, not bundled.

## 2026-06-21 — Retrospect: pre-orient-implementation

**[!REALIZATION]** A retrospect without a preceding improve iteration is not waste — it is the operator-gate making a deliberate choice to hold. When the gate holds twice, the correct response from the retrospect is not to repeat the same claims but to sharpen the brief so the implement step is unambiguous when the gate opens. The retrospect’s value in this run was converting "ORIENT is the next move" (direction) into a precise implementation spec (actionable).

## 2026-06-21 — feat(orient): inject retrospect.md and learning.md into SCAN context

**[!REALIZATION]** /[!REVERSAL] markers) were invisible to the autonomous SCAN context. Every retrospect we wrote was adding value the pipeline could not consume.

## 2026-06-21 — feat(orient): inject retrospect.md and learning.md into SCAN context

**[!REALIZATION]** ` (plain text) but learning.md uses `**[!REALIZATION]**` (markdown bold). Fixed assertion before marking the test passing. [!REVERSAL] within-iteration.

## 2026-06-21 — feat(orient): inject retrospect.md and learning.md into SCAN context

**[!REALIZATION]** :* not fired — the claim that "retrospect.md is invisible to autonomous pipeline" is now resolved, consistent with prior arc.

## 2026-06-22 — fix(record): remove redundant Expected outcome line from trail entry

**[!REALIZATION]** :* not fired.

## 2026-06-22 — fix(record): remove redundant Expected outcome line from trail entry

**[!REALIZATION]** The recurring-class trigger fired: three consecutive RECORD format fixes (prediction field, ORIENT context, Expected outcome). The pattern suggests `_build_entry()` was written as a rough first draft and is being incrementally corrected toward the trail skill standard. The remaining gap (Lenses boilerplate) follows the same pattern. One more iteration would complete the structural alignment. After that, the Reflection call (second LLM call) is a different category of work.

## 2026-06-22 — feat(record): replace hardcoded lenses with examination_summary from SCAN Step 2

**[!REALIZATION]** one more iteration completes the structural alignment." Top candidate: extract lenses from SCAN model output. This is entry 42.

## 2026-06-22 — feat(record): replace hardcoded lenses with examination_summary from SCAN Step 2

**[!REALIZATION]** from entry 41 said this iteration was the last one in this class. That prediction is now testable: the next improve iteration should NOT be a `_build_entry()` fix.

## 2026-06-22 — feat(record): replace hardcoded lenses with examination_summary from SCAN Step 2

**[!REALIZATION]** :* not fired.

## 2026-06-22 — feat(record): replace hardcoded lenses with examination_summary from SCAN Step 2

**[!REALIZATION]** `_build_entry()` is now structurally aligned with the trail skill standard for all fields derivable from a single SCAN + IMPLEMENT cycle. The structural boundary is now clear: Prediction, Lenses, Blind spot come from the SCAN model’s JSON. Reflection, trigger evaluation, and Candidate Next Moves require a second reasoning pass after VERIFY. These are architecturally distinct — the first set is free (the model produces them as part of its reasoning); the second set costs an additional LLM call.

## 2026-06-22 — live-validation: first self-targeting run with all field fixes

**[!REALIZATION]** The first run’s NOTHING FOUND was caused by max_tokens=1024 being too small for the 5-step reasoning protocol. The model was correct, on-mandate, and reasoning well — it was the pipeline’s own token budget that cut it off. This is a structural failure mode: the reasoning quality upgrade (5-step protocol) was not accompanied by a corresponding token budget upgrade. V1 test suite passed but the live run exposed the gap. Live runs are the gate that unit tests cannot replace.

## 2026-06-22 — live-validation: first self-targeting run with all field fixes

**[!REALIZATION]** The second run validates all four field fixes simultaneously. The trail entry is structurally correct: Prediction is a genuine falsifiable statement from Step 4, Lenses applied shows actual file examination findings from Step 2, Blind spot names a specific area with a reason. The trail entry is now indistinguishable in quality from a human-supervised trail skill entry for these fields.

## 2026-06-22 — live-validation: first self-targeting run with all field fixes

**[!REALIZATION]** The IMPLEMENT phase strips trailing newlines when it regenerates files. This is a recurring artifact that should be handled: either IMPLEMENT’s prompt should explicitly say "preserve the trailing newline," or RECORD should append a newline if the file doesn’t end with one. Currently it requires operator intervention.

## 2026-06-22 — live-validation: first self-targeting run with all field fixes

**[!REALIZATION]** markers, ORIENT done, field alignment complete, live validation run. Arc-read is warranted.

## 2026-06-22 — fix(implement): ensure trailing newline after model rewrites file

**[!REALIZATION]** :* not fired.

## 2026-06-22 — fix(record): model-keyed pricing table for accurate cycle cost estimates

**[!REALIZATION]** :* not fired.

## 2026-06-22 — fix(record): model-keyed pricing table for accurate cycle cost estimates

**[!REALIZATION]** `record.py` field-level correctness is now complete for the single-cycle case. The gap between the current trail entries and the trail skill standard is no longer in the fields — it’s in the absence of Reflection (which requires a second LLM call) and the absence of Candidate Next Moves in autonomous entries (which requires the pipeline to know what to suggest next). These are architectural additions, not field additions. The taxonomy of remaining work has shifted.

## 2026-06-22 — fix(record): model-keyed pricing table for accurate cycle cost estimates

**[!REALIZATION]** markers. Arc-read will sharpen the next architectural decision (Reflection).

## 2026-06-22 — feat(reflect): add REFLECT phase — third LLM call producing Reflection section in trail entries

**[!REALIZATION]** :* not fired — the realization that "Reflection/triggers/CNM require architectural additions" is confirmed by this entry, not contradicted. This entry is the first of those architectural additions.

## 2026-06-22 — feat(reflect): add REFLECT phase — third LLM call producing Reflection section in trail entries

**[!REALIZATION]** The pipeline has structural parity with human-supervised trail entries for all single-cycle fields. Silence on autonomous trail entry structural parity for the single-cycle case. Bars not tested: multi-cycle compounding behavior, Candidate Next Moves from autonomous entries (requires the pipeline to know what to suggest next — distinct from Reflection), across-trail trigger evaluation in autonomous entries.

## 2026-06-22 — feat(reflect): add REFLECT phase — third LLM call producing Reflection section in trail entries

**[!REVERSAL]** Prediction said "~86 tests." Actual: 88 (+7, not +5). Under-counted: 5 in test_reflect.py + 1 in test_loop.py + 2 in test_record.py = 8 new; 88 total not 86. All green; the count was wrong, the correctness was not.

## 2026-06-22 — live-validation: REFLECT phase first live run

**[!REALIZATION]** The REFLECT phase produced a genuinely structured reflection on its first live run: prediction accuracy assessed, falsifiable model-claim stated, specific blind spot named. The autonomous trail entry is now indistinguishable in structure from a human-supervised trail entry across all sections: [!DECISION], Prediction, Lenses (examination_summary), Blind spot, Reflection, File, Tokens, Harness session, Diff.

## 2026-06-22 — live-validation: REFLECT phase first live run

**[!REALIZATION]** The model proposed `max_tokens_reflect` (a config field) but the staged diff only touched `config.py` — it did not wire the new field into `reflect.py`. This is structurally correct pipeline behavior: one change per cycle. The operator's gate is the natural place to complete the wiring atomically. Accepted with reflect.py wired in the same commit. This is the intended workflow.

## 2026-06-22 — live-validation: REFLECT phase first live run

**[!REALIZATION]** The blind spot the model named (cli.py `_CONFIG_TEMPLATE` not updated) is the correct next proposal. The model correctly identified it but deferred it as out of scope for this cycle. If the next self-targeting run produces a proposal to update the template, the mandate gate is working as designed.

## 2026-06-22 — fix(harness): complete session coverage — all pipeline LLM calls captured

**[!REALIZATION]** The harness Observable Autonomy guarantee in ai-steward was structurally incomplete: two of three LLM calls per pipeline run (SCAN and REFLECT) were producing unlinked session files. This is fixed on the ai-steward side. The remaining gap is the proxy side — one session file per run (true grouping) requires the proxy to implement `X-Harness-Session`. Until then, trails will list three separate file paths, which is complete evidence, just not grouped in a single JSONL.

## 2026-06-22 — fix(harness): complete session coverage — all pipeline LLM calls captured

**[!REALIZATION]** :* not fired — no prior realization contradicted; the REFLECT harness attribution gap was named as open in the last retrospect (claim 3: "Reflection now also complete. Remaining: multi-cycle convergence, REFLECT harness attribution, external repo testing.").

## 2026-06-22 — fix(cli): CONFIG_TEMPLATE exposes full operator-tunable surface

**[!REALIZATION]** The template test (`test_init_config_includes_full_tuning_surface`) is itself a governance mechanism — it enforces the invariant that operator-tunable fields are discoverable. The field list in the test should be updated whenever `AiStewardConfig` gains a new user-facing field. Without this test, the drift recurred silently three times (max_tokens_scan, max_tokens_implement, max_tokens_reflect).

## 2026-06-22 — fix(cli): CONFIG_TEMPLATE exposes full operator-tunable surface

**[!REALIZATION]** :* not fired — no prior realization argued against template completeness.

## 2026-06-22 — fix(scan): orient context delivers operational rules

**[!REALIZATION]** The 1000-char orient window was a silent governance failure. Every autonomous SCAN call since ORIENT was implemented (entry 35) operated without operational constraints. The constraints were written in retrospect.md, the operational rules section was added with care, and none of it reached the model. The trail entries were recording "ORIENT active" while the ORIENT context was delivering less than 12% of the file. This is the class of failure where the documentation says the feature works, the tests say the feature works, and the feature doesn't work.

## 2026-06-22 — fix(scan): orient context delivers operational rules

**[!REALIZATION]** :* FIRED — prior realizations stated "ORIENT is implemented" and "the autonomous pipeline now reads from the same evidence layer as human-supervised sessions." Both are demonstrably false for the operational rules section. This is a [!REVERSAL] of claims made in retrospect.md entry 4.

## 2026-06-22 — fix(scan): orient context delivers operational rules

**[!REALIZATION]** (arc-level): The pattern across the last three improvements is a single root cause: **the system lacks contract tests that verify inputs reach their consumers.** Session files weren't linked — no test verified all sessions were captured. Config fields weren't in the template — no test verified all fields appeared. Operational rules weren't in SCAN context — no test verified the context contained the rules. Each fix added a contract test. The next retrospect should evaluate whether this pattern persists elsewhere.

## 2026-06-22 — fix(scan): orient context delivers operational rules

**[!REALIZATION]** and one [!REVERSAL] this session warrant a full retrospect before the next improve cycle. Retrospect.md is stale relative to entries 74–78.

## 2026-06-22 — fix(scan): orient context delivers operational rules

**[!REVERSAL]** Retrospect.md claim #4 ("ORIENT is implemented; the autonomous pipeline now reads from the same evidence layer as human-supervised sessions") is demonstrably false for the operational rules section. It was false from the moment ORIENT was implemented. The claim should be updated in the next retrospect run.

## 2026-06-22 — Retrospect: post-governance-layer-completion

**[!REALIZATION]** The loop has been building the instrument rather than using it. 17 iterations building governance primitives is appropriate for V1 — the governance layer had to be trustworthy before it could be trusted to operate autonomously. It is now trustworthy. Continued single-cycle self-targeting sessions have near-zero expected value. The next session should be a multi-cycle run.

## 2026-06-22 — Retrospect: post-governance-layer-completion

**[!REALIZATION]** The govern-layer-only focus has created a gap: the "useful and widely adoptable" destination purpose is untested. ai-steward has been run on external repos twice (vectorium, twice) and on itself ~40 times. The proof purpose is closer to validated than the tool purpose.

## 2026-06-22 — Retrospect: post-governance-layer-completion

**[!REALIZATION]** The retrospect has been an accurate steering mechanism. Each retrospect (entries 7, 25, 36, 38, 39, 44-era) correctly identified the next structural gap before the loop found it. However, the retrospect itself contained a false claim (claim 4) for 12 iterations. The mechanism works; the claims can still be wrong. Arc-level claims require the same falsifiability discipline as any other.

## 2026-06-22 — Retrospect: post-governance-layer-completion

**[!REVERSAL]** Prior claim 4 ("ORIENT is implemented; autonomous pipeline reads from same evidence layer as human sessions") was false from entry 40. Corrected: ORIENT context now delivers both arc-claims and rules, via entry 52's header extraction. Contract-tested.

## 2026-06-22 — fix(record): model ID prefix matching in _model_cost_per_token

**[!REALIZATION]** :* not fired — the realization "delivery contract tests are the missing governance mechanism" is confirmed, not contradicted.

## 2026-06-22 — feat(cli): scope section added to CONFIG_TEMPLATE

**[!REALIZATION]** :* not fired — no prior realization argued against scope discoverability.

## 2026-06-22 — feat(cli): scope section added to CONFIG_TEMPLATE

**[!REALIZATION]** (macro — recurring-class trigger fired): The CONFIG_TEMPLATE gap pattern (entries 51, 80, 81) has now been exhausted. All known operator-tunable fields are in the template and the assertion test enforces them. The test `test_init_config_includes_full_tuning_surface` is the governance mechanism preventing silent recurrence. This class of finding is closed.

## 2026-06-22 — fix(reflect): wire REFLECT token cost into Finding and cycle cost estimate

**[!REALIZATION]** :* FIRED — prior realization "record.py field-level correctness is now complete for the single-cycle case" (entry 46) was false — REFLECT cost was missing. This is a [!REVERSAL] of that claim.

## 2026-06-22 — fix(reflect): wire REFLECT token cost into Finding and cycle cost estimate

**[!REVERSAL]** Entry 46's realization "record.py field-level correctness is now complete for the single-cycle case" was false. REFLECT was added in entry 47 without wiring its cost into record.py. The field-level correctness claim is now accurate: all three LLM phases are tracked.

## 2026-06-22 — ai-steward: Add lenses configuration field to AiStewardConfig

**[!REVERSAL]** Operator rejected — 2026-06-22:** Dead config (YAGNI). The pipeline predicted the field would be inert yet proposed it as structural prep. A config field that does nothing is waste, not preparation. Unstaged and discarded. Next cycle must find a change that alters behaviour.

## 2026-06-22 — ai-steward: Add configurable lenses field to AiStewardConfig with default ['mandate', 'examination']

**[!REVERSAL]** Operator correction — 2026-06-22:** Cycle-1 YAGNI rejection was wrong. destination.md explicitly mandates lenses be operator-configurable and not hardcoded. SCAN was correctly reading the mandate both cycles. The partial-implementation pattern (config field now, scan.py wiring next cycle) is the correct iterative approach. Cycle-2 proposal accepted and committed as `31f4015`. Cycle-3 should wire the lenses field into scan.py prompt construction.

## 2026-06-22 — ai-steward: Add docstring to AiStewardConfig.lenses explaining purpose, defaults, and operator use cases

**[!REVERSAL]** Operator rejected — 2026-06-22:** Dead-field documentation. lenses field is still not consumed by scan.py. Documenting intended-but-not-implemented behavior is misleading, not progress. Pending substantive work: (1) wire lenses into scan.py, (2) wire acm_scope_depth+destination_budget_chars into scan.py, (3) add acm_scope_depth+destination_budget_chars to CONFIG_TEMPLATE. Next cycle must choose one of these or declare silence.

## 2026-06-22 — dead-config-wire-scope-context

**[!REALIZATION]** : not fired -- wiring dead config is consistent with all

## 2026-06-22 — dead-config-wire-scope-context

**[!REALIZATION]** :** The 8-cycle autonomous loop plus the manual improve runs

## 2026-06-22 — test-scope-context-parameter-variation

**[!REALIZATION]** : not fired -- consistent with all prior realizations.

## 2026-06-22 — wire-binary-heuristic-and-skip-dirs

**[!REALIZATION]** : not fired.

## 2026-06-22 — wire-binary-heuristic-and-skip-dirs

**[!REALIZATION]** :** The config surface completion arc spans entries

## 2026-06-22 — wire-lenses-into-scan-system-prompt

**[!REALIZATION]** : FIRED -- prior realization "lenses field is dead config"

## 2026-06-22 — wire-lenses-into-scan-system-prompt

**[!REVERSAL]** of that state.

## 2026-06-22 — wire-lenses-into-scan-system-prompt

**[!REVERSAL]** ** The lenses config field is no longer dead config. Custom lenses now produce

## 2026-06-22 — wire-reflect-lenses-into-reflect-system-prompt

**[!REALIZATION]** below.

## 2026-06-22 — wire-reflect-lenses-into-reflect-system-prompt

**[!REALIZATION]** : FIRED -- prior realization "lenses field is dead config"

## 2026-06-22 — wire-reflect-lenses-into-reflect-system-prompt

**[!REALIZATION]** ** All operator-configurable fields are now live: lenses, reflect_lenses,

## 2026-06-22 — field-validator-for-unknown-lens-names

**[!REALIZATION]** : not fired.

## 2026-06-22 — destination-cost-model-correction

**[!REALIZATION]** : not fired.

## 2026-06-22 — destination-cost-model-correction

**[!REALIZATION]** ** The improve loop for ai-steward's V1 code is structurally converging.

## 2026-06-22 — evo-code-quality-patterns

**[!REALIZATION]** : not fired — checked learning.md, no contradiction.

## 2026-06-22 — evo-code-quality-patterns

**[!REALIZATION]** ** The evo comparison revealed a structural asymmetry: evo was

## 2026-06-22 — evo-code-quality-patterns

**[!REVERSAL]** : test_implement.py was raising RuntimeError as the mock exception.

---

**161 markers — 122 realisations, 39 reversals**
