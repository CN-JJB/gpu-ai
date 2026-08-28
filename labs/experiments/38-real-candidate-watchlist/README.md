# Experiment 38 — Real Candidate Watchlist

硬件等级：L0

## Goal

Maintain a manual, auditable watchlist for actual used-hardware candidates.

## Files

- `watchlist-template.csv`
- `evaluate_watchlist.py`
- `RESULT-TEMPLATE.md`

## Workflow

1. Define one workload card.
2. Calculate one scenario max sticker price.
3. Add multiple candidate alternatives.
4. For each row record:
   - exact model；
   - ask；
   - price state；
   - observed_at；
   - market evidence；
   - condition evidence；
   - fit/software/performance state。
5. Run evaluator.
6. Refresh stale price observations before paying.

## Intelligence bridge

If the candidate price comes from the Phase 4 Intelligence catalog, use:

- `INTELLIGENCE-BRIDGE.md`
- `tools/intelligence/market_evidence_gate.py`

Copy the catalog's claim-scoped `market_evidence_grade` into this lab's `market_evidence` field.

Do not infer a stronger grade from words such as "SOLD".

## No scraping requirement

Manual entries are acceptable and often safer than brittle scraping.

The evaluator never buys anything.

## Suggested refresh

For hot consumer GPUs:
```
7 days
```

For an imminent purchase:
```
refresh within 24–48h
```

when practical.