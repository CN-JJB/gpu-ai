# Multi-Tenant Fairness / Quota Card

## Weak fairness unit

```
request count
```

can hide huge resource differences.

## Better accounting

Record per tenant:
- prompt tokens
- output tokens
- context
- active duration
- KV estimate
- request count

## Basic controls

- max active requests / tenant
- max prompt tokens / request
- max output tokens / request
- max context
- token budget / time window
- priority/weight

## Work-conserving rule

```
enforce fair share under contention
borrow idle capacity when no competitor waits
```

## Report per tenant

- requests
- success/reject
- prompt token share
- output token share
- TTFT p50/p95
- E2E p50/p95

## Watch for

- starvation
- unused capacity from rigid quotas
- long-context KV monopolization
- one tenant dominating active slot time

## Boundary

Application/gateway policy and inference-runtime scheduler are separate layers.
