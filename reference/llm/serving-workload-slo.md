# Serving Workload / SLO Card

## Request timeline

```
arrival
→ queue
→ service/prefill
→ first visible token
→ generated stream
→ completion
```

## Client metrics

```
TTFT = first_visible - arrival
E2E  = completion - arrival
```

Token-level:

```
ITL_i = token_i - token_(i-1)
```

If only stream chunks are visible:

```
chunk gap = proxy
!= guaranteed token ITL
```

## Throughput

- requests/s
- prompt tokens/s
- output tokens/s
- aggregate tokens/s

Always record request-length distribution.

## Tail

Course L0 estimator:

```
nearest-rank percentile
rank = ceil(p × N)
```

Record estimator in real reports.

## SLO example

```
TTFT <= 500 ms
mean ITL <= 80 ms
for >=99% requests
```

## Workload identity

- request-trace SHA:
- arrival schedule:
- prompt-token distribution:
- output-token distribution:
- slots:
- continuous batching:
- cache state:
- context:
- sampler:
- client/server network path:
- percentile estimator:

## Current pinned llama-server observations

Metrics include:
- prompt token/time/rate;
- cached prompt tokens (verified by tests);
- predicted token/time/rate;
- processing requests;
- deferred requests;
- context high watermark;
- busy slots per decode.

## Decision rule

Optimize:

```
throughput
subject to
latency + quality SLO
```

not throughput alone.
