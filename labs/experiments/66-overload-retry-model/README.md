# Experiment 66 — Overload / Retry Amplification Model

硬件等级：L0

## Goal

Compare four synthetic overload policies.

Workload:

```
10 original requests
arrival spacing = 0.5 s
service time = 1.0 s
one active server
```

Scenarios:
1. unbounded queue;
2. queue limit 2, no retry;
3. queue limit 2, immediate retry every 0.1 s, max 3 retries;
4. queue limit 2, deterministic exponential backoff 0.5/1/2 s.

## Run

```bash
python3 simulate.py
```

## Key expected result

Immediate retry:

```
10 originals
→
19 total attempts
```

while completed originals remain:

```
7
```

the same as bounded/no-retry.

That is retry amplification without benefit.

## Caveat

The model uses:
- deterministic arrivals;
- one server;
- fixed service time;
- FIFO queue;
- no jitter.

It is a teaching model, not a production queue simulator.
