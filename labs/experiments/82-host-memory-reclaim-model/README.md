# Experiment 82 — Host Memory Reclaim Model

硬件等级：L0

## Goal

Understand why:

```
MemFree low
```

does not automatically mean:

```
no usable RAM remains
```

The model separates:
- anonymous memory;
- file cache;
- kernel/other;
- free RAM;
- a synthetic reclaimable-cache fraction.

## Run

```bash
python3 memory_model.py scenarios.csv
```

## Important

The calculated:

```
available_proxy
```

is **not** the Linux `MemAvailable` algorithm.

It is only a teaching proxy.

For real Linux evidence, read:

```
/proc/meminfo: MemAvailable
```

## Key cases

Cache-heavy:
```
free = 2 GiB
proxy available = 16.4 GiB
8 GiB request fits after synthetic reclaim
```

Anonymous-heavy:
```
free = 2 GiB
proxy available = 4.4 GiB
8 GiB request leaves 3.6 GiB shortfall
```


## Why this experiment

Linux 把空闲 RAM 用作 file cache 是正常行为。只盯 MemFree 很容易误判“内存快没了”。这个模型训练你区分 anonymous memory、cache、free 和可回收空间。

## Hypothesis

free 同为 2 GiB 的两台 synthetic 机器，cache-heavy 场景可以通过回收 cache 满足 8 GiB 请求，而 anonymous-heavy 场景可能真正短缺。

## Fixed variables

总 RAM 和请求大小保持一致，只改变 memory composition 与 synthetic reclaimable-cache fraction。

## What to observe

1. 两个 case 的 free 一样，但 available_proxy 为什么不同。
2. cache-heavy 场景回收后请求是否 fit。
3. anonymous-heavy 场景为什么不能把匿名内存当 cache 随便回收。
4. proxy 与真实 Linux MemAvailable 的边界。

## Troubleshooting

- available_proxy 不是 Linux 内核算法，不能拿它替代 /proc/meminfo。
- 不要把 page cache 等同“浪费”。
- 真实系统还要看 swap in/out、major faults、cgroup limits、OOM logs。

## Evidence to save

保存 scenarios.csv、输出，并写一句：为什么“free=2GiB”不足以判断 8GiB 新分配是否会成功。

## What this proves

你理解 host-memory reclaim 的方向性模型，并知道为什么 available 比 free 更接近容量判断。

## What this does NOT prove

它不预测真实 kernel reclaim、swap latency、NUMA/cgroup 行为。

## No-hardware path

完整 L0 实验。

## Transfer question

一个模型进程 RSS 很大，同时 page cache 也很大，你还需要看哪些信号才能判断系统是否真的内存紧张？
