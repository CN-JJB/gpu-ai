# Experiment 52 — Architecture Dossier Consistency Model

硬件等级：L0

## Goal

Test the dossier formulas on two synthetic configs:
- one dense GQA model;
- one top-2 MoE model.

Run:

```bash
python3 dossier.py dense-config.json --context 32768 --kv-bits 16 --params-b 8 --weight-bpw 4.5 --reserve-gib 1 --memory-gib 12
python3 dossier.py moe-config.json --context 32768 --kv-bits 16 --params-b 47 --weight-bpw 4.5 --reserve-gib 1 --memory-gib 24
```

All config/model-size values are synthetic teaching inputs.

The purpose is to verify:
- derived head relation;
- KV;
- dense FFN;
- MoE fields;
- asymmetric capacity verdict.
