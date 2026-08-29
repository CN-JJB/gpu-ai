# Experiment 10 — 第一次可复现本地 LLM 运行

Hardware level: L0 CPU baseline；L1/L2 可选 GPU acceleration  
Risk: safe  
Cost: 0（已有机器；需要模型下载与磁盘空间）  
平台：Linux / macOS；Windows 可按 upstream build/runtime 文档迁移

## 目标

不是“让模型说句话”。

而是建立一个可复现链：

```text
runtime identity
→ device identity
→ model artifact identity
→ first generation
→ pp/tg benchmark
→ raw evidence
```

## 需要

1. 一个 current llama.cpp build / trusted binary。
2. 一个与你 backend 兼容的 GGUF。
3. 足够 RAM/unified memory/VRAM。

不要由课程写死某个模型 URL。真实下载前检查 model card/license/revision。

## 0. 定义工具路径

如果你自己 build：

```bash
export LLAMA_CLI=./build/bin/llama-cli
export LLAMA_BENCH=./build/bin/llama-bench
```

如果已安装：

```bash
export LLAMA_CLI=llama-cli
export LLAMA_BENCH=llama-bench
```

定义本地模型：

```bash
export MODEL=/path/to/model.gguf
```

## 1. 保存 runtime/device identity

```bash
"$LLAMA_CLI" --version
"$LLAMA_CLI" --list-devices
"$LLAMA_CLI" --help | head -n 80
"$LLAMA_BENCH" --help | head -n 120
```

建议同时：

```bash
LLAMA_CLI="$LLAMA_CLI" MODEL="$MODEL" ./collect-env.sh | tee env.txt
```

## 2. 保存 artifact identity

Linux：

```bash
stat -c '%n %s bytes' "$MODEL"
sha256sum "$MODEL"
```

macOS：

```bash
stat -f '%N %z bytes' "$MODEL"
shasum -a 256 "$MODEL"
```

如果来自 Hugging Face，再记录：
- repository
- revision/commit
- filename
- model card/license

## 3. CPU baseline first generation

先查看当前 help，确认 GPU-layer flag。

当前 snapshot 使用 `-ngl/--n-gpu-layers`。CPU baseline 概念值为 0：

```bash
"$LLAMA_CLI" \
  -m "$MODEL" \
  -ngl 0 \
  -c 4096 \
  -n 64 \
  -p '用一句话解释为什么显存容量和显存带宽不是一回事。' \
  --perf
```

如果你的 current build 参数名不同，以 `--help` 为准。

### 观察

保存 startup log：
- model metadata
- context
- KV type
- backend/device
- offload layers
- generation/perf lines

## 4. GPU / accelerator first success

### NVIDIA

确认 build 含 CUDA，且 `--list-devices` 看到目标 GPU。

### AMD

确认 build 含 HIP，且设备被发现。

### Apple Silicon

普通 macOS build current upstream 默认启用 Metal；仍以 device list/log 为准。

### First-success strategy

current CLI 支持 automatic GPU-layer choice / memory fitting。可先用当前 help 对应的 auto/fit 方式。

如果你确认模型能完整放下，也可手动选择全部 GPU layers。

**第一次成功允许 auto-fit；下一步 benchmark 必须记录并固定最终实际配置。**

## 5. CPU benchmark

current llama-bench snapshot：

```bash
"$LLAMA_BENCH" \
  -m "$MODEL" \
  -p 512 \
  -n 128 \
  -r 5 \
  -ngl 0 \
  -o json > bench-cpu.json
```

其中：
- pp512：prompt processing 512 tokens
- tg128：text generation 128 tokens
- r5：重复 5 次

确认 current `--help` 后再运行。

## 6. GPU/hybrid benchmark

先从 startup log 确定一个固定、能稳定 fit 的 GPU-layer count。

```bash
export GPU_LAYERS=<固定整数>
```

然后：

```bash
"$LLAMA_BENCH" \
  -m "$MODEL" \
  -p 512 \
  -n 128 \
  -r 5 \
  -ngl "$GPU_LAYERS" \
  -o json > bench-gpu.json
```

不要把 first-success 的 auto-fit run 与固定配置 benchmark 混成一组数字。

## 7. 可选：Context depth sensitivity

current llama-bench 提供 context-depth test 参数。确认当前 `--help` 后，固定其他条件，比较例如：

```text
depth 512
depth 4096
depth 16384
```

观察 TG 是否随 KV depth 改变。

## 8. 可选：CPU thread sweep

```bash
"$LLAMA_BENCH" \
  -m "$MODEL" \
  -p 512 \
  -n 128 \
  -r 5 \
  -ngl 0 \
  -t 4,8,16 \
  -o json > bench-cpu-threads.json
```

不要假定最大逻辑线程数就是最快。

## 9. 解释 pp / tg

`llama-bench`：

- pp ≈ prompt processing / prefill-style baseline
- tg ≈ autoregressive generation / decode-style baseline

官方 benchmark timing 不含 tokenization/sampling，所以不要把 tg 当完整 UI/chat latency。

## 10. Evidence

至少提交：

- `env.txt`
- first-generation startup/output log
- `bench-cpu.json`
- `bench-gpu.json`（若有 accelerator）
- Experiment Card

## Benchmark discipline

两组数据只有以下条件相同才直接比较：

- same exact GGUF SHA256
- same llama.cpp build
- same pp/tg token counts
- same context/depth
- same KV type
- same thread settings where relevant
- same offload setting except the variable you intentionally test
- similar thermal/power state

## 无 GPU 替代路径

完整完成：
- artifact identity
- CPU first generation
- CPU pp/tg benchmark
- thread sweep
- Evidence

这已经是有效 L0/L1 学习成果。

## 完成问题

1. startup log 怎样证明实际 backend？
2. CPU→GPU 后 PP 与 TG 哪一个提升更大？为什么？
3. 如果 GPU layers 增加但 TG 没变，下一步查什么？
4. 如果长 context 下 TG 下降，KV/cache/memory traffic 如何解释？
5. 为什么 raw JSON 比截图 tokens/s 更有价值？


## Hypothesis

一次可复现的本地 LLM 运行必须能从 runtime/device/model identity 追到 generation 与 PP/TG raw evidence；“看到回答”只证明功能输出，不证明 GPU path 或性能。

## Fixed variables

benchmark 比较固定 exact GGUF SHA、runtime build、PP/TG/context/KV/threads，并显式记录 offload。first-success auto-fit 与正式固定 benchmark 分开。

## What to observe

- startup backend/device/offload；
- exact model bytes/SHA；
- CPU first generation；
- CPU vs accelerator PP/TG；
- context/thread sweep；
- raw JSON 与 UI 感知 latency 的边界。

## Troubleshooting

- 参数以 current --help 为准。
- GPU device 可见但 TG 不变时查实际 offload/backend/瓶颈。
- auto-fit 只能用于 first success，不作为受控 benchmark 配置。
- CPU-only 完成也是有效学习成果。

## What this proves

你能建立第一个真实、可重跑、可审计的 Local LLM baseline。

## What this does NOT prove

llama-bench TG 不等于完整聊天 UI latency，也不包含质量判断。

## No-hardware path

CPU baseline 是完整替代路径。

## Transfer question

GPU benchmark 比 CPU 快很多，但 startup log 显示只有部分层 offload。你应该把结论写成“GPU 全模型性能”吗？
