# History

Auto-generated from `.acm/audit-trail.md` by the `record.py history --write` command in the autonomous-agent-skills install.
Do not edit by hand â€” re-run the command to refresh.

| # | Date | Slug | Outcome | Delta |
|---|------|------|---------|-------|
| â–¸ 1 | 2026-05-14 | Evo analysis and new project decision |  |  |
| â–¸ 2 | 2026-05-14 | Naming decision |  |  |
| â–¸ 3 | 2026-05-14 | Repo initialization and first vision |  |  |
| â–¸ 4 | 2026-05-14 | Vision run: understanding operator intent |  |  |
| â–¸ 5 | 2026-05-14 | Architectural clarification: harness-protocol role and dual-use trail |  |  |
| â–¸ 6 | 2026-05-14 | Vision cleanup |  |  |
| â–¸ 7 | 2026-05-15 | First retrospect run; launch orientation before first code sprint |  |  |
| â–¸ 8 | 2026-05-15 | Evo architecture analysis; runtime decision; first scaffold |  |  |
| â–¸ 9 | 2026-05-28 | vision-to-destination-rename | artifact `.trail/vision.md` renamed to `.trail/destination.md` to match the renamed Destination skill (was Vision; now at `destination/SKILL.md` v2.0.0 in the skills suite, commit e3d1577). H1 header updated to match; no other content in destination.md was modified — it remains operator-held. | artifact filename only; skill behaviour unchanged. |
| â–¸ 10 | 2026-06-19 | Post-destination-refinement retrospect |  |  |
| â–¸ 11 | 2026-06-19 | Improve: config.py docstring correction (V1 / V2 framing) |  |  |
| â–¸ 12 | 2026-06-19 | Improve: V1 pipeline design |  |  |
| â–¸ 13 | 2026-06-19 | Improve: harness.py — structural Observable Autonomy |  |  |
| â–¸ 14 | 2026-06-19 | Improve: pipeline loop skeleton + PRE-FLIGHT gates |  |  |
| â–¸ 15 | 2026-06-19 | Improve: VERIFY phase + rollback utility |  |  |
| â–¸ 16 | 2026-06-19 | Improve: SCAN phase |  |  |
| â–¸ 17 | 2026-06-20 | ai-steward: Add validation to reject findings with file paths containing directory traversal sequences. |  |  |
| â–¸ 18 | 2026-06-20 | ai-steward: Refactor _build_entry to capture reasoning structure (lenses, predictions, blind spots) in improve-skill-style format to meet structural equivalence requirement from destination 2026-06-20. |  |  |
| â–¸ 19 | 2026-06-20 | ai-steward: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20. |  |  |
| â–¸ 20 | 2026-06-20 | DRY extraction: run_tests to _utils.py |  |  |
| â–¸ 21 | 2026-06-20 | Fix implement() return type annotation |  |  |
| â–¸ 22 | 2026-06-20 | Make codebase mypy-clean |  |  |
| â–¸ 23 | 2026-06-20 | Add mypy to pyproject.toml |  |  |
| â–¸ 24 | 2026-06-20 | Add GitHub Actions CI |  |  |
| â–¸ 25 | 2026-06-20 | Retrospect: post-CI-closure |  |  |
| â–¸ 26 | 2026-06-20 | First external-repo run: vectorium (TypeScript) — VERIFY gap discovered |  |  |
| â–¸ 27 | 2026-06-20 | verify-deletion-guard |  |  |
| â–¸ 28 | 2026-06-20 | ai-steward: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern. |  |  |
| â–¸ 29 | 2026-06-20 | fix-scan-false-positive-already-exists-check |  |  |
| â–¸ 30 | 2026-06-20 | feat-ai-steward-init-command |  |  |
| â–¸ 31 | 2026-06-20 | feat-configurable-verify-command |  |  |
| â–¸ 32 | 2026-06-20 | ai-steward: Add explicit git installation check in preflight before attempting git commands to provide clearer error messaging when git is unavailable. | .acm-root marker support added; 2 new tests. |  |
| â–¸ 33 | 2026-06-21 | ai-steward: Add token budget constraint to SCAN prompt system message |  |  |
| â–¸ 34 | 2026-06-21 | scan-reasoning-quality + V1-milestone-confirmed | SCAN reasoning raised to trail-skill standard; V1 self-targeting milestone confirmed | _SYSTEM_PROMPT rewritten — "JSON only, no prose" → 5-step reasoning protocol |
| â–¸ 35 | 2026-06-21 | scan-reasoning-quality + V1-milestone-confirmed | SCAN reasoning raised to trail-skill standard; V1 self-targeting milestone confirmed | _SYSTEM_PROMPT rewritten — "JSON only, no prose" → 5-step reasoning protocol |
| â–¸ 36 | 2026-06-21 | Retrospect: post-v1-milestone-config-surface |  |  |
| â–¸ 37 | 2026-06-21 | feat: capture prediction field from SCAN JSON into Finding and trail entry |  |  |
| â–¸ 38 | 2026-06-21 | Retrospect: post-prediction-field |  |  |
| â–¸ 39 | 2026-06-21 | Retrospect: pre-orient-implementation |  |  |

