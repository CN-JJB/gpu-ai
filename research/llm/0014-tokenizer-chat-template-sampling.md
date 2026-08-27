# Research Note 0025 — Tokenizer / Chat Template / Special Tokens / Sampling Boundary

日期：2026-08-27

## Research question

When a user types:

```
你好
```

what does the model actually receive?

Not raw UI text.

A chat inference path is closer to:

```
structured messages
→ chat template
→ rendered prompt bytes/text
→ tokenizer
→ token IDs
→ model
→ logits
→ sampling policy
→ next token ID
→ tokenizer decode
→ displayed text
```

Every boundary can change:
- token count;
- context use;
- PP;
- KV;
- output behavior;
- reproducibility.

---

# Current official/runtime evidence

## Hugging Face chat templates

Current Transformers documentation describes a chat template as a Jinja template stored with tokenizer/model metadata and applied to a list of messages.

Important current guidance:
- templates insert role/control/special tokens;
- `add_generation_prompt` can append the assistant-generation header;
- templates can consume tools/documents/other variables;
- when a rendered template already contains needed special tokens, blindly adding special tokens again can duplicate BOS/EOS/control markers.

## llama.cpp pinned snapshot

Pinned course upstream:

```
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current code includes:
- Jinja chat-template rendering tests;
- `scripts/get_chat_template.py` reading `tokenizer_config.json`;
- `llama-tokenize` tool;
- sampler-chain implementations.

Current `llama-tokenize` loads vocabulary only and can print token IDs/count without loading full model weights.

---

# Part I — A chat is structured data first

Typical messages:

```json
[
  {"role":"system","content":"Answer briefly."},
  {"role":"user","content":"Hello"}
]
```

This is not yet a model prompt.

A model may have been trained on a format like:

```
<system marker>
system text
<end marker>
<user marker>
user text
<end marker>
<assistant marker>
```

Another model may use:

```
[INST] ...
[/INST]
```

The template converts structured messages into the model's expected serialization.

---

# Part II — Chat template is part of the model interface

If a model was instruction-tuned with one control-token format, replacing it with another format changes the token sequence the model conditions on.

Therefore:

```
same weights
+
wrong template
```

can behave like a broken deployment even if:
- GPU is correct;
- quant is correct;
- backend is correct.

Template correctness is not cosmetic UI formatting.

---

# Part III — Special tokens

Common categories include:
- BOS / beginning-of-sequence;
- EOS / end-of-sequence;
- role markers;
- message start/end markers;
- tool-call markers;
- image/video placeholders;
- fill-in-the-middle tokens.

A special token is usually registered so the tokenizer treats that exact control string as one semantic token rather than ordinary text pieces.

Exact IDs are tokenizer/model specific.

Never hardcode one model family's token IDs into another.

---

# Part IV — Duplicate BOS/EOS trap

Suppose the template already emits:

```
<BOS>
...
<EOS>
```

Then a second tokenization step with automatic:

```
add_special_tokens=True
```

may prepend/append another special token.

Possible result:

```
BOS BOS ...
```

Current Hugging Face guidance explicitly warns about this type of double-special-token error when rendering a template first and tokenizing later.

Correct behavior depends on the tokenizer API and template.

Do not memorize:
```
always add BOS
```
or:
```
never add BOS
```.

Inspect the exact model/template/tokenizer behavior.

---

# Part V — add_generation_prompt

For many templates, after the last user message the model needs a marker indicating:

```
assistant response begins here
```

Conceptually:

```
... user message end
<assistant>
```

Current template APIs commonly expose:

```
add_generation_prompt
```

If the model/template uses such a marker and it is missing, the model may see a different task structure.

Not every model needs the same marker.

---

# Part VI — Tokenizer

A tokenizer maps prompt text/control symbols into IDs:

```
rendered prompt
→ [token_id_0, token_id_1, ...]
```

Modern LLM tokenizers can use:
- BPE-like methods;
- SentencePiece/unigram-like methods;
- byte fallback or byte-level components;
- model-specific special-token rules.

For local inference, the stable lesson is:

```
characters
!= bytes
!= tokens
```

and token count must be measured with the exact tokenizer.

---

# Part VII — Why token count is hardware-relevant

Rendered prompt token count T directly affects:

## Prefill

More tokens:

```
T ↑
→ PP work ↑
```

with exact scaling dependent on attention architecture.

## KV

For full attention:

```
KV ∝ T
```

For local/hybrid/compressed architectures, use Slice 30's architecture-specific cache model.

## Context budget

If:

```
system prompt
+ chat history
+ tools schema
+ documents
+ user prompt
+ generation reserve
>
context limit
```

something must be truncated/rejected/compressed.

So a verbose chat template can consume real capacity.

---

# Part VIII — Tools and RAG can silently inflate the prompt

Tool-capable templates may serialize:
- JSON schema;
- function names/descriptions;
- argument schemas.

RAG templates may serialize:
- documents;
- metadata;
- citations.

The user may type only 20 words while the runtime sends thousands of prompt tokens.

Therefore server workload identity should record:

```
rendered token count
```

not only visible user-text length.

---

# Part IX — Dynamic template variables threaten reproducibility

Current chat-template systems can receive additional variables such as:
- tools;
- documents;
- date/time;
- model-specific flags.

Some templating systems expose current-date helpers.

Thus two runs with identical user messages can serialize differently if:
- date changes;
- tool list changes;
- system prompt changes;
- generation-prompt flag changes.

For benchmark Evidence, freeze these inputs.

---

# Part X — Prompt artifact identity

A reproducible prompt should record:

```
messages JSON SHA256
chat template SHA256
rendered prompt SHA256
token IDs SHA256
token count
```

This is the prompt-side equivalent of model GGUF SHA256.

Screenshotting:

> "Hello"

is insufficient evidence of the actual model input.

---

# Part XI — Model output is logits, not text

For newest position the model outputs:

```
z
=
[z_0, z_1, ..., z_(V-1)]
```

one logit per vocabulary token.

Logits are unnormalized scores.

A probability distribution can be formed with softmax:

```
p_i
=
exp(z_i) / Σ_j exp(z_j)
```

Sampling policy decides which token is selected.

---

# Part XII — Greedy decoding

Greedy:

```
token
=
argmax_i z_i
```

This removes RNG from token selection.

But cross-runtime byte-identical output is still not absolutely guaranteed because:
- floating-point kernels can produce tiny logit differences;
- near-ties can switch argmax;
- template/tokenization/backend may differ.

Greedy is more reproducible, not magical identity proof.

---

# Part XIII — Temperature

Conceptually:

```
p_i(T)
∝
exp(z_i / T)
```

For:
```
T > 1
```
distribution becomes flatter.

For:
```
0 < T < 1
```
distribution becomes sharper.

Implementations often special-case:
```
T = 0
```
as greedy/deterministic behavior rather than literally dividing logits by zero.

Check current runtime semantics.

---

# Part XIV — Top-k

Top-k keeps only the k highest-scoring candidate tokens before sampling/renormalization.

Example:

```
vocab = 100k
top-k = 40
```

means only the current best 40 candidates survive that filter.

It does not mean the model has a 40-token vocabulary.

---

# Part XV — Top-p / nucleus

Sort candidates by probability.

Keep the smallest prefix whose cumulative probability reaches the configured p threshold.

Example:

```
top-p = 0.9
```

The number of surviving tokens changes dynamically with distribution shape.

---

# Part XVI — Sampling is an ordered policy

Real runtimes can combine:
- penalties;
- top-k;
- top-p;
- min-p;
- temperature;
- grammar;
- other filters.

The order can matter because one filter changes the candidate distribution seen by the next.

Current llama.cpp implements sampling as a chain rather than an unordered set of knobs.

So benchmark workload identity should record the complete sampler configuration/order when output generation behavior matters.

---

# Part XVII — Random seed

With stochastic sampling, seed controls RNG state.

Same seed improves reproducibility only if the rest is also frozen:

```
same prompt tokens
same logits
same sampler implementation
same sampler order
same parameters
```

Across runtime versions/hardware, tiny numeric differences can change the candidate distribution and then the stochastic trajectory diverges.

Therefore:

```
same seed
!= universal identical text guarantee
```

---

# Part XVIII — Sampling vs llama-bench TG

Benchmark TG often measures model evaluation throughput separately from full chat UX.

End-to-end chat can include:
- tokenization;
- template rendering;
- sampling;
- detokenization;
- network streaming;
- grammar/tool handling.

So:

```
llama-bench TG
!=
full application tokens/s / latency
```

This does not make llama-bench bad.
It means it measures a narrower component.

---

# Part XIX — Prefix cache consequence

Prefix-cache identity depends on the actual token prefix.

Therefore:

```
same visible user text
+
different chat template
```

can produce:

```
different token prefix
→ no cache identity
```

This links directly to Slice 09.

---

# Part XX — Benchmark rule

For performance A/B where prompt matters, freeze:

```
messages
template
special-token policy
rendered prompt
token IDs
sampling config
```

If the optimization test only benchmarks synthetic PP/TG token counts with `llama-bench`, note that it does not represent an exact real chat prompt.

Both experiments are useful; they answer different questions.

---

# Claims to avoid

- "chat template is only UI formatting";
- "same text means same tokens";
- "one character equals one token";
- "BOS should always be manually added";
- "special token strings can be copied between model families";
- "logits are probabilities";
- "temperature 0 literally means divide logits by zero";
- "top-p keeps a fixed number of tokens";
- "same seed guarantees identical output everywhere";
- "TG benchmark includes every chat-system overhead";
- "same visible prefix guarantees prefix-cache hit".
