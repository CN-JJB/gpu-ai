# Research Note 0022 — Mixture of Experts: Total Params vs Active Params vs Weight Traffic

日期：2026-08-27

## Research question

Mixture-of-Experts models are often described with two numbers:

```
total parameters
active parameters per token
```

Those are useful, but incomplete for local inference.

A hardware decision needs at least four separate quantities:

```
1. total model parameters
2. active expert parameters per token
3. resident weight memory
4. actual weight bytes moved per token/batch
```

These are not interchangeable.

---

# Primary sources

## Switch Transformer

Fedus, Zoph & Shazeer:
https://arxiv.org/abs/2101.03961

Stable idea:
- sparse expert activation;
- router selects experts;
- parameter count can scale without activating all expert compute for each token;
- routing/load balancing and communication are first-class problems.

## Mixtral of Experts

https://arxiv.org/abs/2401.04088

Mixtral 8x7B is a concrete decoder-only sparse MoE example:
- eight feed-forward experts per layer;
- router selects two experts per token;
- different tokens can choose different experts.

The paper reports a large gap between total available parameters and active parameters used for a token.

## DeepSeekMoE

https://arxiv.org/abs/2401.06066

Adds:
- finer-grained routed experts;
- always-active shared experts;
- explicit specialization design.

## DeepSeek-V3

https://arxiv.org/abs/2412.19437

Concrete modern large-MoE example:
- 671B total parameters;
- 37B activated per token;
- DeepSeekMoE-derived architecture.

The important course lesson is not the marketing number itself, but why:

```
37B active
does not mean
37B worth of model weights is all you need to store
```

---

# Part I — A dense FFN baseline

A dense SwiGLU-like FFN:

```
Expert(x)
=
W_down(
  SiLU(x W_gate)
  ⊙
  (x W_up)
)
```

with roughly:

```
P_expert
≈
3 d d_ff
```

weights.

In a dense model, every token uses the same one FFN.

---

# Part II — Replace one FFN with N experts

An MoE layer contains multiple FFN experts:

```
E_0
E_1
...
E_(N-1)
```

A router computes routing scores from the token hidden state:

```
r
=
x W_router
```

Conceptually:

```
r: [N]
```

Then choose top-k experts:

```
I
=
TopK(r, k)
```

Selected expert outputs are weighted/combined:

```
y
=
Σ_{i ∈ I}
g_i E_i(x)
```

Exact normalization/gating differs by architecture.

---

# Part III — Total expert parameters

If every expert has the same dense SwiGLU shape:

```
P_expert
=
3 d d_ff
```

and there are N routed experts:

```
P_routed_total
=
N × P_expert
```

If there are S shared experts of the same size:

```
P_shared_total
=
S × P_expert
```

Total expert storage:

```
(N + S) × P_expert
```

plus:
- attention;
- embeddings;
- router;
- norms;
- dense layers;
- architecture-specific weights.

---

# Part IV — Active expert parameters per token

For classic top-k routed experts:

```
P_active_routed
≈
k × P_expert
```

If S shared experts always run:

```
P_active_expert
≈
(k + S) × P_expert
```

if the shared experts use the same dimensions.

But a model's published "active parameter" number may include:
- attention;
- shared experts;
- routed experts;
- embeddings or other conventions.

So do not reconstruct an official active-parameter figure from top-k alone unless the paper/config defines the accounting.

---

# Part V — Active parameters do not determine resident memory

Suppose:

```
N = 8
k = 2
```

Only two experts run for one token.

But if all eight expert weights are resident on one GPU:

```
VRAM must hold all 8
```

not just 2.

Therefore:

```
active params/token
!=
resident params
```

This is the most important local-inference MoE trap.

---

# Part VI — Offloading changes the equation, not the requirement

A runtime can keep some expert weights in:
- CPU RAM;
- another GPU;
- storage-backed/offload mechanisms.

Then one GPU does not need to hold all experts.

But selected experts must still become available when routing chooses them.

That can introduce:

```
PCIe / interconnect / host-memory traffic
→ latency
→ bandwidth bottleneck
```

Dynamic routing makes "only load the needed expert" difficult for low-latency one-token decode because the needed experts can change:
- layer to layer;
- token to token.

---

# Part VII — Concrete Mixtral-like teaching example

Use a synthetic architecture with dimensions matching a familiar 8-expert scale:

```
d = 4096
d_ff = 14336
N = 8 routed experts
k = 2 active
L = 32 MoE layers
effective weight = 4.5 bpw
```

Per expert:

```
P_expert
=
3 × 4096 × 14336
=
176,160,768 weights
```

Per layer all routed experts:

```
8 × P_expert
=
1,409,286,144 weights
```

Per token active routed expert weights:

```
2 × P_expert
=
352,321,536 weights/layer
```

At 4.5 bpw:

```
one expert
≈ 94.5 MiB

all 8 experts/layer
≈ 756 MiB

selected top-2/layer
≈ 189 MiB
```

Across 32 layers, expert-weight storage proxy:

```
≈ 23.625 GiB
```

whereas a no-reuse selected-expert byte proxy is:

```
≈ 5.906 GiB/token
```

across the 32 layers.

These are teaching storage/traffic proxies, not a full Mixtral model accounting or measured runtime traffic.

---

# Part VIII — Why actual weight bytes/token are not simply active params × bytes

Consider one-token decode:

```
M = 1 token
```

If the selected expert weights are too large for useful cache reuse across steps, the runtime may repeatedly stream much of those expert weights.

