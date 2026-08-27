# Dynamic Intelligence — Used-GPU Validation — 2026-08-27

动态内容，不作为永久稳定命令语义。

## NVIDIA

Current official evidence used:

### NVIDIA GPU Debug Guidelines
https://docs.nvidia.com/deploy/pdf/GPU_Debug_Guidelines.pdf

Current guidance includes checking items such as:
- GPU count;
- PCIe link speed;
- VBIOS;
- recent XID errors;
- CUDA workloads.

### NVIDIA management concepts
Current NVML/vGPU management documentation exposes PCIe concepts including:
- max/current generation;
- max/current link width;
- replay counter;
- TX/RX throughput;

Support differs by physical GPU / vGPU / driver.

Course default collection therefore prefers raw:

```bash
nvidia-smi -L
nvidia-smi -q
lspci -nnk
lspci -vv
```

rather than assuming every query field is available.

## AMD

Current AMD SMI CLI documentation:
https://rocm.docs.amd.com/projects/amdsmi/en/latest/how-to/amdsmi-cli-tool.html

Current command families include:

```bash
amd-smi list
amd-smi static
amd-smi metric
amd-smi bad-pages
```

Current `amd-smi static` can expose categories including:
- ASIC;
- bus;
- VBIOS/IFWI;
- driver;
- VRAM;
- board.

Current `amd-smi metric --pcie` can expose, where supported:
- current PCIe speed;
- width;
- replay count;
- newer recovery/NAK counters on supported ASICs.

Current metric CLI also exposes ECC totals/blocks where supported.

AMD SMI API docs distinguish:
- device-type ID — shared by same SKU;
- BDF/UUID — suitable for a specific card identity.

## Linux PCI evidence

`lspci -nnk` provides numeric PCI vendor/device/subsystem identity and driver binding.

`lspci -vv -s BDF` commonly exposes `LnkCap` / `LnkSta` style capability/current link information when available.

OS/tool output can vary.

## Important dynamic caveats

- Current PCIe state can downshift at idle.
- Vendor error/ECC telemetry is hardware/driver dependent.
- Consumer cards may report ECC/RAS as unsupported.
- Current command output should be captured raw in Evidence.
- Installed `--help` and current vendor documentation remain authoritative.
