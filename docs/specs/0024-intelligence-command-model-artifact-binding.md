# Spec 0024 — Benchmark Command ↔ Model Artifact Binding

Status: implementation pending CI verification  
Date: 2026-08-28

## Problem

I22 proves that a supplied local GGUF matches the Experiment 61 manifest SHA256 + byte count.

I21 preserves the exact benchmark argv.

But without binding those two evidence streams, a pathological packet could still:

```text
benchmark model A
+ verify local model B
```

when A and B happen to produce compatible raw metadata such as the same file size.

## Decision

Strengthen both capture and intake.

### Capture

Extend:

```text
tools/intelligence/capture_real_benchmark.py
```

with:

```text
--model-artifact /path/to/model.gguf
```

When supplied, the helper requires the exact command argv to contain exactly one current llama-bench model-file argument:

```text
-m PATH
--model PATH
--model=PATH
```

The argv path and `--model-artifact` must resolve to the same local file before the benchmark is launched.

`command.json` records the bound artifact path, bytes and SHA256.

### Intake

Extend:

```text
verify_real_intake.py
```

with:

```text
--command-record /path/to/command.json
```

For non-synthetic intake, both are required:

```text
--model-artifact
--command-record
```

The verifier independently checks:

1. command record is a valid JSON object;
2. command record is indexed by PACKET SHA256 + bytes;
3. exit_code == 0 and launch_error is empty;
4. command record's manifest SHA/bytes match the supplied manifest;
5. command record's model artifact SHA/bytes match the supplied local model;
6. exact argv contains one `-m/--model` path;
7. that argv model path resolves from the recorded cwd to the same file supplied by `--model-artifact`.

## Trust boundary

The verifier does not merely trust a `model_artifact` field inside command.json.

It reparses the recorded argv and resolves the path itself.

A tampered command record with a freshly recomputed PACKET must still fail if argv points at another file.

## Synthetic fixture exception

Synthetic tool fixtures may omit command evidence only with explicit `--allow-synthetic`.

When command evidence is supplied on a synthetic test path, it is still checked.

## Scope boundary

This closes an internal evidence-consistency gap.

It does not prove:
- the operating system executed an untampered binary outside the recorded executable hash;
- benchmark honesty;
- quality;
- thermal equivalence;
- causal validity;
- purchase suitability.
