# Experiment 22 — Real GEMM Shape / Precision Probe

硬件等级：L2

依赖：
- PyTorch
- CUDA/HIP-visible GPU

## 问题

为什么同一张 GPU：

- large-M GEMM 很容易体现 FP16/BF16 matrix acceleration；
- M=1 decode-like matmul 却可能离“Tensor TOPS”非常远？

## 测试两种 shape

### Prefill-like

```
M=512, K=4096, N=4096
```

### Decode-like

```
M=1, K=4096, N=4096
```

它们都不是完整 LLM，只是把 matrix shape 差异孤立出来。

## dtype

默认尝试：

- float32
- float16
- bfloat16

支持情况由当前 GPU/PyTorch build 决定。

## FP32 内部精度

脚本记录并可设置：

```
torch.set_float32_matmul_precision(...)
```

默认 `highest`，避免把 TF32 偷偷混入 FP32 baseline。

可额外测试：

```bash
python benchmark_matmul.py --fp32-precision high
```

在支持的 NVIDIA CUDA 环境中，这可能允许更快的内部低精度/TF32 路径。它是动态 backend 行为，必须记录。

## 运行

```bash
python benchmark_matmul.py > result.json
```

## 输出

每个 shape/dtype：
- mean ms；
- calculated TFLOP/s；
- status/error；
- device/build metadata。

## 解释

### Prefill-like

大 M：
- tile 数多；
- 更容易喂满 matrix units；
- precision peak 更有机会反映到 achieved TFLOP/s。

### Decode-like

M=1：
- matrix tile 利用差；
- weight read 占比高；
- launch/dispatch overhead 更明显；
- kernel 可能走 GEMV/专用路径。

所以不要拿这个 microbenchmark 的 TFLOP/s 去和产品 FP16 peak 做“效率百分比”后直接推断整个 LLM。

## 不测 INT4 的原因

PyTorch `@` 不能代表本地 LLM 的 Q4 kernel。

Q4/GPTQ/AWQ/GGUF 等需要：
- packed layout；
- scale/zero-point；
- dequant/fused kernel；
- backend-specific path。

硬塞一个“torch int4 matmul”反而会教错。

后续真实量化 benchmark 应以实际推理 backend 为单位做。


## Hypothesis

同一 GPU 上，大 M 的 prefill-like GEMM 更容易利用矩阵单元；M=1 的 decode-like shape 会受到 tile utilization、weight traffic 和 launch/dispatch 的限制，因此 achieved TFLOP/s 可能相差很大。

## Fixed variables

同一 GPU、PyTorch build、K/N、warmup/repetition 规则固定；比较 shape 时只改 M，比较 dtype 时只改 dtype。FP32 precision policy 必须记录。

## What to observe

1. 各 dtype 是否 supported 或明确报错。
2. M=512 与 M=1 的 mean ms / TFLOP/s。
3. FP32 precision=highest/high 时行为是否变化。
4. device/build metadata 是否完整。
5. 为什么 achieved TFLOP/s 不能直接映射成整个 LLM TG。

## Troubleshooting

- 第一次调用可能包含初始化开销，按脚本 warmup 规则解释。
- OOM 时降低 shape，但必须同时修改 baseline/candidate 并记录。
- BF16/FP16 不支持时保留 status/error，不要强制 cast 后假装原生支持。
- 其他进程占 GPU 会污染结果。

## Evidence to save

保存 result.json、完整命令、GPU/PyTorch/build identity 和任何 shape 调整。

## What this proves

你能实测矩阵 shape 与 precision 对该环境 GEMM 路径的影响。

## What this does NOT prove

它不是 LLM benchmark，也不能代表 Q4 kernel、attention、KV 或端到端 tok/s。

## No-hardware fallback

没有可见 CUDA/HIP GPU 时完成 Experiment 21 的 Roofline 模型，真实 probe 留到 Learner Verified。

## Transfer question

同一 GPU FP16 M=512 达到很高 TFLOP/s，但 M=1 很低。为什么这并不矛盾？
