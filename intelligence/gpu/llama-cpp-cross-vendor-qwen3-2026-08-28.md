# llama.cpp × Qwen3 Cross-Vendor Compatibility Snapshot — 2026-08-28

Purpose: dated dynamic intelligence behind the production I08 compatibility observations.

This file does not replace real runtime Evidence.

## Current upstream identities

llama.cpp README blob:

~~~text
0b5598c6e5bd9a8130136ee5009cbc500729c953
~~~

Qwen3 model-loader blob:

~~~text
f4b2a2aebe0f8ce8df355314e5b0429111d25254
~~~

SYCL backend documentation blob:

~~~text
8b68851ff565848cb812cd9626f1c105754ac376
~~~

## Current documented paths

| ecosystem | concrete hardware | backend | catalog status | preflight |
|---|---|---|---|---|
| NVIDIA | GeForce RTX 3090 24GB | CUDA | DOCUMENTED_SUPPORTED | NEEDS-TEST |
| AMD | Radeon RX 7900 XTX 24GB | HIP | DOCUMENTED_SUPPORTED | NEEDS-TEST |
| Apple | Mac Studio M4 Max 40-core GPU / 64GB unified memory | Metal | DOCUMENTED_SUPPORTED | NEEDS-TEST |
| Intel | Arc A770 16GB | SYCL | DOCUMENTED_SUPPORTED | NEEDS-TEST |

## llama.cpp backend documentation

Current upstream README maps:
- CUDA to Nvidia GPU;
- HIP to AMD GPU;
- Metal to Apple Silicon;
- SYCL to Intel GPU.

It also describes Apple Silicon as a first-class target.

Source:
- https://github.com/ggml-org/llama.cpp/blob/master/README.md

## Qwen3 loader

Current upstream source contains the Qwen3 model implementation and recognizes the 8B architecture shape.

Source:
- https://github.com/ggml-org/llama.cpp/blob/master/src/models/qwen3.cpp

This establishes loader implementation existence, not exact artifact success.

## AMD RX 7900 XTX

Hardware source:
- https://www.amd.com/en/products/graphics/desktops/radeon/7000-series/amd-radeon-rx-7900xtx.html

Current AMD documentation records:
- RDNA3;
- 24GB GDDR6.

Current ROCm compatibility matrix:
- https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html

The current ROCm matrix lists RX 7900 XTX as supported hardware.

Still unknown until measured:
- exact OS/driver/ROCm combination;
- exact llama.cpp commit/build;
- exact GGUF/quant;
- PP/TG;
- quality;
- sustained behavior.

## Apple M4 Max

Hardware source:
- https://www.apple.com/uk/mac-studio/specs/

Current Mac Studio specs document a configuration with:
- M4 Max;
- 16-core CPU;
- 40-core GPU;
- 64GB unified memory.

llama.cpp current docs map Metal to Apple Silicon.

Still unknown until measured:
- usable unified-memory headroom for the exact artifact;
- exact macOS/runtime build;
- actual Metal offload behavior;
- PP/TG;
- quality;
- serving behavior.

## Intel Arc A770 16GB

Hardware source:
- https://www.intel.com/content/www/us/en/products/sku/229151/intel-arc-a770-graphics-16gb/specifications.html

Intel documents:
- Arc A770 desktop;
- Xe HPG;
- 16GB GDDR6.

llama.cpp SYCL source:
- https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/SYCL.md

Current SYCL docs explicitly list Arc A770 as a verified Intel device and document oneAPI/SYCL environment requirements.

Still unknown until measured:
- exact driver and oneAPI combination;
- exact current llama.cpp build;
- exact GGUF/quant;
- PP/TG;
- quality;
- sustained behavior.

## Stable evidence rule

~~~text
backend documented
+ hardware documented
+ model loader documented
→ DOCUMENTED_SUPPORTED
→ NEEDS-TEST
~~~

Only exact runtime Evidence may create:

~~~text
MEASURED_SUPPORTED
→ PASS-MEASURED
~~~

## No performance ranking

This snapshot contains no comparative tok/s values.

Do not infer vendor ranking from documented support.

## Revalidation triggers

Re-check before:
- a purchase;
- a real deployment;
- a new llama.cpp major/backend change;
- a ROCm/oneAPI compatibility change;
- a new model architecture revision;
- the catalog revalidate_after date.