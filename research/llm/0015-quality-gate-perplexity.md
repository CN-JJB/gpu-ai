# Research Note 0026 — Quality Gate: Cross-Entropy, Perplexity and Optimization Safety

日期：2026-08-27

## Research question

A performance optimization can improve:

```
tokens/s
VRAM
power
```

while making the model worse.

Therefore a serious local-LLM optimization loop needs:

```
performance gate
+
quality/correctness gate
```

This slice introduces a beginner-first quality model.

---

# Current llama.cpp evidence

Pinned upstream:

```
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current `llama-perplexity` documentation states:
- perplexity measures next-token prediction with lower values better on the same evaluation setup;
- perplexity is not directly comparable across models, especially different tokenizers;
- finetunes can have higher perplexity while human-rated output quality improves;
- llama.cpp uses perplexity heavily to evaluate quantization quality;
- optional KL-divergence analysis can compare quantized logits with a higher-precision baseline.

This matches the course rule:
```
PPL is one quality instrument
not a universal chat-quality score
```

---

# Part I — Next-token probability

For token sequence:

```
x_1, x_2, ... x_T
```

an autoregressive model estimates:

```
p(x_t | x_1 ... x_(t-1))
```

At every position the model produces logits for all vocabulary tokens.

After normalization, look at the probability assigned to the token that actually occurs next.

Example:

```
correct next token probability
=
0.5
```

means the model placed half the probability mass on the observed token at that position.

---

# Part II — Negative log likelihood

If correct-token probability is p:

```
NLL
=
-ln(p)
```

Examples:

```
p=1.0
→ NLL=0

p=0.5
→ NLL≈0.693

