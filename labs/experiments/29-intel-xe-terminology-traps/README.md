# Experiment 29 — Intel Xe Terminology / Backend Traps

硬件等级：L0

## 目标

检查是否分清：

- EU / Vector Engine / Xe-Core；
- XMX；
- SLM；
- subgroup；
- SYCL；
- Level Zero；
- oneAPI；
- Arc A/B generations。

## 运行

```bash
python3 check_lineage.py
```

参考答案应 10/10。

## Assertions

你需要判断：

1. EU can be compared 1:1 with CUDA cores → false
2. Xe-Core and Vector Engine are the same level → false
3. XMX is matrix acceleration → true
4. Xe-LP Iris Xe has the same Arc-class XMX path → false
5. Alchemist is Xe-HPG → true
6. Battlemage is Xe2 → true
7. Intel subgroup is always 32 → false
8. SLM is extra VRAM → false
9. Level Zero is a hardware architecture → false
10. XMX availability guarantees any Q4 GGUF uses XMX → false

## 完成标准

除了 10/10，还要解释每个 false claim 缺少哪层 Evidence。