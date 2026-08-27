# AMD Architecture / ROCm Support Snapshot — 2026-08-27

Purpose: dynamic support and buyer-risk snapshot for the stable AMD GCN→RDNA/CDNA architecture lessons.

Stable architecture material:
- `research/gpu/0009-amd-architecture-generation-spine.md`
- `reference/gpu/amd-generation-spine.md`
- `lessons/15-amd-architecture/`

## Current ROCm release snapshot

Current ROCm Core SDK:
```
7.14.0
```

Current release notes date:
```
2026-07
```

Official docs:
https://rocm.docs.amd.com/en/latest/about/release-notes.html

Important course rule:
```
ROCm version
+ exact SKU
+ gfx target
+ OS
+ component/library
```
must all be recorded.

## Current Instinct support in ROCm 7.14

Current official hardware table lists:

| architecture | target | product family |
|---|---|---|
| CDNA | gfx908 | MI100 |
| CDNA2 | gfx90a | MI200 |
| CDNA3 | gfx942 | MI300 |
| CDNA4 | gfx950 | MI350 |

The standard 7.14 support table captured here does not yet list CDNA5 / MI400 as a normal supported architecture entry.

## Current CDNA5 frontier

AMD's current architecture page now describes CDNA5 / MI400 Series.

Current architectural highlights published by AMD include:
- new WGP architecture;
- Wave32 execution;
- MXFP8 / MXFP6 / MXFP4;
- HBM4;
- rack-scale fabric focus.

Product pages list MI455X as a CDNA5 product introduced in 2026.

Interpretation:

```
hardware frontier
can move ahead of
a stable SDK support matrix
```

Therefore CDNA5 software deployment requires product-specific current validation, not assumptions from the architecture announcement.

## Current Radeon support

ROCm 7.14 unified support docs list broad current support for:
- RDNA4 Radeon RX 9000;
- RDNA3 Radeon RX 7000;
- selected RDNA2 targets/products;
- RDNA3/RDNA3.5 Ryzen APUs.

Current target families include:
```
gfx1200 / gfx1201 → RDNA4
gfx1100 / gfx1101 / gfx1102 → RDNA3
gfx115x → RDNA3.5
gfx1030 → RDNA2 support path
```

Important nuance:
the exact Radeon SKU and OS still matter.

Older Radeon-specific Windows HIP SDK tables show different support levels between:
- runtime visibility;
- full HIP SDK/library support.

Example:
some RX 6000 / gfx1031 / gfx1032 devices can have runtime support while not receiving the same full HIP SDK component support.

Do not generalize:
```
"RDNA2 is supported"
→
"every RX 6000 SKU is equally supported everywhere"
```

## Current GCN/Vega support warning

Current ROCm support tables do not list Radeon VII / GCN5.1 as supported in the current mainstream distribution.

This is a major used-card lesson:
```
high HBM bandwidth
and
interesting architecture
do not guarantee
current prebuilt ROCm library support
```

A Radeon VII can be technically attractive on memory bandwidth yet expensive in software-maintenance time.

## Current AMD SMI

Current AMD SMI docs:
```
AMD SMI 26.5.0
ROCm 7.14.0 platform
```

Current CLI includes:
- `amd-smi version`
- `amd-smi list`
- `amd-smi static`
- `amd-smi metric`
- `amd-smi topology`
- `amd-smi xgmi`

AMD states AMD SMI is intended to replace/deprecate the old `rocm_smi` CLI.

Experiment 26 saves help/version so future interface changes remain auditable.

## Current known LLM issue

ROCm 7.14 release notes currently list a known issue:

```
lower-than-expected LLM inference performance
on RDNA3 Radeon GPUs
and Ryzen AI Max / Max+ Series processors
```

This is exactly why architecture capability and current software quality must be separate course layers.

Do not turn this into:
```
"RDNA3 is bad for LLM"
```

It is a version-specific current software issue that can change.

## Current RDNA4 AI details

AMD current RDNA4 docs identify:
- second-generation AI accelerators;
- FP8 / INT4 support;
- improved scheduling;
- third-generation Infinity Cache.

AMD's RX 9000 launch material says FSR4 uses FP8 WMMA on RDNA4.

Stable interpretation:
```
consumer Radeon now has increasingly explicit low-precision AI hardware
```

Dynamic interpretation:
which local-LLM kernels actually use it depends on the runtime/backend.

## Current gfx-target discovery

Recommended Evidence sources:
- `rocminfo`
- `amd-smi`
- `hipconfig --full`
- current ROCm GPU specifications/support matrix.

Example current targets:
- gfx908 → CDNA;
- gfx90a → CDNA2;
- gfx942 → CDNA3;
- gfx950 → CDNA4;
- gfx1030 → RDNA2;
- gfx1100 → RDNA3;
- gfx1151 → RDNA3.5;
- gfx1201 → RDNA4.

Do not invent a mapping for an unknown/new target.

## Support-state vocabulary

Use:

### Officially supported
Exact SKU appears in current AMD support matrix for the target OS/component.

### Runtime-visible
Driver/HIP can enumerate it, but full library support is not established.

### Community-enabled
TheRock/community build or patch path works, but not official standard support.

### Legacy/pinned
Requires older ROCm/driver/toolchain.

These four labels should never be collapsed into one word: "works".

## Revalidation triggers

Re-check when:
- ROCm major/minor release changes;
- new Radeon/Instinct products appear;
- CDNA5 enters standard support tables;
- RDNA3 known LLM issue is resolved/changed;
- AMD SMI CLI changes;
- PyTorch/vLLM/llama.cpp support changes independently of ROCm;
- Linux vs Windows support matrices diverge.
