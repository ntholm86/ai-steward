# History

Auto-generated from `.acm/audit-trail.md` by the `record.py history --write` command in the autonomous-agent-skills install.
Do not edit by hand — re-run the command to refresh.

| # | Date | Slug | Outcome | Delta |
|---|------|------|---------|-------|
| ▸ 1 | 2026-06-20 | ai-steward: Add explicit git installation check in preflight before attempting git commands to provide clearer error messaging when git is unavailable. | .acm-root marker support added; 2 new tests. |  |
| ▸ 2 | 2026-06-21 | scan-reasoning-quality + V1-milestone-confirmed | SCAN reasoning raised to trail-skill standard; V1 self-targeting milestone confirmed | _SYSTEM_PROMPT rewritten — "JSON only, no prose" → 5-step reasoning protocol |
| ▸ 3 | 2026-06-21 | scan-reasoning-quality + V1-milestone-confirmed | SCAN reasoning raised to trail-skill standard; V1 self-targeting milestone confirmed | _SYSTEM_PROMPT rewritten — "JSON only, no prose" → 5-step reasoning protocol |
| ▸ 4 | 2026-06-21 | feat: capture prediction field from SCAN JSON into Finding and trail entry |  |  |
| ▸ 5 | 2026-06-21 | feat(orient): inject retrospect.md and learning.md into SCAN context |  |  |
| ▸ 6 | 2026-06-22 | fix(record): remove redundant Expected outcome line from trail entry |  |  |
| ▸ 7 | 2026-06-22 | feat(record): replace hardcoded lenses with examination_summary from SCAN Step 2 |  |  |
| ▸ 8 | 2026-06-22 | fix(implement): ensure trailing newline after model rewrites file |  |  |
| ▸ 9 | 2026-06-22 | fix(record): model-keyed pricing table for accurate cycle cost estimates |  |  |
| ▸ 10 | 2026-06-22 | feat(reflect): add REFLECT phase — third LLM call producing Reflection section in trail entries |  |  |
| ▸ 11 | 2026-06-22 | fix(harness): complete session coverage — all pipeline LLM calls captured | REFLECT moved inside harness context; session_paths list replaces single session_path; X-Harness-Session + HARNESS_SESSION_ID added for future proxy grouping | 88 tests → 92 tests; 6 files changed (+153/−67); mypy clean |
| ▸ 12 | 2026-06-22 | fix(cli): CONFIG_TEMPLATE exposes full operator-tunable surface | `ai-steward init` now produces a config that exposes all tunable parameters | _CONFIG_TEMPLATE +10 lines; 1 new test; 94 → 95 tests |
| ▸ 13 | 2026-06-22 | fix(scan): orient context delivers operational rules | SCAN now receives operational rules in every call; head budget raised 1000→2000 chars | scan.py _load_orient_context rewritten (+20 lines); 2 new tests; 95→97 |
| ▸ 14 | 2026-06-22 | fix(record): model ID prefix matching in _model_cost_per_token | date-versioned model IDs resolve to correct pricing; claude-sonnet-4-6 added to table; 4 contract tests added | record.py +11 lines; test_record.py +37 lines; 97→101 tests |
| ▸ 15 | 2026-06-22 | feat(cli): scope section added to CONFIG_TEMPLATE | `ai-steward init` now generates a config with a `scope:` section; operators discover file-targeting on first use | cli.py +9 lines; test assertion widened by 1 field; 101→101 tests (count unchanged; assertion tightened) |
| ▸ 16 | 2026-06-22 | fix(reflect): wire REFLECT token cost into Finding and cycle cost estimate | REFLECT token cost now tracked, reported in trail entries, and included in cycle cost estimate | 6 files changed; +2 fields to Finding; reflect() now returns tuple[str, int, int]; 101→102 tests |
| ▸ 17 | 2026-06-22 | extract-json-fence-overlap-fix | BUG FOUND AND FIXED — _extract_json false-negative on back-to-back code fences |  |
| ▸ 18 | 2026-06-22 | dead-config-wire-scope-context | CHANGE ACCEPTED — acm_scope_depth and destination_budget_chars wired into _load_scope_context |  |
| ▸ 19 | 2026-06-22 | test-scope-context-parameter-variation | CHANGE ACCEPTED — two tests added covering scope_depth and budget_chars parameter variation |  |
| ▸ 20 | 2026-06-22 | wire-binary-heuristic-and-skip-dirs | CHANGE ACCEPTED — binary_heuristic_bytes and default_skip_dirs wired from config |  |
| ▸ 21 | 2026-06-22 | wire-lenses-into-scan-system-prompt | CHANGE ACCEPTED — lenses config field now live; _build_system_prompt wires custom lenses into SCAN |  |
| ▸ 22 | 2026-06-22 | wire-reflect-lenses-into-reflect-system-prompt | CHANGE ACCEPTED — reflect_lenses config field now live; _build_reflect_system_prompt wires custom lenses into REFLECT |  |
| ▸ 23 | 2026-06-22 | field-validator-for-unknown-lens-names | CHANGE ACCEPTED — unknown lens names now trigger UserWarning at config load time |  |
| ▸ 24 | 2026-06-22 | destination-cost-model-correction | CHANGE ACCEPTED — destination.md cost model corrected; retrospect claim #6 falsified |  |
| ▸ 25 | 2026-06-22 | evo-code-quality-patterns | CHANGE ACCEPTED — 3 code quality patterns from evo applied |  |
| ▸ 26 | 2026-06-22 | feat(reorient): add REORIENT phase for arc-level awareness | CHANGE ACCEPTED -- 177 tests pass |  |

