# History

Auto-generated from `.acm/audit-trail.md` by the `record.py history --write` command in the autonomous-agent-skills install.
Do not edit by hand — re-run the command to refresh.

| # | Date | Slug | Outcome | Delta |
|---|------|------|---------|-------|
| ▸ 1 | 2026-05-14 | Evo analysis and new project decision |  |  |
| ▸ 2 | 2026-05-14 | Naming decision |  |  |
| ▸ 3 | 2026-05-14 | Repo initialization and first vision |  |  |
| ▸ 4 | 2026-05-14 | Vision run: understanding operator intent |  |  |
| ▸ 5 | 2026-05-14 | Architectural clarification: harness-protocol role and dual-use trail |  |  |
| ▸ 6 | 2026-05-14 | Vision cleanup |  |  |
| ▸ 7 | 2026-05-15 | First retrospect run; launch orientation before first code sprint |  |  |
| ▸ 8 | 2026-05-15 | Evo architecture analysis; runtime decision; first scaffold |  |  |
| ▸ 9 | 2026-05-28 | vision-to-destination-rename | artifact `.trail/vision.md` renamed to `.trail/destination.md` to match the renamed Destination skill (was Vision; now at `destination/SKILL.md` v2.0.0 in the skills suite, commit e3d1577). H1 header updated to match; no other content in destination.md was modified — it remains operator-held. | artifact filename only; skill behaviour unchanged. |
| ▸ 10 | 2026-06-19 | Post-destination-refinement retrospect |  |  |
| ▸ 11 | 2026-06-19 | Improve: config.py docstring correction (V1 / V2 framing) |  |  |
| ▸ 12 | 2026-06-19 | Improve: V1 pipeline design |  |  |
| ▸ 13 | 2026-06-19 | Improve: harness.py — structural Observable Autonomy |  |  |
| ▸ 14 | 2026-06-19 | Improve: pipeline loop skeleton + PRE-FLIGHT gates |  |  |
| ▸ 15 | 2026-06-19 | Improve: VERIFY phase + rollback utility |  |  |
| ▸ 16 | 2026-06-19 | Improve: SCAN phase |  |  |
| ▸ 17 | 2026-06-20 | ai-steward: Add validation to reject findings with file paths containing directory traversal sequences. |  |  |
| ▸ 18 | 2026-06-20 | ai-steward: Refactor _build_entry to capture reasoning structure (lenses, predictions, blind spots) in improve-skill-style format to meet structural equivalence requirement from destination 2026-06-20. |  |  |
| ▸ 19 | 2026-06-20 | ai-steward: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20. |  |  |
| ▸ 20 | 2026-06-20 | DRY extraction: run_tests to _utils.py |  |  |
| ▸ 21 | 2026-06-20 | Fix implement() return type annotation |  |  |
| ▸ 22 | 2026-06-20 | Make codebase mypy-clean |  |  |
| ▸ 23 | 2026-06-20 | Add mypy to pyproject.toml |  |  |
| ▸ 24 | 2026-06-20 | Add GitHub Actions CI |  |  |
| ▸ 25 | 2026-06-20 | Retrospect: post-CI-closure |  |  |
| ▸ 26 | 2026-06-20 | First external-repo run: vectorium (TypeScript) — VERIFY gap discovered |  |  |
| ▸ 27 | 2026-06-20 | verify-deletion-guard |  |  |
| ▸ 28 | 2026-06-20 | ai-steward: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern. |  |  |
| ▸ 29 | 2026-06-20 | fix-scan-false-positive-already-exists-check |  |  |
| ▸ 30 | 2026-06-20 | feat-ai-steward-init-command |  |  |
| ▸ 31 | 2026-06-20 | feat-configurable-verify-command |  |  |
| ▸ 32 | 2026-06-20 | ai-steward: Add explicit git installation check in preflight before attempting git commands to provide clearer error messaging when git is unavailable. | .acm-root marker support added; 2 new tests. |  |
| ▸ 33 | 2026-06-21 | ai-steward: Add token budget constraint to SCAN prompt system message |  |  |
| ▸ 34 | 2026-06-21 | scan-reasoning-quality + V1-milestone-confirmed | SCAN reasoning raised to trail-skill standard; V1 self-targeting milestone confirmed | _SYSTEM_PROMPT rewritten — "JSON only, no prose" → 5-step reasoning protocol |
| ▸ 35 | 2026-06-21 | scan-reasoning-quality + V1-milestone-confirmed | SCAN reasoning raised to trail-skill standard; V1 self-targeting milestone confirmed | _SYSTEM_PROMPT rewritten — "JSON only, no prose" → 5-step reasoning protocol |
| ▸ 36 | 2026-06-21 | Retrospect: post-v1-milestone-config-surface |  |  |
| ▸ 37 | 2026-06-21 | feat: capture prediction field from SCAN JSON into Finding and trail entry |  |  |
| ▸ 38 | 2026-06-21 | Retrospect: post-prediction-field |  |  |
| ▸ 39 | 2026-06-21 | Retrospect: pre-orient-implementation |  |  |
| ▸ 40 | 2026-06-21 | feat(orient): inject retrospect.md and learning.md into SCAN context |  |  |
| ▸ 41 | 2026-06-22 | fix(record): remove redundant Expected outcome line from trail entry |  |  |
| ▸ 42 | 2026-06-22 | feat(record): replace hardcoded lenses with examination_summary from SCAN Step 2 |  |  |
| ▸ 43 | 2026-06-22 | ai-steward: Add verify_command to the config template to expose test runner control |  |  |
| ▸ 44 | 2026-06-22 | live-validation: first self-targeting run with all field fixes |  |  |
| ▸ 45 | 2026-06-22 | fix(implement): ensure trailing newline after model rewrites file |  |  |
| ▸ 46 | 2026-06-22 | fix(record): model-keyed pricing table for accurate cycle cost estimates |  |  |
| ▸ 47 | 2026-06-22 | feat(reflect): add REFLECT phase — third LLM call producing Reflection section in trail entries |  |  |
| ▸ 48 | 2026-06-22 | ai-steward: Add max_tokens_reflect config parameter for REFLECT phase |  |  |
| ▸ 49 | 2026-06-22 | live-validation: REFLECT phase first live run |  |  |
| ▸ 50 | 2026-06-22 | fix(harness): complete session coverage — all pipeline LLM calls captured | REFLECT moved inside harness context; session_paths list replaces single session_path; X-Harness-Session + HARNESS_SESSION_ID added for future proxy grouping | 88 tests → 92 tests; 6 files changed (+153/−67); mypy clean |
| ▸ 51 | 2026-06-22 | fix(cli): CONFIG_TEMPLATE exposes full operator-tunable surface | `ai-steward init` now produces a config that exposes all tunable parameters | _CONFIG_TEMPLATE +10 lines; 1 new test; 94 → 95 tests |
| ▸ 52 | 2026-06-22 | fix(scan): orient context delivers operational rules | SCAN now receives operational rules in every call; head budget raised 1000→2000 chars | scan.py _load_orient_context rewritten (+20 lines); 2 new tests; 95→97 |
| ▸ 53 | 2026-06-22 | Retrospect: post-governance-layer-completion |  |  |
| ▸ 54 | 2026-06-22 | fix(record): model ID prefix matching in _model_cost_per_token | date-versioned model IDs resolve to correct pricing; claude-sonnet-4-6 added to table; 4 contract tests added | record.py +11 lines; test_record.py +37 lines; 97→101 tests |
| ▸ 55 | 2026-06-22 | feat(cli): scope section added to CONFIG_TEMPLATE | `ai-steward init` now generates a config with a `scope:` section; operators discover file-targeting on first use | cli.py +9 lines; test assertion widened by 1 field; 101→101 tests (count unchanged; assertion tightened) |
| ▸ 56 | 2026-06-22 | fix(reflect): wire REFLECT token cost into Finding and cycle cost estimate | REFLECT token cost now tracked, reported in trail entries, and included in cycle cost estimate | 6 files changed; +2 fields to Finding; reflect() now returns tuple[str, int, int]; 101→102 tests |
| ▸ 57 | 2026-06-22 | ai-steward: Add lenses configuration field to AiStewardConfig |  |  |
| ▸ 58 | 2026-06-22 | ai-steward: Add configurable lenses field to AiStewardConfig with default ['mandate', 'examination'] |  |  |
| ▸ 59 | 2026-06-22 | ai-steward: Add acm_scope_depth and destination_budget_chars config fields |  |  |
| ▸ 60 | 2026-06-22 | ai-steward: Add lenses field to _CONFIG_TEMPLATE with operator-facing documentation |  |  |
| ▸ 61 | 2026-06-22 | ai-steward: Add docstring to AiStewardConfig.lenses explaining purpose, defaults, and operator use cases |  |  |
| ▸ 62 | 2026-06-22 | ai-steward: Add missing config fields (acm_scope_depth, destination_budget_chars, sandbox) to init template |  |  |
| ▸ 63 | 2026-06-22 | ai-steward: VERIFY FAILED — scan.py lenses wiring attempt |  |  |
| ▸ 64 | 2026-06-22 | extract-json-fence-overlap-fix | BUG FOUND AND FIXED — _extract_json false-negative on back-to-back code fences |  |
| ▸ 65 | 2026-06-22 | dead-config-wire-scope-context | CHANGE ACCEPTED — acm_scope_depth and destination_budget_chars wired into _load_scope_context |  |
| ▸ 66 | 2026-06-22 | test-scope-context-parameter-variation | CHANGE ACCEPTED — two tests added covering scope_depth and budget_chars parameter variation |  |
| ▸ 67 | 2026-06-22 | wire-binary-heuristic-and-skip-dirs | CHANGE ACCEPTED — binary_heuristic_bytes and default_skip_dirs wired from config |  |
| ▸ 68 | 2026-06-22 | ai-steward: Add reflect_lenses parameter to AiStewardConfig for operator control of reflection scope |  |  |
| ▸ 69 | 2026-06-22 | wire-lenses-into-scan-system-prompt | CHANGE ACCEPTED — lenses config field now live; _build_system_prompt wires custom lenses into SCAN |  |
| ▸ 70 | 2026-06-22 | wire-reflect-lenses-into-reflect-system-prompt | CHANGE ACCEPTED — reflect_lenses config field now live; _build_reflect_system_prompt wires custom lenses into REFLECT |  |
| ▸ 71 | 2026-06-22 | field-validator-for-unknown-lens-names | CHANGE ACCEPTED — unknown lens names now trigger UserWarning at config load time |  |
| ▸ 72 | 2026-06-22 | destination-cost-model-correction | CHANGE ACCEPTED — destination.md cost model corrected; retrospect claim #6 falsified |  |
| ▸ 73 | 2026-06-22 | evo-code-quality-patterns | CHANGE ACCEPTED — 3 code quality patterns from evo applied |  |
| ▸ 74 | 2026-06-22 | ai-steward: Add dedicated reflect model field to ModelAssignment for cost optimization |  |  |
| ▸ 75 | 2026-06-22 | multi-cycle-convergence-and-scope-gate | CONVERGENCE VALIDATED + SCOPE GATE BUG FOUND AND FIXED |  |
| ▸ 76 | 2026-06-22 | Retrospect: post-multi-cycle-convergence |  |  |
| ▸ 77 | 2026-06-22 | feat(reorient): add REORIENT phase for arc-level awareness | CHANGE ACCEPTED — 129 tests pass |  |
| ▸ 78 | 2026-06-22 | feat(reorient): add REORIENT phase for arc-level awareness | CHANGE ACCEPTED — 129 tests pass |  |

