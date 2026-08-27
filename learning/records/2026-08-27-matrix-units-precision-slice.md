# Learning / Build Record — 2026-08-27 Matrix Units / Precision Slice

## Slice

13 — Matrix units, precision, accumulators and TOPS.

## New distinctions

```
storage
!= matrix input datatype
!= accumulator datatype
!= output datatype
```

and:

```
theoretical peak
!= achieved matrix throughput
!= end-to-end LLM throughput
```

## Architecture bridge

NVIDIA high-level:
- Volta → Tensor Core begins;
- Turing → integer/sub-byte inference modes expand;
- Ampere → BF16/TF32/FP64 matrix modes;
- Hopper → FP8 / fourth-gen;
- Blackwell → fifth-gen / FP4-class current modes.

AMD:
- MFMA matrix units;
- generation-specific CDNA/RDNA precision support.

## Key local-LLM lesson

```
Q4 model
can be:
Q4 storage
→ dequant
→ FP16/BF16 compute
```

So Q4 speedup can come from lower VRAM traffic without native INT4 compute.

## L0 verified

Synthetic prefill-like workload benefits from higher compute roofs until memory roof/overhead dominate.

Synthetic decode-like workload with AI=4 hits the memory roof across all advertised compute peaks.

No synthetic peak is a real GPU spec.

## Real path

Experiment 22 isolates:
- large-M GEMM;
- M=1 decode-like matmul;
- FP32/FP16/BF16;
- current PyTorch FP32 internal precision mode.

It intentionally does not fake an INT4 path.

## Next slice

Start detailed NVIDIA architecture generations:

```
Tesla/G80
→ Fermi
→ Kepler
→ Maxwell
→ Pascal
→ Volta
→ Turing
→ Ampere
→ Ada
→ Hopper
→ Blackwell
```

Teach each generation by:
- what bottleneck/market problem changed;
- SM/execution changes;
- memory/cache changes;
- matrix/AI changes;
- software/CUDA consequences;
- which used cards matter for local LLM today.

Stable architecture history and current used-market intelligence must remain separate.
