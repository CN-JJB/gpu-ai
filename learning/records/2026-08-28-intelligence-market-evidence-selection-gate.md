# Learning / Build Record — 2026-08-28 Market Evidence Selection Gate

## Frontier

Phase 4 Intelligence Stations — I16.

## Implemented

Spec:
- docs/specs/0017-intelligence-market-evidence-selection-gate.md

Tool:
- tools/intelligence/market_evidence_gate.py

Stable-lab bridge:
- labs/experiments/38-real-candidate-watchlist/INTELLIGENCE-BRIDGE.md

Updated:
- intelligence/catalog/market.jsonl
- tools/intelligence/fixtures/catalog/market.jsonl
- tools/intelligence/validate_catalog.py
- tools/intelligence/selftest.py

Evidence:
- examples/evidence/intelligence-16-market-evidence-selection-gate.md

## Reused stable grading

```text
M3 direct normalized platform evidence
M2 transparent current secondary aggregation
M1 weak/article summary
M0 unknown
```

No new confidence scale was created.

## Current bridge

```text
CN SECONDARY_REPORTED → M1 → NEEDS STRONGER
eBay MEDIAN_ASK → M2 → market sub-gate eligible
OfferUp SOLD-marked direct page → M3 → market sub-gate eligible
```

M3 remains claim-scoped.

## Stable decision rule

```text
market M2/M3
alone
!=
BUY-CANDIDATE
```

Experiment 38 still requires fit, software, performance, condition C3/C4 and price-ceiling gates.

## Verification

Exact latest-main contract verification passed for:
- grade counts;
- state/grade consistency;
- claim scopes;
- watchlist eligibility split;
- validator guardrails;
- self-test assertions.
