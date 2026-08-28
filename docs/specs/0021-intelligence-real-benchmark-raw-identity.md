# Spec 0021 — Real Benchmark Raw-Identity Cross-Check

Status: implementation pending CI verification  
Date: 2026-08-28

## Problem

Experiment 61 and I07 already require:

```text
manifest
+ raw llama-bench result
+ PACKET integrity index
+ canonical catalog IDs
```

but the intake verifier did not prove that key manifest claims agreed with the raw `llama-bench` rows.

A packet could therefore be internally hash-consistent while still claiming a different GPU, backend, build, model size, or execution setting than the raw result.

## Decision

Strengthen:

```text
tools/intelligence/verify_real_intake.py
```

with a manifest ↔ raw-result identity cross-check before returning:

```text
INTAKE: READY
```

## Current raw fields used

Current `llama-bench -o json` exposes enough identity/config data to cross-check:

- `build_commit`;
- `gpu_info`;
- `backends`;
- `model_size`;
- `n_threads`;
- `type_k` / `type_v`;
- `n_gpu_layers`;
- `split_mode`;
- `flash_attn`;
- `tensor_split`;
- `n_prompt` / `n_gen`;
- `samples_ts` repetition count.

The verifier does not infer fields that raw `llama-bench` does not prove.

## Cross-check rules

The exact protocol rows must exist:

```text
PP row: n_prompt == manifest.fixed.protocol.pp_tokens
TG row: n_gen    == manifest.fixed.protocol.tg_tokens
```

For the selected PP/TG rows:

1. raw GPU identity must agree with manifest `device_identity`;
2. manifest backend must appear in raw `backends`;
3. raw `build_commit` must be represented by manifest runtime/build identity;
4. raw `model_size` must equal manifest artifact bytes;
5. threads, KV types, GPU layers, split mode, FA and tensor split must agree;
6. raw sample count must equal manifest repetitions;
7. the selected PP and TG rows must agree with each other on shared identity/config fields.

## Scope boundary

This is an internal-consistency gate.

It does **not** prove:

- the benchmark command was honestly executed;
- the GGUF SHA equals a field emitted by llama-bench (llama-bench does not emit that SHA);
- prompt token identity;
- thermal/background-state equality;
- causal validity;
- benchmark truth.

Those remain separate evidence obligations.

## Compatibility

Experiment 61 fixture data is upgraded to carry realistic raw identity fields.

Synthetic fixture values remain synthetic and must never be presented as hardware performance.

## Negative tests

CI must reject a packet that is hash-consistent but whose manifest/raw identities disagree.

This specifically closes the gap where simply recomputing `PACKET.json` after tampering could previously pass I07.
