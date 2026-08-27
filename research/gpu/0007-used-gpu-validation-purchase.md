# Research Note 0007 — Used-GPU Validation / Purchase Acceptance

日期：2026-08-27

## Research question

How should a secondhand GPU buyer decide whether a card is acceptable for local LLM work without relying on:

```
seller label
GPU name string
one screenshot
one 30-second stress run
```

A practical acceptance packet combines:

```
claimed identity
→ observed hardware identity
→ driver/runtime recognition
→ PCIe/link/error state
→ ordinary sustained compute workload
→ thermal/clock stability
→ decision
```

The default course path is read-only plus an ordinary inference workload. It does not flash firmware, overclock, undervolt, inject PCIe errors, or run destructive VRAM tests.

---

# Part I — Seller claim is not evidence

Seller claims can include:
- marketed model;
- VRAM size;
- board vendor;
- outputs working;
- mining/workstation history;
- “fully tested”.

Turn each material claim into an observable field.

Example:

```
claim: RTX-class 24 GiB card

observe:
PCI vendor/device/subsystem
runtime name
UUID/BDF
VRAM total
VBIOS
board/subvendor
```

A cosmetic shroud/sticker is weak evidence.

---

# Part II — Identity is multi-field

Useful evidence can include:
- PCI vendor ID;
- PCI device ID;
- subsystem vendor/device IDs;
- revision;
- BDF/bus address;
- vendor UUID where available;
- VBIOS/firmware version;
- reported VRAM size/type/vendor where supported;
- driver-visible product name.

No single field proves authenticity against every sophisticated modification.

The goal is consistency across independent views.

---

# Part III — PCI IDs vs marketing name

A product-name string is useful but should agree with lower-level identifiers.

Linux:

```
lspci -nnk
```

can expose numeric vendor/device/subsystem identity and the bound kernel driver.

Vendor tools then provide their own device/runtime identity.

Disagreement is a reason to investigate, not to invent a story.

---

# Part IV — VRAM claim

For local LLM buyers, VRAM capacity is often the purchase-critical claim.

Observe total memory through the vendor/runtime.

A major mismatch such as:

```
claimed 24 GiB
observed ~12 GiB
```

is a rejection-level discrepancy for that purchase claim.

Small unit/reporting differences such as GiB vs GB or reserved memory require interpretation.

Do not compare file-manager decimal GB to binary GiB without accounting for units.

---

# Part V — Runtime recognition

A card that appears on PCIe but cannot be used by the intended compute stack may still be unsuitable.

Check:
- vendor driver recognizes it;
- target runtime/backend sees it;
- ordinary llama.cpp/LLM workload executes.

For the course goal, successful local inference is more relevant than display-only recognition.

---

# Part VI — PCIe current state vs capability

A PCIe device has concepts such as:
- maximum/capable link generation;
- maximum/capable width;
- current negotiated generation;
- current negotiated width.

Current state can downshift when idle on some systems.

Therefore:

```
idle current Gen/width low
!= card defective
```

A better question is whether the expected link capability exists and whether a representative workload negotiates/uses a reasonable link state for the platform.

Motherboard slot wiring, CPU lane allocation, risers and bifurcation can limit the observed link even when the card itself is healthy.

---

# Part VII — Current AMD PCIe evidence

Current AMD SMI documentation exposes:
- current PCIe speed;
- current width;
- replay count;
- static maximum PCIe width/speed/interface generation;
- on supported hardware, additional PCIe recovery/NAK counters.

Current CLI:

```
amd-smi metric --pcie
```

and static bus information can provide these fields where supported.

Official:
https://rocm.docs.amd.com/projects/amdsmi/en/latest/how-to/amdsmi-cli-tool.html

The exact output is dynamic; store raw output.

---

# Part VIII — Current AMD identity evidence

Current `amd-smi static` supports categories including:
- ASIC;
- bus;
- VBIOS/IFWI;
- driver;
- VRAM;
- board.

AMD documentation distinguishes a device-type ID from a unique per-card identifier and recommends BDF/UUID for identifying a specific GPU.

Official:
https://rocm.docs.amd.com/projects/amdsmi/en/latest/reference/amdsmi-py-api.html

This is useful when several cards share the same SKU.

---

# Part IX — NVIDIA PCIe/error evidence

NVIDIA management APIs expose concepts including:
- current/max PCIe generation;
- current/max width;
- replay counters;
- device identity;
- clocks/temperature/power;
- XID/error information through appropriate tooling/logs.

NVIDIA's GPU Debug Guidelines explicitly recommend checking:
- GPU count;
- PCIe link speed;
- VBIOS;
- recent XID errors;
- CUDA workloads.

Official:
https://docs.nvidia.com/deploy/pdf/GPU_Debug_Guidelines.pdf

The default course collector stores raw `nvidia-smi -q`, `nvidia-smi -L` and PCI data rather than depending on one fragile parsed field set.

---

