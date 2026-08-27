# Safe Upgrade / Rollback Card

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
