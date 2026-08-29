# Experiment 08 — 在买卡前算清 Weights + KV + Headroom

Hardware level: L0  
Risk: safe  
Cost: 0  
需要：Python 3

## 问题

一张 GPU 能否运行某个本地 LLM，不应该只看 checkpoint 文件大小。

我们先做：

```text
weights baseline
+ KV baseline
+ runtime reserve
= preflight estimate
```

然后再看 headroom。

## 运行内置演示

```bash
python budget.py --demo
```

内置抽象 model：

- 7B parameters
- 4.5 effective bpw
- 32 layers
- 32 attention heads
- 8 KV heads
- head_dim 128
- FP16 KV
- context 4096
- runtime reserve 1.5 GiB

它会比较 concurrency 1 / 2 / 4 / 8。

## 自己计算

例如：

```bash
python budget.py \
  --params-b 7 \
  --weight-bpw 4.5 \
  --layers 32 \
  --attention-heads 32 \
  --kv-heads 8 \
  --head-dim 128 \
  --kv-bits 16 \
  --context 4096 \
  --concurrency 4 \
  --reserve-gib 1.5 \
  --vram-gib 8
```

## 输出

程序报告：

- weight baseline GiB
- attention type
- KV bytes/token/sequence
- KV GiB / sequence
- total KV GiB
- runtime reserve
- total estimate
- VRAM headroom
- headroom %
- preflight status

## Status 不是 runtime guarantee

程序只给三个 preflight 标签：

- `ROOMY`：baseline 之后仍有明显余量
- `TIGHT`：正 headroom，但低于 VRAM 的 10%
- `OVER`：baseline 已超过 VRAM

10% 只是课程 warning threshold，不是 backend 安全线。

## 比较 MHA / GQA / MQA

保持：

- layers=32
- head_dim=128
- KV FP16
- context=4096

依次运行：

```bash
python budget.py --params-b 7 --weight-bpw 4.5 --layers 32 --attention-heads 32 --kv-heads 32 --head-dim 128 --kv-bits 16 --context 4096 --concurrency 1 --reserve-gib 1.5 --vram-gib 16

python budget.py --params-b 7 --weight-bpw 4.5 --layers 32 --attention-heads 32 --kv-heads 8 --head-dim 128 --kv-bits 16 --context 4096 --concurrency 1 --reserve-gib 1.5 --vram-gib 16

python budget.py --params-b 7 --weight-bpw 4.5 --layers 32 --attention-heads 32 --kv-heads 1 --head-dim 128 --kv-bits 16 --context 4096 --concurrency 1 --reserve-gib 1.5 --vram-gib 16
```

应看到：

- MHA：2 GiB KV / sequence
- GQA：0.5 GiB
- MQA：0.0625 GiB

## 真模型：读 config.json

如果你已经有一个 Hugging Face 风格模型目录：

```bash
python inspect_config.py /path/to/model/config.json \
  --params-b 7 \
  --weight-bpw 4.5 \
  --kv-bits 16 \
  --context 8192 \
  --concurrency 1 \
  --reserve-gib 2 \
  --vram-gib 12
```

脚本会尝试读取：

- num_hidden_layers
- hidden_size
- num_attention_heads
- num_key_value_heads
- head_dim

如果顶层有 `text_config`，优先读 text config。

若 `head_dim` 缺失，则只对类似 Llama 的普通配置使用：

```text
hidden_size // num_attention_heads
```

并明确打印这个 fallback。

## 不能机械处理的 config

如果模型包含：

- per-layer heterogeneous config
- sliding-window layers
- chunked attention
- hybrid attention
- state-space / recurrent blocks
- cross attention

脚本只做 baseline，会打印 warning。

这时候你必须人工按层修正。

## Safetensors 调查

参数量不要只从模型名字猜。

优先：
1. model card / official metadata；
2. safetensors metadata；
3. backend converted model 的 metadata。

Hugging Face safetensors header 可以只读 tensor dtype/shape，不下载全部 payload 就统计参数数量。

## Evidence

提交 Experiment Card，并至少做三次决策：

1. 同一模型 4K vs 32K context。
2. concurrency 1 vs 4。
3. MHA vs GQA 或不同 KV dtype。

回答：

- 哪个因素先让你 OOM？
- 你留了多少 runtime reserve？
- 为什么这份 estimate 不能当“肯定能跑”？
- 如果必须 offload，你认为下一层 bottleneck 会在哪里？


## Hypothesis

显存 fit 取决于 weights + KV + runtime/workspace + headroom；context、concurrency、Hkv/KV dtype 中任一变化都可能让同一模型从 ROOMY 变成 TIGHT/OVER。

## Fixed variables

每次比较只改 context、concurrency、KV heads 或 KV dtype 中的一项。weight bpw、layers、reserve 与 candidate VRAM 保持不变。

## What to observe

- weight baseline 与 KV 分开；
- KV bytes/token/sequence；
- context/concurrency 的线性影响；
- MHA/GQA/MQA 的 KV 差异；
- headroom % 与 TIGHT warning；
- config warning 何时要求人工逐层修正。

## Troubleshooting

- 模型文件大小不等于 weights runtime bytes。
- 10% 只是课程 warning，不是 backend safety line。
- heterogeneous/sliding/hybrid 模型不要套 homogeneous baseline 当最终结果。
- OFFLOAD 能避免 OOM 也会改变下一层 bottleneck。

## What this proves

你能在买卡前做可解释的 VRAM preflight，并识别最敏感的容量变量。

## What this does NOT prove

它不保证 runtime 一定成功，也不包含全部 allocator/workspace/backend overhead。

## No-hardware path

完整 L0。

## Transfer question

同一个 7B Q4 模型从 4k 单用户变成 32k 四并发时，为什么“模型权重没变”仍可能突然 OOM？
