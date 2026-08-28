# Intelligence I42 — unified verified tradeoff routing

Date: 2026-08-28

## Added

~~~text
tools/intelligence/verify_tradeoff_route.py
tools/intelligence/unified_tradeoff_route_selftest.py
docs/specs/0043-intelligence-unified-tradeoff-routing.md
~~~

## Routing

~~~text
variant.model*     → I38
variant.execution.* → I41
other variables     → BLOCKED
~~~

The caller cannot override the route.

## Negative cases

The self-test blocks:
- execution evidence without its variable contract;
- model evidence with irrelevant execution contract input;
- a runtime-variable Experiment 61 pair;
- tampered joint evidence.

## Output boundary

The verified envelope contains route/provenance SHA metadata only.

It does not duplicate performance/quality numbers or emit a recommendation.
