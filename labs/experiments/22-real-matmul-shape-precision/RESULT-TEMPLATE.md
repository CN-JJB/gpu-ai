# Result — Experiment 22

## Environment

- Date:
- GPU:
- Driver:
- PyTorch:
- CUDA/HIP:
- FP32 matmul precision:
- Power/thermal notes:

## Prefill-like

| dtype | status | mean ms | achieved TFLOP/s |
|---|---|---:|---:|
| FP32 | | | |
| FP16 | | | |
| BF16 | | | |

## Decode-like

| dtype | status | mean ms | achieved TFLOP/s |
|---|---|---:|---:|
| FP32 | | | |
| FP16 | | | |
| BF16 | | | |

Raw JSON:

## Analysis

1. Which dtype gains most in large-M GEMM?
2. Does M=1 preserve the same ratio?
3. Is any dtype unsupported?
4. Did changing FP32 matmul precision change the FP32 result?
5. What can this say about matrix-unit utilization?
6. What can it **not** say about Q4 local LLM inference?

## Integrity

- [ ] exact shapes recorded
- [ ] exact PyTorch/CUDA/HIP recorded
- [ ] FP32 precision mode recorded
- [ ] no INT4/Q4 claim inferred from FP16/BF16 matmul
- [ ] no product-page TOPS copied as achieved throughput
