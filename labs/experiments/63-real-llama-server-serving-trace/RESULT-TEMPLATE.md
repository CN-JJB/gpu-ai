# Result — Experiment 63

## Identity

- Experiment 61 manifest:
- model SHA:
- llama.cpp commit:
- backend/device:
- server command:
- server slots:
- continuous batching:
- cache policy:
- context:

## Workload

- workload JSONL SHA:
- requests:
- arrival schedule:
- prompt-token distribution:
- requested-output distribution:
- client/server network path:

## Client latency

Percentile estimator:

- TTFT mean:
- TTFT p50:
- TTFT p95:
- TTFT p99:
- E2E p95:
- token-bearing SSE chunk-gap p95:
- caveat about chunk gap:

## Throughput

- requests/s:
- observed output token IDs/s:
- server predicted-token delta:
- server prompt-token delta:
- cached-prompt-token delta:

## Queue / occupancy evidence

- requests_deferred observation:
- requests_processing:
- busy slots/decode:
- note: client trace cannot directly isolate server queue time unless server-side service-start evidence is added.

## SLO

Defined before run:
- TTFT target:
- ITL/chunk proxy target:
- error-rate target:
- required compliance:

Measured:
- compliance:
- PASS/FAIL:

## Tail investigation

Slowest requests:
- prompt size:
- output length:
- cache state:
- overlap/concurrency:
- server metrics around event:

## Decision

- throughput configuration accepted?:
- why:
- uncertainty:
