# Evidence — Experiment 46: Used-GPU Validation / Purchase Acceptance

状态：advanced used-GPU hardware-evidence slice complete; L0 ACCEPT/REVIEW/REJECT cases verified; real read-only acceptance packet ready.

## Relationship to Slice 20

Slice 20 remains the transaction-oriented workflow:

```text
seller evidence
→ arrival/unboxing
→ baseline acceptance
→ ACCEPT / DISCLOSED DEFECT / DISPUTE
```

Slice 46 is the stricter hardware-evidence extension:

```text
identity consistency
→ PCIe capability/current state
→ ECC/RAS/XID/error evidence
→ sustained Local-LLM workload
→ ACCEPT / REVIEW / REJECT
```

The two are linked rather than competing standards.

## Core claim

> A used GPU should not be accepted or rejected from one product-name string, one idle PCIe state, or one short stress screenshot. Purchase-critical claims must be checked against independent identity, capacity, link/error and sustained workload evidence.

## Dynamic NVIDIA evidence

Current NVIDIA GPU Debug Guidelines recommend checking categories including:
- GPU count;
- PCIe link speed;
- VBIOS;
- recent XID errors;
- CUDA workloads.

Official:
https://docs.nvidia.com/deploy/pdf/GPU_Debug_Guidelines.pdf

Current NVIDIA management APIs expose PCIe concepts including current/max generation and width plus replay/throughput information on supported physical devices.

The course collector stores raw `nvidia-smi -L`, `nvidia-smi -q` and PCI evidence instead of assuming every query field exists on every product/driver.

## Dynamic AMD evidence

Current AMD SMI documentation exposes:

```text
amd-smi list
amd-smi static
amd-smi metric --pcie
amd-smi metric --ecc
amd-smi bad-pages
```

where supported.

Current PCIe metric families include:
- current speed;
- current width;
- replay count;
- newer recovery/NAK counters on supported ASICs.

Current static information can include ASIC, bus, VBIOS/IFWI, driver, VRAM and board data.

AMD documentation also distinguishes device-type ID from per-card identity; BDF/UUID should be used when distinguishing a specific card.

Official:
https://rocm.docs.amd.com/projects/amdsmi/en/latest/how-to/amdsmi-cli-tool.html
https://rocm.docs.amd.com/projects/amdsmi/en/latest/reference/amdsmi-py-api.html

## Experiment 86 verification

### Healthy synthetic card

```text
claimed VRAM = 24 GiB
observed VRAM = 24 GiB
runtime recognized = yes
PCIe x16 current/max under load
uncorrectable = 0
TG 50 → 49 tok/s
```

Verified:

```text
DECISION: ACCEPT
```

### Idle PCIe downshift

```text
max width = x16
current width = x1
observation = idle
runtime/workload otherwise healthy
uncorrectable telemetry = UNKNOWN
```

Verified:

```text
DECISION: REVIEW
```

not REJECT.

This prevents the false rule:

```text
idle PCIe x1
=
bad GPU
```

Platform power management, slot wiring, CPU lanes, risers and bifurcation remain possible explanations.

### VRAM mismatch

```text
seller claim = 24 GiB
observed = 12 GiB
```

Verified:

```text
DECISION: REJECT
```

because VRAM capacity is a purchase-critical Local-LLM claim.

## Error semantics

The course explicitly distinguishes:

```text
ECC/RAS unsupported
!=
0 errors
```

Unsupported fields are recorded as:

```text
N/A / NOT_SUPPORTED / UNKNOWN
```

Rejection-level evidence can include, when applicable:
- observed uncorrectable error counters;
- repeated runtime/device-loss/reset failures;
- sustained stock-workload crashes;
- material identity/VRAM contradiction.

A short error-free window is described only as:

```text
no error observed in this test window
```

not lifetime reliability proof.

## Experiment 87

The real packet collects read-only:

### Linux
- `lspci -nnk`;
- `lspci -vv`;
- `nvidia-smi -L/-q/topo` when available;
- AMD SMI identity/PCIe/ECC/bad-page raw output when available;
- filtered kernel GPU/PCIe error context where permission allows.

### Windows
- Win32 video-controller/PnP identity;
- NVIDIA SMI raw output when installed;
- AMD SMI raw output when installed.

Then it reuses Experiment 85 for:
- repeated TG;
- temperatures;
- clocks;
- sustained drift;
- runtime stability.

## Safety boundary

Default lab performs none of:
- VBIOS/firmware flash;
- overclock/undervolt;
- power/fan changes;
- PCIe error injection;
- destructive VRAM stress.

Display-port and physical inspection are separate evidence dimensions.

## Learner should reject

- GPU name string proves authenticity;
- idle low PCIe state proves card failure;
- ECC N/A means zero errors;
- one short clean test proves permanent reliability;
- high temperature alone proves bad thermal paste;
- compute success proves every display port works;
- seller benchmark screenshot replaces buyer-side Local-LLM validation.
