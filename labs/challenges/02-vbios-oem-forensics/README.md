# Challenge 02 — VBIOS / OEM / 工程卡：只读取证与风险判断

硬件等级：L0/L1  
风险：medium；**本挑战默认只读，不执行刷写**  
成本：0

## 为什么课程要讲，但不把“强刷”当作作业

二手市场会遇到：
- OEM 卡；
- 工程样品；
- 矿卡改 BIOS；
- device ID / subsystem 异常；
- 频率/功耗限制与零售版不同；
- 显存容量或板型与普通 SKU 不一致。

如果你不会判断固件身份，可能把“能亮机”误当成“正常零售卡”。

但 firmware 写入失败可能让设备无法启动；错误电源/板级修改还有硬件风险。

所以本挑战核心是：

~~~text
identify
→ compare
→ preserve
→ assess
→ STOP before write
~~~

## 1. 建 firmware identity dossier

只读收集：
- GPU exact identity；
- PCI vendor/device/subsystem IDs；
- reported VBIOS/firmware version；
- board/OEM label/photos；
- clocks/power limits；
- memory capacity/vendor if tool reliably reports；
- driver/runtime behavior。

## 2. 找“它应该是什么”的证据

优先：
- OEM/vendor support page；
- official product/device database；
- original machine/service documentation；
- known board/subsystem identifiers。

第三方 VBIOS database 只能作为线索，不能自动升级成官方匹配证明。

## 3. 对比不是只比版本字符串

问：
- device/subsystem 是否一致？
- board power/cooling 是否对应？
- memory configuration 是否对应？
- firmware 是否来自同一 board revision？
- 当前卡有没有异常限频、识别、display/compute behavior？

## 4. Read-only stop conditions

遇到任一项就停止在调查层：
- board identity 不确定；
- backup/恢复路径不清楚；
- 卡是唯一显示设备且无可靠恢复环境；
- firmware 来源不可信；
- 需要绕过签名/保护；
- 需要跨 board/subsystem 强刷；
- 你无法解释写入失败后的恢复方案。

本课程不把解除这些 stop condition 的固件绕过步骤作为主线技能。

## L0 作业

给一个假设 listing 建：
- seller claims；
- photos/labels；
- device/subsystem evidence；
- firmware evidence；
- mismatch matrix；
- purchase risk。

## Retrieval Practice

1. 同一 GPU 芯片为什么可以存在多个不兼容 board/VBIOS？
2. VBIOS version 字符串相似为什么还不够？
3. 为什么先保存 identity/evidence 比“网上找个 BIOS 刷进去”重要？
4. 哪些 UNKNOWN 应直接阻止购买/写入？

## 完成证据

一份 Firmware Risk Dossier，最终只能：
- IDENTITY-CONSISTENT；
- REVIEW；
- BLOCKED。

不是“刷写成功”证书。

## Sources

- NVIDIA nvidia-smi documentation: https://docs.nvidia.com/deploy/nvidia-smi/index.html
- Linux PCI IDs/sysfs documentation可作为 OS identity 入口；
- 目标 OEM/GPU 厂商手册优先于第三方 firmware 数据库。


## Expected outcome

形成 read-only firmware identity dossier，能说明“当前看到什么、官方/OEM 应该是什么、哪里一致、哪里未知或冲突”。

## Failure recovery

拿不到可信 VBIOS/OEM 来源时停止在 UNKNOWN；不要为了“验证”去强刷、跨型号刷写或绕过厂商保护。

## What this does NOT prove

版本号相同不证明板卡未维修；版本号不同也不自动证明假卡或坏卡。Firmware forensic evidence 只是整体验收的一部分。

## No-hardware path

可用公开 OEM/VBIOS 样本练习字段比较，但必须标成 historical/sample，不冒充自己的设备。
