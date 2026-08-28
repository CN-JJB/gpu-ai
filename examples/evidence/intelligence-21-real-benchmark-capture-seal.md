# Evidence — Intelligence I21: Real Benchmark Capture / Seal Helper

Date: 2026-08-28  
Status: CI verified

## Claim

A learner can now execute an explicit benchmark argv and preserve the run as an Experiment 61-style evidence directory without manual shell redirection or manual PACKET hashing.

The capture helper does not turn a capture into an admitted benchmark.

```text
CAPTURE: SEALED
!=
INTAKE: READY
```

## Implementation

```text
tools/intelligence/capture_real_benchmark.py
tools/intelligence/capture_real_benchmark_selftest.py
docs/specs/0022-intelligence-real-benchmark-capture-seal.md
```

## Capture contract

Everything after `--` is passed as argv with:

```text
subprocess.run(..., shell=False)
```

The helper does not guess or synthesize current llama-bench flags.

It preserves:

```text
manifest.json
result.json
stderr.txt
command.json
PACKET.json
optional evidence/*
```

`command.json` records:
- exact argv;
- cwd;
- UTC start/end;
- exit code / launch error;
- requested and resolved executable identity;
- executable bytes + SHA256 when hashable;
- source/copy manifest identity.

It intentionally does not dump the full environment.

## Positive CI path

The dedicated self-test:
1. launches a synthetic fake benchmark through the capture helper;
2. seals the Experiment 61 fixture result;
3. includes an extra profile evidence file;
4. verifies PACKET file count and paths;
5. runs the sealed manifest/result/PACKET through `verify_real_intake.py`;
6. requires:

```text
RAW IDENTITY: PASS
INTAKE: READY
```

The fixture remains synthetic and is not GPU performance evidence.

## Failure-preserving path

A fake benchmark exits with code 3.

The helper:
- writes stdout;
- writes stderr;
- records exit code 3;
- writes command.json;
- writes PACKET.json;
- returns:

```text
CAPTURE: BLOCKED
```

The failed run is auditable but cannot be treated as successful intake.

## Overwrite safety

A non-empty output directory is rejected.

Existing evidence is not overwritten.

## CI

```text
workflow: Intelligence Self-Test
run #79
run id 33155422668
head 628418be644caee5255eb65dfa5331802b40f729
job id 98796936578
conclusion success
```

Successful steps include:

```text
Compile intelligence tools
Run intelligence self-test
Run real benchmark capture self-test
Run market refresh self-test
```

## Boundary

I21 improves evidence handling only.

It does not prove benchmark honesty, model SHA, prompt identity, quality, thermal control, causal validity, or purchase suitability.

The production benchmark catalog remains empty until a learner-owned real packet passes I07/I20.
