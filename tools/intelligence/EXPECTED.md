# Expected — Intelligence Tooling Self-Test

Run from repository root:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

Full Python execution is verified through I33. I19 retains its market-refresh self-test; I20–I29 cover benchmark and quality execution admission; I30 binds exact quality evaluation argv; I31 extracts and independently verifies a narrow machine-readable PPL artifact; I32 makes that artifact mandatory for non-synthetic intake; I33 gates exact-contract quality A/B arithmetic. The I33 implementation checkpoint is GitHub Actions run #141 on 2026-08-28:

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

Run #141 checked out head 2070476cd272f904476dff4100779a12ec534f59, compiled every Intelligence Python tool, executed the complete Intelligence self-test, then passed the dedicated capture, model-artifact, command-model, hardware-profile, prompt-evidence, quality-corpus, quality-identity, quality-execution, quality-evaluation-argv, quality-metric, quality-comparison, quality execution + metric intake and market-refresh self-tests.

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
workflow run #141
run id 33169970758
job id 98844439875
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


## I27 assertions included in run #131

The dedicated quality-identity gate self-test confirms:
- non-synthetic intake requires a machine-readable Experiment 59 quality identity manifest;
- tokenizer, corpus, fixture revision and evaluation args must match Experiment 61 `fixed.quality_eval.*`;
- the quality identity artifact must be PACKET-indexed;
- semantic identity mismatch remains blocked after PACKET is recomputed.

Evidence:
- examples/evidence/intelligence-27-quality-identity-manifest-gate.md

## I28 assertions included in run #134

The dedicated quality execution self-test confirms:
- capture refuses a model/corpus argv path that differs from the explicitly supplied artifacts before launch;
- quality-command.json records model, corpus and I27 identity SHA256 + bytes;
- raw stdout/stderr and command evidence are PACKET-indexed;
- verify_quality_execution.py independently reparses exact -m/--model and -f/--file argv;
- argv tampering remains blocked after PACKET is recomputed;
- identity-artifact tampering remains blocked after PACKET is recomputed;
- non-zero quality execution remains auditable but returns QUALITY CAPTURE: BLOCKED.

Evidence:
- examples/evidence/intelligence-28-quality-execution-evidence.md

I28 intentionally does not parse a PPL value. QUALITY EXECUTION: PASS is an execution-evidence consistency gate.

## I29 assertions included in run #136

The dedicated quality execution intake self-test confirms:
- the I22–I27 evidence set can no longer reach `INTAKE: READY` without I28 execution evidence;
- all four quality execution paths are required for non-synthetic intake;
- `verify_real_intake.py` reuses the I28 verifier against the same model, corpus and quality identity anchors;
- the quality PACKET remains separate from the benchmark PACKET;
- a tampered `-f/--file` argv remains blocked after the quality PACKET is recomputed.

Evidence:
- examples/evidence/intelligence-29-quality-execution-intake-gate.md

I29 is still evidence-completeness/internal-consistency, not PPL truth or a purchase recommendation.

## I30 assertions included in run #138

The exact evaluation-argv self-test confirms:
- quality identity schema v2 stores `evaluation_args` as exact argv tokens;
- capture blocks declared/executed token mismatches before launch;
- command-record tokens are independently rederived;
- recomputed PACKET cannot hide evaluation-argv tampering.

Evidence:
- examples/evidence/intelligence-30-quality-evaluation-argv-binding.md

## I31 assertions included in run #139

The quality metric self-test confirms:
- one supported Final estimate line becomes a machine-readable PPL artifact;
- verification reparses raw streams instead of trusting copied numbers;
- chunk-only output is blocked instead of guessed;
- multiple Final estimate lines are ambiguous and blocked.

Evidence:
- examples/evidence/intelligence-31-quality-metric-extraction.md

## I32 assertions included in run #140

The intake regression confirms:
- non-synthetic intake requires `--quality-metric`;
- metric evidence is independently reproducible from sealed raw output;
- I22–I27 historical non-synthetic-style gates remain green with synthetic-only metric fixtures.

Evidence:
- examples/evidence/intelligence-32-quality-metric-intake-gate.md

## I33 assertions included in run #141

The exact quality comparison self-test confirms:
- both sides independently pass I31/I32 verification;
- tokenizer/corpus/fixture/evaluation argv/parser/metric/executable identity must match;
- changed evaluation argv blocks comparison;
- changed quality executable bytes block comparison;
- only exact-contract inputs emit descriptive PPL delta/ratio/percent change.

Evidence:
- examples/evidence/intelligence-33-quality-ab-comparability.md

