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


## Multi-GPU / interconnect

### NVIDIA NCCL — GPU troubleshooting / P2P

URL: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/gpu_troubleshooting.html

用途：
- current GPU Direct / P2P sanity model
- `nvidia-smi topo -p2p p` PCIe P2P capability
- `nvidia-smi topo -p2p n` NVLink P2P capability
- topology/configuration failure modes

可信度：NVIDIA official NCCL docs。
适用：dynamic NVIDIA multi-GPU investigation。
局限：P2P status is not measured bandwidth.

### NVIDIA NCCL — Performance and tuning

URL: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/performance_and_tuning.html

用途：
- `nvidia-smi topo -m`
- `nvbandwidth`
- pairwise GPU↔GPU bandwidth validation

可信度：NVIDIA official。
适用：topology + peer-bandwidth Evidence。
局限：collective/application performance still needs workload benchmark.

### AMD HIP — Multi-device management

URL: https://rocm.docs.amd.com/projects/HIP/en/develop/how-to/hip_runtime_api/multi_device.html

用途：
- GPU P2P direct peer memory access
- host staging fallback without activated P2P
- cross-vendor validation of communication-path cost

可信度：AMD ROCm official。
适用：stable P2P reasoning + current HIP behavior。
局限：exact platform support still hardware/runtime dependent.

### AMD TransferBench — presets

URL: https://rocm.docs.amd.com/projects/TransferBench/en/docs-1.66.02/reference/presets.html

用途：
- current `p2p` preset
- GPU↔GPU uni/bidirectional bandwidth
- CPU NUMA ↔ GPU transfer matrix

可信度：AMD ROCm official。
适用：real AMD peer-bandwidth Evidence。
局限：tool versions/options evolve.

### llama.cpp — llama-bench

URL: https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md

用途：
- current split modes
- device/tensor split controls
- PP vs TG benchmark
- JSON raw output

可信度：canonical upstream。
适用：real local-LLM multi-GPU A/B。
局限：flags, separators and experimental modes are dynamic; pin exact build.


## Attention IO / FlashAttention

### FlashAttention paper

URL: https://arxiv.org/abs/2205.14135

用途：
- IO-aware exact attention
- HBM↔SRAM data movement
- tiling
- IO complexity

可信度：original paper。
适用：stable algorithmic foundation。
局限：historical benchmark numbers are not current GPU claims.

### FlashAttention-2

URL: https://arxiv.org/abs/2307.08691

用途：
- block parallelism
- warp work partition
- non-matmul FLOPs
- shared-memory communication

可信度：original paper。
适用：GPU scheduling bridge。
局限：paper hardware/results are historical.

### PyTorch — scaled_dot_product_attention

URL: https://docs.pytorch.org/docs/main/generated/torch.nn.functional.scaled_dot_product_attention.html

用途：
- current SDPA implementations
- auto backend selection
- current fused-kernel limitations

可信度：PyTorch official。
适用：real GPU backend probe。
局限：API/dispatch changes.

### PyTorch — sdpa_kernel

URL: https://docs.pytorch.org/docs/main/generated/torch.nn.attention.sdpa_kernel.html

用途：
- force/select SDPA backend
- reproduce math vs fused comparison

可信度：PyTorch official。
适用：Experiment 20。
局限：currently beta.

### NVIDIA Transformer Engine — Attention

URL: https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/attention/attention.html

用途：
- tiling
- recomputation vs global-memory traffic
- current NVIDIA flash/cudnn attention context

可信度：NVIDIA official。
适用：cross-check IO-aware explanation。
局限：implementation-specific details are dynamic.

### AMD ROCm Composable Kernel

URL: https://rocm.docs.amd.com/projects/composable_kernel/en/develop/

用途：
- AMD optimized kernel ecosystem
- FlashAttention GPU implementation context
- block/warp-style scheduling concepts on AMD

可信度：AMD ROCm official。
适用：AMD migration/intelligence。
局限：hardware/version support must be checked separately.


## Matrix units / precision

### NVIDIA Ampere Tuning Guide

URL: https://docs.nvidia.com/cuda/ampere-tuning-guide/

