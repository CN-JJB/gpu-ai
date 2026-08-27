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
