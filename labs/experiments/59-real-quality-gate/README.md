# Experiment 59 — Real Quant / Backend Quality Gate

硬件等级：L1/L2，取决于 model/runtime。

## Goal

Pair a performance A/B with a quality A/B.

Good targets:
- F16/Q8/Q6/Q5/Q4 variants derived from the same base;
- backend/build changes with the same exact model;
- KV representation changes, with additional target-context tests.

## 0. Freeze identity

Record:
- corpus file + SHA256;
- model/source revision;
- baseline artifact SHA256;
- candidate artifact SHA256;
- tokenizer identity;
- llama.cpp commit;
- exact command args.

Do not compare unrelated model/tokenizer PPL.

## 1. Current llama.cpp perplexity path

Pinned upstream builds target:

```
llama-perplexity
```

Current official helper uses the form:

```bash
llama-perplexity -m MODEL.gguf -f CORPUS.txt
```

Always inspect current:

```bash
llama-perplexity --help
```

before a real run.

Baseline:

```bash
llama-perplexity -m "$BASE" -f "$CORPUS" | tee baseline-ppl.txt
```

Candidate:

```bash
llama-perplexity -m "$CAND" -f "$CORPUS" | tee candidate-ppl.txt
```

Use the same runtime/build and evaluation args.

## 2. Dataset

llama.cpp contributors commonly use Wikitext-2 for quantization comparisons, but your own domain corpus can also be useful.

Never compare numbers if corpus/preprocessing differ.

## 3. Optional KL path

Current llama.cpp can record high-precision reference logits and compare a quantized candidate with KL-based statistics.

This can require **tens of GiB** of logit storage for common models/corpora.

Only use after checking disk budget and current `--help`/README.

Do not make KL-logit capture the default beginner path.

## 4. Target task fixtures

Copy:

```
QUALITY-RESULT-TEMPLATE.md
```

Add your real tasks:
- deterministic JSON;
- coding;
- Chinese;
- RAG;
- long-context retrieval.

Freeze prompt identity using Experiment 57.

## 5. Pair performance

Use Experiment 40:
- baseline PP/TG;
- candidate PP/TG;
- same one-variable discipline.

Then make one decision using both:
```
speed
+
memory
+
quality
```

## No fake results

This lab ships with no model PPL or task scores.
