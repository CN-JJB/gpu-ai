# Used GPU Acceptance Tooling Snapshot — 2026-08-27

Purpose: dynamic tool/support notes for Slice 20.

Stable acceptance method:
- `research/hardware/0002-used-gpu-transaction-verification.md`
- `reference/hardware/used-gpu-acceptance-checklist.md`
- `lessons/20-used-gpu-verification/`

## NVIDIA DCGM current diagnostics

Current official documentation:
https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html

Current command reference:
https://docs.nvidia.com/datacenter/dcgm/latest/reference/command-line-reference/dcgmi/dcgmi-diag.html

Current DCGM diagnostics include:
- software/deployment checks;
- framebuffer memory test;
- PCIe/NVLink;
- sustained compute diagnostic;
- memory bandwidth;
- targeted stress/power;
- deeper memtest at higher suites on supported products.

### Current memory plugin

Official docs:
https://docs.nvidia.com/datacenter/dcgm/latest/reference/diagnostics/plugins/memory.html

The memory plugin:
- allocates a significant portion of framebuffer memory (75% default in current docs);
- writes known patterns;
- reads back;
- detects mismatches;
- checks ECC error conditions where applicable.

Current canonical named form:

```bash
dcgmi diag --run memory
```

Parameters/support are product/config dependent.

### GeForce caveat

Current DCGM command reference states non-datacenter GPUs support level 1, while higher diagnostic availability must be explicitly supported/documented for the product.

Therefore:

```
DCGM installed on GeForce
!=
all DCGM memory/stress suites supported
```

The course does not tell learners to force unsupported diagnostic levels.

---

## memtest_vulkan current state

Project:
https://github.com/GpuZelenograd/memtest_vulkan

Current README:
- cross-platform Vulkan compute memory test;
- reports memory errors during execution;
- current standard period guidance around five minutes;
- Vulkan 1.1 driver path required.

Current project also documents limitations:
- some drivers may expose/test less than full VRAM;
- integrated GPU memory accounting can be unusual;
- some AMD configurations have known load/usage caveats;
- Vulkan driver conflicts can affect test startup.

Current release history page identifies v0.5.0 as the latest published release, with artifacts originally created in 2022 and later republished.

Course status:

```
useful cross-vendor extra evidence
not vendor certification
not proof of future reliability
```

Record exact release/hash and actual tested allocation.

---

## AMD current RAS / ECC

Current AMD SMI RAS docs:
https://rocmdocs.amd.com/projects/amdsmi/en/latest/conceptual/ras.html

AMD documents:
- correctable ECC events;
- uncorrectable ECC events;
- RAS error counts;
- CPER reporting.

Practical current rule:

```
supported Instinct / ECC-capable device
→ record RAS/ECC before and after test
```

Consumer Radeon products may not expose the same ECC/RAS capabilities.

Do not demand fields the hardware does not support.

---

## llama.cpp as acceptance workload

Pinned current upstream used by the course:
```
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Existing course benchmark workflow already separates:
- PP;
- TG;
- exact model artifact;
- raw JSON;
- backend identity.

Why it is useful in acceptance testing:

```
real model allocation
+ actual backend kernels
+ memory traffic
+ sustained workload
```

It complements synthetic stress tools.

It does not replace framebuffer memory-integrity testing.

---

## Platform inspection

Current published Xianyu inspection buyer agreement remains a transaction protection reference.

Course boundary:

```
platform inspection
→ independent transaction evidence for covered attributes

GPU acceptance packet
→ identity + memory + compute + thermal + error evidence
```

These can complement each other.

---

## Current recommended tool order

### All cards

1. vendor identity/inventory;
2. system/kernel errors;
3. supported memory-integrity test;
4. short workload;
5. sustained target workload;
6. after-test error state.

### NVIDIA datacenter

Prefer official DCGM diagnostics where the exact GPU/plugin is supported.

### Cross-vendor consumer cards

Use:
- vendor telemetry;
- optional memtest_vulkan;
- workload-relevant tests;
- error logs.

Do not pretend one cross-vendor utility covers every vendor health feature.

---

## Revalidation triggers

Re-check when:
- DCGM major version changes;
- diagnostic availability by GPU class changes;
- memtest_vulkan releases a new build;
- AMD SMI RAS interfaces change;
- llama.cpp backend behavior changes;
- platform inspection scope changes.