# Part X — Error counters need context

Possible evidence domains:
- ECC corrected/uncorrected errors where ECC exists;
- AMD RAS/ECC/bad pages where supported;
- PCIe replay/recovery/AER counters;
- NVIDIA XID records in system logs;
- runtime CUDA/HIP errors.

Important:

```
feature unsupported
!= zero errors
```

Record:

```
N/A / NOT_SUPPORTED / UNKNOWN
```

when appropriate.

---

# Part XI — ECC-capable vs consumer card

Many consumer GPUs do not expose enterprise-style ECC/RAS telemetry.

Do not reject a non-ECC consumer card merely because:

```
ECC = N/A
```

Instead use the evidence the hardware actually supports:
- ordinary compute stability;
- output correctness/quality checks;
- OS/driver errors;
- thermal/clock stability;
- repeatability.

---

# Part XII — Error-free short test is not reliability proof

A 30-second successful run proves only that this short run completed.

It does not prove:
- long-term reliability;
- all VRAM addresses are fault-free;
- every display port works;
- every temperature/ambient condition is stable.

Use precise language:

```
no error observed during this test window
```

not:

```
card has no errors
```

---

# Part XIII — Sustained inference is purchase-relevant

Reuse Slice 45 / Experiment 85.

A useful used-card workload test records:
- exact model SHA;
- exact llama-bench/runtime identity;
- repeated TG samples;
- temperature;
- clocks;
- power where available;
- runtime/server errors.

This tests the card in the workload you intend to buy it for.

---

# Part XIV — Thermal acceptance

A hot card is not automatically bad.

Look for:

```
temperature trend
+
clock behavior
+
TG drift
+
limiter/event evidence where available
```

A card that begins fast then loses substantial sustained TG may need:
- cleaning;
- fan/cooler inspection;
- thermal service;
- case-airflow changes;
- or may have another limiter.

Do not diagnose thermal paste from temperature alone.

---

# Part XV — Display-output failure vs compute failure

For a headless inference buyer, a dead HDMI/DP port and a compute-unstable GPU are different defects.

Acceptance depends on use case.

Record separately:
- display outputs tested/working;
- compute workload stable;
- video encode/decode needed/tested;
- physical connector damage.

Do not hide display defects just because compute works.

---

# Part XVI — Physical inspection

Read-only/software evidence cannot see everything.

Inspect when safe/powered off:
- PCB/cooler damage;
- corrosion/liquid residue;
- burnt connectors;
- cracked/missing components;
- fan condition/noise;
- power connector heat damage;
- tamper/warranty seals only as contextual evidence.

Avoid disassembly if it would create warranty/return disputes.

---

# Part XVII — Firmware/VBIOS

Record VBIOS/firmware identity.

A strange VBIOS can justify REVIEW.

But the default course lab does **not** flash firmware.

Firmware flashing can brick hardware and changes evidence state.

If firmware recovery is ever taught, it belongs in a separate high-risk L4 workflow with device-specific safeguards.

---

# Part XVIII — VRAM stress boundary

Dedicated VRAM testers can find faults ordinary inference may miss.

However destructive/aggressive stress tools vary by vendor/platform and can produce thermal/system risk.

The v1 default course acceptance path uses:
- vendor telemetry;
- runtime recognition;
- ordinary sustained inference;
- error/log observation.

A specialized VRAM-diagnostic extension can be added later as a clearly labeled higher-risk lab.

---

# Part XIX — Acceptance categories

Use explicit outcomes:

## ACCEPT
Purchase-critical claims match and no material failure is observed in the defined test window.

## REVIEW
Evidence is incomplete or there is a non-critical discrepancy:
- low current PCIe state at idle;
- unsupported ECC telemetry;
- unknown display output;
- thermal drift that needs re-test/maintenance;
- platform slot limiting width.

## REJECT
Examples:
- major VRAM claim mismatch;
- target runtime cannot use the GPU;
- sustained workload repeatedly crashes;
- uncorrectable hardware error evidence;
- identity materially contradicts purchase claim;
- severe instability under ordinary stock operation.

These are course engineering categories, not legal definitions.

---

# Part XX — Seller-test limitations

A seller video/screenshot is stronger if it includes:
- timestamp/current session;
- identifiers tied to the specific card;
- sustained workload;
- telemetry over time.

But your own acceptance test is stronger because:
- same motherboard/PSU/platform;
- same intended LLM workload;
- same runtime;
- known test boundary.

For shipped cards, return-window timing matters operationally.

---

# Claims to avoid

- “GPU name string proves authenticity”;
- “idle PCIe Gen1 means defective card”;
- “ECC N/A means zero ECC errors”;
- “30 minutes error-free proves permanent reliability”;
- “high temperature alone proves bad thermal paste”;
- “display failure means compute must fail”;
- “compute success means every display port is good”;
- “seller stress screenshot replaces your own workload test”;
- “VBIOS should be flashed first when anything looks strange”.
