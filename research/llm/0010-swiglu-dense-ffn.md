# Research Note 0021 — SwiGLU / Dense FFN: The Other Big Weight Path

日期：2026-08-27

## Research question

Attention gets most of the attention.

But in a dense decoder block, the feed-forward network can contain **more weights than the attention projections** and can therefore contribute a very large fraction of:
- model file size;
- runtime weight memory;
- per-token decode weight traffic.

This slice answers:

1. What is a classic Transformer FFN?
2. What changes when modern LLMs use SwiGLU?
3. Why are there gate / up / down matrices?
4. Why does `intermediate_size` matter?
5. Why can FFN weight traffic dominate decode even though it has no KV cache?
6. Why do prefill and decode stress the same FFN weights differently?

---

# Primary sources

## GLU Variants Improve Transformer

Noam Shazeer, 2020:
https://arxiv.org/abs/2002.05202

The paper evaluates GLU variants in Transformer feed-forward sublayers and defines SwiGLU using a Swish/SiLU-style gated branch multiplied elementwise by a second projection.

A GLU-style FFN has three large matrices rather than the classic two-matrix FFN.

## LLaMA

https://arxiv.org/abs/2302.13971

LLaMA adopts SwiGLU in place of ReLU and describes using an intermediate dimension of roughly:

```
(2/3) × 4d
=
8d/3
```

rather than the classic Transformer `4d` baseline.

Exact `intermediate_size` is model-specific and commonly rounded for implementation constraints. Always read the actual config.

---

# Part I — Classic dense Transformer FFN

A simple two-layer FFN:

```
x [M,d]
→ W1 [d,d_ff]
→ activation
→ W2 [d_ff,d]
→ y [M,d]
```

where:
- d = hidden size;
- d_ff = intermediate size;
- M = number of token rows processed together.

Ignoring bias:

```
params
=
d × d_ff
+
d_ff × d
=
2 d d_ff
```

The original Transformer commonly used an FFN expansion around:

```
d_ff ≈ 4d
```

but modern model families choose their own dimensions.

---

# Part II — SwiGLU adds a gate branch

A common SwiGLU-style formulation:

```
gate = x W_gate
up   = x W_up

z
=
SiLU(gate)
⊙
up

y
=
z W_down
```

Shapes:

```
W_gate [d,d_ff]
W_up   [d,d_ff]
W_down [d_ff,d]
```

So ignoring bias:

```
params
≈
3 d d_ff
```

This is the key structural difference from the classic two-matrix FFN.

---

# Part III — What SiLU / Swish does

For the common beta=1 form:

```
SiLU(x)
=
x × sigmoid(x)
```

The gate branch is nonlinear.

The up branch remains a learned linear projection.

Then:

```
SiLU(gate)
⊙
up
```

multiplies them elementwise.

This is **dense gating**.

It is not:
- expert routing;
- sparse MoE;
- selecting only a few neurons from storage.

Both large gate/up projections are still computed in the ordinary dense SwiGLU block.

---

# Part IV — Why LLaMA reduces d_ff relative to 4d

If you naively kept:

```
d_ff = 4d
```

while changing from two matrices to three, FFN parameter count would rise from:

```
2d(4d) = 8d²
```

to:

```
3d(4d) = 12d²
```

The GLU-variant work discusses reducing the hidden FFN width by 2/3 to compare under similar parameter/compute budgets.

LLaMA similarly describes:

```
d_ff ≈ (2/3) × 4d
```

For the idealized value:

```
3d × (8d/3)
=
8d²
```

which restores the same rough dense-FFN parameter order as a two-matrix `4d` FFN.

This is a design-budget intuition, not a rule that every SwiGLU model must use exactly `8d/3`.

---

# Part V — Concrete LLaMA-like dense example

Use:

```
d = 4096
d_ff = 11008
```

Then:

```
FFN params/layer
=
3 × 4096 × 11008
=
135,266,304
```

Now compare a classic 32-head MHA projection baseline:

```
Hq = Hkv = 32
Dh = 128
q_width = kv_width = 4096
```

Q/K/V/O attention projections:

```
4 × 4096 × 4096
=
67,108,864
```

Therefore:

```
FFN / attention-projection weights
≈
2.016×
```

So in this example, the FFN has roughly twice as many projection weights as self-attention.

Important:
- this excludes embeddings/norms;
- it excludes architecture-specific details;
- GQA changes attention K/V projection size;
- not every model uses the same `d_ff`.

---

# Part VI — Weight bytes are the decode story

For the example FFN:

```
135,266,304 weights/layer
```

Storage baseline:

## FP16

```
× 2 bytes
=
270,532,608 bytes
≈
258 MiB/layer
```

## Effective 4.5 bpw

```
× 4.5/8 bytes
≈
76,087,296 bytes
≈
72.56 MiB/layer
```

This is why quantization strongly changes local-LLM decode economics.

