# Experiment 54 — Full vs Sliding vs Hybrid KV Model

硬件等级：L0

## Default

```
layers = 32
full layers = 8
local layers = 24
window = 4096
Hkv = 8
Dh = 128
KV = FP16
```

Evaluate:
- context 32768
- context 131072

## Run

```bash
python3 compare.py
```

## Expected

At 32k:
- all full = 4 GiB
- all local = 0.5 GiB
- hybrid = 1.375 GiB

At 128k:
- all full = 16 GiB
- all local = 0.5 GiB
- hybrid = 4.375 GiB

The model also prints cached position-layer counts.

## Scope

This assumes:
- same Hkv/Dh in every layer;
- rolling local KV exactly W positions;
- no backend padding;
- no compressed KV.

It is a structural model, not runtime VRAM.
