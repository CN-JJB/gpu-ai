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

The stable course ends with whole-machine feasibility and the Graduation Machine Design Capstone.

Do not extend stable Lessons merely to store volatile prices, compatibility or benchmark data.

## Active frontier — Phase 4 Intelligence Stations

Verified:

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
```

These are dynamic Intelligence Stations, not Slice 50–59.

## Current data model

```text
hardware entity
model entity
runtime entity
market observation
compatibility observation
benchmark observation
```

Core rule:

```text
stable-ish identity
+
dated/source-bound observation
```

Production files live under `intelligence/catalog/`.

## Compatibility semantics

```text
MEASURED_SUPPORTED     → PASS-MEASURED
DOCUMENTED_SUPPORTED   → NEEDS-TEST
PARTIAL / EXPERIMENTAL → REVIEW
DOCUMENTED_UNSUPPORTED → FAIL
UNKNOWN / no match     → BLOCKED
stale                  → STALE-REVALIDATE
```

Explicit UNKNOWN is valid.

Documentation does not become measured PASS.

## Four-ecosystem production coverage

For Qwen3-8B + llama.cpp, current dated production observations cover:

```text
NVIDIA GeForce RTX 3090 24GB → CUDA  → NEEDS-TEST
AMD Radeon RX 7900 XTX 24GB  → HIP   → NEEDS-TEST
Apple M4 Max 40-core / 64GB  → Metal → NEEDS-TEST
Intel Arc A770 16GB           → SYCL  → NEEDS-TEST
```

No production PP/TG has been attached to these rows.

## Real benchmark admission

Required chain:

```text
Experiment 61 manifest
+ raw llama-bench result
+ PACKET.json
+ canonical hardware/model/runtime IDs
→ I07 INTAKE: READY
→ ingest benchmark
→ validate catalog
→ derive exact MEASURED_SUPPORTED
→ validate again
```

Repository search found no existing real Experiment 61-compatible bundle.

Therefore:

```text
intelligence/catalog/benchmarks.jsonl
= intentionally empty
```

Missing real Evidence remains missing.

## Comparable benchmark / price / TCO rules

Benchmark comparison requires:

```text
same model_id
+ same artifact SHA
+ same quant
+ same workload
```

Price/performance additionally requires explicitly selected market observations with the same geography/channel/cohort/condition/price-state/currency contract.

TCO is an explicit scenario:

```text
purchase
+ platform delta
+ electricity
+ risk reserve
- resale estimate
→ TCO
```

Neither price/performance nor TCO can rescue a failed feasibility/support/safety/quality gate.

## Freshness

I10 operationalizes `revalidate_after`:

```text
STALE
DUE-TODAY
DUE-SOON
FRESH
```

Verified examples:
- 2026-08-28 with a 1-day window → the RTX 3090 secondary market observation is DUE-SOON;
- 2026-09-29 → 6 current dynamic records are STALE.

```text
STALE != FALSE
```

It means revalidate before using the record as current decision evidence.

## Verification

Latest exact-content verification on 2026-08-28:

```bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
```

Result:

```text
SELFTEST: PASS
```

The self-test covers:
- production/synthetic catalog validation;
- benchmark bridge;
- comparable benchmark grouping;
- price/performance;
- TCO;
- documented vs measured compatibility;
- UNKNOWN → BLOCKED;
- four-ecosystem NEEDS-TEST coverage;
- compatibility coverage matrix;
- freshness queue;
- intact/tampered Evidence Packet intake;
- exact measured compatibility upgrade;
- broken-reference rejection.

Evidence:
- examples/evidence/intelligence-i01-i06-selftest-verification.md
- examples/evidence/intelligence-07-real-benchmark-intake.md
- examples/evidence/intelligence-08-cross-vendor-documented-coverage.md
- examples/evidence/intelligence-09-compatibility-coverage-matrix.md
- examples/evidence/intelligence-10-freshness-revalidation.md

A GitHub Actions workflow exists, but the available connector has not surfaced a run; do not claim CI success from the workflow file alone.

## Current production catalog

Current intentional seed:

```text
hardware entities:      4
model entities:         1
runtime entities:       1
market observations:    1
compatibility rows:     4
real benchmark rows:    0
```

## Next actions

1. Add stronger normalized real market observations with explicit evidence cohorts.
2. Acquire/receive the first real Experiment 61 Evidence Packet and require I07 READY before ingestion.
3. Use I10 to refresh due/stale dynamic observations.
4. Derive exact measured compatibility only from real Evidence.
5. Build recommendation views only after real comparable benchmark + quality/SLO + feasibility evidence exists.
