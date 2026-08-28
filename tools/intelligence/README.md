# Intelligence Tooling

Phase 4 tooling currently implements I01–I54. GitHub Actions run #174 verifies the complete suite, including raw semantic-source capture, byte-derived real-session preparation, and the end-to-end I52 evidence runner.

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

### Recommended I21 capture path

Before verification, capture the explicit benchmark argv into a sealed evidence directory:

~~~bash
python3 capture_real_benchmark.py \
  --manifest /path/to/filled-manifest.json \
  --out-dir /path/to/run-dir \
  --include /path/to/profile.txt \
  -- \
  llama-bench -m /path/to/model.gguf -p 512 -n 128 -r 5 ... -o json
~~~

The helper:
- executes the exact argv with `shell=False`;
- preserves stdout, stderr, command identity and exit status;
- hashes the resolved executable when available;
- copies optional evidence files;
- writes `PACKET.json`;
- refuses a non-empty output directory;
- preserves failed-run evidence but returns `CAPTURE: BLOCKED`.

`CAPTURE: SEALED` is not intake admission.

Before ingestion:

~~~bash
python3 verify_real_intake.py ../../intelligence/catalog \
  --manifest /path/to/manifest.json \
  --result /path/to/result.json \
  --packet /path/to/PACKET.json \
  --hardware-id hw:... \
  --model-id model:... \
  --runtime-id runtime:... \
  --observed-at YYYY-MM-DD \
  --hardware-profile /path/to/profile.txt \
  --prompt-manifest /path/to/prompt-evidence/manifest.json \
  --quality-corpus /path/to/corpus.txt \
  --quality-manifest /path/to/quality-identity.json \
  --model-artifact /path/to/model.gguf \
  --command-record /path/to/command.json \
  --quality-command-record /path/to/quality-command.json \
  --quality-stdout /path/to/stdout.txt \
  --quality-stderr /path/to/stderr.txt \
  --quality-packet /path/to/quality/PACKET.json \
  --quality-metric /path/to/quality-metric.json
~~~

Required result:

~~~text
INTAKE: READY
~~~

The verifier checks:
- canonical IDs;
- required Experiment 61 manifest identity;
- exact protocol PP/TG rows;
- positive raw metrics;
- PACKET SHA/byte integrity;
- manifest ↔ raw llama-bench agreement for GPU identity, backend/build, model bytes, threads, KV types, GPU layers, split mode, flash attention, tensor split, and repetition count.

A hash-consistent PACKET is not enough if the manifest disagrees with the raw benchmark rows.

For non-synthetic intake, I22 requires `--model-artifact`; I23 binds exact `-m/--model` argv through a PACKET-indexed command record; I24 authenticates the hardware profile artifact; I25 validates Experiment 57 prompt evidence; I26 requires `--quality-corpus`, hashes the actual corpus and matches `fixed.quality_eval.corpus_sha256`; I27 additionally requires a PACKET-indexed `--quality-manifest` whose tokenizer/corpus/fixture/evaluation identity exactly matches `fixed.quality_eval.*`.

Expected success now includes:

~~~text
RAW IDENTITY: PASS
INTAKE: READY
~~~

READY is an evidence-completeness/internal-consistency gate, not benchmark truth or purchase approval.

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

Superseded observations are hidden by default.

Use:

~~~text
--include-superseded
~~~

to inspect audit history.

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

## 13. Cross-market signal comparison

~~~bash
python3 compare_market_contracts.py ../../intelligence/catalog   --left-geography GLOBAL-EBAY   --left-channel secondary-aggregated-ebay-active   --left-cohort used-consumer   --left-condition used   --left-price-state MEDIAN_ASK   --left-currency USD   --right-geography US   --right-channel offerup-sold-marked-listing   --right-cohort used-consumer   --right-condition used   --right-price-state SOLD_MARKED_LISTING_PRICE   --right-currency USD
~~~

This reports descriptive cross-contract gaps only. It does not call them transaction discounts.

## 14. China secondary watch

~~~bash
python3 market_matrix.py ../../intelligence/catalog   --geography CN   --channel secondary-summary   --cohort used-consumer   --condition working-unverified   --price-state SECONDARY_REPORTED   --currency CNY   --as-of 2026-08-28
~~~

SECONDARY_REPORTED rows must keep direct_listing_capture=false and confirmed_sale=false.

## 15. Market evidence selection gate

