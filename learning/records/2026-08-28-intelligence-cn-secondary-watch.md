# Learning / Build Record — 2026-08-28 China Secondary Watch

## Frontier

Phase 4 Intelligence Stations — I15.

## Implemented

Spec:
- docs/specs/0016-intelligence-cn-secondary-watch-signals.md

Dynamic snapshot:
- intelligence/market/china-secondary-watch-2026-08-28.md

Updated:
- intelligence/catalog/market.jsonl
- tools/intelligence/validate_catalog.py
- tools/intelligence/selftest.py

Evidence:
- examples/evidence/intelligence-15-cn-secondary-watch.md

## Stable rule

~~~text
secondary market article
→ watch signal
~~~

not:

~~~text
secondary market article
→ sold-price truth
~~~

## Current watch

~~~text
RTX 3090  → 7400 CNY
Arc A770  → 1450 CNY
~~~

Both are unverified-condition secondary signals.

## Verification

Exact latest-main contract verification passed for:
- row count;
- contract identity;
- price values;
- non-direct / non-confirmed semantics;
- validator/self-test guardrails.
