# Learning / Build Record — 2026-08-27 Tokenizer / Chat Template / Sampling

## Slice

31 — Structured messages → template → special tokens → tokenizer → logits → sampler → text.

## Production output

Research:
- `research/llm/0014-tokenizer-chat-template-sampling.md`

Reference:
- `reference/llm/prompt-tokenizer-sampling-identity.md`

Lesson:
- `lessons/31-tokenizer-sampling/01-template-token-logit-sampler.html`

Labs:
- `labs/experiments/56-chat-template-special-token-model/`
- `labs/experiments/57-real-prompt-token-identity/`

Evidence:
- `examples/evidence/experiment-31-tokenizer-chat-template-sampling.md`

## Verified L0 result

Same visible messages:
- template A: 72 bytes / 32 toy tokens;
- template B: 67 bytes / 63 toy tokens.

Duplicate BOS:
- 32 → 33 tokens;
- first two tokens become BOS/BOS.

## Stable skill

Learner can now treat prompt identity with the same rigor as model identity:

```
messages hash
→ template hash
→ rendered hash
→ token-ID hash/count
→ sampler identity
```

## Next

Add a model-quality/evaluation gate so performance optimization never silently trades away correctness/quality:
- next-token probability;
- cross entropy;
- perplexity;
- deterministic task checks;
- quant/backend A/B quality evidence.
