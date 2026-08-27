# Experiment 48 — Dense SwiGLU FFN Weight / Shape Model

硬件等级：L0

## Default

A LLaMA-like dense teaching configuration:

```
layers = 32
hidden d = 4096
intermediate d_ff = 11008

Hq = 32
Hkv = 32
Dh = 128

weight bits = 16
prefill rows = 512
decode rows = 1
```

## Run

```bash
python3 model.py
```

Try quantized storage proxy:

```bash
python3 model.py --weight-bits 4.5
```

## Expected default structure

FFN weights/layer:

```
3 × 4096 × 11008
=
135,266,304
```

Attention Q/K/V/O baseline:

```
67,108,864
```

Ratio:

```
FFN / attention ≈ 2.016
```

FP16 FFN weight storage/layer:

```
≈ 258 MiB
```

## Shape contrast

Prefill:

```
X      [512,4096]
gate   [512,11008]
up     [512,11008]
down   [512,4096]
```

Decode:

```
X      [1,4096]
gate   [1,11008]
up     [1,11008]
down   [1,4096]
```

## Weight-only AI proxy

The script also prints:

```
16M / weight_bits
```

FLOP/weight-byte.

It deliberately ignores activation/dequant/cache overhead and is not a benchmark.
