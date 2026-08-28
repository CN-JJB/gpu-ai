# Evidence — Intelligence I22: Real Model Artifact Admission Gate

Date: 2026-08-28  
Status: CI verified

## Claim

A real, non-synthetic benchmark intake can no longer rely on a manifest-declared GGUF SHA256 alone.

The caller must provide the local model file:

```text
--model-artifact /path/to/model.gguf
```

before I07 returns READY.

## Chain closed

I22 computes the local file:

```text
SHA256
bytes
```

and compares them to:

```text
manifest.variant.model.artifact_sha256
manifest.variant.model.artifact_bytes
```

I20 already compares:

```text
raw llama-bench model_size
↔
manifest artifact_bytes
```

Together:

```text
local GGUF SHA + bytes
↕
Experiment 61 manifest
↕
raw llama-bench model_size
```

## Synthetic exception

Explicit synthetic test paths may skip a large artifact when `--allow-synthetic` is used.

This exception is only for synthetic tool fixtures.

A supplied artifact is checked even on a synthetic path.

## Dedicated self-test

The self-test constructs a tiny test artifact and a corresponding hash-consistent manifest/raw/PACKET.

It proves three cases:

```text
no --model-artifact
→ INTAKE: BLOCKED

matching file SHA + bytes
→ MODEL ARTIFACT status=PASS
→ RAW IDENTITY: PASS
→ INTAKE: READY

same bytes, different content
→ SHA256 mismatch
→ INTAKE: BLOCKED
```

No real GPU performance is represented by this fixture.

## CI

```text
workflow: Intelligence Self-Test
run #84
run id 33155656857
head 233414410c5b3a20ca9a873f411a54e830ef39b1
job id 98797675678
conclusion success
```

Successful steps:

```text
Compile intelligence tools
Run intelligence self-test
Run real benchmark capture self-test
Run model artifact gate self-test
Run market refresh self-test
```

## Boundary

The model file is hashed locally and is not copied into PACKET.

I22 still does not prove that the benchmark command actually referenced that exact file. That command ↔ artifact binding remains a separate evidence obligation.
