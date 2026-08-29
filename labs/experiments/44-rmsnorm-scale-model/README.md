# Experiment 44 — RMSNorm Scale / Mean Model

硬件等级：L0

## Goal

Verify two facts:

1. RMSNorm is approximately invariant to positive global re-scaling.
2. RMSNorm does not force output mean to zero.

Default vector:

```
x = [1, -2, 3, -4]
```

Compare:

```
x
3x
```

using unit gain and epsilon = 1e-6.

## Run

```bash
python3 simulate.py
```

The script also computes a simple LayerNorm-style normalized vector for contrast.

## Expected concept

RMSNorm outputs for x and 3x should be nearly identical.

But RMSNorm output mean should not be forced to zero.

LayerNorm-style output mean should be near zero.


## Why this experiment

RMSNorm 常被一句“类似 LayerNorm”带过，但两者最关键的区别正是本实验要让你亲手看到：RMSNorm 用均方根做尺度归一化，并不强制减去均值。

## Hypothesis

把输入整体乘一个正数后，RMSNorm 输出应该近似不变；但输出均值不必接近 0。LayerNorm-style 对比则应显示去均值效果。

## Fixed variables

只改变输入的全局 scale。epsilon、gain、向量方向都保持不变。

## What to observe

1. 比较 RMSNorm(x) 和 RMSNorm(3x) 的逐元素差异。
2. 记录 RMSNorm 输出均值。
3. 对比 LayerNorm-style 输出均值。
4. 解释为什么 epsilon 使“完全尺度不变”只是近似说法。

## Troubleshooting

- 如果 3x 输出差异很大，先确认公式是不是 x / sqrt(mean(x^2)+eps)。
- 不要把 mean(x^2) 写成 mean(x)^2。
- 不要把 LayerNorm 的 x-mean(x) 偷塞进 RMSNorm。

## Evidence to save

保存脚本输出，并用一句话完成：RMSNorm normalizes ______ but does not force ______。

## What this proves

你能从公式和数值结果解释 RMSNorm 的尺度行为，以及它与 LayerNorm 的一个核心差异。

## What this does NOT prove

这个 toy 不证明任何具体模型使用 RMSNorm 后更快、更稳定或质量更好。

## No-hardware path

完整 L0 实验，不需要 GPU。

## Transfer question

如果把输入从 x 改成 -3x，你预期 RMSNorm 输出与 RMSNorm(x) 有什么关系？为什么？
