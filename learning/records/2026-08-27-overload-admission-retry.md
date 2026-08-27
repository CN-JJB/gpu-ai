# Learning / Build Record — 2026-08-27 Overload / Admission Control

## Slice

36 — Overload, bounded queueing, rejection, retry amplification and backoff.

## Production output

Research:
- `research/llm/0018-overload-admission-retry.md`

Reference:
- `reference/llm/overload-admission-control.md`

Lesson:
- `lessons/36-overload-admission/01-queue-reject-retry.html`

Labs:
- `labs/experiments/66-overload-retry-model/`
- `labs/experiments/67-real-overload-observation/`

Evidence:
- `examples/evidence/experiment-36-overload-admission-retry.md`

## Verified L0 result

```
unbounded:
10 attempts / 10 complete / p95 wait 4.5 s

bounded:
10 / 7 / p95 2.0 s

immediate retry:
19 / 7 / p95 2.0 s

backoff:
18 / 10 / p95 5.5 s
```

## Stable skill

Learner can distinguish:
- availability;
- admitted latency;
- attempt amplification;
- eventual success;
- SLO success.

## Next

Multi-tenant fairness / quotas:
- one long user can occupy scarce slots/KV;
- request-count fairness vs token/resource fairness;
- per-user concurrency/output/context budgets;
- scheduler starvation/fairness tradeoffs.
