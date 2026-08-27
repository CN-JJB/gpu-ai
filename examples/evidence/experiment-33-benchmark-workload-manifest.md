# Evidence — Experiment 33: Benchmark / Workload Manifest

状态：semantic A/B manifest contract implemented and validator self-checked.

## Claim

> A reproducible benchmark needs one explicit workload identity. "One variable" should mean one declared semantic intervention, not blindly one JSON leaf.

## Contract

```
fixed
+
variant
+
audit
```

Baseline and candidate share:
- comparison ID;
- fixed PP/TG protocol;
- quality-evaluation identity.

Only one path below:

```
variant.*
```

may change.

## Why semantic blocks matter

A quantization A/B legitimately changes together:
- artifact SHA256;
- artifact bytes;
- quant label.

So this is valid:

```
intentional_variable = variant.model
```

while an execution leaf can be stricter:

```
intentional_variable = variant.execution.flash_attention
```

## Validator self-check

Synthetic Q8 → Q4 comparison:

Allowed differences:

```
variant.model.artifact_bytes
variant.model.artifact_sha256
variant.model.quant
```

Result:

```
VALIDATION: PASS
```

A second synthetic candidate also changed:

```
variant.prompt.token_ids_sha256
```

Result:

```
VALIDATION: FAIL
```

with the prompt hash reported as an undeclared difference.

## Required identity

The validator requires at least:
- hardware device identity;
- runtime identity;
- exact model artifact SHA;
- context;
- token-ID SHA/count;
- sampler mode;
- PP/TG/repetition protocol;
- tokenizer/corpus identity for quality evaluation.

## Evidence Packet

`build_packet.py` records for each supplied file:
- path;
- bytes;
- SHA256.

This is an integrity index, not a signature and not proof that measurements are truthful.

## Cross-vendor boundary

If changing hardware requires changing backend/runtime too, that is a valid engineering **system comparison** but not a single-variable causal A/B.

The course explicitly refuses to weaken the validator to make such a comparison pass.

## Integration

Slice 33 joins:
- Experiment 40 controlled performance A/B;
- Experiment 57 prompt/token identity;
- Experiment 59 quality gate.

## Learner should reject

- same command means same workload;
- exact model SHA must never change in a valid A/B;
- prompt text is enough without token identity;
- a manifest validator proves benchmark truth;
- every cross-vendor comparison is causal one-variable evidence.
