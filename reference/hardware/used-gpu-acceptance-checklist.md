# Used GPU Acceptance Checklist

<figure>
  <img src="../../assets/diagrams/used-gpu-acceptance-flow.svg" alt="Used GPU Acceptance Checklist 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Used GPU Acceptance Checklist 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## Before payment

Save:
- listing;
- exact model/VRAM;
- price;
- seller claims;
- serial/board photos;
- current test video;
- return/inspection terms.

Ask:
- repair?
- VRAM/core replacement?
- BIOS mod?
- VRAM mod?
- mining/server/workstation history?
- cooler/fan/pad work?

## Arrival — do not disassemble first

Record:
- sealed parcel;
- shipping label;
- unboxing;
- serial;
- board exterior;
- connectors;
- fan/cooler;
- obvious corrosion/repair.

## Test sequence

### 1. Identity
- vendor tool
- lspci
- exact VRAM
- BIOS/firmware if relevant

### 2. Baseline health
- driver errors
- ECC/RAS if supported
- PCIe link
- idle temperature

### 3. Memory
Choose supported tool:
- official DCGM memory diagnostics on supported NVIDIA products
- vendor RAS/error counters
- optional memtest_vulkan cross-vendor

Any reproducible error = serious warning.

### 4. Workload
Run:
- llama-bench PP
- llama-bench TG
- repeated runs
- raw JSON

### 5. Thermals
Record:
- core
- hotspot
- memory junction if exposed
- fan
- clocks
- power
- throttling

### 6. Error log
Check:
- GPU reset
- device lost
- XID
- RAS/ECC
- PCIe error

## Stop immediately

- smoke/smell/arcing
- unsafe connector/PCB
- fan failure + rising temp
- memory errors
- artifacting
- repeated reset
- uncorrectable ECC
- thermal shutdown

## Decision

Transaction-oriented outcome from Slice 20:
- ACCEPT
- ACCEPT WITH DISCLOSED DEFECT
- DISPUTE / RETURN

For the stricter hardware-evidence layer, continue to Slice 46:

```text
reference/gpu/used-gpu-purchase-acceptance.md
labs/experiments/87-real-used-gpu-acceptance/
```

Slice 46 uses technical evidence states:
- ACCEPT — purchase-critical claims match and defined tests pass;
- REVIEW — incomplete/non-critical discrepancy or platform-limited evidence;
- REJECT — material identity/VRAM/runtime/error/stability failure.

These are not competing standards. Slice 20 answers the transaction/return workflow; Slice 46 deepens hardware identity, PCIe capability-vs-current state, ECC/RAS/XID-style evidence and sustained Local-LLM validation.

A technical REJECT can support a dispute/return decision, but transaction/legal outcomes remain separate.

## Evidence packet

Keep:
- raw command output
- benchmark JSON
- memory-test output
- photos/video
- seller promises
- timestamps
