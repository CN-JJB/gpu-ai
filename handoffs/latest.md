# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–46 are implemented.
Experiments 01–87 exist.

## Slice 46 core — Used-GPU Validation / Purchase Acceptance

Slice 20 remains the transaction/arrival acceptance workflow.

Slice 46 is the advanced hardware-evidence layer:

```text
seller claim
→ PCI/device/subsystem identity
→ VRAM
→ runtime recognition
→ PCIe capability/current state
→ ECC/RAS/XID/error evidence
→ sustained Local-LLM workload
→ thermal/clock stability
→ ACCEPT / REVIEW / REJECT
```

Synthetic verified:

```text
healthy card
→ ACCEPT

idle PCIe x1 current, x16 max, no under-load check
→ REVIEW

claimed 24 GiB, observed 12 GiB
→ REJECT
```

Important rules:

```text
idle low PCIe state
!= defective GPU

ECC/RAS unsupported
!= zero errors

short clean test
!= lifetime reliability proof
```

Real Experiment 87:
- Linux + Windows read-only inventory;
- raw NVIDIA/AMD vendor evidence where installed;
- PCI identity/link evidence;
- ordinary sustained LLM workload via Experiment 85;
- separate display/physical inspection;
- no VBIOS flash, OC/UV, power/fan changes, error injection or destructive VRAM stress.

## Active next slice — PSU / Power Delivery / Platform Integration

Build for secondhand/multi-GPU systems:

```text
GPU board power
+ CPU/platform/load
→ PSU continuous capacity
→ headroom
→ PCIe slot power
→ auxiliary connector/cable topology
→ transient behavior
→ connector temperature/damage risk
→ multi-GPU aggregate budget
```

Need teach:
- PSU wattage label alone is insufficient;
- board power/TDP/TGP is not identical to wall draw or transient peak;
- PCIe slot and auxiliary connectors are separate paths;
- daisy-chain/pigtail cable suitability depends on PSU/cable/vendor guidance;
- adapters/connectors require exact specification and inspection;
- multi-GPU needs rail/cable/connector/airflow planning, not only total watts.

Real lab should remain non-invasive:
- inventory PSU label/model externally;
- record GPU telemetry under ordinary workload;
- inspect connectors/cables powered off;
- do not open PSU chassis;
- do not probe mains/high-voltage internals;
- do not intentionally overload connectors/PSU.
