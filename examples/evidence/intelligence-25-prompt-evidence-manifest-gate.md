# Evidence — Intelligence I25: Prompt Evidence Manifest Gate

Date: 2026-08-28  
Status: CI verified

## Claim

A non-synthetic Experiment 61 intake can no longer satisfy `variant.prompt.*` with manifest-only strings.

It must provide an Experiment 57-style prompt evidence manifest:

```text
--prompt-manifest /path/to/prompt-evidence/manifest.json
```

and that artifact must be PACKET-indexed.

## Exact fields cross-checked

```text
messages_sha256
chat_template_sha256
rendered_sha256
token_ids_sha256
token_count
```

The values must exactly match:

```text
Experiment 61 variant.prompt.*
```

## Dedicated self-test

The I25 fixture proves:

```text
missing prompt manifest
→ INTAKE: BLOCKED

matching Experiment 57 prompt manifest
+ PACKET coverage
→ PROMPT EVIDENCE status=PASS
→ INTAKE: READY

token_ids_sha256 changed
+ PACKET freshly recomputed
→ semantic mismatch
→ INTAKE: BLOCKED
```

No real model quality or GPU performance is represented.

## CI

```text
workflow: Intelligence Self-Test
run #108
run id 33156832189
head 195ffb4fd583d6f7df0b5136a27b340c5ce4c812
job id 98801504416
conclusion success
```

Successful steps:

```text
Compile intelligence tools
Run intelligence self-test
Run real benchmark capture self-test
Run model artifact gate self-test
Run command-model binding self-test
Run hardware profile gate self-test
Run prompt evidence gate self-test
Run market refresh self-test
```

## llama-bench boundary

For pure `llama-bench`, this authenticates the paired prompt/workload identity contract.

It does not claim that raw `llama-bench` consumed those chat prompt bytes.

## Boundary

I25 does not prove benchmark honesty, sampler correctness, quality, thermal equivalence, causal validity, or purchase suitability.
