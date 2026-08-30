# Experiment 37 — Max Sticker Price from Total Budget

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/hardware-decision-gates.svg" alt="最大买入价不是“性能分数换算”，而是在硬门槛通过后把风险、替代方案、TCO 和机会成本一起纳入。">
  <figcaption>最大买入价不是“性能分数换算”，而是在硬门槛通过后把风险、替代方案、TCO 和机会成本一起纳入。</figcaption>
</figure>

## 默认 synthetic scenario

```
total ownership budget = 8000
platform extra         = 400
PSU/cooling            = 350
energy horizon         = 500
repair reserve         = 500
maintenance reserve    = 250
expected resale        = 1200
```

Then:

```
max sticker
= 8000 - 400 - 350 - 500 - 500 - 250 + 1200
= 7200
```

## Candidates

Synthetic:

- A ask 6800, hard gates PASS, evidence strong → BUY-CANDIDATE
- B ask 6500, hard gates PASS, evidence weak → NEEDS EVIDENCE
- C ask 7600, hard gates PASS → WATCH
- D ask 4000, FIT FAIL → SKIP

## Run

```bash
python3 evaluate_watchlist.py
```

All values are synthetic and do not represent real GPUs.

## Why this experiment

“这张卡值多少钱”不是一个脱离个人系统的市场真理。你真正需要的是：在总预算、平台补齐成本、维护风险、电费和未来转售假设下，**自己最多愿意为卡本体付多少**。

## Hypothesis

即使市场 ask 很低，只要 FIT fail，就应该 SKIP；即使 FIT pass，只要证据弱，也只能 NEEDS EVIDENCE。价格不能覆盖技术硬门槛和证据缺口。

## Fixed variables

保持总 ownership budget、各项 reserve、resale 假设和候选技术状态不变，只比较 candidate ask/evidence/fit。

## What to observe

1. 逐项验证 max sticker 算术。
2. 比较“便宜但 FIT FAIL”和“略贵但 FIT PASS”为什么结论不同。
3. 看 evidence strength 如何改变 BUY-CANDIDATE 与 NEEDS EVIDENCE。
4. 理解 resale 只是输入假设，不是保证回收金额。

## Troubleshooting

- 不要把平台成本、PSU、维护 reserve 漏掉后再称“总预算”。
- resale 要和 horizon/condition 假设绑定，不能当现金返还。
- synthetic 7200 不是任何真实 GPU 的市场价格。

## Evidence to save

保存默认输入、输出，并写出你自己的 max-sticker 公式，每一个加减项都解释原因。

## What this proves

你会把“总可承受成本”转成“卡本体最高报价”，并让价格判断受 hard gates 和证据等级约束。

## What this does NOT prove

它不提供当前市场价格，也不产生自动购买建议。

## No-hardware path

完整 L0 实验。

## Transfer question

如果一张卡比 max sticker 便宜 20%，但卖家无法提供 VRAM/身份/稳定性证据，你为什么仍然不应直接 BUY？
