# Intelligence Tooling

Phase 4 tooling currently implements I01–I13. I01–I10 have a full Python self-test PASS; I11–I12 have exact-main contract verification pending a fresh full Python rerun.

## 1. Validate a catalog

~~~bash
python3 validate_catalog.py ../../intelligence/catalog
~~~

Checks:
- duplicate IDs;
- record structure;
- provenance;
- canonical references;
- runtime references;
- compatibility status/scope;
- benchmark evidence identity;
- synthetic leakage;
- freshness warnings.

## 2. Validate synthetic fixtures

~~~bash
python3 validate_catalog.py fixtures/catalog --allow-synthetic
~~~

Synthetic records are rejected in production mode.

## 3. Query Hardware ↔ Model ↔ Benchmark

~~~bash
python3 query_bridge.py fixtures/catalog \
  --hardware-id hw:fixture:24g \
  --model-id model:fixture:8b \
  --include-synthetic
~~~

The output groups benchmark observations by workload fingerprint.

## 4. Compatibility preflight

~~~bash
python3 compatibility_preflight.py ../../intelligence/catalog \
  --hardware-id hw:nvidia:geforce-rtx-3090:24g \
  --model-id model:qwen:qwen3-8b \
  --runtime-id runtime:ggml-org:llama.cpp \
  --backend CUDA \
  --as-of 2026-08-27
~~~

Semantics:

~~~text
DOCUMENTED_SUPPORTED → NEEDS-TEST
MEASURED_SUPPORTED   → PASS-MEASURED
PARTIAL/EXPERIMENTAL → REVIEW
DOCUMENTED_UNSUPPORTED → FAIL
UNKNOWN/no match → BLOCKED
stale → STALE-REVALIDATE
~~~

## 5. Verify a real benchmark intake bundle

Before ingestion:

~~~bash
python3 verify_real_intake.py ../../intelligence/catalog   --manifest /path/to/manifest.json   --result /path/to/result.json   --packet /path/to/PACKET.json   --hardware-id hw:...   --model-id model:...   --runtime-id runtime:...   --observed-at YYYY-MM-DD
~~~

Required result:

~~~text
INTAKE: READY
~~~

The verifier checks canonical IDs, manifest identity, positive raw metrics, and PACKET SHA/byte integrity.

READY is not benchmark truth or purchase approval.

## 6. Ingest a real llama-bench result

Preferred input is the Experiment 61 manifest plus raw llama-bench JSON.

~~~bash
python3 ingest_llama_bench.py \
  --manifest /path/to/baseline-manifest.json \
  --result /path/to/baseline.json \
  --hardware-id hw:... \
  --model-id model:... \
  --runtime-id runtime:... \
  --record-id bench:... \
  --observed-at 2026-08-27 \
  --packet-source /path/to/PACKET.json \
  --out benchmark-record.jsonl
~~~

Review the generated JSON before appending it to the production catalog.

## 7. Derive exact measured compatibility

~~~bash
python3 ingest_measured_compatibility.py \
  --benchmark-record benchmark-record.jsonl \
  --record-id compat:... \
  --revalidate-after YYYY-MM-DD \
  --out compatibility-record.jsonl
~~~

This upgrades only the exact recorded artifact/build/device path.

One successful benchmark does not create family-wide support.

## 8. Cross-vendor compatibility matrix

~~~bash
python3 compatibility_matrix.py ../../intelligence/catalog   --model-id model:qwen:qwen3-8b   --runtime-id runtime:ggml-org:llama.cpp   --as-of 2026-08-28
~~~

Current production coverage includes NVIDIA/CUDA, AMD/HIP, Apple/Metal and Intel/SYCL.

The matrix reports evidence state and scope, not performance ranking.

## 9. Freshness / revalidation queue

~~~bash
python3 freshness_report.py ../../intelligence/catalog   --as-of 2026-08-28   --within-days 30
~~~

Use --show-unscheduled to list records without revalidate_after.

STALE means revalidate before a current decision; it does not automatically mean false.

## 10. Market cohort matrix

~~~bash
python3 market_matrix.py ../../intelligence/catalog   --geography GLOBAL-EBAY   --channel secondary-aggregated-ebay-active   --cohort used-consumer   --condition used   --price-state MEDIAN_ASK   --currency USD   --as-of 2026-08-28
~~~

The matrix groups by the complete market contract. It does not call asking prices confirmed sales.

## 11. Market evidence audit

~~~bash
python3 market_evidence_audit.py ../../intelligence/catalog   --geography GLOBAL-EBAY   --channel secondary-aggregated-ebay-active   --cohort used-consumer   --condition used   --price-state MEDIAN_ASK   --currency USD   --as-of 2026-08-28
~~~

The audit surfaces:
- active sample size;
- middle-half range;
- ask-only semantics;
- freshness;
- descriptive sample bands.

MEDIAN_ASK rows without sample/method evidence fail catalog validation.

## 12. Sold-marked listing market

~~~bash
python3 sold_marked_market.py ../../intelligence/catalog
~~~

This view summarizes pages marked SOLD while preserving:

~~~text
confirmed_transaction_price=false
~~~

It reports median displayed listing prices, not confirmed transaction medians.

## 13. Comparable benchmark view

~~~bash
python3 comparable_benchmarks.py fixtures/catalog \
  --model-id model:fixture:8b \
  --runtime-id runtime:fixture \
  --include-synthetic \
  --sort-metric tg_tok_s
~~~

Comparison grouping requires the same:
- model ID;
- artifact SHA;
- quant;
- workload object.

Rows are descriptive system comparisons, not automatically causal A/B claims.

## 14. Explicit price/performance

~~~bash
python3 price_performance.py fixtures/catalog \
  --model-id model:fixture:8b \
  --artifact-sha256 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
  --market-record market:fixture:24g:2026-08-27 \
  --market-record market:fixture:16g:2026-08-27 \
  --metric tg_tok_s \
  --include-synthetic
~~~

The tool never auto-selects a “latest price”.

Selected market records must share the same geography/channel/cohort/condition/price-state/currency contract.

## 15. TCO worksheet

~~~bash
python3 tco_worksheet.py fixtures/catalog \
  --case fixtures/tco-case.json \
  --include-synthetic
~~~

Scenario TCO exposes:
- purchase observation;
- platform delta;
- average power/duty cycle;
- electricity rate;
- risk reserve;
- resale estimate;
- evidence/source note for each material assumption.

TCO is not a feasibility gate or purchase recommendation.

## 16. Self-test

From repository root:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

Verified result:

~~~text
SELFTEST: PASS
~~~

See:
- tools/intelligence/EXPECTED.md
- examples/evidence/intelligence-i01-i06-selftest-verification.md
- examples/evidence/intelligence-08-cross-vendor-documented-coverage.md
- examples/evidence/intelligence-09-compatibility-coverage-matrix.md
- examples/evidence/intelligence-10-freshness-revalidation.md
- examples/evidence/intelligence-11-market-cohort-coverage.md
- examples/evidence/intelligence-12-market-evidence-audit.md
- examples/evidence/intelligence-13-sold-marked-listings.md

## Non-goals

These tools do not:
- scrape marketplaces automatically;
- prove external sources are truthful;
- invent missing benchmark numbers;
- create a universal GPU score;
- compare unlike workloads;
- let TCO override feasibility/support gates;
- auto-purchase hardware.
