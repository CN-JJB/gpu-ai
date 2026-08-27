# Experiment 88 — PSU Capacity + Connector Gate Model

硬件等级：L0

## Goal

Show that total PSU wattage and cable/connector compatibility are independent gates.

Run:

```bash
python3 evaluate.py case-single-good.json
python3 evaluate.py case-multigpu-tight.json
python3 evaluate.py case-cable-mismatch.json
```

## Policy

Each case explicitly defines:

```json
"policy": {
  "min_headroom_fraction": 0.15
}
```

This is a synthetic scenario policy, **not** a universal 15% recommendation.

## Expected

### Single-GPU good

```text
850W PSU
550W estimate
35.294% arithmetic headroom
connector/cable confirmed
→ ACCEPT
```

### Multi-GPU tight

```text
850W PSU
820W estimate
3.529% headroom
policy requires 15%
→ REVIEW
```

### Cable mismatch

```text
1000W PSU
600W estimate
40% headroom
modular cable compatibility = false
→ REJECT
```

## Scope

The model does not predict electrical transients or certify a PSU.
