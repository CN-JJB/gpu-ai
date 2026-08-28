# Evidence — Intelligence I26: Quality Corpus Artifact Gate

Date: 2026-08-28  
Status: CI verified

## Claim

A non-synthetic Experiment 61 intake can no longer satisfy `fixed.quality_eval.corpus_sha256` with a manifest-only hash.

It must provide:

```text
--quality-corpus /path/to/corpus.txt
```

The local corpus SHA256 must match the frozen Experiment 61 quality-evaluation identity and the corpus must be indexed by PACKET.

## Evidence chain

```text
quality corpus bytes
→ SHA256
↕
Experiment 61 fixed.quality_eval.corpus_sha256
→ quality-evaluation identity
```

## Dedicated self-test

The I26 fixture proves:

```text
missing quality corpus
→ INTAKE: BLOCKED

matching corpus SHA + PACKET coverage
→ QUALITY CORPUS status=PASS
→ INTAKE: READY

same-size wrong corpus
+ freshly recomputed PACKET
→ manifest corpus SHA mismatch
→ INTAKE: BLOCKED
```

No real model quality or GPU performance is represented.

## CI

```text
workflow: Intelligence Self-Test
run #120
run id 33157154448
head ecc41744bbbf464af88cbc9a67388cca868afc7c
job id 98802553888
conclusion success
```

The successful job compiled all Intelligence tools and passed the full suite plus dedicated capture, artifact, command-model, hardware-profile, prompt-evidence, quality-corpus and market-refresh tests.

## Large-corpus boundary

PACKET is an integrity index, not necessarily a portable archive. I26 does not force large corpora into Git.

## Boundary

I26 authenticates the corpus bytes only. Tokenizer identity, fixture revision, evaluation arguments, actual quality-command binding and quality result correctness remain separate evidence obligations.
