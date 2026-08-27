# Spec 0009 — Cross-Vendor Documented Compatibility Coverage

Status: implemented and verified  
Date: 2026-08-28

## Goal

Expand the production compatibility catalog beyond one NVIDIA example while preserving the I02 rule:

~~~text
documented support
!=
measured deployment support
~~~

This slice covers one concrete hardware target in each major course ecosystem using the same model/runtime identity:

~~~text
Qwen3-8B
+ llama.cpp
~~~

## Production hardware seeds

~~~text
NVIDIA GeForce RTX 3090 24GB
AMD Radeon RX 7900 XTX 24GB
Apple Mac Studio M4 Max, 40-core GPU, 64GB unified memory
Intel Arc A770 16GB
~~~

## Backend paths

~~~text
NVIDIA → CUDA
AMD    → HIP
Apple  → Metal
Intel  → SYCL
~~~

## Source composition

A compatibility observation may require more than one official source.

For this slice the documented path is composed from:
1. exact hardware/product documentation;
2. current llama.cpp backend documentation;
3. current upstream Qwen3 model-loader implementation;
4. vendor runtime compatibility documentation where needed.

The catalog preserves the bounded claim rather than pretending one source proves the whole deployment.

## Current upstream snapshot

llama.cpp current README blob:

~~~text
0b5598c6e5bd9a8130136ee5009cbc500729c953
~~~

It documents:
- CUDA → Nvidia GPU;
- HIP → AMD GPU;
- Metal → Apple Silicon;
- SYCL → Intel GPU.

Current Qwen3 loader blob:

~~~text
f4b2a2aebe0f8ce8df355314e5b0429111d25254
~~~

Current SYCL documentation blob:

~~~text
8b68851ff565848cb812cd9626f1c105754ac376
~~~

The SYCL document explicitly lists Arc A770 among verified Intel devices.

## AMD boundary

Current AMD ROCm compatibility documentation lists Radeon RX 7900 XTX / RDNA3 / gfx1100 as supported hardware.

This establishes a current ROCm hardware-support prerequisite.

It does not prove:
- a particular llama.cpp build;
- a particular GGUF quant;
- the local driver/ROCm combination;
- real performance.

## Apple boundary

Current Apple Mac Studio technical specifications document a configurable M4 Max:
- 16-core CPU;
- 40-core GPU;
- 64GB unified memory.

Current llama.cpp documentation identifies Apple Silicon as first-class and Metal as the Apple Silicon GPU backend.

This does not prove the exact model artifact fits the usable unified-memory budget or meets a target TG/SLO.

## Intel boundary

Intel's current Arc A770 16GB specification documents:
- Arc A770 desktop;
- Xe HPG;
- 16GB GDDR6.

Current llama.cpp SYCL docs list Arc A770 among verified devices.

This still requires the exact:
- driver;
- oneAPI;
- llama.cpp build;
- artifact/quant;
- workload

to be tested.

## Catalog semantics

All four production paths remain:

~~~text
DOCUMENTED_SUPPORTED
→ NEEDS-TEST
~~~

No performance numbers are added.

## Self-test

The production preflight now explicitly checks:

~~~text
RTX 3090 / CUDA
RX 7900 XTX / HIP
M4 Max / Metal
Arc A770 / SYCL
~~~

All must return:

~~~text
PREFLIGHT: NEEDS-TEST
~~~

until exact measured Evidence is ingested.

## Freshness

New I08 observations use:

~~~text
observed_at: 2026-08-28
revalidate_after: 2026-09-28
~~~

Revalidate earlier if:
- llama.cpp backend support changes;
- ROCm support changes;
- oneAPI/SYCL support changes;
- model-loader support changes;
- a purchase/deployment decision is imminent.