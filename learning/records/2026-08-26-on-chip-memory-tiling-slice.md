---
date: 2026-08-26
type: course-build-record
---

# GPU on-chip memory / tiling vertical slice completed

第三个 bounded slice 完成：

Research → Reference → HTML Lesson → L0 Experiment → Example Evidence → optional L2 real-GPU Experiment → Resources update → Learning update。

## Built artifacts

- research/gpu/0003-on-chip-memory-tiling-reuse.md
- reference/gpu/on-chip-memory-tiling-reuse.md
- lessons/03-gpu-memory/01-registers-shared-tiling-reuse.html
- labs/experiments/04-gemm-tile-reuse-model/
- labs/experiments/05-naive-vs-tiled-gemm/
- examples/evidence/experiment-03-gemm-tile-reuse.md
- resources/RESOURCES.md
- learning/CURRENT.md

## Research conclusions

### Registers are not simply “the fastest memory”

Registers provide thread-local reuse and accumulators, but consume finite SM/CU register resources.

More registers can:
- improve ILP；
- keep intermediates close；
- reduce memory traffic。

It can also reduce resident threads/warps and occupancy.

### Spill is the occupancy trap

NVIDIA CUDA local memory is logically thread-local but physically follows device/global-memory storage behavior; register spilling can place data there.

AMD private/scratch spill has the same teaching consequence.

Therefore:

**reducing registers just to raise occupancy can make a kernel slower.**

### Shared memory/LDS buys reuse

A block/work-group can cooperatively load a tile from global memory once, synchronize, then reuse the data many times.

This is the core bridge from execution model to GEMM.

### Coalescing and tiling solve different problems

- coalescing：让每次 global-memory transaction 更有效；
- tiling/reuse：减少需要多少次 global-memory transaction。

Lesson explicitly separates them to prevent “coalesced = memory optimized” misconception.

### Tile size is a real trade-off

Larger tiles can increase arithmetic intensity, but cost:
- threads/work per block；
- shared/LDS；
- registers；
- resident blocks；
- tile-level parallelism；
- synchronization/layout complexity。

This is directly supported by NVIDIA GEMM performance guidance and CUTLASS hierarchy.

## L0 experiment validation

For N=1024 FP32 concept GEMM, ignoring cache/broadcast:

- naive input-load requests：2,147,483,648
- tile 8：268,435,456（8× fewer）
- tile 16：134,217,728（16× fewer）
- tile 32：67,108,864（32× fewer）

Approx arithmetic intensity rises from 0.250 FLOP/B to:
- tile 8：1.992
- tile 16：3.969
- tile 32：7.877

The model intentionally exposes the cost side too:
- tile 16 → 256 threads/block, 2 KiB A+B tile
- tile 32 → 1024 threads/block, 8 KiB A+B tile

These are algorithm/resource counts, not real DRAM benchmark claims.

## L2 experiment

Added one CUDA/HIP source that compares:

- naive 16×16 GEMM
- tiled 8
- tiled 16
- tiled 32 when device limits allow

The program records:
- static shared/LDS
- occupancy API active blocks
- approximate thread occupancy
- kernel time
- GFLOP/s
- correctness

The lab also requires compiler resource reports:
- NVIDIA `nvcc -res-usage`
- AMD `hipcc --resource-usage`

and profiler evidence when available.

No fake GPU numbers are included.

## Skill workflow notes

- teach：kept one real problem, minimal prerequisites, retrieval practice, experiment/evidence loop.
- research：NVIDIA CUDA/CUTLASS and AMD ROCm/HIP official sources first.
- scaffold-exercises idea reused only as problem/solution/verifiable exercise discipline.
- domain-modeling not triggered: no new project-level glossary boundary was needed.
- to-spec/grill not triggered: scope was already frozen and current slice had no unresolved requirement branch.

## Architecture lesson

This slice confirms that “GPU execution model” and “GPU memory hierarchy” should not be taught as separate fact lists.

The useful causal model is:

resident groups
↔ register/shared resource pressure
↔ tile reuse
↔ global traffic
↔ measured throughput

That model is the correct setup for the next slice: bandwidth / arithmetic intensity / memory-bound vs compute-bound.

## Next

Build the bandwidth + Roofline-style slice, then use it to explain why LLM decode often behaves differently from large GEMM/prefill workloads without hard-coding current backend benchmark numbers.
