# Spec 0026 — Prompt Evidence Manifest Admission Gate

Status: implemented and CI verified  
Date: 2026-08-28

## Problem

Experiment 61 records a prompt identity block:

```text
variant.prompt.messages_sha256
variant.prompt.chat_template_sha256
variant.prompt.rendered_sha256
variant.prompt.token_ids_sha256
variant.prompt.token_count
```

Experiment 57 already produces an auditable prompt-evidence `manifest.json` containing the same identity fields.

Before I25, real benchmark intake only required the Experiment 61 prompt fields to be present. It did not require the actual Experiment 57 evidence manifest.

## Decision

Strengthen:

```text
tools/intelligence/verify_real_intake.py
```

with:

```text
--prompt-manifest /path/to/prompt-evidence/manifest.json
```

For non-synthetic intake, this argument is required.

The verifier loads the Experiment 57-style prompt manifest and requires exact agreement for:

```text
messages_sha256
chat_template_sha256
rendered_sha256
token_ids_sha256
token_count
```

The prompt manifest must also be indexed by `PACKET.json` SHA256 + byte count.

## Evidence chain

```text
messages + tokenizer chat template
→ Experiment 57 rendered/token IDs
→ prompt-evidence/manifest.json
↕
Experiment 61 variant.prompt.*
→ I07 intake
```

## Synthetic fixture exception

Explicit synthetic tool fixtures may omit prompt evidence only when `--allow-synthetic` is used.

If a prompt manifest is supplied on a synthetic path, it is still checked.

## Failure behavior

Block intake when:
- non-synthetic intake omits `--prompt-manifest`;
- the file is missing/invalid;
- any required prompt identity field differs;
- the prompt manifest is not indexed by PACKET.

A freshly recomputed PACKET cannot override a semantic mismatch between the Experiment 57 prompt evidence and Experiment 61 manifest.

## Important llama-bench boundary

Pure `llama-bench` PP/TG model evaluation does not prove that it consumed the recorded chat prompt bytes.

I25 therefore authenticates the **paired workload/prompt identity contract**.

It must not be described as proof that raw `llama-bench` used the chat prompt.

For an end-to-end generation benchmark that actually consumes rendered prompt bytes, command/runtime-specific prompt binding remains a separate evidence obligation.

## Scope boundary

I25 does not prove:
- benchmark honesty;
- model quality;
- sampler identity beyond what is separately recorded;
- thermal equivalence;
- causal validity;
- purchase suitability.

## CI verification

```text
workflow: Intelligence Self-Test
run #108
run id 33156832189
head 195ffb4fd583d6f7df0b5136a27b340c5ce4c812
job id 98801504416
conclusion success
```

The dedicated I25 self-test proves:
- non-synthetic intake without `--prompt-manifest` is blocked;
- matching Experiment 57 prompt hashes/token count plus PACKET coverage pass;
- a semantic prompt mismatch remains blocked after PACKET is freshly recomputed.

Runs #102–#107 were intermediate migration/fix heads. #108 is the accepted I25 checkpoint.
