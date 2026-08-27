# Quality Gate Card

## Identity

Freeze:
- source model:
- source revision:
- candidate model/artifact:
- tokenizer:
- corpus:
- corpus SHA256:
- runtime commit:
- evaluation args:

## Math

```
NLL_t = -ln p(correct token)

CE = mean(NLL_t)

PPL = exp(CE)
```

Lower PPL:
```
better next-token fit
on the same evaluation setup
```

## A/B

- baseline PPL:
- candidate PPL:
- ΔPPL:
- PPL ratio:
- uncertainty if reported:

Optional:
- KL:
- mean probability change:
- top-token agreement:

## Task fixtures

- fixture revision:
- deterministic settings:
- baseline pass:
- candidate pass:
- critical failures:

## Performance

- baseline PP/TG:
- candidate PP/TG:
- speedup:
- memory delta:

## Decision

- ACCEPT
- ACCEPT WITH QUALITY TRADEOFF
- REJECT
- NEEDS MORE EVIDENCE

## Do not compare PPL directly when

- tokenizer differs;
- corpus differs;
- preprocessing differs;
- evaluation method differs.

## Chat quality

PPL alone is insufficient.
Use target-task evaluation.
