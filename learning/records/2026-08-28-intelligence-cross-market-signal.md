# Learning / Build Record — 2026-08-28 Cross-Market Signal Comparison

## Frontier

Phase 4 Intelligence Stations — I14.

## Implemented

Spec:
- docs/specs/0015-intelligence-cross-market-signal-comparison.md

Tool:
- tools/intelligence/compare_market_contracts.py

Evidence:
- examples/evidence/intelligence-14-cross-market-signal.md

## Current descriptive gaps

```text
RTX 3090      → -36.6%
RX 7900 XTX   → -31.4%
Arc A770 16GB → -39.4%
```

The right side is the median displayed price of OfferUp pages marked SOLD.

It is not a confirmed transaction amount.

## Stable rule

```text
market-contract mismatch
can dominate a price conclusion
```

Therefore never hide the selected market contract inside a recommendation score.

## Verification

Exact latest-main contract verification passed for:
- 3 common hardware IDs;
- medians;
- percentage gaps;
- currency guardrail;
- descriptive-only semantics.