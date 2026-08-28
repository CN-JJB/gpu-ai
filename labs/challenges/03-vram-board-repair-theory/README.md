# Challenge 03 — 显存扩容 / 板级维修：原理、诊断与“什么时候不该动手”

硬件等级：L0 主路径  
风险：high（真实板修）  
成本：L0 为 0

## 安全边界

这门课可以教你：
- 为什么 VRAM 容量不是“焊更多颗粒就行”；
- memory channel / bus width / rank/density/strap/firmware 的关系；
- 常见故障证据如何分类；
- 怎样决定交给专业维修还是放弃。

**不要求你进行 BGA 返修、显存更换、供电注入或带电板级测量。**

不要打开 PSU；不要把网络视频里的温度/电压/焊接参数当通用配方。

## 1. “扩容”至少跨五层

~~~text
GPU memory controller capability
→ PCB routed channels / placements
→ DRAM device density/organization
→ straps/board configuration
→ firmware/driver memory training & address map
~~~

所以：

~~~text
空焊盘存在
!=
焊芯片就能扩容
~~~

## 2. 故障症状不是根因

可能观察：
- artifact；
- driver reset；
- memory test error；
- load-dependent crash；
- hot/cold sensitivity；
- 一部分 workload 正常。

这些只能形成 hypothesis。

可能根因还包括：
- VRAM；
- GPU core；
- VRM/power；
- PCIe/contact；
- overheating；
- firmware；
- host/platform instability。

## 3. 先做非侵入 Evidence

优先：
- exact identity；
- error counters；
- vendor diagnostics；
- memory test；
- sustained workload；
- temperature/power/clock timeline；
- known-good platform cross-check。

只有在这些证据后，才有资格说“怀疑某个板级区域”。

## 4. Repair economics

即使技术上可修，也要算：

~~~text
card value
- expected repair parts
- tools
- failed attempts
- lost return window
- opportunity cost
- reliability uncertainty
~~~

垃圾佬能力包括“知道不值得修”。

## L0 项目

给三个 case：
1. memory test error；
2. load-only crash；
3. PCIe/link instability。

分别写至少 3 个 competing hypotheses，并设计**非侵入**证据来排除。

## Retrieval Practice

1. 为什么 VRAM bus width 与芯片数量不是随意组合？
2. artifact 为什么不能直接等价成“显存坏”？
3. 退货窗口内为什么不应该先做不可逆维修？
4. 什么情况下“专业板修”比“自己学焊 BGA”更符合 TCO？

## 完成证据

提交：
- memory-system layer diagram；
- failure hypothesis tree；
- non-invasive diagnostic plan；
- repair/return economics；
- STOP/ESCALATE decision。

## Sources

- GPU vendor diagnostics 与 memory/RAS 文档；
- DRAM/board 具体电气事实必须来自目标器件 datasheet、board evidence 或专业维修资料；
- 不把另一个 PCB revision 的维修经验直接迁移。
