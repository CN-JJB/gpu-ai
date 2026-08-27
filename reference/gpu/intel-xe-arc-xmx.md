# Intel Xe / Arc / XMX 速查

## Lineage

```
Gen / EU
→ Xe-LP
→ Xe-HPG / Arc Alchemist
→ Xe2 / Arc Battlemage
```

Datacenter branch:
```
Xe-HP / Xe-HPC
```

## Main building blocks

### Vector Engine

Intel current Xe docs:
- smallest thread-level building block；
- multithreaded；
- hardware thread executes SIMD 16/32；
- per-thread GRF。

### Xe-Core

Contains:
- Vector Engines；
- Matrix Engines / XMX on relevant families；
- shared L1；
- SLM。

Do not map one Xe-Core mechanically to one NVIDIA SM.

### XMX

```
Xe Matrix Extensions
```

Matrix/dot-product acceleration via systolic/DPAS-style paths.

Problem-class analogy:
- NVIDIA Tensor Core；
- AMD MFMA；
- Intel XMX。

Not interchangeable unit counts.

### SLM

```
Shared Local Memory
```

Transferable concept:
```
CUDA shared
≈ AMD LDS
≈ Metal threadgroup memory
≈ Intel SLM
```

## Architecture milestones

### Xe-LP
- integrated graphics focus；
- EU-era terminology；
- no Arc-class XMX path in the same sense as Xe-HPG。

### Alchemist / Xe-HPG
- Arc A-series discrete GPU；
- Xe-Core；
- XMX；
- GDDR VRAM；
- modern Intel AI/media stack。

### Battlemage / Xe2
- Arc B-series；
- second-gen Xe-Core；
- newer XMX；
- refined cache/execution。

## Software stack

```
llama.cpp / PyTorch
→ SYCL / torch.xpu
→ oneAPI libraries
→ Level Zero
→ Intel GPU
```

### SYCL
High-level heterogeneous C++ programming model.

### oneAPI
Compiler + optimized libraries + development ecosystem.

### Level Zero
Low-level Intel GPU runtime/device API.

## Subgroups

Do not assume one width.

Current Intel families expose combinations such as:
```
8 / 16 / 32
16 / 32
```

## Local LLM checklist

1. exact Arc/iGPU model?
2. discrete or integrated?
3. VRAM / shared memory?
4. memory bandwidth?
5. Xe generation?
6. XMX available?
7. driver?
8. oneAPI/SYCL version?
9. llama.cpp/PyTorch XPU backend?
10. quant kernel path?
11. PP/TG real result?

## Anti-pattern

```
"Arc has 160 XMX,
therefore 4-bit LLM is fast"
```

Wrong.

Need:
```
quant format
→ runtime
→ kernel
→ XMX/vector path
→ achieved bandwidth/compute
```
