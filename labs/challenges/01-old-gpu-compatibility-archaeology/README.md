# Challenge 01 — 老计算卡 / 特殊 GPU 兼容性考古

硬件等级：L0 主路径；L1/L2 真机增强  
风险：safe  
成本：0；不要求购买旧卡

## 真实问题

一张旧 Tesla、Quadro、FirePro、Instinct、Arc 或 OEM 特殊卡参数看起来很香：

~~~text
显存大
价格低
理论算力还行
~~~

它今天到底能不能成为本地 LLM 机器的一部分？

## 你要学的不是“旧卡名单”

真正要建立的是：

~~~text
silicon capability
→ driver lifecycle
→ compiler/runtime target
→ backend build
→ operation/kernel coverage
→ model/quant compatibility
→ measured workload
~~~

任何一层断掉，都可能让“纸面神卡”变成时间黑洞。

## 1. 先冻结精确身份

不要只写：

~~~text
Tesla
Instinct
Arc
~~~

至少调查：
- exact SKU；
- device / PCI ID；
- architecture/generation；
- VRAM type/capacity；
- compute capability / gfx target / Xe generation；
- power/connectors/form factor；
- video output/fan/passive cooling constraints。

## 2. Capability 不等于 Current Support

建立四列：

| Layer | Question | Evidence | Status |
|---|---|---|---|
| hardware | 芯片理论支持什么 | 官方架构资料 | |
| driver | 当前 OS/driver 是否识别 | 当前官方支持资料/真机 | |
| runtime | CUDA/ROCm/SYCL/Vulkan 等能否 target | current docs/build | |
| LLM backend | 目标 op/quant/kernel 是否覆盖 | upstream source/test | |

## 3. L0 路径

选一张你感兴趣的旧卡。

只用公开资料完成：
1. identity；
2. driver/runtime lifecycle；
3. llama.cpp/目标 backend 当前证据；
4. 可能 fallback；
5. platform/power/cooling cost；
6. UNKNOWN。

禁止从“有人跑起来过”直接推导你的目标 workload 也可用。

## 4. 真机增强

如果你已经有卡：
- 保存 device discovery；
- 保存 runtime/build identity；
- 跑最小 backend operation test；
- 再跑固定模型；
- 先 correctness/quality，再 PP/TG。

不要为了挑战去买一张你还没完成 L0 dossier 的卡。

## Retrieval Practice

1. 驱动能看到 GPU 为什么不等于当前 backend 可用？
2. backend 能 load model 为什么还不等于常用 quant 高效？
3. 为什么旧计算卡的散热/风道可能是整机 hard gate？
4. 低价格应该进入哪个阶段：compatibility 前还是 hard gates 后？

## 完成证据

提交：
- compatibility ladder；
- 当前支持来源日期；
- 预计 fallback；
- whole-machine hidden costs；
- GO-TO-REAL-TEST / BLOCKED / NOT-WORTH-THE-TIME。

这不是购买推荐。

## Primary / Current Sources

- NVIDIA CUDA documentation: https://docs.nvidia.com/cuda/
- AMD ROCm documentation: https://rocm.docs.amd.com/
- Intel oneAPI GPU architecture: https://www.intel.com/content/www/us/en/docs/oneapi/optimization-guide-gpu/latest/intel-xe-gpu-architecture.html
- llama.cpp backend operation coverage: https://github.com/ggml-org/llama.cpp/blob/master/docs/ops.md

所有 current-support claim 运行挑战时重新验证。


## Expected outcome

你最终应该得到一条分层结论：

~~~text
historical capability
→ current driver/runtime support
→ current backend build
→ actual workload evidence
~~~

其中任何一层缺失，都保留 UNKNOWN，而不是用“老卡以前支持 CUDA”替代当前可用性。

## Failure recovery

如果官方旧文档难找，先冻结 exact GPU/compute capability，再从当前 driver/runtime support matrix 反向查；不要用论坛一句“还能跑”直接升级成正式结论。

## What this does NOT prove

兼容性考古不证明性能值得、不证明功耗划算，也不等于购买建议。

## No-hardware path

主路径本来就是资料考古；有真卡时才追加 device/runtime probe。
