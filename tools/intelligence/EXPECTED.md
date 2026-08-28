# Expected — Intelligence Tooling Self-Test

Run from repository root:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

Full Python execution is verified through I17 on 2026-08-28 via GitHub Actions run #54:

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

The latest full verification checked out head bbf624e44579cbc765974bf8b5070330002f294e on GitHub Actions, compiled every Intelligence Python tool, and executed the complete self-test.

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

Verified CI identity:

~~~text
workflow run #54
run id 33137613634
job id 98741045301
conclusion success
Python 3.12.14
Ubuntu 24.04.4
~~~



## I11–I16 assertions included in run #48

The successful log explicitly includes:
- GLOBAL-EBAY MEDIAN_ASK cohort and values;
- 47/23/8 asking-listing sample bands;
- MEDIAN_ASK negative validation;
- 9 OfferUp SOLD-marked rows and non-confirmed transaction semantics;
- SOLD_MARKED_LISTING_PRICE negative validation;
- cross-market descriptive gaps;
- China SECONDARY_REPORTED watch signals;
- SECONDARY_REPORTED negative validation;
- M1/M2/M3 market evidence selection gate;
- mismatched market evidence grade rejection.

Evidence:
- examples/evidence/intelligence-i01-i16-ci-selftest.md


## I17 assertions included in run #54

The successful log explicitly confirms:
- market evidence eligibility is freshness-aware;
- every real market row requires a revalidation date;
- Experiment 38 blocks due-today, stale and invalid market evidence from BUY-CANDIDATE.

Evidence:
- examples/evidence/intelligence-17-freshness-aware-watchlist.md
