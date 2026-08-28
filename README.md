# 垃圾佬 GPU × Local LLM Course

一套面向电脑爱好者的、自学优先的 GPU 与本地大语言模型实践课程。

本项目不是“背型号”和“抄命令”的教程。最终目标是培养五种可迁移能力：

> **会理解 → 会调查 → 会选择 → 会实践 → 会改造**

## 核心路线

- GPU 架构演进与现代 GPU 执行/内存模型
- 二手 GPU 调查、验卡、诊断、TCO 与垃圾佬决策
- LLM 架构演进、量化、KV Cache、推理与现代优化
- Linux 主平台上的长期本地 LLM 服务
- 单机多 GPU 为主线，多机低成本集群为硬核支线
- 开源项目考古、源码定向阅读、patch/fork 与兼容性处理
- 硬件情报站 + LLM 部署情报站 + 可复现 Benchmark
- 主线里程碑 + Challenge Lab + 毕业项目

## 我是学生，从这里开始

**第一入口：[curriculum/README.md](curriculum/README.md)**

不要求你先会 Linux、Python、CUDA、机器学习或高等数学，也不要求现在就有独立 GPU。

第一次按：

~~~text
学生入口
→ Foundations（按需）
→ Slice 01–49
→ 每节实验 / Retrieval Practice / Evidence
→ Graduation Capstone
→ Challenge Labs（选修）
~~~

真实 GPU 实验暂时没有硬件时，按课程标记 `DEFERRED-HARDWARE`，先完成 L0/设计路径并继续下一课。

## 项目建设者 / 维护者入口

1. [MISSION.md](MISSION.md) — 为什么做、为谁做、成功标准和边界
2. [COURSE-MAP.md](COURSE-MAP.md) — 能力图与课程主线
3. [CONTEXT.md](CONTEXT.md) — 项目统一术语
4. [AGENTS.md](AGENTS.md) — Agent / ChatGPT 工作规则
5. [skills/SKILL-MAP.md](skills/SKILL-MAP.md) — skills 与项目任务如何映射
6. [learning/CURRENT.md](learning/CURRENT.md) — 当前建设/学习状态

## 仓库是外部记忆

Chat session 可以结束，项目状态不能丢。重要决定、学习证据、实验、研究来源与当前任务都沉淀在仓库中。

## 仓库说明

本仓库是独立维护的“垃圾佬 GPU × Local LLM”课程工程，不保留原 fork 关系。第三方 skills、外部代码与研究资料的来源/许可信息继续在对应文件中记录。