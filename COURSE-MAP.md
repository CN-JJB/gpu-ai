# Course Map

课程是能力图，不是只能线性阅读的教材。

## 双主线

### GPU 演进线
GPU 历史与架构演进
→ GPU 执行模型
→ 显存/缓存/带宽/互联
→ 最小 GPU 编程实验
→ Tensor/Matrix 单元与数值类型
→ 二手与特殊 GPU
→ 验卡/诊断/Benchmark
→ 改造与多 GPU

### LLM 演进线
语言模型背景
→ Transformer / Attention
→ Decoder-only LLM
→ 现代模型结构（RoPE、RMSNorm、GQA/MQA、SwiGLU、MoE 等）
→ 模型仓库与权重格式
→ 量化
→ KV Cache / Context
→ Prefill / Decode
→ 推理后端
→ FlashAttention / Paged Attention / Continuous Batching / Prefix Cache / Speculative Decoding
→ 长期服务与优化

两条线最终汇合：

> **模型需要什么 ↔ 硬件能提供什么 ↔ 部署策略是什么**

## 支撑能力

- Linux：驱动、Shell、SSH、systemd、日志、权限、Docker、监控
- Python/脚本：JSON/CSV、subprocess、API、自动 Benchmark、数据清洗
- 数学：矩阵、softmax、数值表示、复杂度、显存/带宽/算力估算
- 整机平台：PCIe、lane、bifurcation、RAM/NUMA、PSU、散热、SSD、网络
- 安全与 License：本地隐私、服务暴露、访问控制、模型许可证

## 主线里程碑

1. M01 认识一张 GPU
2. M02 二手 GPU 选择与风险报告
3. M03 到货验卡与稳定性 SOP
4. M04 最小 GPU Compute 实验
5. M05 第一次本地量化 LLM
6. M06 找瓶颈并完成性能优化
7. M07 低风险垃圾佬改造并用数据验证
8. M08 建立长期可用的本地 LLM 服务
9. M09 单机多 GPU 与扩展效率分析
10. M10 毕业项目：我的本地 LLM 机器设计报告

## Challenge Lab

AMD/老计算卡、特殊 OEM/工程卡、VBIOS、显存扩容、板级维修、Triton、FlashAttention 源码、多机集群、LoRA/QLoRA、RAG、Tool Calling、社区 PR 等。

## 实践门槛

- L0：无额外硬件
- L1：任意 GPU / 核显
- L2：独立 GPU
- L3：额外硬件或工具
- L4：高风险硬核实验

每个 Lesson/Lab 必须声明门槛和可替代路径。


## v1 已实现内容索引

这部分记录仓库中已经落地的 Slice；上面的能力图仍然是长期课程地图。

### A. GPU / LLM 推理基础

| Slice | 主题 |
|---:|---|
| 01 | Fixed-function → unified programmable GPU |
| 02 | Thread / warp-wave / SM-CU / scheduler / latency hiding |
| 03 | Registers / shared-LDS / tiling / reuse |
| 04 | Bandwidth / arithmetic intensity / Roofline |
| 05 | LLM weights / KV / VRAM capacity |
| 06 | Quantization / datatype / container / backend |

### B. 本地运行与 Serving

| Slice | 主题 |
|---:|---|
| 07 | 第一次可复现 llama.cpp 本地 LLM |
| 08 | Slots / continuous batching / TTFT |
| 09 | Prefix Cache / paged-KV concepts |
| 10 | Speculative Decoding |
| 11 | Single-node multi-GPU / interconnect |
| 12 | Attention I/O / FlashAttention |
| 13 | Tensor Core / MFMA / matrix precision / TOPS traps |

### C. 四生态 GPU 架构

| Slice | 主题 |
|---:|---|
| 14 | NVIDIA Tesla/G80 → Blackwell |
| 15 | AMD GCN/Vega → RDNA/CDNA → current frontier |
| 16 | Apple Silicon Unified Memory / Metal / ANE / MLX |
| 17 | Intel EU → Xe-Core/XMX → Arc / oneAPI / SYCL |

### D. 垃圾佬采购与二手市场

| Slice | 主题 |
|---:|---|
| 18 | Cross-vendor fit/support/roof/TCO decision framework |
| 19 | 中国二手 GPU 市场采样与价格归一化 |
| 20 | 二手 GPU 付款前/到手验收 |
| 21 | Max-buy-price / watchlist |

### E. Capstone

| Slice | 主题 |
|---:|---|
| 22 | Measure → diagnose → one-variable A/B |
| 23 | NVIDIA / AMD / Apple / Intel vendor capstone runbooks |

### F. LLM 模型架构主线

