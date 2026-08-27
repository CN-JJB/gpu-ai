# SwiGLU / Dense FFN Quick Reference

## Classic FFN

```
x [M,d]
→ W1 [d,d_ff]
→ activation
→ W2 [d_ff,d]
```

Ignoring bias:

```
params ≈ 2 d d_ff
```

## SwiGLU-style FFN

```
gate = x W_gate
up   = x W_up
z    = SiLU(gate) ⊙ up
out  = z W_down
```

Matrices:

```
W_gate [d,d_ff]
W_up   [d,d_ff]
W_down [d_ff,d]
```

Parameters:

```
≈ 3 d d_ff
```

## SiLU

```
SiLU(x)
=
x × sigmoid(x)
```

## LLaMA design intuition

Paper describes:

```
d_ff
≈
(2/3) × 4d
=
8d/3
```

Exact `intermediate_size` is model-specific.

## Example

```
d = 4096
d_ff = 11008
```

FFN:

```
135,266,304 weights/layer
```

Classic 4096-wide MHA Q/K/V/O:

```
67,108,864 weights/layer
```

Ratio:

```
≈ 2.016×
```

## Weight storage for example FFN

- FP16: ~258 MiB/layer
- 4.5 bpw effective: ~72.56 MiB/layer

Storage is not identical to physical runtime traffic, but it sets the scale.

## Prefill vs decode

Prefill:
```
M = B×T >> 1
→ large GEMMs
→ more weight reuse opportunity
```

Decode:
```
M ≈ 1 per active sequence
→ small-row matrix work
→ weight traffic often dominates
```

## Inspect these fields

- hidden_size
- intermediate_size
- hidden_act
- num_hidden_layers
- attention dimensions
- MoE/expert fields

## Caveat

```
3 d d_ff
```

is a common dense gated-MLP baseline, not universal.
