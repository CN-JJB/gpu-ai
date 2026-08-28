# Expected — Experiment 05 Naive vs Tiled GEMM

There is no required speedup ratio and **tiled is not guaranteed to win at every tile size**.

## Expected qualitative observations

A tiled kernel can improve performance because block/work-group cooperation reuses A/B data from shared memory / LDS instead of repeatedly fetching the same useful values from global memory.

Common shapes include:
- tiled > naive;
- tile 16 > tile 8 because reuse/overhead balance improves;
- tile 32 < tile 16 because 1024-thread blocks or resource pressure reduce scheduling flexibility;
- naive unexpectedly close to tiled because cache/broadcast/compiler behavior already removes some apparent global traffic.

## Correctness first

Every performance point is invalid if correctness fails.

Expected:
- max absolute error remains within the experiment's FP32 tolerance;
- same N, datatype and input are used for every variant.

## PASS conditions

Complete evidence includes:
- exact GPU / driver / toolchain;
- N and every tile/block shape;
- compiler resource report;
- shared/LDS bytes;
- active blocks / occupancy;
- >=5 stable kernel timings per variant;
- GFLOP/s;
- correctness;
- profiler evidence when available;
- an explanation of any non-monotonic tile result.

## Investigation triggers

If tile 32 moves fewer global bytes but is slower, inspect:
- registers/VGPR/SGPR;
- resident blocks;
- shared/LDS usage;
- bank conflicts;
- synchronization;
- spills/scratch/local memory;
- tile-level parallelism;
- clock / thermal changes.

If naive is close to tiled, inspect:
- L1/L2/cache reuse;
- problem size;
- compiler optimization;
- synchronization overhead.

## BLOCKED conditions

Block comparison when variants differ in N/datatype/input, correctness fails, timings include different measurement boundaries, or exact build/config identity is missing.
