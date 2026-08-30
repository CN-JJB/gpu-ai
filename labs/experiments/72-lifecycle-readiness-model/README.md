# Experiment 72 — Lifecycle / Readiness State Model

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/readiness-recovery.svg" alt="服务 lifecycle 要区分进程启动、依赖就绪、模型加载与真正可接请求；readiness gate 防止“进程活着”被误判为服务可用。">
  <figcaption>服务 lifecycle 要区分进程启动、依赖就绪、模型加载与真正可接请求；readiness gate 防止“进程活着”被误判为服务可用。</figcaption>
</figure>

## Goal

Show that startup/recovery has multiple states.

Synthetic trace:

```
spawn
→ first HTTP
→ health-ready
→ first inference complete
→ later warm request
```

## Run

```bash
python3 analyze.py trace-synthetic.json
```

## Key result

Cold start:

```
first HTTP: 400 ms
ready: 5000 ms
first inference complete: 5800 ms
warm request: 150 ms
```

Restart:

```
first HTTP: 450 ms
ready: 5100 ms
first inference complete: 6300 ms
warm request: 160 ms
```

All numbers are synthetic.

## Lesson

```
listener
!= readiness
!= first usable inference
!= warm steady state
```


## Why this experiment

服务进程“已经监听端口”并不代表模型已经可用。这个实验训练你把 startup 拆成多个可观察状态，从而避免 readiness probe 写得过早或过晚。

## Hypothesis

第一次 HTTP 可达时间通常早于真正 ready；第一次可用推理又可能晚于 ready。重启后的时间线也不一定与冷启动完全相同。

## Fixed variables

使用同一 synthetic trace 结构，只比较 cold start 与 restart 两条生命周期。不要把不同模型大小或不同 readiness 定义混进来。

## What to observe

1. listener、ready、first inference、warm request 四个时间点之间的间隔。
2. 哪个时间点才真正对应“可以接业务流量”。
3. restart 是否恢复到 warm steady state，而不是只恢复 PID。

## Troubleshooting

- 如果 readiness 比 listener 还早，先检查事件时间戳/字段定义。
- 如果把 first HTTP 当 ready，说明 probe 只证明网络栈，而不是模型可用。
- 真机实验时要记录模型大小、storage state 和 backend identity，因为它们都会改变 startup。

## Evidence to save

保存 trace、analyze.py 输出，并画一条 startup timeline。

## What this proves

你能区分 liveness、listener、readiness、first usable inference 与 warm steady state。

## What this does NOT prove

synthetic 数字不代表任何具体 runtime 的真实启动速度，也不证明自动恢复已经配置正确。

## No-hardware path

完整 L0 实验。

## Transfer question

如果 watchdog 在 3 秒时开始接流量，但模型 5 秒才 ready，会出现什么失败模式？
