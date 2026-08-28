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

## Intelligence decision-readiness path

Experiment 38 now has machine-readable Phase 4 companions.

### Performance target

Copy:

~~~text
performance-target-policy.template.json
~~~

Then use I46/I47 to evaluate explicit PP/TG/PPL hard thresholds.

No weighted score is used.

### Personal price ceiling

Copy:

~~~text
price-ceiling-policy.template.json
~~~

I48 preserves the existing max-sticker/watch-band arithmetic but uses neutral outputs:

~~~text
WITHIN-CEILING
WATCH-BAND
ABOVE-BAND
~~~

WITHIN-CEILING is not BUY.

### Condition evidence

Stable C-grade semantics now live in:

~~~text
reference/hardware/condition-evidence-grades.md
~~~

I50 defines C3 as learner-owned, PACKET-bound, independently reproducible I44 technical evidence.

The evidence grade is separate from the card-health decision:

~~~text
C3 provenance
+
I44 ACCEPT
~~~

are separate requirements.

### Final evidence matrix

I43 combines the independent evidence components and may return:

~~~text
READY-FOR-HUMAN-REVIEW
~~~

It never performs a purchase.
