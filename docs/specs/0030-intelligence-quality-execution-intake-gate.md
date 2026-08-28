# Spec 0030 — Intelligence quality execution intake gate

Status: implemented in I29.

## Problem

I28 can independently seal and verify a quality execution, but I27-era `verify_real_intake.py` can still return `INTAKE: READY` without that execution evidence.

That leaves a gap between:
- authenticated corpus + quality identity;
- an actually executed quality command/result bundle.

## Decision

For non-synthetic intake, require four additional quality-execution evidence paths:

~~~text
--quality-command-record
--quality-stdout
--quality-stderr
--quality-packet
~~~

The existing paths remain the semantic anchors:

~~~text
--model-artifact
--quality-corpus
--quality-manifest
~~~

`verify_real_intake.py` calls the reusable I28 verifier and requires:

~~~text
QUALITY EXECUTION
- status=PASS
~~~

before `INTAKE: READY`.

## Two-packet design

Keep:
1. the Experiment 61 benchmark PACKET for performance/static evidence;
2. the I28 quality PACKET for quality command + raw stream evidence.

The main intake gate does not duplicate quality-command/stdout/stderr into the benchmark PACKET.

This keeps each integrity index aligned with its capture boundary.

## Fail-closed behavior

For a non-synthetic model record:
- no I28 paths -> BLOCKED;
- partial I28 paths -> BLOCKED;
- missing model/corpus/quality identity anchor -> BLOCKED;
- I28 verifier error -> BLOCKED;
- only a full I28 PASS can satisfy the quality-execution requirement.

Synthetic catalog fixtures may skip this only with the existing explicit `--allow-synthetic` path.

## Tamper model

A freshly recomputed quality PACKET does not override semantic checks.

The I29 negative test edits the recorded `-f/--file` argv to a different same-size corpus and recomputes the quality PACKET. Main intake still blocks because argv no longer resolves to the I26 corpus.

## Trust boundary

I29 closes execution-evidence completeness.

It still does not prove:
- PPL parsing or interpretation;
- that every evaluation argument matches `evaluation_args` semantically;
- tokenizer correctness;
- chat/task quality;
- causal A/B conclusions;
- purchase suitability.

Those remain later evidence/decision layers.
