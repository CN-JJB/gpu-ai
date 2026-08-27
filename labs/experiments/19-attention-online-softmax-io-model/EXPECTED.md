# Expected — Experiment 19

默认 correctness 部分应得到极小误差，通常在普通 double-precision rounding 范围，例如：

```text
max_abs_error ~ 1e-16 ... 1e-15
```

具体最低位可能随 Python/platform 有轻微变化。

默认 materialization 表：

| N | one N×N / head | two N×N / head | two × 32 heads |
|---:|---:|---:|---:|
| 1024 | 2 MiB | 4 MiB | 0.125 GiB |
| 2048 | 8 MiB | 16 MiB | 0.5 GiB |
| 4096 | 32 MiB | 64 MiB | 2 GiB |
| 8192 | 128 MiB | 256 MiB | 8 GiB |
| 16384 | 512 MiB | 1024 MiB | 32 GiB |

## 应得出的结论

- N 翻倍，N×N intermediate 变 4×。
- Online softmax 能让 blockwise exact attention 不需要先保留完整 score row。
- IO-aware fused attention 避免的是 quadratic intermediate materialization / HBM traffic；exact dense attention 的 QK/PV compute 仍然是 quadratic。
- 这张表不是 runtime peak memory benchmark，也没有包含 Q/K/V/O、workspace、allocator 等其他内存。
