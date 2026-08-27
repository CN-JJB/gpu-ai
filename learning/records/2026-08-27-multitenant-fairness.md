# Learning / Build Record — 2026-08-27 Multi-Tenant Fairness

## Slice

37 — Resource-aware multi-tenant fairness, quotas and work-conserving borrowing.

## Production output

Research:
- `research/llm/0019-multitenant-fairness-quotas.md`

Reference:
- `reference/llm/multitenant-fairness-quotas.md`

Lesson:
- `lessons/37-multitenant-fairness/01-slots-quotas-borrowing.html`

Labs:
- `labs/experiments/68-multitenant-fairness-model/`
- `labs/experiments/69-real-tenant-serving-report/`

Evidence:
- `examples/evidence/experiment-37-multitenant-fairness.md`

## Verified L0 result

FIFO:
```
B mean wait = 10.5 s
util = 100%
```

Strict cap:
```
B mean wait = 1.5 s
util = 60%
```

Fair borrowing:
```
B mean wait = 1.5 s
util ≈ 85.714%
```

## Stable skill

Learner can distinguish:
```
request fairness
from
resource fairness
```

and can evaluate fairness together with hardware utilization.

## Next

Service exposure / privacy / authentication:
- localhost vs LAN vs public bind;
- authentication boundary;
- TLS/reverse proxy;
- logs/prompts as sensitive data;
- metrics/slots endpoints;
- least exposure;
- model license / redistribution boundary.
