# Resources

真实课程内容开始后维护。

## Source priority

1. 官方架构白皮书 / 官方开发文档 / 官方源码
2. 原始论文与规范
3. 推理框架官方文档与实现
4. 项目维护者 Issue/PR/Release
5. 可复现社区测试
6. 社区经验帖
7. 卖家描述（只能作为待验证线索）

每条资源记录：用途、可信度、适用版本/日期和局限。

## GPU execution model / memory hierarchy

### NVIDIA CUDA Programming Guide

URL: https://docs.nvidia.com/cuda/cuda-programming-guide/

用途：
- thread/block/warp/SM
- scheduler / hardware multithreading
- registers/shared/global/local memory
- CUDA 编程模型与资源限制

可信度：官方一手资料。  
适用：CUDA 当前文档；架构具体常数仍需查目标 compute capability。  
局限：NVIDIA-specific，不直接代表 AMD/Apple。

### NVIDIA CUDA C++ Best Practices Guide

URL: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/

用途：
- occupancy
- coalescing
- shared-memory tiling
- bank conflicts
- matrix-multiply memory reuse
- theoretical/effective bandwidth
- compiler resource/spill guidance

可信度：官方一手最佳实践。  
适用：CUDA；部分原理可迁移。  
局限：示例数字与细节可能针对特定 GPU/compute capability。

### NVIDIA Nsight Compute Profiling Guide

URL: https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html

用途：
- Roofline
- achieved performance
- memory/compute ceilings
- per-kernel profiler interpretation

可信度：NVIDIA 官方 profiler 文档。  
适用：真实 CUDA kernel Evidence。  
局限：section/metric 名随工具版本与架构变化。

### NVIDIA GPU Performance Background

URL: https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html

用途：
- arithmetic intensity
- math bandwidth vs memory bandwidth
- compute-bound / memory-bound

可信度：NVIDIA 官方。  
适用：AI/GPU performance 基础。  
局限：是性能心智模型，不替代 kernel profiler。

### NVIDIA Matrix Multiplication Background

URL: https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html

用途：
- GEMM tiling
- arithmetic intensity
- tile efficiency vs tile parallelism
- problem-size / tile quantization intuition

可信度：NVIDIA 官方深度学习性能资料。  
适用：理解 GPU GEMM 与 AI workload。  
局限：具体 tile 选择由库、架构、datatype 和 problem shape 决定。

### NVIDIA CUTLASS — Efficient GEMM in CUDA

URL: https://docs.nvidia.com/cutlass/latest/media/docs/cpp/efficient_gemm.html

用途：
- global → shared → register hierarchical tiling
- warp/threadblock/thread GEMM
- register accumulator
- software pipelining / double buffering
- 为什么高性能 GEMM 不追求最高 occupancy

可信度：NVIDIA 官方开源 kernel library 文档。  
适用：高阶 GEMM/kernel 研究。  
局限：实现细节偏 NVIDIA/CUDA；初学阶段只抽稳定心智模型。

### AMD ROCm HIP — Programming model

URL: https://rocm.docs.amd.com/projects/HIP/en/latest/understand/programming_model.html

用途：
- work-item/work-group/wavefront/CU
- registers
- LDS/shared memory
- HBM/global memory
- occupancy / resource pressure

可信度：AMD 官方 ROCm 文档。  
适用：HIP、CDNA/RDNA 的编程模型。  
局限：wave size、CU/WGP/cache 等细节需按目标架构确认。

### AMD ROCm HIP — Performance guidelines

URL: https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html

用途：
- coalescing
- LDS data reuse
- bank conflicts
- register pressure
- occupancy
- memory throughput
- `hipcc --resource-usage`

可信度：AMD 官方性能指南。  
适用：HIP kernel optimization。  
局限：示例不等同于所有架构的最佳 tile/layout。

### AMD ROCm — GPU performance optimization

URL: https://rocm.docs.amd.com/projects/HIP/en/latest/understand/performance_optimization.html

用途：
- Roofline
- arithmetic intensity
- memory-bound / compute-bound
- memory hierarchy
- bank conflict theory
- architecture-sensitive performance analysis

可信度：AMD 官方。  
适用：跨 kernel performance reasoning。  
局限：Roofline 忽略 latency；实际 performance 仍需 profiler。

### ROCm Compute Profiler

URL: https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/how-to/analyze/cli.html

用途：
- per-kernel Roofline
- hierarchical HBM/L2/L1/LDS Roofline
- memory chart
- achieved compute / traffic analysis

可信度：AMD 官方 profiler 文档。  
适用：真实 AMD GPU Evidence。  
局限：CLI 与 metric 名会随 ROCm 版本变化。

### ROCprofiler SDK / rocprofv3

URL: https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/latest/how-to/using-rocprofv3.html

