# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–34 are implemented.
Experiments 01–63 exist.

## Slice 34 core

Serving request timeline:

```
arrival
→ queue
→ prefill/service
→ first visible token
→ token stream
→ completion
```

Metrics:

```
TTFT
ITL
E2E
requests/s
output tok/s
p50/p95/p99
SLO compliance
```

Synthetic verified:

```
mean TTFT 214.583 ms
p95 TTFT 1200 ms
mean ITL 50 ms
SLO 99% required
actual 91.667%
→ FAIL
```

This demonstrates:
```
healthy mean
!= healthy tail
```

Real Experiment 63:
- exact prompt files;
- streaming client timestamps;
- raw SSE logs;
- /metrics before/after;
- token-bearing chunk-gap explicitly labeled proxy, not true ITL.

## Active next slice — Serving Capacity Planning

Teach Little's Law:

```
L = λ W
```

where:
- L = average number in system;
- λ = long-run arrival/completion rate;
- W = average time in system.

Use it for planning:
```
req/s × seconds/request
→ average in-flight requests
```

Then connect:
```
in-flight sequences
× per-sequence KV
→ average KV pressure
```

But keep boundaries:
- average is not peak;
- Little's Law does not predict p95;
- overloaded/non-stationary systems need trace evidence;
- slots should include headroom above average, not equal L blindly.
