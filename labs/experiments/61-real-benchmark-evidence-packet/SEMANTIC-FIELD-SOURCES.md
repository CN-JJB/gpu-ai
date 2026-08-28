# Experiment 61 — Semantic Field Sources

This file answers one question:

> For each non-byte-derived manifest field, what evidence should I use instead of guessing?

I53 deliberately does **not** fill these fields.

## Source classes

Use these source classes in descending order of usefulness:

~~~text
A. exact raw output from the executable used in the run
B. local machine/runtime observation captured immediately before the run
C. exact model conversion/source record
D. learner-defined experiment policy
~~~

Do not substitute:
- a marketplace listing;
- a generic product page;
- a filename guess;
- a remembered default;
- a value copied from another machine.

## Capture sources without turning them into claims

I54 exists to retain source observations before you fill these fields:

~~~text
tools/intelligence/capture_semantic_sources.py
~~~

For the NVIDIA-first path, use/review:

~~~text
semantic-source-probes.rtx3090-llamacpp.json
~~~

A successful I54 run gives `READY-FOR-SEMANTIC-REVIEW` plus raw stdout/stderr and hashes. It does **not** mean the tool has interpreted those bytes correctly for any manifest field.

The learner must still review the observations and make the semantic claim deliberately.

## Experiment identity

| Field | Source | Rule |
| --- | --- | --- |
| `comparison_id` | learner-defined policy | Choose one stable ID for the A/B pair. It is not discovered from hardware. |
| `label` | learner-defined policy | Human label such as baseline/candidate. |
| `intentional_variable` | learner-defined policy | Name the one semantic variable you intend to change. Do not force a multi-variable system change into a one-variable contract. |

## Protocol

| Field | Source | Rule |
| --- | --- | --- |
| `fixed.protocol.pp_tokens` | experiment policy + benchmark argv | Must match the selected raw PP row. |
| `fixed.protocol.tg_tokens` | experiment policy + benchmark argv | Must match the selected raw TG row. |
| `fixed.protocol.repetitions` | experiment policy + raw `samples_ts` count | Raw PP/TG sample count must reproduce it. |
| `fixed.protocol.warmup_runs` | experiment procedure | Record the procedure actually used; do not infer it from result rows. |

## Hardware

### `variant.hardware.device_identity`

Preferred evidence:
1. the device identity reported by the exact llama.cpp build;
2. the immediately captured hardware profile;
3. vendor utility output on the same machine.

Useful retained observations may include:

~~~text
llama-bench --list-devices
nvidia-smi -L
nvidia-smi --query-gpu=...
amd-smi ...
system_profiler ...
sycl-ls
~~~

For intake, raw `gpu_info` must agree with the manifest identity.

Do **not** copy only the catalog marketing name if the runtime reports a more specific identity.

### `variant.hardware.profile_sha256`

Do not type this manually.

I53 hashes the actual profile file.

## Runtime

### `variant.runtime.runtime_identity`

Source:
- exact `llama-bench --version` / runtime version observation;
- local source revision when self-built.

Write enough identity that the raw benchmark `build_commit` can be related back to this run.

### `variant.runtime.backend`

Source:
- exact backend enabled in the run;
- raw benchmark `backends` field.

The intake verifier checks that the manifest backend appears in the raw backend identity.

Examples of conceptual backend identities include CUDA, HIP, Metal, or SYCL, but use what the actual build reports.

### `variant.runtime.build_identity`

Source:
- exact build commit/version/configuration for the executable used.

Raw `build_commit` must be represented by either `runtime_identity` or `build_identity`.

Do not use a current upstream branch name as a substitute for the executable actually run.

## Model

### `variant.model.artifact_sha256`
### `variant.model.artifact_bytes`

Do not type these manually.

I53 derives them from the exact local GGUF.

### `variant.model.quant`

Source:
- verified GGUF metadata;
- the exact conversion artifact record.

Do not trust a filename suffix alone unless you have independently established that it matches the artifact.

### `variant.model.source_revision`

Source:
- exact upstream model revision;
- exact conversion input revision;
- exact internal artifact provenance record.

A GGUF SHA identifies the local artifact but does not by itself tell you the upstream source revision.

## Execution

These fields describe the intended/executed runtime configuration:

~~~text
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

Use:
- exact argv you are about to execute;
- current executable help for that build;
- raw benchmark fields after the run.

The intake gate independently cross-checks these raw fields where llama-bench exposes them:

~~~text
n_threads
type_k
type_v
n_gpu_layers
split_mode
flash_attn
tensor_split
~~~

### Defaults are not evidence

If you rely on a runtime default, establish what that installed build actually did.

Do not write a remembered default from another llama.cpp revision.

### `tensor_split`

An intentionally empty/zero semantic value may be valid.

The raw benchmark still needs an explicit machine-readable value such as its runtime-reported zero form.

## Prompt

These fields should come from the Experiment 57 prompt manifest:

~~~text
messages_sha256
chat_template_sha256
rendered_sha256
token_ids_sha256
token_count
~~~

Do not copy them by hand.

I53 synchronizes them into the prepared Experiment 61 manifest.

## Quality identity

Explicitly establish in `quality-identity.json`:

~~~text
tokenizer_identity
fixture_revision
evaluation_args
~~~

The quality argv must reproduce `evaluation_args` token-for-token after the model/corpus selectors are removed by the existing I30 contract.

I53 computes the concrete corpus SHA and synchronizes the Experiment 61 quality block.

## Audit fields

Audit fields may point to records that are created by the capture session itself.

Do not invent a command record before the command has run.

The sealed I52 directories become the authoritative executed-command evidence.

## Before I53

Prefer to retain an I54 semantic-source bundle from the actual benchmark machine before making the explicit semantic claims.

A good source session should therefore contain three kinds of information.

### Raw semantic source bundle

~~~text
semantic-source-evidence/bundle.json
semantic-source-evidence/probes/*.stdout.txt
semantic-source-evidence/probes/*.stderr.txt
~~~

### Explicit semantic facts

~~~text
device identity
runtime identity/backend/build
model quant/source revision
execution configuration
protocol
quality tokenizer/fixture/evaluation args
canonical catalog IDs
~~~

### Real source files

~~~text
GGUF
hardware profile
prompt manifest
quality corpus
quality identity
~~~

Then I53 can materialize the byte-derived identity without guessing.

## After I52

Treat raw output as a cross-check, not something to rewrite to match the manifest.

If raw output disagrees with the intended manifest:
1. preserve the failed evidence;
2. determine what was actually executed;
3. correct the source configuration;
4. create a new run in a new output directory.

Never edit sealed raw evidence to force agreement.