### Run 1 — 2026-06-20 — ai-steward: Add explicit git installation check in preflight before attempting git commands to provide clearer error messaging when git is unavailable.

- **decided:** ** Proposed: Add explicit git installation check in preflight before attempting git commands to provide clearer error messaging when git is unavailable.

### Run 2 — 2026-06-21 — scan-reasoning-quality + V1-milestone-confirmed

- **decided:** with rejected alternatives → Prediction → Blind spot before any conclusion. SCAN should enforce the same discipline, explicitly trading token budget for proposal quality.
- **decided:** with at least one rejected alternative, Prediction, Blind spot. None of these were present in the SCAN prompt.
- **decided:** Replace flat "JSON only" prompt with a 5-step reasoning protocol mirroring the trail skill standard:
- **decided:** : choice + rationale + at least one rejected alternative
- **decided:** with rejected alternative (workspace config file — rejected as unnecessary complexity for V1)

### Run 3 — 2026-06-21 — scan-reasoning-quality + V1-milestone-confirmed

- **decided:** with rejected alternatives → Prediction → Blind spot before any conclusion. SCAN should enforce the same discipline, explicitly trading token budget for proposal quality.
- **decided:** with at least one rejected alternative, Prediction, Blind spot. None of these were present in the SCAN prompt.
- **decided:** Replace flat "JSON only" prompt with a 5-step reasoning protocol mirroring the trail skill standard:
- **decided:** : choice + rationale + at least one rejected alternative
- **decided:** with rejected alternative (workspace config file — rejected as unnecessary complexity for V1)

### Run 4 — 2026-06-21 — feat: capture prediction field from SCAN JSON into Finding and trail entry

- **decided:** Add `prediction` as a required JSON field in the SCAN prompt schema, add `prediction: str = ""` to the `Finding` dataclass, extract it in `scan()`, and use `finding.prediction` in `_build_entry()` with `finding.proposed_change` as fallback.

### Run 5 — 2026-06-21 — feat(orient): inject retrospect.md and learning.md into SCAN context

- **decided:** Add `_load_orient_context()` helper that reads retrospect.md (first 1000 chars) and learning.md (last 500 chars) from repo `.acm/`, then restructure `scan()` to assemble user_content as a `parts` list joined by `---` separators.

### Run 6 — 2026-06-22 — fix(record): remove redundant Expected outcome line from trail entry

- **decided:** Remove `f"*Expected outcome:* {finding.rationale}\n\n"` from `_build_entry()`. The Prediction field now carries a clean, single falsifiable statement.

### Run 7 — 2026-06-22 — feat(record): replace hardcoded lenses with examination_summary from SCAN Step 2

- **decided:** Add `examination_summary: str = ""` to `Finding`, `"examination_summary"` to SCAN JSON schema, extract in `scan()`, and replace the two hardcoded lines in `_build_entry()` with the model’s value (fallback to generic lines if empty).
- **decided:** (description + rationale + risk), Prediction (Step 4 falsifiable statement), Lenses (Step 2 examination summary), Blind spot (Step 5). The remaining gap is fundamentally different: Reflection (a second LLM call after VERIFY), across-trail trigger evaluation, and Candidate Next Moves. These require architecture changes to the pipeline, not field additions.

### Run 8 — 2026-06-22 — fix(implement): ensure trailing newline after model rewrites file

- **decided:** Add `if not new_content.endswith("\n"): new_content += "\n"` immediately before `target.write_text()`, after the empty-content guard. Applies unconditionally to both the fenced and unfenced paths.

### Run 9 — 2026-06-22 — fix(record): model-keyed pricing table for accurate cycle cost estimates

- **decided:** Replace two module-level constants with `_MODEL_PRICING` dict (haiku, sonnet, opus), a `_model_cost_per_token(model)` lookup, and `_estimate_cycle_cost(config, finding)` helper. Calculate in `record()` and pass `cycle_cost_usd` into `_build_entry()`.
- **decided:** , Prediction, Lenses, Blind spot, Token counts, and Cycle cost. The remaining architectural gap is Reflection (second LLM call), across-trail triggers, and Candidate Next Moves. These are not field additions; they require a second LLM call after VERIFY and architectural changes to the loop.

### Run 10 — 2026-06-22 — feat(reflect): add REFLECT phase — third LLM call producing Reflection section in trail entries