### Run 1 — 2026-05-14 — Evo analysis and new project decision

- **decided:** ** New project, not an Evo extension.

### Run 2 — 2026-05-14 — Naming decision

- **decided:** ** Name: AI Steward. Repo: `ai-steward`.

### Run 4 — 2026-05-14 — Vision run: understanding operator intent

- **REVERSAL:** ** Vision corrected: removed "demonstration artifact" framing; replaced with "earned unsupervised operation as normal running state."

### Run 5 — 2026-05-14 — Architectural clarification: harness-protocol role and dual-use trail

- **decided:** ** Harness-protocol is a standalone application — not built into ai-steward.
- **decided:** ** Harness-protocol must support all model families.
- **decided:** ** Harness-protocol repo is outside ai-steward's autonomous scope.

### Run 6 — 2026-05-14 — Vision cleanup

- **decided:** ** Harness-protocol stays a standalone application — not built into ai-steward.
- **decided:** ** Harness-protocol must support all model families.
- **decided:** ** Scope enforcement: harness-protocol repo is outside ai-steward's autonomous improvement scope by default.
- **REVERSAL:** ** Vision corrected: removed "demonstration artifact" framing; replaced with "earned unsupervised operation as normal running state."

### Run 8 — 2026-05-15 — Evo architecture analysis; runtime decision; first scaffold

