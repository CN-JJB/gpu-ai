# Current State

## Source of truth

- Repo: CN-JJB/gpu-ai
- Branch: main
- Stable course and dynamic intelligence are separate layers.

## Stable course frontier

```text
Slices 01–49 implemented
Experiments 01–93 exist
Stable v1 mainline complete
```

Do not extend stable Lessons merely to store volatile price, compatibility or benchmark data.

## Active frontier — Phase 4 Intelligence Stations

Implemented frontier:

```text
I01 catalog + benchmark bridge
I02 compatibility preflight
I03 exact measured compatibility ingestion
I04 comparable benchmark view
I05 explicit price/performance
I06 evidence-linked TCO
I07 real benchmark intake gate
I08 four-ecosystem documented compatibility
I09 compatibility coverage matrix
I10 freshness / revalidation queue
I11 explicit real MEDIAN_ASK market cohort
I12 market sample/method evidence audit
```

These are Intelligence Stations, not stable Slice 50–61.

## Compatibility state

For Qwen3-8B + llama.cpp:

```text
RTX 3090 / CUDA  → DOCUMENTED_SUPPORTED → NEEDS-TEST
RX 7900 XTX / HIP → DOCUMENTED_SUPPORTED → NEEDS-TEST
M4 Max / Metal → DOCUMENTED_SUPPORTED → NEEDS-TEST
Arc A770 / SYCL → DOCUMENTED_SUPPORTED → NEEDS-TEST
```

No production PP/TG exists for these paths.

## Real benchmark admission

Required chain:

```text
Experiment 61 manifest
+ raw llama-bench result
+ PACKET.json
+ canonical hardware/model/runtime IDs
→ I07 INTAKE: READY
→ ingest benchmark
→ validate
→ derive exact MEASURED_SUPPORTED
→ validate again
```

Repository search found no real Experiment 61-compatible bundle.

Therefore:

```text
intelligence/catalog/benchmarks.jsonl
= intentionally empty
```

## Market state

Production market observations now include two deliberately separate evidence contracts.

Existing China secondary signal:

```text
CN
secondary-summary
used-consumer
working-unverified
SECONDARY_REPORTED
CNY
```

Current same-cohort global used asking data:

```text
GLOBAL-EBAY
secondary-aggregated-ebay-active
used-consumer
used
MEDIAN_ASK
USD
```

Current dated asks:

```text
RTX 3090      1499 USD
RX 7900 XTX   1020 USD
Arc A770 16G   330 USD
```

These are asking prices, not confirmed sales.

## Market sample/method evidence

I12 preserves:

```text
active listing count
middle-half asking range
methodology
source export timestamp
confirmed_sale=false
freshness
```

Current source samples:

```text
RTX 3090
47 active
1400–1520
→ BROAD-SAMPLE

RX 7900 XTX
23 active
997–1080
→ LIMITED-SAMPLE

Arc A770 16GB
8 active
325–347
→ SMALL-SAMPLE
```

These sample bands are descriptive heuristics, not confidence scores.

Production MEDIAN_ASK rows now fail validation if sample/method evidence is missing or if confirmed_sale is not false.

## Benchmark / price / TCO guardrails

Comparable benchmark requires:

```text
same model_id
+ exact artifact SHA
+ quant
+ workload
```

Price/performance additionally requires explicit market-record selection and one matching market contract.

TCO:

```text
purchase
+ platform delta
+ electricity
+ risk reserve
- resale
→ scenario TCO
```

Neither price/performance nor TCO can rescue a failed capacity/support/safety/quality gate.

## Freshness

I10 states:

```text
STALE != FALSE
```

STALE means revalidate before current use.

The eBay ask observations use a 7-day revalidation horizon.

## Verification levels

### Full Python execution

Verified through I10 on 2026-08-28:

```bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
```

Result:

```text
SELFTEST: PASS
```

### I11–I12 exact-main verification

After the market additions, local full-repository execution timed out/rate-limited.

I11–I12 were therefore checked directly against latest GitHub blobs with contract-equivalent execution.

I11 confirmed:
- 3 market rows;
- 1 complete contract;
- all hardware IDs resolve;
- 330 / 1020 / 1499 USD;
- current freshness as of 2026-08-28;
- self-test assertions present.

I12 confirmed:
- BROAD=1 / LIMITED=1 / SMALL=1;
- all medians inside their recorded middle-half ranges;
- confirmed_sale=false on all three;
- MEDIAN_ASK validator gate present;
- malformed-sample rejection assertion present.

Do not call I11–I12 a newly re-run full Python PASS until that execution is recorded.

## Current production catalog

```text
hardware entities:      4
model entities:         1
runtime entities:       1
market observations:    4
compatibility rows:     4
real benchmark rows:    0
```

## Evidence

- examples/evidence/intelligence-07-real-benchmark-intake.md
- examples/evidence/intelligence-08-cross-vendor-documented-coverage.md
- examples/evidence/intelligence-09-compatibility-coverage-matrix.md
- examples/evidence/intelligence-10-freshness-revalidation.md
- examples/evidence/intelligence-11-market-cohort-coverage.md
- examples/evidence/intelligence-12-market-evidence-audit.md

## Next actions

1. Add stronger local-market or confirmed-sale evidence while preserving a separate contract.
2. Acquire/receive the first real Experiment 61 packet and require I07 READY.
3. Refresh observations when I10 marks them due/stale.
4. Repeat full Python self-test when the execution path is available.
5. Build recommendation views only after real comparable benchmark + quality/SLO + feasibility Evidence exists.
