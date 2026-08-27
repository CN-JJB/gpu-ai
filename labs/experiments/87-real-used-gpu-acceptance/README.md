# Experiment 87 — Real Used-GPU Purchase Acceptance Packet

硬件等级：L2。

## Goal

Collect read-only hardware identity/error evidence and combine it with the ordinary sustained Local-LLM workload from Experiment 85.

Default lab does **not**:
- flash VBIOS/firmware;
- overclock/undervolt;
- change power limit/fan curve;
- inject errors;
- run destructive VRAM stress.

## 1. Write seller claim first

Copy:

```bash
cp CLAIM-TEMPLATE.md claim.md
```

Record before interpreting the card:
- exact marketed model;
- promised VRAM;
- promised display/output condition;
- included accessories/adapters;
- any seller test claim.

## 2. Collect hardware identity

### Linux

```bash
./collect-linux.sh evidence-hardware
```

The script stores, when available:
- `lspci -nnk`;
- verbose PCI information;
- `nvidia-smi -L` and `nvidia-smi -q`;
- AMD SMI list/static/PCIe/ECC/bad-page raw output.

It is read-only.

### Windows

```powershell
./collect-windows.ps1 -OutDir evidence-hardware
```

It stores:
- PnP/display-controller identity;
- NVIDIA SMI raw output if installed;
- AMD SMI raw output if installed.

## 3. Check PCIe carefully

Record both:
- max/capability where available;
- current/negotiated state.

If current state is unexpectedly low while idle:

```text
REVIEW
```

then check:
- motherboard slot wiring;
- CPU lanes;
- riser;
- bifurcation;
- representative under-load state.

Do not call the card defective from idle downshift alone.

## 4. Error telemetry

Record exactly what the hardware supports.

If ECC/RAS is unavailable:

```text
N/A / NOT_SUPPORTED
```

not:

```text
0 errors
```

Look for raw evidence such as:
- NVIDIA query/error state and relevant OS/driver logs;
- AMD ECC/RAS/bad pages/PCIe replay/recovery where supported;
- runtime errors during the workload.

## 5. Run intended workload

Reuse Experiment 85 with the exact card/model you are evaluating.

Record:
- model SHA;
- runtime identity;
- repeated TG samples;
- telemetry;
- sustained drift;
- any runtime failure.

This is more purchase-relevant than a random graphics benchmark if your use case is Local LLM.

## 6. Display outputs

Software collection does not prove HDMI/DP works.

If display output matters to your purchase, test each required port separately with known-good:
- cable;
- monitor;
- mode/resolution.

Record results in `RESULT-TEMPLATE.md`.

## 7. Physical inspection

With power off and using ordinary electrical safety:
- inspect connectors;
- fan condition/noise;
- corrosion/liquid residue;
- damaged PCB/cooler/power connector.

Do not disassemble during a return-window test unless you accept warranty/return consequences.

## 8. Decision

Finish with one of:

```text
ACCEPT
REVIEW
REJECT
```

and list the exact evidence supporting the decision.

## 9. Evidence hygiene

Hash the packet using Experiment 61.

Do not publish serials/UUIDs if you consider them private inventory identifiers; redact in the public copy while retaining local originals if needed.