用途：
- Volta/Turing/Ampere Tensor Core evolution
- BF16/TF32/FP64 additions
- input/accumulator type mapping

可信度：NVIDIA official。
适用：stable generation bridge。
局限：exact SKU peak is separate.

### CUDA Programming Guide — WMMA / alternate floating point

URL: https://docs.nvidia.com/cuda/cuda-programming-guide/

用途：
- BF16
- TF32
- accumulator semantics
- matrix fragment model

可信度：NVIDIA official。
适用：stable precision semantics。
局限：API details evolve.

### NVIDIA Transformer Engine

URL: https://docs.nvidia.com/deeplearning/transformer-engine/

用途：
- FP8
- scaling/amax
- Hopper/Ada/Blackwell
- MXFP8/NVFP4 current modes

可信度：NVIDIA official。
适用：current low-precision intelligence。
局限：TE-specific runtime details are dynamic.

### AMD HIP — Hardware implementation

URL: https://rocm.docs.amd.com/projects/HIP/en/latest/understand/hardware_implementation.html

用途：
- MFMA
- matrix core mental model
- FP16→FP32 accumulation example

可信度：AMD ROCm official。
适用：AMD stable mapping。
局限：current exact architecture support is separate.

### ROCm — Data types and precision support

URL: https://rocm.docs.amd.com/en/latest/reference/precision-support.html

用途：
- CDNA/RDNA matrix-core datatype matrix
- generation-specific FP8/FP16/BF16/INT8 support

可信度：AMD official。
适用：dynamic compatibility intelligence。
局限：must revalidate as ROCm docs evolve.

### PyTorch — float32 matmul precision

URL: https://docs.pytorch.org/docs/main/generated/torch.set_float32_matmul_precision.html

用途：
- TF32/internal precision distinction
- real GEMM probe control

可信度：PyTorch official。
适用：Experiment 22。
局限：backend-specific dynamic behavior.


## NVIDIA architecture generations

### NVIDIA architecture timeline
URL: https://www.nvidia.com/en-us/technologies/
用途：official Tesla→Blackwell chronology and family naming.
可信度：NVIDIA official。

### NVIDIA Research — Tesla unified architecture
URL: https://research.nvidia.com/publication/2008-04_nvidia-tesla-unified-graphics-and-computing-architecture
用途：unified programmable processor, massively multithreaded CUDA-era foundation.
可信度：NVIDIA Research / IEEE publication。

### NVIDIA Fermi Compute Architecture
URL: https://www.nvidia.com/content/PDF/fermi_white_papers/NVIDIA_Fermi_Compute_architecture_Whitepaper.pdf
用途：G80/GT200 bridge, Fermi SM/cache/L2/FMA/HPC changes.
可信度：NVIDIA official whitepaper。

### Kepler Tuning Guide
URL: https://docs.nvidia.com/cuda/kepler-tuning-guide/
用途：SMX, TLP/ILP, Hyper-Q, Dynamic Parallelism, warp shuffle.
可信度：NVIDIA official CUDA docs。
局限：GK110-specific features must be labeled.

### Maxwell Tuning Guide
URL: https://docs.nvidia.com/cuda/maxwell-tuning-guide/
用途：SMM partitioning, shared-memory/L1 changes, occupancy, shared atomics.
可信度：NVIDIA official。

### Pascal Tuning Guide
URL: https://docs.nvidia.com/cuda/pascal-tuning-guide/
用途：GP100 vs GP104, FP16/INT8 differences, HBM2, NVLink, Unified Memory.
可信度：NVIDIA official。
关键：architecture-family variation.

### Volta Tuning Guide
URL: https://docs.nvidia.com/cuda/volta-tuning-guide/
用途：Tensor Cores, Independent Thread Scheduling, unified L1/shared, warp synchronization.
可信度：NVIDIA official。

### Turing Tuning Guide
URL: https://docs.nvidia.com/cuda/turing-tuning-guide/
用途：concurrent FP32/INT32, Independent Thread Scheduling, Tensor inference modes, unified L1/shared.
可信度：NVIDIA official。

