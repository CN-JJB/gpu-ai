# Learning / Build Record — 2026-08-27 Capstone Controlled Optimization

## Slice

22 — Real local-LLM capstone: profile → baseline → diagnose → one-variable A/B → interpret.

## Production output

Research:
- `research/system/0001-capstone-measure-diagnose-optimize.md`

Reference:
- `reference/system/capstone-bottleneck-decision-tree.md`

Lesson:
- `lessons/22-capstone/01-measure-diagnose-one-variable.html`

Labs:
- `labs/experiments/39-capstone-bottleneck-diagnosis/`
- `labs/experiments/40-real-llm-capstone/`

Evidence:
- `examples/evidence/experiment-22-capstone-controlled-ab.md`

## Stable skill

The learner can now execute:

```
profile
→ baseline
→ bottleneck hypothesis
→ choose one variable
→ A/B discipline check
→ compare
→ interpret
→ next experiment
```

## L0 result

Bottleneck diagnosis reference:
```
7/7
```

## Real experiment safeguards

The capstone manifest validator freezes:
- model artifact identity;
- runtime identity;
- device;
- PP/TG workload;
- repetitions.

It requires one semantic config difference.

Exact command strings are retained separately as audit evidence.

## Build-time correction

A validator-design issue was found and fixed:
- command string was initially counted as an independent config change;
- it is now stored outside semantic config.

The corrected synthetic self-check detects only the declared variable.

## Graduation condition

A real learner result does **not** need to be fast.

It must be:
- reproducible;
- controlled;
- explained;
- raw-data backed.

## Next production direction

Vendor-specific practical runbooks:

```
NVIDIA CUDA
AMD ROCm/HIP
Apple Metal/MLX
Intel SYCL/XPU
```

Each should reuse the same capstone logic while preserving ecosystem-specific device discovery, memory model and backend evidence.
