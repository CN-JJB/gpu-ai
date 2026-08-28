# Spec 0027 — Quality Corpus Artifact Admission Gate

Status: implemented and CI verified  
Date: 2026-08-28

## Problem

Experiment 61 requires:

```text
fixed.quality_eval.corpus_sha256
```

but before I26 that value only had to be present.

A non-synthetic intake could therefore claim a frozen quality corpus without presenting the actual corpus artifact.

## Decision

Strengthen:

```text
tools/intelligence/verify_real_intake.py
```

with:

```text
--quality-corpus /path/to/corpus.txt
```

For non-synthetic intake, the corpus file is required.

The verifier computes its SHA256 and requires exact agreement with:

```text
manifest.fixed.quality_eval.corpus_sha256
```

The corpus artifact must also be indexed by `PACKET.json` SHA256 + byte count.

## Evidence chain

```text
quality corpus bytes
→ SHA256
↕
Experiment 61 fixed.quality_eval.corpus_sha256
→ frozen quality-evaluation identity
```

## Large-corpus boundary

I26 does not automatically copy a large corpus into the capture directory.

`PACKET.json` is an integrity index, not necessarily a portable archive of every large artifact.

The learner may:
- include a small corpus in the sealed evidence directory; or
- index an external learner-owned corpus when rebuilding the final Experiment 61 packet.

## Synthetic fixture exception

Explicit synthetic tool fixtures may omit the corpus only with `--allow-synthetic`.

If a corpus is supplied on a synthetic path, it is still checked.

## Failure behavior

Block intake when:
- non-synthetic intake omits `--quality-corpus`;
- the path is missing/not a file;
- SHA256 differs;
- the corpus is not indexed by PACKET.

A freshly recomputed PACKET over the wrong corpus still fails when its SHA does not match the frozen Experiment 61 manifest.

## Scope boundary

I26 authenticates corpus bytes only.

It does not yet prove:
- tokenizer identity;
- fixture revision;
- evaluation arguments;
- that a particular quality command actually consumed this corpus;
- quality result correctness;
- benchmark honesty;
- purchase suitability.

## CI verification

```text
workflow: Intelligence Self-Test
run #120
run id 33157154448
head ecc41744bbbf464af88cbc9a67388cca868afc7c
job id 98802553888
conclusion success
```

The dedicated I26 self-test proves:
- non-synthetic intake without `--quality-corpus` is blocked;
- a matching corpus SHA256 plus PACKET coverage pass;
- a same-size wrong corpus remains blocked after PACKET is freshly recomputed.

Runs #112 and #114–#117 were intermediate fixture migration heads. #118 restored the prior suite; #120 is the accepted I26 checkpoint.
