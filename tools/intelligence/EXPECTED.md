# Expected — Intelligence Tooling Self-Test

Run from repository root:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

Full Python execution was verified through I10 on 2026-08-28:

~~~text
SELFTEST: PASS
- production catalog validates
- synthetic catalog validates only with explicit allowance
- Hardware ↔ Model ↔ Benchmark bridge returns the fixture observation
- same artifact/workload observations form one descriptive comparison group
- explicit same-cohort market rows enable descriptive price/performance
- evidence-linked TCO fixture reproduces the expected scenario arithmetic
- documented compatibility returns NEEDS-TEST, not measured PASS
- NVIDIA/CUDA, AMD/HIP, Apple/Metal and Intel/SYCL production paths all remain NEEDS-TEST
- compatibility coverage matrix reports four production NEEDS-TEST observations without ranking
- freshness queue surfaces due-soon and stale production observations
- explicit UNKNOWN remains valid and returns BLOCKED
- real benchmark intake accepts an intact packet and rejects a tampered packet
- Experiment 61 importer reproduces PP/TG
- exact benchmark Evidence upgrades only the matching path to PASS-MEASURED
- a different artifact falls back to NEEDS-TEST
- broken canonical hardware reference is rejected
~~~

The final verification used a local tree whose checked Git blob SHAs matched the latest main-branch scripts and fixture/catalog files.

Detailed evidence:

~~~text
examples/evidence/intelligence-i01-i06-selftest-verification.md
examples/evidence/intelligence-08-cross-vendor-documented-coverage.md
examples/evidence/intelligence-09-compatibility-coverage-matrix.md
examples/evidence/intelligence-10-freshness-revalidation.md
~~~

Fixture PP/TG/price/TCO values are synthetic and prove only tool behavior.

They are not GPU performance or purchase claims.

## CI

The same checks are defined in:

~~~text
.github/workflows/intelligence-selftest.yml
~~~

The available GitHub connector did not surface a workflow run for this checkpoint, so do not claim CI success from the workflow file alone.


## I11–I12 added assertions

The latest self-test additionally checks:
- one GLOBAL-EBAY / used / MEDIAN_ASK / USD contract across three GPUs;
- 1499 / 1020 / 330 USD values;
- BROAD / LIMITED / SMALL sample bands;
- ASK-ONLY and NOT-CONFIRMED-SALE semantics;
- rejection of MEDIAN_ASK when sample metadata is removed.

Exact latest-main contract verification for these checks is recorded in:
- examples/evidence/intelligence-11-market-cohort-coverage.md
- examples/evidence/intelligence-12-market-evidence-audit.md

A fresh full Python repository run has not yet been re-recorded after I11–I12 because the local execution path timed out/rate-limited. Do not claim a new full-Python PASS for I11–I12 until that run exists.
