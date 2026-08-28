# Evidence — Intelligence I23: Command ↔ Model Artifact Binding

Date: 2026-08-28  
Status: CI verified

## Claim

Real intake now binds the exact benchmark command to the same local GGUF admitted by I22.

A manifest/raw/local-artifact chain is no longer sufficient if the command evidence points at another model file.

## Capture-side binding

`capture_real_benchmark.py` accepts:

```text
--model-artifact MODEL.gguf
```

When supplied, it parses the explicit argv for exactly one:

```text
-m PATH
--model PATH
--model=PATH
```

The argv model path and `--model-artifact` must resolve to the same file before the command is launched.

`command.json` records:

```text
model_artifact.argv_value
model_artifact.resolved
model_artifact.bytes
model_artifact.sha256
```

## Intake-side independent check

For non-synthetic intake, `verify_real_intake.py` now also requires:

```text
--command-record command.json
```

It checks:
- command record JSON schema version;
- exit_code == 0;
- no launch_error;
- command record manifest SHA/bytes match the supplied manifest;
- command record model SHA/bytes match the I22 local artifact;
- exact argv independently reparses to one model path;
- the argv model path resolves from recorded cwd to the same local artifact;
- command.json itself is indexed by PACKET SHA/bytes.

## Positive test

The dedicated self-test:
1. creates a tiny local test artifact;
2. builds a corresponding manifest + raw result;
3. runs the I21 capture helper with `--model-artifact`;
4. verifies the sealed bundle through I07/I20/I22/I23;
5. requires `INTAKE: READY`.

No real GPU performance is represented.

## Pre-launch negative test

Capture is given:

```text
--model-artifact model-A.gguf
```

but argv contains:

```text
-m model-B.gguf
```

The helper refuses before creating the output bundle.

## Hash-consistent tamper negative test

The self-test then:
- copies a valid sealed bundle;
- changes command.json argv from model A to same-size model B;
- recomputes a valid PACKET over the tampered command record.

Intake still returns:

```text
INTAKE: BLOCKED
```

because it reparses argv instead of trusting packet integrity alone.

## CI

```text
workflow: Intelligence Self-Test
run #91
run id 33155944603
head b875a4f76a5ec306b9a1764cc6caa2bde1b2e823
job id 98798617756
conclusion success
```

Successful steps:

```text
Compile intelligence tools
Run intelligence self-test
Run real benchmark capture self-test
Run model artifact gate self-test
Run command-model binding self-test
Run market refresh self-test
```

## Boundary

I23 proves internal consistency between capture command evidence and the locally verified model artifact.

It still does not prove benchmark honesty, thermal equivalence, quality, causality, or purchase suitability.
