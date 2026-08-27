# Learning / Build Record — 2026-08-28 Real Market Cohort

## Frontier

Phase 4 Intelligence Stations — I11.

## Implemented

Spec:
- docs/specs/0012-intelligence-market-cohort-coverage.md

Tool:
- tools/intelligence/market_matrix.py

Dynamic snapshot:
- intelligence/market/ebay-used-gpu-asking-cohort-2026-08-28.md

Production observations:
- RTX 3090;
- RX 7900 XTX;
- Arc A770 16GB.

## Stable rule

```text
same currency
!=
same market evidence
```

Comparable market rows require the same:
- geography;
- channel;
- cohort;
- condition;
- price state;
- currency.

## Verification

Latest-main contract verification confirms:
- 3 observations;
- 1 contract;
- all hardware IDs resolve;
- current freshness on 2026-08-28.

Do not call these confirmed sales.