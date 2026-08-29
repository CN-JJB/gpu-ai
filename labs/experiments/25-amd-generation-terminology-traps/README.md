# Experiment 25 — AMD Architecture Lineage / Terminology Traps

硬件等级：L0

## 目标

AMD 架构最常见的错误不是记错产品名，而是把：

```
GCN
RDNA
CDNA
CU
WGP
Wave32
Wave64
MFMA
Infinity Cache
```

机械翻译成 NVIDIA 术语。

这个实验用 assertions 检查你是否真正分清这些概念。

## 运行

```bash
python3 check_lineage.py
```

仓库自带 `student_answers.json` 是已验证参考答案。

## Stable assertions

你要能判断：

- classic GCN primary wave size = 64；
- RDNA supports only Wave32 → false；
- WGP contains/organizes two closely coupled CUs in the RDNA mental model；
- Infinity Cache is extra VRAM → false；
- RDNA and CDNA are one sequential line → false；
- CDNA MFMA is matrix acceleration；
- RDNA3 dual issue guarantees 2× → false；
- MI300A and MI300X package architecture are identical → false；
- RDNA4 FP8/INT4 means every Q4 LLM uses native path → false。

## Dynamic assertions

还会检查当前 2026 snapshot：

- CDNA5 currently introduces WGP/Wave32；
- current ROCm 7.14 standard support matrix is not a blanket "all AMD GPUs" list；
- exact gfx target + OS/SKU matters。

## 完成标准

1. reference answers 12/12；
2. 把答案复制后故意改错至少三条；
3. 对每条 false claim 写一句“还缺哪层 Evidence”。

## Why this experiment

AMD 架构跨 GCN、RDNA、CDNA 后，最容易犯的是把不同层级术语强行翻译成 NVIDIA 一对一对应。这个实验训练你把 execution grouping、compute unit、matrix path、cache 和产品线分开。

## Hypothesis

每条 false assertion 都应该能指出错在：代际、层级、产品线、或“硬件能力 ≠ 当前 runtime 使用”之一，而不是只背答案。

## Fixed variables

Stable assertions 不随当前市场变化；Dynamic assertions 必须绑定课程记录的 2026 snapshot，未来更新时重新核验来源。

## What to observe

1. GCN/RDNA wave size 的代际差异。
2. WGP 与 CU 的层级关系。
3. RDNA 与 CDNA 为什么不是一条简单顺序线。
4. MFMA/低精度硬件能力与 backend kernel 使用的区别。
5. ROCm support 为什么要落到 exact gfx target + OS/SKU。

## Troubleshooting

- Infinity Cache 不是额外 VRAM。
- dual issue 不等于所有 workload 2×。
- matrix dtype support 不等于任意 Q4 GGUF 自动走 native path。
- dynamic support matrix 结论必须随时间更新。

## Evidence to save

保存 12/12 输出，并为所有 false assertion 写“错误层级 + 需要的 Evidence”。

## What this proves

你能避免 AMD↔NVIDIA 的机械术语映射。

## What this does NOT prove

它不证明当前某张 AMD 卡的真实 ROCm/LLM 性能。

## No-hardware path

完整 L0。

## Transfer question

一张 RDNA4 GPU 支持某种低精度矩阵能力，但 llama.cpp 当前 backend 未调用它，你应该把哪一条写成稳定事实，哪一条写成动态兼容性事实？
