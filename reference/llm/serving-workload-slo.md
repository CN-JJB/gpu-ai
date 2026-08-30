# Serving Workload / SLO Card

<figure>
  <img src="../../assets/diagrams/serving-slo-timeline.svg" alt="Serving Workload / SLO Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Serving Workload / SLO Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


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
