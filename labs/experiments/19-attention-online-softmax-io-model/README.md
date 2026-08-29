# Experiment 19 — Online Softmax + Attention Materialization Model

硬件等级：L0

依赖：Python 3 标准库，不需要 NumPy/GPU。

## Part A — 验证 tiled online attention 的数学结果

脚本同时实现：

1. naive full attention；
2. 按 K/V block 处理的 online-softmax attention。

它会输出最大绝对误差。

运行：

```bash
python3 simulate.py
```

默认使用小型 deterministic Q/K/V。

预期：

```
max_abs_error
```

只来自普通 floating-point 舍入，应该非常小。

这证明：

```
分块
!=
近似 attention
```

只要 online normalization / accumulator 更新正确，最终仍是同一个 exact attention 公式。

## Part B — 看 N×N materialization 膨胀

脚本还会打印：

```
one N×N matrix
two N×N matrices
two matrices × heads
```

默认：
- fp16-like = 2 bytes/value；
- 32 heads；
- N = 1024, 2048, 4096, 8192, 16384。

这些只是“naive materialized intermediate”概念模型，不是任何 runtime 的真实峰值显存。

## 可以玩的参数

```bash
python3 simulate.py --seq 512 1024 2048 4096 --heads 8 --bytes-per-value 2
```

## 思考题

1. N 翻倍时 N×N intermediate 变几倍？
2. 为什么 FlashAttention 仍然有 N² compute，但峰值 intermediate memory 可以不按 N² materialize？
3. 为什么“多做一点 exp / rescale”可能比“写 HBM 再读回来”快？
4. block size 太小/太大分别可能遇到什么 GPU 问题？


## Why this experiment

FlashAttention/IO-aware attention 最关键的思想是：不需要把完整 N×N score/probability 中间矩阵反复写回高成本显存。这个实验同时验证数学等价性和 materialization 成本。

## Hypothesis

正确的 online-softmax 分块实现应与 naive full attention 给出几乎相同结果；而 naive N×N intermediate 的存储会随 N² 增长。

## Fixed variables

Q/K/V 数值、dtype proxy 和 heads 固定；先只改变 sequence length，再单独改变 block/heads。

## What to observe

1. max_abs_error 是否只剩 floating-point 误差量级。
2. N 翻倍时 N² matrix bytes 变 4×。
3. heads 如何进一步放大 naive materialization。
4. 为什么“不 materialize”不等于“不做 N² attention compute”。
5. block size 的片上容量/并行度 tradeoff。

## Troubleshooting

- online softmax 需要正确更新 running max 与 normalization accumulator。
- materialized bytes 只是概念上限模型，不是 runtime peak VRAM。
- 分块不是近似的同义词。
- 小 block/大 block 都可能在真实 GPU 上有资源利用问题。

## Evidence to save

保存默认误差与 N-size 表，再用另一组 seq/head 参数运行一次。

## What this proves

你理解 exact tiled attention 与 IO reduction 的核心机制。

## What this does NOT prove

它不 benchmark FlashAttention，也不模拟真实 HBM/shared-memory traffic。

## No-hardware path

完整 L0。

## Transfer question

为什么一个算法 FLOPs 仍是 O(N²)，却可能因为少写中间矩阵而在 GPU 上快很多？
