# Learning / Build Record — 2026-08-27 Serving Workload / SLO

## Slice

34 — TTFT, ITL, E2E, request/token throughput, tail percentiles and SLO-driven serving decisions.

## Production output

Research:
- `research/llm/0016-serving-workload-slo.md`

Reference:
- `reference/llm/serving-workload-slo.md`

Lesson:
- `lessons/34-serving-slo/01-ttft-itl-tail-throughput.html`

Labs:
- `labs/experiments/62-serving-tail-latency-trace/`
- `labs/experiments/63-real-llama-server-serving-trace/`

Evidence:
- `examples/evidence/experiment-34-serving-workload-slo.md`

## Verified L0 result

Synthetic:
- mean TTFT 214.583 ms;
- p95 TTFT 1200 ms;
- mean ITL 50 ms;
- 99% SLO compliance fails at 91.667%.

## Real path

Experiment 63 captures:
- exact request workload;
- client TTFT/E2E;
- token-bearing SSE chunk-gap proxy;
- raw SSE;
- server metrics before/after.

No real hardware performance is prefilled.

## Stable skill

Learner can now distinguish:
```
server throughput
from
interactive latency
from
tail-SLO compliance
```

## Next

Serving capacity planning:
```
arrival rate
×
time in system
→
average in-flight requests
→
slots/KV pressure
```

with Little's Law as a planning relation, not a latency predictor.
