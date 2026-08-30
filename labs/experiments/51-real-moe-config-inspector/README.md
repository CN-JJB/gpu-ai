# Experiment 51 — Inspect a Real MoE config.json

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/moe-routing.svg" alt="真实 MoE config 要同时记录 expert 数、top-k、shared expert 与路由规则，才能解释 active compute 与内存驻留。">
  <figcaption>真实 MoE config 要同时记录 expert 数、top-k、shared expert 与路由规则，才能解释 active compute 与内存驻留。</figcaption>
</figure>

## Goal

Inspect a real Hugging Face-style MoE config and separate:

- routed expert count;
- top-k;
- shared experts;
- hidden size;
- expert intermediate size;
- per-expert dense weight baseline;
- total routed expert storage/layer;
- active routed expert storage/token/layer;
- architecture caveats.

## Run

```bash
python3 inspect_moe_config.py /path/to/config.json --weight-bits 4.5
```

## Supported common field aliases

The script recognizes common names such as:

Routed experts:
- `num_local_experts`
- `n_routed_experts`
- `num_experts`

Top-k:
- `num_experts_per_tok`
- `num_selected_experts`

Expert FFN:
- `moe_intermediate_size`
- fallback `intermediate_size`

Shared experts:
- `n_shared_experts`
- `num_shared_experts`

## Important

Field aliases do not make architectures identical.

If the config exposes:
- shared expert width;
- dense-first layers;
- MoE frequency;
- expert-specific projection structure;
- unusual routing;

read the model implementation/paper before extrapolating full-model totals.

The script intentionally reports per-layer baselines first.


## Why this experiment

真实 MoE config 的字段名并不统一。这个工具的目标不是“见到 aliases 就自动算完整模型”，而是先把可确认字段提取出来，再明确哪些地方必须读实现或论文。

## Hypothesis

对于结构信息足够的 config，可以安全得到 per-expert / per-layer baseline；但只凭字段 alias 不能推出共享 expert、MoE frequency、dense-first layers 等完整拓扑。

## Fixed variables

一次只检查一个 exact config/revision，weight-bits 固定。

## What to observe

1. routed expert count。
2. top-k。
3. shared expert fields 是否存在。
4. expert intermediate size。
5. per-expert baseline、total routed storage/layer、active routed storage/token/layer。
6. 工具输出的 caveats。

## Troubleshooting

- alias 同名/同义不代表 architecture identical。
- fallback intermediate_size 只是候选解释，要核对模型实现。
- shared experts、dense layers、frequency 会改变 full-model totals。
- config 缺失时保留 UNKNOWN。

## Evidence to save

保存原始 config、来源/revision、命令、输出和一段 caveat summary。

## What this proves

你能从真实 MoE config 提取结构证据，同时知道何时停止自动推导。

## What this does NOT prove

它不证明真实 active FLOPs、resident VRAM、routing 分布或性能。

## No-hardware path

完整 L0。

## Transfer question

如果 config 写 num_experts=64、top_k=2，但没有 MoE layer frequency，你能直接计算整模型 expert 总量吗？
