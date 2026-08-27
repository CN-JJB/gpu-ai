# Agent Instructions

## Mission first

任何课程、工具、研究或架构工作开始前，先读取 `MISSION.md`。不要为了“内容丰富”扩大已经冻结的 v1 范围；新想法进入 backlog。

## Required context

按任务读取最少必要上下文：

- 术语或领域边界：`CONTEXT.md`
- 学习路线：`COURSE-MAP.md`
- 当前工作/学习状态：`learning/CURRENT.md`
- 课程写作：对应 Lesson/Lab + `resources/RESOURCES.md`
- 动态数据：`intelligence/`，不要把易腐数据写死进稳定 Lesson
- 重大架构：先读 `docs/adr/`

## Agent skills

本仓库使用 Matt Pocock stable skill pack。完整路由见 `skills/SKILL-MAP.md` 与 `skills/WORKFLOWS.md`。

必须遵守：
- 需求还不清楚：`grill-me`；有既有文档时优先 `grill-with-docs`。
- 已讨论清楚、要沉淀规范：`to-spec`，不要重新采访。
- 写真实课程内容或动态情报：`teach` + `research`；优先一手来源并保留 provenance。
- 改统一术语/领域边界：`domain-modeling`，同步 `CONTEXT.md`；ADR 只用于难逆、意外、存在真实权衡的决定。
- 超出单次上下文的大任务：`wayfinder`。
- 实现工具：`prototype`（需要先验证时）→ `to-spec` → `to-tickets` → `implement`；适用时用 `tdd`、`diagnosing-bugs`、`code-review`。
- 学生没听懂：`wait-what`，不要简单重复原文。
- 跨 Session：更新仓库状态后使用 `handoff`；handoff 只引用已存在产物，不重复大段内容。
- 写或改 `AGENTS.md` / `SKILL.md`：遵循 `writing-for-agents`，用清晰 context pointer 控制上下文负担。

不要机械调用全部 skills；只调用当前任务能产生价值的 skill。

## Content quality

真实课程内容必须：
1. 从真实问题开始。
2. 原理只讲到能解释实践和迁移。
3. 有实验/练习和明确反馈。
4. 标注硬件门槛、成本、风险、替代路径。
5. 关键事实有来源。
6. Benchmark 有完整测试条件，不能只报一个数字。
7. 能产生 Evidence。
8. 区分稳定知识与动态情报。

## Session bootstrap

新 Session：
1. Read MISSION.md
2. Read CONTEXT.md
3. Read relevant COURSE-MAP section
4. Read learning/PROFILE.md
5. Read learning/CURRENT.md
6. Read recent relevant learning records/evidence
7. Continue from current ZPD / current build task

## Session close

重要工作结束：
1. 更新 learning/CURRENT.md
2. 新增必要的 learning/build record
3. 引用新 Evidence/Research/Spec
4. 更新 next step
5. 如需跨 session，生成 handoff
