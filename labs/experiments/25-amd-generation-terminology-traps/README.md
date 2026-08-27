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