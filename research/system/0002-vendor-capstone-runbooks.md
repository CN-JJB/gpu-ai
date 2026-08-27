# Research Note 0017 — Vendor Capstone Runbooks

日期：2026-08-27

## Goal

Apply the same controlled optimization capstone to four ecosystems without pretending their device models are identical.

Shared loop:

```
device identity
→ backend build/runtime identity
→ model SHA
→ baseline PP/TG
→ vendor telemetry
→ bottleneck hypothesis
→ ONE variable
→ Experiment 40 validation
→ compare
```

The scientific loop is shared.
The commands, memory model and support boundaries are not.

---

# NVIDIA / CUDA

Current pinned llama.cpp build entry:

```bash
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release
```

Device proof:

```bash
nvidia-smi -L
nvidia-smi --query-gpu=name,compute_cap,driver_version,memory.total,pci.bus_id --format=csv
./build/bin/llama-bench --list-devices
```

Important checks:
- exact compute capability;
- current CUDA/driver support;
- actual device chosen by llama.cpp;
- model fully resident or hybrid;
- PP vs TG.

Good first optimization candidates **only if evidence points there**:
- FlashAttention for PP/attention path;
- quant/backend for bandwidth-bound TG;
- KV type/context for capacity pressure;
- multi-GPU split if one GPU cannot fit or scaling is the explicit goal.

Stop and investigate before optimizing when:
- device is not listed;
- old architecture requires pinned CUDA;
- driver/runtime mismatch;
- memory capacity is already failing.

---

# AMD / ROCm-HIP

Current pinned llama.cpp build entry:

```bash
rocminfo
hipconfig --full
```

Then:

```bash
HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)" \
cmake -S . -B build \
  -DGGML_HIP=ON \
  -DGPU_TARGETS=<exact-gfx-target> \
  -DCMAKE_BUILD_TYPE=Release

cmake --build build --config Release -j
```

Current upstream says `GPU_TARGETS` is optional; specifying it is useful when you deliberately target one known GPU.

Device proof:
- `amd-smi`;
- `rocminfo`;
- exact `gfx*` target;
- llama.cpp device list.

Important rule:

```
hardware enumerates
!= exact ROCm libraries/backend fully supported
```

Do not make `HSA_OVERRIDE_GFX_VERSION` the default recipe for an unsupported GPU.
If a workaround is required, label the run as:
```
community-enabled
```
and separate it from official-current support.

Good first optimization candidates:
- FA/backend when PP is weak;
- quant/memory traffic when TG is bandwidth-bound;
- KV/context when memory margin is low.

---

# Apple / Metal

Current pinned upstream behavior:

```
macOS build
→ Metal enabled by default
```

Build:

```bash
cmake -B build
cmake --build build --config Release
```

Metal can be disabled at build time with:
```
-DGGML_METAL=OFF
```

so device/startup logs are still required proof.

Device/system proof:
- `system_profiler SPHardwareDataType SPDisplaysDataType`;
- installed unified memory;
- Experiment 28 Metal properties;
- llama.cpp device list.

Memory interpretation:

```
installed unified memory
!= safe model working set
```

Record:
- installed UMA;
- recommended GPU working set when available;
- model/KV/runtime footprint.

Good first optimization candidates:
- model/quant choice if capacity or TG bytes dominate;
- FA/backend path if PP is weak;
- context/KV if unified-memory headroom becomes tight.

Do not translate:
```
Metal backend
→ Neural Engine
```

and do not assume M5 GPU neural/tensor hardware is active without runtime evidence.

---

# Intel / SYCL

Current pinned llama.cpp build entry:

```bash
source /opt/intel/oneapi/setvars.sh
sycl-ls
```

Current Intel GPU build:

```bash
cmake -B build \
  -DGGML_SYCL=ON \
  -DCMAKE_C_COMPILER=icx \
  -DCMAKE_CXX_COMPILER=icpx \
  -DGGML_SYCL_F16=ON

cmake --build build --config Release -j
```

Current upstream also provides:
```
./examples/sycl/build.sh
```

Device proof:

```bash
sycl-ls
./build/bin/llama-ls-sycl-device
./build/bin/llama-bench --list-devices
```

Current SYCL path is Intel-first and uses Level Zero by default for Intel GPU devices.

Important:
- discrete Arc VRAM and integrated shared system memory are different capacity models;
- XMX existence does not prove the selected quant kernel uses XMX;
- exact oneAPI/runtime version matters.

Good first optimization candidates:
- FP16 vs FP32 SYCL build only as a controlled runtime-build experiment;
- FA/backend for PP;
- quant/reorder path for TG;
- device selection when iGPU and dGPU are both visible.

---

# Shared preflight stop conditions

Do not start an optimization A/B if any of these are unresolved:

- exact device unknown;
- runtime/backend unknown;
- model SHA unknown;
- workload does not fit;
- driver/backend support state unknown;
- baseline is unstable;
- temperature/power state is abnormal;
- more than one intended variable is already changing.

Return to the relevant earlier slice instead.

---

# Shared graduation output

For every vendor path, the final packet should look the same conceptually:

```
profile.txt
baseline manifest
baseline raw JSON
hypothesis
candidate manifest
candidate raw JSON
validate_ab output
compare_bench output
CAPSTONE-CARD
```

Vendor diversity changes the evidence sources, not the requirement for evidence.
