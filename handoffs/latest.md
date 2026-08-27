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
I01–I15 implemented
```

Verification split:
- I01–I10: full Python SELFTEST PASS;
- I11–I15: exact-main contract verified; fresh full Python rerun still owed.

## Compatibility

```text
3090/CUDA    → NEEDS-TEST
7900XTX/HIP  → NEEDS-TEST
M4Max/Metal  → NEEDS-TEST
A770/SYCL    → NEEDS-TEST
```

No production benchmark Evidence yet.

## Benchmark admission

```text
manifest + raw result + PACKET + canonical IDs
→ I07 READY
→ ingest
→ validate
→ exact MEASURED_SUPPORTED
```

Production benchmark catalog remains empty.

## Market evidence

### Active eBay median asks

```text
3090 1499 USD
7900 XTX 1020 USD
A770 330 USD
```

Ask-only; not confirmed sales.

### Sample evidence

```text
3090 47 listings → BROAD-SAMPLE
7900 XTX 23 → LIMITED-SAMPLE
A770 8 → SMALL-SAMPLE
```

### OfferUp sold-marked listing pages

Displayed-price medians:

```text
3090 950 USD
7900 XTX 700 USD
A770 200 USD
```

Pages are SOLD-marked, but actual transaction amount remains unknown.

### Cross-contract gap

```text
3090 -36.6%
7900 XTX -31.4%
A770 -39.4%
```

Not a transaction discount.

### China secondary watch

```text
3090 7400 CNY
A770 1450 CNY
```

Secondary reported only; no direct sample or confirmed sale.

## Market semantic validator

Production validation now rejects:
- MEDIAN_ASK without sample/method evidence;
- MEDIAN_ASK claiming confirmed sale;
- SOLD_MARKED_LISTING_PRICE without SOLD/listing evidence;
- sold-marked row claiming confirmed transaction;
- SECONDARY_REPORTED claiming direct capture or confirmed sale.

## Freshness

I10 remains authoritative.

A770 China watch is DUE-TODAY on 2026-08-28.

## Next work

1. Obtain a complete repository execution path and rerun all intelligence Python tests.
2. Add stronger direct/local transaction evidence if auditable.
3. Ingest real benchmark only after I07 READY.
4. Do not build a recommendation leaderboard yet.

No auto-purchase or unsafe hardware modification.