### Run 1 â€” 2026-05-14 â€” Evo analysis and new project decision

- **decided:** ** New project, not an Evo extension.

### Run 2 â€” 2026-05-14 â€” Naming decision

- **decided:** ** Name: AI Steward. Repo: `ai-steward`.

### Run 4 â€” 2026-05-14 â€” Vision run: understanding operator intent

- **REVERSAL:** ** Vision corrected: removed "demonstration artifact" framing; replaced with "earned unsupervised operation as normal running state."

### Run 5 â€” 2026-05-14 â€” Architectural clarification: harness-protocol role and dual-use trail

- **decided:** ** Harness-protocol is a standalone application — not built into ai-steward.
- **decided:** ** Harness-protocol must support all model families.
- **decided:** ** Harness-protocol repo is outside ai-steward's autonomous scope.

### Run 6 â€” 2026-05-14 â€” Vision cleanup

- **decided:** ** Harness-protocol stays a standalone application — not built into ai-steward.
- **decided:** ** Harness-protocol must support all model families.
- **decided:** ** Scope enforcement: harness-protocol repo is outside ai-steward's autonomous improvement scope by default.
- **REVERSAL:** ** Vision corrected: removed "demonstration artifact" framing; replaced with "earned unsupervised operation as normal running state."

### Run 8 â€” 2026-05-15 â€” Evo architecture analysis; runtime decision; first scaffold

- **decided:** ** Runtime: Python.
- **decided:** ** First scaffold: `pyproject.toml`, `src/ai_steward/__init__.py`, `src/ai_steward/config.py`.

### Run 9 â€” 2026-05-28 â€” vision-to-destination-rename

- **decided:** Run the mechanical migration in ai-steward: `git mv .trail/vision.md .trail/destination.md`, update the H1 header line only, leave the rest of the file untouched (operator-held content per the vision-management discipline), append this entry, regenerate derived artifacts, commit only the migration-related files, push.

### Run 11 â€” 2026-06-19 â€” Improve: config.py docstring correction (V1 / V2 framing)

- **decided:** ** The `ModelAssignment` five-field structure is correct for both V1 and V2. V1 assigns the same model to all five fields. V2 enforces diversity with a validator. No structural change needed — documentation only.

### Run 12 â€” 2026-06-19 â€” Improve: V1 pipeline design

- **decided:** ** ANALYZE and PROPOSE are combined into a single phase called SCAN for V1. Same context, one LLM call. Output is `Finding` (file, description, proposed change, rationale, risk level). This directly enacts the token-efficiency constraint.
- **decided:** ** V1 pipeline design — full specification follows.

### Run 13 â€” 2026-06-19 â€” Improve: harness.py — structural Observable Autonomy

