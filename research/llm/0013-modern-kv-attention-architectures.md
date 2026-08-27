# Research Note 0024 — Sliding / Hybrid Attention and Compressed KV Families

日期：2026-08-27

## Research question

The earlier homogeneous KV baseline assumed:

```
every layer
caches
every token
with ordinary K/V heads
```

Modern models can violate every part of that assumption.

This slice introduces three architecture families:

1. full-context attention;
2. sliding/local attention and hybrid full+local layers;
3. compressed/latent KV attention such as DeepSeek-style MLA.

The goal is not to teach one universal replacement formula.

The goal is to know when:

```
2 × L × Hkv × Dh × bytes × context
```

is only a rough upper/model baseline rather than the exact runtime KV cache.

---

# Primary sources

## Mistral 7B

https://arxiv.org/abs/2310.06825

Mistral combines:
- Grouped-Query Attention;
- Sliding Window Attention.

The sliding window reduces attention/cache cost by limiting direct attention to a recent window.

## Gemma 2

https://arxiv.org/abs/2408.00118

Gemma 2 is a concrete hybrid example using interleaved local-global attention rather than one identical attention pattern in every layer.

## DeepSeek-V2

https://arxiv.org/abs/2405.04434

DeepSeek-V2 introduces Multi-head Latent Attention (MLA), which compresses the KV state into a low-dimensional latent representation for inference.

The report attributes a major KV-cache reduction to MLA.

---

# Part I — Full attention baseline

Let:

- S = cached sequence length;
- L = number of attention layers;
- Hkv = KV heads;
- Dh = head dimension;
- b = bytes per KV element.

For ordinary homogeneous full attention:

```
KV_full
=
2 × L × Hkv × Dh × b × S
```

For active sequences:

```
× sequence_count
```

Every layer retains K/V state for all S positions.

---

# Part II — Sliding/local attention

Define a causal local window W as:

> at most W cached historical/current positions directly available to that layer's attention kernel.

Then after the sequence grows beyond W:

```
cached positions/layer
≈
min(S, W)
```

So a homogeneous local-attention KV baseline becomes:

```
KV_local
≈
2 × L × Hkv × Dh × b × min(S,W)
```

This can stop growing linearly with total sequence length once:

```
S > W
```

provided the runtime actually uses a rolling/local cache matching the model architecture.

Do not assume every backend does this equally efficiently.

---

# Part III — Sliding window does not mean "the model remembers only W tokens"

A single local layer directly attends only within its window.

But a token representation at an earlier layer can already contain information propagated from older positions.

Across stacked local layers, information can move through the network beyond one direct window.

Hybrid models can also periodically use global/full layers.

Therefore distinguish:

```
direct attention span
!=
effective information propagation
!=
KV cache size
```

---

# Part IV — Hybrid full + local layers

Suppose:

- F layers use full attention;
- R layers use local/sliding attention;
- L = F + R;
- all share the same Hkv/Dh for this teaching baseline.

Then:

```
KV_hybrid
≈
2 × Hkv × Dh × b
×
[
F × S
+
R × min(S,W)
]
```

This is one of the most useful corrections to the homogeneous formula.

The full layers still grow with total context.
The local layers saturate at W.

---

# Part V — Concrete hybrid example

Use:

```
L = 32
F = 8 full layers
R = 24 local layers
W = 4096
Hkv = 8
Dh = 128
FP16
S = 32768
```

Per cached position/layer:

```
2 × 8 × 128 × 2
=
4096 bytes
=
4 KiB
```

## All full

```
32 × 32768 × 4 KiB
=
4 GiB
```

## All local, W=4096

```
32 × 4096 × 4 KiB
=
0.5 GiB
```

## Hybrid 8 full + 24 local

```
[
8×32768
+
24×4096
]
× 4 KiB

=
1.375 GiB
```

So the homogeneous 4 GiB estimate would overstate this teaching hybrid layout by almost 3×.

But actual model/backend layout must still be inspected.

---

# Part VI — What happens at 128k context?

Same model:

```
S = 131072
```

## All full

```
16 GiB
```

## All local

Still:

```
0.5 GiB
```

because each local layer keeps only W=4096 positions in the teaching model.

## Hybrid

```
8 full layers continue growing
+
24 local layers remain capped
```

Result:

```
4.375 GiB
```

This shows why long-context architecture cannot be inferred from the maximum context number alone.

---

# Part VII — Compute changes too

For prefill length T:

## Full attention

