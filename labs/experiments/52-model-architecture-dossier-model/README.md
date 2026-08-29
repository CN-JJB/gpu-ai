# Experiment 52 — Architecture Dossier Consistency Model

硬件等级：L0

## Goal

Test the dossier formulas on two synthetic configs:
- one dense GQA model;
- one top-2 MoE model.

Run:

```bash
python3 dossier.py dense-config.json --context 32768 --kv-bits 16 --params-b 8 --weight-bpw 4.5 --reserve-gib 1 --memory-gib 12
python3 dossier.py moe-config.json --context 32768 --kv-bits 16 --params-b 47 --weight-bpw 4.5 --reserve-gib 1 --memory-gib 24
```

All config/model-size values are synthetic teaching inputs.

The purpose is to verify:
- derived head relation;
- KV;
- dense FFN;
- MoE fields;
- asymmetric capacity verdict.


## Why this experiment

以后拿到陌生模型时，最危险的习惯是只看“8B / 47B”。这个实验训练你从 config 提取真正影响本地部署的结构字段，再把它们转成硬件假设。

## Hypothesis

两个总参数规模相近或看起来都“能量化”的模型，可能因为 KV heads、FFN/MoE 结构、resident experts 等差异，在显存和执行行为上完全不同。

## Fixed variables

同一次比较中固定 context、KV bits、weight bpw、reserve 和目标显存；只让 config 结构不同。

## What to observe

逐项核对：
- hidden_size / num_attention_heads = head_dim 是否一致；
- KV heads 如何改变 KV budget；
- dense FFN 与 MoE active/resident 参数的语义不同；
- 最终 capacity verdict 为什么可能不对称。

## Troubleshooting

- config 字段缺失时写 UNKNOWN，不要猜默认值。
- 不要把 total MoE parameters 直接当每 token active parameters。
- 不要把模型文件大小当成 runtime VRAM 全部占用。

## Evidence to save

保存两条完整命令、两个 config、工具输出，并写一张两列 dossier：field → hardware implication。

## What this proves

你会把模型结构转成可审计的显存/执行假设。

## What this does NOT prove

它不证明真实 PP/TG、质量或 backend 支持；所有输入仍是 synthetic。

## No-hardware path

这是完整 L0 主路径。

## Transfer question

遇到一个 30B MoE 模型时，为什么仅凭“每 token 只激活 3B”不能推导它只需要约 3B 权重的显存？
