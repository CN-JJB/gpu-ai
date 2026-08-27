# Experiment 30 — Real Intel XPU / SYCL / Level Zero Inventory

硬件等级：L1/L2

适用：
- Intel Arc A/B dGPU；
- Intel built-in Arc；
- supported modern Intel iGPU；
- Data Center Max/Flex。

风险：只读。

## 目标

一次采集：

```
PCI device
→ SYCL / Level Zero visibility
→ torch.xpu visibility
→ llama.cpp SYCL visibility
→ VRAM/global memory
→ subgroup/workgroup properties
```

## A. 一键采集

```bash
./collect-intel.sh > intel-inventory.txt 2>&1
```

尝试记录：

- `lspci`
- `sycl-ls`
- `clinfo -l`
- `icpx --version`
- Level Zero related environment
- PyTorch `torch.xpu`
- llama.cpp `--list-devices`
- `llama-ls-sycl-device` if available

缺少工具是 valid Evidence。

## B. PyTorch XPU

当前 PyTorch 正式提供：

```python
torch.xpu.is_available()
torch.xpu.device_count()
torch.xpu.get_device_name()
```

当前官方验证范围包括 Arc A/B 系列和部分 Core Ultra integrated Arc。

运行：

```bash
python3 xpu_probe.py
```

## C. SYCL / Level Zero

当前 oneAPI 推荐用：

```bash
sycl-ls
```

观察是否出现：

```
[level_zero:gpu]
```

`ONEAPI_DEVICE_SELECTOR` 可以筛选 Level Zero GPU。

## D. llama.cpp SYCL

如果是 SYCL build：

```bash
llama-bench --list-devices
llama-ls-sycl-device
```

当前 upstream 会显示诸如：
- device name；
- global mem；
- max work group；
- max subgroup；
- driver version。

## E. dGPU vs iGPU

### Arc dGPU
```
dedicated GDDR VRAM
```

### Intel iGPU
```
shared system memory
```

不要把两种 “Global mem size” 按相同容量模型解释。

## F. Real LLM A/B

在已有 Experiment 10 基础上记录：
- llama.cpp commit；
- oneAPI/SYCL；
- device；
- model/SHA；
- quant；
- PP；
- TG；
- FlashAttention on/off if current backend supports it；
- raw JSON。

## G. 结果

填写 `RESULT-TEMPLATE.md`。