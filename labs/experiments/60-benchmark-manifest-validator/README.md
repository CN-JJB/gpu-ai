# Experiment 60 — Semantic Benchmark Manifest Validator

硬件等级：L0

## Goal

Prove that "one variable" can be a semantic block.

Synthetic experiment:

```
Q8_0 artifact
→
Q4_K_M artifact
```

The model change necessarily changes:
- artifact SHA;
- bytes;
- quant label.

All belong to:

```
variant.model
```

## Valid run

```bash
python3 validate_manifest_ab.py \
  baseline.json \
  candidate-valid.json
```

Expected:

```
VALIDATION: PASS
```

Semantic differences should be only:

```
variant.model.artifact_bytes
variant.model.artifact_sha256
variant.model.quant
```

## Invalid run

```bash
python3 validate_manifest_ab.py \
  baseline.json \
  candidate-invalid-prompt.json
```

Expected non-zero exit and:

```
VALIDATION: FAIL
undeclared differences:
variant.prompt.token_ids_sha256
```

## Leaf-variable mode

For an execution-only A/B, declare for example:

```
intentional_variable
=
variant.execution.flash_attention
```

Then only that exact semantic leaf may change.

## Scope

The manifests use synthetic hashes and device names.

No performance or quality result is implied.
