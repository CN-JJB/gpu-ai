# Experiment 29 — Intel Xe Terminology / Backend Traps

硬件等级：L0

## 目标

检查是否分清：

- EU / Vector Engine / Xe-Core；
- XMX；
- SLM；
- subgroup；
- SYCL；
- Level Zero；
- oneAPI；
- Arc A/B generations。

## 运行

```bash
python3 check_lineage.py
```

参考答案应 10/10。

## Assertions

你需要判断：

1. EU can be compared 1:1 with CUDA cores → false
2. Xe-Core and Vector Engine are the same level → false
3. XMX is matrix acceleration → true
4. Xe-LP Iris Xe has the same Arc-class XMX path → false
5. Alchemist is Xe-HPG → true
6. Battlemage is Xe2 → true
7. Intel subgroup is always 32 → false
8. SLM is extra VRAM → false
9. Level Zero is a hardware architecture → false
10. XMX availability guarantees any Q4 GGUF uses XMX → false

## 完成标准

除了 10/10，还要解释每个 false claim 缺少哪层 Evidence。

## Why this experiment

跨厂商学习最危险的是做“名词一一对应”：EU=CUDA core、Xe-Core=SM、subgroup=warp。Intel 的术语层级和代际会变化，这个实验训练你先找抽象层，再找对应关系。

## Hypothesis

10 个 assertion 中的 false claim 都应该能指出“错在层级、代际、软件栈或实际 kernel 使用”中的哪一类，而不仅是背 false。

## Fixed variables

不要修改题目；参考 Intel 架构/oneAPI 文档解释每一题的证据层级。

## What to observe

把术语按四层整理：
- hardware execution：Vector Engine / Xe-Core / XMX / SLM；
- execution grouping：subgroup；
- low-level runtime/API：Level Zero；
- programming ecosystem：SYCL / oneAPI。

## Troubleshooting

- 不要把营销代际名和架构名混为一谈。
- subgroup size 不是跨设备永远固定值。
- XMX 存在只说明硬件能力，不证明某个 GGUF/kernel 真会调用。
- SLM 是片上共享局部存储概念，不是额外显存。

## Evidence to save

保存 10/10 输出，并给每个 false assertion 写一句“缺少/混淆的 Evidence 层”。

## What this proves

你能避免 Intel↔NVIDIA 的机械名词映射，并区分硬件、runtime、编程模型和 backend 使用证据。

## What this does NOT prove

它不证明任何 Arc GPU 的当前 llama.cpp/oneAPI 性能或支持状态。

## No-hardware path

完整 L0。

## Transfer question

一张 Arc 卡有 XMX，但你的 runtime log 显示走普通 vector path；你应该把“有 XMX”写成硬件能力还是当前加速证据？