用途：
- kernel/memory trace
- scratch memory trace
- AMD spill/private-memory 观察

可信度：AMD 官方 profiler 文档。  
适用：真实 AMD GPU Evidence。  
局限：CLI 与 metric 名可能随 ROCm 版本变化，实验必须记录版本。

## LLM inference phases

### NVIDIA Dynamo — Disaggregated Serving

URL: https://docs.nvidia.com/dynamo/dev/knowledge-base/concepts/system-architecture/disaggregated-serving

用途：
- prefill vs decode resource characteristics
- prefill compute-bound / decode memory-bound 的稳定系统级抽象
- 为什么不同阶段可采用不同 GPU/parallelism

可信度：NVIDIA 官方 inference framework 文档。  
适用：现代 LLM serving 概念。  
局限：具体 bottleneck 会随 batch/context/model/backend 改变。

### AMD Infera Glossary

URL: https://rocm.docs.amd.com/projects/infera/en/latest/reference/glossary.html

用途：
- AMD 侧 prefill/decode 术语
- decode memory-bandwidth-bound / concurrency 的系统级定义

可信度：AMD 官方。  
适用：跨 NVIDIA/AMD 验证稳定 LLM inference 阶段语言。  
局限：不是 kernel-level benchmark 资料。


## Local LLM memory / KV cache

### Hugging Face Transformers — Caching

URL: https://huggingface.co/docs/transformers/en/cache_explanation

用途：
- KV cache 为什么存在
- K/V tensor shape
- per-layer cache
- sequence growth

可信度：Transformers 官方文档。  
适用：decoder autoregressive inference 的基础 cache 模型。  
局限：具体 backend storage/layout 不一定与 Transformers Python implementation 相同。

### Hugging Face Transformers — Cache strategies

URL: https://huggingface.co/docs/transformers/en/kv_cache

用途：
- Dynamic / Static / Quantized cache
- sliding-window / chunked-attention cache growth
- offload options

可信度：Transformers 官方。  
适用：理解 runtime cache policy 会怎样改变显存。  
局限：cache classes 与支持矩阵会随 Transformers 版本更新。

### Hugging Face — LlamaConfig

URL: https://huggingface.co/docs/transformers/model_doc/llama

用途：
- hidden_size
- num_hidden_layers
- num_attention_heads
- num_key_value_heads
- head_dim
- MHA/GQA/MQA 判定

可信度：Transformers 官方 model config 文档。  
适用：Llama-like architecture preflight。  
局限：不能把 Llama config assumptions 套到所有模型。

### Hugging Face Safetensors — Metadata parsing

URL: https://huggingface.co/docs/safetensors/metadata_parsing

用途：
- 不下载完整 payload 即读取 tensor dtype/shape
- parameter count / dtype mix 调查
- checkpoint payload verification

可信度：Safetensors/Hugging Face 官方。  
适用：模型仓库调查。  
局限：runtime converted weight layout 仍可能不同。

### NVIDIA TensorRT-LLM — Memory Usage

URL: https://nvidia.github.io/TensorRT-LLM/reference/memory.html

用途：
- weights / activations / I/O / KV 的 runtime memory 分类
- paged KV pool
- free-memory fraction / token-budget allocation
- runtime preallocation

可信度：NVIDIA 官方 TensorRT-LLM 文档。  
适用：现实 inference runtime memory policy。  
局限：具体默认值和 runtime implementation 会更新，不能写死到稳定公式。

### NVIDIA TensorRT-LLM — KV cache system

URL: https://nvidia.github.io/TensorRT-LLM/features/kvcache.html

用途：
- block/paged KV
- MHA/MQA/GQA support
- KV cache dtype / windows
- capacity management

可信度：NVIDIA 官方。  
适用：理解 baseline formula 与 runtime block-pool 的差异。  
局限：TensorRT-LLM-specific。

### AMD ROCm Infera — PD disaggregation / KV tiering

URL: https://rocm.docs.amd.com/projects/infera/en/main/features/pd_disaggregation.html

URL: https://rocm.docs.amd.com/projects/infera/en/latest/

用途：
- prefill 构建 KV、decode 使用 KV
- KV GPU-to-GPU transfer
- GPU→RAM/NVMe/network KV tier/offload

可信度：AMD 官方 ROCm inference 文档。  
适用：跨厂商理解 KV 是独立 state/capacity/traffic 对象。  
局限：Infera 是 serving orchestration layer，不给通用模型 KV shape 公式。


## LLM quantization / formats / backend compatibility

### Hugging Face Transformers — Quantization overview

URL: https://huggingface.co/docs/transformers/quantization/overview

用途：
- quantization methods / datatype / bits
- current hardware compatibility matrix
- deployment integration discovery

可信度：Transformers 官方。  
适用：生态入口 + current support discovery。  
局限：compatibility matrix 易变，真实部署必须带查询日期。

