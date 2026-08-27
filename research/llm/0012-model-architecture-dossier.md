# Research Note 0023 — Model Architecture Dossier: Config → Memory → Performance Hypotheses

日期：2026-08-27

## Goal

Turn a real model `config.json` into a hardware-facing dossier without pretending a formula is a benchmark.

The dossier integrates Slices 24–28:

```
decoder dimensions
→ attention head structure
→ KV cache
→ dense FFN
→ MoE if present
→ weight-storage proxy
→ lower-bound capacity planning
→ PP/TG hypotheses
→ questions that require real runtime evidence
```

This is the model-side counterpart to the hardware candidate dossier.

---

# Part I — Identity first

Record:

- model repository;
- revision/commit;
- config source/hash;
- architecture/model_type;
- exact inference artifact when available;
- GGUF filename/bytes/SHA256 when available.

A config from one model revision must not be silently paired with a different quantized artifact.

---

# Part II — Structural fields

At minimum inspect:

```
hidden_size
num_hidden_layers
num_attention_heads
num_key_value_heads
head_dim
intermediate_size
vocab_size
max_position_embeddings
rope_theta / rope_scaling
sliding_window / layer_types
```

MoE may add:

```
num_local_experts / n_routed_experts
num_experts_per_tok
n_shared_experts
moe_intermediate_size
first_k_dense_replace
moe_layer_freq
```

Field names are architecture-specific.

---

# Part III — KV baseline

For a homogeneous attention baseline:

```
KV bytes/token
=
2 × L × Hkv × Dh × bytes_per_KV_element
```

Then:

```
KV total
=
KV bytes/token
× context
× active sequences
```

This is not exact for:
- sliding/local attention;
- hybrid layer types;
- compressed/latent KV;
- per-layer head differences;
- backend padding/layout.

If those exist, the dossier must mark the homogeneous estimate as incomplete.

---

# Part IV — Weight storage proxy

If total parameter count P and effective weight bits b are known:

```
weight storage proxy
=
P × b/8
```

This is useful planning scale.

It is not:
- exact GGUF file size;
- exact runtime VRAM;
- proof of native low-bit compute.

Prefer actual artifact bytes when the exact GGUF exists.

---

# Part V — Dense block structure

Attention projection baseline:

```
q_width = Hq × Dh
kv_width = Hkv × Dh

P_attn
≈
d×q_width
+ 2d×kv_width
+ q_width×d
```

Common gated dense FFN baseline:

```
P_ffn
≈
3 d d_ff
```

This tells the learner where dense weights are concentrated.

---

# Part VI — MoE structure

For a common SwiGLU-like expert:

```
P_expert
≈
3 d d_e
```

Then distinguish:

```
total routed experts/layer
active routed experts/token/layer
shared experts
```

Do not multiply across all layers unless the layer pattern is known.

---

# Part VII — Capacity lower bound

A useful planning lower bound is:

```
lower_bound
=
actual artifact bytes OR weight proxy
+
KV baseline
+
explicit reserve
```

This deliberately excludes unknown runtime overhead.

Therefore capacity verdicts are asymmetric:

### If lower_bound > usable memory

```
FAIL-WITHOUT-OFFLOAD
```

The workload cannot fully fit under the stated assumptions.

### If lower_bound <= usable memory

```
POSSIBLE-NOT-PROVEN
```

Never call this PASS from formulas alone.

Real runtime must still prove:
- backend allocations;
- workspace;
- KV layout;
- offload split;
- fragmentation/headroom.

---

# Part VIII — Architecture can suggest hypotheses, not benchmark results

## Dense model / fully resident

Possible TG hypothesis:

```
large weight matrices
→ repeated one-token weight use
→ memory bandwidth may dominate
```

## Large Hkv / long context

Possible hypothesis:

```
KV capacity/traffic may become material
```

## GQA/MQA

Possible hypothesis:

```
KV pressure lower than same-Hq MHA baseline
```

## MoE

Possible hypothesis:

```
active compute < total params
but resident/offload/expert routing can dominate local inference
```

## Large prompt

Possible PP hypothesis:

```
large GEMMs / attention kernels / matrix units matter
```

These are experiment-design hypotheses only.

---

# Part IX — Dossier output

A useful dossier ends with three sections:

## Known

Facts directly supported by config/artifact.

## Derived

Transparent formula outputs.

## Unknown / must measure

Examples:
- actual VRAM;
- PP/TG;
- backend support;
- real attention kernel;
- MoE expert batching;
- power/thermal behavior.

This evidence separation prevents config inspection from becoming fake benchmarking.

---

# Part X — Bridge to hardware selection

Once the model dossier exists, pair it with Slice 18 hardware dossier:

```
MODEL:
weight/KV/layer structure
+
HARDWARE:
capacity/bandwidth/software support
=
candidate experiment
```

Then use Slice 22:

```
baseline
→ diagnose
→ one-variable A/B
```

---

# Claims to avoid

- "weight proxy = runtime VRAM";
- "fits by formula = confirmed fit";
- "config determines actual tokens/s";
- "same Hkv implies same KV runtime allocation";
- "total parameters are enough to compare local inference";
- "active MoE parameters are enough to size VRAM";
- "architecture bottleneck hypothesis is a benchmark result".
