# Challenge 11 — 从课程 Evidence 到第一个 Upstream Contribution

硬件等级：L0–L2  
风险：safe  
成本：0

## Goal

毕业后的最高 transfer 不是“自己有 fork”，而是能把真实问题变成上游愿意 review 的：
- bug report；
- reproduction；
- docs fix；
- test；
- small patch；
- PR。

## 1. 先读项目规则

找：
- CONTRIBUTING；
- issue template；
- code style；
- tests；
- supported platforms；
- CLA/DCO（如果有）。

课程规则不能覆盖 upstream 规则。

## 2. 从小贡献开始

很好的第一贡献：
- 文档与实际 CLI 不一致；
- 可复现 bug 的 test；
- 错误信息改善；
- supported-device docs；
- tiny compatibility fix。

不需要第一 PR 就重写 GPU backend。

## 3. Issue quality

Bug report 至少：
- exact commit/version；
- OS/driver/device；
- build command；
- model/input identity；
- minimal reproduction；
- actual behavior；
- expected behavior；
- logs；
- 是否能复现。

不要贴含隐私/API key 的完整日志。

## 4. PR quality

PR 尽量：
- 一个问题；
- 一个清楚 rationale；
- 小 diff；
- test；
- before/after；
- no unrelated formatting；
- known limitations。

## 5. Review 是开发的一部分

收到 change request：
- 先确认技术点；
- 更新同一个 PR；
- 补 test/evidence；
- 不把 review 当“谁赢了”。

PR 不被 merge 也可以是成功学习 Evidence。

## 6. 回馈课程

如果你发现课程命令过期、某架构 assumption 错、新 backend 支持改变：

先用 primary/upstream Evidence 修课程，再考虑 Intelligence update。

## Retrieval Practice

1. 为什么 minimal reproduction 比长篇抱怨更有用？
2. 第一个贡献为什么 docs/test 往往比大 feature 更适合？
3. upstream 不接受 patch 为什么不等于你的实验没价值？
4. PR 中为什么要把 unrelated cleanup 拆掉？

## 完成证据

任选：
- 一个高质量 issue draft；
- 一个 docs/test PR；
- 一个小 code PR。

保存：
- issue/PR link 或本地 draft；
- reproduction；
- tests；
- review changes；
- learning note。

## Sources

- GitHub — Finding ways to contribute: https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github
- GitHub — Contributing to open source: https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-open-source


## Expected outcome

形成一个最小、可复现、尊重项目规则的 issue/PR：问题清楚、Evidence 完整、change scope 小、测试与文档匹配。

## Failure recovery

维护者指出方向错误时，先复现反馈并缩小 patch；不要为了“贡献成功”扩大 scope 或与 review 对抗。

## What this does NOT prove

PR 被 merge 不等于你的方案在所有环境最优；未 merge 也不等于学习失败。

## No-hardware path

文档、测试、错误信息、复现 fixture 都可以成为有效贡献，不要求 GPU。