p=0.01
→ NLL≈4.605
```

Being confidently wrong is heavily penalized.

The logarithm makes probabilities across a sequence add cleanly in log space.

---

# Part III — Cross entropy / mean NLL

For N scored tokens:

```
loss
=
-(1/N)
Σ_t ln p_t(correct)
```

For language-model evaluation this mean token negative log likelihood is often referred to as cross-entropy loss under the evaluation distribution.

Lower is better predictive fit on the same evaluation setup.

---

# Part IV — Perplexity

Perplexity:

```
PPL
=
exp(loss)
```

Equivalent:

```
PPL
=
exp(
- mean log probability of correct token
)
```

Intuition:

Lower PPL means the model is less "surprised" by the held-out token sequence.

A loose interpretation is an effective branching uncertainty, but do not turn this into a literal number of choices at each token.

---

# Part V — Tiny example

Correct-token probabilities:

```
[0.5, 0.25, 0.125, 0.5]
```

Mean NLL:

```
≈ 1.213008
```

Perplexity:

```
≈ 3.363586
```

Now degrade them slightly:

```
[0.48, 0.22, 0.10, 0.45]
```

Mean NLL:

```
≈ 1.337297
```

PPL:

```
≈ 3.808736
```

PPL ratio:

```
≈ 1.13234×
```

The candidate got worse on this synthetic token stream.

---

# Part VI — Why PPL comparisons are easy to misuse

To compare A/B, freeze:

```
dataset bytes
tokenizer
tokenization/special-token policy
context/evaluation method
runtime/tool behavior
```

Changing tokenizer changes:
- token boundaries;
- number of scored tokens;
- probability factorization.

Therefore:

```
Model A PPL 5
vs
Model B PPL 6
```

with different tokenizers is not a clean "A is better" claim.

---

# Part VII — Base vs instruct/chat model

A chat/instruction finetune is optimized for behavior beyond generic next-token fit on one plain-text corpus.

It may:
- follow instructions better;
- produce safer/helpful responses;
- score worse on a generic base-model PPL corpus.

So:

```
lower generic PPL
!=
better assistant
```

This is explicitly noted by current llama.cpp documentation.

---

# Part VIII — Why PPL is useful for quantization

Quantization changes model numerical representation.

If:
- exact source model;
- exact tokenizer;
- exact corpus;
- exact evaluation method;

are frozen, then PPL delta can detect prediction-quality loss caused by quantization.

That is a much cleaner use case than comparing unrelated models.

Useful metrics can include:

```
PPL_base
PPL_candidate
ΔPPL
PPL ratio
```

---

# Part IX — KL divergence adds distribution detail

Two models can have similar average PPL while differing in full token distributions.

KL divergence can compare a candidate distribution q against a reference p.

A common form:

```
D_KL(p || q)
=
Σ_i
p_i ln(p_i/q_i)
```

If distributions are identical:

```
KL = 0
```

Current llama.cpp perplexity tooling has an optional quantization-comparison workflow that records reference logits and computes KL-oriented statistics.

Important:
reference-logit files can be extremely large.

Do not enable this casually on a machine without enough storage.

---

# Part X — Backend correctness

Changing backend should ideally preserve the same trained model function up to expected numerical variation.

Quality checks can catch:
- unsupported/incorrect kernels;
- precision bugs;
- conversion mistakes;
- wrong tokenizer/template pairing;
- severe numerical regressions.

But exact output text is a noisy correctness metric because sampling can magnify tiny logit differences.

For backend validation prefer:
- teacher-forced probability/PPL tests;
- deterministic fixtures;
- raw logits/probability comparisons if available.

---

# Part XI — Quantized KV quality

KV quantization does not change stored model weights, but it changes cached activation representation.

Potential quality impact can depend on:
- context length;
- model;
- KV quant type;
- workload.

A short generic perplexity run may not expose long-context degradation.

So pair:
- PPL;
- target context tests;
- target task fixtures.

---

# Part XII — Deterministic task fixtures

PPL answers:

> How well does the model predict this corpus?

A task fixture answers:

> Does the optimized system still perform the behavior I need?

Fixture types can include:

## Exact
For tightly constrained deterministic output.

## Contains / regex
For a required fact/format.

## JSON schema / grammar
For structured-output systems.

## Multiple choice
Preferably scored by model probabilities rather than free-form stylistic output.

## Domain regression set
Your actual:
- coding prompts;
- Chinese questions;
- RAG tasks;
- tool calls;
- long-context retrieval.

The fixture set should be versioned.

---

# Part XIII — Avoid stochastic confounding

For quality A/B:
- use the same exact prompt token IDs;
- prefer greedy or controlled logprob evaluation;
- freeze sampler if generation is required.

A stochastic chat transcript mismatch does not by itself prove quality loss.

Likewise, identical output on five prompts does not prove quantization is lossless.

---

# Part XIV — Quality budget

Before optimization, define what degradation is acceptable.

Examples of project-specific constraints:

```
PPL ratio <= chosen limit
AND
all critical JSON fixtures pass
AND
long-context retrieval success unchanged
```

The course does **not** provide one universal PPL threshold.

A good quality budget depends on:
- model;
- task;
- baseline;
- user tolerance;
- performance gain.

---

# Part XV — Performance + quality Pareto

Imagine:

### A
```
TG 20 tok/s
PPL 6.0
```

### B
```
TG 30 tok/s
PPL 8.5
```

### C
```
TG 27 tok/s
PPL 6.1
```

There is no universal answer from speed alone.

The decision is multi-objective:

```
capacity
speed
quality
power
software risk
```

This reconnects to Slice 18 hardware/TCO decision logic.

---

# Part XVI — Capstone integration

For changes that can alter numerics/model representation:

- quant;
- KV type;
- backend/build;
- FlashAttention implementation;
- speculative settings where distribution correctness matters;

Capstone should record a quality gate.

A controlled optimization becomes:

```
baseline performance
+
baseline quality
→ one variable
→ candidate performance
+
candidate quality
→ accept/reject tradeoff
```

---

# Claims to avoid

- "perplexity is chat quality";
- "PPL from different tokenizers is directly comparable";
- "lower PPL always means a better instruction model";
- "same output on a few prompts proves numerical equivalence";
- "different stochastic output proves regression";
- "faster quant is better regardless of quality";
- "one universal ΔPPL threshold exists";
- "KV quant quality can be judged only at short context";
- "KL divergence file generation is cheap storage-wise".
