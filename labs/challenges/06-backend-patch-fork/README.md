# Challenge 06 — 定向读源码 → 最小 Patch → 可维护 Fork

硬件等级：L0–L2  
风险：safe（软件）  
成本：0

## 真实问题

遇到：
- 某旧 GPU compile fail；
- backend 缺一个 op；
- 某 flag 在你的平台被禁用；
- loader 不认识一个模型字段；

你应该 fork 整个项目大改，还是先做最小 patch？

## 1. Reproduce before patch

保存：
- upstream repo + commit；
- build command；
- device/runtime；
- exact error；
- minimal model/input。

如果不能稳定复现，不进入 patch。

## 2. 找最小 owning layer

从 error/trace 找到：
- parser/loader；
- backend registry；
- op implementation；
- compile target guard；
- device capability check；
- build system。

不要一开始全库搜索“GPU”。

## 3. 先写 hypothesis

~~~text
I believe X blocks this device because Y evidence.
If I change Z only, expected outcome is ...
~~~

## 4. Minimal patch

目标：
- 小；
- 可 review；
- 不隐藏 unsupported state；
- 不把 fallback 冒充 accelerated path；
- 尽量带 test。

## 5. Verify

至少：
- before fail；
- after target case pass；
- existing relevant tests pass；
- correctness；
- performance regression check if hot path；
- exact diff retained。

## 6. Fork maintenance cost

长期 patch 要记录：
- upstream base commit；
- patch series；
- why upstream cannot be used；
- rebase conflict surface；
- removal condition。

最好的 fork 是未来能删除的 fork。

## Retrieval Practice

1. 为什么 reproduce 是 patch 的前置条件？
2. compile success 为什么不等于 functional correctness？
3. fallback “能跑”为什么不能被宣传成新 backend support？
4. 什么证据说明你的 patch 可以删掉并回 upstream？

## 完成证据

做一个**安全的小软件 patch**：
- 文档 typo / test / tiny parser guard 都可以；
- before/after；
- diff；
- tests；
- rollback；
- upstreamability note。

不要求你直接改 GPU kernel。

## Sources

- Git documentation: https://git-scm.com/docs
- GitHub pull request documentation: https://docs.github.com/en/pull-requests
- 目标项目自己的 CONTRIBUTING.md / tests / style guide 优先。


## Expected outcome

得到最小 reproducible bug、明确 hypothesis、最小 patch、before/after test 与维护成本说明。Patch 无收益或假设被推翻也属于合格结果。

## Failure recovery

如果 patch 同时改多个 subsystem，先缩小；如果无法复现 upstream behavior，停止写代码，先补 environment/build/fixture Evidence。

## What this does NOT prove

本地 patch 通过一个 case 不代表 upstream 通用正确，也不等于值得长期维护 fork。

## No-hardware path

可选择 parser/docs/test-only 小问题完成贡献闭环；不要求必须写 GPU kernel。
