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


## Why this experiment

Vendor Capstone 之前先做 preflight，是为了确认“设备、驱动/runtime、backend 枚举”这条最小路径已经成立。否则直接调性能参数只会把兼容性问题和优化问题混在一起。

## Hypothesis

所选 vendor path 如果真的可用，应能在只读检查里同时得到硬件身份、runtime/driver 身份和 llama.cpp/device enumeration 证据。

## Fixed variables

只选一个 vendor path；不要一边 preflight 一边升级 driver、换 runtime、改模型。

## What to observe

1. exact device identity。
2. driver/runtime version。
3. memory/capability evidence。
4. backend 是否枚举目标 device。
5. 哪一步首次失败。

## Troubleshooting

- preflight fail 时停止性能调参。
- device 能被 OS 看见但 backend 不枚举，优先查 runtime/build/support。
- AMD/Intel 等路径要记录 exact target，不要只写品牌。
- Apple unified memory 是整机共享资源，不要直接当 discrete VRAM。

## Evidence to save

保存完整 preflight-*.txt，保留失败输出，不要只截成功行。

## What this proves

你证明了进入 vendor capstone 的最小环境前提。

## What this does NOT prove

它不证明模型已成功推理、性能达标或质量正确。

## No-hardware path

没有对应 vendor 硬件时，可阅读对应脚本并填写“每条 probe 证明什么”的 worksheet；真机证据留到以后。

## Transfer question

OS 能看到 GPU，但 llama.cpp device list 看不到。下一步应该先调 batch/threads，还是查 build/backend？为什么？
