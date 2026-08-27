# ADR-0001: Repository is the external memory

## Status
Accepted

## Context
课程需要长期学习和跨 ChatGPT/Agent Session 连续性。聊天历史不应成为唯一状态源。

## Decision
Mission、术语、课程地图、当前状态、Learning Records、Evidence、Research、Experiment Cards、Specs 与 ADR 均持久化在仓库中。Session 可以丢失，仓库状态必须足以恢复工作。

## Consequences
新增 Session 必须走 bootstrap；结束重要工作必须更新当前状态。handoff 只做薄交接层，不复制仓库已有内容。
