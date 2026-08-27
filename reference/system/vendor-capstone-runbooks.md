# Vendor Capstone Runbook — Quick Reference

## NVIDIA CUDA

### Preflight

```bash
nvidia-smi -L
nvidia-smi --query-gpu=name,compute_cap,driver_version,memory.total --format=csv
```

### Build

```bash
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release
```

### Prove backend

```bash
./build/bin/llama-bench --list-devices
```

### First optimization branch

Choose from evidence:
- PP weak → FA/backend
- TG near bandwidth roof → quant/memory traffic
- low VRAM margin → KV/context
- multi-GPU goal → split/topology

---

## AMD ROCm/HIP

### Preflight

```bash
amd-smi list
rocminfo
hipconfig --full
```

### Build

```bash
HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)" \
cmake -S . -B build -DGGML_HIP=ON -DGPU_TARGETS=<gfx> -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j
```

### Prove backend

```bash
./build/bin/llama-bench --list-devices
```

### Stop if

Exact GPU needs an unsupported/community workaround you have not explicitly accepted.

---

## Apple Metal

### Preflight

```bash
system_profiler SPHardwareDataType SPDisplaysDataType
```

Reuse Experiment 28 for:
- unified memory;
- recommended working set;
- Metal pipeline properties.

### Build

```bash
cmake -B build
cmake --build build --config Release
```

Metal is current upstream default on macOS.

### Prove backend

```bash
./build/bin/llama-bench --list-devices
```

### Interpret

Do not call installed UMA "VRAM".
Do not call Metal GPU "Neural Engine".

---

## Intel SYCL/XPU

### Preflight

```bash
source /opt/intel/oneapi/setvars.sh
sycl-ls
```

### Build

```bash
cmake -B build \
  -DGGML_SYCL=ON \
  -DCMAKE_C_COMPILER=icx \
  -DCMAKE_CXX_COMPILER=icpx \
  -DGGML_SYCL_F16=ON
cmake --build build --config Release -j
```

### Prove backend

```bash
./build/bin/llama-ls-sycl-device
./build/bin/llama-bench --list-devices
```

### Interpret

- Arc dGPU → dedicated VRAM
- Intel iGPU → shared system memory
- XMX available ≠ target quant kernel proven to use XMX

---

## Shared A/B

Always reuse:

```
labs/experiments/40-real-llm-capstone/
```

Do not invent a second benchmark methodology per vendor.
