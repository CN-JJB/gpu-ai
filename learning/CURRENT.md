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
```

## Compatibility

For Qwen3-8B + llama.cpp:

```text
RTX 3090 / CUDA   → NEEDS-TEST
RX 7900 XTX / HIP → NEEDS-TEST
M4 Max / Metal    → NEEDS-TEST
Arc A770 / SYCL   → NEEDS-TEST
```

All are DOCUMENTED_SUPPORTED, not MEASURED_SUPPORTED.

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

## Market contracts

### GLOBAL-EBAY active asks

```text
MEDIAN_ASK / USD
RTX 3090      1499
RX 7900 XTX   1020
Arc A770 16G   330
```

Samples:

```text
3090      47 → BROAD-SAMPLE
7900 XTX  23 → LIMITED-SAMPLE
A770       8 → SMALL-SAMPLE
```

Grade:

```text
M2
```

### OfferUp SOLD-marked pages

```text
SOLD_MARKED_LISTING_PRICE / USD
3090      median displayed 950
7900 XTX  median displayed 700
A770      median displayed 200
```

Every row remains:

```text
confirmed_transaction_price=false
```

Grade:

```text
M3
```

M3 is claim-scoped to the direct page state/displayed price; it does not prove the negotiated transaction amount.

### China secondary watch

```text
SECONDARY_REPORTED / CNY
3090 7400
A770 1450
```

Both:

```text
direct_listing_capture=false
confirmed_sale=false
```

Grade:

```text
M1
```

## I16 Experiment 38 bridge

Stable market evidence grades are reused:

```text
M3 direct normalized platform evidence
M2 transparent current secondary aggregation
M1 weak/article summary
M0 unknown
```

Current production count:

```text
M1=2
M2=3
M3=9
```

Experiment 38 bridge:

```text
M0/M1 → NEEDS-STRONGER-MARKET-EVIDENCE
M2/M3 → market-evidence component ELIGIBLE
```

This does not satisfy FIT, SOFTWARE, PERFORMANCE, CONDITION or price-ceiling gates.

## Full verification

GitHub Actions run #48:

```text
run id = 33137329016
head = 097c8d4839314851e1f4b07267b3c7b2102d50e0
job id = 98740118394
Ubuntu 24.04.4
Python 3.12.14
conclusion = success
```

Executed:

```bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
```

Result:

```text
SELFTEST: PASS
```

This closes the previous I11–I16 full-Python verification debt.

Evidence:
- examples/evidence/intelligence-i01-i16-ci-selftest.md
- examples/evidence/intelligence-16-market-evidence-selection-gate.md

## Production catalog counts

```text
hardware:       4
models:         1
runtimes:       1
market:        14
compatibility:  4
real benchmark: 0
```

## Next

1. Make Experiment 38/watchlist market evidence freshness-aware.
2. Refresh due/stale market records through I10.
3. Acquire first real Experiment 61 Evidence Packet.
4. Add stronger direct/confirmed transaction evidence only if auditable.
5. Delay ranking/recommendation until real benchmark + quality/SLO + feasibility Evidence exists.