### Ampere Tuning Guide
URL: https://docs.nvidia.com/cuda/ampere-tuning-guide/
用途：BF16/TF32, async global→shared, split barriers, L2 residency, cc8.0 vs 8.6.
可信度：NVIDIA official。

### NVIDIA Ada Lovelace architecture
URL: https://www.nvidia.com/en-us/geforce/ada-lovelace-architecture/
Whitepaper: https://images.nvidia.com/aem-dam/Solutions/geforce/ada/nvidia-ada-gpu-architecture.pdf
用途：4th-gen Tensor, FP8-era RTX, SER, AD102 large L2, AV1.
可信度：NVIDIA official。
局限：full AD102 numbers are not every Ada SKU.

### NVIDIA Hopper architecture
URL: https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/
用途：FP8/Transformer Engine, TMA, block clusters, 4th-gen Tensor.
可信度：NVIDIA official technical blog。

### NVIDIA RTX Blackwell whitepaper
URL: https://images.nvidia.com/aem-dam/Solutions/geforce/blackwell/nvidia-rtx-blackwell-gpu-architecture.pdf
用途：RTX Blackwell SM, 5th-gen Tensor, FP4, GDDR7; distinguish RTX from datacenter Blackwell.
可信度：NVIDIA official。

### Current CUDA architecture matrix
URL: https://docs.nvidia.com/datacenter/tesla/drivers/cuda-toolkit-driver-and-architecture-matrix.html
用途：compute capability, first/last CUDA toolkit, last/current driver branch.
可信度：NVIDIA official current docs。
适用：dynamic used-GPU software-lifetime intelligence.

### CUDA release notes
URL: https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/
用途：current architecture deprecation/removal status, including CUDA 13 Maxwell/Pascal/Volta cutoff.
可信度：NVIDIA official。


## AMD architecture generations

### AMD ROCm GPU architecture documentation
URL: https://rocm.docs.amd.com/en/latest/reference/gpu-arch/index.html
用途：canonical index for CDNA1-4, RDNA1-4, Vega/GCN architecture documents.
可信度：AMD ROCm official。

### HIP hardware implementation
URL: https://rocm.docs.amd.com/projects/HIP/en/latest/understand/hardware_implementation.html
用途：wavefront, CU/WGP, LDS, VALU, MFMA Matrix Core, cache hierarchy.
可信度：AMD ROCm official。

### AMD GPUOpen — GCN occupancy/resource article
URL: https://gpuopen.com/learn/optimizing-gpu-occupancy-resource-usage-large-thread-groups/
用途：classic GCN CU, Wave64, SIMD, SGPR/VGPR, LDS, occupancy.
可信度：AMD GPUOpen official。

### AMD GPUOpen — GCN cross-lane operations
URL: https://gpuopen.com/learn/amd-gcn-assembly-cross-lane-operations/
用途：Wave64, SIMD16 row execution, lane communication, LDS/DPP.
可信度：AMD GPUOpen official。

### AMD RDNA architecture / ISA
URL: https://gpuopen.com/rdna/
URL: https://docs.amd.com/v/u/en-US/rdna-shader-instruction-set-architecture
用途：Wave32/Wave64, WGP, RDNA execution changes.
可信度：AMD official/GPUOpen。

### AMD RDNA family page
URL: https://www.amd.com/en/technologies/rdna.html
用途：RDNA1-4 generation features, Infinity Cache, AI accelerator generations.
可信度：AMD official。
局限：marketing performance claims are not course benchmarks.

### AMD RDNA3 ISA
URL: https://docs.amd.com/v/u/en-US/rdna3-shader-instruction-set-architecture-feb-2023_0
用途：VOPD dual issue and constraints.
可信度：AMD official ISA。

### AMD RDNA4 ISA
URL: https://docs.amd.com/v/u/en-US/rdna4-instruction-set-architecture
用途：Wave32/Wave64, current instruction behavior.
可信度：AMD official ISA。

### AMD Vega launch / architecture features
URL: https://ir.amd.com/news-events/press-releases/detail/782/amd-redefines-the-enthusiast-gaming-experience-with-radeon-rx-vega-and-radeon-packs
用途：Rapid Packed Math, HBM2, High Bandwidth Cache Controller.
可信度：AMD official historical material。

