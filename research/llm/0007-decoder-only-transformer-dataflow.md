# Research Note 0018 — Decoder-only Transformer Dataflow: Prefill vs Decode

日期：2026-08-27

## Research question

为什么同一个 decoder-only Transformer：

```
处理一段 prompt
```

和：

```
逐 token 生成
```

会表现成两种完全不同的硬件工作负载？

答案不是“它用了两个模型”。

是同一组 block 在不同 tensor shape / cache state 下执行。

本节先建立稳定的数据流骨架：

```
token ids
→ embedding
→ repeated decoder blocks
   → norm
   → self-attention
   → residual
   → norm
   → gated MLP
   → residual
→ final norm
→ LM head
→ logits
→ sampler
```

然后区分：

```
prefill: many new tokens at once
decode: one/few new token(s) + historical KV
```

---

# Primary sources

## Transformer

Vaswani et al., 2017:
https://arxiv.org/abs/1706.03762

Stable ideas:
- attention-based sequence model;
- multi-head attention;
- feed-forward sublayer;
- residual path;
- normalization.

The original paper is encoder-decoder and not identical to modern Llama-style decoder-only blocks, but it establishes the core attention/FFN structure.

## Modern decoder-only Llama lineage

LLaMA:
https://arxiv.org/abs/2302.13971

Llama 2:
https://arxiv.org/abs/2307.09288

Llama 3:
https://arxiv.org/abs/2407.21783

Modern Llama-family models provide concrete examples of:
- decoder-only autoregressive Transformer;
- RMSNorm;
- RoPE;
- SwiGLU-style gated FFN;
- GQA in later variants.

This course uses those mechanisms as examples, not as a claim that every LLM has identical architecture.

---

# Part I — Token ids are not model vectors yet

Tokenizer outputs integer token IDs.

Example:

```
[1, 923, 42, 7811]
```

An embedding table maps each token ID to a learned vector:

```
E ∈ R^(vocab_size × d_model)
```

For batch B and token count T:

```
token ids: [B, T]
embedding output X: [B, T, d_model]
```

The Transformer block works on these hidden vectors.

## Embedding parameter count

Ignoring special sharing/tied-output details:

```
embedding params
≈ vocab_size × d_model
```

This is one reason larger vocabulary can materially increase model parameter count.

---

# Part II — One modern pre-norm decoder block

A simplified Llama-like block:

```
x
│
├─ RMSNorm
│    ↓
│  Attention
│    ↓
├─ + residual ─────────→ h
│
├─ RMSNorm
│    ↓
│  SwiGLU / gated MLP
│    ↓
└─ + residual ─────────→ y
```

Stable conceptual equation:

```
h = x + Attention(Norm(x))
y = h + MLP(Norm(h))
```

Exact ordering can vary by model family.

Do not freeze this as a universal Transformer law.

---

# Part III — Attention projection shapes

Let:

- B = batch
- T = number of new/query tokens in this call
- d = hidden size
- Hq = number of query heads
- Hkv = number of key/value heads
- Dh = head dimension

Commonly:

```
Hq × Dh = d
```

but some modern models expose `head_dim` explicitly, so always read the actual config.

Input:

```
X: [B, T, d]
```

Projection outputs:

```
Q: [B, Hq, T, Dh]
K: [B, Hkv, T, Dh]
V: [B, Hkv, T, Dh]
```

If Hkv = Hq:
```
MHA
```

If Hkv = 1:
```
MQA
```

If:
```
1 < Hkv < Hq
```

typically:
```
GQA
```

Detailed tradeoffs are the next attention-head slice.

---

# Part IV — Conceptual attention matrix

For self-attention:

```
score = Q K^T / sqrt(Dh)
```

Conceptually, for prompt length T:

```
scores: [B, Hq, T, T]
```

Causal masking prevents position i from attending to future positions.

Then:

```
P = softmax(scores)
O = P V
```

The head outputs are merged/projected back to hidden size.

Important:

```
conceptual T×T score matrix
!= runtime must materialize full T×T matrix
```

FlashAttention-style kernels deliberately avoid writing the full intermediate to high-cost memory.

That connects directly to Slice 12.

---

# Part V — Prefill

Suppose the prompt has T tokens.

The first model pass can process many prompt positions in parallel:

```
X: [B, T, d]
Q: [B, Hq, T, Dh]
K/V new: [B, Hkv, T, Dh]
```

Attention conceptually handles:

```
T queries × T keys
```

Matrix operations are relatively large.

This increases:
- arithmetic intensity;
- GEMM utilization;
- opportunities to use matrix units;
- opportunity for FlashAttention tiling.

So PP is often more compute/kernel sensitive than TG.

This is why a GPU with excellent matrix throughput can show a very high PP score.

---

# Part VI — KV cache creation during prefill

The prompt's keys and values are stored for future autoregressive generation.

Per layer:

```
K cache: [B, Hkv, context, Dh]
V cache: [B, Hkv, context, Dh]
```

