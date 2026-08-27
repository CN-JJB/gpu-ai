# Research Note 0020 — MHA / MQA / GQA: Query Heads vs KV Heads

日期：2026-08-27

## Research question

Why can two models with similar total parameter counts have radically different KV-cache cost and incremental-decoding behavior?

Because:

```
query heads
and
key/value heads
do not have to be the same count
```

The important symbols are:

- Hq = query heads
- Hkv = key/value heads
- Dh = head dimension
- d = hidden size
- L = layers

This slice derives:
- projection widths;
- attention parameter counts;
- grouping;
- KV bytes/token;
- decode memory-traffic consequences.

---

# Primary sources

## Multi-Head Attention

Transformer:
https://arxiv.org/abs/1706.03762

Classic MHA uses multiple Q/K/V heads in parallel.

## Multi-Query Attention

Shazeer, 2019:
https://arxiv.org/abs/1911.02150

MQA shares one set of K/V heads across multiple query heads.

The paper motivates this for incremental decoding:
- KV tensors are repeatedly read;
- sharing K/V reduces cache size and memory-bandwidth cost.

## Grouped-Query Attention

Ainslie et al., 2023:
https://arxiv.org/abs/2305.13245

GQA uses:
```
1 < Hkv < Hq
```

so groups of query heads share K/V heads.

It aims to preserve quality closer to MHA while retaining much of MQA's decoding efficiency.

## Llama 2 production example

https://arxiv.org/abs/2307.09288

Llama 2 explicitly describes using GQA to improve inference scalability in relevant larger variants.

---

# Part I — Query heads answer different questions

Start with hidden state:

```
X [B,T,d]
```

Q projection:

```
Q [B,Hq,T,Dh]
```

Usually:
```
Hq × Dh ≈ d
```

Each query head has its own projected query subspace.

---

# Part II — MHA

Classic multi-head attention:

```
Hkv = Hq
```

Shapes:

```
Q [B,Hq,T,Dh]
K [B,Hq,T,Dh]
V [B,Hq,T,Dh]
```

Each query head has its own K/V head.

If:
```
Hq = 32
```

then:
```
Hkv = 32
```

in the simple MHA case.

---

# Part III — MQA

Multi-query attention:

```
Hkv = 1
```

while:

```
Hq can still be 32, 40, 64...
```

Example:

```
32 query heads
share
1 K head
1 V head
```

Conceptual grouping:

```
Q0 ┐
Q1 │
...├─→ same K/V
Q31┘
```

This dramatically reduces:
- K/V projection output width;
- KV-cache storage;
- historical K/V read traffic during decode.

---

# Part IV — GQA

Grouped-query attention is the intermediate case.

Example:

```
Hq = 32
Hkv = 8
```

Then:

```
group size
=
Hq / Hkv
=
4
```

So every K/V head serves four query heads.

Conceptually:

```
Q0 Q1 Q2 Q3   → KV0
Q4 Q5 Q6 Q7   → KV1
...
Q28..Q31      → KV7
```

The backend may broadcast/index K/V logically.

It does not have to physically duplicate the entire KV cache to Hq heads.

---

# Part V — Projection widths

Let:

```
d = hidden size
Dh = head_dim
```

Q output width:

```
q_width = Hq × Dh
```

KV output width:

```
kv_width = Hkv × Dh
```

Typical projection matrices:

```
Wq: d → q_width
Wk: d → kv_width
Wv: d → kv_width
Wo: q_width → d
```

Ignoring bias:

```
attention params/layer
≈
d×q_width
+
2d×kv_width
+
q_width×d
```

If:
```
q_width = d
```

then:

```
≈ 2d² + 2d×kv_width
```

Reducing Hkv lowers K/V projection parameters, but Q/O remain large.

So GQA/MQA can reduce attention parameters without shrinking the whole model proportionally.

The MLP may still dominate a large fraction of total parameters.

---

# Part VI — KV cache depends on Hkv, not Hq

Per token across all layers:

```
KV bytes/token
=
2
× L
× Hkv
× Dh
× bytes_per_element
```

Important:

```
Hq
does not appear directly
```

because the cache stores K/V heads.

This is one of the most useful model-config facts for local inference.

---

# Part VII — Concrete 32-layer example

Use:

```
L = 32
Hq = 32
Dh = 128
FP16 KV = 2 bytes
d = 4096
```

## MHA

```
Hkv = 32
```

KV bytes/token:

```
2 × 32 × 32 × 128 × 2
=
524,288 bytes
=
512 KiB/token
```