### AMD CDNA whitepaper
URL: https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/white-papers/amd-cdna-white-paper.pdf
用途：MI100, Matrix Core, HBM2, Infinity Fabric, dedicated compute branch.
可信度：AMD official whitepaper。

### AMD CDNA2 whitepaper
URL: https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/white-papers/amd-cdna2-white-paper.pdf
用途：matrix FP64, BF16/FP16, multi-die, HBM2e, Infinity Fabric.
可信度：AMD official whitepaper。

### AMD CDNA3 whitepaper
URL: https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/white-papers/amd-cdna-3-white-paper.pdf
用途：XCD/IOD, HBM3, FP8, Infinity Cache, MI300A/MI300X.
可信度：AMD official whitepaper。

### AMD CDNA current architecture page
URL: https://www.amd.com/en/technologies/cdna.html
用途：CDNA1-5 current family, MI350/CDNA4 and MI400/CDNA5 frontier.
可信度：AMD official。
局限：current product/software details must be separated from stable architecture.

### ROCm 7.14 release notes / hardware support
URL: https://rocm.docs.amd.com/en/latest/about/release-notes.html
用途：current supported gfx targets/SKUs, known issues including current LLM inference issues.
可信度：AMD ROCm official current docs。

### ROCm 7.14 compatibility matrix
URL: https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html
用途：exact architecture/gfx target/OS support.
可信度：AMD ROCm official current docs。

### AMD GPU specifications
URL: https://rocm.docs.amd.com/en/latest/reference/gpu-specs.html
用途：current VRAM/CU/wavefront/LDS/cache/gfx-target inventory.
可信度：AMD ROCm official current docs。

### AMD SMI CLI
URL: https://rocm.docs.amd.com/projects/amdsmi/en/latest/how-to/amdsmi-cli-tool.html
用途：current amd-smi version/list/static/topology/xgmi interfaces.
可信度：AMD ROCm official current docs。


## Apple Silicon / Metal / MLX

### Apple M1
URL: https://www.apple.com/newsroom/2020/11/apple-unleashes-m1/
用途：Apple-Silicon Mac SoC baseline, Unified Memory Architecture.
可信度：Apple official historical source。

### Apple M2
URL: https://www.apple.com/newsroom/2022/06/apple-unveils-m2-with-breakthrough-performance-and-capabilities/
用途：M2 scale-up, official unified-memory bandwidth/capacity example.
可信度：Apple official。
局限：product numbers are dynamic, not stable architecture constants.

### Apple M3 family
URL: https://www.apple.com/newsroom/2023/10/apple-unveils-m3-m3-pro-and-m3-max-the-most-advanced-chips-for-a-personal-computer/
用途：new GPU architecture, Dynamic Caching, hardware ray tracing/mesh shading.
可信度：Apple official。

### Apple M4
URL: https://www.apple.com/newsroom/2024/05/apple-introduces-m4-chip/
用途：M4 continues M3 GPU architecture, stronger Neural Engine/memory system.
可信度：Apple official。

### Apple M5
URL: https://www.apple.com/newsroom/2025/10/apple-unleashes-m5-the-next-big-leap-in-ai-performance-for-apple-silicon/
用途：GPU Neural Accelerator per core, Metal 4 Tensor APIs, 2nd-gen Dynamic Caching, separate Neural Engine.
可信度：Apple official。

### M5 Pro / M5 Max
URL: https://www.apple.com/newsroom/2026/03/apple-introduces-macbook-pro-with-all-new-m5-pro-and-m5-max/
用途：current Fusion Architecture, exact current memory capacity/bandwidth tiers.
可信度：Apple official current product source。
局限：do not generalize package/product numbers.

### Metal storage modes
URL: https://developer.apple.com/documentation/metal/setting-resource-storage-modes
用途：Apple-Silicon shared default, private/shared semantics, synchronization.
可信度：Apple Developer official。

### Metal unified-memory properties
URL: https://developer.apple.com/documentation/metal/mtldevice/hasunifiedmemory
URL: https://developer.apple.com/documentation/metal/mtldevice/recommendedmaxworkingsetsize
用途：real device unified-memory Evidence and recommended working-set budget.
可信度：Apple Developer official。

