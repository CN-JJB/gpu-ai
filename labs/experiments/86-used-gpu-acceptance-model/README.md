# Experiment 86 — Used-GPU Acceptance Decision Model

硬件等级：L0

## Goal

Practice evidence classification without pretending one metric proves card health.

Run three synthetic cases:

```bash
python3 evaluate.py case-healthy.json
python3 evaluate.py case-idle-link-review.json
python3 evaluate.py case-vram-mismatch.json
```

## Expected

### Healthy

```text
ACCEPT
```

### Idle-link case

Current link is low but:
- max capability matches;
- observation is idle;
- runtime/workload otherwise pass.

Result:

```text
REVIEW
```

not REJECT.

### VRAM mismatch

Seller claims 24 GiB while observed is 12 GiB.

Result:

```text
REJECT
```

## Rules

Critical reject examples:
- major purchase-critical VRAM mismatch;
- target runtime not recognized;
- sustained workload repeatedly fails;
- observed uncorrectable hardware errors >0.

Review examples:
- PCIe current state lower than expected without a representative under-load check;
- telemetry unsupported;
- meaningful thermal/TG drift needing investigation;
- display outputs untested for a display-dependent purchase.

## Scope

All cases are synthetic.

The script is not a warranty or hardware-authenticity certificate.
