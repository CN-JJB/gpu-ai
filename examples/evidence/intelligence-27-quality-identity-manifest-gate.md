# Evidence — Intelligence I27: Quality Identity Manifest Gate

Date: 2026-08-28  
Status: CI verified

## Claim

A non-synthetic Experiment 61 intake now requires a separate machine-readable Experiment 59 quality identity artifact:

```text
--quality-manifest quality-identity.json
```

The artifact must be PACKET-indexed and exactly match `fixed.quality_eval.*`.

## Schema v1

```text
quality_identity_schema_version = 1
tokenizer_identity
corpus_sha256
fixture_revision
evaluation_args
```

I26 independently verifies the real corpus bytes behind `corpus_sha256`.

## Dedicated self-test

The I27 fixture proves:

```text
missing quality identity manifest
→ INTAKE: BLOCKED

matching tokenizer/corpus/fixture/eval identity
+ PACKET coverage
→ QUALITY IDENTITY status=PASS
→ INTAKE: READY

evaluation_args changed
+ PACKET freshly recomputed
→ semantic mismatch
→ INTAKE: BLOCKED
```

No real quality score or GPU performance is represented.

## CI

```text
workflow: Intelligence Self-Test
run #131
run id 33157420701
head bed49fe2878c314ee08a215e7fc8d4c31516ae35
job id 98803423115
conclusion success
```

The successful job compiled all Intelligence tools and passed the full self-test plus dedicated capture, model-artifact, command-model, hardware-profile, prompt-evidence, quality-corpus, quality-identity and market-refresh tests.

## Boundary

I27 freezes and authenticates the declared quality-evaluation identity artifact.

It does not prove that the named tokenizer/evaluation args were actually executed, nor that a quality result is correct. Those remain runtime/command/result evidence obligations.
