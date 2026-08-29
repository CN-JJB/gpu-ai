# Experiment 35 — Seller Evidence Quality

硬件等级：L0

## 目标

卖家说得很多，不等于 Evidence 很强。

本实验训练：

```
seller response
→ C0/C1/C2/C3/C4
```

## Condition evidence scale

### C0
没有可用状态证据。

### C1
卖家口述/旧截图。

### C2
当前功能证据：
- 当前识别；
- 当前负载；
- 基本温度/画面。

### C3
强售前证据：
- exact serial/board；
- current identity；
- VRAM；
- sustained load；
- memory test；
- thermals/error state。

### C4
第三方或买家本人独立验证。

## 运行

```bash
python3 check_evidence.py
```

## 思考

“验货宝通过”是否必然是 C4 的完整 GPU 健康证明？

不是。

它可以提高某些交易属性的独立证据强度，但是否覆盖显存/持续 LLM/温度，仍取决于具体查验范围。

所以 C4 在本课程里指：

```
target acceptance properties
were independently verified
```

而不是只看一个平台标签。

## Why this experiment

买二手 GPU 时，卖家“说得很详细”与“证据足够强”是两回事。这个实验把售前状态证据按强度分级，让你知道什么时候应该继续问、什么时候仍然不能 ACCEPT。

## Hypothesis

同一句“显卡正常”，若只有口述属于低等级；如果有当前身份、VRAM、持续负载、温度/error state，证据等级才会上升。第三方标签也只有在覆盖目标验收属性时才有高价值。

## Fixed variables

使用同一套 C0–C4 定义，不因为你“很想买”而提高等级。

## What to observe

1. C1 与 C2 的差别是“当前可验证功能证据”。
2. C3 为什么要求多个与目标用途直接相关的字段。
3. C4 的关键是独立验证目标属性，而不是平台名。
4. evidence strength 与 technical health 是两条轴。

## Troubleshooting

- 旧截图不能当当前状态。
- 单张 GPU-Z 截图不能证明 sustained stability。
- “验货服务通过”要看具体覆盖范围。
- 缺失项写 UNKNOWN，不用乐观补齐。

## Evidence to save

保存 check_evidence.py 输出，并给一个自拟卖家回复打等级，逐条解释依据。

## What this proves

你能把 seller claim 与 condition evidence strength 分开。

## What this does NOT prove

C3/C4 也不保证硬件永远可靠；它只是提高当前购买决策的证据质量。

## No-hardware path

完整 L0。

## Transfer question

卖家给出今天的型号/VRAM截图和 30 秒负载截图，但没有持续稳定性或 error state，你会给到什么等级，为什么？
