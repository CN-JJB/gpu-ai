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
