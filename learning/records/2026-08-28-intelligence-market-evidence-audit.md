# Learning / Build Record — 2026-08-28 Market Evidence Audit

## Frontier

Phase 4 Intelligence Stations — I12.

## Implemented

Spec:
- docs/specs/0013-intelligence-market-evidence-audit.md

Tool:
- tools/intelligence/market_evidence_audit.py

Updated:
- intelligence/catalog/market.jsonl
- tools/intelligence/validate_catalog.py
- tools/intelligence/selftest.py

Evidence:
- examples/evidence/intelligence-12-market-evidence-audit.md

## Stable rule

```text
market price
→ preserve sample + method + ask/sale semantics + freshness
```

Do not collapse all market evidence into one confidence score.

## Current sample bands

```text
RTX 3090      → BROAD-SAMPLE
RX 7900 XTX   → LIMITED-SAMPLE
Arc A770 16GB → SMALL-SAMPLE
```

All remain ASK-ONLY, not confirmed sales.