# retrospect.md — ai-steward

_Last updated: 2026-06-20 (run: post-P1-P2-closure)_

---

## Current claims

**1. V1 is structurally complete.**
Both P1 (reasoning visibility) and P2 (harness capture) are closed. The first P1+P2-complete self-targeting run succeeded on 2026-06-20. Harness session was genuinely captured: `.trail/sessions/01KVHXEFZ5DJ6THCP099PKA8WB.jsonl`. 66 tests pass.

**2. Observable Autonomy is structural, not policy.**
The harness writes sessions to the target repo's `.trail/sessions/` directory via the `X-Harness-Root` header. The agent cannot fabricate or omit evidence — the harness writes BEFORE the response is processed. This is the P2 closure.

**3. Commander's Intent is structural, not policy.**
SCAN reads `.trail/destination.md` from the target repo before proposing. Section-boundary truncation ensures the most recent operator decisions (not founding vision) are in context. This is the P1 closure.

**4. Trail entries capture reasoning structure.**
Every trail entry shows: `[!DECISION]`, rationale, risk, prediction, lenses applied, blind spot, tokens, cost, harness session link. The harness session (independent evidence) and the trail entry (agent-authored claim) are co-located but distinct.

**5. The AI keeps targeting record.py with the wrong proposal.**
Two self-targeting runs, two proposals to refactor `_build_entry`, two rejections. The proposals read the destination correctly (it calls for improve-skill-style formatting) but make the same error: hardcoding a `[!REVERSAL]` placeholder in every entry. `[!REVERSAL]` is a marker for actual reversals — a permanent stub pollutes the learning signal. This pattern will repeat until either (a) the destination specifies the exact format or (b) the current format is accepted as correct.

**6. Dual purpose holds.**
ai-steward is both a proof (PEA reference implementation) and a tool (adoptable, cost-provable). The destination makes this explicit. V1 demonstrates both: the harness is structural proof; the ~$0.018/cycle cost is measured, not claimed.

---

## What the next runs should test

**1. Accept the current trail format as sufficient (or write a spec).**
The destination says "improve-skill-style entries" but does not define them. Either write a concrete format spec that the AI can implement correctly, or accept that the current format (decision, rationale, risk, prediction, lenses, blind_spot, tokens, session link) is already sufficient. Until then, every self-targeting run will propose the same wrong fix.

**2. Run against external repos.**
Self-targeting proved the mechanism. The next test is improving a repo the AI has never seen. Pick a small, well-tested project. The hypothesis: the same loop, same cost, same trail structure.

**3. Multi-cycle convergence.**
Run the loop multiple times on the same target until SCAN returns nothing_found. Does the loop stop when it should? Does the trail show a reasonable arc of diminishing returns?

**4. Harness ledger integrity over cycles.**
The harness session files exist. Are they correctly hash-chained? Can the ledger be replayed? This is untested — the structural mechanism exists but has not been exercised beyond single-run capture.

---

## Active operational rules

- **V1 stops before release.** Operator reviews every staged diff. Inviolable.
- **harness-protocol is outside ai-steward's autonomous scope.** Structural exclusion.
- **Token cost is a design constraint.** V1 uses 2 LLM calls per cycle (~$0.018 typical). Justified.
- **Execution layer must remain separate from reasoning layer.** Phases execute; skills reason.
- **Use `write_bytes(content.encode("utf-8"))` in byte-sensitive tests.** [CRLF hazard]
- **Patch the consuming module's namespace, not the source module.** When monkeypatching with top-level imports, use `ai_steward.pipeline.loop.scan` not `scan_mod.scan`.
- **`[!REVERSAL]` marks actual reversals, never placeholders.** Learned from 2 rejected proposals.
- **Retrospect after substantive implementation arcs.** One day old, three commits behind is already stale.

---

## Loop-effectiveness notes

**Bar this retrospect tested:** Structural completeness (P1+P2 closure), cost measurement, self-targeting capability, harness evidence co-location.

**Finding:** The V1 arc is complete. The loop can now improve any repo that has a `.ai-steward.yaml` and a `.trail/destination.md`. The founding hypothesis — "structural guarantees replace social contracts" — validated under operational contact.

**Silence on:** Text-layer consistency of ai-steward's own code. Harness ledger replay integrity. External repo targeting.

**Bars not tested:**
- Multi-cycle convergence (does the loop stop appropriately?)
- External observer audit (can someone who was not there verify the trail?)
- Tool adoption viability (cost + usability under external users)
- Comparative analysis against other autonomous coding systems
