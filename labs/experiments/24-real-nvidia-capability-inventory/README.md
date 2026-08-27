# Experiment 24 — Real NVIDIA Capability / Architecture Inventory

硬件等级：L1/L2（任意可被 NVIDIA driver 识别的 GPU）

风险：只读。

## 目标

把“我这张卡是什么架构”从型号印象变成 Evidence：

```
exact GPU name
→ compute capability
→ driver
→ memory
→ PCIe/topology
→ current software-support boundary
```

## A. 采集

```bash
./collect-nvidia.sh > nvidia-inventory.txt 2>&1
```

当前 NVIDIA Programming Guide 官方推荐可直接查询：

```bash
nvidia-smi --query-gpu=name,compute_cap
```

脚本还会保存：
- driver/version；
- memory；
- PCI bus；
- topology；
- full `nvidia-smi -q`；
- optional PyTorch capability/build。

## B. Architecture mapping

运行：

```bash
python3 identify_arch.py
```

脚本调用：

```
nvidia-smi --query-gpu=name,compute_cap
```

然后把 compute capability 映射到当前 architecture family。

## C. 为什么 compute capability 比“RTX 30/40/50”更干净

CUDA software targets architecture capability, not marketing series name.

Examples:
- 7.5 → Turing；
- 8.0 / 8.6 → Ampere variants；
- 8.9 → Ada；
- 9.0 → Hopper；
- 10.x / 12.x → current Blackwell families。

映射表属于动态 intelligence；新架构出现后必须更新。

## D. 接下来检查什么

拿到 architecture 后不要停止。继续问：

1. exact VRAM?
2. memory bandwidth/spec source?
3. Tensor/low-precision support?
4. current CUDA toolkit support?
5. target llama.cpp/PyTorch/TensorRT backend support?
6. PP/TG real benchmark?

## E. 特别是旧卡

如果是 Maxwell/Pascal/Volta：
- 不要只看到“CUDA still runs”就认为能使用最新 Toolkit；
- 对照 `intelligence/gpu/nvidia-generation-support-2026-08-27.md`。

如果是 Kepler/Fermi：
- modern CUDA software-stack compatibility is much more constrained；
- treat them as legacy/educational unless exact older stack is intentionally maintained.

## 结果

填写 `RESULT-TEMPLATE.md`，保留原始 `nvidia-inventory.txt`。