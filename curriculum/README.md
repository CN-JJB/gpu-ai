# 学生入口 — 垃圾佬 GPU × Local LLM

这是学生入口，不是项目建设日志。

你的起点可以只是：
- 会正常使用电脑；
- 会安装普通软件；
- 不要求 Linux、Python、CUDA、机器学习或高等数学；
- 不要求现在拥有独立 GPU。

## 怎么学

主线按六个阶段走：

| 阶段 | Slice | 你在解决什么 |
|---|---:|---|
| 0. 工具箱 | JIT | 看懂命令、路径、JSON、hash、单位和 Evidence |
| 1. GPU 与推理基础 | 01–13 | GPU 为什么这样执行，LLM 为什么吃显存/带宽/矩阵 |
| 2. 四生态与垃圾佬决策 | 14–23 | NVIDIA/AMD/Apple/Intel 怎么看，二手卡怎么调查和验收 |
| 3. LLM 架构与可比实验 | 24–33 | 从 config 看模型结构，冻结 tokenizer/quality/benchmark identity |
| 4. Serving 与长期运行 | 34–43 | concurrency、SLO、过载、公平、暴露、升级、监控、能耗、存储 |
| 5. 整机与毕业设计 | 44–49 | RAM/Swap、散热、二手验卡、PSU、整机 hard gates、毕业报告 |

推荐第一次学习按：

~~~text
Foundations
→ 01 → 02 → ... → 49
~~~

不要因为某个 Real Experiment 暂时没有硬件而停课。

## 两条实验路径

每个关键主题尽量有两层：

~~~text
L0 model / simulation / document exercise
→ 先学会因果与测量方法

L1–L3 real experiment
→ 以后有对应机器时补 learner-owned Evidence
~~~

真实实验暂时不能做时：

1. 完成 Lesson；
2. 完成 L0 实验；
3. 阅读 Real Experiment 的 README + EXPECTED；
4. 在学习记录中写 `DEFERRED-HARDWARE`；
5. 继续下一课。

这不是“跳过掌握”，而是把：
- 概念掌握；
- 实验设计能力；
- 真实硬件 Evidence

分成不同层次。

## 每课完成标准

一节课不是“看完 HTML”就结束。

至少完成：

~~~text
读懂真实问题
→ 做小实验/替代路径
→ 回答 Retrieval Practice
→ 产出完成证据
→ 能解释它不能证明什么
→ 能把方法迁移到另一个 GPU/模型
~~~

掌握度：

- **exposed**：看懂并能复述；
- **independent**：不看答案能完成实验/分析；
- **transfer**：换硬件、模型、backend 仍能用同一方法解决问题。

## 什么时候查 Foundations

不是先学完整 Linux/Python/数学，再进 GPU。

需要时再查：

- [01 Shell / 路径 / 进程](foundations/01-shell-paths-processes.md)
- [02 Python / JSON / SHA256](foundations/02-python-json-hash.md)
- [03 数学 / 单位 / 估算](foundations/03-math-units-estimation.md)
- [04 Git / GitHub / 一手资料](foundations/04-git-source-reading.md)
- [05 安全 / 实验纪律](foundations/05-safety-experiment-discipline.md)

先读：
- [00 如何使用这门课](foundations/00-how-to-use-course.md)

## 六个阶段的出口能力

### 01–13 后

你应该能解释：
- warp/wave 与 latency hiding；
- register/shared/LDS 与 reuse；
- bandwidth / arithmetic intensity / Roofline；
- weights/KV/VRAM；
- quant/container/backend；
- PP/TG；
- batching/cache/speculative；
- multi-GPU/interconnect；
- attention I/O；
- matrix precision。

### 14–23 后

你应该能：
- 按代际因果看 NVIDIA；
- 正确迁移到 AMD/Apple/Intel；
- 做跨厂商候选卡 dossier；
- 规范化二手市场证据；
- 写付款前/到货验收 SOP；
- 给自己设 max buy price；
- 做 one-variable A/B；
- 在四生态保留同一 Evidence contract。

### 24–33 后

你应该能：
- 从真实 config 画 decoder；
- 算 KV；
- 识别 dense/MoE、MHA/GQA/MQA、SwiGLU；
- 处理 sliding/hybrid/latent KV；
- 冻结 prompt/tokenizer/sampler；
- 设计 PPL/task quality gate；
- 写可验证 benchmark manifest。

### 34–43 后

你应该能：
- 设计 serving workload/SLO；
- 做容量规划和 admission control；
- 防止 tenant starvation；
- 安全暴露服务；
- 做 readiness/restart；
- 安全升级/rollback；
- 用 timeline + golden signals 诊断 incident；
- 计算 J/token；
- 区分 storage startup 与 steady inference。

### 44–49 后

你应该能：
- 诊断 host RAM/swap/OOM；
- 评估 sustained thermal；
- 验收二手 GPU；
- 做 PSU/platform dossier；
- 用 hard gates 判断整机；
- 写 Evidence-linked Machine Design Report。

## 学习时不要做的事

- 不背“神卡排行榜”；
- 不把 synthetic 数字冒充真实硬件数据；
- 不因为卖家描述就写 PASS；
- 不为了课程进度做危险供电/刷 BIOS/板修；
- 不把一个 tok/s 当完整 benchmark；
- 不把“当前支持”写成永久架构事实。

下一步：读 [00 如何使用这门课](foundations/00-how-to-use-course.md)，然后进入 [Lessons](../lessons/README.md)。
