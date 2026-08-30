# Safe Upgrade / Rollback Card

<figure>
  <img src="../../assets/diagrams/release-rollback.svg" alt="Safe Upgrade / Rollback Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Safe Upgrade / Rollback Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## Baseline identity

- runtime SHA:
- model SHA:
- config SHA:
- manifest:
- readiness:
- smoke:
- performance:
- quality:
- serving SLO:

## Candidate change

Classify:
- runtime
- model
- execution config
- multi-block system release

Declared change:

## Policy — define before run

- max readiness:
- max first inference:
- min PP/TG:
- max memory:
- max PPL ratio:
- critical fixtures:
- max TTFT p95:
- min SLO compliance:
- max errors:

## Candidate result

- identity expected?:
- ready?:
- smoke?:
- performance:
- quality:
- SLO:

## Decision

- ACCEPT
- ROLLBACK
- BLOCKED_MISSING_EVIDENCE

## Rollback verification

Restore exact known-good:
- runtime SHA:
- model SHA:
- config SHA:

Then:
- ready:
- smoke:
- recovery time:

## Rule

```
rollback complete
only after
identity + readiness + smoke
```
