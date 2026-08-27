# Result — Experiment 67

## Identity

- server/model manifest:
- runtime:
- slots:
- continuous batching:
- cache:
- context:

## Baseline workload

- trace SHA:
- requests:
- spacing:
- prompt tokens:
- output budget:

## Burst workload

- trace SHA:
- requests:
- spacing:
- prompt tokens:
- output budget:

## Client result

- success:
- errors/rejections:
- TTFT p50:
- TTFT p95:
- E2E p95:
- chunk-gap proxy p95:

## Server result

- requests_processing:
- requests_deferred:
- prompt token delta:
- cached prompt delta:
- predicted token delta:

## Admission policy

- queue/concurrency limit:
- where enforced:
- overload response:
- retry-after signal if any:

## Retry

- original requests:
- total attempts:
- amplification:
- retry policy:
- eventual success:
- user p95 E2E:

## Cancellation

- client timeout:
- server cancellation evidence:

## Decision

- keep current queue policy
- add/tighten admission
- reduce retry
- add backoff
- needs more evidence

## Why

Separate:
1. latency tail;
2. success/reject rate;
3. attempt amplification;
4. resource/KV protection;
5. user SLO.
