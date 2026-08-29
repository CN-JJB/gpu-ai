# Experiment 80 — Storage / Model-Load Stage Model

硬件等级：L0

## Goal

Separate:
- source read time;
- host/backend overhead;
- device upload;
- steady TG.

## Run

```bash
python3 model_load.py scenarios.csv
```

Synthetic setup:

```
model = 20 GiB
host/backend = 1 s
GPU upload = 20 GiB @ 12 GiB/s
steady TG = 50 tok/s
```

Only source bandwidth changes.

## Lesson

Startup can change by tens of seconds while steady TG remains fixed in the model.

This demonstrates:

```
storage startup bottleneck
!=
steady decode bottleneck
```

## Boundary

The script assumes serial full-read + upload stages.

Real mmap, page faults, read-ahead and device loading may overlap or defer work.


## Why this experiment

很多人看到 NVMe benchmark 就直接推导“换更快 SSD，LLM 每秒 token 会更高”。这个实验专门拆开 startup path 与 steady decode，让你避免这种错误迁移。

## Hypothesis

只提高 source bandwidth 时，模型读取阶段会明显缩短，但固定的 steady TG 不应该变化，因为 toy 模型把 decode bottleneck 放在别处。

## Fixed variables

model size、host/backend overhead、device upload bandwidth、steady TG 全部保持不变；只改变 source bandwidth。

## What to observe

1. source read time 如何随带宽变化。
2. 总 startup 中哪个 stage 成为新 bottleneck。
3. 为什么 startup 缩短后 steady TG 仍保持 50 tok/s。
4. 当 source read 已经很快时，继续提高 SSD 带宽为何收益递减。

## Troubleshooting

- 确认 GiB 与 GB 单位没有混。
- 不要把 warm page-cache load 当 cold storage result。
- 真机 mmap 可能延迟 page fault，因此“process ready”与“全部文件已读完”未必同义。

## Evidence to save

保存 scenarios.csv、命令、输出，并画一张 stage breakdown：read / host / upload / steady decode。

## What this proves

你会把 model load 分阶段，并知道 storage 主要影响 startup/cold path。

## What this does NOT prove

它不证明真实 mmap、page cache、read-ahead、GPU upload 能完全串行，也不证明某块 SSD 的实际 LLM 性能。

## No-hardware path

完整 L0 实验。

## Transfer question

如果从 SATA SSD 换 NVMe 后 cold load 从 70 秒降到 20 秒，但 TG 不变，这个结果应该怎样写成正确结论？
