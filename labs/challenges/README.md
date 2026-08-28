# Challenge Labs

Challenge Labs 是主线毕业后的选修/硬核课程，不是 Slice 01–49 的毕业硬门槛。

它们训练“会改造”和真正的 transfer：遇到不标准硬件、快速变化的软件或上游源码时，仍然能定义问题、找 Evidence、控制风险、做最小实验。

## 顺序

| Challenge | 主题 | 主路径门槛 | 风险 |
|---:|---|---|---|
| 01 | 老计算卡 / 特殊 GPU 兼容性考古 | L0 | safe |
| 02 | VBIOS / OEM / 工程卡只读取证 | L0/L1 | medium；默认不刷写 |
| 03 | 显存扩容 / 板级维修理论与止损 | L0 | high；真实板修非必做 |
| 04 | Triton kernel first principles | L0→L1/L2 | safe |
| 05 | FlashAttention 源码考古 | L0→L1/L2 | safe |
| 06 | 最小 backend patch / 可维护 fork | L0–L2 | safe |
| 07 | 多机垃圾佬集群 / network roof | L0→L3 | medium；隔离网络 |
| 08 | LoRA / QLoRA 低成本适配 | L0→L2/L3 | safe |
| 09 | Local RAG / retrieval Evidence | L0/L1 | safe；注意隐私 |
| 10 | Tool Calling / Agent | L0/L1 | medium；最小权限 |
| 11 | Upstream Issue / Test / PR | L0–L2 | safe |
| 12 | 本地多模态 | L0→L1/L2 | safe；注意媒体隐私 |

## 推荐路径

### 想玩老卡 / 魔改潜力

~~~text
14–23
→ 44–48
→ C01
→ C02
→ C03
~~~

C02/C03 的毕业标准是“会判断是否该停手”，不是必须刷 BIOS 或做 BGA。

### 想改 kernel / backend

~~~text
02–04
→ 12–13
→ 22–23
→ C04
→ C05
→ C06
→ C11
~~~

### 想做低成本多机

~~~text
11
→ 34–43
→ 48–49
→ C07
~~~

### 想做模型应用

~~~text
24–33
→ 34–41
→ C08 LoRA/QLoRA
→ C09 RAG
→ C10 Tool Calling
→ C12 Multimodal
~~~

## 共同规则

每个 Challenge 都要：
1. 读 README；
2. 做 L0/设计路径；
3. 回答 Retrieval Practice；
4. 对照 EXPECTED；
5. 填 [CHALLENGE-CARD.md](CHALLENGE-CARD.md)；
6. 真机缺失时允许 `DEFERRED-HARDWARE`；
7. 写 Non-claims；
8. 高风险路径必须遵守 stop conditions。

## 动态软件规则

Triton、llama.cpp RPC/tool-calling/multimodal、PEFT 等会变化。

因此 Challenge：
- 稳定原理写在课程；
- current API/flags 链到 upstream；
- 真跑时 pin commit/version；
- 不把今天的 CLI 当永久事实。

## 安全边界

Challenge 不是“危险操作许可证”。

课程不会把以下操作当作完成要求：
- 带电拆装；
- PSU 内部维修；
- 绕过 firmware/签名保护；
- 跨板型强刷；
- BGA/显存返修；
- 未隔离网络上的实验性 RPC；
- 给 agent 任意 shell/文件写权限。

能证明“应该 BLOCKED / 交给专业维修 / 换更简单方案”同样是优秀工程结果。
