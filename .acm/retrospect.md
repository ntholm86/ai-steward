# retrospect.md — ai-steward

_Last updated: 2026-06-20 (run: post-CI-closure)_

---

## Current claims

**1. V1 is structurally complete and quality-gated.**
P1 (Commander's Intent) and P2 (Observable Autonomy) are closed. Self-targeting proved the mechanism. CI now enforces `mypy src/` and `pytest` on every push/PR. 66 tests pass. 13 source files are mypy-clean. The code quality infrastructure is as complete as the functional code.

**2. Annotation discipline debt is paid.**
The P2 token-tracking pass landed fast and left a cluster of annotation gaps (wrong return type, missing TYPE_CHECKING guards, unnarrowed nulls). All four were identified and fixed in consecutive iterations. The process gap was closed by wiring mypy into `pyproject.toml` and CI. A future rapid implementation pass cannot leave the same kind of debt silently.

**3. The record.py attractor loop was correctly avoided.**
The prior retrospect documented an attractor: every self-targeting run proposed the same wrong `_build_entry` refactor with hardcoded `[!REVERSAL]` placeholders. This session's five iterations all found improvements elsewhere (DRY extraction, annotation fixes, infrastructure). The attractor remains — the destination still says "improve-skill-style entries" without defining them — but it did not dominate this session.

**4. Candidate next moves are being followed efficiently.**
Each of the five iterations picked the top-ranked candidate from the prior iteration. The operator-gate is steering the loop without friction. This is evidence that the candidate-ranking mechanism is working as designed.

**5. Three structural next steps remain before convergence can be claimed.**
External repo targeting, harness ledger integrity (hash-chain replay), and multi-cycle convergence are all untested. Self-targeting proved the loop works on one repo (itself). Generalisation is the next proof layer.

**6. Dual purpose holds.**
ai-steward is both a proof (PEA reference implementation) and a tool (adoptable, cost-provable). V1 demonstrates both: harness is structural proof; ~$0.018/cycle cost is measured; CI enforcement makes onboarding frictionless.

---

## What the next runs should test

**1. External repo targeting.**
Pick a small, well-tested Python project. Run `ai-steward run <path>`. Does the loop propose, implement, verify, and stage a genuine improvement? Does the trail entry land in `.acm/audit-trail.md` in that repo? Does the harness session land in `.acm/sessions/`?

**2. Multi-cycle convergence.**
Run the loop multiple times on the same target until SCAN returns `nothing_found`. Does the loop stop when it should? Does the trail show a reasonable arc of diminishing returns, not infinite busy-work?

**3. Harness ledger integrity.**
The harness session files exist (`.acm/sessions/*.jsonl`). Are they correctly hash-chained per SPEC §8? Can the ledger be replayed? Can a verifier confirm the trail entry's claim matches the JSONL evidence? This is untested end-to-end.

**4. Accept or spec the trail format.**
The destination says "improve-skill-style entries" without defining them. Either write a concrete format spec or accept the current format as sufficient. Until then, the record.py attractor will fire on future self-targeting runs.

---

## Active operational rules

- **V1 stops before release.** Operator reviews every staged diff. Inviolable.
- **llm-harness-proxy is outside ai-steward's autonomous scope.** Structural exclusion — changes there require separate session.
- **Token cost is a design constraint.** V1 uses 2 LLM calls per cycle (~$0.018 typical). Justified.
- **Execution layer must remain separate from reasoning layer.** Phases execute; skills reason.
- **Use `write_bytes(content.encode("utf-8"))` in byte-sensitive tests.** [CRLF hazard on Windows]
- **Patch the consuming module's namespace, not the source module.** `ai_steward.pipeline.loop.scan` not `scan_mod.scan`.
- **`[!REVERSAL]` marks actual reversals, never placeholders.** Learned from 2 rejected proposals.
- **Retrospect after substantive implementation arcs.** One day old, three commits behind is already stale.
- **Run mypy before committing annotation-adjacent changes.** CI catches it, but catching locally is faster.

---

## Loop-effectiveness notes

**Bar this retrospect tested:** Annotation discipline, CI infrastructure, candidate-next-move tracking, attractor-loop avoidance.

**Finding:** The five-iteration arc was efficient. Every iteration picked the prior iteration's top candidate. No wasted exploration. The recurring-class trigger (annotation fixes) was identified, diagnosed to a root cause (P2 landing without a gate), and structurally closed (CI). The attractor loop (record.py wrong proposals) was successfully avoided by steering attention elsewhere.

**Silence on:** Self-targeting code quality — the loop has not found anything else to improve in its own codebase for two consecutive sessions. This is weak evidence of internal convergence, not proof.

**Bars not tested:**
- External repo targeting (generalisation)
- Harness ledger integrity (hash-chain replay)
- Multi-cycle convergence (does the loop stop appropriately?)
- Hostile external review (publication-rigour-level scrutiny)
- Operational deployability (real users, real cost, real adoption)
