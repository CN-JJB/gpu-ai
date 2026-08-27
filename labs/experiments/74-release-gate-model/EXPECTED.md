# Expected — Experiment 74

## candidate-good

```
TG speedup = 1.08x
PPL ratio = 1.01
TTFT p95 = 450 ms
SLO = 99.3%

DECISION: ACCEPT
```

## candidate-fast-bad

```
TG speedup = 1.20x
PPL ratio = 1.04  → FAIL
TTFT p95 = 900 ms → FAIL
SLO = 92% → FAIL

DECISION: ROLLBACK
ROLLBACK: VERIFIED
```

Central lesson:

```
faster
!= release accepted
```
