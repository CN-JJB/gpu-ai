# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–36 are implemented.
Experiments 01–67 exist.

## Slice 36 core

Synthetic overload:

```
10 originals
arrival 0.5 s apart
service 1 req/s
```

Results:

```
unbounded:
10 attempts → 10 complete
p95 wait 4.5 s

bounded no retry:
10 → 7 complete
p95 wait 2.0 s

immediate retry:
19 attempts → still 7 complete
1.9× attempt amplification

backoff:
18 attempts → 10 complete
p95 wait 5.5 s
```

Key distinction:

```
eventual success
!= latency SLO
```

Admission can protect tail latency/resource stability by rejecting some work early.

Real lab is bounded, local/authorized only, and observes actual server behavior rather than assuming rejection.

## Active next slice — Multi-Tenant Fairness / Quotas

Build:

```
tenant A long requests
tenant B short requests
shared slots/KV
→ fairness policy
→ latency/throughput allocation
```

Teach:
- equal requests != equal tokens/resource cost;
- per-user concurrency limits;
- output/context budgets;
- token-weighted or cost-aware accounting;
- fairness vs utilization;
- starvation risk under shortest-job-first-like policies;
- priority needs explicit policy.

Do not assume llama-server itself implements all quota/scheduling features; separate application/gateway policy from inference runtime.
