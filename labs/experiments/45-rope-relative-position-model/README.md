# Experiment 45 — RoPE Relative-Position Geometry

硬件等级：L0

## Goal

Verify:

1. rotation preserves vector norm;
2. base RoPE dot product depends on relative position;
3. shifting both positions by the same offset preserves the idealized RoPE dot product.

Toy dimension:
```
d = 4
```

Pairs use standard-style inverse frequencies:

```
omega_i = base^(-2i/d)
```

Default:
```
base = 10000
q = [1, 0, 1, 0]
k = [0.6, 0.8, 0.3, -0.4]
q position = 3
k position = 7
shared shift = 11
```

## Run

```bash
python3 simulate.py
```

## Expected concept

```
dot(R(3)q, R(7)k)
≈
dot(R(14)q, R(18)k)
```

because both pairs have relative offset 4.

Changing only one position should change the dot product.

## Scope

This demonstrates base RoPE geometry only.

It is not a claim that:
- whole model output is shift invariant;
- every model uses the same base/scaling;
- every runtime stores K internally in the same representation.


## Why this experiment

RoPE 常被背成“给 token 加位置”。这个 toy 用二维旋转几何让你真正看到：它把位置写进 Q/K 的相位，而 dot product 会保留相对位置信息。

## Hypothesis

同一向量旋转后范数保持不变；同时平移 q/k 的位置，理想化 dot product 近似保持，因为相对 offset 不变；只改一边位置则 dot product 改变。

## Fixed variables

q、k、base、dimension 不变，只改变 position/共享 shift。

## What to observe

1. 旋转前后向量 norm。
2. offset=4 的两组位置 pair dot product。
3. 只移动 q 或 k 时 dot product 的变化。
4. 不同 frequency pair 如何对应不同旋转速度。

## Troubleshooting

- 不要把 whole-model shift invariance 当成结论。
- 不同模型可能使用不同 RoPE base/scaling/NTK/YARN 等扩展。
- 真实 runtime 的 KV 表示和 scaling 需要查具体实现。

## Evidence to save

保存 simulate.py 输出，并手算至少一对二维旋转的 norm。

## What this proves

你理解 base RoPE 的相对位置几何。

## What this does NOT prove

它不证明长上下文扩展质量，也不代表所有现代 RoPE 变体。

## No-hardware path

完整 L0。

## Transfer question

为什么“共享平移不改相对 offset”不能自动推出模型整体输出完全不变？
