# Spec 0053 — Intelligence real evidence session runner

Status: implemented in I52.

## Problem

The I20–I32 trust chain is complete, but the learner still has to manually compose multiple capture and verification commands.

That makes the first real packet operationally error-prone.

I52 does not add a new trust gate.

It orchestrates the already verified gates.

## Input

A session JSON names:
- catalog;
- filled Experiment 61 manifest;
- exact local GGUF;
- hardware profile;
- Experiment 57 prompt manifest;
- concrete quality corpus;
- quality identity schema v2;
- canonical hardware/model/runtime IDs;
- observation date;
- exact benchmark argv;
- exact quality argv.

Both argv fields are JSON token arrays.

No shell command string is accepted.

## Execution sequence

~~~text
1 capture_real_benchmark.py
2 capture_quality_eval.py
3 extract_quality_metric.py
4 verify_real_intake.py
~~~

Each subprocess uses `shell=False`.

The runner does not reinterpret or invent benchmark/quality flags.

## Main PACKET coverage

The benchmark capture includes:
- hardware profile;
- prompt manifest;
- quality corpus;
- quality identity.

This is required because I24–I27 verify these source artifacts against the main benchmark PACKET by SHA + bytes.

The quality command/raw streams remain in their own quality PACKET.

## Failure behavior

The session output directory must be empty.

Each step writes separate stdout/stderr logs.

If a capture or verification step fails:
- already captured evidence is preserved;
- `session-summary.json` records BLOCKED and the exact failed step;
- later stages do not run.

No existing output directory is overwritten.

## Success output

A successful session writes:
- benchmark sealed directory;
- quality sealed directory;
- machine PPL artifact;
- `intake-args.json`;
- `session-summary.json` with status READY.

READY means the existing I20–I32 admission chain accepted the evidence.

It is not benchmark truth, quality superiority or purchase approval.

## Synthetic self-test

The dedicated test uses explicit fake executables and the synthetic fixture catalog with `--allow-synthetic`.

No synthetic values are added to production catalogs.
