# Evidence — Experiment 27: SwiGLU / Dense FFN Weight Traffic

状态：stable dense-FFN lesson complete; L0 parameter/storage/shape arithmetic verified; real config comparison path ready.

## Claim

> In a dense decoder, the gated FFN can contain more weights than the attention projections. During one-token decode, repeatedly using these large gate/up/down matrices can make FFN weight traffic a major contributor to bandwidth pressure.

## Primary evidence

### GLU Variants Improve Transformer
https://arxiv.org/abs/2002.05202

Stable mechanism:
```
gate = x W_gate
up   = x W_up
z    = SiLU(gate) ⊙ up
out  = z W_down
```

Common dense gated-FFN baseline:

```
params ≈ 3 d d_ff
```

### LLaMA
https://arxiv.org/abs/2302.13971

LLaMA documents SwiGLU and an intermediate width chosen around the parameter-budget idea:
```
(2/3) × 4d
```
with exact `intermediate_size` model-specific.

## Experiment 48 verification

Default:

```
d = 4096
d_ff = 11008
Hq = Hkv = 32
Dh = 128
```

Verified dense FFN:

```
3 × 4096 × 11008
=
135,266,304 weights/layer
```

Verified MHA Q/K/V/O baseline:

```
4 × 4096 × 4096
=
67,108,864 weights/layer
```

Ratio:

```
135,266,304 / 67,108,864
=
2.015625×
```

FFN storage/layer:

```
FP16:
270,532,608 bytes
=
258.0000 MiB

4.5 bpw:
76,087,296 bytes
=
72.5625 MiB
```

## Prefill vs decode shape

Prefill M=512:

```
[512,4096] × [4096,11008]
```

Decode M=1:

```
[1,4096] × [4096,11008]
```

The weights are the same; token-row count changes.

## Weight-only Roofline proxy

Ignoring activations/dequant/cache:

```
AI_weight
≈
16M / weight_bits
```

For FP16:

```
M=512 → 512 FLOP/weight-byte
M=1   →   1 FLOP/weight-byte
```

This is a teaching proxy, not measured kernel arithmetic intensity.

## Experiment 49

Real config comparison reads:
- hidden_size;
- intermediate_size;
- Hq/Hkv/head_dim;
- dense gated-FFN baseline;
- attention projection baseline.

If MoE fields are detected, the tool marks `MOE-CAVEAT` rather than pretending one dense FFN describes the expert architecture.

## Consequence for optimization

```
FlashAttention improves attention I/O
!=
whole model weight traffic disappears
```

If TG remains bandwidth-bound after attention optimization, FFN/other weight matrices are a plausible remaining source.

## Learner should reject

- attention always contains most decoder weights;
- SwiGLU is sparse expert routing;
- every SwiGLU model has the same expansion ratio;
- quantized storage proves native low-bit matrix execution;
- FlashAttention optimizes FFN;
- prefill/decode use different FFN weights.
