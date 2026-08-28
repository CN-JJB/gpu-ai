# Experiment 61 — Real Acquisition Checklist

Use this on the actual benchmark machine.

This checklist prepares evidence. It does not tell you which GPU/model to buy.

## 0. Optional RTX 3090 canonical skeleton

For the first NVIDIA path:

~~~bash
cp real-evidence-session.rtx3090-qwen3-8b-llamacpp.skeleton.json real-session.json
~~~

This pre-fills only:

~~~text
hardware_id = hw:nvidia:geforce-rtx-3090:24g
model_id    = model:qwen:qwen3-8b
runtime_id  = runtime:ggml-org:llama.cpp
~~~

Do not treat any remaining placeholder as a suggested value.

## 1. Prepare real source artifacts

Have these real files ready:

~~~text
model.gguf
profile.txt
prompt-evidence/manifest.json
quality-corpus.txt
quality-identity.json
real-session.json
~~~

The prompt manifest should come from Experiment 57.

The hardware profile should be captured on the machine that will run the benchmark.

The quality corpus must be the exact corpus used by the quality command.

## 2. Fill semantic fields manually

Use the source map:

~~~text
SEMANTIC-FIELD-SOURCES.md
~~~

It distinguishes learner-defined experiment policy from machine/runtime observations and model provenance.

In the Experiment 61 manifest, explicitly fill the facts that cannot be derived from bytes:

~~~text
comparison_id
intentional_variable
variant.hardware.device_identity

variant.runtime.runtime_identity
variant.runtime.backend
variant.runtime.build_identity

variant.model.quant
variant.model.source_revision

variant.execution.context
variant.execution.sequences
variant.execution.gpu_layers
variant.execution.flash_attention
variant.execution.kv_k
variant.execution.kv_v
variant.execution.split_mode
variant.execution.tensor_split
variant.execution.threads
~~~

Do not leave REPLACE/TBD/TODO/UNKNOWN placeholders.

Do not infer a runtime/build identity from the GPU name.

Do not infer quant or source revision from a filename unless that identity is actually established.

## 3. Fill the session JSON

Start from:

~~~bash
cp real-evidence-session.template.json real-session.json
~~~

Fill:
- catalog path;
- manifest path;
- GGUF path;
- profile path;
- prompt manifest path;
- quality corpus path;
- quality identity path;
- canonical hardware/model/runtime IDs;
- observation date;
- exact benchmark argv token array;
- exact quality argv token array.

Do not use shell command strings.

Do not leave the literal `...` token in either argv.

## 4. Prepare byte-derived identity

Run:

~~~bash
python3 ../../../tools/intelligence/prepare_real_evidence_session.py \
  real-session.json \
  --out-dir prepared-session
~~~

Required output:

~~~text
REAL SESSION PREPARE: READY-TO-RUN-I52
~~~

Inspect:

~~~text
prepared-session/manifest.json
prepared-session/quality-identity.json
prepared-session/session.json
prepared-session/preflight.json
~~~

I53 should have materialized:
- model SHA256 + bytes;
- profile SHA256;
- corpus SHA256;
- prompt identity;
- fixed quality identity.

It should not have changed your runtime/device/execution semantics.

## 5. Check the current executables yourself

Before running the session, inspect the actual binaries on this machine:

~~~bash
llama-bench --version
llama-bench --help
llama-perplexity --help
~~~

Use the flags supported by the installed build.

Do not copy a stale command line only because it worked on another revision.

## 6. Run I52

Run:

~~~bash
python3 ../../../tools/intelligence/run_real_evidence_session.py \
  prepared-session/session.json \
  --out-dir real-session-output
~~~

Required result:

~~~text
REAL SESSION: READY
~~~

If it blocks, inspect:

~~~text
real-session-output/session-summary.json
real-session-output/logs/
~~~

Do not edit the sealed output to force a pass.

Fix the source input and create a new empty output directory.

## 7. Review before ingestion

Review at minimum:

~~~text
real-session-output/benchmark/result.json
real-session-output/benchmark/command.json
real-session-output/benchmark/PACKET.json
real-session-output/quality/stdout.txt
real-session-output/quality/stderr.txt
real-session-output/quality/quality-command.json
real-session-output/quality/quality-metric.json
real-session-output/session-summary.json
~~~

Confirm the observed hardware/runtime/model/execution identity is what you intended to test.

## 8. Only then ingest deliberately

After review, use the existing real-ingest helper.

Do not append a failed, synthetic, stale-identity or unexplained run to the production benchmark catalog.

After reviewed ingestion, derive exact measured compatibility only for that exact hardware/model/runtime/build path.

## 9. Production boundary

Until a learner-owned real session passes and is manually reviewed:

~~~text
real production benchmark rows = 0
~~~

Synthetic self-tests never change that count.

`READY-TO-RUN-I52` is not a benchmark result.

`REAL SESSION: READY` is not a purchase recommendation.