Conceptual attention score work:

```
O(T²)
```

per full layer.

## Sliding/local attention

Conceptually:

```
O(TW)
```

once T is much larger than W.

Actual optimized kernels may tile/fuse and should not be reduced to one raw score-matrix allocation.

The complexity distinction still explains why local attention can improve long-prompt scaling.

---

# Part VIII — Decode read traffic

At one-token decode step:

## Full layer

Attention reads history up to:

```
S
```

positions.

## Local layer

Attention reads at most:

```
W
```

positions.

So local attention reduces not only KV capacity but also attention-side historical read traffic during decode.

It does not reduce:
- model FFN weight traffic;
- all dense projection weights;
- LM head.

Therefore TG may remain weight-bandwidth-bound even with tiny local KV.

---

# Part IX — Hybrid attention implementation details matter

A config may expose:
- `sliding_window`;
- `layer_types`;
- `attention_pattern`;
- alternating/global-layer metadata.

Do not infer:
```
all layers are sliding
```
from a single `sliding_window` field unless the architecture documentation says so.

Some model families:
- alternate local/global;
- use periodic global layers;
- use different window sizes across layers.

The safe general formula is a per-layer sum:

```
KV
=
Σ_l
[
cached_width_l
× cached_positions_l
× bytes
]
```

---

# Part X — Compressed / latent KV

Some architectures do not cache ordinary full K/V head tensors at all.

DeepSeek-V2 MLA is an important example.

Conceptually:

```
hidden state
→ low-rank compressed KV latent
→ reconstruct/project key/value information as needed
```

The cache stores a compact latent state rather than:

```
Hkv × Dh K
+
Hkv × Dh V
```

for every token.

This changes the memory-vs-compute tradeoff.

---

# Part XI — DeepSeek-style MLA cache concept

A useful **architecture-specific** mental model is:

```
cached state/token/layer
≈
compressed KV latent
+
position/RoPE-specific cached component
```

Common DeepSeek configs expose fields such as:

```
kv_lora_rank
qk_rope_head_dim
```

A teaching proxy for that family can be:

```
cached elements/token/layer
≈
kv_lora_rank
+
qk_rope_head_dim
```

only when the exact model/runtime architecture matches the DeepSeek MLA formulation.

Do **not** use this as a universal MLA formula.

---

# Part XII — Why compression can trade memory for compute

Ordinary attention caches wider K/V states.

A latent scheme stores less state, then uses projection/reconstruction work around attention.

So the architecture can move along:

```
less memory traffic
↔
more projection/compute work
```

This is relevant on GPUs where decode is often bandwidth-limited.

A hardware-centric study is not needed to accept the core principle:
DeepSeek-V2 itself explicitly designs MLA for lower KV-cache cost and efficient inference.

Actual kernel performance remains a runtime question.

---

# Part XIII — Local attention and MLA solve different problems

Sliding/local attention:

```
reduce number of cached/read positions
```

MLA/compressed KV:

```
reduce width/state stored per cached position
```

These axes can be written generically as:

```
KV bytes
≈
Σ layers
(
cached positions
× cached state width
× bytes
)
```

This is the most general mental model in the course.

---

# Part XIV — Why the old formula is still useful

The homogeneous formula:

```
2 × L × Hkv × Dh × bytes × S
```

remains excellent for:
- ordinary MHA/GQA/MQA full-attention models;
- first-pass comparison;
- sanity checking.

The correct behavior is not to discard it.

It is to ask:

```
Does this model actually satisfy those assumptions?
```

---

# Part XV — Dossier consequence

When building a Model Dossier:

### Ordinary full attention
Use the standard KV formula.

### Confirmed all-layer sliding attention
Use:
```
min(S,W)
```
per local layer.

### Confirmed hybrid
Sum full/local layer contributions.

### Compressed/latent KV
Use model-specific cache-state dimensions.

### Unknown pattern
Mark:

```
KV EXACTNESS = UNKNOWN
```

Do not invent a number.

---

# Claims to avoid

- "sliding window means the model cannot use information older than W.";
- "sliding_window in config means every layer is local.";
- "local attention makes total model memory constant.";
- "hybrid attention KV is just full-attention KV divided by the local/full ratio.";
- "MLA is the same as GQA.";
- "MLA only changes KV cache and has no compute tradeoff.";
- "kv_lora_rank + qk_rope_head_dim is a universal compressed-KV formula.";
- "maximum context length directly determines KV without layer-pattern knowledge.";
