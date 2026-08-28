# Handoff — GPU × Local LLM Course / Intelligence Stations

## Repo

- CN-JJB/gpu-ai
- main

## Stable course

```text
Slices 01–49
Experiments 01–93
v1 stable mainline complete
```

## Phase 4 frontier

```text
I01–I17 implemented and CI verified
```

## Latest CI

```text
run #54
run id 33137613634
head bbf624e44579cbc765974bf8b5070330002f294e
job id 98741045301
SELFTEST: PASS
```

## Market evidence gate

```text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
```

M3 is claim-scoped.

## Freshness gate

```text
CURRENT + M2/M3 → ELIGIBLE
DUE-TODAY → REVALIDATE-NOW
STALE → STALE-REVALIDATE
UNSCHEDULED / INVALID → REVALIDATION-SCHEDULE-REQUIRED
```

Every real market row requires revalidate_after.

## Experiment 38 fix

Old possible state:

```text
BUY-CANDIDATE + stale=YES
```

is no longer allowed.

CI verifies:
- current evidence can produce BUY-CANDIDATE;
- due-today/stale/invalid evidence produces NEEDS EVIDENCE.

## Current market signals

```text
eBay active asks:
3090 1499
7900 XTX 1020
A770 330 USD

OfferUp SOLD-marked displayed medians:
3090 950
7900 XTX 700
A770 200 USD

China secondary:
3090 7400
A770 1450 CNY
```

## Active next defect/data need

The newer China A770 source reports a range:

```text
1200–1600 CNY
```

not a scalar.

Do not invent a midpoint merely to satisfy the current scalar market schema.

I18 should add:
- range-valued SECONDARY_REPORTED support;
- append-only refresh lineage;
- superseded observations excluded from active refresh/purchase use while history remains preserved.

## Benchmark boundary

Production benchmark catalog remains empty until real Experiment 61 Evidence passes I07.

No auto-purchase or unsafe hardware modification.
