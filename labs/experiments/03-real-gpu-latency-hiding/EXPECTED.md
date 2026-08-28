# Expected — Experiment 03 Real GPU Latency-Hiding Sensitivity

This experiment has **no universal correct throughput number**. A valid result is a measured curve plus a defensible explanation.

## Expected qualitative shape

As dynamic shared memory / LDS reservation increases:

1. reported active blocks per SM/CU should stay the same until a resource threshold is crossed;
2. at one or more thresholds, active blocks and approximate occupancy may step down;
3. if the pointer-chain kernel still needs more resident warps/waves to hide memory latency, throughput may fall after a large residency reduction;
4. once residency is already sufficient, increasing occupancy may produce little or no benefit.

A monotonic slowdown is **not required**.

## Valid contrary results

These are not automatic failures:

- lower occupancy but higher throughput;
- little throughput change across occupancy steps;
- a non-monotonic curve.

Investigate before concluding:
- cache residency / hit behavior;
- memory transaction pattern;
- register or other resource limits;
- compiler code generation;
- clock / thermal / power state;
- profiler scheduler-stall evidence.

## PASS conditions

Your experiment is complete when:
- exact GPU + architecture are recorded;
- driver and CUDA/ROCm/compiler versions are recorded;
- each tested shared-memory/LDS setting has >=5 stable timings;
- active blocks / occupancy evidence is saved;
- the raw table is preserved;
- at least one observed threshold or lack of sensitivity is explained;
- you explicitly state what this test does **not** prove.

## BLOCKED conditions

Mark the experiment BLOCKED rather than guessing when:
- the executable/backend identity is unknown;
- tested settings silently fail/skip without being recorded;
- timings are mixed across different workloads/builds;
- thermal/background state changes materially and is not separated;
- only a single timing is available.

No synthetic result can be presented as learner-owned GPU evidence.
