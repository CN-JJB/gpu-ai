# Research Note 0003 — 第一次可解释的本地 LLM：llama.cpp / GGUF / CPU-GPU Offload / Benchmark

日期：2026-08-26

## Research question

怎样让没有 CUDA/Python/ML 前置的学习者完成第一次真实本地 LLM 运行，同时不是“复制一条命令看到聊天框”就算结束？

需要建立最小可迁移部署模型：

```text
backend build
→ device discovery
→ model artifact identity
→ model load
→ context/KV settings
→ CPU/GPU offload
→ first generation
→ pp/tg benchmark
→ reproducible Evidence
```

## Why llama.cpp is the first deployment path

不是因为 llama.cpp 是唯一或永远最好的 backend。

而是因为 current upstream 同时覆盖：
- CPU
- NVIDIA CUDA
- AMD HIP
- Apple Metal
- Vulkan / SYCL 等
- GGUF model artifacts
- CPU+GPU hybrid offload
- CLI / server / benchmark tools

这让同一个课程实验可以从无独显迁移到 NVIDIA/AMD/Apple，而不必每个平台重写整个教学模型。

## Primary sources

### 1. llama.cpp README

https://github.com/ggml-org/llama.cpp/blob/master/README.md

支撑：
- local GGUF `llama-cli -m ...`
- Hugging Face direct model path `-hf`
- OpenAI-compatible `llama-server`
- CPU / CUDA / HIP / Metal 等 backends
- CPU+GPU hybrid inference

### 2. llama.cpp build docs

https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md

支撑 current build paths：

**CPU**
```text
cmake -B build
cmake --build build --config Release
```

**NVIDIA**
```text
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release
```

**AMD HIP**
`-DGGML_HIP=ON`，可选 `GPU_TARGETS`。

**Apple**
Metal on macOS is enabled by default in normal build；可以用 `--n-gpu-layers 0` 显式禁用 GPU inference。

### 3. llama.cpp model docs

https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md

支撑：
- llama.cpp requires GGUF model format；
- compatible Hugging Face repo can use `-hf <user>/<model>[:quant]`；
- local filesystem model can be loaded directly；
- other formats can be converted to GGUF。

### 4. llama.cpp CLI docs

https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md

支撑 current CLI concepts：
- `--version`
- `--list-devices`
- `--threads`
- `--ctx-size`
- `--n-predict`
- `--prompt`
- `--perf`
- `--device`
- `--n-gpu-layers`
- `--fit` / `--fit-target`
- model path / HF repo

当前 CLI 中 `--n-gpu-layers` 接受 exact number / auto / all，且 `--fit` 可以根据 device memory 调整未设置参数。

这些 flag 是动态 interface，稳定 Lesson 只讲概念，dated snapshot 保存 current spelling。

### 5. llama-bench

https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md

支撑：
- prompt processing (pp)
- text generation (tg)
- combined pp+tg
- GPU layer sweep
- thread sweep
- context depth
- KV cache type
- repetitions
- JSON/CSV/JSONL/SQL output

官方说明：
- each test repeated and reports average t/s + stddev；
- llama-bench timing does not include tokenization/sampling；
- JSON includes build commit、CPU/GPU、backend、model size、parameter count、threads、GPU layers、KV type、timing samples 等。

## Findings

### F1 — 第一次“跑起来”至少要证明四件事

1. **Binary identity**：你运行的是哪个 llama.cpp build？
2. **Model identity**：你运行的是哪个 exact artifact？
3. **Execution path**：CPU / CUDA / HIP / Metal，到底用了什么？
4. **Result + conditions**：prompt/context/offload/timing 是什么？

如果只截图“它回答了”，无法复现，也无法比较。

### F2 — Model name 不足以标识 artifact

Evidence 至少记录：
- repository + revision（若来自 model hub）
- local filename
- file bytes
- SHA256
- GGUF quant/model type from loader or benchmark metadata

同一个 model family 可以有很多不同 quant artifacts。

### F3 — Backend build 与 runtime device 是两层

编译了 CUDA/HIP/Metal backend，不代表当前运行一定使用 GPU。

所以 first-run workflow 先：
```text
llama-cli --version
llama-cli --list-devices
```

再看实际 startup log / benchmark `backends`、`devices`、`n_gpu_layers`。

