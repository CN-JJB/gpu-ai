# Expected — Experiment 30

没有固定设备输出。

Correct evidence chain:

```
PCI-visible
→ SYCL/Level Zero-visible
→ torch.xpu-visible
→ llama.cpp-visible
```

These states can differ.

## Valid examples

### Arc dGPU
Expect dedicated device memory reported by Arc/driver/runtime.

### Intel integrated GPU
Global/shared memory reporting may reflect system-memory access rather than dedicated VRAM.

Do not compare the number directly with an Arc A770/B580 VRAM figure.

## Valid failure modes

- no oneAPI installed；
- `sycl-ls` missing；
- driver visible but Level Zero missing；
- PyTorch build lacks XPU；
- llama.cpp not built with SYCL。

Each failure identifies a different software layer.
