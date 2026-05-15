# retrospect.md — ai-steward

_Last updated: 2026-05-15 (run: founding-arc-first-retrospect)_

---

## Current claims

**1. The founding decisions are complete and coherent, but the first execution decision has not been made.**
The arc covers naming, architecture, harness relationship, and vision clarification — all conceptual work from a single session (2026-05-14). No decision has been made about the execution layer's runtime (Python? Rust? Go?), entry point, or pipeline structure. Vision says "informed by Evo, not derived from it" — but Evo's execution layer documentation has not been read in this arc. The first code decision is suspended on a read that hasn't happened. A future run can falsify this by showing a trail entry where Evo's ARCHITECTURE.md was read and the execution layer design was decided.

**2. The Vision skill run produced two reversals and one realization — all three are structurally important.**
The reversals corrected concrete wrong readings of the vision: "while you sleep" is continuous trusted operation, not a demo event; Evo is a reference, not a dependency. The realization — "the execution layer is deliberately dumb; gates are reasoning decisions, not mechanical rules" — is the single most important architectural constraint and has been held consistently across all subsequent entries. These are the three ideas to anchor the first design sprint against.

**3. The trail is a single founding session. There is no arc yet — there is a launch orientation.**
Every entry is dated 2026-05-14. No iteration, no Improve run, no code-level decision. A retrospect at this point cannot identify patterns in the loop's attention because there has been only one pass. The value of this run is: establish the current orientation before work begins, so future retrospects have a baseline to arc-read against.

**4. The harness-protocol precondition is now satisfied.**
Vision designates harness-protocol as the structural integrity layer. As of 2026-05-15 (harness-protocol session), the extraction layer has unit test coverage across all six provider/execution-path combinations. The claim "if proxy and audit-trail diverge, the proxy wins" now rests on tested code. ai-steward can begin designing against harness-protocol as a reliable dependency.

**5. The model-family independence principle is architecturally sound but has no phase assignment.**
Vision defines the principle clearly (proposer and judge from different families, so the judge cannot share the proposer's blind spots). But the trail has no entry assigning model families to pipeline phases. Which family handles ANALYZE? PROPOSE? VERIFY? JUDGE? This is the most concrete open design decision in the vision — it affects cost, latency, and the integrity guarantee's practical strength.

---

## What the next runs should test

**1. Read Evo's ARCHITECTURE.md and make the take/leave/redesign decision.**
This is the stated precondition for the first execution layer commit. Read `c:\git\evo\ARCHITECTURE.md`. For each major Evo component: take (as-is or adapted), leave (structurally wrong for ai-steward), or redesign (concept sound, implementation wrong). Record the decision in audit-trail.md before writing a line of code.

**2. Decide the execution layer's runtime and entry point.**
One decision per run. Likely candidates: Python (matches evo, rich LLM/RAG library ecosystem), Rust (performance, type safety — the operator is clearly comfortable with it), Go (JD nice-to-have, Corti stack). The decision should be traceable to the constraints in vision (multi-provider, self-targeting, structured pipeline).

**3. Define the first pipeline phase.**
Vision specifies: analyze → propose → implement → verify → decide → release → record. Define ANALYZE in full: what inputs it takes, what it produces, what counts as correct output. This is the smallest possible slice that makes the rest of the pipeline testable.

**4. Assign model families to pipeline phases.**
At minimum: decide which family handles PROPOSE (the high-creativity phase) and which handles VERIFY/JUDGE (the adversarial phase). This is the integrity mechanism; designing it as an afterthought risks building the whole pipeline around a single family.

---

## Active operational rules

- **Read Evo's ARCHITECTURE.md before the first execution layer commit.** Not after. The reversal "Evo is a reference, not a dependency" is only meaningful if the reference has actually been read. Designing from memory of Evo's README is not the same as reading the architecture.
- **Execution layer must remain architecturally separate from the reasoning layer.** Do not mix inline LLM calls into pipeline logic. The execution layer executes, verifies, and logs. Reasoning calls go through the reasoning layer. This is the founding realization — violating it recreates Evo's architectural mistake.
- **harness-protocol is outside ai-steward's autonomous improvement scope.** Changes to it require explicit operator action. This is a structural guarantee, not a gate — structural exclusion cannot be autonomously overridden.
- **Write evidence before accepting model output.** The fail-closed design from harness applies here: ai-steward should never consume a model response without the harness having recorded it. If the ledger write fails, the response is withheld. Build the pipeline with this constraint from the first phase.
- **Never scope milestones to single demonstration events.** The destination is continuous trusted operation, not a demo run. Milestones should be states of the system, not events.
- **Record every design decision in audit-trail.md before writing code.** The trail is also documentation — when the repo goes public at MVP, the trail is part of the public argument. Decisions made in code with no trail entry are invisible to that argument.

---

## Loop-effectiveness notes

The arc is too short to assess loop effectiveness in the usual sense — one session, no code, no Improve iterations. What can be said:

The Vision skill run was effective. It produced falsifiable reversals rather than affirmation. The founding decisions are internally consistent and cleanly separate the three layers. The dual-trust-level trail design (proxy-captured JSONL vs. `audit-trail.md`) is architecturally sound and has been consistently held.

The risk going into the first code sprint is the opposite of what harness-protocol's early loop suffered (iterating on visible features while the core claim was untested). ai-steward's risk is: deferring the first phase assignment and model family decision until the pipeline feels "ready" — which means those decisions get made by the code rather than before it.
