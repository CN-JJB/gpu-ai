# Quality Gate Card

<figure>
  <img src="../../assets/diagrams/quality-gate.svg" alt="Quality Gate Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Quality Gate Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


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
