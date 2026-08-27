---
date: 2026-08-26
type: course-build-record
---

# GPU bandwidth / Roofline vertical slice completed

第四个 bounded slice 完成：

Research → Reference → HTML Lesson → L0 Experiment → Example Evidence → optional L2 real-GPU Experiment → Resources update → Learning update。

## Built artifacts

- research/gpu/0004-bandwidth-arithmetic-intensity-roofline.md
- reference/gpu/bandwidth-roofline-llm-bottleneck.md
- lessons/04-gpu-bandwidth/01-bandwidth-roofline-llm.html
- labs/experiments/06-roofline-bottleneck-model/
- labs/experiments/07-real-gpu-roofline-probe/
- examples/evidence/experiment-04-roofline-bottleneck.md
- resources/RESOURCES.md
- learning/CURRENT.md

## Research conclusions

### Capacity, bandwidth and compute are separate axes

This is the first slice that directly turns architecture into garbage-hardware selection.

A learner must distinguish:
- capacity：does it fit?
- bandwidth：how fast can bytes move?
- compute：how fast can the target math execute?

No single “GPU strength” number replaces these.

### Effective bandwidth matters more than marketing bandwidth for a kernel

NVIDIA Best Practices explicitly distinguishes theoretical and effective bandwidth.

The course now requires bandwidth Evidence to record:
- useful/requested bytes；
- elapsed time；
- profiler actual traffic when available。

### Arithmetic intensity connects software to hardware

AI = FLOPs / bytes

Previous tiling work now has a higher-level interpretation:

reuse ↑
→ remote bytes ↓
→ AI ↑
→ Roofline point moves right。

### Ridge point gives a decision boundary

For an abstract GPU:

20 TFLOP/s / 500 GB/s
→ 40 FLOP/B ridge。

A workload below that balance is bounded first by memory throughput in the simple Roofline model.

### More compute can be useless

L0 experiment makes the counterexample explicit:

At AI=4:
- 20 TFLOP/s + 500 GB/s → 2 TFLOP/s ceiling
- 40 TFLOP/s + 500 GB/s → still 2 TFLOP/s
- 20 TFLOP/s + 1000 GB/s → 4 TFLOP/s

This is the clean mathematical reason not to rank decode-oriented hardware by TFLOPS alone.

### Roofline has boundaries

AMD documentation explicitly notes that Roofline ignores latency.

So the course keeps three models separate but connected:

1. scheduler / latency hiding
2. on-chip reuse / occupancy
3. throughput Roofline

A kernel can be far below both roofs because execution efficiency is poor.

## LLM connection

NVIDIA Dynamo and AMD Infera independently use the same stable high-level split:

- prefill: generally compute-bound
- decode: generally memory-bandwidth-bound

The Lesson deliberately says “usually”, not “always”.

Batch, concurrency, context length, model architecture, quantization and backend can move the actual bottleneck.

## Quantization bridge

The slice introduces a precise reason quantization can help memory-bound inference:

weight bytes ↓
→ bytes/token ↓
→ arithmetic intensity ↑
→ same raw memory bandwidth can feed more useful model work。

But it also records:
- dequant compute；
- metadata/scales；
- kernel support；
- quality。

No “4-bit = 4× faster” shortcut is taught.

## L0 validation

Three abstract GPUs:

- A: 20 TFLOP/s, 500 GB/s
- B: 40 TFLOP/s, 500 GB/s
- C: 20 TFLOP/s, 1000 GB/s

Ridges:
- A: 40 FLOP/B
- B: 80 FLOP/B
- C: 20 FLOP/B

Expected table verified with Python.

## L2 design

Added a CUDA/HIP arithmetic-intensity sweep.

All mixed kernels use:
- 2 FP32 reads
- 1 FP32 write
- increasing register-resident FMA work

Nominal AI points:
- 0.667
- 2.667
- 10.667
- 42.667
- 170.667 FLOP/B

The experiment measures:
- useful effective GB/s
- achieved GFLOP/s
- empirical crossover

and asks learners to confirm with:
- Nsight Compute Roofline
- ROCm Compute Profiler hierarchical Roofline

No fake performance values are included.

## Skill workflow

- teach：real hardware-choice problem → minimal math → experiment → transfer to LLM.
- research：official NVIDIA/AMD primary docs first.
- scaffold-exercises ideas reused only for verifiable exercise/evidence structure.
- no grill / to-spec because v1 requirements remain frozen.
- no domain-modeling change required.

## Next

Move from “how fast can bytes move?” to “how many bytes must a local LLM keep resident?”:

weights → quantization → KV cache → context → concurrency → VRAM headroom → offload.
