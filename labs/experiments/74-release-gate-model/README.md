# Experiment 74 — Synthetic Release Gate / Rollback

硬件等级：L0

## Goal

Prove that a faster candidate can still fail release gates.

## Policy

Bundled example:

```
ready <= 8000 ms
first inference <= 9000 ms
TG speedup >= 1.0x
PPL ratio <= 1.02
critical fixtures pass
TTFT p95 <= 500 ms
SLO compliance >= 99%
```

These are synthetic project thresholds, not universal recommendations.

## Good candidate

```bash
python3 evaluate.py \
  policy.json baseline.json candidate-good.json rollback.json
```

Expected:

```
DECISION: ACCEPT
```

## Fast-but-bad candidate

```bash
python3 evaluate.py \
  policy.json baseline.json candidate-fast-bad.json rollback.json
```

Expected:
- TG gate passes;
- PPL gate fails;
- TTFT gate fails;
- SLO gate fails;

then:

```
DECISION: ROLLBACK
ROLLBACK: VERIFIED
```

## Rollback identity

The rollback JSON exactly restores baseline:
- runtime SHA;
- model SHA;
- config SHA.

Readiness/smoke are checked again.

## Scope

All values/hashes are synthetic.
