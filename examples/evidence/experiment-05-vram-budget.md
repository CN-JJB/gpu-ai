---
experiment_id: example-local-llm-vram-budget
date: 2026-08-26
hardware_level: L0
risk_level: safe
status: reference-example
---

# Question

在没有下载完整权重、没有真实 GPU 的情况下，能否从 parameter count、effective bpw 与 attention config 先做一份有边界声明的 VRAM preflight？

## Hardware

无特殊硬件。

## Software

Python 3。

## Model

抽象 7B-like GQA model；不是现实 checkpoint。

## Configuration

- parameters：7B
- effective weight bpw：4.5
- layers：32
- query heads：32
- KV heads：8
- head_dim：128
- KV dtype：FP16 / 16 bit
- context：4096
- runtime reserve：1.5 GiB
- target VRAM：8 GiB
- concurrency：1 / 2 / 4 / 8

## Procedure

```bash
python labs/experiments/08-vram-capacity-budget/budget.py --demo
```

## Raw Results

| concurrency | weights | KV | reserve | total | 8 GiB headroom |
|---:|---:|---:|---:|---:|---:|
| 1 | 3.667 GiB | 0.5 | 1.5 | 5.667 | 2.333 |
| 2 | 3.667 | 1.0 | 1.5 | 6.167 | 1.833 |
| 4 | 3.667 | 2.0 | 1.5 | 7.167 | 0.833 |
| 8 | 3.667 | 4.0 | 1.5 | 9.167 | -1.167 |

KV architecture comparison：

| type | KV heads | KiB/token | 4096-token KV |
|---|---:|---:|---:|
| MHA | 32 | 512 | 2 GiB |
| GQA | 8 | 128 | 0.5 GiB |
| MQA | 1 | 16 | 0.0625 GiB |

## Observations

1. weights 在整个实验里不变。
2. full-attention Dynamic KV baseline 与 concurrency 线性增长。
3. 4 并发时 baseline 仍小于 8 GiB，但余量已经很小。
4. 8 并发时，仅 baseline 就超过目标 VRAM。
5. 在相同 layers/head_dim/cache dtype 下，KV footprint 与 KV-head count 成正比。

## Conclusion

“模型能放进显存”不能只看 weight file。

最小判断链：

```text
weight payload
+ KV(context × concurrency)
+ runtime reserve
→ headroom
```

并且这个结果仍然只是 preflight，不是 runtime guarantee。

Paged/static cache、sliding-window attention、KV quantization、backend workspace、allocator 与 offload 都会改变真实数字。

## Transfer

在调查真实模型时：

- 用 config.json 查 attention structure；
- 用 safetensors/model metadata 查 parameter count/dtype；
- 用 backend docs 查 KV dtype/cache policy；
- 最后用真实 GPU/runtime 验证 peak 与 steady memory。

## Sources

- Hugging Face Transformers — Caching
- Hugging Face Transformers — Cache strategies
- Hugging Face LlamaConfig
- Hugging Face Safetensors metadata
- NVIDIA TensorRT-LLM Memory Usage
