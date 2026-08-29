# Foundation 05 — 安全与实验纪律

硬件等级：L0  
成本：0

## 1. 课程默认安全边界

主线默认只做：
- 普通用户态软件；
- 官方/正常驱动；
- 只读硬件信息；
- 正常 benchmark/stress；
- 标准硬件安装；
- 已有机器上的受控实验。

主线不要求：
- 带电拆装；
- PSU 内部维修；
- 自制高功率转接；
- VBIOS 强刷；
- 绕过保护；
- 板级焊接；
- 显存更换。

这些如果以后进入 Challenge Lab，会单独定义门槛和风险；不是完成主线的条件。

## 2. One-variable discipline

Baseline 和 candidate 比较时：

~~~text
只改变一个有意义的 semantic variable
~~~

其他条件尽量固定。

否则：
“更快了”
不能回答：
“为什么更快”。

## 3. Warm-up 与 repeated runs

一次 timing 很容易受：
- cold startup/cache；
- 后台进程；
- clock boost；
- thermal state

影响。

所以 benchmark 常要求：
- warm-up；
- repeated runs；
- raw values；
- summary；
- telemetry。

## 4. 先 correctness，再 performance

如果输出错了：

~~~text
10000 tok/s
~~~

也没有意义。

Kernel/quant/backend A/B 先过 correctness/quality gate。

## 5. 不删失败 Evidence

失败输出通常能告诉你：
- unsupported flag；
- runtime fallback；
- OOM；
- wrong model；
- thermal/power issue。

正确做法：
- 保留；
- 标 BLOCKED/FAIL；
- 修输入；
- 新建干净输出目录重跑。

不是编辑 sealed evidence 让它 PASS。

## 6. Non-claim

每次结论都加一句：

~~~text
This evidence does not prove...
~~~

例如：
- 10 分钟稳定不证明一年 24/7；
- hash 一致不证明 benchmark 诚实；
- seller photo 不证明 VRAM 健康；
- synthetic test 不证明真实 GPU 性能。

## 7. 二手交易安全

技术课程不能消除交易风险。

付款前：
- 保留平台规则；
- 保存 listing/聊天/承诺；
- 明确退货/验货窗口；
- 不把卖家自述升级成实测。

到货：
- 先外观/身份；
- 再正常负载；
- 发现异常保留证据；
- 不用危险改造“抢救”来不及退的卡。

## Retrieval Practice

1. 为什么失败数据不应该删除？
2. 为什么 correctness 是 performance 的前置 gate？
3. one-variable A/B 为什么比“调一堆参数试试”更慢但更有价值？
4. 一次 10 分钟 soak PASS 可以证明什么、不能证明什么？

## 完成证据

为未来第一次真实 GPU benchmark 写一份 8 项 preflight checklist。

## Primary Sources

具体硬件安全与接线始终以目标 PSU/GPU/主板厂商手册为准。

## Mental Model：先分“可逆软件实验”与“可能造成不可逆损失的硬件动作”

课程默认升级路径：

~~~text
read-only inspection
→ user-space software
→ normal benchmark
→ reversible config
→ standard installation
→ advanced / risky challenge only when explicitly designed
~~~

越往下风险越高，Evidence 要求和止损条件也越严格。

## 实验 Stop Conditions

出现以下情况时，先停实验而不是“再跑一次看看”：

- 异常气味、冒烟、火花；
- 线材或接头异常发热、变色；
- 风扇停转同时温度持续上升；
- PSU/GPU/主板反复掉电；
- 文件系统或模型 Evidence 正在被错误命令覆盖；
- 工具明确给出 BLOCKED/unsafe；
- 你无法解释下一步动作是否可逆。

软件 crash 通常可以调查；电气异常不能用“多试几次”建立统计信心。

## Worked Example：Benchmark 更快了，但同时改了 4 个变量

Baseline：

~~~text
driver A
backend X
quant Q4
power limit default
~~~

Candidate：

~~~text
driver B
backend Y
quant Q5
power limit changed
~~~

即使 candidate 快 30%，你也不能回答“哪个改动导致更快”。正确做法是回到 baseline，逐个变量 A/B，并为每一步先过 correctness/quality gate。

## Failure Evidence 为什么尤其重要

假设一次运行 OOM：

~~~text
FAILED run
model artifact = exact
context = 32768
KV type = exact
available VRAM = recorded
stderr = preserved
~~~

这不是“废数据”。它可以证明在该条件下 fit gate 失败，并帮助你设计下一次只改变 context 或 KV type 的实验。

## 二手 GPU 到货止损顺序

~~~text
identity / external inspection
→ normal power-on
→ basic device enumeration
→ conservative memory/load test
→ sustained LLM workload
→ only then consider tuning
~~~

如果还在退货窗口，优先保存 Evidence 和判断是否退货；不要先拆散热器、刷 VBIOS、改焊或做会破坏争议证据的操作。

## No-hardware fallback

写一份“未来真实 GPU benchmark preflight + stop conditions”即可完成 Foundation 05。没有 GPU 不影响掌握实验纪律。

## Decision Rule

一个结果只有同时满足：

~~~text
safe
+ correct
+ comparable
+ reproducible enough
~~~

才有资格进入性能解释。任何一项失败都应先 BLOCKED，而不是拿速度数字继续比较。

## Transfer

同一纪律可迁移到量化 A/B、driver upgrade、多 GPU、散热/功耗优化、二手验卡、kernel patch、服务升级/回滚。核心一直是：先保护人和设备，再保护 Evidence，再追性能。

## 完成模板

~~~text
Experiment:
Safety boundary:
One semantic variable:
Fixed variables:
Correctness/quality gate:
Warm-up/repetitions:
Raw evidence:
Stop conditions:
Rollback/recovery:
What this does NOT prove:
~~~