### GPTQ paper

URL: https://arxiv.org/abs/2210.17323

用途：GPTQ 是 post-training weight quantization method，而不是 container format。  
可信度：原始论文。  
局限：具体 runtime implementations 已有多个后继项目。

### AWQ paper

URL: https://arxiv.org/abs/2306.00978

用途：activation-aware weight quantization；algorithm vs kernel/packing 分层。  
可信度：原始论文。  
局限：loader/kernel compatibility 需查 current backend。

### llama.cpp — GGUF implementation

URL: https://github.com/ggml-org/llama.cpp/blob/master/ggml/include/gguf.h

用途：GGUF container structure；metadata + typed tensor descriptor + data blob。  
可信度：canonical upstream implementation。  
局限：具体 quant type 与实现动态演进。

### llama.cpp — quantize tool

URL: https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/quantize.cpp

用途：current quant options、mixed/selective tensor quantization、artifact size intuition。  
可信度：canonical upstream source。  
局限：quant list/defaults 动态演进，不能写成永久兼容表。

### ExLlamaV2 — EXL2

URL: https://github.com/turboderp-org/exllamav2

用途：mixed-bit 2–8 bpw representation、target average bitrate、ecosystem/runtime relationship。  
可信度：project upstream。  
局限：platform compatibility 动态变化。

### vLLM — Quantization

URL: https://docs.vllm.ai/en/latest/features/quantization/

用途：backend-specific quant implementations 与 current hardware matrix。  
可信度：vLLM 官方。  
局限：官方明确提示 matrix 会变化。

### vLLM — GGUF

URL: https://docs.vllm.ai/en/latest/features/quantization/gguf/

用途：current vLLM GGUF support state 与 plugin/maturity caveats。  
可信度：vLLM 官方。  
局限：高度动态，不写入稳定 compatibility claims。


## First local LLM deployment — llama.cpp

### llama.cpp README

URL: https://github.com/ggml-org/llama.cpp/blob/master/README.md

用途：
- current project capabilities
- GGUF local/Hugging Face model examples
- CLI/server entry points
- CPU/CUDA/HIP/Metal backend overview
- CPU+GPU hybrid inference

可信度：canonical upstream。  
适用：first local deployment orientation。  
局限：README examples and supported features evolve; pin build commit in Evidence.

### llama.cpp Build

URL: https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md

用途：
- CPU build
- CUDA build
- HIP build
- Metal behavior
- architecture/toolchain options

可信度：canonical upstream。  
适用：reproducible backend build。  
局限：CMake flags/toolchain requirements change over time.

### llama.cpp Models / GGUF

URL: https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md

用途：
- GGUF requirement
- local model loading
- Hugging Face loading path
- conversion boundary

可信度：canonical upstream。  
适用：artifact identity / loading workflow。  
局限：supported architectures and conversion tools evolve.

### llama.cpp CLI

URL: https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md

用途：
- runtime/device discovery
- context
- threads
- GPU-layer offload
- prompt/generation controls
- current auto-fit behavior

可信度：canonical upstream。  
适用：Experiment 10 current commands。  
局限：CLI flags are dynamic; always record `--version` and `--help`.

### llama-bench

URL: https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md

用途：
- pp / tg split
- repetitions
- thread / GPU-layer / context/KV sweeps
- raw JSON reproducibility metadata

可信度：canonical upstream benchmark tool docs。  
适用：backend-level performance Evidence。  
局限：timing excludes tokenization/sampling; not a full serving latency benchmark.


## Local LLM serving / concurrency

### llama.cpp — HTTP Server

URL: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

用途：
- OpenAI-compatible API
- multi-user parallel decoding
- server slots
- continuous/dynamic batching
- streaming
- context/KV/cache settings
- /slots monitoring
- /metrics Prometheus metrics

可信度：canonical upstream。  
适用：llama-server serving model 与真实 Experiment Evidence。  
局限：CLI flags、defaults、metrics/schema 会演进；保存 upstream commit 与 dated intelligence snapshot。

### llama.cpp — Server benchmark

URL: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/bench/README.md

用途：
- concurrent-user load generation
- continuous batching server setup
- OpenAI chat-completion load
- k6 VUs / iterations
- client/server metrics comparison

可信度：canonical upstream benchmark docs。  
适用：从课程 lightweight probe 迁移到更正式 load test。  
局限：需要 k6/xk6-sse 与 dataset；课程第一并发实验不用强制安装。

### llama.cpp — SPEED-Bench server client

URL: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/bench/speed-bench/README.md

用途：
- concurrency
- prompt/decode throughput
- end-to-end latency
- raw JSON output
- long-input throughput splits

可信度：canonical upstream。  
适用：更高阶 serving benchmark 与 speculative-decoding 比较。  
局限：依赖 dataset/Python packages；具体 fields/options 动态演进。