- **decided:** Add `pipeline/reflect.py` — a new phase that makes one LLM call (max 400 tokens) after VERIFY passes. The prompt provides prediction + diff + verify result; the model returns 2-3 paragraph prose (prediction accuracy, falsifiable model-claim, specific blind spot). Add `reflection: str = ""` to `Finding`. Call `reflect()` from `loop.py` after `verify()` passes. Output `**Reflection:**` in `_build_entry()` when non-empty (omit section when empty — graceful degradation if model call fails).
- **decided:** , Prediction, Lenses (examination_summary), Blind spot (from SCAN Step 5), Reflection (from REFLECT LLM call), Token counts, Cycle cost, Harness session. The pipeline is architecturally complete for V1's trail quality requirement.
- **REVERSAL:** Prediction said "~86 tests." Actual: 88 (+7, not +5). Under-counted: 5 in test_reflect.py + 1 in test_loop.py + 2 in test_record.py = 8 new; 88 total not 86. All green; the count was wrong, the correctness was not.

### Run 11 — 2026-06-22 — fix(harness): complete session coverage — all pipeline LLM calls captured

- **decided:** **Fix the Observable Autonomy gap in two layers:**

### Run 12 — 2026-06-22 — fix(cli): CONFIG_TEMPLATE exposes full operator-tunable surface

- **decided:** Backfill `_CONFIG_TEMPLATE` with the full operator-tunable surface: `max_tokens_scan`, `max_tokens_implement`, `max_tokens_reflect`, `max_iterations`, `budget_usd`, `allow_dirty`. Add inline comments explaining what each controls and why the default was chosen.

### Run 13 — 2026-06-22 — fix(scan): orient context delivers operational rules

- **decided:** Fix in two parts:
- **REVERSAL:** Retrospect.md claim #4 ("ORIENT is implemented; the autonomous pipeline now reads from the same evidence layer as human-supervised sessions") is demonstrably false for the operational rules section. It was false from the moment ORIENT was implemented. The claim should be updated in the next retrospect run.

### Run 14 — 2026-06-22 — fix(record): model ID prefix matching in _model_cost_per_token

- **decided:** Fix with prefix matching: `model == key or model.startswith(key + "-")`. Add `claude-sonnet-4-6` to the table (distinct model, not a date variant of 4-5). Add 4 contract tests.

### Run 15 — 2026-06-22 — feat(cli): scope section added to CONFIG_TEMPLATE

- **decided:** Add `scope:` section to `_CONFIG_TEMPLATE` with `allowed` and `blocked` example patterns and explanatory comments. Extend test assertion to include `scope` as a required field.

### Run 16 — 2026-06-22 — fix(reflect): wire REFLECT token cost into Finding and cycle cost estimate

- **decided:** Add `reflect_input_tokens: int = 0` and `reflect_output_tokens: int = 0` to `Finding`. Change `reflect()` return type to `tuple[str, int, int]`. Capture usage in reflect.py (same try/except pattern as implement.py). Update loop.py to unpack. Update `_estimate_cycle_cost()` and the trail tokens line.
- **REVERSAL:** Entry 46's realization "record.py field-level correctness is now complete for the single-cycle case" was false. REFLECT was added in entry 47 without wiring its cost into record.py. The field-level correctness claim is now accurate: all three LLM phases are tracked.

### Run 18 — 2026-06-22 — dead-config-wire-scope-context

- **decided:** ** Wire acm_scope_depth and destination_budget_chars into _load_scope_context.

### Run 19 — 2026-06-22 — test-scope-context-parameter-variation

- **decided:** ** Add two tests calling _load_scope_context directly:

### Run 20 — 2026-06-22 — wire-binary-heuristic-and-skip-dirs

- **decided:** ** Add binary_heuristic_bytes: int = 8192 and default_skip_dirs: list[str]

### Run 21 — 2026-06-22 — wire-lenses-into-scan-system-prompt

- **decided:** ** Additive injection: keep _BASE_SYSTEM_PROMPT as the unchanged base (Steps 1-5).
- **REVERSAL:** of that state.
- **REVERSAL:** ** The lenses config field is no longer dead config. Custom lenses now produce

### Run 22 — 2026-06-22 — wire-reflect-lenses-into-reflect-system-prompt

- **decided:** ** Mirror the scan.py lenses architecture in reflect.py:

### Run 23 — 2026-06-22 — field-validator-for-unknown-lens-names

- **decided:** ** Add _KNOWN_SCAN_LENSES and _KNOWN_REFLECT_LENSES frozensets to config.py

### Run 24 — 2026-06-22 — destination-cost-model-correction

- **decided:** ** Append a new dated section to destination.md with the validated cost

### Run 25 — 2026-06-22 — evo-code-quality-patterns

- **decided:** Iteration 1 — Logging infrastructure (highest leverage)**
- **decided:** Iteration 2 — Narrow exception types**
- **decided:** Iteration 3 — from __future__ annotations**
- **REVERSAL:** : test_implement.py was raising RuntimeError as the mock exception.

### Run 26 — 2026-06-22 — feat(reorient): add REORIENT phase for arc-level awareness

- **decided:** Add REORIENT phase — the robot's equivalent of the Retrospect skill.

**26 runs total — 26 with changes, 0 silence**
