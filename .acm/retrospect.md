# retrospect.md -- ai-steward

_Last updated: 2026-06-21 (run: post-acm-scope-conformance)_

---

## Current claims

**1. External repo targeting is proven.**
The post-CI-closure retrospect listed external targeting as the #1 unproven claim. Entry "First external-repo run: vectorium (TypeScript)" (2026-06-20) confirmed: the loop proposes, implements, verifies, and stages a genuine improvement on an external TypeScript repo. Trail entry lands in the target's .acm/audit-trail.md. Cost: ~$0.021/cycle. This is now evidence, not hypothesis.
**Falsifiable by:** showing the vectorium run produced a false improvement or failed to stage.

**2. V1 refinement arc (post-retro entries 45-56) addressed the findings from the external run.**
Eight iterations after the retrospect on 2026-06-20 closed gaps exposed by the vectorium run and prior self-targeting: VERIFY deletion guard (prevents false positives on delete-only diffs), _build_entry improved to improve-skill-style format, false-positive already_exists_check fix, init command, configurable verify command, technology-agnostic default scope, git auto-init in PRE-FLIGHT, explicit git installation check. Each found its fix in the iteration that opened it. The candidate-next-moves mechanism is steering correctly.
**Falsifiable by:** finding a trail entry where the candidate from the prior iteration was skipped in favor of something unrelated.

**3. ACM §4 scope context traversal is implemented and tested.**
_load_scope_context() traverses parent directories up to 4 levels, collecting .acm/destination.md files from each scope. Higher scopes labeled and listed first; SCAN prompt updated with "Commander's Intent (operator destination -- higher scope governs)." Stop conditions now match ACM §4.2: filesystem root, .acm-root marker (operator ceiling), 4-level cap. Two conformance tests added (test_scan_includes_parent_scope_destination, test_scan_stops_at_acm_root_marker). 78 tests pass. mypy clean.
**Falsifiable by:** finding a SCAN run that ignores a parent-scope destination.md, or a test that passes despite the .acm-root ceiling being violated.

**4. Three structural gaps from the prior retrospect remain open.**
(a) Multi-cycle convergence: not yet tested end-to-end. Does the loop stop when SCAN returns nothing_found? (b) Harness ledger integrity (hash-chain replay): JSONL files exist but replay verification is untested. (c) Trail format spec: destination.md says "improve-skill-style entries" but the _build_entry refactor (entry 48) moved toward this, not to a formal spec. The attractor loop risk exists but has not re-fired.

**5. Dual purpose (proof + tool) still holds. Adoption friction has been further reduced.**
Git auto-init and configurable verify command reduce the setup requirement to near zero. The init command (`ai-steward init`) initializes .acm/ structure in a new target. Technology-agnostic default scope means any repo (not just Python) is a valid first target.

---

## What the next runs should test

1. **Multi-cycle convergence on a real target.** Run the loop multiple times on the same external repo until SCAN returns nothing_found. Does the loop stop? Does the trail show diminishing returns, not busy-work? This is the convergence proof layer.

2. **Harness ledger integrity.** .acm/sessions/*.jsonl files exist (e.g., from the vectorium run). Are they correctly hash-chained per SPEC §8? Can a verifier confirm the trail entry's claim matches the JSONL evidence? Untested end-to-end.

3. **Trail format spec acceptance.** Either write a concrete format spec (replacing "improve-skill-style entries" in destination.md) or explicitly accept the current _build_entry output as sufficient. The attractor loop risk: future self-targeting runs will keep proposing _build_entry changes as long as the destination is vague here.

4. **Test the .acm-root marker in a live workspace scenario.** The unit test confirms the stop condition. A real scenario with the PEA workspace and a nested repo would validate it end-to-end.

5. **ai-steward GitHub repo creation.** No remote exists for this repo. Consistent with how AII was handled today.

---

## Active operational rules

- **V1 stops before release.** Operator reviews every staged diff. Inviolable.
- **llm-harness-proxy is outside ai-steward's autonomous scope.** Structural exclusion — changes there require separate session.
- **Token cost is a design constraint.** V1 uses ~2 LLM calls per cycle (~$0.021 typical on external repos). Justified.
- **Execution layer must remain separate from reasoning layer.** Phases execute; skills reason.
- **ACM §4.2 stop conditions govern scope traversal.** Filesystem root, .acm-root marker, 4-level cap. Not "two consecutive levels without .acm/" (revoked).
- **Trail entries are required for all scan.py changes.** Scope context traversal and .acm-root work were both unrecorded until this retrospect run triggered cleanup (entries 57-58). Any future scan.py change must include a trail entry in the same session.