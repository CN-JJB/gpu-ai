# Used GPU Acceptance Checklist

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

- ACCEPT
- ACCEPT WITH DISCLOSED DEFECT
- DISPUTE / RETURN

## Evidence packet

Keep:
- raw command output
- benchmark JSON
- memory-test output
- photos/video
- seller promises
- timestamps
