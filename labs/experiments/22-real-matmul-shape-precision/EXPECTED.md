# Expected — Experiment 22

没有统一正确性能数字。

Expected pattern on many matrix-accelerated GPUs:

- large-M prefill-like GEMM shows much clearer FP16/BF16 acceleration;
- M=1 decode-like case gets much less value from matrix peak;
- exact ratios vary with GPU, library, clocks, shape and dtype support.

Possible valid exceptions:
- library has highly optimized GEMV path;
- BF16 unsupported or slow on older hardware;
- FP32 mode internally uses a faster reduced-precision path if explicitly enabled;
- thermal/power limits change repeated results.

The only fixed expectation is methodological:

```
same GPU
+ same K/N
+ radically different M
→ matrix-unit utilization can change radically
```

Do not fill in expected TFLOP/s from a spec sheet.
