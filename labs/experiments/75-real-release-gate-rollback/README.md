# Experiment 75 — Real Release Gate / Rollback Packet

硬件等级：L1/L2/L3，复用前面实验。

## Goal

Turn existing Evidence into one release decision.

This lab does not install/replace a system service.

It consumes results from:
- Experiment 61 — manifest / controlled A/B;
- Experiment 59 — quality;
- Experiment 63 — serving SLO;
- Experiment 73 — readiness/restart.

## 1. Preserve baseline artifacts

Before testing candidate, keep exact:
- server binary;
- model;
- config.

Hash them.

Do not overwrite known-good files in place.

## 2. Define policy first

Copy:

```bash
cp policy.template.json policy.json
```

Choose thresholds for your own workload.

Do not edit them after seeing candidate output merely to force a pass.

## 3. Fill releases

Copy:
`release.template.json`

for:
- baseline;
- candidate;
- rollback verification.

Every `REPLACE` must be resolved.

## 4. Candidate gate

```bash
python3 release_gate.py \
  policy.json \
  baseline-release.json \
  candidate-release.json \
  --rollback rollback-release.json
```

Possible:

```
GATE: ACCEPT
GATE: ROLLBACK
GATE: BLOCKED_MISSING_EVIDENCE
```

## 5. Rollback semantics

Rollback JSON must restore the exact baseline identity block:

```
runtime SHA
model SHA
config SHA
manifest SHA
```

and prove:
- readiness;
- smoke.

If identity is different:

```
ROLLBACK: FAILED
```

even if something answers on the port.

## 6. Causal discipline

Before release gating, use Experiment 60/61 to classify the change.

If multiple semantic blocks changed:
- call it a system release comparison;
- do not claim one-variable causality.

The release gate can still decide operational acceptance.

## 7. Preserve failed-candidate Evidence

Do not delete:
- logs;
- manifests;
- quality traces;
- serving traces;

after rollback.

Redact secrets/private prompts as required.

## 8. Complete

Use:
`RESULT-TEMPLATE.md`.
