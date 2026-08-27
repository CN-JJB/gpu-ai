# Experiment 62 — Serving Tail-Latency Trace Analyzer

硬件等级：L0

## Goal

Learn to compute:
- queue wait;
- TTFT;
- E2E;
- request-level mean ITL;
- p50/p95/p99;
- request throughput;
- output-token throughput;
- SLO compliance.

The bundled CSV is **synthetic**.

## Run

```bash
python3 analyze_trace.py trace-synthetic.csv
```

Default SLO:

```
TTFT <= 500 ms
AND
mean ITL <= 80 ms
for >= 99% of requests
```

## Why the trace is useful

11 requests have TTFT between 100–150 ms.

One request queues for 1000 ms and gets:

```
TTFT = 1200 ms
```

All requests have request-level mean ITL:

```
50 ms
```

This isolates the idea:

```
queue tail
→ TTFT tail
```

without changing active-generation cadence.

## Percentile method

The script deliberately uses:

```
nearest-rank
rank = ceil(p × N)
```

Other tools can use different estimators.

## Scope

This trace is not a continuous-batching simulator and contains no real hardware result.

It is a metric-reading exercise.
