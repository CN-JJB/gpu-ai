# Experiment 17 — Multi-GPU Interconnect Roof Model

硬件等级：L0（不需要 GPU）

<figure>
  <img src="../../../assets/diagrams/multi-gpu-split-interconnect.svg" alt="多 GPU 分割模型必须同时看计算分工与跨卡传输；互连带宽/延迟可能把理论算力收益吃掉。">
  <figcaption>多 GPU 分割模型必须同时看计算分工与跨卡传输；互连带宽/延迟可能把理论算力收益吃掉。</figcaption>
</figure>

## 问题

为什么两张 GPU 即使理想计算部分减半，也可能因为跨卡通信而比单卡更慢？

## 模型

单卡：
```
T1 = single_compute_ms
```

N 卡简化模型：
```
TN =
  single_compute_ms / N
  + critical_transfer_bytes / effective_link_bandwidth
  + sync_ms
  + imbalance_ms
```

然后计算：
```
speedup = T1 / TN
efficiency = speedup / N
```

## 默认教学参数

- 单卡计算：10 ms/token
- GPU 数：2
- 关键路径通信：64 MiB/token
- 同步：0.2 ms/token
- imbalance：0
- P2P：8, 16, 32, 64, 128 GiB/s

## 运行

```bash
python3 simulate.py
```

也可修改参数：

```bash
python3 simulate.py --single-ms 10 --gpus 2 --transfer-mib 64 --sync-ms 0.2 --bandwidth 8 16 32 64 128
```

## 观察

重点不是记住某个 crossover，而是回答：

1. 哪个带宽以下双卡反而更慢？
2. 通信量翻倍时发生什么？
3. 如果单卡计算从 10 ms 降到 5 ms，但通信量不变，为什么 interconnect 更容易成为瓶颈？
4. efficiency 与 speedup 为什么不是一回事？

## 约束

这是 deterministic teaching model，不代表任何真实 GPU、PCIe generation、NVLink 或 xGMI 的实际性能。

## Hypothesis

在计算理想按 N 卡均分的前提下，只要关键路径通信、同步和 imbalance 足够大，多卡 speedup 就会低于线性，甚至低于 1×。

## Fixed variables

默认只改变 effective link bandwidth。之后的扩展实验一次只改 transfer MiB 或 single-compute ms。

## What to observe

1. bandwidth 增加时 TN 如何下降。
2. speedup 与 efficiency 的差别。
3. transfer 翻倍如何移动 crossover。
4. compute 变快但通信不变时，为什么通信占比上升。
5. 哪种情况下“第二张卡增加容量但降低单 token 速度”仍可能值得。

## Troubleshooting

- GiB/s 与 GB/s 不要混。
- 64 MiB/token 是 synthetic critical-path traffic，不代表任何真实 split。
- effective link bandwidth 已经是折后量，不等于 PCIe 标称峰值。
- 不要把模型输出当真实 NVLink/PCIe benchmark。

## Evidence to save

保存默认输出，再做两次单变量变化：transfer×2、single compute÷2。记录 crossover/efficiency 的方向变化。

## What this proves

你理解多卡扩展由 compute、communication、sync、imbalance 共同决定。

## What this does NOT prove

它不预测任何真实 runtime 的 split strategy、P2P 路径或性能。

## No-hardware path

完整 L0。

## Transfer question

如果单卡 kernel 优化后 compute 时间减半，而跨卡通信完全不变，多卡 scaling 为什么可能反而变差？