- **decided:** ** `harness.py` exposes three functions only: `is_reachable()` (TCP socket, no HTTP), `anthropic_base_url()` (returns proxy endpoint as string), `harness_session()` (context manager for HARNESS_ROOT). No SDK imports — keeps the module dependency-free and independently testable.
- **decided:** ** TCP socket check for reachability, not HTTP. A GET to a POST-only route would return 405, which proves connectivity but sends a malformed request. TCP is cleaner and sufficient.

### Run 14 â€” 2026-06-19 â€” Improve: pipeline loop skeleton + PRE-FLIGHT gates

- **decided:** ** `Finding` and `LoopResult` defined in `pipeline/loop.py`, re-exported from `pipeline/__init__.py`. Single source of truth.
- **decided:** ** `_baseline_tests()` uses `python -m pytest` — V1 targets Python repos only. Known scope constraint.
- **decided:** ** `run()` raises `NotImplementedError` after PRE-FLIGHT passes. Honest about what's not done; prevents silent partial execution.

### Run 15 â€” 2026-06-19 â€” Improve: VERIFY phase + rollback utility

- **decided:** ** `rollback.py` at package root (not in pipeline/) per design spec.
- **decided:** ** `verify.py` owns its own `_run_tests()` rather than importing from `loop.py`. Coupling cost exceeds DRY benefit for 5 lines.
- **REVERSAL:** ** Prediction partially failed — 2 test bugs. Both pass-path tests triggered the 2x size guard inadvertently (6-byte original, 19-byte modified = 3x). The verify.py code was correct. Fixed by using same-size file content. Three runs to get to green (initial fail, stale assertion, pass).

### Run 16 â€” 2026-06-19 â€” Improve: SCAN phase

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

### Run 17 â€” 2026-06-20 â€” ai-steward: Add validation to reject findings with file paths containing directory traversal sequences.

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

### Run 18 â€” 2026-06-20 â€” ai-steward: Refactor _build_entry to capture reasoning structure (lenses, predictions, blind spots) in improve-skill-style format to meet structural equivalence requirement from destination 2026-06-20.

- **decided:** ** Proposed: Refactor _build_entry to capture reasoning structure (lenses, predictions, blind spots) in improve-skill-style format to meet structural equivalence requirement from destination 2026-06-20.
- **decided:** ** Proposed: {finding.description}  \n"
- **decided:** ** Fix via per-request header: `X-Harness-Root`. The Rust proxy already had the pattern (`X-Harness-Session`, `X-Harness-Upstream` as per-request overrides). Adding `X-Harness-Root` follows the same pattern. When present, the proxy writes the session to `<header-value>/sessions/<sid>.jsonl` instead of the static startup root. All three handlers updated (openai, anthropic, gemini — both SSE and buffered paths). Header stripped from upstream forwarding.
- **decided:** ** Discard staged bad diff from self-targeting run. The RECORD phase proposed hardcoding `[!REVERSAL]` in every trail entry as a "prediction mismatch placeholder." `[!REVERSAL]` is a marker for actual reversals — a hardcoded placeholder semantically pollutes the learning signal. Diff discarded with `git restore --staged; git checkout --`.
- **REVERSAL:** ** placeholder section for capturing prediction mismatches in future runs, and reorganize the entry so the blind_spot field is prominent as a named decision gate rather than a trailing afterthought.
- **REVERSAL:** ** Prediction Mismatch Gate:  \n"

### Run 19 â€” 2026-06-20 â€” ai-steward: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20.

