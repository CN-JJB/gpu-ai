# Experiment 64 — Little's Law Trace Identity

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/serving-capacity-littles-law.svg" alt="Little's Law 用 L = λW 把在途请求、到达率与平均停留时间联系起来；它是容量一致性检查，不是延迟承诺。">
  <figcaption>Little's Law 用 L = λW 把在途请求、到达率与平均停留时间联系起来；它是容量一致性检查，不是延迟承诺。</figcaption>
</figure>

## Goal

Verify three consistent boundaries:

```
L_system = λ W_system
L_active = λ W_active
L_queue  = λ W_queue
```

and:

```
L_system
=
L_active + L_queue
```

## Run

```bash
python3 little.py trace-synthetic.csv
```

## Expected teaching result

```
lambda = 1.2 req/s

L_system = 3.0
L_active = 2.7
L_queue  = 0.3
```

But peaks:

```
system peak = 5
active peak = 4
queue peak  = 1
```

So average occupancy is not peak capacity.

## KV proxy

Default:

```
1.5 GiB / active sequence
```

gives:

```
average active KV proxy = 4.05 GiB
peak active KV proxy = 6.0 GiB
```

Synthetic only.

Real KV depends on current sequence/cache state.


## Why this experiment

Little's Law 最容易被误用成“L 算出来多少，就配多少 slots”。这个实验用一条 trace 同时验证 system、active、queue 三个边界，让你先学会边界一致性。

## Hypothesis

只要 L、λ、W 取自同一个边界，三条 Little's Law identity 应成立；但平均 L 不等于 peak concurrency，因此不能直接拿平均值做容量硬上限。

## Fixed variables

同一 trace、同一 observation window、同一 λ。只改变你计算 W/L 时选取的系统边界。

## What to observe

1. L_system 是否等于 L_active + L_queue。
2. 三条 λW 是否分别匹配对应 L。
3. average 与 peak 差多少。
4. KV proxy 用 average 和 peak 时差多少 GiB。

## Troubleshooting

- 不要把 system W 与 active L 混用。
- throughput λ 必须使用同一 observation window。
- synthetic KV/request 只是 proxy；真实 sequence context 长度不同。

## Evidence to save

保存命令、trace、输出，并写一句：为什么 L_active=2.7 不能推出“3 slots 永远足够”。

## What this proves

你能正确使用 Little's Law 做 steady-state sanity check，并区分平均 occupancy 与 peak capacity。

## What this does NOT prove

它不预测 burst arrival、tail latency，也不自动给出最佳 slot 数。

## No-hardware path

完整 L0 实验。

## Transfer question

如果平均 active=3.2、peak active=7，而你的 SLO 不允许排队，你会只配 4 slots 吗？还需要什么证据？
