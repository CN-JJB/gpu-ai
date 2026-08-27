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
