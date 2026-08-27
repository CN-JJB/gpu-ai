# Experiment 18 — Real Multi-GPU Scaling

硬件等级：L3（需要已经安全安装、供电、散热并能正常工作的至少两张 GPU）

风险：本实验只做只读拓扑调查和软件 benchmark。**不指导带电插拔、改线、改 BIOS 电气参数或硬件改造。**

## 目标

把“第二张 GPU 值不值”变成可复现 Evidence：

```
exact hardware
→ topology
→ P2P capability
→ measured peer bandwidth if available
→ one-GPU PP/TG baseline
→ two-GPU split PP/TG
→ speedup + efficiency
```

## A. 固定实验身份

记录：

- GPU exact model × count
- VRAM per GPU
- motherboard / platform
- OS / kernel
- driver
- runtime/backend
- llama.cpp exact commit/build
- exact GGUF filename + SHA256
- model fits one GPU? yes/no
- thermal/power state
- display GPU / background load

先运行：

```bash
./collect-topology.sh > topology.txt 2>&1
llama-bench --help > llama-bench-help.txt 2>&1
llama-bench --list-devices > devices.txt 2>&1 || true
```

## B. NVIDIA topology

当前常用只读调查：

```bash
nvidia-smi -L
nvidia-smi topo -m
nvidia-smi topo -p2p p
nvidia-smi topo -p2p n
```

如果系统里的 `nvidia-smi` 支持其他 capability，可额外保存，但必须以本机 `--help` 为准。

若已安装 NVIDIA 官方 `nvbandwidth` 或 CUDA Samples 的 P2P benchmark，可记录 GPU↔GPU 实测带宽。不要用 PCIe 规格表数字冒充实测 P2P。

## C. AMD topology / peer bandwidth

先保存：

```bash
rocminfo
amd-smi --help
```

如果安装了当前 TransferBench：

```bash
./TransferBench p2p
```

它可测 CPU/GPU 与 GPU/GPU pair 的单向/双向 transfer。若没有该工具，不要求为了本实验临时改系统；记录“not available”即可。

## D. 性能实验必须分两类

### D1. Performance scaling

选择一个<strong>能完整放进单张目标 GPU</strong>的模型，这样才能公平比较：

- one GPU baseline
- same model + same quant + same PP/TG config
- two GPU layer split
- optional row/tensor split

先根据本机构建的 `llama-bench --help` 和 `--list-devices` 确认 exact device ID。

当前 llama-bench 的概念性示例：

```bash
# 单卡：把 <GPU0> 换成 --list-devices 的真实 ID
llama-bench -m "$MODEL" -dev "<GPU0>" -sm none -p 512 -n 128 -r 5 -o json > single.json

# 双卡 layer split；设备 ID 和 tensor split 语法必须按当前 help 核对
llama-bench -m "$MODEL" -dev "<GPU0>/<GPU1>" -sm layer -ts "1/1" -p 512 -n 128 -r 5 -o json > layer.json
```

如果你的当前 build 对 `-dev` / `-ts` 的分隔符定义不同，以保存下来的本机 help 为准。不要为了“照抄课程”覆盖真实 CLI。

当前上游还存在 `row` 与 `tensor` split-mode；其中 tensor 当前标记为 experimental。它们属于动态接口，只在确认当前版本后再测。

### D2. Capacity-only experiment

如果目标模型单卡装不下、双卡能装下，可以单独记录“capacity success”。

这类实验不能拿来计算相对单卡 speedup，因为单卡不存在可比运行。

## E. 为什么 PP / TG 要分别看

`llama-bench` 的 PP 与 TG 是不同 workload：

- PP：prompt processing
- TG：text generation

多 GPU 可能 PP 提升明显、TG 提升有限，或反过来。结果表必须分别填写。

## F. 结果表

至少记录：

| mode | devices | split | PP t/s | TG t/s | GPU0 VRAM | GPU1 VRAM | notes |
|---|---|---|---:|---:|---:|---:|---|
| single | | none | | | | n/a | |
| layer | | | | | | | |
| row | optional | | | | | | |
| tensor | optional | | | | | | |

计算：

```
PP speedup = PP_multi / PP_single
TG speedup = TG_multi / TG_single
efficiency = speedup / GPU_count
```

## G. 结论必须区分

1. **Capacity**：是否让原本装不下的模型成功加载？
2. **Latency/per-token performance**：TG 是否更快？
3. **Prompt throughput**：PP 是否更快？
4. **Aggregate user throughput**：是否应该改成每卡一个 replica，而不是模型切分？

## 禁止的结论

- “两张卡总显存 24 GB，所以等于一张 24 GB 卡。”
- “PCIe Gen4 x16 理论带宽就是本机 GPU↔GPU 实测带宽。”
- “模型成功加载就说明 P2P 正常。”
- “PP 提升 1.8×，所以 TG 也提升 1.8×。”
- “一次 benchmark 就能决定任何机器上的双卡价值。”
