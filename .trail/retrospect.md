# retrospect.md — ai-steward

_Last updated: 2026-06-19 (run: post-destination-refinement-orientation)_

---

## Current claims

**1. The project has been dormant for 35 days; the destination just leapt forward.**
Last substantive code work: 2026-05-15 (first scaffold). Last entry: 2026-05-28 (mechanical filename migration). The destination received major updates today — token efficiency as architectural constraint, V1 defined as lightweight autonomous loop stopping before release. The trail has not kept pace with the destination's evolution.

**2. The founding decisions are structurally aligned with the new token-efficiency constraint.**
The harness as tokenless structural capture, the "dumb execution layer" realization, the separation of execution from reasoning — these were articulated in May before token cost was named as a first-class constraint, but they support it directly. The founding vision's architecture *enables* the token-efficiency discipline; the June refinement *requires* it.

**3. The existing code (config.py) encodes the full vision, not V1.**
`config.py` defines five-phase model assignment with model-family independence validation. V1 explicitly says: "Single-model operation (no model-family independence yet)." This is a concrete gap. Either the config needs simplification for V1 (a `ModelConfig` with one model, not `ModelAssignment` with five), or V1 inherits complexity it said it would defer. A future run can falsify this by showing the config was simplified or by showing V1's "single-model" claim was revised.

**4. The May retrospect's "next work" candidates are still open.**
- ANALYZE phase definition: not built
- Model-family phase assignment: config exists but no pipeline to use it
- Harness integration module: not built
These were ranked candidates 35 days ago. None advanced.

**5. A tension now exists between the founding vision and V1 scope.**
The founding vision describes: full model-family independence, multi-tier reasoning (tiers 2-3), complete Skills suite integration (Improve, Retrospect, Probe), convergence-based stopping. V1 explicitly defers all of these. The founding realizations (especially model-family independence as reasoning integrity mechanism) may pull toward complexity that V1 intentionally avoids.

**Resolution:** V1 is a corrective commitment, not a regression. The founding vision is the destination; V1 is the first step toward it. The config.py gap is the signal: either simplify the config to match V1, or accept that V1 carries some V2 scaffolding that isn't load-bearing yet.

**6. The harness precondition is still satisfied, but integration is unbuilt.**
Harness-protocol exists at `C:\git\harness-protocol` with tested extraction. The first scaffold references it in `HarnessConfig`. No code actually calls it yet.

---

## What the next runs should test

**1. Resolve the config.py / V1 mismatch.**
Either simplify `config.py` to match V1's "single-model, tier 0/1 only" scope, or explicitly document that the config carries forward structure for V2 while V1 uses a subset. The current state is ambiguous.

**2. Build the minimal V1 loop.**
Per today's destination: analyze → propose → implement → verify → record. Single model. Tier 0 (structural) and tier 1 (cheap model) reasoning only. Manual trigger. Stops with proposal ready for human review. This is the concrete deliverable.

**3. Connect to harness-protocol.**
The execution layer must route all LLM calls through `http://localhost:8474`. The harness captures evidence; the agent processes responses. This integration is the structural Observable Autonomy guarantee — V1 does not earn trust without it.

**4. Define what "tier 0" and "tier 1" mean in code.**
The destination describes the tiers conceptually. What are the actual gates? "Tests pass" is tier 0. "Diff looks reasonable" is tier 1. Where exactly is the boundary? This needs to be concrete before the loop is built.

---

## Active operational rules

*Carried forward from May, updated where the destination changed:*

- **V1 first.** Do not build multi-model-family infrastructure until the single-model loop works end-to-end. The founding realizations are valid; the ordering is corrected.
- **Execution layer must remain separate from reasoning layer.** Do not mix inline LLM calls into pipeline logic. This founding realization holds.
- **harness-protocol is outside ai-steward's autonomous scope.** Changes require explicit operator action. Structural exclusion, not a gate.
- **Write evidence before accepting model output.** Fail-closed: if the ledger write fails, the response is withheld. This is the Observable Autonomy guarantee.
- **Token cost is a design constraint, not an optimization.** Every LLM call must justify its tier. Most cycles should never reach tier 2/3.
- **V1 stops before release.** The operator reviews and decides. Push/release autonomy is earned by demonstrating the pre-release loop produces consistently acceptable proposals.

---

## Loop-effectiveness notes

**Bar this retrospect tested:** Internal consistency between the destination and the trail. Does the arc support the new direction?

**Finding:** The founding decisions support the token-efficiency constraint, but the first code artifact (config.py) was written against the full vision, not V1. The trail has not kept pace with destination evolution.

**Bars not tested:** Whether V1's scope is actually achievable with tier 0/1 reasoning only (that requires building it). Whether the harness integration works in practice. Whether the token-budget numbers from Evo's history are transferable.

**The deepest uncertainty:** Can the autonomous loop produce acceptable proposals without tier 2/3 reasoning? The destination asserts this is possible but offers no evidence. V1 is the test. If it fails — if tier 1 reasoning cannot produce proposals worth reviewing — then the token-efficiency constraint conflicts with the earned-delegation destination, and something has to give.
