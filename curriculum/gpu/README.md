# GPU Curriculum

GPU 是课程开篇主线，但目标不是背型号。

核心追问：

1. 上一代瓶颈是什么？
2. 改了什么，为什么？
3. 对执行、内存、矩阵和软件有什么影响？
4. 对今天本地 LLM 推理意味着什么？
5. 对二手价值、软件支持和整机风险意味着什么？

## 学习顺序

### A. 执行与内存 — Slice 01–04

~~~text
01 GPU 演进
→ 02 thread/warp/SM/scheduler
→ 03 register/shared/LDS/tiling
→ 04 bandwidth/arithmetic intensity/Roofline
~~~

出口能力：
- 不再用“CUDA Core 数”解释一切；
- 能画 scheduler / latency hiding；
- 能解释 reuse 与 on-chip memory；
- 能判断 memory-bound vs compute-bound 假设。

### B. LLM 把 GPU 逼到哪里 — Slice 05–13

~~~text
05 weights/KV/VRAM
→ 06 quant/backend
→ 07 inference
→ 08–10 serving/cache/speculation
→ 11 multi-GPU
→ 12 attention I/O
→ 13 matrix units
~~~

出口能力：
- 从模型 bytes 反推显存；
- 区分 PP/TG；
- 解释多卡通信 roof；
- 不把 quant file bits 与 matrix precision 混为一谈。

### C. 四生态 — Slice 14–17

~~~text
14 NVIDIA
15 AMD
16 Apple
17 Intel
~~~

每个生态都用同一框架：

~~~text
execution
+ memory hierarchy
+ matrix/numerics
+ memory system/interconnect
+ software enablement
+ exact SKU
~~~

NVIDIA 是主 spine；AMD 系统覆盖；Apple 重点看 unified memory/Metal；Intel 重点看 Xe/XMX/oneAPI。

### D. 垃圾佬选择与验证 — Slice 18–23

从架构能力走到：
- candidate dossier；
- 二手价格 Evidence；
- 卖家 claim；
- 到货验收；
- max buy price；
- controlled A/B；
- vendor capstone。

### E. 整机 — Slice 42–49

GPU 不独立存在。

最终回到：
- energy；
- storage；
- host RAM；
- thermal；
- used-GPU validation；
- PSU；
- whole-machine hard gates；
- graduation design。

## 真机缺失时

历史架构、跨厂商和多卡内容都有 L0 路径。

不要为了学架构收集硬件。真实卡只在它能产生新的 learner-owned Evidence 时使用。

## 进阶

完成主线后进入：
- [Challenge Labs](../../labs/challenges/README.md)
- 旧卡兼容考古；
- VBIOS/OEM forensic；
- VRAM/板修理论；
- Triton/FlashAttention/source patch；
- 多机垃圾佬集群。
