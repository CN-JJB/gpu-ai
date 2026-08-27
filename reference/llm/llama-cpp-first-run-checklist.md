# 第一次本地 LLM 运行速查 — llama.cpp / GGUF

## 目标

第一次运行不是“看见一句回答”，而是产生可复现 Evidence。

## 运行前 4 个身份

### 1. Runtime

```bash
llama-cli --version
```

保存：
- build version / commit
- compiler/backend info if shown

### 2. Devices

```bash
llama-cli --list-devices
```

确认：
- CPU
- CUDA
- HIP
- Metal
- other backend

### 3. Model artifact

本地 GGUF：

```bash
ls -lh model.gguf
sha256sum model.gguf
```

macOS：

```bash
shasum -a 256 model.gguf
```

保存：
- repo/revision
- filename
- bytes
- hash
- quant/model metadata

### 4. Execution config

至少记录：
- ctx size
- GPU layers / offload
- CPU threads
- KV type
- Flash Attention mode
- device selection

## Build paths

具体 command 以 current upstream `docs/build.md` 为准。

概念：

| platform | llama.cpp backend |
|---|---|
| CPU | native/BLAS |
| NVIDIA | CUDA |
| AMD | HIP |
| Apple Silicon | Metal |
| Intel GPU | SYCL / other supported path |

不要从“binary name”猜 backend；用 `--version`、`--list-devices` 与 run log 验证。

## First success vs benchmark

### First success

目标：
- 能加载
- 能生成
- 不 OOM

可以允许 runtime auto-fit。

### Benchmark

目标：
- A/B 可比较

必须固定：
- model artifact
- context
- prompt/gen token counts
- offload
- threads
- KV type
- backend
- power/thermal state

## CPU baseline

概念：

```text
n_gpu_layers = 0
```

价值：
- 验证 model/runtime
- 建立 fallback
- 为 GPU speedup 提供 baseline

具体 current flag 用 `llama-cli --help` 确认。

## GPU offload

概念：

```text
0 layers → CPU
some layers → hybrid
all/auto → more GPU residency
```

more GPU residency 往往：
- VRAM use ↑
- CPU model work ↓

但性能不保证单调，因为还受 memory placement、CPU/GPU transfer、KV、backend kernels 影响。

## Context

```text
ctx size ↑
→ KV budget ↑
```

所以 benchmark 不能偷偷让不同 run 使用不同 ctx。

## PP vs TG

`llama-bench`：

### PP

prompt processing。

更接近：
```text
prefill
```

### TG

text generation。

更接近：
```text
decode
```

但 benchmark 不包含 tokenization 与 sampling time。

## 推荐 benchmark 最小集

同一 model/config：

```text
pp 512
tg 128
5 repetitions
JSON output
```

另外可选 context depth：

```text
depth 4096
```

观察 KV depth 是否改变 tg。

## Evidence minimum

```text
runtime commit/version
OS
CPU
RAM
GPU
driver/backend
model repo/revision/hash
model size/params/quant
ctx
threads
ngl/offload
KV type
PP tokens/s ± stddev
TG tokens/s ± stddev
raw JSON
temperature/power notes
```

## 如何解释

PP 高、TG 低：
→ 先回到 prefill vs decode / Roofline。

GPU offload 增加但没快：
→ 查 CPU↔GPU、VRAM fit、kernel/backend、KV placement。

长 context TG 下降：
→ 查 KV traffic/cache/context-depth effects。

CPU threads 增加反而慢：
→ 查 memory bandwidth、SMT/NUMA/oversubscription。

## 不能直接比较的 benchmark

若以下任一不同，不要只拿 t/s 做显卡排名：
- model
- quant
- backend version
- context
- PP/TG token count
- offload
- KV type
- sampling/server path
- thermals/power
