# Learning / Build Record — 2026-08-28 Sold-Marked Listing Evidence

## Frontier

Phase 4 Intelligence Stations — I13.

## Implemented

Spec:
- docs/specs/0014-intelligence-sold-marked-listing-evidence.md

Tool:
- tools/intelligence/sold_marked_market.py

Dynamic snapshot:
- intelligence/market/offerup-sold-marked-gpu-listings-2026-08-28.md

Updated:
- intelligence/catalog/market.jsonl
- tools/intelligence/validate_catalog.py
- tools/intelligence/selftest.py

Evidence:
- examples/evidence/intelligence-13-sold-marked-listings.md

## Stable rule

```text
listing marked SOLD
!=
confirmed transaction amount
```

Keep the platform state and the monetary certainty as separate fields.

## Current descriptive medians

```text
RTX 3090      → 950 USD
RX 7900 XTX   → 700 USD
Arc A770 16GB → 200 USD
```

These are displayed listing-price medians only.

## Verification

Exact latest-main contract verification passed for:
- 9 observations;
- 3 hardware groups;
- SOLD status;
- false transaction-confirmation flag;
- displayed-price consistency;
- validator/self-test guardrails.