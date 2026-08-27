# Experiment 68 — Multi-Tenant Slot Fairness Model

硬件等级：L0

## Goal

Compare:
- global FIFO;
- strict one-active-request-per-tenant cap;
- work-conserving fair borrowing.

Synthetic:
```
2 slots
10 output tok/s/slot
all requests arrive at t=0
```

Tenant A:
```
2 × 100-token jobs
```

Tenant B:
```
4 × 10-token jobs
```

## Run

```bash
python3 simulate.py
```

## Key lesson

Global FIFO:
- utilization 100%;
- B mean wait 10.5 s.

Strict tenant cap:
- B mean wait 1.5 s;
- utilization only 60%.

Fair borrowing:
- B mean wait stays 1.5 s;
- utilization rises to ~85.7%.

## Scope

This is a non-preemptive slot scheduler teaching model.

Real continuous batching is more complex.
