# Evidence — Experiment 32: Quality Gate / Perplexity

状态：stable quality-gate lesson complete; L0 CE/PPL arithmetic verified; real quant/backend quality packet ready.

## Claim

> Performance optimization is not complete until quality/correctness is checked. Perplexity is useful for controlled same-tokenizer/same-corpus A/B, but it is not a universal chat-quality score.

## Current llama.cpp evidence

Pinned upstream:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current `tools/perplexity/README.md` explicitly states:
- lower perplexity means better next-token prediction on the evaluation text;
- PPL is not directly comparable across models, especially different tokenizers;
- finetunes can have higher PPL while human-rated output improves;
- perplexity is commonly used in llama.cpp to evaluate quantization loss;
- optional reference-logit/KL analysis can compare quantized logit distributions.

The current helper path uses:

```bash
llama-perplexity -m MODEL.gguf -f CORPUS.txt
```

after building the `llama-perplexity` target.

## Math

For correct next-token probability `p_t`:

```
NLL_t = -ln(p_t)
CE = mean(NLL_t)
PPL = exp(CE)
```

## Experiment 58 verification

Synthetic baseline:

```
[0.5, 0.25, 0.125, 0.5]
```

Verified:

```
CE  = 1.2130075659799042
PPL = 3.363585661014858
```

Synthetic candidate:

```
[0.48, 0.22, 0.10, 0.45]
```

Verified:

```
CE  = 1.3372974242304483
PPL = 3.8087361853561723
```

Derived:

```
ΔCE = 0.12428985825054406
PPL ratio = 1.1323440426984708×
```

The candidate is worse on this synthetic token stream.

## Experiment 59

The real quality packet freezes:
- source/model revision;
- baseline/candidate artifact SHA256;
- tokenizer;
- exact corpus bytes/SHA256;
- llama.cpp commit;
- evaluation arguments.

It pairs:
- PPL / optional KL evidence;
- target-task fixtures;
- Experiment 40 PP/TG;
- memory delta.

No real PPL values ship with the course.

## Quality budget

The learner defines the acceptance budget **before** deciding whether the performance gain is worth it.

The course deliberately does not publish a universal rule like:

```
ΔPPL < 0.1 = safe
```

because acceptable degradation is model/task/project specific.

## PPL boundary

Direct PPL comparison is invalid or weak when:
- tokenizer differs;
- corpus differs;
- preprocessing differs;
- evaluation method differs.

PPL also does not replace:
- chat helpfulness;
- coding tests;
- structured-output fixtures;
- long-context retrieval tests.

## Capstone consequence

Numerical/model-representation changes should become:

```
baseline PP/TG + quality
→ ONE variable
→ candidate PP/TG + quality
→ accept / tradeoff / reject
```

## Learner should reject

- faster quant is automatically better;
- PPL is a universal assistant-quality score;
- different-tokenizer PPL can be ranked directly;
- same output on five prompts proves equivalence;
- different stochastic output proves regression;
- one universal quality threshold exists.
