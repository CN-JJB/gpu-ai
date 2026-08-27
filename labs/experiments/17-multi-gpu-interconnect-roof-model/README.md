# Experiment 17 — Multi-GPU Interconnect Roof Model

硬件等级：L0（不需要 GPU）

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