- **decided:** ** Runtime: Python.
- **decided:** ** First scaffold: `pyproject.toml`, `src/ai_steward/__init__.py`, `src/ai_steward/config.py`.

### Run 9 — 2026-05-28 — vision-to-destination-rename

- **decided:** Run the mechanical migration in ai-steward: `git mv .trail/vision.md .trail/destination.md`, update the H1 header line only, leave the rest of the file untouched (operator-held content per the vision-management discipline), append this entry, regenerate derived artifacts, commit only the migration-related files, push.

### Run 11 — 2026-06-19 — Improve: config.py docstring correction (V1 / V2 framing)

- **decided:** ** The `ModelAssignment` five-field structure is correct for both V1 and V2. V1 assigns the same model to all five fields. V2 enforces diversity with a validator. No structural change needed — documentation only.

### Run 12 — 2026-06-19 — Improve: V1 pipeline design

- **decided:** ** ANALYZE and PROPOSE are combined into a single phase called SCAN for V1. Same context, one LLM call. Output is `Finding` (file, description, proposed change, rationale, risk level). This directly enacts the token-efficiency constraint.
- **decided:** ** V1 pipeline design — full specification follows.

### Run 13 — 2026-06-19 — Improve: harness.py — structural Observable Autonomy

- **decided:** ** `harness.py` exposes three functions only: `is_reachable()` (TCP socket, no HTTP), `anthropic_base_url()` (returns proxy endpoint as string), `harness_session()` (context manager for HARNESS_ROOT). No SDK imports — keeps the module dependency-free and independently testable.
- **decided:** ** TCP socket check for reachability, not HTTP. A GET to a POST-only route would return 405, which proves connectivity but sends a malformed request. TCP is cleaner and sufficient.

### Run 14 — 2026-06-19 — Improve: pipeline loop skeleton + PRE-FLIGHT gates

- **decided:** ** `Finding` and `LoopResult` defined in `pipeline/loop.py`, re-exported from `pipeline/__init__.py`. Single source of truth.
- **decided:** ** `_baseline_tests()` uses `python -m pytest` — V1 targets Python repos only. Known scope constraint.
- **decided:** ** `run()` raises `NotImplementedError` after PRE-FLIGHT passes. Honest about what's not done; prevents silent partial execution.

### Run 15 — 2026-06-19 — Improve: VERIFY phase + rollback utility

- **decided:** ** `rollback.py` at package root (not in pipeline/) per design spec.
- **decided:** ** `verify.py` owns its own `_run_tests()` rather than importing from `loop.py`. Coupling cost exceeds DRY benefit for 5 lines.
- **REVERSAL:** ** Prediction partially failed — 2 test bugs. Both pass-path tests triggered the 2x size guard inadvertently (6-byte original, 19-byte modified = 3x). The verify.py code was correct. Fixed by using same-size file content. Three runs to get to green (initial fail, stale assertion, pass).

### Run 16 — 2026-06-19 — Improve: SCAN phase

