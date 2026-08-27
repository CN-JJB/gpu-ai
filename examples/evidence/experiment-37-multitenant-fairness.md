# Evidence — Experiment 37: Multi-Tenant Fairness / Quotas

状态：stable fairness lesson complete; L0 scheduler model verified; real per-tenant report path ready.

## Claim

> Equal request count is not equal resource use. Multi-tenant LLM serving needs explicit fairness units such as concurrent slots, prompt/output tokens, context/KV budgets and per-tenant latency.

## Synthetic workload

```
2 slots
10 output tok/s/slot
all requests arrive at t=0
```

Tenant A:

```
2 requests × 100 output tokens
=
200 tokens
```

Tenant B:

```
4 requests × 10 output tokens
=
40 tokens
```

Request share:
```
A 33.3%
B 66.7%
```

Output-work share:
```
A 83.3%
B 16.7%
```

So request count and resource share are not aligned.

## Experiment 68 verification

### Global FIFO

Verified:

```
makespan = 12 s
slot utilization = 100%

Tenant A:
mean wait = 0
p95 wait = 0
last done = 10 s

Tenant B:
mean wait = 10.5 s
p95 wait = 11 s
last done = 12 s
```

Maximum utilization produces poor B latency.

### Strict one-active-per-tenant cap

Verified:

```
makespan = 20 s
slot utilization = 60%

Tenant A:
mean wait = 5 s
p95 = 10 s
last done = 20 s

Tenant B:
mean wait = 1.5 s
p95 = 3 s
last done = 4 s
```

Fairness improves but spare capacity is wasted after B finishes.

### Work-conserving borrowing

Under contention:
```
max one active per tenant
```

When B has no queued work:
```
A may borrow the idle slot
```

Verified:

```
makespan = 14 s
slot utilization = 85.714%

Tenant A:
mean wait = 2 s
p95 = 4 s
last done = 14 s

Tenant B:
mean wait = 1.5 s
p95 = 3 s
last done = 4 s
```

B keeps the fairness benefit while utilization recovers significantly.

## Stable fairness dimensions

Potential quotas:
- per-tenant concurrent active requests;
- max prompt tokens;
- max output tokens;
- max context;
- token budget/time window;
- estimated KV budget;
- explicit priority/weight.

Token count is a better cost signal than request count for many workloads, but still not a perfect GPU-cost model.

## Starvation boundary

Policies such as:
- strict priority;
- shortest-job-first-like scheduling;

can improve some averages while starving low-priority/long jobs.

Fairness policy needs explicit:
- priority;
- aging/minimum share;
- starvation expectations.

## Experiment 69

The real report joins:
- workload metadata;
- Experiment 63 request trace.

Per tenant it reports:
- request/success count;
- exact prompt-token total if provided;
- requested output budget;
- observed output token IDs;
- TTFT p50/p95;
- E2E p95.

It uses pseudonymous tenant IDs and does not require publishing private prompt content.

## Runtime boundary

The course does not claim llama-server itself implements every quota/scheduler policy.

Application/gateway and inference runtime are separate control layers.

## Learner should reject

- equal request count means fair;
- rigid per-tenant caps always improve utilization;
- token count perfectly predicts GPU cost;
- global p95 proves every tenant gets good service;
- priority has no starvation risk;
- every quota must live inside the inference runtime.