## GQA-8

```
Hkv = 8
```

```
131,072 bytes
=
128 KiB/token
```

## MQA

```
Hkv = 1
```

```
16,384 bytes
=
16 KiB/token
```

---

# Part VIII — Context capacity consequence

At:

```
32,768 tokens
```

single-sequence FP16 KV baseline:

## MHA

```
512 KiB × 32768
=
16 GiB
```

## GQA-8

```
128 KiB × 32768
=
4 GiB
```

## MQA

```
16 KiB × 32768
=
0.5 GiB
```

Same:
- layer count;
- query-head count;
- head dimension.

Only Hkv changed.

This is why Hkv matters so much for:
- long context;
- concurrency;
- serving slots;
- local VRAM budgets.

---

# Part IX — Projection-parameter consequence

Same example:

```
d = 4096
Hq = 32
Dh = 128
q_width = 4096
```

## MHA

```
kv_width = 4096

Wq  = 4096×4096
Wk  = 4096×4096
Wv  = 4096×4096
Wo  = 4096×4096
```

Total:

```
67,108,864 weights/layer
```

## GQA-8

```
kv_width = 1024
```

Total:

```
41,943,040 weights/layer
```

## MQA

```
kv_width = 128
```

Total:

```
34,603,008 weights/layer
```

This is meaningful, but do not infer full-model parameter count from attention alone.

---

# Part X — Decode bandwidth consequence

During one-token decode, the current query attends over cached K/V from S historical tokens.

Historical cache read size is roughly proportional to:

```
Hkv × Dh × S
```

Reducing Hkv:
- reduces stored KV;
- reduces K/V memory traffic;
- improves serving capacity;
- can reduce incremental decode memory-bandwidth pressure.

This is exactly the motivation emphasized by the MQA paper.

---

# Part XI — Prefill is a different tradeoff

During prefill:
- K/V are generated for many new tokens;
- attention does large matrix work;
- compute and attention-kernel efficiency matter heavily.

GQA still reduces K/V projection width and cache writes.

But the dramatic user-visible benefit is often most obvious in:
- incremental decode;
- long context;
- concurrency.

Do not assume a 4× smaller KV means 4× PP or TG.

---

# Part XII — Quality tradeoff

Why not always use one KV head?

Model quality/capacity can benefit from having more independent K/V representations.

MQA paper reports strong decoding benefits with a possible quality tradeoff.

GQA explicitly targets the middle ground:
- more than one KV head;
- fewer than query heads;
- quality closer to MHA;
- efficiency closer to MQA.

This is a model-design decision.

You cannot convert an already trained MHA model to GQA at inference by simply dropping KV heads.

The weights and training/uptraining strategy matter.

---

# Part XIII — Group mapping must be valid

Common GQA:

```
Hq % Hkv == 0
```

so query heads divide evenly into groups.

But model implementations can have architecture-specific details.

Always read exact config/runtime metadata.

Do not blindly assume:
```
group_size = Hq/Hkv
```
if the architecture exposes unusual head mapping.

---

# Part XIV — KV quant and Hkv multiply together

Suppose GQA already reduces Hkv.

Then lower KV precision can reduce cache further:

```
KV bytes
∝
Hkv
×
bits_per_KV_element
```

So:

```
GQA
+
quantized KV
```

can combine.

But they are different layers:

- GQA: trained architecture.
- KV quant: runtime numerical representation.

Do not confuse them.

---

# Part XV — Total params vs active memory traffic

A model can have:
- similar total parameter count;
- much smaller Hkv.

Then:
- weight storage may remain similar;
- KV capacity changes dramatically.

This means:

```
parameter count
!=
context/concurrency cost
```

Two 8B-class models can have very different practical long-context VRAM usage.

---

# Part XVI — Buyer / deployment consequence

Before choosing a local LLM, record:

```
num_hidden_layers
num_attention_heads
num_key_value_heads
head_dim
KV datatype
target context
concurrency
```

Then calculate KV.

Do not choose only by:

```
7B / 14B / 32B
```

or:

```
Q4 file size
```

because those do not define runtime KV.

---

# Claims to avoid

- "number of query heads determines KV size";
- "MHA/MQA/GQA are runtime flags";
- "MQA means one attention head";
- "GQA physically duplicates KV for every query head";
- "4× fewer KV heads means 4× faster generation";
- "GQA only changes KV cache, not projection weights";
- "KV quant and GQA are the same technique";
- "two same-parameter models have the same context memory";
- "every architecture has evenly divisible Hq/Hkv mapping".
