# Learning / Build Record — 2026-08-28 Freshness-Aware Watchlist

## Frontier

Phase 4 Intelligence Stations — I17.

## Implemented

Spec:
- docs/specs/0018-intelligence-freshness-aware-watchlist-gate.md

Updated:
- tools/intelligence/market_evidence_gate.py
- tools/intelligence/validate_catalog.py
- tools/intelligence/selftest.py
- intelligence/catalog/market.jsonl
- labs/experiments/38-real-candidate-watchlist/evaluate_watchlist.py
- labs/experiments/38-real-candidate-watchlist/watchlist-template.csv
- labs/experiments/38-real-candidate-watchlist/EXPECTED.md
- labs/experiments/38-real-candidate-watchlist/INTELLIGENCE-BRIDGE.md

Evidence:
- examples/evidence/intelligence-17-freshness-aware-watchlist.md

## Stable correction

Old behavior could produce:

~~~text
BUY-CANDIDATE + stale=YES
~~~

New behavior:

~~~text
stale/due/invalid market evidence
→ NEEDS EVIDENCE
~~~

unless a harder failure already yields SKIP.

## CI

~~~text
run #54
bbf624e44579cbc765974bf8b5070330002f294e
SELFTEST: PASS
~~~

## Next

The Arc A770 China secondary observation reaches its revalidation boundary on 2026-08-28.

The next useful work is to refresh it with newer auditable evidence rather than merely leaving it marked due.
