# Experiment 20 — Real SDPA Backend Probe

硬件等级：L2（可用 GPU + 已安装 PyTorch）

主路径：PyTorch current SDPA API。NVIDIA CUDA 是主要验证路径；ROCm/AMD 是否能使用某个 fused backend 取决于当前 PyTorch/ROCm/build/hardware，unsupported 也是有效 Evidence。

## 目标

回答：

1. 当前环境到底支持哪些 SDPA backend？
2. `MATH`、`FLASH_ATTENTION`、auto dispatch 的 latency 有什么差异？
3. 峰值临时分配是否随 sequence length 明显分化？
4. fused backend 结果是否与 math reference 在合理浮点误差内一致？

## 环境

建议单独 venv，不强制课程统一版本。

记录：

```bash
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.version.hip); print(torch.cuda.is_available())"
```

## 运行

```bash
python benchmark_sdpa.py --seq 512 1024 2048 --heads 8 --dim 64 --reps 20 > result.json
```

长上下文会快速放大 math backend 的中间内存。不要一开始就上 8K/16K；先从小尺寸验证。

## Backend

脚本尝试：

- `math`
- `flash`
- `auto`

当前 PyTorch API 使用：

```python
from torch.nn.attention import SDPBackend, sdpa_kernel
```

如果 fused backend 对当前 dtype/shape/device 不可用，脚本记录 `unsupported/error`，而不是偷偷切换后宣称“FlashAttention 已测试”。

## 指标

每个 sequence/backend：

- mean latency ms
- tokens/s proxy = sequence / latency
- peak allocated delta MiB
- max abs error vs math reference
- error/status

这里的 tokens/s proxy 只比较 attention operator，不是 LLM end-to-end throughput。

## 注意

- PyTorch allocator/cache 会影响内存观察；本实验是同一进程内相对对比，不当成精确 kernel workspace 审计。
- auto backend 可能随版本、shape、dtype、GPU 改变。
- math backend OOM 是有效结果，但不要因此直接推断某个 fused backend 的全模型最大上下文。
- 不同 fused implementation 的浮点顺序不同，不要求 byte-identical。
