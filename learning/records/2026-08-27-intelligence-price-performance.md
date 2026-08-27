# Learning / Build Record — 2026-08-27 Explicit Price / Performance

## Frontier

Phase 4 Intelligence Stations — I05.

## Implemented

Spec:
- docs/specs/0006-intelligence-explicit-price-performance.md

Tool:
- tools/intelligence/price_performance.py

Fixture:
- second same-cohort synthetic market observation.

Self-test verifies:
- same benchmark comparison group;
- explicit market record selection;
- same market contract;
- expected fixture arithmetic.

## Stable rule

~~~text
latest visible price
!=
valid price/performance denominator
~~~

The exact market observation is part of the comparison evidence.