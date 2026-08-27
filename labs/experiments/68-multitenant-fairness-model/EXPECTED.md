# Expected — Experiment 68

## FIFO

```
makespan = 12 s
slot utilization = 100%

A:
mean wait = 0
p95 wait = 0
last done = 10 s

B:
mean wait = 10.5 s
p95 wait = 11 s
last done = 12 s
```

## Strict per-tenant cap

```
makespan = 20 s
slot utilization = 60%

A:
mean wait = 5 s
p95 wait = 10 s
last done = 20 s

B:
mean wait = 1.5 s
p95 wait = 3 s
last done = 4 s
```

## Fair borrowing

```
makespan = 14 s
slot utilization ≈ 85.714%

A:
mean wait = 2 s
p95 wait = 4 s
last done = 14 s

B:
mean wait = 1.5 s
p95 wait = 3 s
last done = 4 s
```

All values are synthetic.