During autoregressive decode, these large matrices are used again for every generated token.

If the workload cannot reuse enough of the weight data from cache:

```
large FFN weights
→ repeated memory traffic
→ bandwidth pressure
```

Attention is not the only source of decode memory traffic.

---

# Part VII — Prefill FFN shape

Let prompt/token rows:

```
M = B × T
```

Then:

```
X [M,d]

gate:
[M,d] × [d,d_ff]
→ [M,d_ff]

up:
[M,d] × [d,d_ff]
→ [M,d_ff]

down:
[M,d_ff] × [d_ff,d]
→ [M,d]
```

For:

```
T = 512
B = 1
```

the same weight matrices serve 512 token rows in one large GEMM regime.

This creates much more compute per weight byte than a one-token decode call.

---

# Part VIII — Decode FFN shape

For one sequence and one new token:

```
M = 1
```

The shapes become:

```
[1,d] × [d,d_ff]
[1,d] × [d,d_ff]
[1,d_ff] × [d_ff,d]
```

The weight matrices are unchanged.

Only the number of useful token rows collapsed.

That lowers arithmetic intensity and makes bandwidth/launch/dequant overhead comparatively more important.

This is the same PP-vs-TG shape transition taught in Slice 24, now applied specifically to the MLP.

---

# Part IX — Weight-only arithmetic-intensity intuition

Ignoring:
- activation reads/writes;
- cache effects;
- dequant metadata;
- kernel overhead;

three SwiGLU matrices do roughly:

```
≈ 6 M d d_ff FLOPs
```

if one multiply-add is counted as 2 FLOPs.

Weight storage at `b` bits/weight is:

```
3 d d_ff × b/8 bytes
```

So a weight-only arithmetic-intensity proxy is:

```
AI_weight
≈
16M / b
FLOP/byte
```

For FP16:

```
AI_weight
≈ M FLOP/byte
```

Thus:
- decode M=1 → roughly 1 FLOP/weight-byte baseline;
- prefill M=512 → roughly 512 FLOP/weight-byte baseline.

This is only a teaching roof proxy, not a measured kernel AI.

It explains why the same FFN can be:
- bandwidth-sensitive in TG;
- compute-efficient in PP.

---

# Part X — Elementwise gate work is smaller but not free

After gate/up GEMMs:

```
SiLU(gate) ⊙ up
```

is O(M × d_ff) elementwise work.

Compared with the O(M × d × d_ff) dense projections, it has far fewer arithmetic operations.

But it still:
- touches intermediate activation memory;
- creates a kernel/fusion opportunity;
- can contribute launch/latency overhead.

Good backends may fuse activation/gating operations with neighboring kernels.

---

# Part XI — Quantization affects FFN heavily

Because dense FFN weights are often a large share of total model weights:

```
lower effective bpw
→ much smaller FFN storage/traffic
```

But Slice 06/13 still applies:

```
Q4 file/storage
!=
native 4-bit matrix instruction automatically
```

The backend may:
- dequantize blocks;
- use mixed-precision matrix kernels;
- fuse scaling;
- choose GEMM/GEMV variants.

So quantization changes both:
- bytes;
- kernel behavior.

---

# Part XII — Why attention optimization is not whole-model optimization

Suppose FlashAttention makes the attention portion faster.

The model still executes:
- RMSNorm/residual;
- Q/K/V/O projections;
- dense FFN gate/up/down;
- LM head;
- other model-specific operations.

If FFN weight streaming dominates TG:

```
attention kernel improvement
→ may strongly improve PP
→ may barely move TG
```

That is exactly the type of Capstone result Slice 22 teaches learners to interpret.

---

# Part XIII — intermediate_size is a first-class config field

Before estimating a model, inspect:

```
hidden_size
intermediate_size
num_hidden_layers
num_attention_heads
num_key_value_heads
head_dim
hidden_act
```

Do not infer FFN width from:
- parameter-count label;
- hidden size alone;
- “uses SwiGLU”.

Modern models may use different expansion ratios or per-layer structures.

---

# Part XIV — Bias / parallel / fused variants

Some architectures:
- include bias;
- omit bias;
- use parallel attention/MLP arrangements;
- fuse projections;
- use different gated activations;
- use MoE instead of one dense FFN.

Therefore:

```
3 d d_ff
```

is a useful baseline for common dense gated FFNs, not a universal model parser.

Real config/model code remains authoritative.

---

# Claims to avoid

- "attention contains most model weights";
- "SwiGLU is sparse expert routing";
- "SwiGLU always uses exactly 4d or exactly 8d/3";
- "three FFN matrices means 50% more full-model parameters";
- "quantized FFN weights automatically execute as native low-bit matrix ops";
- "FlashAttention optimizes the FFN";
- "small SiLU parameter count means zero runtime overhead";
- "same parameter count means same FFN width";
- "decode and prefill use different FFN weights".
