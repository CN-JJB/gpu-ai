# GPU Thermal / Clock Telemetry Snapshot — 2026-08-27

This file records dynamic vendor/tool facts.

## NVIDIA

Official current references:
- https://docs.nvidia.com/deploy/nvidia-smi/index.html
- https://docs.nvidia.com/deploy/nvml-api/group__nvmlClocksEventReasons.html

Current concepts exposed include:
- GPU temperature;
- supported memory temperature;
- power readings;
- current/performance clocks;
- performance state;
- clock-event reasons.

Clock-event reason families currently include concepts such as:
- software power cap;
- software thermal slowdown;
- hardware thermal slowdown;
- hardware power brake;
- sync/other clock limitations.

Exact field names/support vary by GPU and driver.

## AMD

Official current references:
- https://rocm.docs.amd.com/projects/amdsmi/en/latest/how-to/amdsmi-cli-tool.html
- https://rocm.docs.amd.com/projects/amdsmi/en/latest/doxygen/docBin/html/group__tagGPUMonitor.html

Current AMD SMI concepts include:
- edge/hotspot/memory temperature where supported;
- GFX/memory clocks;
- GPU/memory activity;
- power;
- VRAM usage.

Current CLI documentation includes `amd-smi monitor` and watch-mode examples.

## Course rule

Before a real lab:

```
nvidia-smi --help
amd-smi --help
```

or the installed tool's equivalent remains authoritative.

Do not turn this snapshot into a permanent CLI contract.
