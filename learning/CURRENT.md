# Current State

## Source of truth

- Repo: CN-JJB/gpu-ai
- Branch: main
- Stable course and dynamic intelligence remain separate.

## Stable course

```text
Slices 01–49 implemented
Experiments 01–93 exist
Stable v1 mainline complete
```

## Active Phase 4 frontier

```text
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
```

## Benchmark boundary

```text
real production benchmark rows = 0
```

Required admission:

```text
Experiment 61 manifest
+ raw result
+ PACKET.json
+ canonical IDs
→ I07 READY
→ ingest
→ validate
→ exact MEASURED_SUPPORTED
```

## Market evidence grades

```text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
```

Current counts:

```text
M1=2
M2=3
M3=9
```

M3 remains claim-scoped and does not imply a confirmed transaction amount.

## Freshness-aware market eligibility

I17 requires:

```text
market grade
+
freshness
```

Current mapping:

```text
CURRENT + M2/M3
→ ELIGIBLE

CURRENT + M0/M1
→ NEEDS-STRONGER-MARKET-EVIDENCE

DUE-TODAY
→ REVALIDATE-NOW

STALE
→ STALE-REVALIDATE

UNSCHEDULED / INVALID
→ REVALIDATION-SCHEDULE-REQUIRED
```

Every real market record now requires revalidate_after.

Experiment 38 was corrected so due-today/stale/unknown/invalid price evidence cannot remain BUY-CANDIDATE.

## Experiment 38 deterministic test

The CI self-test proves:

```text
CURRENT + PASS + M2 + C3 + under ceiling
→ BUY-CANDIDATE

DUE-TODAY
→ NEEDS EVIDENCE

STALE
→ NEEDS EVIDENCE

INVALID revalidate_after
→ NEEDS EVIDENCE
```

## CI

Latest verified Intelligence run:

```text
workflow: Intelligence Self-Test
run #54
run id 33137613634
head bbf624e44579cbc765974bf8b5070330002f294e
job id 98741045301
Python 3.12.14
Ubuntu 24.04.4
conclusion success
```

Log:

```text
SELFTEST: PASS
- market evidence eligibility is freshness-aware and all real market rows require revalidation dates
- Experiment 38 blocks due-today, stale and invalid market evidence from BUY-CANDIDATE
```

Evidence:
- examples/evidence/intelligence-17-freshness-aware-watchlist.md

## Current production market signals

### eBay active asks

```text
RTX 3090      1499 USD
RX 7900 XTX   1020 USD
Arc A770       330 USD
```

### OfferUp sold-marked displayed medians

```text
RTX 3090      950 USD
RX 7900 XTX   700 USD
Arc A770      200 USD
```

All nine OfferUp rows now revalidate on 2026-09-04.

### China secondary watch

```text
RTX 3090 → 7400 CNY
Arc A770 → 1450 CNY
```

The A770 2026-08-21 scalar observation reaches its revalidation boundary on 2026-08-28.

## Next

1. I18: append a newer A770 China range observation without inventing a midpoint.
2. Preserve observation history with explicit refresh lineage so old records do not remain forever in the active revalidation queue.
3. Acquire first real Experiment 61 Evidence Packet.
4. Delay ranking/recommendation until real benchmark + quality/SLO + feasibility Evidence exists.
