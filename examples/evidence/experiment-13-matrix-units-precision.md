# Evidence — Experiment 13: Matrix Units / Precision / TOPS

状态：stable research + L0 synthetic model verified；real GEMM shape probe ready。

## Claim

> Storage precision, matrix input precision, accumulation precision and advertised peak throughput must be treated separately. Low-bit LLM speedups can come from memory-bandwidth reduction even when the kernel does not execute native low-bit matrix arithmetic.

## L0 synthetic evidence

Experiment:
- `labs/experiments/21-tops-vs-roofline-model/`

Synthetic paths:
- FP32 peak 50;
- FP16 matrix peak 200;
- INT8 peak 400;
- native INT4 peak 800;
- Q4 weight-only uses FP16-like 200 compute peak + dequant overhead.

These are arbitrary teaching peaks, not GPU specs.

### Prefill-like

AI = 200 ops/byte, memory roof = 200 TOPS-equivalent.

Results:
- FP32 effective: 42.5;
- FP16 matrix: 180;
- INT8: ~190.5 after memory roof + overhead;
- native INT4: ~185.2 after memory roof + overhead;
- Q4 weight-only: ~154.5.

Lesson:
higher theoretical peak stops helping after the workload hits another roof.

### Decode-like

AI = 4 ops/byte.

All paths first hit the same 4 TOPS-equivalent memory roof before overhead.

Lesson:
```
50 vs 800 advertised compute peak
can collapse to almost no practical gap
when the workload is memory-bound
```

## Primary-source architecture evidence

NVIDIA official:
- Volta/Turing/Ampere Tensor Core evolution;
- Ampere BF16/TF32/FP64 additions;
- input and accumulator types differ;
- Hopper fourth-gen + FP8;
- current Blackwell fifth-gen + FP4-class modes.

AMD official:
- CDNA MFMA matrix units;
- FP16 example with FP32 accumulation;
- current precision support varies by CDNA/RDNA generation.

## Real Evidence path

Experiment 22:
- compare large-M and M=1 matmul;
- FP32/FP16/BF16;
- exact runtime identity;
- no fake INT4 path.

## Stable conclusions

- 4-bit storage is not proof of native INT4/FP4 matrix arithmetic.
- accumulator precision is separate from input precision.
- matrix TOPS is a compute roof for a specific precision/mode.
- shape/utilization and memory bandwidth determine achieved throughput.
- quantized decode can accelerate by reducing weight bytes alone.
