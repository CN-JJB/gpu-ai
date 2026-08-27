# Research Note 0019 — RMSNorm / Pre-Norm Residual / RoPE

日期：2026-08-27

## Research question

Modern decoder-only LLM blocks often contain three mechanisms that are easy to mentally blur together:

```
RMSNorm
Residual connection
RoPE
```

They solve different problems.

- RMSNorm: control hidden-state scale.
- Residual: preserve/add information across sublayers.
- RoPE: inject token position into attention Q/K geometry.

This slice connects their math to inference behavior and KV-cache identity.

---

# Primary sources

## RMSNorm

Zhang & Sennrich, 2019:
https://arxiv.org/abs/1910.07467

The paper proposes RMSNorm as a normalization that keeps re-scaling invariance without LayerNorm's explicit re-centering.

## RoPE

Su et al., 2021:
https://arxiv.org/abs/2104.09864

RoPE encodes position through rotations and gives attention inner products an explicit relative-position structure.

## LLaMA modern decoder example

https://arxiv.org/abs/2302.13971

LLaMA explicitly documents:
- pre-normalization;
- RMSNorm;
- SwiGLU;
- RoPE at each layer.

---

# Part I — Why normalize hidden vectors?

Suppose a hidden vector has dimension d:

```
x = [x₁, x₂, ..., x_d]
```

Deep residual networks repeatedly apply transformations and additions.

Without scale control, hidden magnitudes can drift into ranges that make optimization/training unstable.

At inference time, the trained normalization remains part of the exact model function.

Normalization is not an optional performance tweak that can be removed.

---

# Part II — LayerNorm vs RMSNorm

LayerNorm conceptually computes:

```
μ = mean(x)
σ² = mean((x - μ)²)

LN(x)
= g ⊙ (x - μ) / sqrt(σ² + ε)
+ b
```

RMSNorm removes explicit mean subtraction.

Define:

```
RMS(x)
=
sqrt(
  mean(x_i²)
  + ε
)
```

Then a common RMSNorm form:

```
RMSNorm(x)
=
g ⊙ x / RMS(x)
```

where g is a learned scale vector.

Important difference:

```
LayerNorm
→ centers + rescales

RMSNorm
→ rescales, does not force zero mean
```

Do not say:

> RMSNorm is LayerNorm without learned parameters.

It still has learned scale parameters in common implementations.

---

# Part III — Re-scaling intuition

Ignoring epsilon for intuition:

```
RMSNorm(c x)
≈
sign(c) × RMSNorm(x)
```

For positive c:

```
RMSNorm(c x)
≈
RMSNorm(x)
```

So multiplying the entire input vector by 3 does not make the normalized vector 3× larger.

This is the scale-invariance intuition.

With finite epsilon, the equality is approximate, especially for extremely small values.

---

# Part IV — Why RMSNorm is cheap in parameter count

Per hidden vector, common RMSNorm has one learned scale per hidden dimension:

```
params ≈ d
```

Compare with a dense projection:

```
d × d
```

or gated MLP:

```
≈ 3 d d_ff
```

So RMSNorm is tiny in model parameter count.

But runtime still needs:
- read hidden vector;
- square/reduce;
- compute reciprocal scale;
- multiply;
- write/use normalized values.

Small parameter count does not mean zero runtime cost.

Fusion matters.

---

# Part V — Pre-Norm residual block

A Llama-style simplified block:

```
h
=
x
+
Attention(RMSNorm(x))

y
=
h
+
MLP(RMSNorm(h))
```

The residual path lets the input bypass the transformed branch.

Geometrically:

```
output
=
existing representation
+
learned update
```

This is a useful mental model.

It does not mean the sublayer output is always numerically small.

---

# Part VI — Why residual matters for implementation

Residual addition itself has no huge weight matrix.

But it:
- reads hidden state;
- combines with sublayer output;
- creates a dependency boundary.

Optimized runtimes may fuse:
- norm;
- elementwise ops;
- residual updates;

to reduce kernel-launch and memory-traffic overhead.

This is especially relevant during decode, where matrix shapes are small enough that elementwise/kernel overhead can matter more.

---

# Part VII — Position cannot be ignored

Self-attention without position information is largely permutation-symmetric over token order.

The model needs to distinguish:

```
"dog bites man"
```

from:

```
"man bites dog"
```

RoPE injects position into Q/K vectors rather than adding one absolute position vector to the token embedding.

---

# Part VIII — 2D rotation intuition

Take one pair of hidden dimensions:

```
[x₀, x₁]
```

For angle φ:

