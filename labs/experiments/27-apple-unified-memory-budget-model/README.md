# Experiment 27 — Apple Unified-Memory Capacity + Bandwidth Roof Model

硬件等级：L0

## 目标

验证两个最重要的 Apple Silicon 判断：

1. **统一内存容量可以被 GPU 访问，但不能把 installed RAM 全部当成免费 VRAM。**
2. **Unified Memory 消除了离散 VRAM copy boundary，却没有消除 memory-bandwidth roof。**

## 默认 synthetic machine

```
Unified memory       = 32 GiB
OS/apps reserve      = 6 GiB
Safety headroom      = 3 GiB

Model weights        = 18 GiB
KV cache             = 2 GiB
Workspace/runtime    = 1 GiB

Memory bandwidth     = 200 GiB/s
Other system traffic = 40 GiB/s

Comparison dGPU VRAM = 16 GiB
```

这些数字都是教学参数，不代表任何 M-series SKU。

## Part A — Capacity

```
safe workload budget
= unified memory
- OS/apps reserve
- safety headroom
```

```
runtime footprint
= weights + KV + workspace
```

默认：

```
safe budget = 23 GiB
runtime     = 21 GiB
→ fits with 2 GiB margin
```

如果把同样 21 GiB runtime footprint 放进一张 16 GiB 独显：

```
full-GPU-resident fit = false
```

这说明 unified memory 能解决某些“独显 VRAM 太小”的容量问题。

它不说明：
- 32 GiB 全部能给模型；
- Apple 一定更快；
- 离散 GPU 不能 CPU offload。

## Part B — Decode bandwidth roof

极简 memory-bound decode：

```
ideal tokens/s
≈ bandwidth available to model
 / weight bytes streamed per token
```

默认其他系统流量先占 40 GiB/s：

```
model bandwidth budget
= 200 - 40
= 160 GiB/s
```

若每 token 近似流过 18 GiB 权重：

```
160 / 18
≈ 8.89 token/s
```

若没有其他流量：

```
200 / 18
≈ 11.11 token/s
```

这只是 bandwidth upper-bound teaching model。

真实实现会受到：
- cache/reuse；
- quant/dequant；
- GPU utilization；
- memory controller；
- thermal；
- KV；
- speculative decoding；
- batching；

影响。

## 运行

```bash
python3 simulate.py
```

自定义：

```bash
python3 simulate.py \
  --total-gib 64 \
  --system-reserve-gib 8 \
  --safety-gib 6 \
  --weights-gib 34 \
  --kv-gib 4 \
  --workspace-gib 2 \
  --bandwidth-gib-s 400 \
  --other-traffic-gib-s 50 \
  --discrete-vram-gib 24
```

## 思考题

1. 为什么增加统一内存容量不一定增加 TG？
2. 为什么相同 64 GB，Pro/Max 的 memory bandwidth 可能比 GPU core 数更值得先看？
3. 为什么 `recommendedMaxWorkingSetSize` 比 installed RAM 更接近真实 GPU working-set Evidence？
4. 如果 context/concurrency 增加 KV，capacity margin 会怎样？
