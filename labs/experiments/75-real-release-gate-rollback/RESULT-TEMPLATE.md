# Result — Experiment 75

## Baseline

- release ID:
- runtime SHA:
- model SHA:
- config SHA:
- manifest:
- known-good evidence:

## Candidate

- release ID:
- change classification:
- declared semantic change:
- runtime SHA:
- model SHA:
- config SHA:

## Policy

Defined before candidate:
- readiness:
- first inference:
- TG:
- PPL:
- critical fixtures:
- TTFT p95:
- SLO compliance:
- error rate:

## Gate result

- readiness:
- smoke:
- performance:
- quality:
- serving:
- final:
  - ACCEPT
  - ROLLBACK
  - BLOCKED_MISSING_EVIDENCE

## Rollback, if triggered

- restored runtime SHA:
- restored model SHA:
- restored config SHA:
- identity equals baseline?:
- readiness:
- smoke:
- VERIFIED / FAILED:

## Evidence retained

- candidate logs:
- benchmark:
- quality:
- serving:
- rollback:

## Postmortem note

If rejected:
- which gate failed first?:
- root cause known?:
- candidate artifact preserved for diagnosis?:
