# Evidence — Experiment 11: Multi-GPU Interconnect

状态：课程设计 + L0 synthetic model 已验证；真实双卡结果留空，等待实际硬件 Evidence。

## Claim under test

> 两张 GPU 的价值必须拆成 capacity、single-request performance、aggregate throughput 三个问题；跨卡模型并行的 scaling 由 compute saving 与 interconnect/synchronization cost 共同决定。

## Stable causal model

```
partition
→ per-GPU compute
→ cross-GPU data movement
→ synchronization
→ imbalance
→ observed scaling
```

延迟近似：

```
T_N ≈ T_compute / N
    + bytes_critical / B_link
    + T_sync
    + T_imbalance
```

## L0 synthetic evidence

Experiment:
- `labs/experiments/17-multi-gpu-interconnect-roof-model/`

Parameters:
- single GPU baseline = 10 ms/token
- 2 GPUs
- 64 MiB critical transfer/token
- sync = 0.2 ms
- imbalance = 0

| effective link | total | speedup | efficiency |
|---:|---:|---:|---:|
| 8 GiB/s | 13.0125 ms | 0.7685× | 38.4% |
| 16 GiB/s | 9.1063 ms | 1.0981× | 54.9% |
| 32 GiB/s | 7.1531 ms | 1.3980× | 69.9% |
| 64 GiB/s | 6.1766 ms | 1.6190× | 81.0% |
| 128 GiB/s | 5.6883 ms | 1.7580× | 87.9% |

Interpretation:
- ideal compute halving alone cannot predict speedup;
- slow link can erase all compute gain;
- scaling efficiency remains below ideal even at high link bandwidth because communication/sync remain;
- these are synthetic teaching units, not hardware claims.

## Real experiment path

Experiment:
- `labs/experiments/18-real-multi-gpu-scaling/`

Required raw Evidence:
1. exact GPU/platform identity;
2. topology;
3. P2P capability;
4. peer bandwidth if a suitable tool is available;
5. exact llama.cpp build;
6. exact model + SHA256;
7. one-GPU PP/TG baseline;
8. same-artifact multi-GPU PP/TG;
9. per-device VRAM;
10. raw JSON outputs.

## Current externally verified implementation facts

Snapshot date: 2026-08-27.

- Current llama.cpp `llama-bench` exposes split modes `none|layer|row|tensor`, device selection, tensor split, PP/TG tests and JSON output.
- Current llama.cpp CLI/server docs describe layer as layer+KV split, row as parallel row split, and tensor as parallel weights+KV split; tensor is currently marked experimental.
- NVIDIA current NCCL troubleshooting docs describe `nvidia-smi topo -p2p p` for PCIe P2P capability and `-p2p n` for NVLink capability; topology alone is not a bandwidth benchmark.
- AMD current HIP docs state that P2P permits direct peer memory access; without P2P activation, `hipMemcpy` may use a host staging buffer with a performance penalty.
- AMD current TransferBench `p2p` preset measures single-node CPU/GPU and GPU/GPU uni/bidirectional transfers.

These are dynamic tool facts and belong in `intelligence/`, not the timeless Lesson.

## What would falsify a simplistic buying rule?

Any of the following:
- two GPUs load a larger model but TG is slower than one-GPU baseline;
- PP gains much more than TG;
- nominally similar dual-GPU machines differ because topology/P2P differs;
- two replicas outperform one cross-GPU model for aggregate request throughput;
- a slow/heterogeneous second GPU lowers synchronized parallel performance.

## No fabricated benchmark rule

This Evidence file intentionally contains no named-GPU real performance numbers until a real machine is tested with raw outputs preserved.
