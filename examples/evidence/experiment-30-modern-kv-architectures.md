# Evidence — Experiment 30: Sliding / Hybrid / Latent KV Architectures

状态：stable modern-KV lesson complete; hybrid/local arithmetic verified; real architecture inspector ready.

## Claim

> The homogeneous full-attention KV formula is exact only under its architectural assumptions. Modern models may reduce cached positions per layer, mix local/global layers, or compress the cached state width itself.

## Primary evidence

### Mistral 7B
https://arxiv.org/abs/2310.06825

Uses GQA with Sliding Window Attention to reduce inference cost.

### Gemma 2
https://arxiv.org/abs/2408.00118

Uses interleaved local-global attention, demonstrating a hybrid layer pattern.

### DeepSeek-V2
https://arxiv.org/abs/2405.04434

Introduces Multi-head Latent Attention and reports substantial KV-cache reduction by storing a compressed latent representation.

## General cache model

```
cache bytes
=
Σ_l
(
cached positions_l
× cached state width_l
× bytes/element
)
```

Ordinary full attention:

```
positions_l = S
state width_l = 2 × Hkv × Dh
```

Confirmed local layer:

```
positions_l ≈ min(S,W)
```

## Experiment 54 verification

Default:

```
L=32
full layers=8
local layers=24
W=4096
Hkv=8
Dh=128
FP16
```

Verified at 32k:

```
all-full  = 4.000 GiB
all-local = 0.500 GiB
hybrid    = 1.375 GiB
hybrid/full = 0.34375
```

Verified at 128k:

```
all-full  = 16.000 GiB
all-local = 0.500 GiB
hybrid    = 4.375 GiB
hybrid/full = 0.2734375
```

## Direct window vs effective context

The course explicitly separates:

```
direct attention window
effective information propagation
KV cache size
```

A local layer only directly reads W positions, but information can propagate across layers and hybrid architectures can periodically use global/full attention.

## MLA boundary

For DeepSeek-style MLA, relevant config fields can include:

```
kv_lora_rank
qk_rope_head_dim
```

The course allows a model-specific cached-width proxy using those dimensions only with explicit confirmation of the exact DeepSeek-style architecture.

It is never presented as a universal MLA formula.

## Experiment 55

The real inspector:
- prints full-attention baseline;
- does not assume every layer is sliding from one field;
- can derive a hybrid sum from explicit classifiable `layer_types`;
- requires explicit opt-in for all-sliding or DeepSeek-style MLA proxies.

UNKNOWN is an allowed and preferred result when evidence is insufficient.

## Performance consequence

Sliding/local:
- reduces positions cached/read.

Latent/compressed KV:
- reduces cached state width.

Neither automatically removes:
- FFN weight traffic;
- other dense projection traffic;
- runtime/kernel overhead.

## Learner should reject

- sliding window means the whole model remembers only W tokens;
- one sliding_window field proves all layers are local;
- local attention makes whole-model memory constant;
- MLA = GQA;
- compressed KV has no compute tradeoff;
- one DeepSeek field formula applies to all latent-attention models.
