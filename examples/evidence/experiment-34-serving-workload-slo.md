# Evidence — Experiment 34: Serving Workload / SLO

状态：stable serving-metrics lesson complete; synthetic tail-latency analyzer verified; real llama-server collector syntax-checked and ready.

## Claim

> A serving system cannot be summarized by one tokens/s number. Interactive serving must combine client-observed latency, throughput, request-length distribution, queue/occupancy evidence and an explicit SLO.

## Current pinned llama.cpp evidence

Pinned upstream:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current server documentation exposes:
- `--parallel` slots;
- continuous batching;
- `--metrics`;
- prompt-cache controls.

Current `/metrics` documents:
- prompt tokens/time/rate;
- predicted tokens/time/rate;
- requests processing;
- requests deferred;
- context high watermark;
- busy slots per decode;
- speculative metrics.

Pinned tests additionally verify:
- `llamacpp:prompt_tokens_cached_total`;
- cached prompt tokens are accounted separately from actually processed prompt tokens.

Pinned server benchmark tooling uses k6/concurrent requests and warns that its simple dataset prefilter tokenizer is not the real model tokenizer.

## Stable metrics

```
TTFT = first visible token - client request arrival
E2E  = completion - client request arrival
```

True token ITL:

```
ITL_i = token_i_time - token_(i-1)_time
```

Client SSE chunk gap is only a proxy unless one chunk is proven to correspond to one token.

## Experiment 62 verification

Synthetic TTFT values:

```
100,105,110,115,120,125,
130,135,140,145,150,1200 ms
```

Nearest-rank outputs verified:

```
mean TTFT = 214.583 ms
p50 TTFT  = 125 ms
p95 TTFT  = 1200 ms
p99 TTFT  = 1200 ms

mean queue = 83.333 ms
p95 queue  = 1000 ms

mean E2E = 1164.583 ms
p95 E2E  = 2150 ms

mean request ITL = 50 ms
p95 request ITL  = 50 ms
```

Makespan:

```
4.350 s
```

Throughput:

```
2.759 req/s
55.172 output tok/s
```

SLO:

```
TTFT <= 500 ms
AND mean ITL <= 80 ms
for >=99% requests
```

Measured synthetic compliance:

```
11/12
=
91.667%
→ FAIL
```

So the mean TTFT appears healthy while the declared tail/SLO fails.

## Experiment 63

The real collector:
- schedules exact rendered prompt files;
- hashes each prompt;
- streams `/completion`;
- requests returned token IDs;
- timestamps first token-bearing SSE chunk and completion;
- saves raw SSE logs;
- snapshots `/metrics` before/after.

It explicitly labels:
```
token-bearing SSE chunk gap
```
as a client-visible proxy rather than true ITL.

It does not invent server queue time from client TTFT.

## Decision rule

For interactive serving:

```
maximize throughput
subject to
latency SLO + quality
```

not raw maximum tokens/s.

## Learner should reject

- tokens/s fully describes serving;
- TTFT equals GPU prefill time;
- SSE chunk gap is always token ITL;
- request throughput equals token throughput;
- mean latency represents tail;
- p95 has one universal estimator;
- maximum concurrency is always best;
- warm-prefix and cold-prefix traffic are the same workload.
