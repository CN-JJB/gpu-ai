# Expected — Experiment 20

没有固定性能数字。

正确的实验可能得到：

- `math`: available;
- `flash`: available, or explicitly unsupported for the current device/shape/dtype/build;
- `auto`: available but selected implementation is dynamic.

Expected qualitative behavior on a supported fused GPU stack:
- as N grows, math backend often pays much larger quadratic intermediate cost;
- fused/flash latency advantage can grow with sequence length;
- fused peak allocation can be much lower than naive math;
- short sequences may show little advantage because launch/setup overhead matters.

But any of these can differ by version/hardware.

Correctness:
- fused vs math may differ slightly due to floating-point operation order;
- exact byte equality is not required;
- large or pathological error requires investigation.

A backend rejection is Evidence, not a failed course run.