- **decided:** ** Lazy-import anthropic inside scan() when client is None. TYPE_CHECKING guard for the annotation. Tests pass a MagicMock and never trigger the import. anthropic added to pyproject.toml as a declared runtime dependency.
- **decided:** ** _collect_files defaults to `**/*.py` when scope.allowed is empty. V1 targets Python repos. No context-window size limit in V1 -- bounded by scope config.
- **decided:** ** V1 gate: skip `risk: high` findings silently (return None). High-risk changes require tier 2/3 reasoning which V1 defers.
- **decided:** ** Same lazy-import + client-injection pattern as scan.py. Local `import anthropic as _anthropic` inside function body; TYPE_CHECKING guard for annotation.
- **decided:** ** IMPLEMENT returns `(True, "", original_size_bytes)` on success. The original_size_bytes feeds directly into VERIFY's 2x size guard. Return (False, reason, 0) on any failure; file is NOT modified on failure paths.
- **decided:** ** Defensive code-fence stripping: strip leading fence + language tag and trailing ` if present. Applies only when response starts with ` after lstrip(). Known gap: preamble + fence pattern not handled in V1.
- **decided:** ** record() takes `diff: str` as a parameter (precomputed by loop.py) so loop.py can populate both LoopResult.diff and the trail entry from one source.
- **decided:** ** _stage_file() is silent on failure (no check=True). VERIFY already confirmed a git repo exists; staging failure at this point is a transient OS issue. Operator will notice on review.
- **decided:** ** open("a", encoding="utf-8", newline="\n") -- explicit LF prevents Windows CRLF expansion in the trail file. Proactive application of the CRLF [!REALIZATION] from the implement iteration.
- **decided:** ** `config` parameter kept in record() signature even though V1 doesn't use it. V2 will use it for trail format and model tagging. Avoids a breaking change at wiring time.
- **decided:** ** Phase modules (scan, implement, verify, record) are lazy-imported inside run() to break the circular import: all phases import Finding from loop.py. Python resolves the import from sys.modules at call time, so monkeypatching source modules before calling run() still works in tests.
- **decided:** ** `implement_failed` added to LoopResult.status Literal. The loop has 5 real exit paths; suppressing one into "nothing_found" or "verify_failed" would mislead operators.
- **decided:** ** harness_session wraps only SCAN + IMPLEMENT (the two LLM calls). VERIFY and RECORD are tier-0 and run outside the context. _get_diff() captures the unstaged diff between IMPLEMENT and RECORD so LoopResult.diff and the trail entry are sourced from the same subprocess call.
- **decided:** ** cli.py imports yaml at module level. This means --help fails if pyyaml isn't installed. Known V1 footgun; lazy import inside run() would fix it but adds noise. Accepted.
- **decided:** ** pyyaml>=6.0 added to pyproject.toml. Required for cli.py config loading.
- **decided:** ** `allow_dirty: bool = False` added to `AiStewardConfig`. The dirty-tree gate is preserved as the default; operators opt in explicitly. Bypassing the gate when `allow_dirty=True` means the loop may mix its staged change with operator WIP -- accepted tradeoff documented in field comment.
- **decided:** ** The session summary described this as "config carries the field, code ignores it" -- but the field did not exist in the actual code. The gap was in both config.py and loop.py. Corrected both.
- **REVERSAL:** ** test_implement_returns_original_size_bytes initially used `write_text(original)` and asserted `len(original.encode("utf-8"))`. On Windows, `write_text` emits CRLF, inflating the on-disk size by 4 bytes (32 vs 28). Fixed by using `write_bytes(original.encode("utf-8"))` to control exact byte layout. Same CRLF class as verify tests -- this is now the third occurrence in one session.
- **REVERSAL:** , multiple [!REALIZATION])
- **REVERSAL:** markers across 15 entries. Prediction accuracy: high -- most held exactly. One class of mistake repeated 3 times (CRLF/byte-size on Windows), documented and mitigated.

### Run 17 — 2026-06-20 — ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