- **decided:** ** Proposed: Refactor _build_entry to structure reasoning output as improve-skill-style trail entry per destination decision 2026-06-20.
- **decided:** `, blind spot). Currently record.py builds a trail entry that names lenses but does not structurally separate reasoning integrity from outcomes. Aligning the trail format with the skill-suite pattern ensures P2's requirement that 'reasoning is independently verified' is materialized in the audit trail itself, making reasoning integrity auditable.
- **decided:** `, blind spot). Currently record.py builds a trail entry that names lenses but does not structurally separate reasoning integrity from outcomes. Aligning the trail format with the skill-suite pattern ensures P2's requirement that 'reasoning is independently verified' is materialized in the audit trail itself, making reasoning integrity auditable.
- **decided:** ** {finding.description}  \n"
- **decided:** ** Proposed: {finding.description}  \n"
- **REVERSAL:** ` marker stub for future VERIFY data binding, and formats the prediction/rationale structure to match the skill-suite pattern (lenses, predictions, decision marker, blind spot) rather than the current lightweight summary format.
- **REVERSAL:** ` markers when VERIFY data becomes available in future runs; the current record.py has no mechanism to query prior session data or link reversals across cycles.
- **REVERSAL:** ** *stub â€” VERIFY binding pending*\n"
- **REVERSAL:** ` placeholder error)
- **REVERSAL:** ` in the `_types.py` refactor (monkeypatch timing). Honest handling.

### Run 20 â€” 2026-06-20 â€” DRY extraction: run_tests to _utils.py

- **decided:** ** Extract `run_tests(repo: Path) -> tuple[bool, int]` to `_utils.py`. Both `loop.py` and `verify.py` import from it.

### Run 21 â€” 2026-06-20 â€” Fix implement() return type annotation

- **decided:** ** Fix the annotation to `-> tuple[bool, str, int, int, int]` and update the docstring to name all 5 return values.

### Run 22 â€” 2026-06-20 â€” Make codebase mypy-clean

- **decided:** ** Fix all 4 errors as one coherent action ("make codebase mypy-clean"):

### Run 23 â€” 2026-06-20 â€” Add mypy to pyproject.toml

- **decided:** ** Add [tool.mypy] + [project.optional-dependencies] dev extras to pyproject.toml. Minimum change that makes mypy a tracked, consistently-configured tool. No new files, no CI workflows -- that is the next layer.

### Run 24 â€” 2026-06-20 â€” Add GitHub Actions CI

- **decided:** ** Create .github/workflows/ci.yml running mypy src/ then pytest on push and PR to main. Uses pip install -e ".[dev]" -- pulls the dev extras already declared in pyproject.toml. No API keys needed: all tests mock the harness proxy.

### Run 25 â€” 2026-06-20 â€” Retrospect: post-CI-closure

- **REVERSAL:** markers across the full session (one from _types.py refactor, one from implement-tuple test unpacking). Honest, within expected noise.

### Run 28 â€” 2026-06-20 â€” ai-steward: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern.

- **decided:** ** Proposed: Refactor _build_entry to structure reasoning as improve-skill format entries with lenses, predictions, and decision markers matching audit-trail pattern.
- **decided:** ** Proposed: {finding.description}  \n"
- **REVERSAL:** markers when VERIFY data contradicts predictions.
- **REVERSAL:** placeholder section for future verification data—transforming the trail entry from outcome-focused to reasoning-focused per the 2026-06-20 decision on structural equivalence.
- **REVERSAL:** markers when VERIFY data contradicts predictions.
- **REVERSAL:** ** *(Reserved for VERIFY phase)*  \n"
- **REVERSAL:** placeholder is explicitly prohibited by operational rules — it marks actual reversals, never reserved sections; (2) removes trailing newline at EOF (regression). The refactoring itself is cosmetic with no leverage. This is the attractor loop documented in retrospect.md firing and the operator gate holding. Evidence that the review-then-commit workflow functions correctly.

### Run 29 â€” 2026-06-20 â€” fix-scan-false-positive-already-exists-check

- **decided:** Add `already_exists_check` as a required JSON field in the SCAN prompt. The model must quote the specific line(s) from the target file that prove the change is already implemented, or write `not found`. scan() then does a literal case-insensitive substring check: if the quoted text (10+ chars) is found in the target file, return None. The proposal is rejected before IMPLEMENT runs.

### Run 30 â€” 2026-06-20 â€” feat-ai-steward-init-command

