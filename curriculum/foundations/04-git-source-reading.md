# Foundation 04 — Git / GitHub / 一手资料：不会写代码也要会考古

硬件等级：L0  
风险：safe  
成本：0

## 真实问题

“网上有人说这张卡支持某功能”到底够不够？

课程证据优先级：

~~~text
官方架构/开发文档
→ 原始论文/规范
→ canonical upstream source/docs
→ maintainer issue/PR/release
→ 可复现社区测试
→ 社区经验
→ 卖家描述
~~~

## 1. Repo、commit、branch

- repository：项目历史；
- branch：可移动的开发线；
- commit：一个具体历史快照。

课程做严格实验时偏好记录 commit，因为：

~~~text
master/main 今天
!=
master/main 三个月后
~~~

## 2. README 不是全部真相

README 适合发现功能。

要判断细节时继续看：
- docs；
- source；
- release notes；
- tests；
- issue/PR。

## 3. Issue / PR 怎么读

先分：
- confirmed bug；
- feature request；
- open question；
- workaround；
- merged fix；
- unreproduced report。

一个 open issue 只能证明：
“有人报告/讨论了这个问题”。

不能自动证明：
“所有机器都有这个 bug”。

## 4. Pin exact version

Evidence 里记录：

~~~text
project
commit/tag/version
build flags
driver/runtime
~~~

否则“同一个 llama.cpp”可能已经不是同一个实现。

## 5. 找 primary source 的最短流程

遇到 claim：

~~~text
RTX 某代支持 X
~~~

优先：
1. 厂商 architecture/programming docs；
2. 对应 SDK/tool docs；
3. runtime upstream support；
4. 实测。

遇到模型结构：
1. model config；
2. model card；
3. paper/technical report；
4. runtime parser/implementation。

## 小练习

选一个开源项目：
1. 找 README；
2. 找最新 release/tag；
3. 找一个相关 source 文件；
4. 找一个 issue；
5. 分别写出这四种来源能证明什么、不能证明什么。

## Retrieval Practice

1. 为什么 branch 名不能替代 commit identity？
2. open issue 能证明什么，不能证明什么？
3. 硬件 capability 与 runtime support 为什么要查两类来源？
4. 卖家描述在证据层级里为什么最低？

## 完成证据

为一个课程 claim 写 3 层来源：
- primary;
- implementation;
- experiment plan.

## Primary Sources

- Git documentation: https://git-scm.com/docs
- GitHub Docs — commits: https://docs.github.com/repositories/committing-changes-to-your-project
