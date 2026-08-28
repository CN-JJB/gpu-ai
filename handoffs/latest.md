# Handoff — GPU × Local LLM Course / Intelligence Stations

## Repo

- CN-JJB/gpu-ai
- main

## Stable course

~~~text
Slices 01–49
Experiments 01–93
v1 stable mainline complete
~~~

## Phase 4 frontier

~~~text
I01–I19 implemented and CI verified
~~~

## Latest CI

~~~text
run #67
run id 33154549739
head 8ab1d5435e867570c2a5c2a48cc94d45c533179f
job id 98794100639
full SELFTEST: PASS
market refresh SELFTEST: PASS
~~~

## Benchmark boundary

Production benchmark catalog remains empty.

Required:

~~~text
manifest + raw result + PACKET + canonical IDs
→ I07 READY
→ ingest
→ validate
→ exact MEASURED_SUPPORTED
~~~

## Market evidence

~~~text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
~~~

Current active signals:

~~~text
eBay asks:
3090 1499
7900 XTX 1020
A770 330 USD

OfferUp SOLD-marked displayed medians:
3090 950
7900 XTX 700
A770 200 USD

China secondary:
3090 7400
A770 1400 CNY
~~~

## A770 append-only refresh

Historical:

~~~text
2026-08-21
1450 CNY
~~~

Current:

~~~text
2026-08-25
1400 CNY
revalidate_after=2026-09-01
~~~

Lineage:

~~~text
old.superseded_by = new
new.supersedes = old
~~~

The old row remains audit history but is not current purchase evidence.

## Active-view semantics

~~~text
market_matrix
→ hides superseded by default

freshness_report
→ SUPERSEDED, not active stale queue

market_evidence_gate
→ SUPERSEDED-USE-NEWER-OBSERVATION
~~~

Use --include-superseded for audit history.

## Watchlist freshness

~~~text
CURRENT + M2/M3 → ELIGIBLE
DUE/STALE/INVALID → not purchase-eligible
~~~

Experiment 38 cannot emit BUY-CANDIDATE from stale/due/invalid market evidence.

## I19 reusable refresh helper

```text
tools/intelligence/market_refresh.py
```

Use a complete new observation candidate plus the active old record.

The helper creates reciprocal append-only lineage and rejects:
- already-superseded forks;
- cross-hardware links;
- non-newer observations.

CI run #67 verifies the helper and keeps the original full self-test green.

## Next work

1. Use the helper for the next due/stale market refresh.
2. Find stronger/newer RTX 3090 China evidence; do not promote the current 7400 CNY M1 signal without stronger provenance.
3. Ingest real benchmark only after I07 READY.
4. No recommendation leaderboard yet.

No auto-purchase or unsafe hardware modification.