Approximate bytes per cached token across all layers:

```
KV bytes/token
=
2
× n_layers
× Hkv
× Dh
× bytes_per_KV_element
```

For concurrency/parallel sequences:

```
× sequence_count
```

This is the formula already used in Slice 05.

Now its origin should be clear:
- two tensors: K and V;
- every layer;
- KV-head width;
- one entry per cached token.

---

# Part VII — Decode

After prompt prefill, generate one new token.

The new input shape becomes approximately:

```
X_new: [B, 1, d]
```

New projections:

```
Q_new: [B, Hq, 1, Dh]
K_new: [B, Hkv, 1, Dh]
V_new: [B, Hkv, 1, Dh]
```

But attention reads historical cache:

```
K_cache: [B, Hkv, S, Dh]
V_cache: [B, Hkv, S, Dh]
```

where S is current sequence length.

Conceptual score shape:

```
[B, Hq, 1, S]
```

The new K/V are appended for the next step.

---

# Part VIII — Why decode is fundamentally serial

Token t+1 depends on the output sampled from token t.

```
logits_t
→ sample token_t
→ embed token_t
→ next forward
```

So along one sequence:

```
generation step 1
→ step 2
→ step 3
```

cannot all be computed in ordinary autoregressive decoding ahead of time.

This serial dependency is why:
- TG is latency-sensitive;
- small GEMV/GEMM shapes are common;
- repeatedly streaming model weights can dominate;
- speculative decoding matters.

Speculative decoding changes how many future token proposals can be verified per target pass, but does not remove the autoregressive correctness dependency.

---

# Part IX — Same weights, different shape regime

This is the key bridge to GPU hardware.

## Prefill

Typical shape character:

```
many rows × big matrices
```

So:
- better matrix-unit utilization;
- better batching;
- compute can dominate.

## Decode

Typical shape character:

```
one/few row(s) × big weight matrices
```

So:
- lower arithmetic intensity;
- weight streaming matters;
- memory bandwidth often dominates.

Therefore:

```
PP ranking of GPUs
can differ from
TG ranking of GPUs
```

This is not mysterious.
It comes directly from tensor shapes.

---

# Part X — MLP / FFN is also a major block cost

Attention is famous, but a decoder block also contains a large feed-forward network.

A common gated MLP pattern:

```
gate = W_gate x
up   = W_up x
hidden = activation(gate) ⊙ up
out  = W_down hidden
```

If:

```
W_gate: d → d_ff
W_up:   d → d_ff
W_down: d_ff → d
```

then the dense gated MLP contains roughly:

```
3 × d × d_ff
```

weight parameters per block, ignoring bias.

For many dense LLMs, FFN weight traffic is a large fraction of total per-token decode traffic.

So:

```
attention optimization
!= whole model optimization
```

---

# Part XI — Residual and normalization are not the parameter majority

Norm scale vectors are O(d), while large linear layers are O(d²) or O(d×d_ff).

So in parameter count:
- attention/MLP matrices dominate;
- norm vectors are tiny.

But runtime importance is not identical to parameter count.

Norm/residual:
- touch hidden-state memory;
- may need fusion;
- can create extra kernel launches;
- can be latency-relevant in small-shape decode.

Thus:

```
small parameter count
!= zero runtime cost
```

---

# Part XII — LM head and logits

After final block:

```
hidden: [B, T, d]
→ final norm
→ LM head
→ logits: [B, T, vocab_size]
```

For decode, usually only the newest-position logits are needed for sampling.

The LM head may share/tie weights with the input embedding in some architectures, but not all.

Never infer tying from “decoder-only” alone.

---

# Part XIII — Sampling is outside the Transformer block

The model outputs logits.

A sampler can then apply:
- temperature;
- top-k;
- top-p;
- min-p;
- repetition penalties;
- grammar constraints;
- greedy argmax.

These affect output/token selection and end-to-end latency.

But:

```
sampler settings
!= model weights
```

and llama-bench timing may intentionally exclude some UI/sampling overhead.

So benchmark TG and chat UX latency are related but not identical metrics.

---

# Part XIV — One block, two hardware stories

The same architecture yields two major inference modes:

```
PREFILL
many new tokens
large matrix shapes
attention T×T conceptually
build KV cache
PP metric

DECODE
one/few new tokens
read existing KV
small matrix batch dimension
serial autoregression
TG metric
```

This is the most important structural bridge between:
- Transformer math;
- KV memory;
- Roofline;
- matrix units;
- FlashAttention;
- speculative decoding.

---

# Claims to avoid

- "attention is the entire Transformer";
- "7B parameters tells me the KV size";
- "prefill and decode use different model weights";
- "decode recomputes the entire prompt from scratch every token";
- "the full T×T attention matrix must exist in VRAM";
- "KV cache stores Q, K and V";
- "more query heads always means larger KV";
- "PP and TG should scale identically";
- "norm has few parameters so it has no runtime cost";
- "logits are already the final text token".
