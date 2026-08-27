# Expected result

本实验**没有固定 tokens/s 答案**。

不同 CPU/GPU、model、quant、backend、offload、context 会产生不同结果。

## 必须验证的结构性结果

### 1. Runtime identity exists

```text
llama-cli --version
```

能保存当前 build/version/commit 信息。

### 2. Device discovery exists

```text
llama-cli --list-devices
```

至少能说明 runtime 看到了哪些 execution devices。

无 GPU 时 CPU-only 路径仍然有效。

### 3. Artifact is uniquely identified

Evidence 中必须有：
- filename
- exact bytes
- SHA256
- source repo/revision if known

### 4. First generation succeeds

CPU baseline 应能够：
- load GGUF
- tokenize prompt
- generate tokens
- print performance/runtime information

如果失败，失败日志本身就是 diagnostic evidence，不要伪造成功。

### 5. Benchmark raw output is saved

`llama-bench` JSON 应包含足够 metadata 来复现/解释：
- build information
- CPU/GPU/backend
- model size/parameter metadata
- threads
- GPU layers
- KV type
- timing samples
- throughput statistics

字段随版本可能演进，以当前 JSON 为准。

## PP / TG interpretation

不要期待 PP 和 TG 相同。

通常：
- PP 更接近高并行 prefill；
- TG 更接近 decode；
- 两者对 compute/bandwidth 的敏感性不同。

这正是实验要观察的结果。

## CPU vs GPU

如果有 accelerator，至少比较一组相同 model/config 的：
- CPU baseline
- fixed GPU/hybrid offload

不要把不同 context、不同 quant 或 auto-fit 后未知实际参数的 run 放在同一速度表里。

## What counts as failure

以下都属于有效实验结果，只要记录完整：
- model OOM
- model unsupported
- backend not detected
- GPU offload slower than CPU
- more threads slower
- PP improves but TG barely moves
- long-context TG degrades

Evidence 的目标不是“必须快”，而是能解释。
