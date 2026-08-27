# Evidence — Experiment 24: Decoder-only Transformer Dataflow

状态：stable dataflow lesson complete; L0 tensor-shape/KV model verified; real config inspector ready.

## Claim

> Prefill and decode use the same decoder block weights but operate in different tensor-shape/cache regimes. This structural difference explains why PP and TG can have different hardware bottlenecks.

## Stable architecture evidence

Transformer foundation:
- Vaswani et al., 2017 — attention, multi-head attention, feed-forward sublayers, residual/normalization.

Modern decoder-only example:
- LLaMA / Llama 2 / Llama 3 lineage.

LLaMA explicitly documents:
- pre-normalization;
- RMSNorm;
- SwiGLU;
- RoPE;
- decoder-style autoregressive Transformer.

## Dataflow

```
token ids
→ embedding
→ repeated decoder blocks
→ final norm
→ LM head
→ logits
→ sampler
```

Within a simplified pre-norm block:

```
h = x + Attention(Norm(x))
y = h + MLP(Norm(h))
```

## Prefill shapes

```
X [B,T,d]
Q [B,Hq,T,Dh]
K [B,Hkv,T,Dh]
V [B,Hkv,T,Dh]
scores [B,Hq,T,T] conceptual
```

## Decode shapes

At cached length S:

```
X_new [B,1,d]
Q_new [B,Hq,1,Dh]
K/V_new [B,Hkv,1,Dh]
K/V cache [B,Hkv,S,Dh]
scores [B,Hq,1,S] conceptual
```

## KV derivation

```
KV bytes/token
=
2 × layers × KV_heads × head_dim × bytes/element
```

This explains the earlier Slice 05 formula from tensor structure rather than memorization.

## Experiment 42 verification

Default synthetic config:

```
B=1
L=2
d=16
Hq=4
Hkv=2
Dh=4
d_ff=32
T=8
KV bytes/element=2
```

Verified values:

```
prefill conceptual score elements = 256
KV bytes/token = 64
KV after 8 prompt tokens = 512
decode score elements after append = 36
KV after 9 total tokens = 576
attention Q/K/V/O baseline = 768 weights/layer
gated MLP baseline = 1536 weights/layer
```

All are synthetic teaching values.

## Experiment 43

The real config inspector reads common Hugging Face architecture fields and derives:
- Q/KV width;
- MHA/MQA/GQA-like head relation;
- homogeneous KV baseline;
- gated-MLP projection baseline.

It explicitly warns when the config contains:
- MoE;
- sliding/local attention;
- per-layer attention types;
- unusual architecture fields.

It does not force every model into a homogeneous Llama-like baseline.

## Hardware consequence

Prefill:
```
more token rows
→ larger matrix work
→ higher arithmetic intensity
→ matrix units/kernel quality often matter
```

Decode:
```
one/few token rows
+ historical KV
+ serial autoregression
→ lower arithmetic intensity
→ memory bandwidth often matters
```

## Learner should reject

- parameter count alone describes model execution;
- attention is the whole decoder block;
- prefill/decode use different model weights;
- decode recomputes the prompt every step;
- KV stores Q/K/V;
- full conceptual attention score must be materialized;
- PP and TG should scale identically;
- logits are already text.
