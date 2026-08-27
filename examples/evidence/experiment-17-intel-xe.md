# Evidence — Experiment 17: Intel Xe / Arc / XMX

状态：stable Intel architecture coverage complete; L0 terminology checker verified; real XPU/SYCL inventory path ready.

## Claim

> Intel GPU architecture should be understood through EU/Vector Engine/Xe-Core/XMX plus the oneAPI/SYCL/Level Zero software stack. Hardware XMX capability does not by itself prove a local-LLM quant kernel uses XMX.

## Stable official evidence

Intel current Xe optimization guide documents:
- Vector Engine as smallest thread-level Xe building block；
- multiple hardware threads per Vector Engine；
- SIMD 16/32 execution；
- per-thread GRF；
- Xe-Core containing vector and matrix engines；
- shared L1 and SLM；
- Xe2/Battlemage as a newer Xe generation。

Intel Xe-HPG material documents XMX / DPAS-style matrix acceleration.

Stable interpretation:
```
EU-era terminology
→ modern Xe-Core / Vector Engine / XMX organization
```

without claiming physical 1:1 identity across generations.

## L0 verification

Experiment:
`labs/experiments/29-intel-xe-terminology-traps/`

Reference answers:

```
10 / 10 PASS
```

Rejected claims:
- EU = CUDA core 1:1；
- Xe-Core = Vector Engine；
- Xe-LP has the same Arc XMX path；
- Intel subgroup always 32；
- SLM is VRAM；
- Level Zero is architecture；
- XMX guarantees arbitrary Q4 GGUF native execution。

## Real Evidence path

Experiment 30 records:

```
PCI
→ sycl-ls / Level Zero
→ torch.xpu
→ llama.cpp SYCL
```

along with:
- dedicated vs shared memory；
- device/global memory；
- subgroup/workgroup；
- driver/build；
- raw output。

No Intel tokens/s values are prefilled.

## Dynamic current evidence

Current 2026:
- oneAPI Toolkit 2026.1；
- PyTorch current XPU support validates Arc A/B and current integrated Arc families；
- llama.cpp current SYCL backend is Intel-first and has current FlashAttention/oneDNN/oneMKL paths；
- Arc B580 is current Xe2 12 GB / 456 GB/s consumer reference；
- 2026 Arc Pro B70/B65 offer current 32 GB workstation VRAM options。

These facts live in:
`intelligence/gpu/intel-oneapi-xpu-2026-08-27.md`.

## Learner should reject

- core-count-only cross-vendor comparisons；
- XMX-count / Tensor-Core-count ratio performance estimates；
- “SYCL = automatic portability/performance”；
- “Level Zero = architecture”；
- “integrated global memory = dedicated VRAM”；
- “Arc has XMX so every Q4 model runs XMX”；
- “current Intel driver alone proves PyTorch/llama.cpp support”。
