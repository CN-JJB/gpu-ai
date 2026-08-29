# Experiment 58 — Cross-Entropy / Perplexity Toy Model

硬件等级：L0

## Goal

Compute quality metrics from correct-next-token probabilities without ML libraries.

Default:

Baseline:
```
[0.5, 0.25, 0.125, 0.5]
```

Candidate:
```
[0.48, 0.22, 0.10, 0.45]
```

## Run

```bash
python3 ppl.py
```

## Expected

Baseline:
```
CE ≈ 1.213007566
PPL ≈ 3.363585661
```

Candidate:
```
CE ≈ 1.337297424
PPL ≈ 3.808736185
```

```
PPL ratio ≈ 1.132344
ΔCE ≈ 0.124290
```

The candidate is worse on this synthetic token stream.

## Try

Change only one probability to 0.001.

Observe how strongly a confidently bad prediction affects NLL.


## Why this experiment

Perplexity 很容易被当成神秘 benchmark。本实验先去掉模型、tokenizer、框架，只保留最核心数学：正确 next-token 概率越低，negative log-likelihood 越大，PPL 越差。

## Hypothesis

只把一个正确 token 的概率压得非常低，就会显著拉高平均 NLL；这说明 PPL 对“自信地预测错”很敏感。

## Fixed variables

token 数和其他位置概率保持不变；Try 阶段只改一个位置。

## What to observe

1. 手算一个位置的 -ln(p)。
2. 检查 CE 是否等于这些 NLL 的平均。
3. 检查 PPL = exp(CE)。
4. 把一个概率改成 0.001，观察它对整体的非线性影响。

## Troubleshooting

- 确认使用 natural log；若换 log base，公式定义必须一起变。
- 概率必须在 (0,1]。
- 比较真实模型时，tokenizer、corpus、tokenization 和 evaluation protocol 必须一致，否则 PPL 不可直接比。

## Evidence to save

保存 baseline/candidate 输出，并写出一条完整计算链：p → -ln(p) → CE → PPL。

## What this proves

你理解 PPL 的数学来源，并知道“PPL 更低”只在同一评价协议下才可比较。

## What this does NOT prove

这个 toy 不证明任何实际模型的语言质量，也不代表真实 corpus。

## No-hardware path

完整 L0 实验。

## Transfer question

两个模型分别使用不同 tokenizer 得到 PPL 5.8 和 6.1，你为什么不能立刻宣布 5.8 的模型更好？
