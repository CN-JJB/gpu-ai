# Expected — Experiment 62

Default synthetic result:

```
requests: 12

TTFT mean:
214.583 ms

TTFT p50:
125 ms

TTFT p95:
1200 ms

TTFT p99:
1200 ms

queue mean:
83.333 ms

queue p95:
1000 ms

E2E mean:
1164.583 ms

E2E p95:
2150 ms

mean ITL:
50 ms

p95 mean-ITL:
50 ms

makespan:
4.350 s

request throughput:
2.759 req/s

output token throughput:
55.172 tok/s

SLO compliance:
91.667% (11/12)

required:
99%

SLO:
FAIL
```

## Lesson

Average TTFT is below 500 ms while the defined SLO fails.

Mean latency alone is insufficient.
