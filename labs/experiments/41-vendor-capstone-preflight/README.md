# Experiment 41 — Vendor Capstone Preflight

硬件等级：L1/L2

## Goal

Before Experiment 40, prove the selected vendor path is ready.

Choose exactly one script:

```
nvidia-preflight.sh
amd-preflight.sh
apple-preflight.sh
intel-preflight.sh
```

They are read-only/best-effort.

## NVIDIA

```bash
./nvidia-preflight.sh > preflight-nvidia.txt 2>&1
```

PASS evidence should include:
- NVIDIA device;
- driver;
- memory;
- llama.cpp device list.

## AMD

```bash
./amd-preflight.sh > preflight-amd.txt 2>&1
```

Need:
- exact gfx target;
- ROCm/HIP identity;
- llama.cpp device list.

If exact support is community-only, record that before Capstone.

## Apple

```bash
./apple-preflight.sh > preflight-apple.txt 2>&1
```

Need:
- Apple Silicon identity;
- installed unified memory;
- Metal-capable display/device info;
- llama.cpp device list.

For deeper Metal working-set evidence, run Experiment 28.

## Intel

```bash
./intel-preflight.sh > preflight-intel.txt 2>&1
```

Need:
- `sycl-ls`;
- Level Zero GPU if using Intel GPU;
- optional `llama-ls-sycl-device`;
- llama.cpp device list.

## Important

A preflight can legitimately fail.

That means:
```
return to driver/runtime/support investigation
```

not:
```
start changing performance flags
```
