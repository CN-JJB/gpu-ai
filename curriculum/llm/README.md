# LLM Curriculum

LLM 主线的目标是：**先看模型需要什么，再反推硬件、backend 与服务设计。**

## A. 本地推理基础 — Slice 05–10

先建立：
- weights / KV / VRAM；
- quant / container / backend；
- 第一次可复现本地运行；
- serving slots / batching；
- prefix cache；
- speculative decoding。

这部分让你不再把“模型能运行”与“模型适合这个 workload”混在一起。

## B. 模型结构 — Slice 24–30

~~~text
24 decoder-only / prefill / decode
25 RMSNorm / residual / RoPE
26 MHA / MQA / GQA
27 SwiGLU / FFN
28 MoE
29 Architecture Dossier
30 sliding / hybrid / latent KV
~~~

出口能力：

拿到一个没学过的新模型 config，你能：
1. 找 hidden/layers/FFN/attention；
2. 判断 dense/MoE；
3. 算标准 KV 或指出标准公式失效；
4. 形成 VRAM/bandwidth/compute hypothesis；
5. 明确哪些结论仍需 runtime measurement。

## C. 输入与实验身份 — Slice 31–33

~~~text
tokenizer/chat template/sampler
→ quality gate
→ benchmark manifest
~~~

这一步把“同一个 prompt/同一个模型”变成真正可验证的 identity。

## D. Serving / Ops — Slice 34–43

~~~text
SLO
→ capacity
→ overload
→ fairness
→ exposure/privacy
→ readiness/recovery
→ upgrade/rollback
→ observability
→ energy
→ storage
~~~

出口能力：

不是只会启动 server，而是会问：
- 谁在用？
- arrival/length 分布是什么？
- p95/p99 是否过 SLO？
- queue/KV/compute 谁饱和？
- 过载怎样失败？
- 升级怎样回滚？
- 长期电费与稳定性怎样记录？

## E. Machine Design — Slice 44–49

模型最终落到整机：
- host RAM；
- swap/OOM；
- thermal；
- 二手 GPU；
- PSU；
- whole-machine feasibility；
- graduation report。

## 扩展应用

主线完成后：
- [LoRA / QLoRA](../../labs/challenges/08-lora-qlora-adaptation/README.md)
- [Local RAG](../../labs/challenges/09-local-rag-evidence/README.md)
- [Tool Calling / Agent](../../labs/challenges/10-tool-calling-agent/README.md)
- [Multimodal](../../labs/challenges/12-multimodal-local-inference/README.md)

这些不是平行大课程；它们复用主线已经建立的：
- identity；
- memory budget；
- quality；
- serving；
- Evidence；
- safety。
