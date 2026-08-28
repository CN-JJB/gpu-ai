# Current State

## Source of truth

- Repo: CN-JJB/gpu-ai
- Branch: main
- Stable course and dynamic intelligence remain separate.

## Stable course

~~~text
Slices 01–49 implemented
Experiments 01–93 exist
Stable v1 mainline complete
~~~

## Active Phase 4 frontier

~~~text
I01 catalog + benchmark bridge
I02 compatibility preflight
I03 exact measured compatibility
I04 comparable benchmark view
I05 explicit price/performance
I06 evidence-linked TCO
I07 real benchmark intake
I08 four-ecosystem documented compatibility
I09 compatibility matrix
I10 freshness queue
I11 real MEDIAN_ASK cohort
I12 market evidence audit
I13 sold-marked listing cohort
I14 cross-market signal comparison
I15 China secondary watch
I16 stable M0–M3 market evidence selection gate
I17 freshness-aware watchlist gate
I18 append-only market refresh lineage
I19 reusable market refresh helper + CI self-test
~~~

## Benchmark boundary

~~~text
real production benchmark rows = 0
~~~

Required admission:

~~~text
Experiment 61 manifest
+ raw result
+ PACKET.json
+ canonical IDs
→ I07 READY
→ ingest
→ validate
→ exact MEASURED_SUPPORTED
~~~

## Market evidence grades

~~~text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
~~~

Current production count after I18:

~~~text
M1=3
M2=3
M3=9
market observations=15
~~~

One M1 A770 record is historical/superseded.

## Current active market signals

### eBay active asks

~~~text
RTX 3090      1499 USD
RX 7900 XTX   1020 USD
Arc A770       330 USD
~~~

### OfferUp SOLD-marked displayed medians

~~~text
RTX 3090      950 USD
RX 7900 XTX   700 USD
Arc A770      200 USD
~~~

Every OfferUp row remains:

~~~text
confirmed_transaction_price=false
~~~

### China secondary watch

Current active records:

~~~text
RTX 3090 → 7400 CNY
Arc A770 → 1400 CNY
~~~

Historical A770 record:

~~~text
2026-08-21 → 1450 CNY
superseded_by
2026-08-25 → 1400 CNY
~~~

The current 1400 CNY observation is still M1 secondary evidence:
- direct_listing_capture=false;
- confirmed_sale=false;
- revalidate_after=2026-09-01.

## I17 freshness-aware purchase use

~~~text
CURRENT + M2/M3 → ELIGIBLE
CURRENT + M0/M1 → NEEDS-STRONGER-MARKET-EVIDENCE
DUE-TODAY → REVALIDATE-NOW
STALE → STALE-REVALIDATE
UNSCHEDULED / INVALID → REVALIDATION-SCHEDULE-REQUIRED
~~~

Experiment 38 blocks due-today/stale/unknown/invalid market evidence from BUY-CANDIDATE.

## I18 append-only refresh

Refresh does not overwrite old market evidence.

Lineage:

~~~text
old.superseded_by = new
new.supersedes = old
~~~

Default behavior:
- market_matrix hides superseded rows;
- freshness_report removes superseded rows from active revalidation queue;
- market_evidence_gate returns SUPERSEDED-USE-NEWER-OBSERVATION.

Audit history remains available with:

~~~text
--include-superseded
~~~

Validator checks:
- reference existence;
- reciprocal lineage;
- same hardware_id;
- newer timestamp;
- no self-reference;
- no cycle.

## Latest CI

GitHub Actions:

~~~text
workflow: Intelligence Self-Test
run #67
run id 33154549739
head 8ab1d5435e867570c2a5c2a48cc94d45c533179f
job id 98794100639
conclusion success
~~~

Result:

~~~text
SELFTEST: PASS
~~~

Log/steps explicitly confirm:
- the original full Intelligence self-test still passes;
- the reusable market refresh helper compiles;
- the dedicated market refresh self-test passes;
- reciprocal lineage is created without deleting history;
- already-superseded tails, cross-hardware links and non-newer dates are rejected.

Evidence:
- examples/evidence/intelligence-17-freshness-aware-watchlist.md
- examples/evidence/intelligence-18-append-only-market-refresh.md
- examples/evidence/intelligence-19-market-refresh-helper.md

## Next

1. Use market_refresh.py for future due/stale observation replacement instead of manual lineage edits.
2. Refresh RTX 3090 China secondary evidence when a stronger/newer source is available; current public evidence remains M1 around 7400 CNY.
3. Acquire the first real Experiment 61 Evidence Packet.
4. Add stronger direct/confirmed transaction evidence only when auditable.
5. Delay recommendation/ranking until real benchmark + quality/SLO + feasibility Evidence exists.
