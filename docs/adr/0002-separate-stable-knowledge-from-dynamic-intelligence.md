# ADR-0002: Separate stable knowledge from dynamic intelligence

## Status
Accepted

## Context
GPU 二手价格、驱动支持、模型、量化、推理框架和社区 benchmark 会快速变化；原理和判断方法变化较慢。

## Decision
Lessons/Reference 保存稳定知识与判断方法；`intelligence/` 保存带来源、日期、测试条件与可信度的动态数据。两者通过链接和查询连接，不把“当前价格/当前最好模型”写死在长期 Lesson。

## Consequences
更新情报不要求重写课程；Lesson 引用动态结论时必须声明数据日期。