### Metal threads / SIMD groups
URL: https://developer.apple.com/documentation/metal/creating-threads-and-threadgroups
URL: https://developer.apple.com/documentation/apple-silicon/porting-your-metal-code-to-apple-silicon
用途：threadgroup/SIMD group, divergence, runtime threadExecutionWidth.
可信度：Apple Developer official。

### Core ML compute units
URL: https://developer.apple.com/documentation/coreml/mlcomputeunits
用途：CPU/GPU/Neural Engine are distinct selectable compute-unit paths.
可信度：Apple Developer official。

### MLX
URL: https://ml-explore.github.io/mlx/
URL: https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html
用途：Apple-Silicon unified-memory CPU/GPU framework model.
可信度：Apple ML Research project docs。

### Metal Performance Primitives / Tensor APIs
URL: https://developer.apple.com/download/files/Metal-Performance-Primitives-Programming-Guide.pdf
URL: https://developer.apple.com/documentation/metal/running-inline-ml-operations-in-a-shader-with-metal-4
用途：M5 GPU Neural Accelerators, Metal 4 tensor resources/operations.
可信度：Apple Developer official current docs。

### llama.cpp M5 Metal tensor issue
URL: https://github.com/ggml-org/llama.cpp/issues/27473
Related PR: https://github.com/ggml-org/llama.cpp/pull/27461
用途：current backend-integration case study: hardware capability != runtime readiness.
可信度：canonical llama.cpp upstream issue/PR。
局限：open/unconfirmed and rapidly changing; intelligence only.


## Intel Xe / Arc / oneAPI

### Intel Xe GPU Architecture
URL: https://www.intel.com/content/www/us/en/docs/oneapi/optimization-guide-gpu/latest/intel-xe-gpu-architecture.html
用途：Vector Engine, Xe-Core, XMX, SLM, current Arc A/B and integrated Xe tables.
可信度：Intel official optimization guide。

### Intel Xe-HPG architecture
URL: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-xe-hpg-architecture.html
用途：Alchemist/Xe-HPG, XMX/DPAS matrix path.
可信度：Intel official。

### Intel oneAPI Toolkit
URL: https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneapi-toolkit.html
Release notes: https://www.intel.com/content/www/us/en/developer/articles/release-notes/oneapi-toolkit/2026.html
用途：current oneAPI/SYCL compiler/libraries/GPU support.
可信度：Intel official current docs。

### Intel Level Zero backend
URL: https://www.intel.com/content/www/us/en/docs/dpcpp-cpp-compiler/developer-guide-reference/latest/programming-with-intel-oneapi-level-zero-backend.html
用途：device discovery, Level Zero backend, sycl-ls, multi-device.
可信度：Intel official。

### PyTorch XPU
URL: https://docs.pytorch.org/docs/stable/xpu.html
Getting started: https://docs.pytorch.org/docs/stable/notes/get_start_xpu.html
用途：current torch.xpu API and validated Intel GPU families.
可信度：PyTorch official current docs。

### llama.cpp SYCL backend
URL: https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/SYCL.md
用途：current Intel-oriented SYCL backend, oneDNN/oneMKL/FA, Arc A/B support, current issues.
可信度：canonical upstream。
局限：rapidly changing; pin exact commit.

### Intel Arc B-Series
URL: https://www.intel.com/content/www/us/en/ark/products/series/240391/intel-arc-b-series-graphics.html
用途：current B570/B580 Xe2 product facts.
可信度：Intel official current product database。

### Intel Arc Pro B-Series
URL: https://www.intel.com/content/www/us/en/ark/products/series/242616/intel-arc-pro-b-series-graphics.html
用途：current 2026 workstation Xe2/32GB options.
可信度：Intel official current product database。


## China secondhand GPU market

### Xianyu inspection-service buyer agreement
URL: https://terms.alicdn.com/legal-agreement/terms/product/20221213134628952/20221213134628952.html
用途：third-party inspection transaction flow, scope limits, buyer decision/return rules.
可信度：official published Xianyu/Alibaba agreement。
局限：inspection scope is category/service specific; not a GPU engineering test specification.

