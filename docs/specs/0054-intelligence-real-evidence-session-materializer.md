# Spec 0054 — Intelligence real evidence session materializer

Status: implemented in I53.

## Problem

I52 safely orchestrates the real benchmark/quality admission chain, but a learner can still make avoidable transcription mistakes while copying SHA256, byte counts and prompt/quality identity into the Experiment 61 manifest.

I53 reduces that clerical risk without inventing any runtime or performance facts.

## Safe materialization boundary

I53 may write only fields that are determined by local source bytes or already-explicit machine-readable identity.

It materializes:

~~~text
variant.hardware.profile_sha256
variant.model.artifact_sha256
variant.model.artifact_bytes
fixed.quality_eval.*
variant.prompt.*
quality_identity.corpus_sha256
~~~

Sources:
- local GGUF bytes;
- hardware-profile bytes;
- quality-corpus bytes;
- Experiment 57 prompt manifest;
- quality identity schema v2.

## Fields I53 must not infer

I53 preserves and requires explicit values for:

~~~text
comparison_id
intentional_variable
variant.hardware.device_identity
variant.runtime.*
variant.model.quant
variant.model.source_revision
variant.execution.*
~~~

If these remain placeholders, preparation is BLOCKED before any benchmark launches.

## Exact argv checks

I53 does not interpret benchmark performance flags.

It only verifies:
- benchmark argv contains exactly one model path and it resolves to the selected GGUF;
- quality argv contains exactly one model and corpus path;
- quality argv evaluation args exactly equal the explicit quality identity v2 argv list.

No shell-string parsing is used.

## Canonical identity preflight

hardware_id, model_id and runtime_id must exist exactly once in the selected catalog.

Synthetic canonical identities require explicit test allowance.

## Output

I53 writes to a new empty directory:

~~~text
manifest.json
quality-identity.json
session.json
preflight.json
~~~

Source files are never modified in place.

The prepared session uses resolved source paths and points to the newly materialized manifest and quality identity.

Success means:

~~~text
REAL SESSION PREPARE: READY-TO-RUN-I52
~~~

This means only that the local byte-derived identities and explicit semantic inputs are prepared.

It does not run a benchmark and produces no PP/TG/PPL claim.
