# Spec 0028 — Quality Identity Manifest Admission Gate

Status: implemented and CI verified  
Date: 2026-08-28

## Problem

After I26, the actual quality corpus bytes are authenticated.

Experiment 61 still carries three additional quality-evaluation identity fields that were only present inside the main benchmark manifest:

```text
fixed.quality_eval.tokenizer_identity
fixed.quality_eval.fixture_revision
fixed.quality_eval.evaluation_args
```

The corpus SHA also belongs in the same quality identity record so the frozen evaluation setup can be reviewed as one artifact.

## Decision

Add a minimal machine-readable Experiment 59 quality identity manifest and require it at real intake:

```text
--quality-manifest /path/to/quality-identity.json
```

Schema version 1 contains only:

```text
quality_identity_schema_version
tokenizer_identity
corpus_sha256
fixture_revision
evaluation_args
```

The verifier requires exact equality between that artifact and:

```text
manifest.fixed.quality_eval.*
```

The quality identity manifest must be indexed by `PACKET.json`.

## Evidence chain

```text
real corpus bytes
→ I26 SHA256
↕
quality-identity.json corpus_sha256
+
tokenizer / fixture / evaluation args identity
↕
Experiment 61 fixed.quality_eval.*
```

## Important trust boundary

I27 freezes and authenticates the declared quality-evaluation identity artifact.

It does not yet prove that:
- the named tokenizer was actually loaded;
- a quality command consumed the corpus;
- the recorded evaluation arguments were the executed argv;
- a reported PPL/quality score is correct.

Those require runtime/command/result evidence.

## Synthetic exception

Explicit synthetic fixtures may omit the quality identity manifest only with `--allow-synthetic`.

If supplied on a synthetic path, it is still checked.

## Failure behavior

Block non-synthetic intake when:
- `--quality-manifest` is missing;
- JSON/schema is invalid;
- any quality identity field differs from Experiment 61;
- the artifact is not PACKET-indexed.

A recomputed PACKET does not override a semantic identity mismatch.

## CI verification

```text
workflow: Intelligence Self-Test
run #131
run id 33157420701
head bed49fe2878c314ee08a215e7fc8d4c31516ae35
job id 98803423115
conclusion success
```

The dedicated I27 self-test proves:
- non-synthetic intake without `--quality-manifest` is blocked;
- exact tokenizer/corpus/fixture/evaluation identity plus PACKET coverage pass;
- semantic quality identity mismatch remains blocked after PACKET recomputation.

Runs #124–#128 were intermediate migration heads. #129 restored the prior suite, #130 verified the dedicated gate, and #131 is the accepted I27 checkpoint.
