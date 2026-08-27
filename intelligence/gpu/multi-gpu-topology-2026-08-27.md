# Multi-GPU Topology / llama.cpp Snapshot — 2026-08-27

Purpose: dynamic implementation/tool snapshot for Slice 11. Stable concepts live in Lesson/Reference.

## Pinned llama.cpp upstream

Pinned master snapshot:

```
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Commit date: 2026-08-27.

## llama-bench current interface

Current upstream `tools/llama-bench/README.md` exposes:

```
-sm, --split-mode <none|layer|row|tensor>   default: layer
-mg, --main-gpu <i>
-dev, --device <dev0/dev1/...>
-ts, --tensor-split <ts0/ts1/..>
-ngl, --n-gpu-layers <n>
-ctk, --cache-type-k
-ctv, --cache-type-v
-fa, --flash-attn
```

It supports:
- PP via `-p`;
- TG via `-n`;
- PG via `-pg`;
- repeated runs via `-r`;
- JSON / JSONL / CSV / Markdown output.

Important parser note:
- llama-bench's own README/help describes multiple devices / tensor split with slash-shaped examples such as `dev0/dev1` and `ts0/ts1`;
- common CLI/server docs currently show comma-separated `--tensor-split N0,N1,...`.

Therefore experiments must save the exact local `llama-bench --help` rather than treating punctuation as stable API.

## Current split semantics in common CLI/server docs

Current docs describe:

- `none`: one GPU only;
- `layer`: split layers and KV across GPUs, pipelined;
- `row`: split weights across GPUs by rows, parallelized;
- `tensor`: split weights and KV across GPUs, parallelized, currently experimental.

These labels/semantics are dynamic runtime facts. The stable course maps them to broader families rather than promising eternal flag behavior.

## NVIDIA topology / P2P

Current NCCL troubleshooting guidance:

```
nvidia-smi topo -m
nvidia-smi topo -p2p p
nvidia-smi topo -p2p n
```

Current capability meaning in NCCL docs:
- `p`: PCIe peer-to-peer;
- `n`: NVLink peer-to-peer.

`nvidia-smi topo -m` can expose topology labels such as PIX/PXB/PHB/NODE/SYS/NV# and CPU/NUMA affinity on applicable systems.

Current NVIDIA NCCL performance guidance recommends `nvbandwidth` for measuring GPU memory and GPU-to-GPU bandwidth over PCIe/NVLink.

Stable warning:
```
P2P capability matrix != measured bandwidth
topology label != application throughput
```

## AMD HIP P2P

Current HIP multi-device docs state:

- P2P allows one GPU to directly read/write another GPU's memory;
- avoiding host involvement can reduce transfer time;
- without activated P2P, `hipMemcpy` can still operate using a staging buffer in host memory, with a performance penalty.

This is useful cross-vendor evidence for why “both GPUs enumerate” is insufficient.

## AMD TransferBench

Current TransferBench docs expose a `p2p` preset:

```
./TransferBench p2p
```

It measures device-memory bandwidth across CPU NUMA nodes and GPUs and includes:
- CPU→CPU;
- CPU→GPU;
- GPU→GPU;
- unidirectional;
- bidirectional.

It is single-node for this preset. Current environment controls include direction mode and DMA/GFX executor selection.

## Evidence capture rule

For every real multi-GPU result record:

```
hardware identity
+ runtime build
+ topology
+ P2P capability
+ peer bandwidth tool/method
+ exact model artifact
+ PP
+ TG
+ raw output
```

Do not substitute:
- PCIe marketing/spec bandwidth for measured P2P;
- model load success for peer-access proof;
- PP speedup for TG speedup.

## Revalidation triggers

Re-check this snapshot when:
- llama.cpp split flags change;
- `tensor` loses/gains experimental status;
- device/tensor-split syntax changes;
- NVIDIA topology capability letters change;
- AMD topology/benchmark tooling changes;
- backend implementation begins using a substantially different multi-GPU scheduler.
