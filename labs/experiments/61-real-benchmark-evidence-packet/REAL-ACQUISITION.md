# Experiment 61 — Real Acquisition Checklist

Use this on the actual benchmark machine.

This checklist prepares evidence. It does not tell you which GPU/model to buy.

## 0. Preferred: bootstrap a clean real workspace

For the first NVIDIA path:

~~~bash
python3 ../../../tools/intelligence/bootstrap_real_evidence_workspace.py \
  --out-dir /absolute/path/to/e61-real \
  --profile rtx3090-qwen3-8b-llamacpp
~~~

If the real GGUF/corpus already exist, optionally add their **existing absolute paths** plus an explicit observation date.

The bootstrap pre-fills only repository/template facts, including the existing canonical RTX 3090 / Qwen3-8B / llama.cpp IDs for that profile. It does not claim the physical machine actually matches them.

It creates:

~~~text
baseline-manifest.json
quality-identity.json
real-session.json
semantic-probes.json
prompt-evidence/
workspace.json
RUN.md
~~~

It deliberately does not create:

~~~text
model GGUF
profile.txt
prompt-evidence/manifest.json
quality corpus
semantic-source-evidence/
prepared-session/
real-session-output/
~~~

Read `RUN.md`, then continue below.

Manual fallback: copy `real-evidence-session.rtx3090-qwen3-8b-llamacpp.skeleton.json` and the probe templates yourself.

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

## 2. Capture same-machine semantic sources

For the NVIDIA-first path, start from:

~~~bash
cp semantic-source-probes.rtx3090-llamacpp.json semantic-probes.json
~~~

Review the argv arrays against the binaries actually installed on this machine. Remove or replace probes that do not match the build rather than pretending a stale command succeeded.

Do not put passwords, API tokens, cookies, SSH keys or other secrets in probe argv.

Run:

~~~bash
python3 ../../../tools/intelligence/capture_semantic_sources.py \
  semantic-probes.json \
  --out-dir semantic-source-evidence
~~~

Required output:

~~~text
SEMANTIC SOURCE CAPTURE: READY-FOR-SEMANTIC-REVIEW
~~~

Review:

~~~text
semantic-source-evidence/bundle.json
semantic-source-evidence/probes/*.stdout.txt
semantic-source-evidence/probes/*.stderr.txt
~~~

The capture is raw source evidence only. It does not authorize automatic manifest edits.

## 3. Assemble the hardware profile artifact

After I54 is READY, generate the exact `profile.txt` path already referenced by the bootstrap session:

~~~bash
python3 ../../../tools/intelligence/assemble_hardware_profile.py \
  semantic-source-evidence/bundle.json \
  --out profile.txt
~~~

Required output:

~~~text
HARDWARE PROFILE ASSEMBLER: READY
~~~

The assembler verifies the I54 stream hashes and embeds their exact bytes. It does not decide what GPU/runtime those bytes mean.

Review `profile.txt` together with the original I54 bundle.

## 4. Fill semantic fields manually

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

## 5. Fill the session JSON

If you used the bootstrap, edit the generated `real-session.json`.

Otherwise start from:

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

## 6. Prepare byte-derived identity

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

## 7. Check the current executables yourself

Before running the session, re-check the actual binaries on this machine if anything changed after the I54 capture:

~~~bash
llama-bench --version
llama-bench --help
llama-perplexity --help
~~~

Use the flags supported by the installed build.

Do not copy a stale command line only because it worked on another revision.

## 8. Run I52

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

## 9. Review before ingestion

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

## 10. Only then ingest deliberately

After review, use the existing real-ingest helper.

Do not append a failed, synthetic, stale-identity or unexplained run to the production benchmark catalog.

After reviewed ingestion, derive exact measured compatibility only for that exact hardware/model/runtime/build path.

## 11. Production boundary

Until a learner-owned real session passes and is manually reviewed:

~~~text
real production benchmark rows = 0
~~~

Synthetic self-tests never change that count.

`READY-TO-RUN-I52` is not a benchmark result.

`REAL SESSION: READY` is not a purchase recommendation.