```
R(φ)
=
[ cosφ  -sinφ
  sinφ   cosφ ]
```

Then:

```
x' = R(φ) x
```

A rotation preserves Euclidean norm:

```
||R(φ)x||
=
||x||
```

RoPE applies different rotation frequencies to different dimension pairs.

Position p determines the angle:

```
φ_i(p)
=
p × ω_i
```

where ω_i is the frequency for dimension pair i.

---

# Part IX — RoPE applies to Q and K

Conceptually:

```
q_p'
=
R(p) q_p

k_s'
=
R(s) k_s
```

Attention uses:

```
(q_p')ᵀ k_s'
```

Because rotations are orthogonal:

```
(R(p)q)ᵀ(R(s)k)
=
qᵀ R(s-p) k
```

up to rotation-sign convention.

The important stable idea:

```
attention inner product
contains relative position difference
```

not merely independent absolute labels.

---

# Part X — Shift-both-positions experiment

For base RoPE:

```
q at p
k at s
```

and:

```
q at p+c
k at s+c
```

have the same relative offset:

```
(s+c) - (p+c)
=
s-p
```

so the idealized RoPE dot-product contribution stays the same.

This does **not** mean the whole language model is globally shift invariant.

Other factors include:
- causal mask boundaries;
- content;
- context truncation;
- scaling schemes;
- model training distribution.

---

# Part XI — Why KV cache has position identity

During inference, each historical key corresponds logically to:

```
token content
+
layer
+
attention projection
+
position under this RoPE configuration
```

A runtime may choose different internal storage details, but the key used for attention is position-aware.

Therefore:

```
cached K for token at position 100
```

cannot be blindly reinterpreted as:

```
same K at position 500
```

without applying whatever position-remapping logic the model/runtime requires.

This connects to prefix cache:

```
same text bytes
!= automatically same reusable KV
```

Tokenization, model, RoPE/context configuration and prefix position matter.

---

# Part XII — Decode position

After prefill length S:

```
next query position
≈ S
```

The new Q is rotated for the current position.

Historical K values represent their own earlier positions.

Attention compares:

```
current query position
vs
historical key positions
```

This is how the model gets relative-position geometry while using the KV cache.

---

# Part XIII — RoPE theta / base frequencies

Many configs expose:

```
rope_theta
```

This affects the frequency schedule.

But:

```
same "uses RoPE"
!= same RoPE frequencies
```

Models can choose different base values and scaling rules.

Therefore a runtime must load the exact model metadata/configuration.

---

# Part XIV — Context extension is not "just set a bigger -c"

If a model was trained for a certain positional distribution, running far beyond that range can require a position-scaling strategy.

Configs may expose fields such as:

```
rope_scaling
```

and current model families can use different schemes.

Stable course rule:

```
context allocation
and
positional extrapolation quality
are separate questions
```

A runtime may successfully allocate 128k KV memory while the model's effective quality degrades under an inappropriate position scheme.

Do not teach one RoPE-scaling recipe as universally correct.

---

# Part XV — RoPE does not increase KV width

Applying RoPE changes values, not tensor width.

If:

```
K shape
=
[B,Hkv,S,Dh]
```

then after RoPE it remains:

```
[B,Hkv,S,Dh]
```

So base KV capacity formula does not gain another "RoPE tensor".

Runtime may hold auxiliary position/frequency data, but that is not the dominant KV-cache term.

---

# Part XVI — Performance consequences

## RMSNorm / residual

Usually:
- O(d) per token/layer elementwise/reduction work;
- low parameter count;
- possible fusion opportunity;
- more visible as overhead when matrix work is small.

## RoPE

Usually:
- elementwise/pairwise rotation of Q/K;
- no model-wide dense matrix;
- shape remains same;
- must be correctly integrated with attention/cache positions.

## Local inference failure modes

Wrong:
- RoPE config/scale;
- position indexing;
- cache reuse across incompatible context state;

can cause output-quality/correctness issues even if:
- model fits memory;
- kernels run quickly.

Correctness is a separate gate from performance.

---

# Claims to avoid

- "RMSNorm subtracts the mean.";
- "RMSNorm has no learned parameters.";
- "small parameter count means no runtime cost.";
- "residual means the sublayer can be skipped.";
- "RoPE adds a position vector to embeddings.";
- "RoPE rotates V as a universal rule.";
- "RoPE makes the whole model shift invariant.";
- "cached K can be moved to any position unchanged.";
- "larger allocated context automatically preserves long-context quality.";
- "RoPE increases KV tensor width."