### Xianyu community user agreement
URL: https://terms.alicdn.com/legal-agreement/terms/suit_bu1_other/suit_bu1_other201708081618_51146.html
用途：current platform agreement context.
可信度：official current agreement。

### August 2026 secondhand GPU market video
URL: https://www.bilibili.com/video/BV1Q5GV6WEeP/
用途：current Chinese secondhand-GPU market direction and recurring monthly observation.
可信度：community secondary。
局限：raw normalized item-level dataset not exposed in searchable page.

### Mid-August 2026 market update
URL: https://www.bilibili.com/video/BV1XgbD6zEYR
用途：mid-month 黄鱼行情 direction.
可信度：community secondary。
局限：not direct sold-price evidence.

### August local-AI / used-GPU price summary
URL: https://post.smzdm.com/p/a825vp66/
用途：current secondary price signals for 3060/4060Ti16/5060Ti16/3090/4090/5090.
可信度：secondary market summary。
局限：underlying item-level transaction dataset unavailable; grade M1.

### Intel Arc August used-price summary
URL: https://post.smzdm.com/p/agg4xrq3/
用途：current A770/B570/B580 secondary ranges and buyer-risk discussion.
可信度：secondary current article。
局限：not direct normalized platform dataset.

### A770 local-AI demand article
URL: https://post.smzdm.com/p/axklwq32/
用途：current A770 16G demand/price movement signal.
可信度：secondary current article。

### China AI hardware merchant market
URL: https://www.cplight.com/
Data-center GPU category:
https://www.cplight.com/category/data-center-gpu-tesla
用途：current merchant quotes for dismantled/datacenter/workstation GPUs.
可信度：direct merchant quote source。
局限：MERCHANT-QUOTE only; not peer-to-peer sold market.

### Multi-SKU price-trap example
URL: https://www.xing73.com/taobao-xl-AM5AzMh2Y5_ip5Lmo5MqL5.html
用途：demonstrate why teaser/multi-SKU display prices must be rejected from exact-model samples.
可信度：secondary aggregation。
局限：do not use as fair-value data.


## Used GPU acceptance testing

### NVIDIA DCGM Diagnostics
URL: https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html
Command reference:
https://docs.nvidia.com/datacenter/dcgm/latest/reference/command-line-reference/dcgmi/dcgmi-diag.html
用途：official supported GPU diagnostics, memory/PCIe/compute/stress suites.
可信度：NVIDIA official current docs。
局限：plugin/suite availability depends on GPU class/product.

### NVIDIA DCGM GPU Memory Plugin
URL: https://docs.nvidia.com/datacenter/dcgm/latest/reference/diagnostics/plugins/memory.html
用途：framebuffer write/read pattern integrity test and ECC conditions.
可信度：NVIDIA official current docs。

### AMD SMI RAS
URL: https://rocmdocs.amd.com/projects/amdsmi/en/latest/conceptual/ras.html
用途：ECC/RAS/CPER concepts and error-counter interpretation on supported AMD GPUs.
可信度：AMD official current docs。

### memtest_vulkan
URL: https://github.com/GpuZelenograd/memtest_vulkan
用途：optional cross-vendor Vulkan GPU memory test.
可信度：open-source project / community tool。
局限：not vendor certification; exact tested allocation and driver limitations must be recorded.


## Transformer / modern decoder architecture

### Attention Is All You Need
URL: https://arxiv.org/abs/1706.03762
用途：Transformer foundation, multi-head attention, feed-forward sublayers, residual/normalization.
可信度：original research paper。
局限：original encoder-decoder architecture is not identical to modern decoder-only LLM blocks.

### LLaMA
URL: https://arxiv.org/abs/2302.13971
用途：modern decoder-only example; pre-normalization, RMSNorm, SwiGLU, RoPE.
可信度：primary model paper。

### Llama 2
URL: https://arxiv.org/abs/2307.09288
用途：modern autoregressive Transformer lineage and GQA inference-scalability example.
可信度：primary model paper。