## Prefix / Paged KV cache

### llama.cpp — Server prompt cache / response timings

URL: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

用途：
- prompt cache current controls
- cache reuse
- cache RAM / context checkpoints
- unified KV
- response cache_n / prompt_n / prompt_ms evidence

可信度：canonical upstream。  
适用：real llama-server cold/warm prefix Evidence。  
局限：flags/defaults/cache implementation dynamically evolve; pin commit/version.

### vLLM — Automatic Prefix Caching

URL: https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html

用途：
- shared-prefix KV reuse
- long-document / multi-round use cases
- prefill-only optimization boundary

可信度：vLLM official docs。  
适用：stable prefix-caching concept。  
局限：vLLM-specific API/implementation details evolve.

### vLLM — Prefix Caching design

URL: https://docs.vllm.ai/en/latest/design/prefix_caching/

用途：
- KV block pool
- prefix hash
- finite cache
- eviction
- current cache-salt isolation

可信度：vLLM official design docs。  
适用：paged/block cache internals and isolation reasoning。  
局限：current implementation details must not be generalized to all runtimes.

### NVIDIA TensorRT-LLM — KV cache reuse

URL: https://nvidia.github.io/TensorRT-LLM/advanced/kv-cache-reuse.html

用途：
- reusable prompt KV pages
- first-token latency effect
- system-prompt / multi-turn reuse
- eviction
- concurrent warm-up timing caveat

可信度：NVIDIA official TensorRT-LLM docs。  
适用：cross-backend validation of prefix-reuse concepts。  
局限：TensorRT-LLM-specific policy and interfaces change.

### NVIDIA TensorRT-LLM — KV Cache System

URL: https://nvidia.github.io/TensorRT-LLM/features/kvcache.html

用途：
- finite KV block pool
- allocation/reuse/offload/eviction
- paged/block memory-management mental model

可信度：NVIDIA official。  
适用：paged KV architecture reasoning。  
局限：do not equate its blocks with llama.cpp unified-KV internals.


## Speculative decoding

### Leviathan et al. — Fast Inference from Transformers via Speculative Decoding

URL: https://arxiv.org/abs/2211.17192

用途：
- original speculative-decoding algorithm
- serial target-step problem
- exact/target-distribution-preserving verification idea
- speedup dependence on approximation quality/cost

可信度：original research paper。  
适用：stable algorithmic foundation。  
局限：paper benchmarks do not predict current local-runtime speedups.

### Chen et al. — Accelerating Large Language Model Decoding with Speculative Sampling

URL: https://arxiv.org/abs/2302.01318

用途：
- draft continuation + target parallel scoring
- modified rejection sampling
- target-distribution preservation
- verification batching motivation

可信度：original research paper。  
适用：stochastic speculative-sampling correctness model。  
局限：hardware/results are historical examples, not current benchmark claims.

### llama.cpp — Speculative Decoding

URL: https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md

用途：
- current draft / n-gram / learned proposer implementations
- acceptance statistics
- current draft controls
- benchmark path

可信度：canonical upstream。  
适用：real llama.cpp speculative Evidence。  
局限：method list/flags/defaults change rapidly; pin commit/version.

### llama.cpp — SPEED-Bench server benchmark

URL: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/bench/speed-bench/README.md

用途：
- speculative baseline vs spec comparison
- acceptance rate
- prompt/decode throughput
- latency
- raw JSON

可信度：canonical upstream benchmark docs。  
适用：post-smoke-test serving benchmark。  
局限：dataset/client dependencies and exact interfaces evolve.

### vLLM — Speculative Decoding

URL: https://docs.vllm.ai/en/latest/features/speculative_decoding/

用途：
- current proposer methods
- low/medium-QPS use case
- memory-bound decode motivation
- lossless verifier/rejection-sampler framing

可信度：vLLM official docs。  
适用：cross-runtime stable concept validation + dynamic compatibility。  
局限：implementation/version compatibility belongs in intelligence.

### vLLM Speculators — Algorithms

URL: https://docs.vllm.ai/projects/speculators/en/latest/user_guide/algorithms/

用途：
- EAGLE/P-EAGLE/DFlash/DSpark/MTP proposer evolution
- target-aware/non-standalone proposer examples

可信度：vLLM project official docs。  
适用：advanced proposer taxonomy。  
局限：rapidly evolving research/runtime integration.

### NVIDIA TensorRT-LLM — Speculative Decoding

URL: https://nvidia.github.io/TensorRT-LLM/1.3.0rc20/features/speculative-decoding.html

用途：
- proposal + target single-forward verification
- low-batch speedup emphasis
- draft/target compatibility requirements

可信度：NVIDIA official TensorRT-LLM docs。  
适用：cross-backend system validation。  
局限：versioned implementation details evolve rapidly.