- **decided:** Add `ai-steward init [REPO]` subcommand. Creates .ai-steward.yaml with working defaults (all phases: claude-haiku-4-5) and scaffolds .trail/destination.md with fill-in-the-blank sections. Skips destination if it already exists. Prints explicit next-steps: edit destination, set API key, start proxy, run.

### Run 31 â€” 2026-06-20 â€” feat-configurable-verify-command

- **decided:** ** Change default scope from `["**/*.py"]` to `["**/*"]` with binary file filtering (NUL-byte heuristic, same as git) and system directory exclusions (`.trail`, `.git`, `.harness`, `node_modules`, `__pycache__`, `.venv`, `.mypy_cache`, `.pytest_cache`, `.tox`). Binary filter and directory exclusions apply only in default mode — explicit `scope.allowed` gives the operator full control.
- **decided:** ** Replace `_is_git_repo → fail` gate with `_is_git_repo → auto-init` in PRE-FLIGHT. Add `_git_auto_init(repo)`: runs `git init`, `git add -A`, `git commit --allow-empty`. Sets minimal git identity (ai-steward@local) so it works in any environment, including CI with no global git config. Only fails if git binary itself is unavailable.
- **REVERSAL:** ** First run: 2 pre-existing tests failed. `**/*` collected `.trail/destination.md` as a file, causing its raw content to appear twice in the SCAN prompt (once from `_load_destination()`, once from `_collect_files()`). Fix: add `_DEFAULT_SKIP_DIRS` to exclude `.trail/` and other system dirs when using the default scope. Fixed in same iteration.
- **REVERSAL:** fired again — test relying on directory isolation broke when scope was widened. Class: "test isolation assumptions break when collection scope widens." Documented. Mitigated by `_DEFAULT_SKIP_DIRS`.

### Run 32 â€” 2026-06-20 â€” ai-steward: Add explicit git installation check in preflight before attempting git commands to provide clearer error messaging when git is unavailable.

- **decided:** ** Proposed: Add explicit git installation check in preflight before attempting git commands to provide clearer error messaging when git is unavailable.

### Run 33 â€” 2026-06-21 â€” ai-steward: Add token budget constraint to SCAN prompt system message

- **decided:** ** Proposed: Add token budget constraint to SCAN prompt system message

### Run 34 â€” 2026-06-21 â€” scan-reasoning-quality + V1-milestone-confirmed

- **decided:** with rejected alternatives → Prediction → Blind spot before any conclusion. SCAN should enforce the same discipline, explicitly trading token budget for proposal quality.
- **decided:** with at least one rejected alternative, Prediction, Blind spot. None of these were present in the SCAN prompt.
- **decided:** Replace flat "JSON only" prompt with a 5-step reasoning protocol mirroring the trail skill standard:
- **decided:** : choice + rationale + at least one rejected alternative
- **decided:** with rejected alternative (workspace config file — rejected as unnecessary complexity for V1)

### Run 35 â€” 2026-06-21 â€” scan-reasoning-quality + V1-milestone-confirmed

- **decided:** with rejected alternatives → Prediction → Blind spot before any conclusion. SCAN should enforce the same discipline, explicitly trading token budget for proposal quality.
- **decided:** with at least one rejected alternative, Prediction, Blind spot. None of these were present in the SCAN prompt.
- **decided:** Replace flat "JSON only" prompt with a 5-step reasoning protocol mirroring the trail skill standard:
- **decided:** : choice + rationale + at least one rejected alternative
- **decided:** with rejected alternative (workspace config file — rejected as unnecessary complexity for V1)

### Run 37 â€” 2026-06-21 â€” feat: capture prediction field from SCAN JSON into Finding and trail entry

- **decided:** Add `prediction` as a required JSON field in the SCAN prompt schema, add `prediction: str = ""` to the `Finding` dataclass, extract it in `scan()`, and use `finding.prediction` in `_build_entry()` with `finding.proposed_change` as fallback.

**39 runs total â€” 39 with changes, 0 silence**
