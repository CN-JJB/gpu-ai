# Spec 0029 — Intelligence quality execution evidence binding

Status: implemented in I28.

## Problem

I26 proves the quality corpus bytes. I27 proves the small machine-readable quality identity artifact. Neither proves that a quality command actually ran against that exact model/corpus pair, or preserves the raw command/result evidence needed to audit the run.

## Decision

Add a separate fail-closed quality execution lane:

~~~text
capture_quality_eval.py
  -> exact argv, shell=False
  -> exact -m/--model binding
  -> exact -f/--file corpus binding
  -> model SHA256 + bytes
  -> corpus SHA256 + bytes
  -> I27 quality-identity artifact SHA256 + bytes
  -> raw stdout.txt + stderr.txt
  -> quality-command.json
  -> PACKET.json
  -> QUALITY CAPTURE: SEALED

verify_quality_execution.py
  -> reparses exact argv independently
  -> re-hashes model/corpus/identity artifacts
  -> verifies command exit state
  -> verifies PACKET coverage
  -> QUALITY EXECUTION: PASS
~~~

The capture helper does not invent or append llama.cpp flags.

## Current command contract

As checked against current llama.cpp documentation on 2026-08-28, the standard perplexity form is:

~~~text
llama-perplexity -m MODEL.gguf -f CORPUS.txt
~~~

The helper therefore recognizes exactly one model path from -m/--model and exactly one corpus path from -f/--file. Real runs must still inspect the pinned build's --help before execution.

## Raw-result policy

I28 deliberately does not parse a PPL value.

Reasons:
- raw output format is upstream-owned and can drift;
- valid options can change the terminal summary behavior;
- evidence preservation must not depend on one fragile text regex.

At least one of stdout/stderr must be non-empty. Both streams are preserved and PACKET-indexed.

## Large-artifact policy

The model and corpus are not copied into the quality packet by default.

Instead the command record stores:
- resolved path;
- byte count;
- SHA256.

The verifier re-hashes the supplied local files and requires exact agreement.

This keeps the packet small while preserving a cryptographic link to I26/I27.

## Failure behavior

Binding failures happen before command launch and before creating the output directory.

A launched command that exits non-zero still preserves:
- raw streams;
- exact argv;
- command metadata;
- PACKET.

It returns QUALITY CAPTURE: BLOCKED.

## Trust boundary

QUALITY EXECUTION: PASS means the sealed execution evidence is internally consistent with the supplied model, corpus, and I27 identity artifact.

It does not prove:
- that a PPL number was parsed correctly;
- that evaluation_args semantically equals every non-input argv flag;
- that tokenizer semantics are correct;
- that the metric implies chat/task quality;
- that an A/B is causal;
- that hardware should be purchased.

Semantic parsing/metric admission remains a later gate.