- **decided:** ** Add _load_destination(repo) to scan.py. Reads .trail/destination.md from the target repo, caps at 3000 chars (~750 tokens) to honour the tier-1 cost constraint. When present, the user message becomes: Commander's Intent section + file list + "Identify one improvement that advances the stated destination." When absent, falls back to the V1 undirected prompt.
- **decided:** ** Change 	ext[:3000] to 	ext[-3000:]. Move truncation marker to the top of the excerpt (as a preamble) rather than the bottom (where it was appended, misleadingly inside the "recent" content). Update docstring to make the tail-taking explicit.
- **decided:** ** Create pipeline/_types.py with Finding and LoopResult. Update imports across scan.py, implement.py, record.py, __init__.py, and all test files. Promote phase imports in run() to top-level.
- **decided:** ** Add `input_tokens: int = 0` and `output_tokens: int = 0` to Finding. Extract usage in scan.py with safe fallback (AttributeError/TypeError/ValueError). Add haiku pricing constants to record.py (`.80/MTok` input, `.00/MTok` output). Include `Tokens (SCAN): N in / M out — est. .XXXXX USD` in trail entries. Update `_mock_client` to set integer usage on the mock message.
- **decided:** ** Add `impl_input_tokens: int = 0` and `impl_output_tokens: int = 0` to Finding. Change implement() return from `tuple[bool, str, int]` to `tuple[bool, str, int, int, int]`. Set impl tokens on finding in loop.py after successful implement call. Update record.py to show SCAN + IMPL + cycle total. Update all test unpack patterns.
- **decided:** ** Three coordinated changes:
- **decided:** , Prediction, lenses, blind spot. Pipeline-generated entries had none of these. If ai-steward is the PEA exemplar, its automated entries must meet the same standard as the manual ones.
- **decided:** ** Refactor _build_entry in record.py only. Use existing Finding fields to produce improve-skill-style entries: [!DECISION] marker, Prediction (proposed_change + expected outcome from rationale), structural lens declarations (Commander's Intent + Code examination), honest blind_spot placeholder. _types.py and scan.py unchanged -- blind_spot is a follow-on candidate.
- **decided:** ** Three coordinated changes, no new LLM calls: add blind_spot: str = "" to Finding in _types.py; add blind_spot to SCAN system prompt JSON schema and extract with .get() (not in required -- degrades gracefully if model omits it); update record.py to use finding.blind_spot with a minimal fallback.
- **decided:** , Prediction, Lenses (Commander's Intent + Code examination), Blind spot (model-identified, not placeholder), File, Tokens, Harness session. An operator reviewing a self-targeting run can verify the reasoning structure.
- **decided:** ** Add 3 tests for harness_session() session discovery: (1) single new session discovered, (2) latest ULID picked when multiple sessions created, (3) None when no session created. No production code changes.
- **decided:** ** Add a "Current State" section at the top of destination.md synthesizing all dated sections. Preserve historical record below. Newest-wins on conflicts. Explicitly state dual purpose: (1) proof -- PEA reference implementation, (2) tool -- actually useful, cost-efficiency provable.
- **decided:** ** Add section-boundary logic to _load_destination: search for the first ## YYYY-MM-DD heading at or after the cutoff position using re.search with MULTILINE; if found, start there; fallback to raw tail. One new test. Existing test still passes (no headings in its test data, exercises fallback unchanged).
- **REVERSAL:** markers across 17 entries. High prediction accuracy. CRLF class documented and mitigated.
- **REVERSAL:** ** The top-level import promotion broke 3 tests. With lazy imports, monkeypatching scan_mod.scan worked because run() called
- **REVERSAL:** fix.
- **REVERSAL:** ** Prediction of 61/61 on first attempt failed: 7 test_implement.py tests unpacked the return as 3-tuples (`ok, _, _` and `ok, reason, size`). They all raised `ValueError: too many values to unpack`. I missed that test_implement.py calls implement() directly — test_loop.py uses monkeypatched lambdas (which I did update), but test_implement.py unpacks the real return. Fixed by updating all 7 unpackings to use `*_` for the extra values: `ok, *_`, `ok, reason, size, *_`, `_, _, original_size, *_`. 61/61 after fix.
- **REVERSAL:** ** Prediction of 61/61 on first attempt failed: test_harness.py had two tests asserting `str(tmp_path / ".harness")` that needed updating to `str(tmp_path / ".trail")`. Caught immediately, fixed in same iteration. This is the same pattern as the previous implement-tuple reversal: tests that directly test the changed contract need updating; tests that mock out the whole function do not.
- **REVERSAL:** fired for the second consecutive iteration (test assertions on changed return contracts). Pattern: when changing a contract that has direct test coverage, those tests need updating. Not a structural problem -- honest coverage catching real changes. Not fired as "recurring problem," fired as "pattern documented."
- **REVERSAL:** ` markers across 20+ entries. High prediction accuracy. Recurring class (test assertions on changed contracts) documented and mitigated.
- **REVERSAL:** ** Initial test data was ~2585 chars total -- below the 3000-char threshold -- so truncation never fired and both section headings appeared in the output. Fixed by increasing old_section padding from "A" * 2500 to "A" * 3500 (total ~3587 chars). Same class of mistake as the CRLF test failures: test data that does not actually trigger the code path under test.

### Run 18 — 2026-06-20 — ai-steward: Refactor _build_entry to capture reasoning structure (lenses, predictions, blind spots) in improve-skill-style format to meet structural equivalence requirement from destination 2026-06-20.

- **decided:** ** Proposed: Refactor _build_entry to capture reasoning structure (lenses, predictions, blind spots) in improve-skill-style format to meet structural equivalence requirement from destination 2026-06-20.
- **decided:** ** Proposed: {finding.description}  \n"
- **decided:** ** Fix via per-request header: `X-Harness-Root`. The Rust proxy already had the pattern (`X-Harness-Session`, `X-Harness-Upstream` as per-request overrides). Adding `X-Harness-Root` follows the same pattern. When present, the proxy writes the session to `<header-value>/sessions/<sid>.jsonl` instead of the static startup root. All three handlers updated (openai, anthropic, gemini — both SSE and buffered paths). Header stripped from upstream forwarding.
- **decided:** ** Discard staged bad diff from self-targeting run. The RECORD phase proposed hardcoding `[!REVERSAL]` in every trail entry as a "prediction mismatch placeholder." `[!REVERSAL]` is a marker for actual reversals — a hardcoded placeholder semantically pollutes the learning signal. Diff discarded with `git restore --staged; git checkout --`.
- **REVERSAL:** ** placeholder section for capturing prediction mismatches in future runs, and reorganize the entry so the blind_spot field is prominent as a named decision gate rather than a trailing afterthought.
- **REVERSAL:** ** Prediction Mismatch Gate:  \n"

### Run 19 — 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20.

- **decided:** ** Proposed: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20.
- **decided:** `, blind spot). Currently record.py builds a trail entry that names lenses but does not structurally separate reasoning integrity from outcomes. Aligning the trail format with the skill-suite pattern ensures P2's requirement that 'reasoning is independently verified' is materialized in the audit trail itself, making reasoning integrity auditable.
- **decided:** `, blind spot). Currently record.py builds a trail entry that names lenses but does not structurally separate reasoning integrity from outcomes. Aligning the trail format with the skill-suite pattern ensures P2's requirement that 'reasoning is independently verified' is materialized in the audit trail itself, making reasoning integrity auditable.
- **decided:** ** {finding.description}  \n"
- **decided:** ** Proposed: {finding.description}  \n"
- **REVERSAL:** ` marker stub for future VERIFY data binding, and formats the prediction/rationale structure to match the skill-suite pattern (lenses, predictions, decision marker, blind spot) rather than the current lightweight summary format.
- **REVERSAL:** ` markers when VERIFY data becomes available in future runs; the current record.py has no mechanism to query prior session data or link reversals across cycles.
- **REVERSAL:** ** *stub — VERIFY binding pending*\n"
- **REVERSAL:** ` placeholder error)
- **REVERSAL:** ` in the `_types.py` refactor (monkeypatch timing). Honest handling.

### Run 20 — 2026-06-20 — DRY extraction: run_tests to _utils.py

- **decided:** ** Extract `run_tests(repo: Path) -> tuple[bool, int]` to `_utils.py`. Both `loop.py` and `verify.py` import from it.

### Run 21 — 2026-06-20 — Fix implement() return type annotation

- **decided:** ** Fix the annotation to `-> tuple[bool, str, int, int, int]` and update the docstring to name all 5 return values.

### Run 22 — 2026-06-20 — Make codebase mypy-clean

- **decided:** ** Fix all 4 errors as one coherent action ("make codebase mypy-clean"):

### Run 23 — 2026-06-20 — Add mypy to pyproject.toml

- **decided:** ** Add [tool.mypy] + [project.optional-dependencies] dev extras to pyproject.toml. Minimum change that makes mypy a tracked, consistently-configured tool. No new files, no CI workflows -- that is the next layer.

### Run 24 — 2026-06-20 — Add GitHub Actions CI

- **decided:** ** Create .github/workflows/ci.yml running mypy src/ then pytest on push and PR to main. Uses pip install -e ".[dev]" -- pulls the dev extras already declared in pyproject.toml. No API keys needed: all tests mock the harness proxy.

### Run 25 — 2026-06-20 — Retrospect: post-CI-closure

- **REVERSAL:** markers across the full session (one from _types.py refactor, one from implement-tuple test unpacking). Honest, within expected noise.

### Run 28 — 2026-06-20 — ai-steward: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern.

- **decided:** ** Proposed: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern.
- **decided:** ** Proposed: {finding.description}  \n"
- **REVERSAL:** markers when VERIFY data contradicts predictions.
- **REVERSAL:** placeholder section for future verification data—transforming the trail entry from outcome-focused to reasoning-focused per the 2026-06-20 decision on structural equivalence.
- **REVERSAL:** markers when VERIFY data contradicts predictions.
- **REVERSAL:** ** *(Reserved for VERIFY phase)*  \n"
- **REVERSAL:** placeholder is explicitly prohibited by operational rules — it marks actual reversals, never reserved sections; (2) removes trailing newline at EOF (regression). The refactoring itself is cosmetic with no leverage. This is the attractor loop documented in retrospect.md firing and the operator gate holding. Evidence that the review-then-commit workflow functions correctly.

### Run 29 — 2026-06-20 — fix-scan-false-positive-already-exists-check

- **decided:** Add `already_exists_check` as a required JSON field in the SCAN prompt. The model must quote the specific line(s) from the target file that prove the change is already implemented, or write `not found`. scan() then does a literal case-insensitive substring check: if the quoted text (10+ chars) is found in the target file, return None. The proposal is rejected before IMPLEMENT runs.

### Run 30 — 2026-06-20 — feat-ai-steward-init-command

- **decided:** Add `ai-steward init [REPO]` subcommand. Creates .ai-steward.yaml with working defaults (all phases: claude-haiku-4-5) and scaffolds .trail/destination.md with fill-in-the-blank sections. Skips destination if it already exists. Prints explicit next-steps: edit destination, set API key, start proxy, run.

### Run 31 — 2026-06-20 — feat-configurable-verify-command

- **decided:** ** Change default scope from `["**/*.py"]` to `["**/*"]` with binary file filtering (NUL-byte heuristic, same as git) and system directory exclusions (`.trail`, `.git`, `.harness`, `node_modules`, `__pycache__`, `.venv`, `.mypy_cache`, `.pytest_cache`, `.tox`). Binary filter and directory exclusions apply only in default mode — explicit `scope.allowed` gives the operator full control.
- **decided:** ** Replace `_is_git_repo → fail` gate with `_is_git_repo → auto-init` in PRE-FLIGHT. Add `_git_auto_init(repo)`: runs `git init`, `git add -A`, `git commit --allow-empty`. Sets minimal git identity (ai-steward@local) so it works in any environment, including CI with no global git config. Only fails if git binary itself is unavailable.
- **REVERSAL:** ** First run: 2 pre-existing tests failed. `**/*` collected `.trail/destination.md` as a file, causing its raw content to appear twice in the SCAN prompt (once from `_load_destination()`, once from `_collect_files()`). Fix: add `_DEFAULT_SKIP_DIRS` to exclude `.trail/` and other system dirs when using the default scope. Fixed in same iteration.
- **REVERSAL:** fired again — test relying on directory isolation broke when scope was widened. Class: "test isolation assumptions break when collection scope widens." Documented. Mitigated by `_DEFAULT_SKIP_DIRS`.

### Run 32 — 2026-06-20 — ai-steward: Add explicit git installation check in preflight before attempting git commands to provide clearer error messaging when git is unavailable.

- **decided:** ** Proposed: Add explicit git installation check in preflight before attempting git commands to provide clearer error messaging when git is unavailable.

### Run 33 — 2026-06-21 — ai-steward: Add token budget constraint to SCAN prompt system message

- **decided:** ** Proposed: Add token budget constraint to SCAN prompt system message

### Run 34 — 2026-06-21 — scan-reasoning-quality + V1-milestone-confirmed

- **decided:** with rejected alternatives → Prediction → Blind spot before any conclusion. SCAN should enforce the same discipline, explicitly trading token budget for proposal quality.
- **decided:** with at least one rejected alternative, Prediction, Blind spot. None of these were present in the SCAN prompt.
- **decided:** Replace flat "JSON only" prompt with a 5-step reasoning protocol mirroring the trail skill standard:
- **decided:** : choice + rationale + at least one rejected alternative
- **decided:** with rejected alternative (workspace config file — rejected as unnecessary complexity for V1)

### Run 35 — 2026-06-21 — scan-reasoning-quality + V1-milestone-confirmed

- **decided:** with rejected alternatives → Prediction → Blind spot before any conclusion. SCAN should enforce the same discipline, explicitly trading token budget for proposal quality.
- **decided:** with at least one rejected alternative, Prediction, Blind spot. None of these were present in the SCAN prompt.
- **decided:** Replace flat "JSON only" prompt with a 5-step reasoning protocol mirroring the trail skill standard:
- **decided:** : choice + rationale + at least one rejected alternative
- **decided:** with rejected alternative (workspace config file — rejected as unnecessary complexity for V1)

### Run 37 — 2026-06-21 — feat: capture prediction field from SCAN JSON into Finding and trail entry

- **decided:** Add `prediction` as a required JSON field in the SCAN prompt schema, add `prediction: str = ""` to the `Finding` dataclass, extract it in `scan()`, and use `finding.prediction` in `_build_entry()` with `finding.proposed_change` as fallback.

### Run 40 — 2026-06-21 — feat(orient): inject retrospect.md and learning.md into SCAN context

- **decided:** Add `_load_orient_context()` helper that reads retrospect.md (first 1000 chars) and learning.md (last 500 chars) from repo `.acm/`, then restructure `scan()` to assemble user_content as a `parts` list joined by `---` separators.

### Run 41 — 2026-06-22 — fix(record): remove redundant Expected outcome line from trail entry

- **decided:** Remove `f"*Expected outcome:* {finding.rationale}\n\n"` from `_build_entry()`. The Prediction field now carries a clean, single falsifiable statement.

### Run 42 — 2026-06-22 — feat(record): replace hardcoded lenses with examination_summary from SCAN Step 2

- **decided:** Add `examination_summary: str = ""` to `Finding`, `"examination_summary"` to SCAN JSON schema, extract in `scan()`, and replace the two hardcoded lines in `_build_entry()` with the model’s value (fallback to generic lines if empty).
- **decided:** (description + rationale + risk), Prediction (Step 4 falsifiable statement), Lenses (Step 2 examination summary), Blind spot (Step 5). The remaining gap is fundamentally different: Reflection (a second LLM call after VERIFY), across-trail trigger evaluation, and Candidate Next Moves. These require architecture changes to the pipeline, not field additions.

### Run 43 — 2026-06-22 — ai-steward: Add verify_command to the config template to expose test runner control

- **decided:** ** Proposed: Add verify_command to the config template to expose test runner control

### Run 44 — 2026-06-22 — live-validation: first self-targeting run with all field fixes

- **decided:** add max_tokens_scan and max_tokens_implement to AiStewardConfig
- **decided:** Implement the model’s own proposal: add `max_tokens_scan: int = 4096` and `max_tokens_implement: int = 4096` to AiStewardConfig; wire into scan.py and implement.py; update .ai-steward.yaml self-targeting config.

### Run 45 — 2026-06-22 — fix(implement): ensure trailing newline after model rewrites file

- **decided:** Add `if not new_content.endswith("\n"): new_content += "\n"` immediately before `target.write_text()`, after the empty-content guard. Applies unconditionally to both the fenced and unfenced paths.

### Run 46 — 2026-06-22 — fix(record): model-keyed pricing table for accurate cycle cost estimates

- **decided:** Replace two module-level constants with `_MODEL_PRICING` dict (haiku, sonnet, opus), a `_model_cost_per_token(model)` lookup, and `_estimate_cycle_cost(config, finding)` helper. Calculate in `record()` and pass `cycle_cost_usd` into `_build_entry()`.
- **decided:** , Prediction, Lenses, Blind spot, Token counts, and Cycle cost. The remaining architectural gap is Reflection (second LLM call), across-trail triggers, and Candidate Next Moves. These are not field additions; they require a second LLM call after VERIFY and architectural changes to the loop.

### Run 47 — 2026-06-22 — feat(reflect): add REFLECT phase — third LLM call producing Reflection section in trail entries

- **decided:** Add `pipeline/reflect.py` — a new phase that makes one LLM call (max 400 tokens) after VERIFY passes. The prompt provides prediction + diff + verify result; the model returns 2-3 paragraph prose (prediction accuracy, falsifiable model-claim, specific blind spot). Add `reflection: str = ""` to `Finding`. Call `reflect()` from `loop.py` after `verify()` passes. Output `**Reflection:**` in `_build_entry()` when non-empty (omit section when empty — graceful degradation if model call fails).
- **decided:** , Prediction, Lenses (examination_summary), Blind spot (from SCAN Step 5), Reflection (from REFLECT LLM call), Token counts, Cycle cost, Harness session. The pipeline is architecturally complete for V1's trail quality requirement.
- **REVERSAL:** Prediction said "~86 tests." Actual: 88 (+7, not +5). Under-counted: 5 in test_reflect.py + 1 in test_loop.py + 2 in test_record.py = 8 new; 88 total not 86. All green; the count was wrong, the correctness was not.

### Run 48 — 2026-06-22 — ai-steward: Add max_tokens_reflect config parameter for REFLECT phase

- **decided:** ** Proposed: Add max_tokens_reflect config parameter for REFLECT phase

### Run 50 — 2026-06-22 — fix(harness): complete session coverage — all pipeline LLM calls captured

- **decided:** **Fix the Observable Autonomy gap in two layers:**

### Run 51 — 2026-06-22 — fix(cli): CONFIG_TEMPLATE exposes full operator-tunable surface

- **decided:** Backfill `_CONFIG_TEMPLATE` with the full operator-tunable surface: `max_tokens_scan`, `max_tokens_implement`, `max_tokens_reflect`, `max_iterations`, `budget_usd`, `allow_dirty`. Add inline comments explaining what each controls and why the default was chosen.

### Run 52 — 2026-06-22 — fix(scan): orient context delivers operational rules

- **decided:** Fix in two parts:
- **REVERSAL:** Retrospect.md claim #4 ("ORIENT is implemented; the autonomous pipeline now reads from the same evidence layer as human-supervised sessions") is demonstrably false for the operational rules section. It was false from the moment ORIENT was implemented. The claim should be updated in the next retrospect run.

### Run 53 — 2026-06-22 — Retrospect: post-governance-layer-completion

- **REVERSAL:** Prior claim 4 ("ORIENT is implemented; autonomous pipeline reads from same evidence layer as human sessions") was false from entry 40. Corrected: ORIENT context now delivers both arc-claims and rules, via entry 52's header extraction. Contract-tested.

### Run 54 — 2026-06-22 — fix(record): model ID prefix matching in _model_cost_per_token

- **decided:** Fix with prefix matching: `model == key or model.startswith(key + "-")`. Add `claude-sonnet-4-6` to the table (distinct model, not a date variant of 4-5). Add 4 contract tests.

### Run 55 — 2026-06-22 — feat(cli): scope section added to CONFIG_TEMPLATE

- **decided:** Add `scope:` section to `_CONFIG_TEMPLATE` with `allowed` and `blocked` example patterns and explanatory comments. Extend test assertion to include `scope` as a required field.

### Run 56 — 2026-06-22 — fix(reflect): wire REFLECT token cost into Finding and cycle cost estimate

- **decided:** Add `reflect_input_tokens: int = 0` and `reflect_output_tokens: int = 0` to `Finding`. Change `reflect()` return type to `tuple[str, int, int]`. Capture usage in reflect.py (same try/except pattern as implement.py). Update loop.py to unpack. Update `_estimate_cycle_cost()` and the trail tokens line.
- **REVERSAL:** Entry 46's realization "record.py field-level correctness is now complete for the single-cycle case" was false. REFLECT was added in entry 47 without wiring its cost into record.py. The field-level correctness claim is now accurate: all three LLM phases are tracked.

### Run 57 — 2026-06-22 — ai-steward: Add lenses configuration field to AiStewardConfig

- **decided:** ** Proposed: Add lenses configuration field to AiStewardConfig
- **REVERSAL:** Operator rejected — 2026-06-22:** Dead config (YAGNI). The pipeline predicted the field would be inert yet proposed it as structural prep. A config field that does nothing is waste, not preparation. Unstaged and discarded. Next cycle must find a change that alters behaviour.

### Run 58 — 2026-06-22 — ai-steward: Add configurable lenses field to AiStewardConfig with default ['mandate', 'examination']

- **decided:** ** Proposed: Add configurable lenses field to AiStewardConfig with default ['mandate', 'examination']
- **REVERSAL:** Operator correction — 2026-06-22:** Cycle-1 YAGNI rejection was wrong. destination.md explicitly mandates lenses be operator-configurable and not hardcoded. SCAN was correctly reading the mandate both cycles. The partial-implementation pattern (config field now, scan.py wiring next cycle) is the correct iterative approach. Cycle-2 proposal accepted and committed as `31f4015`. Cycle-3 should wire the lenses field into scan.py prompt construction.

### Run 59 — 2026-06-22 — ai-steward: Add acm_scope_depth and destination_budget_chars config fields

- **decided:** ** Proposed: Add acm_scope_depth and destination_budget_chars config fields

### Run 60 — 2026-06-22 — ai-steward: Add lenses field to _CONFIG_TEMPLATE with operator-facing documentation

- **decided:** ** Proposed: Add lenses field to _CONFIG_TEMPLATE with operator-facing documentation

### Run 61 — 2026-06-22 — ai-steward: Add docstring to AiStewardConfig.lenses explaining purpose, defaults, and operator use cases

- **decided:** ** Proposed: Add docstring to AiStewardConfig.lenses explaining purpose, defaults, and operator use cases
- **REVERSAL:** Operator rejected — 2026-06-22:** Dead-field documentation. lenses field is still not consumed by scan.py. Documenting intended-but-not-implemented behavior is misleading, not progress. Pending substantive work: (1) wire lenses into scan.py, (2) wire acm_scope_depth+destination_budget_chars into scan.py, (3) add acm_scope_depth+destination_budget_chars to CONFIG_TEMPLATE. Next cycle must choose one of these or declare silence.

### Run 62 — 2026-06-22 — ai-steward: Add missing config fields (acm_scope_depth, destination_budget_chars, sandbox) to init template

- **decided:** ** Proposed: Add missing config fields (acm_scope_depth, destination_budget_chars, sandbox) to init template

### Run 65 — 2026-06-22 — dead-config-wire-scope-context

- **decided:** ** Wire acm_scope_depth and destination_budget_chars into _load_scope_context.

### Run 66 — 2026-06-22 — test-scope-context-parameter-variation

- **decided:** ** Add two tests calling _load_scope_context directly:

### Run 67 — 2026-06-22 — wire-binary-heuristic-and-skip-dirs

- **decided:** ** Add binary_heuristic_bytes: int = 8192 and default_skip_dirs: list[str]

### Run 68 — 2026-06-22 — ai-steward: Add reflect_lenses parameter to AiStewardConfig for operator control of reflection scope

- **decided:** ** Proposed: Add reflect_lenses parameter to AiStewardConfig for operator control of reflection scope

### Run 69 — 2026-06-22 — wire-lenses-into-scan-system-prompt

- **decided:** ** Additive injection: keep _BASE_SYSTEM_PROMPT as the unchanged base (Steps 1-5).
- **REVERSAL:** of that state.
- **REVERSAL:** ** The lenses config field is no longer dead config. Custom lenses now produce

### Run 70 — 2026-06-22 — wire-reflect-lenses-into-reflect-system-prompt

- **decided:** ** Mirror the scan.py lenses architecture in reflect.py:

### Run 71 — 2026-06-22 — field-validator-for-unknown-lens-names

- **decided:** ** Add _KNOWN_SCAN_LENSES and _KNOWN_REFLECT_LENSES frozensets to config.py

### Run 72 — 2026-06-22 — destination-cost-model-correction

- **decided:** ** Append a new dated section to destination.md with the validated cost

### Run 73 — 2026-06-22 — evo-code-quality-patterns

- **decided:** Iteration 1 — Logging infrastructure (highest leverage)**
- **decided:** Iteration 2 — Narrow exception types**
- **decided:** Iteration 3 — from __future__ annotations**
- **REVERSAL:** : test_implement.py was raising RuntimeError as the mock exception.

### Run 74 — 2026-06-22 — ai-steward: Add dedicated reflect model field to ModelAssignment for cost optimization

- **decided:** ** Proposed: Add dedicated reflect model field to ModelAssignment for cost optimization

### Run 75 — 2026-06-22 — multi-cycle-convergence-and-scope-gate

- **decided:** ** Accept convergence as validated. Three consecutive NOTHING FOUND cycles

### Run 77 — 2026-06-22 — feat(reorient): add REORIENT phase for arc-level awareness

- **decided:** Add REORIENT phase — the robot's equivalent of the Retrospect skill.

### Run 78 — 2026-06-22 — feat(reorient): add REORIENT phase for arc-level awareness

- **decided:** Add REORIENT phase — the robot's equivalent of the Retrospect skill.

**78 runs total — 78 with changes, 0 silence**
