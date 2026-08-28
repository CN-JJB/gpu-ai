# Reference Library

Reference 用来“忘了就查”，不是 Lesson 的替代品。这里保存公式、术语、架构对照、SOP、decision card 与 cheat sheet。

学生主入口仍然是 [curriculum/README.md](../curriculum/README.md)。

## GPU

### 执行 / 内存 / 性能
- [GPU evolution](gpu/evolution-fixed-to-ai.md)
- [Thread / Warp / SM / Latency](gpu/execution-model-thread-warp-sm-latency.md)
- [On-chip Memory / Tiling / Reuse](gpu/on-chip-memory-tiling-reuse.md)
- [Bandwidth / Roofline / LLM](gpu/bandwidth-roofline-llm-bottleneck.md)
- [Multi-GPU Split / Interconnect](gpu/multi-gpu-split-interconnect.md)
- [Attention I/O / Online Softmax](gpu/attention-io-online-softmax.md)
- [Matrix Units / Precision / TOPS](gpu/matrix-units-precision-tops.md)

### 四生态架构
- [NVIDIA Generation Spine](gpu/nvidia-generation-spine.md)
- [AMD Generation Spine](gpu/amd-generation-spine.md)
- [Apple Silicon / Unified Memory / Metal](gpu/apple-silicon-unified-memory-metal.md)
- [Intel Xe / Arc / XMX](gpu/intel-xe-arc-xmx.md)

### 实体硬件
- [Thermal / Sustained Performance](gpu/thermal-sustained-performance.md)
- [Used-GPU Purchase Acceptance](gpu/used-gpu-purchase-acceptance.md)

## LLM

### 第一次运行 / 容量 / 量化
- [llama.cpp First-Run Checklist](llm/llama-cpp-first-run-checklist.md)
- [Weights / KV / VRAM Budget](llm/vram-weights-kv-budget.md)
- [Quantization / Format / Backend](llm/quantization-format-backend-map.md)
- [Prefix / Paged KV](llm/prefix-paged-kv-cache.md)
- [Speculative Decoding](llm/speculative-decoding-acceptance-overhead.md)

### 模型结构
- [Decoder-only Block Shapes](llm/decoder-only-block-shapes.md)
- [RMSNorm / Residual / RoPE](llm/rmsnorm-residual-rope.md)
- [MHA / MQA / GQA / KV](llm/mha-mqa-gqa-kv.md)
- [SwiGLU / FFN Weight Traffic](llm/swiglu-ffn-weight-traffic.md)
- [MoE Total / Active / Resident / Traffic](llm/moe-total-active-resident-traffic.md)
- [Model Architecture Dossier](llm/model-architecture-dossier-card.md)
- [Sliding / Hybrid / Latent KV](llm/sliding-hybrid-latent-kv.md)

### 输入 / 质量 / Serving
- [Prompt / Tokenizer / Sampling Identity](llm/prompt-tokenizer-sampling-identity.md)
- [Quality Gate](llm/quality-gate-card.md)
- [Server Concurrency / Batching / Metrics](llm/server-concurrency-batching-metrics.md)
- [Serving Workload / SLO](llm/serving-workload-slo.md)
- [Serving Capacity / Little's Law](llm/serving-capacity-littles-law.md)
- [Overload / Admission Control](llm/overload-admission-control.md)
- [Multi-Tenant Fairness](llm/multitenant-fairness-quotas.md)
- [Service Exposure / Privacy / Auth](llm/service-exposure-privacy-auth.md)

### 长期运行
- [Operational Reliability / Recovery](llm/operational-reliability-recovery.md)
- [Safe Upgrade / Rollback](llm/safe-upgrade-rollback.md)
- [Observability / Incident Diagnosis](llm/observability-incident-diagnosis.md)
- [Power / Energy Efficiency](llm/power-energy-efficiency.md)
- [Storage / Model Loading](llm/storage-model-loading.md)
- [Host Memory / Swap / OOM](llm/host-memory-pressure-swap-oom.md)

## Hardware / Market

- [Cross-Vendor Decision Card](hardware/cross-vendor-decision-card.md)
- [Used-GPU Acceptance Checklist](hardware/used-gpu-acceptance-checklist.md)
- [Condition Evidence Grades](hardware/condition-evidence-grades.md)
- [PSU / Power Delivery](hardware/psu-power-delivery.md)
- [China Secondhand GPU Sampling](market/china-secondhand-gpu-sampling-card.md)
- [Max Buy Price / Watchlist](market/max-buy-price-watchlist-card.md)

## System / Capstone

- [Benchmark / Workload Manifest](system/benchmark-workload-manifest.md)
- [Capstone Bottleneck Decision Tree](system/capstone-bottleneck-decision-tree.md)
- [Vendor Capstone Runbooks](system/vendor-capstone-runbooks.md)
- [Whole-Machine Integration Dossier](system/whole-machine-integration-dossier.md)
- [Graduation Machine Design Capstone](system/graduation-machine-design-capstone.md)

## 使用原则

查到一张 Reference 卡后仍然要问：

1. 这是稳定原理，还是会过期的 current support？
2. 这个公式的单位和适用范围是什么？
3. 哪些字段需要真机/真实 artifact 才能填？
4. 哪些结论应该转到 Intelligence 查询？
5. 这张卡能支持哪个 claim，又不能支持什么？

Reference 是工作记忆，不是权威来源的替代品；需要做 material decision 时继续追到页面列出的 primary/current source。
