# Learning / Build Record — 2026-08-27 Quality Gate

## Slice

32 — Cross-entropy, perplexity and quality/correctness gating for optimization.

## Production output

Research:
- `research/llm/0015-quality-gate-perplexity.md`

Reference:
- `reference/llm/quality-gate-card.md`

Lesson:
- `lessons/32-quality-gate/01-cross-entropy-perplexity.html`

Labs:
- `labs/experiments/58-perplexity-math-model/`
- `labs/experiments/59-real-quality-gate/`

Evidence:
- `examples/evidence/experiment-32-quality-gate.md`

## Verified L0 result

```
baseline CE  = 1.213007566
baseline PPL = 3.363585661

candidate CE  = 1.337297424
candidate PPL = 3.808736185

PPL ratio = 1.132344043×
```

All values are synthetic.

## Stable skill

Learner can distinguish:

```
performance improvement
from
quality-preserving optimization
```

and can pair PPL/logit evidence with target-task fixtures.

## Key boundary

```
same tokenizer
+ same corpus
+ same evaluation
```

is required for clean PPL A/B.

## Next integration

Build a benchmark/workload manifest that freezes:
- hardware;
- runtime;
- model artifact;
- model architecture dossier;
- prompt/token identity;
- sampler;
- quality gate;
- raw benchmark outputs.
