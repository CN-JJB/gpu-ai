# Evidence — Experiment 23: Four-Vendor Capstone Runbooks

状态：four vendor runbooks implemented; current llama.cpp build/device entry points verified against pinned upstream.

## Claim

> NVIDIA CUDA, AMD HIP, Apple Metal and Intel SYCL should share one experimental method but keep their own device identity, memory model and software-support evidence.

## Current upstream pin

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

## Verified current build entry points

### NVIDIA

```
-DGGML_CUDA=ON
```

### AMD

```
-DGGML_HIP=ON
-DGPU_TARGETS=<gfx>  # optional upstream, explicit in course when known
```

### Apple

Current macOS upstream build:
```
Metal enabled by default
```

### Intel

```
-DGGML_SYCL=ON
-DGGML_SYCL_F16=ON   # current recommended high-performance option in SYCL docs
```

Current upstream also provides:
```
examples/sycl/build.sh
```

## Device proof

Runbooks require both:
```
vendor runtime sees device
+
llama.cpp sees device
```

Examples:
- nvidia-smi + llama-bench device list;
- rocminfo/amd-smi + llama-bench;
- Apple system/Metal evidence + llama-bench;
- sycl-ls/llama-ls-sycl-device + llama-bench.

## Support boundaries preserved

### AMD
Community override/workaround is not silently upgraded to official support.

### Apple
Metal GPU is not called Neural Engine; installed UMA is not called free VRAM.

### Intel
Arc dGPU dedicated VRAM is not merged with iGPU shared memory; XMX availability is not kernel-use proof.

### NVIDIA
Old architecture/toolkit lifecycle remains a separate software gate.

## Experiment 41

Preflight scripts are read-only/best-effort and intentionally allow NOT READY outcomes.

A device visible to the vendor driver but absent from llama.cpp is:
```
not ready for performance tuning
```

The learner should return to support/build investigation first.

## Shared controlled-A/B method

All four runbooks reuse:
```
labs/experiments/40-real-llm-capstone/
```

No vendor-specific benchmark methodology is invented.
