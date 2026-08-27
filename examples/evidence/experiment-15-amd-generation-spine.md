# Evidence — Experiment 15: AMD Architecture Generation Spine

状态：stable architecture research complete; L0 terminology/lineage assertions verified; real ROCm inventory path ready.

## Claim

> AMD GPU history must be read through AMD-native execution and product branches: GCN Wave64/CU evolved toward RDNA Wave32/WGP for graphics/latency, while CDNA became a dedicated Instinct compute/HPC/AI branch with MFMA Matrix Cores, HBM and Infinity Fabric. Current usefulness depends on exact gfx target and ROCm support, not architecture name alone.

## Stable architecture evidence

### GCN

AMD GPUOpen documents classic GCN:
- Wave64;
- four SIMD units per CU in the documented model;
- classic SIMD16 execution over four cycles;
- SGPR / VGPR distinction;
- LDS;
- resident-wave latency hiding.

### Vega

AMD official material documents:
- Rapid Packed Math;
- HBM2;
- High Bandwidth Cache Controller;
- next-generation compute unit changes.

### RDNA

Official RDNA ISA/architecture material documents:
- Wave32 and Wave64;
- Wave32 as the primary low-latency path;
- WGP organization;
- new cache hierarchy.

### RDNA2

AMD current RDNA lineage identifies:
- first-generation Infinity Cache;
- first-generation ray acceleration.

### CDNA

AMD CDNA whitepaper documents:
- dedicated compute architecture;
- MI100;
- Matrix Core Technology;
- HBM2;
- Infinity Fabric.

### CDNA2

Official whitepaper documents:
- matrix FP64;
- higher BF16/FP16;
- multi-die packaging;
- HBM2e;
- Infinity Fabric scale-up.

### RDNA3

Official AMD launch/ISA material documents:
- GCD + MCD chiplets;
- dedicated AI acceleration;
- VOPD dual-issue;
- strict Wave32/operand/register constraints.

### CDNA3

Official MI300 material documents:
- XCD compute chiplets;
- I/O dies;
- HBM3;
- large Infinity Cache;
- FP8/TF32/sparse matrix paths;
- MI300A coherent CPU+GPU shared-HBM package;
- MI300X GPU-focused package.

### RDNA4

Current AMD docs document:
- second-gen AI accelerators;
- FP8 / INT4;
- Wave32 / Wave64;
- improved on-chip scheduling;
- third-gen Infinity Cache.

### CDNA4 / CDNA5

Current AMD CDNA material documents:
- CDNA4 MI350 with MX low-precision formats and HBM3E;
- current CDNA5 MI400 frontier with new WGP, Wave32, MXFP formats and HBM4.

## L0 verification

Experiment:
`labs/experiments/25-amd-generation-terminology-traps/`

Reference answers validated:

```
12 / 12 PASS
```

Key rejected claims:
- RDNA only supports Wave32;
- Infinity Cache is VRAM;
- RDNA and CDNA are one sequential line;
- RDNA3 dual issue always gives 2×;
- MI300A and MI300X are the same package;
- RDNA4 FP8/INT4 guarantees native Q4 local-LLM execution;
- architecture name alone decides ROCm support;
- ROCm 7.14 standard support matrix already lists CDNA5.

## Real Evidence path

Experiment 26 records:
- exact GPU;
- gfx target;
- wavefront properties;
- AMD SMI;
- ROCm/HIP;
- PyTorch HIP build;
- official support matrix status;
- raw output.

No real Radeon/Instinct benchmark numbers are fabricated.

## Dynamic 2026 software evidence

Current ROCm 7.14 support:
- Instinct CDNA through CDNA4 in standard table;
- current Radeon RDNA4/RDNA3 and selected RDNA2 paths;
- exact support depends on SKU/OS/component.

Current release notes also contain a version-specific known issue for lower-than-expected LLM inference performance on RDNA3 Radeon and Ryzen AI Max/Max+.

These facts live in:
`intelligence/gpu/amd-rocm-generation-support-2026-08-27.md`.

## Learner should reject

- "AMD wavefront = always 64";
- "Wave32 means RDNA is the same as NVIDIA warp32";
- "WGP = just another name for SM";
- "Infinity Cache adds model capacity";
- "new Radeon architecture = good ROCm automatically";
- "MFMA unit count compares directly with Tensor Core count";
- "VOPD means every shader is 2×";
- "FP8/INT4 hardware support proves a Q4 backend uses native AI units";
- "AMD GPU driver visibility means full ROCm library support".
