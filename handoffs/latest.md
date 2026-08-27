# Handoff — GPU × Local LLM Course / Intelligence Stations

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Stable course

```text
Slices 01–49 implemented
Experiments 01–93 exist
Stable v1 mainline complete
```

Stable decision semantics:

```text
known required FAIL → REVISE
critical UNKNOWN / missing evidence → BLOCKED
all required gates PASS → ACCEPT
```

No weighted score may average away a hard gate.

## Phase 4 frontier

Implemented:

```text
I01 catalog / benchmark bridge
I02 compatibility preflight
I03 exact measured compatibility
I04 comparable benchmark view
I05 explicit price/performance
I06 TCO
I07 real benchmark intake
I08 four-ecosystem documented coverage
I09 compatibility matrix
I10 freshness queue
I11 real MEDIAN_ASK cohort
I12 market evidence audit
```

## Current compatibility coverage

```text
RTX 3090 / CUDA  → NEEDS-TEST
RX 7900 XTX / HIP → NEEDS-TEST
M4 Max / Metal → NEEDS-TEST
Arc A770 / SYCL → NEEDS-TEST
```

All are DOCUMENTED_SUPPORTED, not MEASURED_SUPPORTED.

## Real benchmark boundary

Production benchmark catalog remains empty.

Required future chain:

```text
manifest
+ raw result
+ PACKET.json
+ canonical IDs
→ I07 READY
→ ingest
→ validate
→ exact measured compatibility
```

Do not create production tok/s from prose or estimates.

## Current market cohort

Three current global used-GPU observations share:

```text
GLOBAL-EBAY
secondary-aggregated-ebay-active
used-consumer
used
MEDIAN_ASK
USD
```

Values:

```text
RTX 3090      1499
RX 7900 XTX   1020
Arc A770 16G   330
```

These are ask prices, not confirmed sales.

## Market evidence audit

Preserved source evidence:

```text
RTX 3090      active=47  middle-half=1400–1520  BROAD-SAMPLE
RX 7900 XTX   active=23  middle-half=997–1080   LIMITED-SAMPLE
Arc A770 16G  active=8   middle-half=325–347    SMALL-SAMPLE
```

All have:

```text
confirmed_sale=false
ASK-ONLY
```

MEDIAN_ASK now requires sample/method/export metadata in the production validator.

## Verification status

Full Python self-test:

```text
I01–I10 → SELFTEST: PASS
```

I11–I12:
- exact latest-main blobs checked;
- contract-equivalent execution passed;
- self-test assertions present;
- fresh full Python repository run not repeated because local execution timed out/rate-limited.

Do not claim a fresh I11–I12 Python PASS until it is actually recorded.

## Freshness

I10 remains authoritative:

```text
STALE
DUE-TODAY
DUE-SOON
FRESH
```

STALE means revalidate, not automatically false.

Current eBay ask rows use 7-day revalidation windows.

## Next work

1. Add a separate, auditable local-market or confirmed-sale cohort if reliable evidence can be obtained.
2. Ingest real benchmark Evidence only after I07 READY.
3. Refresh due/stale records rather than overwriting history.
4. Re-run full Python self-test when possible.
5. Delay recommendation/ranking until real benchmark/quality/SLO/feasibility evidence exists.

No auto-purchase or unsafe hardware modification.
