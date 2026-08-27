# Intel Xe / oneAPI / XPU Snapshot — 2026-08-27

Purpose: dynamic support/product snapshot for Slice 17.

Stable material:
- `research/gpu/0011-intel-xe-arc-xmx-oneapi.md`
- `reference/gpu/intel-xe-arc-xmx.md`
- `lessons/17-intel-xe/`

## Current oneAPI

Intel oneAPI Toolkit current release:
```
2026.1
```

Intel unified the former Base Toolkit + HPC Toolkit starting with 2026.0.

Current Intel GPU support list includes:
- Intel UHD 11th-gen+；
- Iris Xe；
- Arc；
- Server GPU；
- Flex；
- Data Center GPU Max。

oneAPI provides:
- DPC++/C++ SYCL compiler；
- optimized math/AI libraries；
- Level Zero backend/runtime path；
- debug/profile tools。

## Level Zero

Current Intel compiler docs use Level Zero as the low-level Intel GPU backend for:
- device discovery；
- memory；
- queues/commands；
- multi-card/tile control。

`sycl-ls` is the standard current way to see SYCL backends/devices.

Current naming examples:
```
[level_zero:gpu]
```

`ONEAPI_DEVICE_SELECTOR` filters/selects visible devices.

## Current PyTorch XPU

Current PyTorch docs:
```
torch.xpu
```

Last updated May 2026 in the current documentation snapshot.

Current validated Intel client GPU families include:
- Arc A-Series / Alchemist；
- Arc B-Series / Battlemage；
- Meteor Lake integrated Arc；
- Arrow Lake integrated Arc；
- Lunar Lake；
- current newer Core Ultra paths by OS/version。

Do not infer:
```
driver sees GPU
→ current PyTorch wheel has XPU support
```

The build/runtime must be checked.

## Current llama.cpp SYCL backend

Pinned upstream:
```
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current `docs/backend/SYCL.md` states:
- backend primarily designed for Intel GPUs；
- current verified hardware includes Arc A-Series, Arc B-Series, built-in Arc, Flex, Data Center Max and newer Intel iGPUs；
- Linux and Windows supported；
- Level Zero is the main Intel runtime path；
- oneDNN / oneMKL integration exists；
- FlashAttention support added in 2026；
- quantized matmul/reorder and fused-MoE work continued in 2026；
- current multi-GPU supports layer and tensor modes；
- row split is currently not supported。

Current SYCL backend removed NVIDIA/AMD plugin support in 2026 because the oneAPI plugins were no longer practically available through supported channels.

Therefore current course interpretation:
```
llama.cpp SYCL
→ Intel-first backend
```

not a universal replacement for CUDA/HIP.

## Current Arc B580

Current Intel product data:
- Battlemage / Xe2；
- 20 Xe-Cores；
- 160 XMX engines；
- 12 GB GDDR6；
- 456 GB/s memory bandwidth；
- PCIe 4.0 x8 current product interface；
- current published AI peak is an INT8/XMX product metric。

Use case:
a relatively modern 12 GB dGPU with current Intel software support.

Do not turn INT8 TOPS into expected GGUF tokens/s.

## Current Arc B570

Current Intel product data:
- 18 Xe-Cores；
- 144 XMX；
- 10 GB；
- 380 GB/s。

Again dynamic product facts only.

## Current 2026 Arc Pro B-Series

Current workstation lineup materially changes Intel local-AI capacity options.

Current Intel product guide:
- Arc Pro B70: 32 GB GDDR6, 608 GB/s, 32 Xe2 cores, 256 XMX；
- Arc Pro B65: 32 GB GDDR6, 608 GB/s, 20 Xe2 cores, 160 XMX；
- B60/B50 smaller variants.

This makes Intel a more relevant local-LLM/workstation capacity option than older consumer Arc alone.

Important:
- workstation driver/support；
- actual street price；
- power；
- backend maturity；
- current model kernels；

must still be measured.

## Current Arc Pro B70 ECC note

Intel currently documents that ECC can reduce user-visible VRAM capacity on B70-class products.

That is a useful buyer lesson:

```
advertised physical VRAM
!= necessarily runtime-available VRAM
```

when ECC/reservation is enabled.

## Current llama.cpp SYCL memory paths

Current backend includes dynamic implementation options for:
- direct Level Zero allocation；
- host-memory fallback；
- VMM；
- current experimental system-USM path on Xe2+ Linux systems.

These are runtime details, not stable architecture features.

Do not teach:
```
Battlemage = unified memory
```

Arc B-series remains a discrete VRAM GPU.

## Current FlashAttention

Current llama.cpp SYCL backend has:
- native SYCL flash-attention；
- current oneDNN fused SDPA path；
- current oneMKL-assisted conditions for some quantized-KV prefill paths。

Exact env vars/conditions change rapidly; record current build/help.

## Intel support-state vocabulary

### Hardware capability
Xe-Core / XMX exists.

### Driver visible
OS driver enumerates GPU.

### Level Zero/SYCL visible
oneAPI runtime sees GPU.

### Framework visible
torch.xpu or llama.cpp sees GPU.

### Kernel optimized
target quant/attention actually maps efficiently to XMX/vector path.

### Workload competitive
PP/TG benchmark justifies the card.

Never collapse these into:
```
"Arc supports AI"
```

## Revalidation triggers

Re-check when:
- oneAPI release changes；
- PyTorch XPU validated hardware changes；
- llama.cpp SYCL current news/known issues change；
- Arc/Celestial/new Xe generations appear；
- Intel client driver branches change；
- Arc Pro product availability/pricing changes。
