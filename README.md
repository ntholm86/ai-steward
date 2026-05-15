# ai-steward

Autonomous software evolution engine with structurally separated execution and reasoning layers.

## Architecture

```
Reasoning layer  (Skills: Vision, Trail, Improve, Retrospect, Probe)
      │
      ▼
Execution layer  (pipeline phases: ANALYZE → PROPOSE → IMPLEMENT → VERIFY → DECIDE → RELEASE)
      │
      ▼
Structural integrity layer  (harness-protocol — standalone, outside autonomous scope)
```

The execution layer is deliberately dumb: it collects metrics, runs commands, tracks state. It does not reason. All reasoning is the Skills suite's domain.

## Pipeline

| Phase | What it does |
|-------|-------------|
| DETECT | Infer language profile (cached) |
| ANALYZE | Collect baseline metrics, find weaknesses (evidence collection only) |
| PROPOSE | Reasoning layer selects a targeted improvement |
| IMPLEMENT | Apply file changes in a feature branch |
| VERIFY | Re-run all metrics |
| DECIDE | Reasoning layer gates the merge (soft evidence, not hard Pareto rule) |
| RELEASE | Merge, tag, record in harness-protocol ledger |

## Key design principles

- **Model-family independence**: PROPOSE, VERIFY, and JUDGE use different LLM families. This is an integrity mechanism, not a performance optimization.
- **All LLM calls through harness-protocol**: The proxy handles session/ledger recording. The execution layer never calls LLM APIs directly.
- **harness-protocol is outside the autonomous scope**: ai-steward may not modify harness-protocol during a self-targeting run.

## Setup

```
pip install -e ".[dev]"
```

## Usage

```
ai-steward run /path/to/target/repo
```

Requires `.ai-steward.yaml` in the target repo (see `src/ai_steward/config.py` for schema).
