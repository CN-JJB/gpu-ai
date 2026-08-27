# Skill Map

上游锁定：`mattpocock/skills` @ `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`。

## 核心高频

| 任务 | Skill |
|---|---|
| 从模糊想法澄清需求 | grill-me |
| 基于已有文档继续澄清并维护领域语言 | grill-with-docs |
| 长期教学、ZPD、lesson/records/resources | teach |
| 一手资料研究与带引用的研究笔记 | research |
| 统一术语、CONTEXT、必要 ADR | domain-modeling |
| 超长项目规划与跨上下文推进 | wayfinder |
| 已讨论清楚后沉淀正式规范 | to-spec |
| 规范拆成可独立推进 tickets | to-tickets |
| 工程实现 | implement |
| 跨 session 交接 | handoff |
| Agent 文档/skills 的写法 | writing-for-agents |
| 学生没听懂时补前提、换解释 | wait-what |

## 工程按需

prototype、tdd、diagnosing-bugs、codebase-design、code-review、improve-codebase-architecture、resolving-merge-conflicts、wizard、setup-pre-commit、git-guardrails-claude-code、triage。

## 课程按需

scaffold-exercises 用于练习骨架，但其上游默认 TypeScript/ai-hero lint 约定**不能机械照搬**；本项目只复用 problem/solution/explainer、编号和可验证练习的思想，并由 project skill 适配本课程。

## 低相关/条件触发

- migrate-to-shoehorn：仅未来 TypeScript 测试真的采用对应库时。
- to-questionnaire：答案主要掌握在外部专家/玩家手中，需要结构化收集经验时。
- ask-matt：不知道该选哪个 Matt skill 时。

## 重要规则

1. 写真实 GPU/LLM 内容时才触发 research；架构讨论不伪装成资料研究。
2. research 结果先成为 research note / source note，再经过教学设计进入 Lesson。
3. domain-modeling 只在改变领域语言时触发；只读取 CONTEXT 不算调用。
4. handoff 不替代 CURRENT/records/evidence，它只指向它们。
5. 工具开发按复杂度选择流程，不给十行脚本强加完整 ticket 仪式。