~~~bash
python3 market_evidence_gate.py ../../intelligence/catalog
~~~

This reuses stable M0–M3 grades and reports whether an observation can satisfy only Experiment 38's market-evidence component.

Current mapping:

~~~text
SECONDARY_REPORTED        → M1 → NEEDS-STRONGER
MEDIAN_ASK                → M2 → ELIGIBLE
SOLD_MARKED_LISTING_PRICE → M3 → ELIGIBLE
~~~

M3 does not imply a confirmed transaction amount.

Freshness is evaluated separately:

~~~text
CURRENT + M2/M3 → ELIGIBLE
DUE-TODAY → REVALIDATE-NOW
STALE → STALE-REVALIDATE
~~~

## 16. Comparable benchmark view

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

## 17. Explicit price/performance

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

## 18. TCO worksheet

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

## 19. Append-only market refresh helper

Prepare one complete new market observation JSON object, then preflight it against the current active observation:

~~~bash
python3 market_refresh.py ../../intelligence/catalog \
  --old-record-id market:cn:rtx3090:secondary:2026-08-22 \
  --candidate /path/to/new-observation.json \
  --out /tmp/market.refreshed.jsonl \
  --check-only
~~~

When the candidate is reviewed, omit `--check-only` to write the refreshed JSONL.

The helper:
- preserves the old record;
- creates reciprocal `superseded_by` / `supersedes`;
- rejects already-superseded forks;
- rejects cross-hardware lineage;
- rejects non-newer observation dates;
- does not invent source, price, grade, or provenance.

After writing, run `validate_catalog.py` and the market views/gates before committing production data.

## 20. Quality execution evidence

Seal an actual quality command without guessing flags:

~~~bash
python3 capture_quality_eval.py \
  --out-dir /tmp/quality-run \
  --model-artifact /path/to/model.gguf \
  --quality-corpus /path/to/corpus.txt \
  --quality-manifest /path/to/quality-identity.json \
  -- \
  llama-perplexity -m /path/to/model.gguf -f /path/to/corpus.txt
~~~

Then verify the sealed evidence against the original artifacts:

~~~bash
python3 verify_quality_execution.py \
  --quality-command-record /tmp/quality-run/quality-command.json \
  --stdout /tmp/quality-run/stdout.txt \
  --stderr /tmp/quality-run/stderr.txt \
  --packet /tmp/quality-run/PACKET.json \
  --model-artifact /path/to/model.gguf \
  --quality-corpus /path/to/corpus.txt \
  --quality-manifest /tmp/quality-run/quality-identity.json
~~~

The helper binds the exact -m/--model and -f/--file argv paths before launch, preserves both raw streams, and does not invent a PPL metric.

I30 upgrades the quality identity/capture contract to schema v2: `evaluation_args` is an exact JSON argv-token list. Capture and verification strip only executable + model/corpus selectors, then require exact token/order equality.

QUALITY EXECUTION: PASS is an evidence-binding result, not a quality or purchase claim.

I29 makes that execution evidence mandatory for non-synthetic `verify_real_intake.py` admission. Supply all four:

~~~text
--quality-command-record /path/to/quality-command.json
--quality-stdout /path/to/stdout.txt
--quality-stderr /path/to/stderr.txt
--quality-packet /path/to/quality/PACKET.json
~~~

The main benchmark PACKET and the quality PACKET remain separate integrity domains.

## 21. Machine-readable quality metric

After a sealed quality run passes, extract only the supported final-estimate contract:

~~~bash
python3 extract_quality_metric.py \
  --quality-command-record /tmp/quality-run/quality-command.json \
  --stdout /tmp/quality-run/stdout.txt \
  --stderr /tmp/quality-run/stderr.txt \
  --packet /tmp/quality-run/PACKET.json \
  --model-artifact /path/to/model.gguf \
  --quality-corpus /path/to/corpus.txt \
  --quality-manifest /tmp/quality-run/quality-identity.json \
  --out /tmp/quality-run/quality-metric.json
~~~

I31 accepts exactly one supported `Final estimate: PPL = VALUE +/- UNCERTAINTY` line across stdout/stderr. Chunk-only or ambiguous output is BLOCKED.

I32 makes `--quality-metric` mandatory for non-synthetic `verify_real_intake.py` admission.

## 22. Exact quality A/B comparison

When baseline and candidate quality bundles are complete:

~~~bash
python3 compare_quality_metrics.py \
  --baseline-dir /path/to/baseline-quality-run \
  --candidate-dir /path/to/candidate-quality-run \
  --baseline-model /path/to/baseline.gguf \
  --candidate-model /path/to/candidate.gguf \
  --quality-corpus /path/to/corpus.txt \
  --out /tmp/quality-comparison.json
~~~

I33 independently verifies both sides and requires exact tokenizer/corpus/fixture/evaluation-argv/parser/metric/executable identity before descriptive PPL delta/ratio arithmetic.

This is not a significance test, causal claim, task-quality verdict, or recommendation.

## 23. Reproducible model tradeoff

Model-artifact A/B path:

~~~text
compare_quality_metrics.py
→ verify_quality_comparison.py
→ bind_performance_quality_ab.py
→ verify_joint_tradeoff.py
~~~

I36 requires `quality-comparison.json` to reproduce both sealed quality bundles.

I37 requires that reproduction inside the PP/TG × PPL binder.

I38 independently rebuilds the entire model joint artifact.

The model joint path is only for `variant.model` / `variant.model.*`.

## 24. Declared execution-variable quality A/B

Copy and fill:

~~~text
labs/experiments/59-real-quality-gate/quality-variable-contract.template.json
~~~

Then run:

~~~bash
python3 compare_quality_execution_variable.py \
  --baseline-manifest baseline-manifest.json \
  --candidate-manifest candidate-manifest.json \
  --baseline-dir baseline-quality-run \
  --candidate-dir candidate-quality-run \
  --baseline-model /path/to/model.gguf \
  --candidate-model /path/to/model.gguf \
  --quality-corpus /path/to/corpus.txt \
  --variable-contract quality-variable-contract.json \
  --out quality-comparison.json
~~~

I35/I39 currently support `variant.execution.*` only.

The contract binds each manifest value to the exact side-specific evaluation argv already authenticated by I30.

The model artifact and quality executable must stay identical.

## 25. Reproduce execution-variable quality comparison

~~~bash
python3 verify_quality_execution_variable_comparison.py \
  --quality-comparison quality-comparison.json \
  --baseline-manifest baseline-manifest.json \
  --candidate-manifest candidate-manifest.json \
  --baseline-dir baseline-quality-run \
  --candidate-dir candidate-quality-run \
  --baseline-model /path/to/model.gguf \
  --candidate-model /path/to/model.gguf \
  --quality-corpus /path/to/corpus.txt \
  --variable-contract quality-variable-contract.json
~~~

I39 rebuilds the schema-v2 comparison from sealed metric roots + the declared variable contract.

## 26. Execution-variable performance × quality binding

~~~bash
python3 bind_execution_performance_quality_ab.py \
  --baseline-manifest baseline-manifest.json \
  --candidate-manifest candidate-manifest.json \
  --baseline-benchmark baseline-benchmark.json \
  --candidate-benchmark candidate-benchmark.json \
  --quality-comparison quality-comparison.json \
  --baseline-quality-dir baseline-quality-run \
  --candidate-quality-dir candidate-quality-run \
  --baseline-model-artifact /path/to/model.gguf \
  --candidate-model-artifact /path/to/model.gguf \
  --quality-corpus /path/to/corpus.txt \
  --variable-contract quality-variable-contract.json \
  --out execution-joint.json
~~~

I40 requires I39 reproduction before binding PPL to PP/TG.

## 27. Reproduce execution-variable joint artifact

~~~bash
python3 verify_execution_joint_tradeoff.py \
  --joint-tradeoff execution-joint.json \
  --baseline-manifest baseline-manifest.json \
  --candidate-manifest candidate-manifest.json \
  --baseline-benchmark baseline-benchmark.json \
  --candidate-benchmark candidate-benchmark.json \
  --quality-comparison quality-comparison.json \
  --baseline-quality-dir baseline-quality-run \
  --candidate-quality-dir candidate-quality-run \
  --baseline-model-artifact /path/to/model.gguf \
  --candidate-model-artifact /path/to/model.gguf \
  --quality-corpus /path/to/corpus.txt \
  --variable-contract quality-variable-contract.json
~~~

I41 requires exact full-object reproduction.

## 28. Decision-readiness evidence lane

I42–I51 add an evidence-only path toward human review.

Key tools:

~~~text
verify_tradeoff_route.py
decision_evidence_gap.py
evaluate_used_gpu_acceptance.py
verify_used_gpu_acceptance.py
evaluate_performance_target.py
verify_performance_target.py
evaluate_price_ceiling.py
verify_price_ceiling.py
derive_condition_evidence_grade.py
verify_condition_evidence_grade.py
~~~

