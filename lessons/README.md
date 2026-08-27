# Lessons

每个 Lesson 是一个短、自包含、绑定 Mission 和 ZPD 的教学单元。默认结构见 `templates/LESSON.md`。

Lesson 只承载获得目标技能所需知识；需要查表的信息链接到 Reference；易变信息链接到 Intelligence。


## 已实现 Lesson 索引

| Slice | 目录 | 内容 |
|---:|---|---|
| 01 | `01-gpu-evolution/` | unified programmable GPU |
| 02 | `02-gpu-execution-model/` | scheduler / latency hiding |
| 03 | `03-gpu-memory/` | registers/shared/tiling |
| 04 | `04-gpu-bandwidth/` | Roofline |
| 05 | `05-llm-memory/` | weights/KV/VRAM |
| 06 | `06-llm-quantization/` | datatype/quant/container/backend |
| 07 | `07-local-inference/` | first reproducible local LLM |
| 08 | `08-local-serving/` | slots/batching/TTFT |
| 09 | `09-kv-cache/` | prefix/paged KV |
| 10 | `10-speculative-decoding/` | draft/verify/accept |
| 11 | `11-multi-gpu/` | capacity split/interconnect |
| 12 | `12-attention-kernels/` | FlashAttention / I/O |
| 13 | `13-matrix-units/` | matrix precision / TOPS |
| 14 | `14-nvidia-architecture/` | Tesla → Blackwell |
| 15 | `15-amd-architecture/` | GCN/RDNA/CDNA |
| 16 | `16-apple-silicon/` | UMA/Metal/ANE/MLX |
| 17 | `17-intel-xe/` | Xe/XMX/oneAPI |
| 18 | `18-hardware-decision/` | cross-vendor hardware decision |
| 19 | `19-secondhand-market/` | China used-GPU market |
| 20 | `20-used-gpu-verification/` | transaction/acceptance |
| 21 | `21-watchlist/` | max buy price |
| 22 | `22-capstone/` | controlled optimization |
| 23 | `23-vendor-capstone/` | CUDA/HIP/Metal/SYCL runbooks |
| 24 | `24-transformer-anatomy/` | decoder-only prefill/decode |
| 25 | `25-rmsnorm-rope/` | RMSNorm / residual / RoPE |
| 26 | `26-attention-heads/` | MHA / MQA / GQA |
| 27 | `27-swiglu-ffn/` | dense SwiGLU FFN |
| 28 | `28-moe/` | MoE active/resident/traffic |
| 29 | `29-model-dossier/` | config → hardware hypothesis |
| 30 | `30-modern-kv/` | sliding / hybrid / latent KV |
| 31 | `31-tokenizer-sampling/` | chat template / tokenizer / sampler |
| 32 | `32-quality-gate/` | cross-entropy / perplexity / quality gate |
| 33 | `33-benchmark-manifest/` | semantic A/B manifest / Evidence Packet |
| 34 | `34-serving-slo/` | TTFT / ITL / tail / SLO |
| 35 | `35-serving-capacity/` | Little's Law / slots / KV |
| 36 | `36-overload-admission/` | queue / reject / retry / backoff |
| 37 | `37-multitenant-fairness/` | quotas / borrowing / fairness |
| 38 | `38-service-exposure/` | bind / auth / TLS / privacy |
| 39 | `39-operational-reliability/` | readiness / restart / recovery |
| 40 | `40-safe-upgrade/` | release gates / rollback |
| 41 | `41-observability/` | timeline / saturation / incident diagnosis |
| 42 | `42-power-energy/` | watts / joules / J-token / TCO |

## 使用方式

不需要从 01 线性读到 42。

推荐：
- 想买卡：05 → 06 → 14/15/16/17 → 18 → 19 → 20 → 21
- 想部署：05 → 06 → 07 → 08/09/10 → 22
- 想优化 kernel：02 → 03 → 04 → 12 → 13 → 22
- 想玩多卡：04 → 05 → 07 → 11 → 22


推荐模型结构线：
```
24 → 25 → 26 → 27 → 28 → 29
```

推荐“选模型再选硬件”：
```
24–29
→ 05/06
→ 18
→ 22
```
