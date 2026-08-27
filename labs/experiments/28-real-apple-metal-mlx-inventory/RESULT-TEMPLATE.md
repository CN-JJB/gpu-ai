# Result — Experiment 28

## System

- Date:
- Mac model:
- Chip:
- Chip tier: base / Pro / Max / Ultra:
- macOS:
- Installed unified memory:
- Official memory bandwidth source/value:
- Thermal/power mode:

Raw:
- `apple-inventory.txt`

## Metal

- Device name:
- hasUnifiedMemory:
- recommendedMaxWorkingSetSize:
- currentAllocatedSize at probe:
- maxBufferLength:
- threadExecutionWidth:
- maxTotalThreadsPerThreadgroup:
- static threadgroup memory used by probe:

## MLX

- Installed?:
- Version:
- Default device:
- CPU device info:
- GPU device info:
- Neural Engine claimed? **No unless a separate framework Evidence proves it.**

## llama.cpp

- Commit/build:
- Metal device:
- Model:
- SHA256:
- Quant:
- Context:
- KV type:
- PP t/s:
- TG t/s:
- raw JSON:
- Metal initialization log:

## M5 / Metal Tensor status, if applicable

- M5/A19-class hardware?:
- Metal 4 capable environment?:
- runtime reports tensor support?:
- correctness tests run?:
- relevant upstream issue/PR status at test date:

## Interpretation

### Capacity
How large is installed memory vs recommended working set vs runtime footprint?

### Bandwidth
Does TG behavior look consistent with memory-bandwidth pressure?

### Compute
Does PP benefit more from GPU/tensor capability than TG?

### Unified Memory
Which copies/staging did the runtime avoid, and which buffers still exist?

### GPU vs ANE
What Evidence proves the actual compute unit?

## Buying decision

Would a different tier with:
- more memory;
- more memory bandwidth;
- more GPU compute;

change the result most for this workload?

Explain separately for model fit, PP and TG.
