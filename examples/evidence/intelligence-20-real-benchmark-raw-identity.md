# Evidence — Intelligence I20: Raw Benchmark Identity Cross-Check

Date: 2026-08-28  
Status: CI verified

## Claim

A hash-consistent Experiment 61 packet is no longer sufficient by itself for I07 intake.

The manifest's key runtime/device/model/execution claims must agree with the selected raw `llama-bench` PP/TG rows before:

```text
INTAKE: READY
```

## Implementation

```text
tools/intelligence/verify_real_intake.py
tools/intelligence/fixtures/experiment61/result.json
tools/intelligence/fixtures/experiment61/PACKET.json
tools/intelligence/selftest.py
docs/specs/0021-intelligence-real-benchmark-raw-identity.md
```

## Raw identity/config fields cross-checked

For the exact manifest protocol PP/TG rows:

```text
build_commit
gpu_info
backends
model_size
n_threads
type_k
type_v
n_gpu_layers
split_mode
flash_attn
tensor_split
n_prompt / n_gen
samples_ts count
```

The verifier also requires the selected PP and TG rows to agree with each other on shared build/device/model/config identity.

## Positive fixture

The synthetic Experiment 61 fixture was enriched with realistic raw `llama-bench` identity fields.

It remains synthetic.

Successful intake now includes:

```text
RAW IDENTITY: PASS
INTAKE: READY
```

Fixture PP/TG values prove tool behavior only and are not hardware performance claims.

## Negative proof

The self-test creates a second manifest whose:

```text
variant.hardware.device_identity
```

is changed to a different GPU identity.

It then recomputes a completely valid `PACKET.json` over:

```text
tampered manifest
+ original raw result
```

so SHA256 and byte counts are internally correct.

The verifier still returns:

```text
INTAKE: BLOCKED
```

because raw `gpu_info` disagrees with the manifest.

This proves the new gate is stronger than packet-integrity checking alone.

## CI

```text
workflow: Intelligence Self-Test
run #74
run id 33155088741
head 719c51d130ee4b932e6a0b8d7c26c3337af7d928
job id 98795852292
conclusion success
```

Successful steps:

```text
Compile intelligence tools
Run intelligence self-test
Run market refresh self-test
```

## Boundary

I20 is an internal-consistency gate, not proof that:
- the benchmark was honestly executed;
- model SHA is emitted by llama-bench;
- prompt/token identity is correct;
- thermal/background state is controlled;
- a causal claim is valid;
- any GPU should be purchased.

The production benchmark catalog remains empty until a real learner-owned Experiment 61 packet passes the strengthened I07 gate.
