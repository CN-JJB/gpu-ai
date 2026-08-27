# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–31 are implemented.

Latest model/system chain:

```
24 decoder-only dataflow
25 RMSNorm / RoPE
26 MHA/MQA/GQA
27 SwiGLU FFN
28 MoE
29 Model Dossier
30 Sliding/Hybrid/Latent KV
31 Tokenizer / Chat Template / Sampling
```

## Slice 31 core

Actual model input identity:

```
structured messages
→ chat template
→ rendered bytes
→ tokenizer
→ token IDs
```

Output:

```
logits
→ ordered sampler policy
→ token ID
→ decoded text
```

Benchmark prompt Evidence should preserve:
- message hash;
- template hash;
- rendered hash;
- token-ID hash/count;
- sampling config.

Current pinned llama.cpp includes Jinja template support/tests and `llama-tokenize`.

## Active next slice — Quality Gate

Build beginner-first:

```
logits
→ probabilities
→ probability assigned to correct next token
→ negative log likelihood
→ mean cross entropy
→ perplexity = exp(loss)
```

Teach:
- lower PPL on same dataset/tokenizer is better predictive fit;
- PPL across different tokenizers is not directly comparable;
- PPL is not chat helpfulness;
- quant/backend optimization needs quality/correctness check;
- deterministic task fixtures complement PPL.

Then add a real quant/backend A/B quality packet without fake quality results.
