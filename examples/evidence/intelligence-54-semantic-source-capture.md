# Intelligence 54 — Semantic Source Capture

## Claim

The first real Experiment 61 path now has a machine-readable way to preserve the raw observations used to fill non-byte-derived semantic fields without automatically inferring or rewriting those fields.

## Tool

~~~text
tools/intelligence/capture_semantic_sources.py
~~~

Input is an explicit JSON probe plan. Each probe supplies an argv array, purpose, required/optional status, accepted return codes, and timeout.

The runner uses subprocess with shell disabled and writes a fresh output directory containing:

~~~text
bundle.json
probes/<probe-id>.stdout.txt
probes/<probe-id>.stderr.txt
~~~

For every probe the bundle records argv, working directory, timestamps, return code, timeout/launch error state, byte counts, and SHA256 for stdout/stderr.

## Boundary

~~~text
automatic_manifest_update = NOT-PERMITTED
~~~

I54 does not parse a GPU name into device_identity, does not turn version output into runtime_identity, and does not infer backend/build/execution values.

The learner reviews the captured source bundle and deliberately fills the Experiment 61 semantic manifest fields. I53 then verifies that required semantic fields are explicit before materializing byte-derived identity.

## NVIDIA-first skeleton

~~~text
labs/experiments/61-real-benchmark-evidence-packet/
  semantic-source-probes.rtx3090-llamacpp.json
~~~

The skeleton captures current llama-bench, llama-perplexity, and nvidia-smi observations on the benchmark machine. It remains a probe plan, not a claim that any observed text has a particular semantic meaning.

## Self-test evidence

GitHub Actions:

~~~text
workflow: Intelligence Self-Test
run #174
run id 33194275501
head f65da6ff82da6f0fb9983508f3bb0e3daa5034fa
job id 98927303916
conclusion success
~~~

The dedicated self-test proves:
- shell metacharacters remain literal argv tokens;
- stdout/stderr SHA256 reproduces the captured bytes;
- optional missing probes remain auditable without blocking;
- required failures block while preserving raw evidence;
- unsafe probe IDs cannot escape the output directory;
- non-empty output directories are rejected;
- no Experiment 61 manifest is rewritten automatically.

All self-test probe output is synthetic fixture evidence only. It is not production hardware/runtime evidence.
