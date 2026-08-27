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