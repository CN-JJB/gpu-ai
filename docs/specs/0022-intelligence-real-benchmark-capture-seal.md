# Spec 0022 — Real Benchmark Capture / Seal Helper

Status: implemented and CI verified  
Date: 2026-08-28

## Problem

After I20, admission is stricter, but the first learner-owned Experiment 61 packet still requires several manual evidence-handling steps:

```text
run command
→ redirect stdout
→ preserve stderr
→ remember exact argv
→ record exit status
→ hash files
→ build PACKET
→ run I07/I20
```

Manual redirection and packet assembly can lose command identity or accidentally omit failed-run evidence.

## Decision

Add:

```text
tools/intelligence/capture_real_benchmark.py
```

The helper runs an explicitly supplied command without a shell and seals the raw capture into one portable directory.

It does **not** construct or guess llama-bench flags.

## CLI shape

```bash
python tools/intelligence/capture_real_benchmark.py \
  --manifest /path/to/filled-manifest.json \
  --out-dir /path/to/run-dir \
  [--include /path/to/profile.txt ...] \
  -- \
  /path/to/llama-bench -m MODEL.gguf -p 512 -n 128 -r 5 ... -o json
```

Everything after `--` is passed as argv with:

```text
shell=False
```

No shell interpolation is performed.

## Captured files

Minimum successful capture:

```text
manifest.json
result.json
stderr.txt
command.json
PACKET.json
```

Optional `--include` evidence is copied under:

```text
evidence/
```

## command.json

Record:

- exact argv;
- working directory;
- UTC start/end timestamps;
- process exit code;
- requested executable;
- resolved executable path when available;
- executable SHA256 and byte count when hashable;
- source manifest path and copied manifest SHA256.

Do not capture the entire process environment because it may contain secrets.

## Write safety

The helper refuses a non-empty output directory.

It never overwrites an existing evidence bundle.

## Failure behavior

A launched command that exits non-zero still leaves:

```text
result.json
stderr.txt
command.json
PACKET.json
```

for audit.

The helper then returns non-zero and prints:

```text
CAPTURE: BLOCKED
```

A zero-exit command whose stdout is not JSON/JSONL is also sealed for audit but blocked.

## Admission boundary

`CAPTURE: SEALED` is **not** `INTAKE: READY`.

After capture, the learner still runs:

```text
verify_real_intake.py
```

with canonical IDs.

Only I07/I20 can return:

```text
RAW IDENTITY: PASS
INTAKE: READY
```

## Non-claims

The helper does not prove:
- the model SHA unless separately evidenced in the manifest/packet;
- benchmark honesty;
- prompt identity;
- thermal equivalence;
- quality;
- causality;
- purchase suitability.

It only makes raw execution evidence harder to lose or silently rewrite.

## CI verification

```text
workflow: Intelligence Self-Test
run #79
run id 33155422668
head 628418be644caee5255eb65dfa5331802b40f729
job id 98796936578
conclusion success
```

The successful job compiled all Intelligence tools and passed:
- the complete Intelligence self-test;
- the dedicated real benchmark capture self-test;
- the dedicated market refresh self-test.

The capture self-test seals a synthetic Experiment 61 run, sends the sealed bundle through I07/I20, and requires `RAW IDENTITY: PASS` + `INTAKE: READY`.

It also proves that a non-zero benchmark exit remains auditable but returns `CAPTURE: BLOCKED`, and that a non-empty output directory is never overwritten.
