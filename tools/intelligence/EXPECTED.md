# Expected — Intelligence Tooling Self-Test

Run from repository root:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

Full Python execution is verified through I26. I19 retains its market-refresh self-test, I20 checks raw benchmark identity, I21 seals explicit argv evidence, I22 verifies local model-artifact SHA256/bytes, I23 binds exact benchmark argv, I24 verifies hardware-profile evidence, I25 verifies prompt identity evidence, and I26 verifies the real quality corpus artifact. The I26 implementation checkpoint is GitHub Actions run #120 on 2026-08-28:

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

Run #120 checked out head ecc41744bbbf464af88cbc9a67388cca868afc7c, compiled every Intelligence Python tool, executed the complete Intelligence self-test, then passed the dedicated real benchmark capture, model artifact, command-model, hardware-profile, prompt-evidence, quality-corpus and market-refresh self-tests.

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
workflow run #120
run id 33157154448
job id 98802553888
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


## I22 assertions included in run #84

The dedicated model artifact gate self-test confirms:
- non-synthetic intake without a local model artifact is blocked;
- matching local SHA256 and bytes pass;
- the local artifact bytes agree with the manifest, while I20 separately ties raw llama-bench model_size to the same manifest bytes;
- a same-size but different-content artifact is rejected by SHA256.

Evidence:
- examples/evidence/intelligence-22-real-model-artifact-gate.md

The GGUF is hashed locally and is not copied into PACKET.json.


## I23 assertions included in run #91

The dedicated command-model binding self-test confirms:
- capture refuses a supplied model artifact that differs from exact `-m/--model` argv before launch;
- command.json records the bound artifact SHA256 + bytes;
- intake independently reparses argv from command.json;
- command.json itself must be indexed by PACKET SHA256 + bytes;
- a tampered argv pointing to another same-size file remains blocked even after PACKET is recomputed.

Evidence:
- examples/evidence/intelligence-23-command-model-artifact-binding.md


## I24 assertions included in run #98

The dedicated hardware-profile gate self-test confirms:
- non-synthetic intake without a concrete hardware profile is blocked;
- matching profile SHA256 plus PACKET coverage pass;
- a same-size wrong profile remains blocked after PACKET is recomputed.

Evidence:
- examples/evidence/intelligence-24-hardware-profile-artifact-gate.md


## I25 assertions included in run #108

The dedicated prompt evidence self-test confirms:
- non-synthetic intake requires an Experiment 57-style prompt manifest;
- messages, chat-template, rendered, token-ID hashes and token count must match Experiment 61 `variant.prompt.*`;
- the prompt evidence artifact must be PACKET-indexed;
- semantic prompt mismatch remains blocked after PACKET is recomputed.

Evidence:
- examples/evidence/intelligence-25-prompt-evidence-manifest-gate.md


## I26 assertions included in run #120

The dedicated quality-corpus gate self-test confirms:
- non-synthetic intake requires a concrete quality corpus;
- the corpus SHA256 must match `fixed.quality_eval.corpus_sha256`;
- the corpus must be PACKET-indexed;
- a same-size wrong corpus remains blocked after PACKET is recomputed.

Evidence:
- examples/evidence/intelligence-26-quality-corpus-artifact-gate.md