### The Llama 3 Herd of Models
URL: https://arxiv.org/abs/2407.21783
用途：large modern dense decoder-only model family; current architecture comparison context.
可信度：primary model paper。


### RMSNorm paper
URL: https://arxiv.org/abs/1910.07467
用途：RMS-based normalization, no explicit recentering, rescaling invariance.
可信度：original research paper。

### RoFormer / RoPE
URL: https://arxiv.org/abs/2104.09864
用途：rotary position embedding, paired rotations and relative-position attention structure.
可信度：original research paper。


### Multi-Query Attention — Fast Transformer Decoding
URL: https://arxiv.org/abs/1911.02150
用途：shared K/V heads, incremental-decoding KV memory-bandwidth motivation.
可信度：original research paper。

### Grouped-Query Attention
URL: https://arxiv.org/abs/2305.13245
用途：GQA as intermediate KV-head grouping between MHA and MQA.
可信度：original research paper。


### GLU Variants Improve Transformer
URL: https://arxiv.org/abs/2002.05202
用途：GLU/SwiGLU gated feed-forward structure and parameter-budget comparison.
可信度：original research paper。


### Switch Transformers
URL: https://arxiv.org/abs/2101.03961
用途：sparse expert routing, top-1 Switch routing, load balancing and communication concerns.
可信度：original research paper。

### Mixtral of Experts
URL: https://arxiv.org/abs/2401.04088
用途：decoder-only 8-expert/top-2 MoE example and active-vs-total parameter distinction.
可信度：primary model paper。

### DeepSeekMoE
URL: https://arxiv.org/abs/2401.06066
用途：fine-grained routed experts and shared-expert architecture.
可信度：primary research/model paper。

### DeepSeek-V3 Technical Report
URL: https://arxiv.org/abs/2412.19437
用途：modern large-MoE example; 671B total / 37B activated parameter accounting context.
可信度：primary technical report。


### Mistral 7B
URL: https://arxiv.org/abs/2310.06825
用途：Grouped-Query Attention + Sliding Window Attention model example.
可信度：primary model paper。

### Gemma 2
URL: https://arxiv.org/abs/2408.00118
用途：interleaved local-global attention hybrid example.
可信度：primary model report。

### DeepSeek-V2
URL: https://arxiv.org/abs/2405.04434
用途：Multi-head Latent Attention / compressed KV and DeepSeekMoE.
可信度：primary technical report。


### Hugging Face chat templates
URL: https://huggingface.co/docs/transformers/chat_templating_writing
用途：current Jinja chat-template model interface, special tokens and generation-prompt behavior.
可信度：official current Transformers documentation。

### Hugging Face chat template basics
URL: https://huggingface.co/docs/transformers/main/en/chat_template_basics
用途：template application/tokenization workflow and duplicate-special-token warning.
可信度：official current Transformers documentation。


### llama.cpp Perplexity
URL: https://github.com/ggml-org/llama.cpp/blob/d7a2074112d27649303fa107eb8c94db1ee435f3/tools/perplexity/README.md
用途：current pinned perplexity semantics, quantization-quality workflow, optional KL/logit comparison and comparability warnings.
可信度：pinned upstream official repository documentation。

### llama.cpp simple perplexity helper
URL: https://github.com/ggml-org/llama.cpp/blob/d7a2074112d27649303fa107eb8c94db1ee435f3/examples/model-conversion/scripts/utils/perplexity-run-simple.sh
用途：current pinned command path for `llama-perplexity -m MODEL -f CORPUS`.
可信度：pinned upstream official repository script。


### llama.cpp server metrics / benchmark
URL: https://github.com/ggml-org/llama.cpp/blob/d7a2074112d27649303fa107eb8c94db1ee435f3/tools/server/README.md
用途：pinned llama-server slots, continuous batching, metrics endpoint and current server options.
可信度：pinned upstream official repository documentation。

### llama.cpp server benchmark
URL: https://github.com/ggml-org/llama.cpp/blob/d7a2074112d27649303fa107eb8c94db1ee435f3/tools/server/bench/README.md
用途：pinned concurrent serving benchmark workflow, request-count/concurrency/prompt-output controls.
可信度：pinned upstream official repository documentation。