Then:

```
active expert storage
```

is a useful rough bandwidth scale.

But now consider prefill or a serving batch:

```
M = 16 tokens
```

Several tokens may choose the same expert.

A backend can group token rows by expert:

```
expert 0:
token 1,4,9,...

expert 1:
token 2,5,...
```

Then one expert's weight tiles can serve multiple token rows in one GEMM-like batch.

Therefore:

```
actual bytes/token
can be much lower
than
k × expert_weight_bytes
```

because expert weights can be amortized across routed tokens.

---

# Part IX — Expert reuse vs load balance

These two goals can conflict.

Imagine 16 tokens, top-2, 8 experts.

Total routed assignments:

```
16 × 2
=
32
```

## Balanced

Each expert receives four assignments:

```
[4,4,4,4,4,4,4,4]
```

Good:
- parallel balance;
- all expert devices have work.

But all eight experts become active in the batch.

## Extremely skewed

Only experts 0 and 1 receive all assignments:

```
[16,16,0,0,0,0,0,0]
```

Good from one narrow weight-reuse perspective:
- only two expert weight sets are needed.

Bad for expert parallelism:
- two experts/devices can become overloaded;
- other expert devices idle;
- latency tail can worsen.

So:

```
minimum unique expert bytes
!=
maximum parallel efficiency
```

---

# Part X — Router overhead

A simple router projection:

```
W_router: d → N
```

has roughly:

```
d × N
```

weights.

Compared with expert FFNs, this is often small.

But router behavior is important because it determines:
- which experts execute;
- token grouping;
- device traffic;
- load balance.

Small parameter count can control large downstream cost.

---

# Part XI — Capacity / load balancing belongs to training and serving design

MoE research includes:
- capacity factors;
- auxiliary balancing losses;
- token dropping/overflow behavior;
- alternative routing strategies.

Do not blindly transfer a training-time "expert capacity" rule into inference.

At inference, runtimes commonly aim to process all requested tokens, but routing imbalance can still cause:
- uneven expert batches;
- device imbalance;
- queueing;
- poor kernel occupancy.

The exact behavior is backend/model-specific.

---

# Part XII — Expert parallelism across GPUs

A common distributed idea:

```
GPU0 owns experts 0,1
GPU1 owns experts 2,3
GPU2 owns experts 4,5
GPU3 owns experts 6,7
```

For each MoE layer:

1. router selects experts;
2. token hidden states are sent to expert owners;
3. experts execute;
4. outputs return/are combined.

This creates token-dispatch communication.

It is different from ordinary tensor parallel all-reduce.

A useful conceptual cost:

```
T_layer
≈
router
+
dispatch/collect over interconnect
+
expert compute
+
imbalance tail
```

Poor PCIe/P2P can therefore become a new MoE roof.

This connects directly to Slice 11.

---

# Part XIII — Local single-GPU implication

MoE can reduce active compute relative to a dense model with the same total parameter count.

But a local user can still face:

```
huge total weight file
+
huge resident VRAM requirement
```

if all experts must remain available on the GPU.

Thus:

```
"only 13B active"
```

does not imply:

```
"fits like a dense 13B"
```

Likewise:

```
37B active
```

does not imply:
```
37B-sized storage
```

---

# Part XIV — Quantization matters twice

Quantizing MoE weights reduces:
- total resident expert storage;
- selected expert byte traffic.

Because there can be many experts, total-memory savings are especially valuable.

But the same caveat remains:

```
low-bit storage
!=
native low-bit expert compute automatically
```

Backend support for:
- expert grouping;
- dequantization;
- batched expert GEMM;
- routing kernels;

can dominate practical performance.

---

# Part XV — Prefill and decode behave differently again

## Prefill / batched serving

Many tokens:
- richer expert batches;
- more weight reuse;
- better GEMM shapes;
- routing imbalance still matters.

## Single-sequence decode

One new token per step:
- only k routed experts per layer;
- tiny per-expert token batch;
- selected expert weights can be bandwidth-heavy;
- routing changes between tokens;
- expert offload/interconnect latency can be painful.

This is why an MoE model can have attractive active FLOPs but still be awkward on consumer hardware.

---

# Part XVI — Shared experts

DeepSeekMoE-style shared experts are always active.

Conceptually:

```
y
=
Shared(x)
+
Σ routed top-k
```

They capture common transformations while routed experts specialize.

For inference accounting:

```
active expert work
=
shared experts
+
selected routed experts
```

Never ignore shared experts when estimating active compute/traffic.

---

# Part XVII — Active parameter count is still useful

It is useful for estimating:
- approximate arithmetic work;
- comparison with dense compute scale;
- why giant sparse models can have manageable FLOPs/token.

But it is not enough for:
- VRAM fit;
- weight file size;
- CPU offload behavior;
- multi-GPU communication;
- actual TG.

The complete chain is:

```
total params
→ resident placement
→ routing
→ active experts
→ token grouping/reuse
→ interconnect
→ real PP/TG
```

---

# Claims to avoid

- "MoE only loads active experts into memory.";
- "active parameters = model size.";
- "top-2 means two experts total.";
- "every layer must use the same expert pair.";
- "fewer active parameters guarantees faster TG.";
- "expert weights must be reread separately for every token in a batch.";
- "perfect load balance always minimizes memory traffic.";
- "MoE multi-GPU communication is just tensor-parallel all-reduce.";
- "shared experts can be ignored in active-parameter accounting.";
- "published active-param counts all use the same accounting convention."
