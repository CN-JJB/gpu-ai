# Experiment 55 — Inspect Real Attention/KV Architecture

硬件等级：L0

## Goal

Inspect a real `config.json` for evidence that the homogeneous full-attention KV formula may be incomplete.

The tool checks common fields for:
- sliding window;
- explicit layer types;
- Hq/Hkv/Dh;
- DeepSeek-style MLA dimensions.

## Run

```bash
python3 inspect_attention.py config.json --context 32768 --kv-bits 16
```

Optional:

```bash
--assume-all-sliding
```

Only use that flag after architecture documentation confirms every attention layer uses the configured sliding window.

Optional DeepSeek-family proxy:

```bash
--deepseek-mla-proxy
```

Only use after confirming the model uses the matching MLA cache formulation.

## Principle

The tool prefers:

```
UNKNOWN
```

over silently applying the wrong formula.


## Why this experiment

真实模型的 attention 结构越来越多样。工具的价值不是“自动算出唯一 KV”，而是先识别什么时候简单 full-attention 公式已经不够。

## Hypothesis

遇到 sliding window、显式 layer types 或 MLA 字段时，工具应该更愿意输出 caveat/UNKNOWN，而不是静默给一个看起来精确但语义错误的 GiB 数。

## Fixed variables

固定同一个 config、context、kv-bits。只有在外部 architecture evidence 明确支持时，才使用可选 assume/proxy flag。

## What to observe

1. 工具识别到哪些 attention fields。
2. 哪些字段足够支持直接计算，哪些只能提示 caveat。
3. --assume-all-sliding 为什么需要额外架构证据。
4. --deepseek-mla-proxy 为什么只能用于匹配的模型族/缓存定义。

## Troubleshooting

- 不要因为 config 里出现 sliding_window 就自动假设所有层都 sliding。
- 不要把一个 model-family proxy 推广到所有 latent attention。
- 字段缺失时优先 UNKNOWN。
- 真实 runtime 可能还有 padding、quantized KV、allocator overhead。

## Evidence to save

保存原始 config、来源/revision、命令、工具输出和你使用任何 optional flag 的依据。

## What this proves

你能识别真实模型中“简单 KV 公式何时失效”的证据。

## What this does NOT prove

它不等于 runtime VRAM 实测，也不证明 backend 是否实现了对应 cache 优化。

## No-hardware path

完整 L0，只需要 config 和架构资料。

## Transfer question

如果 config 有 sliding_window=4096，但只有一半层是 local attention，你为什么不能使用 --assume-all-sliding？
