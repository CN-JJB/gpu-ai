# Learning / Build Record — 2026-08-27 Serving Capacity / Little's Law

## Slice

35 — Average serving occupancy, queue vs active boundaries, peak concurrency and KV planning.

## Production output

Research:
- `research/llm/0017-serving-capacity-littles-law.md`

Reference:
- `reference/llm/serving-capacity-littles-law.md`

Lesson:
- `lessons/35-serving-capacity/01-littles-law-slots-kv.html`

Labs:
- `labs/experiments/64-littles-law-trace-model/`
- `labs/experiments/65-real-serving-capacity/`

Evidence:
- `examples/evidence/experiment-35-serving-capacity-littles-law.md`

## Verified L0 result

```
λ = 1.2 req/s

L_system = 3.0
L_active = 2.7
L_queue  = 0.3

peak system = 5
peak active = 4
peak queue = 1
```

Constant-KV synthetic:
```
average = 4.05 GiB
peak = 6.0 GiB
```

## Stable skill

Learner can define the boundary before applying:

```
L = λW
```

and does not map E2E in-flight requests directly to slots/KV.

## Next

Overload / admission control:
- unbounded queue tail;
- bounded queue;
- reject/load-shed;
- timeout;
- retry amplification;
- backoff;
- SLO-aware admission.