### llama.cpp server metrics tests
URL: https://github.com/ggml-org/llama.cpp/blob/d7a2074112d27649303fa107eb8c94db1ee435f3/tools/server/tests/unit/test_metrics.py
用途：pinned tests for Prometheus metrics including cached-vs-processed prompt token accounting.
可信度：pinned upstream official test source。


### Little's Law original proof
URL: https://doi.org/10.1287/opre.9.3.383
用途：original 1961 proof of the queueing relation L = λW and formal conditions.
可信度：original peer-reviewed paper。

### Little's Law 50-year retrospective
URL: https://doi.org/10.1287/opre.1110.0940
用途：historical/practical context and broader use of Little's Law.
可信度：author retrospective in Operations Research。


### llama.cpp health readiness
URL: https://github.com/ggml-org/llama.cpp/blob/d7a2074112d27649303fa107eb8c94db1ee435f3/tools/server/README.md
用途：pinned /health 503-loading vs 200-ready semantics and public endpoint behavior.
可信度：pinned upstream official repository documentation。


### Google SRE four golden signals
URL: https://sre.google/sre-book/monitoring-distributed-systems/
用途：latency / traffic / errors / saturation monitoring framework and tail/saturation reasoning.
可信度：official Google SRE book。

### Google SRE Monitoring workbook
URL: https://sre.google/workbook/monitoring/
用途：metrics/logging, monitoring use cases and actionable service-health diagnosis.
可信度：official Google SRE workbook。


### NVIDIA GPU telemetry / power monitoring
URL: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
用途：NVIDIA management/monitoring capabilities including utilization, clocks, temperature and board power where reported.
可信度：official NVIDIA CUDA documentation。

### NVIDIA performance monitoring
URL: https://docs.nvidia.com/vgpu/latest/grid-vgpu-user-guide/performance-monitoring-gpu.html
用途：current nvidia-smi monitoring examples and GPU state/usage context.
可信度：official NVIDIA documentation。


### Linux page cache
URL: https://www.kernel.org/doc/html/v6.9/mm/page_cache.html
用途：normal filesystem reads/writes/mmaps and the Linux page-cache path.
可信度：official Linux kernel documentation。

### Linux memory-management concepts — page cache
URL: https://www.kernel.org/doc/html/v5.17/admin-guide/mm/concepts.html
用途：page-cache motivation and repeated file access avoiding expensive backing-storage reads.
可信度：official Linux kernel documentation。

### Linux mmap(2)
URL: https://man7.org/linux/man-pages/man2/mmap.2.html
用途：file-backed virtual-memory mapping and page-fault/prefault concepts.
可信度：Linux man-pages documentation。

### util-linux fincore
URL: https://man7.org/linux/man-pages/man1/fincore.1.html
用途：file-page residency evidence using cachestat/mincore where supported.
可信度：util-linux upstream manual page。

### llama.cpp pinned load-mode
URL: https://github.com/ggml-org/llama.cpp/blob/d7a2074112d27649303fa107eb8c94db1ee435f3/tools/server/README.md
用途：dated load-mode auto/none/mmap/mlock/mmap+mlock/dio CLI snapshot.
可信度：pinned upstream repository documentation。


### Linux /proc/meminfo
URL: https://man7.org/linux/man-pages/man5/proc_meminfo.5.html
用途：MemFree, MemAvailable, Cached, swap and system-memory field semantics.
可信度：Linux man-pages documentation。

### Linux /proc/vmstat
URL: https://man7.org/linux/man-pages/man5/proc_vmstat.5.html
用途：cumulative pswpin/pswpout/pgmajfault/workingset counters for window-delta analysis.
可信度：Linux man-pages documentation。

### Linux OOM handling
URL: https://www.kernel.org/doc/html/v6.0/mm/oom.html
用途：kernel out-of-memory handling boundary.
可信度：official Linux kernel documentation。

### Linux VM sysctl / OOM policy
URL: https://cdn.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html
用途：OOM/paging policy context; course uses as reference only, not a tuning recipe.
可信度：official Linux kernel documentation。