The final matrix keeps independent components for:
- verified performance × quality evidence;
- real benchmark provenance;
- exact measured compatibility;
- current market evidence;
- whole-machine feasibility;
- used-GPU technical acceptance;
- explicit performance target;
- explicit personal price ceiling;
- condition-evidence provenance.

It can emit `READY-FOR-HUMAN-REVIEW`, never BUY.

Condition provenance is defined in:

~~~text
reference/hardware/condition-evidence-grades.md
~~~

C3 means learner-owned, PACKET-bound, independently reproducible I44 technical evidence. ACCEPT/REVIEW/REJECT remains separate.

## 29. Capture semantic source observations

Before manually filling the non-byte-derived Experiment 61 fields, capture the exact machine/runtime observations that support them.

For the NVIDIA-first path, start from:

~~~text
labs/experiments/61-real-benchmark-evidence-packet/semantic-source-probes.rtx3090-llamacpp.json
~~~

Review the argv arrays against the executables actually installed on the benchmark machine, then run:

~~~bash
python3 tools/intelligence/capture_semantic_sources.py \
  /path/to/semantic-probes.json \
  --out-dir /path/to/semantic-source-evidence
~~~

Required success:

~~~text
SEMANTIC SOURCE CAPTURE: READY-FOR-SEMANTIC-REVIEW
~~~

I54 preserves each explicit argv, stdout/stderr, return code, timestamps and SHA256 in a fresh output directory.

It never parses those observations into Experiment 61 fields and always records:

~~~text
automatic_manifest_update = NOT-PERMITTED
~~~

Review the bundle and deliberately fill the semantic manifest fields from the retained sources.

## 30. Prepare one real evidence session

After filling the semantic fields and source paths in a session JSON, materialize only byte-derived identity:

~~~bash
python3 tools/intelligence/prepare_real_evidence_session.py \
  /path/to/real-session.json \
  --out-dir /path/to/prepared-session
~~~

Required success:

~~~text
REAL SESSION PREPARE: READY-TO-RUN-I52
~~~

I53 computes/synchronizes:
- exact GGUF SHA256 + bytes;
- hardware-profile SHA256;
- concrete quality-corpus SHA256;
- Experiment 57 prompt identity;
- quality identity corpus SHA;
- Experiment 61 `fixed.quality_eval`.

It never infers device identity, runtime/build/backend, quant/source revision, or execution semantics.

Then use:

~~~text
/path/to/prepared-session/session.json
~~~

as the I52 input.

## 31. Run one real evidence session

Copy and fill:

~~~bash
cp labs/experiments/61-real-benchmark-evidence-packet/real-evidence-session.template.json \
  /path/to/real-session.json
~~~

Then run:

~~~bash
python3 tools/intelligence/run_real_evidence_session.py \
  /path/to/real-session.json \
  --out-dir /path/to/session-output
~~~

I52 executes, in order:

~~~text
capture_real_benchmark.py
capture_quality_eval.py
extract_quality_metric.py
verify_real_intake.py
~~~

The session JSON contains exact benchmark and quality argv token arrays. The runner does not invent flags and does not use a shell.

Success is:

~~~text
REAL SESSION: READY
~~~

The output also contains:
- benchmark and quality sealed directories;
- `session-summary.json`;
- `intake-args.json`.

Review the real evidence before ingestion. READY is not benchmark truth or purchase approval.

## 32. Self-test

From repository root:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

GitHub Actions verified result:

