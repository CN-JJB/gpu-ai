# Experiment 90 — Whole-Machine Feasibility Validator

硬件等级：L0

## Goal

Validate the distinction between:
- known hard failure;
- purchase-critical unknown;
- feasible design.

Run:

```bash
python3 validate.py case-balanced.json
python3 validate.py case-vram-fail.json
python3 validate.py case-unknown-cable.json
```

## Expected

### Balanced

All declared hard gates pass:

```text
DECISION: ACCEPT
```

### VRAM failure

Known capacity requirement exceeds runtime-confirmed available capacity:

```text
DECISION: REVISE
```

### Unknown PSU cable

Capacity is otherwise adequate, but modular-cable compatibility is unknown:

```text
DECISION: BLOCKED
```

## Important

There is no weighted score.

The validator does not choose or purchase replacement hardware.
