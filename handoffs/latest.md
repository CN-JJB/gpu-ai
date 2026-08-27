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

Stable machine-decision semantics remain:

```text
known required FAIL → REVISE
critical UNKNOWN / missing evidence → BLOCKED
all required gates PASS → ACCEPT
```

No weighted score may average away a hard gate.

## Active Phase 4 frontier

Verified:

```text
I01 catalog / benchmark bridge
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

These are Intelligence Stations, not stable Lesson slices.

## Current compatibility coverage

For `model:qwen:qwen3-8b` + `runtime:ggml-org:llama.cpp`:

```text
RTX 3090 24GB / CUDA  → DOCUMENTED_SUPPORTED → NEEDS-TEST
RX 7900 XTX / HIP     → DOCUMENTED_SUPPORTED → NEEDS-TEST
M4 Max / Metal        → DOCUMENTED_SUPPORTED → NEEDS-TEST
Arc A770 16GB / SYCL  → DOCUMENTED_SUPPORTED → NEEDS-TEST
```

No production performance ranking exists.

## Real benchmark gate

Before production benchmark ingestion:

```text
manifest
+ raw result
+ PACKET.json
+ canonical IDs
→ verify_real_intake.py
→ INTAKE: READY
```

Then:

```text
ingest_llama_bench.py
→ validate_catalog.py
→ ingest_measured_compatibility.py
→ validate_catalog.py
```

Repository search found no real Experiment 61-compatible bundle, so the production benchmark catalog remains empty by design.

## Benchmark / market / TCO guardrails

Comparable benchmark:

```text
same model + exact artifact + quant + workload
```

Price/performance:
- explicit market record selection only;
- same market cohort contract;
- no automatic latest-price join.

TCO:

```text
purchase + platform + electricity + risk - resale
```

TCO is not a feasibility gate.

## Freshness

Tool:
- tools/intelligence/freshness_report.py

States:
- STALE
- DUE-TODAY
- DUE-SOON
- FRESH

STALE means revalidate before current use; it does not automatically mean false.

## Verification

Exact-content local execution on 2026-08-28:

```bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
```

Result:

```text
SELFTEST: PASS
```

Latest verified additions include:
- I08 four vendor/backend production paths;
- I09 `NEEDS-TEST=4` compatibility matrix;
- I10 due-soon/stale revalidation cases.

Evidence:
- examples/evidence/intelligence-07-real-benchmark-intake.md
- examples/evidence/intelligence-08-cross-vendor-documented-coverage.md
- examples/evidence/intelligence-09-compatibility-coverage-matrix.md
- examples/evidence/intelligence-10-freshness-revalidation.md

GitHub Actions workflow exists at `.github/workflows/intelligence-selftest.yml`, but no run has surfaced through the connector; do not claim CI success.

## Production data boundary

```text
hardware:      4
models:        1
runtimes:      1
market:        1
compatibility: 4
benchmarks:    0 real rows
```

## Next work

1. Strengthen normalized real market observations.
2. Ingest the first real benchmark only after I07 READY.
3. Refresh dynamic observations when I10 marks them due/stale.
4. Delay recommendation/ranking until real comparable Evidence and quality/SLO gates exist.

No auto-purchase or unsafe hardware modification is part of this workflow.
