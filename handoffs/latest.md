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
I01–I16 implemented and full-CI verified
```

## CI

GitHub Actions run #48:

```text
head 097c8d4839314851e1f4b07267b3c7b2102d50e0
run id 33137329016
job id 98740118394
Python 3.12.14
SELFTEST: PASS
```

The successful log includes all I11–I16 market assertions and negative validator cases.

## Compatibility

```text
3090/CUDA    → NEEDS-TEST
7900XTX/HIP  → NEEDS-TEST
M4Max/Metal  → NEEDS-TEST
A770/SYCL    → NEEDS-TEST
```

No real benchmark Evidence yet.

## Benchmark admission

```text
manifest + raw result + PACKET + canonical IDs
→ I07 READY
→ ingest
→ validate
→ exact MEASURED_SUPPORTED
```

Production benchmark catalog remains empty.

## Market evidence states

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

Experiment 38 market sub-gate:

```text
M0/M1 → NEEDS STRONGER
M2/M3 → ELIGIBLE
```

M3 remains claim-scoped. Current OfferUp rows do not prove actual transaction amount.

## Current market signals

```text
eBay asks:
3090 1499
7900 XTX 1020
A770 330 USD

OfferUp SOLD-marked displayed medians:
3090 950
7900 XTX 700
A770 200 USD

China secondary watch:
3090 7400
A770 1450 CNY
```

## Freshness gap discovered

Experiment 38 currently prints stale age but its decision status is computed before freshness.

Therefore a stale M2/M3 observation can still appear as BUY-CANDIDATE.

This is the active I17 defect to fix.

## Next work

1. I17: freshness-aware watchlist market gate.
2. Refresh due/stale dynamic observations.
3. Ingest real benchmark only after I07 READY.
4. No recommendation leaderboard yet.

No auto-purchase or unsafe hardware modification.
