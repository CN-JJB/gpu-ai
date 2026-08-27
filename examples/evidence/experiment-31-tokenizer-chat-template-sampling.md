# Evidence — Experiment 31: Tokenizer / Chat Template / Sampling Identity

状态：stable prompt-interface lesson complete; toy serialization/special-token model verified; real prompt-artifact path ready.

## Claim

> Chat-template serialization, tokenizer identity, special-token policy and sampler configuration are part of the model workload. Same visible user text does not imply the same token input or output process.

## Current official evidence

Hugging Face current chat-template documentation:
- chat templates render structured messages into model-specific prompt serialization;
- `add_generation_prompt` can append assistant-generation markers;
- templates can include special tokens/tools/documents;
- separately tokenizing an already rendered template with extra automatic special tokens can duplicate required control tokens.

Current pinned llama.cpp:
```
d7a2074112d27649303fa107eb8c94db1ee435f3
```

includes:
- Jinja chat-template tests;
- `scripts/get_chat_template.py`;
- `llama-tokenize`;
- ordered sampler-chain code.

## Experiment 56 verification

Messages:

```
system: Answer briefly.
user: Hello!
```

Synthetic special-token + byte-fallback tokenizer:

### Template A
Registered role/control tokens:

```
rendered bytes = 72
toy tokens = 32
```

### Template B
Verbose plain-text headings:

```
rendered bytes = 67
toy tokens = 63
```

Therefore:

```
fewer bytes
!=
fewer tokens
```

because special-token registration changes tokenization.

## Duplicate BOS verification

Template A already emits BOS.

Synthetic auto-BOS tokenization:

```
normal count = 32
auto-BOS count = 33
first two tokens = ["<BOS>","<BOS>"]
```

This is a teaching model of the real duplicate-special-token failure class.

## Experiment 57

Real prompt evidence saves:
- messages SHA256;
- chat-template SHA256;
- rendered prompt SHA256;
- token-ID SHA256;
- token count;
- special-token map;
- generation-prompt state.

Optional llama.cpp cross-check can use the current `llama-tokenize` vocabulary-only tool.

BOS/special-token behavior must be deliberately aligned before comparing token IDs.

## Sampling boundary

```
model
→ logits
→ sampler chain
→ selected token ID
```

Stable distinctions:
- logits are not probabilities;
- greedy uses argmax;
- temperature changes distribution sharpness;
- top-k keeps fixed candidate count;
- top-p keeps a variable-size cumulative-probability set;
- sampler order can affect output;
- seed alone does not guarantee cross-runtime identical text.

## Hardware consequence

Prompt token count affects:
- PP;
- KV/context;
- prefix-cache identity;
- TTFT.

Tools/RAG/system templates can make actual prompt size much larger than visible user text.

## Learner should reject

- chat template is cosmetic;
- characters/bytes/tokens are interchangeable;
- BOS should always be added manually;
- same visible prefix guarantees cache identity;
- logits are final text;
- top-p keeps a fixed number of tokens;
- same seed guarantees universal output identity;
- llama-bench TG includes all chat/template/sampling/network overhead.
