# Evidence — Experiment 25: RMSNorm / Residual / RoPE

状态：stable mechanism lesson complete; RMSNorm and RoPE numeric models verified.

## Claim

> RMSNorm, residual paths and RoPE solve different problems: scale control, information/update flow and positional attention geometry. Their tensors are small relative to major weight matrices, but correctness depends on them.

## RMSNorm evidence

Primary:
https://arxiv.org/abs/1910.07467

Stable formula:

```
RMS(x) = sqrt(mean(x²) + eps)
RMSNorm(x) = g ⊙ x / RMS(x)
```

Unlike LayerNorm, RMSNorm does not explicitly subtract the mean.

## LLaMA architecture evidence

Primary:
https://arxiv.org/abs/2302.13971

LLaMA documents:
- pre-normalization;
- RMSNorm;
- SwiGLU;
- RoPE at each layer.

## RoPE evidence

Primary:
https://arxiv.org/abs/2104.09864

Stable idea:
- paired rotations;
- position-dependent angle;
- relative-position structure in Q/K attention inner products.

## Experiment 44 verification

Input:

```
x = [1,-2,3,-4]
eps = 1e-6
```

Verified:

```
RMS(x) = 2.7386129701
RMSNorm(x)
= [0.3651483473,
  -0.7302966947,
   1.09544504198,
  -1.4605933893]

mean(RMSNorm(x))
= -0.1825741737
```

So output is not forced to zero mean.

For `3x`:

```
max |RMSNorm(x)-RMSNorm(3x)|
≈ 8.66e-8
```

The small difference comes from finite epsilon.

## Experiment 45 verification

Default toy:
- d=4;
- base=10000;
- q position=3;
- k position=7;
- common shift=11.

Verified norm preservation:

```
||q|| = ||R(3)q||
≈ 1.41421356237

||k|| = ||R(7)k||
≈ 1.11803398875
```

Base RoPE dot:

```
dot(R(3)q, R(7)k)
≈ 0.5290115894

dot(R(14)q, R(18)k)
≈ 0.5290115894
```

Difference:

```
≈ 1.11e-16
```

Changing only key position gives:

```
dot(R(3)q, R(8)k)
≈ 1.2569534768
```

So the relative-position relation changes.

## KV consequence

RoPE changes the values/position identity of Q/K but does not widen the KV tensor:

```
[B,Hkv,S,Dh]
→
[B,Hkv,S,Dh]
```

The earlier KV capacity formula therefore does not add a large extra RoPE term.

## Cache correctness consequence

A historical key logically corresponds to a position under a specific RoPE configuration.

Therefore cache reuse must preserve relevant:
- model;
- tokenization;
- position/context state;
- RoPE configuration.

## Context extension boundary

```
enough memory for long KV
!=
model preserves quality at that position range
```

Exact `rope_theta` / `rope_scaling` behavior is model/runtime specific.

## Learner should reject

- RMSNorm subtracts mean;
- RMSNorm has no learned scale;
- residual means sublayer can be skipped;
- RoPE adds an embedding vector;
- RoPE universally rotates V;
- whole model is shift invariant;
- cached K can move to arbitrary positions unchanged;
- bigger context allocation guarantees long-context quality.
