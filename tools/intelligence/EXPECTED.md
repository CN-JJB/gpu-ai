# Expected — Intelligence Tooling Self-Test

Run from repository root:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

Full Python execution is verified through I21. I19 retains its dedicated market-refresh self-test, I20 strengthens real benchmark intake identity, and I21 adds an evidence-preserving explicit-argv capture/seal helper. The I21 implementation checkpoint is GitHub Actions run #79 on 2026-08-28:

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
- real benchmark intake cross-checks manifest identity/config against raw llama-bench rows
- hash-consistent identity tampering is blocked, not only broken PACKET hashes
- Experiment 61 importer reproduces PP/TG
- exact benchmark Evidence upgrades only the matching path to PASS-MEASURED
- a different artifact falls back to NEEDS-TEST
- broken canonical hardware reference is rejected
~~~

Run #79 checked out head 628418be644caee5255eb65dfa5331802b40f729, compiled every Intelligence Python tool, executed the complete Intelligence self-test, executed the dedicated real benchmark capture self-test, and then executed the dedicated market refresh self-test.

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
workflow run #79
run id 33155422668
job id 98796936578
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


## I18 assertions included in run #62

The successful log explicitly confirms:
- append-only A770 refresh supersedes the old observation without deleting audit history;
- superseded observations leave active market/freshness/watchlist views by default;
- broken market refresh lineage is rejected.

Evidence:
- examples/evidence/intelligence-18-append-only-market-refresh.md

## I19 assertions included in run #67

The dedicated self-test confirms:
- reciprocal append-only lineage is generated while keeping the old record;
- the generated catalog still passes validate_catalog.py;
- already-superseded history cannot fork;
- cross-hardware lineage is rejected;
- equal/older observations are rejected.

Evidence:
- examples/evidence/intelligence-19-market-refresh-helper.md


## I20 assertions included in run #74

The successful run confirms:
- exact manifest protocol PP/TG rows are selected from raw llama-bench JSON;
- PP/TG raw rows must agree on shared device/build/model/config identity;
- manifest GPU identity must agree with raw gpu_info;
- manifest backend/build must agree with raw backends/build_commit;
- model bytes, threads, KV types, GPU layers, split mode, flash attention, tensor split and repetition count are cross-checked;
- a tampered manifest with a freshly recomputed, hash-consistent PACKET is still rejected.

Evidence:
- examples/evidence/intelligence-20-real-benchmark-raw-identity.md

The gate remains an internal-consistency check. It is not benchmark truth, causal proof, or a purchase recommendation.


## I21 assertions included in run #79

The dedicated capture self-test confirms:
- an explicit argv is executed with no shell interpolation;
- stdout, stderr, exact command identity and executable hash are preserved;
- optional evidence is copied into the sealed directory;
- PACKET.json indexes the sealed evidence files;
- a sealed synthetic Experiment 61 bundle passes the strengthened I07/I20 verifier;
- a non-zero benchmark exit remains auditable but returns CAPTURE: BLOCKED;
- a non-empty output directory is never overwritten.

Evidence:
- examples/evidence/intelligence-21-real-benchmark-capture-seal.md

`CAPTURE: SEALED` is not `INTAKE: READY`.
