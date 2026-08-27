# Experiment 26 — Real AMD gfx Target / ROCm Inventory

硬件等级：L1/L2（任意 AMD GPU；完整 ROCm path 需要已安装 ROCm/HIP）

风险：只读。

## 目标

把：

```
"这是 RDNA3 / RDNA2 / Vega"
```

升级成：

```
exact model
→ exact gfx target
→ wavefront properties
→ ROCm/HIP version
→ official support status
→ backend visibility
```

## A. 一键采集

```bash
./collect-amd.sh > amd-inventory.txt 2>&1
```

采集器只做只读命令：

- `lspci`
- `amd-smi version/list/static`
- `rocminfo`
- `hipconfig --full`
- optional PyTorch HIP identity

## B. 解析 gfx target

```bash
python3 identify_arch.py
```

脚本解析 `rocminfo` 中形如：

```
gfx1030
gfx1100
gfx1201
gfx90a
gfx942
gfx950
```

的 target，并给出课程 snapshot mapping。

## C. 当前 mapping

常见：

```
gfx803       → GCN/Polaris-era
gfx900/906   → Vega / GCN5
gfx908       → CDNA / MI100
gfx90a       → CDNA2 / MI200
gfx942       → CDNA3 / MI300
gfx950       → CDNA4 / MI350

gfx101x      → RDNA
gfx103x      → RDNA2
gfx110x      → RDNA3
gfx115x      → RDNA3.5
gfx120x      → RDNA4
```

CDNA5/current future targets必须按最新 AMD docs 更新，不在脚本里猜。

## D. Support check

拿到 gfx target 后，打开当前 AMD ROCm support/compatibility matrix，确认：

- exact product 是否列出；
- OS；
- ROCm version；
- Runtime vs full SDK/library support；
- PyTorch/vLLM/llama.cpp support。

不能只因为：

```
gfx1030 = RDNA2
```

就推导：

```
all RX 6000 cards fully supported on this OS
```

## E. AMD SMI current commands

Current AMD SMI docs support：

```bash
amd-smi version
amd-smi list
amd-smi static
amd-smi topology
```

脚本保存 `--help`，所以未来 CLI 改动可追溯。

## F. LLM next step

如果目标 backend 是 llama.cpp：

1. exact build；
2. HIP/ROCm device detection；
3. exact model；
4. PP；
5. TG；
6. VRAM；
7. compare CPU / Vulkan / HIP path if relevant。

不要假设 HIP 一定是每张 Radeon 的最佳 backend；需要 Evidence。

## 结果

填写 `RESULT-TEMPLATE.md` 并保留 `amd-inventory.txt`。