### F4 — CPU-only 不是“失败路径”

CPU path 是课程的最低硬件基线。

它能验证：
- model artifact 正确；
- tokenizer/chat template 能工作；
- runtime build 正确；
- benchmark/evidence 流程正确。

GPU 是把 execution path 换成 CUDA/HIP/Metal，不是把整个实验换掉。

### F5 — `n_gpu_layers` 是最直观的 offload knob，但不能当永久 CLI 语法记忆题

概念：
```text
more model layers on GPU
→ more VRAM pressure
→ usually less CPU weight traffic/work
```

current llama-cli supports exact/auto/all and a fit mechanism。

但这个 interface 会演进，所以 Lesson 教“GPU layer offload”，实验开始必须运行 `--help` / `--version`。

### F6 — Auto-fit 很方便，但会降低 benchmark 可比性

current CLI `--fit` 可自动调整未设置参数以留 device memory margin。

对第一次成功运行很有价值。

但做 A/B benchmark 时：
- 如果两个 run 实际 ctx/offload 不同；
- 结果不能直接比较。

因此：
- **first success** 可以用 auto-fit；
- **benchmark** 要把实际 context、ngl、KV type 等参数固定并记录。

### F7 — Context size 同时是功能参数和资源参数

`--ctx-size` 决定可用 context budget，并影响 KV cache capacity。

从 Slice 05 已知：
```text
larger context
→ more KV capacity
```

所以一个“GPU offload 更多”的配置可能因为 context/KV 变大反而 OOM。

### F8 — Threads 主要是 CPU execution knob，不是“越多越快”

current CLI 区分：
- generation threads
- batch/prompt-processing threads

真实最优与：
- physical cores
- SMT
- NUMA
- memory bandwidth
- prompt/decode phase

有关。

所以 `--threads` 必须 benchmark，不背“等于逻辑核心数”的口诀。

### F9 — PP 与 TG 必须分开

`llama-bench` 官方定义：

**PP (prompt processing)**
- processing a prompt in batches；
- 更接近 prefill-style work。

**TG (text generation)**
- generating tokens；
- 更接近 autoregressive decode-style work。

它们在同一 GPU 上可相差很大，因为 workload arithmetic intensity 不同。

这直接连接 Slice 04 Roofline。

### F10 — `tokens/s` 不是完整服务体验

`llama-bench` 的 pp/tg 很适合 kernel/runtime baseline，但官方明确说它不包含 tokenization 和 sampling time。

真实交互还要看：
- model load time
- time to first token (TTFT)
- inter-token latency
- prompt tokenization
- sampling
- server queueing / concurrency

所以课程第一 benchmark 不冒充完整 serving benchmark。

### F11 — GPU offload 不是“必须全放 GPU 才有意义”

llama.cpp supports CPU+GPU hybrid inference。

如果 VRAM 不够：
- 只 offload 一部分 layers；
- 其余留 host memory。

这解决 capacity，但性能由：
- CPU work
- memory bandwidth
- CPU↔GPU transfer
- layer placement

共同决定。

它是后续 multi-GPU/offload slice 的入口。

### F12 — Apple 的“显存”心智模型要调整

Apple Silicon 的 CPU/GPU 共享 unified memory，而不是独显式独立 VRAM。

但课程仍可以用同一问题：
- model + KV + runtime 占多少 unified memory？
- Metal backend 是否实际启用？
- system memory 是否有足够 headroom？

因此 capacity model 可迁移，但“VRAM vs RAM”物理边界不同。

## Stable first-run workflow

```text
1. identify runtime
2. list devices
3. identify/hash model
4. run a small deterministic-ish prompt
5. record context/offload/threads
6. verify actual backend/device
7. benchmark pp and tg separately
8. save raw JSON
9. explain result with capacity + Roofline models
```

## Claims to avoid

- “能生成文本 = GPU acceleration 正常。”
- “编了 CUDA 版 = 一定用了 CUDA。”
- “GPU layers 越多一定越快。”
- “threads 越多一定越快。”
- “一个 tokens/s 能代表所有 LLM 性能。”
- “llama-bench tg = 完整聊天延迟。”
- “CPU fallback 没有教学价值。”
- “Apple unified memory 可以直接等同独显 VRAM。”
