# Experiment 28 — Real Apple Silicon / Metal / MLX Inventory

硬件等级：L1/L2（Apple Silicon Mac；Metal probe 需要 Xcode Command Line Tools）

风险：只读，不修改系统 memory limits。

## 目标

在真实 Mac 上收集：

```
exact chip
→ installed unified memory
→ Metal unified-memory properties
→ recommended GPU working set
→ SIMD-group width
→ threadgroup limit
→ MLX CPU/GPU identity
→ llama.cpp Metal device
```

这样“Mac 有多少可用显存”“Apple SIMD 是多少宽”“MLX/llama.cpp 在跑什么”都不靠猜。

## A. 一键采集

```bash
./collect-apple.sh > apple-inventory.txt 2>&1
```

脚本记录：

- `sw_vers`
- `uname -m`
- `system_profiler SPHardwareDataType SPDisplaysDataType`
- `hw.memsize`
- `vm_stat`
- Metal probe
- optional MLX probe
- optional llama-bench device/build

## B. Metal probe

```bash
xcrun swift metal_inventory.swift
```

输出：

- device name；
- `hasUnifiedMemory`；
- `recommendedMaxWorkingSetSize`；
- `currentAllocatedSize`；
- `maxBufferLength`；
- `threadExecutionWidth`；
- `maxTotalThreadsPerThreadgroup`。

### Why compile a tiny kernel?

`threadExecutionWidth` belongs to the compute pipeline state, not merely to the marketing chip name.

The probe compiles a no-op Metal compute kernel and queries the resulting pipeline.

This is the correct runtime Evidence.

## C. MLX probe

If MLX is installed:

```bash
python3 mlx_probe.py
```

Current MLX API records:
- MLX version if exposed;
- default device;
- CPU device info;
- GPU device info;
- device counts.

It does **not** claim Neural Engine use.

## D. llama.cpp

If `llama-bench` is available:

```bash
llama-bench --version
llama-bench --list-devices
```

For a real performance run, use the existing course Experiment 10 / llama-bench workflow and record:

- exact llama.cpp commit/build；
- Metal device；
- exact GGUF + SHA256；
- PP；
- TG；
- context/KV；
- thermal/power mode。

## E. What to compare across Macs

Use the same model/config and record:

| Mac | unified memory | recommended working set | chip tier | PP | TG |
|---|---:|---:|---|---:|---:|
| | | | | | |

Then add official memory bandwidth from Apple product documentation.

Do not infer bandwidth from `recommendedMaxWorkingSetSize`; they are different properties.

## F. Important M5 check

On M5/A19-era hardware, current Metal 4 tensor support is a rapidly changing backend area.

Save:
- exact macOS；
- Xcode/Metal compiler；
- llama.cpp commit；
- initialization log；
- tensor-path status if runtime reports it。

Do not assume a hardware Neural Accelerator is active just because the chip is M5.

## G. Result

Fill `RESULT-TEMPLATE.md` and preserve raw `apple-inventory.txt`.
