# Expected — Experiment 07 Empirical Roofline Probe

This is a **shape experiment**, not a vendor-certified peak bandwidth or peak FLOP benchmark.

## Expected curve

As nominal arithmetic intensity increases:

### Low-AI region

Often:
- achieved GFLOP/s rises roughly with added arithmetic work;
- useful effective bandwidth is relatively high;
- the workload behaves more memory-side limited.

### Crossover

At some device/workload-specific region:
- GFLOP/s stops rising proportionally with nominal AI;
- effective useful GB/s may fall;
- added FMAs begin to expose compute/instruction/resource limits.

### High-AI region

Often:
- achieved GFLOP/s growth flattens;
- the kernel behaves more compute-side limited.

The crossover **does not have a universal AI value**.

## Important interpretation limits

Nominal useful bytes = 12 B/element is a teaching model. Actual DRAM bytes can differ because of:
- caches;
- transaction granularity;
- write behavior;
- compiler/code generation;
- working-set effects.

The high-AI point is not the GPU's official peak compute number.

## PASS conditions

Record:
- exact GPU / architecture;
- driver, CUDA/ROCm, compiler;
- workload elements / MiB;
- power/clock policy or default-state note;
- >=5 stable timings per point;
- repeats / nominal AI;
- achieved GFLOP/s and useful GB/s;
- correctness;
- compiler resources;
- profiler Roofline/memory evidence when available.

Identify:
- one low-AI point;
- the observed crossover region, or explicitly “not observed in tested range”;
- one high-AI point.

## BLOCKED conditions

Do not interpret the curve when different points use different workloads/builds, correctness fails, or thermal/background state makes timings incomparable.
