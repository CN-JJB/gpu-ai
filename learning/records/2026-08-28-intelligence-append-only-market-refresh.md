# Learning / Build Record — 2026-08-28 Append-Only Market Refresh

## Frontier

Phase 4 Intelligence Stations — I18.

## Implemented

Spec:
- docs/specs/0019-intelligence-append-only-market-refresh-lineage.md

Dynamic snapshot:
- intelligence/market/china-a770-refresh-2026-08-28.md

Updated:
- intelligence/catalog/market.jsonl
- tools/intelligence/freshness_report.py
- tools/intelligence/market_evidence_gate.py
- tools/intelligence/market_matrix.py
- tools/intelligence/validate_catalog.py
- tools/intelligence/selftest.py

Evidence:
- examples/evidence/intelligence-18-append-only-market-refresh.md

## Important correction

The current 2026-08-25 A770 source supports an approximately 1400 CNY asking/listing signal, not the previously summarized 1200–1600 range.

The implementation follows the source rather than the stale internal summary.

## Stable rule

```text
refresh
!=
overwrite history
```

and:

```text
superseded
!=
false
```

## CI

```text
run #62
SELFTEST: PASS
```

## Next

Continue using append-only lineage for future dynamic refreshes.

Do not build a price trend from two weak secondary points as if they were normalized comparable transactions.
