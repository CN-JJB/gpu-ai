---
experiment_id: example-latency-hiding-scheduler-model
date: 2026-08-26
hardware_level: L0
risk_level: safe
status: reference-example
---

# Question

当一个抽象 scheduler 面对长延迟 memory dependency 时，增加 resident execution groups 能否减少 idle cycles？

## Hardware

无特殊硬件；CPU 运行 Python 概念模型。

## Software

Python 3。

## Configuration

- 1 个抽象 scheduler
- 每 cycle 最多 issue 1 条 instruction
- 每 group 每轮：4 compute instructions + 1 memory instruction
- memory instruction 后等待 20 cycles
- 每 group 20 rounds
- resident groups：1、2、4、8、16、32

## Procedure

运行：

~~~bash
python labs/experiments/02-latency-hiding-scheduler-model/simulate.py
~~~

## Results

- 1 group：20.8% issue utilization
- 2 groups：35.7%
- 4 groups：55.3%
- 8 groups：76.4%
- 16 groups：94.4%
- 32 groups：100.0%

## Observations

更多 resident groups 让 scheduler 更容易在当前 group stall 时找到另一个 ready group。

收益不是线性的：16 groups 已经覆盖了大部分 idle cycles，继续增加到 32 只获得最后约 5.6 个百分点的 issue utilization。

## Conclusion

这个模型支持 latency hiding 的最小因果链：

**stall 不会消失 → scheduler 换到其他 ready resident group → idle cycles 下降 → throughput 更接近 issue 上限。**

它也提供 occupancy 纠偏：更多 resident groups 只提供隐藏延迟的 headroom。达到“足够”之后，再增加 occupancy 的收益会变小。

如果真实 kernel 为了更大的 tile 使用更多 registers/shared memory/LDS，把 resident groups 从 16 压到 8，也不能只凭 occupancy 宣布优化失败；真实代码可能用这些资源换来更少 global-memory traffic、更好 reuse 或 ILP。

## Reproducibility

见：

- labs/experiments/02-latency-hiding-scheduler-model/simulate.py
- labs/experiments/02-latency-hiding-scheduler-model/EXPECTED.md

## Sources

- NVIDIA CUDA Programming Guide — Hardware Multithreading
- NVIDIA CUDA C++ Best Practices Guide — Occupancy
- AMD ROCm HIP — Programming model / Hardware implementation
