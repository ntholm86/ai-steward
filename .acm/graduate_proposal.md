# ai-steward V2 — Behavioral Validation & Generalization

_Destination established: 2026-06-22_  
_Prior destination (V1 — Pipeline & Meta-Cognition): ACHIEVED 2026-06-22_

---

## What this destination is for

**V1 achieved:** Structurally complete autonomous improvement loop with execution, governance, and meta-cognitive layers. All phases implemented, wired, and unit-tested (180 tests).

**V2 goal:** Prove the V1 structure generalizes. Validate behavior under operational conditions (multi-cycle runs, external repos, cost limits, compounding-error detection). Surface and fix the gaps that only appear when the robot runs without human cycle-by-cycle supervision.

This destination closes when:
1. At least one **live multi-cycle run** completes successfully (REORIENT fires, GRADUATE or ESCALATE fires, retrospect rewrite validated)
2. At least one **external repo run** completes post-deletion-guard fix (generalization proven beyond self-targeting)
3. **Cost-cap enforcement** verified in a live run (loop stops on budget_usd, not just max_iterations)
4. **Compounding-error detection** tested across N≥3 cycles (stale claim in retrospect.md at cycle N does not corrupt SCAN reasoning at cycle N+1)

Success criteria: each of the four conditions above produces a trail entry documenting the outcome. If all four succeed, V2 is ACHIEVED. If any structural defect surfaces (not just tuning), that defect is the next destination.

---

## What is out of scope for this destination

- Multi-model independence (harness.models API exists but only Claude tested)
- Hash-chain integrity verification (record.py audit trail uses append-only discipline but no cryptographic proof)
- Real-time cost tracking from LLM provider APIs (current budget enforcement uses static per-token rates)
- CODIFY phase (learning.md crystallization into rules.md — deferred until learning.md markers accumulate enough recurring patterns to justify the phase)
- Production deployment patterns (this remains a research/validation prototype)

If V2 surfaces evidence that any of these are required for correctness, they become the V3 destination.

---

## Initial proposed approach

### 1. Live multi-cycle validation (highest priority)

**Preparation:**
- Set up a clean clone or branch of ai-steward
- Configure scope.allowed to include one small Python module (e.g., pipeline/record.py or pipeline/analyze.py)
- Set `reorient_interval: 3`, `max_iterations: 10`, `budget_usd: 0.50` (safe limits for validation run)
- Ensure harness is reachable and configured

**Execution:**