| Slice | 主题 |
|---:|---|
| 24 | Decoder-only Transformer：Prefill vs Decode tensor dataflow |
| 25 | RMSNorm / residual / RoPE |
| 26 | MHA / MQA / GQA 与 KV cost |
| 27 | SwiGLU / dense FFN weight traffic |
| 28 | MoE：total / active / resident / traffic |
| 29 | Model Architecture Dossier：config → hardware hypothesis |
| 30 | Sliding / Hybrid / Latent KV architecture |
| 31 | Tokenizer / Chat Template / Sampling identity |
| 32 | Quality Gate：Cross-Entropy / Perplexity / task regression |
| 33 | Benchmark / Workload Manifest：one semantic variable + Evidence Packet |
| 34 | Serving Workload / SLO：TTFT / ITL / tail latency / throughput |
| 35 | Serving Capacity：Little's Law / slots / KV pressure |
| 36 | Overload / Admission Control：bounded queue / retry / backoff |
| 37 | Multi-Tenant Fairness：quotas / work-conserving borrowing / per-tenant SLO |
| 38 | Service Exposure / Privacy / Auth：bind scope / TLS / endpoints / logs |
| 39 | Operational Reliability：liveness / readiness / restart recovery |
| 40 | Safe Upgrade / Rollback：release gates / exact rollback verification |
| 41 | Observability / Incident Diagnosis：latency / traffic / errors / saturation |
| 42 | Power / Energy Efficiency：watts / joules / J-token / electricity |
| 43 | Storage / Model Loading：page cache / mmap / startup vs steady inference |
| 44 | Host Memory Pressure / Swap / OOM：available RAM / paging / host-vs-VRAM OOM |
| 45 | Thermal / Cooling / Sustained Performance：thermal soak / clocks / TG drift |
| 46 | Used-GPU Validation / Purchase Acceptance：identity / PCIe / errors / sustained LLM |
| 47 | PSU / Power Delivery / Platform Integration：capacity / cables / headroom |
| 48 | Whole-Machine System Integration：hard gates / blockers / dossier |
| 49 | Graduation Machine Design Capstone：Evidence review / revisions / upgrade roadmap |

### v1 稳定主线状态

Slice 49 已把前面的模型、GPU、平台、Serving 与 Evidence 汇合成毕业 Machine Design Capstone。

毕业交付物：

~~~text
goal/workload
→ Experiment 91 machine dossier
→ material-claim Evidence index
→ architecture narrative
→ benchmark / quality / SLO
→ TCO / risk
→ revision alternatives
→ evidence-triggered upgrade roadmap
→ explicit non-claims
→ ACCEPT / REVISE / BLOCKED
~~~

稳定主线默认不再为了“继续加内容”扩张。下一阶段优先：
1. 用真实 learner-owned target 完成 Experiment 93；
2. 根据真实毕业报告暴露的缺口回修稳定 Lesson；
3. 否则进入 Intelligence Stations，维护动态硬件 / 模型 / Benchmark 数据。

## Phase 4 Intelligence 实现索引

这部分不是稳定 Lesson Slice；它是动态情报/工具层。

| ID | 内容 | 状态 |
|---|---|---|
| I01 | Hardware/Model entities + Market/Benchmark observations + Experiment 61 bridge | verified |
| I02 | Runtime entities + compatibility observations + documented-vs-measured preflight | verified |
| I03 | exact benchmark Evidence → exact MEASURED_SUPPORTED compatibility | verified |
| I04 | same artifact/quant/workload descriptive benchmark comparison | verified |
| I05 | explicit same-cohort market pairing → price/performance | verified |
| I06 | evidence-linked TCO scenario worksheet | verified |
| I07 | real Experiment 61 Evidence Packet intake gate | verified |
| I08 | NVIDIA/AMD/Apple/Intel documented compatibility coverage | verified |
| I09 | compatibility coverage matrix with scope/freshness | verified |
| I10 | freshness / revalidation queue | verified |
| I11 | explicit GLOBAL-EBAY used MEDIAN_ASK cohort for 3090 / 7900 XTX / A770 | contract-verified |
| I12 | market sample/method audit + MEDIAN_ASK evidence validator | contract-verified |
| I13 | OfferUp SOLD-marked listing cohort with non-confirmed transaction semantics | contract-verified |
| I14 | explicit eBay-ask vs OfferUp-sold-marked cross-contract signal comparison | contract-verified |
| I15 | China 3090/A770 SECONDARY_REPORTED watch signals | verified |
| I16 | stable M0–M3 market evidence selection gate + Experiment 38 bridge | verified |
| I17 | freshness-aware market evidence + Experiment 38 stale BUY-CANDIDATE fix | verified |
| I18 | append-only A770 market refresh lineage + superseded active-view semantics | verified |
| I19 | reusable append-only market refresh helper + lineage preflight/self-test | verified |
| I20 | Experiment 61 manifest ↔ raw llama-bench identity/config cross-check | verified |
| I21 | explicit-argv real benchmark capture/seal + failure-preserving Evidence Packet | verified |
| I22 | non-synthetic local model artifact SHA256/bytes admission gate | verified |
| I23 | exact benchmark argv ↔ verified model artifact binding + command evidence admission | verified |

当前稳定边界：

~~~text
Lesson/Reference
→ durable reasoning

Intelligence
→ dated current observation

Evidence Packet
→ raw/hashed measurement chain
~~~

不要把动态排行榜结果反写成“永久硬件常识”。
