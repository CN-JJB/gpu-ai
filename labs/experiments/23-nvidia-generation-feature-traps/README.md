# Experiment 23 — NVIDIA Generation Feature-Lineage Traps

硬件等级：L0

## 问题

架构学习最容易出现的错误不是“年份记错”，而是：

```
architecture family
→ 被误当成
every SKU has the same feature
```

这个实验不模拟真实性能，而是把代际知识做成可验证 assertions。

## 运行

```bash
python3 check_lineage.py
```

脚本验证两类东西：

### A. First-introduction lineage

例如：
- unified programmable CUDA-era foundation → Tesla/G80
- compute L2 cache hierarchy → Fermi
- warp shuffle → Kepler
- SMM scheduler partitioning → Maxwell
- page-faulting Unified Memory → Pascal
- Tensor Core → Volta
- Independent Thread Scheduling → Volta
- async global→shared pipeline → Ampere
- TMA / block cluster → Hopper
- FP4 Tensor path in RTX Blackwell → Blackwell

### B. Variant traps

例如：
- “all Pascal has HBM2” → false
- “all Pascal has GP100-class FP16” → false
- “all Ampere has same FP32 SM” → false
- “Hopper is simply the GeForce successor to Ampere” → false
- “all Blackwell is dual-die” → false
- “Q4 GGUF on Blackwell automatically means native FP4” → false

## 为什么这是实验而不是背答案

你要做的是修改 `student_answers.json` 中的答案，然后让脚本自动判断。

它训练的是：

```
claim
→ architecture family?
→ exact variant?
→ workload/kernel?
→ stable or dynamic?
```

而不是型号记忆。

## 完成标准

- 所有 stable lineage 题正确；
- 所有 variant trap 都能解释为什么错；
- 能自己再添加至少一条“同名架构不同能力”的 assertion。