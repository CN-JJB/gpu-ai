# Spec 0023 — Real Model Artifact Admission Gate

Status: implementation pending CI verification  
Date: 2026-08-28

## Problem

I20 cross-checks the Experiment 61 manifest against raw `llama-bench` identity/config fields.

Current `llama-bench -o json` exposes:

```text
model_size
```

but it does not expose the GGUF artifact SHA256.

Therefore a manifest could carry the correct byte count but a wrong:

```text
variant.model.artifact_sha256
```

and I20 alone could not detect it.

## Decision

Strengthen:

```text
tools/intelligence/verify_real_intake.py
```

with:

```text
--model-artifact /path/to/model.gguf
```

For a non-synthetic model intake this argument is required.

The verifier computes the local file:

- byte count;
- SHA256.

It compares them to:

```text
manifest.variant.model.artifact_bytes
manifest.variant.model.artifact_sha256
```

The existing I20 check already compares raw `llama-bench model_size` to the manifest byte count.

The resulting chain is:

```text
local model file SHA + bytes
↕
Experiment 61 manifest artifact identity
↕
raw llama-bench model_size
```

## Synthetic fixture exception

When the selected catalog model is explicitly synthetic and the caller uses:

```text
--allow-synthetic
```

the large fixture artifact does not need to exist.

The verifier reports the artifact check as skipped for that synthetic-only test path.

If a model artifact is explicitly supplied even on a synthetic path, it is still checked.

## Failure behavior

Block intake when:
- a real model intake omits `--model-artifact`;
- the path is missing/not a file;
- SHA256 differs;
- bytes differ.

A PACKET that is otherwise internally valid cannot override an artifact mismatch.

## Scope boundary

The local file is not copied into PACKET.json.

Large GGUF files remain external artifacts.

The verifier proves local artifact identity at intake time; it does not prove:
- download provenance beyond the recorded manifest/source revision;
- model quality;
- benchmark honesty;
- causal validity;
- purchase suitability.
