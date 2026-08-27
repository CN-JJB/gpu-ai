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
```

These are Intelligence Stations, not stable Lesson slices.

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

Real production benchmark rows:

```text
0
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
→ exact measured compatibility
```

No real packet currently exists in the repo.

## Market contracts

### GLOBAL-EBAY active asks

```text
GLOBAL-EBAY
secondary-aggregated-ebay-active
used-consumer
used
MEDIAN_ASK
USD
```

```text
RTX 3090      1499
RX 7900 XTX   1020
Arc A770 16G   330
```

Sample/method evidence:

```text
RTX 3090      47 active  range 1400–1520  BROAD-SAMPLE
RX 7900 XTX   23 active  range 997–1080   LIMITED-SAMPLE
Arc A770 16G   8 active  range 325–347    SMALL-SAMPLE
```

All are ASK-ONLY and confirmed_sale=false.

### US OfferUp sold-marked pages

```text
US
offerup-sold-marked-listing
used-consumer
used
SOLD_MARKED_LISTING_PRICE
USD
```

```text
RTX 3090      850 / 950 / 1050 → median displayed 950
RX 7900 XTX   580 / 700 / 800  → median displayed 700
Arc A770 16G  150 / 200 / 250  → median displayed 200
```

Every page is marked SOLD, but every record preserves:

```text
confirmed_transaction_price=false
```

### Cross-contract signal

```text
RTX 3090      → -36.6%
RX 7900 XTX   → -31.4%
Arc A770 16G  → -39.4%
```

This is an eBay-active-ask vs OfferUp-sold-marked-display gap.

It is not a confirmed transaction discount or fair-value discount.

### China secondary watch

```text
CN
secondary-summary
used-consumer
working-unverified
SECONDARY_REPORTED
CNY
```

```text
RTX 3090 → 7400 CNY
Arc A770 → 1450 CNY
```

Both preserve:

```text
direct_listing_capture=false
confirmed_sale=false
```

The A770 watch signal is due for revalidation on 2026-08-28.

## Freshness

```text
STALE != FALSE
```

STALE means revalidate before current use.

## Verification levels

### Full Python execution

I01–I10 were executed end-to-end on exact main content:

```text
SELFTEST: PASS
```

### I11–I15 exact-main contract verification

After the market expansions, the available local full-repo execution path timed out/rate-limited.

For I11–I15:
- latest GitHub blobs were read directly;
- contract-equivalent calculations/checks were executed;
- validator guardrails were inspected on exact blobs;
- self-test assertions were verified present.

Do not claim a fresh full Python PASS for I11–I15 until a real rerun is recorded.

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

1. Resolve the full-Python/CI rerun debt.
2. Add stronger direct-listing or confirmed-transaction evidence without collapsing contracts.
3. Acquire the first real Experiment 61 Evidence Packet.
4. Refresh due/stale observations through I10.
5. Delay recommendation ranking until real benchmark + quality/SLO + feasibility evidence exists.
