# retrospect.md — ai-steward

_Last updated: 2026-06-20 (run: V1-completion-arc-read)_

---

## Current claims

**1. V1 is structurally complete but operationally untested.**
57 tests pass. All five phases exist (PRE-FLIGHT, SCAN, IMPLEMENT, VERIFY, RECORD), the loop is wired, the CLI loads config and calls `run()`. Every test uses mocks — no real LLM call, no real harness connection, no real diff, has ever been exercised. The loop has never produced a proposal on a real repo. The next event that matters is the first real run, not more code.

**2. The execution layer received all attention; the reasoning layer has zero code presence.**
10 consecutive improve iterations built the execution layer in one day. This is correct for V1. But the destination names model-family independence, Probe-based reasoning verification, and convergence-based stopping as the differentiators. None of these exist yet. The arc shows a risk pattern: the loop is most comfortable in execution-layer infrastructure and may stay there. A future run can falsify this by showing reasoning-layer code was added.

**3. Observable Autonomy is structurally implemented but not verified at integration level.**
`harness.py` enforces fail-closed via TCP check; RECORD writes the trail entry and stages the file. These are correct. But the harness ledger write path — the actual `HARNESS_ROOT` JSONL append that is the independent evidence — has never been exercised in this arc. `is_reachable()` only proves TCP. A proxy accepting connections but failing all ledger writes would pass PRE-FLIGHT and produce no evidence trail. This is the most important untested claim in V1.

**4. The founding architecture decisions aged exactly as predicted.**
The "dumb execution layer" realization (May 2026) was validated by the V1 build: tier 0/1 loop built in one session, no inline reasoning needed. Model-family independence as a reasoning integrity mechanism (not performance) remains the right frame but is deferred to V2. The five-field `ModelAssignment` in config.py was not a mistake — V1 sets all five to the same model, and the structure is forward-compatible.

**5. One recurring test-infrastructure hazard: CRLF on Windows.**
Three hits in one session (verify tests, implement tests; caught at design for scan tests). Documented and partially mitigated (`write_bytes` for byte-sensitive tests; `newline="\n"` in `record.py`). The root cause — Windows `write_text` emitting CRLF — remains live for any new test that writes files and compares byte sizes.

**6. One structural debt deferred: `pipeline/_types.py`.**
`Finding` and `LoopResult` live in `loop.py`. Every phase module imports `Finding` from `loop.py`, which creates a circular import. `run()` uses lazy phase imports as a workaround. This is a smell. The correct fix — `pipeline/_types.py` — was recognized, noted as `[!REALIZATION]`, and explicitly deferred. It will compound if V2 adds phases or phases import each other for other reasons.

---

## What the next runs should test

**1. First real run (highest priority).**
Install pyyaml. Start harness proxy. Create `.ai-steward.yaml` in a small real Python repo. Run `ai-steward run <repo>`. Observe what actually happens: does the loop produce a useful proposal, does VERIFY catch anything, does the trail entry look right, does the harness ledger get written? This is V1's test. No amount of additional code work advances the destination more than this.

**2. Harness ledger verification.**
After the first real run, check `<repo>/.harness/` for the JSONL ledger entries. Verify both LLM calls were captured with full request/response. This is the Observable Autonomy guarantee made concrete. If the ledger is empty or absent, the structural guarantee has a hole.

**3. `pipeline/_types.py` refactor.**
Move `Finding` and `LoopResult` to a dedicated types module. Eliminates the lazy-import workaround in `run()`. Changes ~10 files mechanically. Do this before adding any V2 phases.

**4. Reasoning layer first contact.**
After the first real run produces one proposal: run the Improve skill on the PROPOSAL itself (is the proposed change sensible?). That is the first time the reasoning layer examines what the execution layer produced. This is the V1→V2 bridge.

---

## Active operational rules

*Updated from the V1 build arc. Rules that changed are marked.*

- **V1 stops before release.** The operator reviews the staged diff and decides. This remains inviolable — do not wire auto-commit.
- **harness-protocol is outside ai-steward's autonomous scope.** Changes require explicit operator action. Structural exclusion, not a gate.
- **Write evidence before accepting model output.** Fail-closed: harness ledger write must succeed before the loop continues. Not yet verified at runtime — see claim 3.
- **Token cost is a design constraint.** Every LLM call must justify its tier. V1 uses 2 calls per cycle. Any new phase that adds a call must justify it in the trail.
- **Execution layer must remain separate from reasoning layer.** No inline reasoning in pipeline phases. The phases execute; Improve/Retrospect/Probe reason about what they produced.
- **Use `write_bytes(content.encode("utf-8"))` in tests that compare byte sizes.** [NEW — from CRLF [!REALIZATION]] Windows `write_text` emits CRLF; byte counts will diverge silently.
- **Record every design decision before writing code.** Consistently followed in V1 build. Carry forward.
- **Session summaries are forward-planning, not code-describing.** [NEW] The `allow_dirty` gap was described in a session summary as "config carries the field, code ignores it" — but the field didn't exist. Always verify claims against actual files.
- **`_types.py` refactor before adding V2 phases.** [NEW] The lazy-import workaround in `run()` will compound. Do not add phases on top of it.

---

## Loop-effectiveness notes

**Bar this retrospect tested:** Arc consistency, reversal density, coverage of the destination's claims, operational debt accumulation.

**Finding:** The loop built V1 correctly and efficiently. Predictions held at high rate; reversals were marked and explained. No pattern of confabulation detected. The loop is examining the right thing *for now* — but "execution layer completeness" is a bar V1 has clearly satisfied. The next bar is "operational correctness," and the loop has not been challenged on it yet.

**Bars not tested by this retrospect:** Whether V1 produces useful proposals on real code (requires a real run). Whether the harness ledger writes are correct. Whether tier 1 reasoning is sufficient without tier 2/3 (V1's deepest open question from the June 19 retrospect — still open, still the right question).

**Silence on:** Internal code quality (unit test coverage, structural correctness of each phase). The test suite is comprehensive for its scope.

**Bars not tested, explicitly named:** End-to-end integration correctness, proposal quality on real repositories, harness ledger integrity at runtime, reasoning layer existence and behavior.
