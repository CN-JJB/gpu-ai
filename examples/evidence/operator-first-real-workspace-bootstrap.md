# Operator Evidence — First Real Experiment 61 Workspace Bootstrap

## Purpose

Reduce setup mistakes before the first learner-owned Experiment 61 run without adding another Intelligence evidence gate.

The operator helper is:

~~~text
tools/intelligence/bootstrap_real_evidence_workspace.py
~~~

It is deliberately **not I55**.

## What it creates

From repository templates:

~~~text
baseline-manifest.json
quality-identity.json
real-session.json
semantic-probes.json
prompt-evidence/
workspace.json
RUN.md
~~~

It binds the repository root, production catalog, workspace paths, manifest path, profile path, prompt-manifest path, and quality-identity path.

For an existing real GGUF/corpus supplied explicitly on the command line, it may bind those exact file paths into the session argv.

## What it refuses to fabricate

It does not create:

~~~text
GGUF bytes
hardware profile evidence
Experiment 57 prompt manifest
quality corpus
semantic probe output
benchmark output
quality output
measured compatibility
purchase recommendation
~~~

It launches neither I54 nor I53 nor I52.

The workspace state records:

~~~text
automatic_benchmark_launch = NOT-PERMITTED
automatic_catalog_ingestion = NOT-PERMITTED
automatic_purchase_decision = NOT-PERMITTED
~~~

## Profiles

~~~text
generic
rtx3090-qwen3-8b-llamacpp
~~~

The NVIDIA-first profile copies only the existing canonical catalog IDs and the NVIDIA probe-plan template. Those template IDs remain subject to real-machine observation and human review.

## Verification

GitHub Actions:

~~~text
workflow: Intelligence Self-Test
run #176
run id 33195115141
head d53497366645254fa2d0bf96714a5d46dc4622b7
job id 98930161758
conclusion success
~~~

Dedicated self-test:

~~~text
REAL WORKSPACE BOOTSTRAP SELFTEST: PASS
~~~

It verifies:
- generic and NVIDIA-first workspace creation;
- explicit repo/catalog/workspace path binding;
- no fake GGUF/profile/prompt/corpus/output evidence;
- optional binding only of files that already exist;
- rejection of non-empty output directories;
- rejection of invalid dates;
- rejection of missing explicitly bound artifacts;
- no benchmark launch or catalog ingestion.

The production benchmark count remains unchanged.
