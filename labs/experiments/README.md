# Experiments

短实验用于把原理变成可观察现象。默认追求低硬件门槛、快速反馈、可复现。

首批方向：CPU/GPU 并行、访问模式、内存带宽、简单 GEMM、量化显存、KV Cache、context/batch/offload 对性能的影响。


## 已实现实验索引

### 01–10：GPU / LLM 基础

- 01 unified shader load balancing
- 02 latency-hiding scheduler model
- 03 real GPU latency hiding
- 04 GEMM tile reuse model
- 05 naive vs tiled GEMM
- 06 Roofline bottleneck model
- 07 real GPU Roofline probe
- 08 VRAM capacity budget
- 09 effective bpw / metadata
- 10 first reproducible local LLM run

### 11–18：Serving / Cache / Speculation / Multi-GPU

- 11 slots / continuous batching model
- 12 real llama-server concurrency probe
- 13 prefix-cache capacity model
- 14 real prefix-cache probe
- 15 speculative acceptance/overhead model
- 16 real speculative server probe
- 17 multi-GPU interconnect roof model
- 18 real multi-GPU scaling

### 19–22：Attention / Matrix

- 19 online-softmax / attention-I/O model
- 20 real SDPA backend probe
- 21 TOPS vs Roofline model
- 22 real matmul shape/precision

### 23–30：Vendor architecture / capability

- 23 NVIDIA generation traps
- 24 real NVIDIA capability inventory
- 25 AMD generation terminology traps
- 26 real AMD ROCm inventory
- 27 Apple unified-memory capacity/bandwidth model
- 28 real Apple Metal/MLX inventory
- 29 Intel Xe terminology traps
- 30 real Intel XPU/SYCL inventory

### 31–38：买卡 / 市场 / 验收 / Watchlist

- 31 scenario hardware decision model
- 32 real candidate dossier
- 33 secondhand-market normalization
- 34 real market snapshot builder
- 35 seller evidence quality
- 36 real used-GPU acceptance packet
- 37 max-buy-price model
- 38 real candidate watchlist

### 39–41：Capstone

- 39 bottleneck diagnosis cases
- 40 real controlled local-LLM A/B capstone
- 41 vendor capstone preflight

### 42–53：LLM 模型架构

- 42 decoder Transformer shape flow
- 43 real model config anatomy
- 44 RMSNorm scale model
- 45 RoPE relative-position model
- 46 MHA/GQA/MQA KV cost model
- 47 real attention-config comparison
- 48 dense SwiGLU FFN model
- 49 real FFN structure comparison
- 50 MoE active/weight-reuse model
- 51 real MoE config inspector
- 52 model architecture dossier consistency model
- 53 real model architecture dossier

## 实验原则

- L0 synthetic 数据必须显式标记 synthetic。
- 真实实验不预填真实硬件性能。
- 所有可比较结果尽量保存 raw JSON/CSV/log。
- 一个 A/B 只改一个声明变量。
- vendor device identity 必须由实际 runtime/device log 证明。


### 54–59：Modern KV / Prompt / Quality

- 54 sliding/full/hybrid KV model
- 55 real attention/KV architecture inspector
- 56 chat-template/special-token toy model
- 57 real prompt/token identity packet
- 58 cross-entropy/perplexity math model
- 59 real quant/backend quality gate