~~~text
run #174
SELFTEST: PASS
QUALITY EXECUTION SELFTEST: PASS
QUALITY EVALUATION ARGS SELFTEST: PASS
QUALITY METRIC SELFTEST: PASS
QUALITY COMPARISON SELFTEST: PASS
QUALITY COMPARISON ARTIFACT SELFTEST: PASS
JOINT TRADEOFF SELFTEST: PASS
JOINT TRADEOFF ARTIFACT SELFTEST: PASS
QUALITY EXECUTION-VARIABLE SELFTEST: PASS
QUALITY EXECUTION-VARIABLE ARTIFACT SELFTEST: PASS
EXECUTION JOINT TRADEOFF SELFTEST: PASS
EXECUTION JOINT TRADEOFF ARTIFACT SELFTEST: PASS
UNIFIED TRADEOFF ROUTE SELFTEST: PASS
DECISION EVIDENCE GAP SELFTEST: PASS
USED GPU ACCEPTANCE SELFTEST: PASS
USED GPU ACCEPTANCE READINESS BRIDGE SELFTEST: PASS
PERFORMANCE TARGET SELFTEST: PASS
PERFORMANCE TARGET READINESS BRIDGE SELFTEST: PASS
PRICE CEILING SELFTEST: PASS
PRICE CEILING READINESS BRIDGE SELFTEST: PASS
CONDITION EVIDENCE GRADE SELFTEST: PASS
CONDITION EVIDENCE READINESS BRIDGE SELFTEST: PASS
QUALITY EXECUTION INTAKE SELFTEST: PASS
REAL EVIDENCE SESSION SELFTEST: PASS
REAL EVIDENCE SESSION PREPARE SELFTEST: PASS
SEMANTIC SOURCE CAPTURE SELFTEST: PASS
MARKET REFRESH SELFTEST: PASS
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
- examples/evidence/intelligence-14-cross-market-signal.md
- examples/evidence/intelligence-15-cn-secondary-watch.md
- examples/evidence/intelligence-16-market-evidence-selection-gate.md
- examples/evidence/intelligence-i01-i16-ci-selftest.md
- examples/evidence/intelligence-17-freshness-aware-watchlist.md
- examples/evidence/intelligence-18-append-only-market-refresh.md
- examples/evidence/intelligence-19-market-refresh-helper.md
- examples/evidence/intelligence-20-real-benchmark-raw-identity.md
- examples/evidence/intelligence-21-real-benchmark-capture-seal.md
- examples/evidence/intelligence-22-real-model-artifact-gate.md
- examples/evidence/intelligence-23-command-model-artifact-binding.md
- examples/evidence/intelligence-24-hardware-profile-artifact-gate.md
- examples/evidence/intelligence-25-prompt-evidence-manifest-gate.md
- examples/evidence/intelligence-26-quality-corpus-artifact-gate.md
- examples/evidence/intelligence-27-quality-identity-manifest-gate.md
- examples/evidence/intelligence-28-quality-execution-evidence.md
- examples/evidence/intelligence-29-quality-execution-intake-gate.md
- examples/evidence/intelligence-33-quality-ab-comparability.md
- examples/evidence/intelligence-32-quality-metric-intake-gate.md
- examples/evidence/intelligence-31-quality-metric-extraction.md
- examples/evidence/intelligence-30-quality-evaluation-argv-binding.md

- examples/evidence/intelligence-34-performance-quality-ab-binding.md

- examples/evidence/intelligence-35-quality-execution-variable-contract.md

- examples/evidence/intelligence-36-quality-comparison-artifact-verification.md

- examples/evidence/intelligence-37-joint-tradeoff-quality-reproduction.md

- examples/evidence/intelligence-38-joint-tradeoff-artifact-verification.md

- examples/evidence/intelligence-39-quality-execution-variable-artifact-verification.md

- examples/evidence/intelligence-40-execution-performance-quality-binding.md

- examples/evidence/intelligence-41-execution-joint-tradeoff-artifact-verification.md

- examples/evidence/intelligence-42-unified-tradeoff-routing.md

- examples/evidence/intelligence-43-decision-evidence-gap-matrix.md

- examples/evidence/intelligence-44-used-gpu-acceptance-artifact.md

- examples/evidence/intelligence-45-used-gpu-acceptance-readiness-bridge.md

- examples/evidence/intelligence-46-performance-target-policy.md

- examples/evidence/intelligence-47-performance-target-readiness-bridge.md

- examples/evidence/intelligence-48-price-ceiling-policy.md

- examples/evidence/intelligence-49-price-ceiling-readiness-bridge.md

- examples/evidence/intelligence-50-condition-evidence-grades.md

- examples/evidence/intelligence-51-condition-evidence-readiness-bridge.md

- examples/evidence/intelligence-52-real-evidence-session-runner.md

- examples/evidence/intelligence-53-real-evidence-session-materializer.md

- examples/evidence/intelligence-54-semantic-source-capture.md

## Non-goals

These tools do not:
- scrape marketplaces automatically;
- prove external sources are truthful;
- invent missing benchmark numbers;
- create a universal GPU score;
- compare unlike workloads;
- let TCO override feasibility/support gates;
- auto-purchase hardware.
