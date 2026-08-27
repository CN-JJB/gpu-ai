# Result — Experiment 69

## Identity

- serving packet:
- workload SHA:
- model/runtime:
- slots:
- cache:
- quota/scheduler layer:

## Tenants

### Tenant A
- request share:
- prompt-token share:
- output-token share:
- TTFT p50/p95:
- E2E p95:
- rejects:
- concurrency/context limits:

### Tenant B
Same fields.

## Fairness policy

- per-tenant concurrent limit:
- prompt limit:
- output limit:
- context limit:
- token budget:
- priority/weight:
- borrowing allowed?:

## Utilization

- aggregate output tok/s:
- slot utilization proxy:
- idle capacity:
- reason:

## Fairness result

- did one tenant monopolize slots?:
- did one tenant monopolize KV?:
- did rigid caps waste capacity?:
- starvation observed?:

## Decision

- keep policy
- add/tighten quota
- allow borrowing
- adjust weights
- needs more evidence
