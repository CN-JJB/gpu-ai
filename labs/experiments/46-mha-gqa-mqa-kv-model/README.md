# Experiment 46 — MHA / GQA / MQA KV Cost Model

硬件等级：L0

## Default model

```
layers = 32
hidden = 4096
query heads = 32
head_dim = 128
KV bits = 16
context = 32768
```

Compare:
- MHA Hkv=32
- GQA Hkv=8
- MQA Hkv=1

## Run

```bash
python3 compare.py
```

## Expected

| type | KV/token | KV @ 32k |
|---|---:|---:|
| MHA | 512 KiB | 16 GiB |
| GQA-8 | 128 KiB | 4 GiB |
| MQA | 16 KiB | 0.5 GiB |

The script also prints rough Q/K/V/O projection parameter counts.

## Important

This is a homogeneous full-KV teaching model.

Architectures with:
- sliding attention;
- per-layer KV differences;
- latent attention;
- compressed KV;
- hybrid attention;

require a model-specific calculation.
