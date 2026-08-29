# Foundation 00 — 如何使用这门课

## 你不是在准备考试

这门课训练的是：

~~~text
看到陌生硬件/模型
→ 定义问题
→ 找可信资料
→ 建最小模型
→ 做实验
→ 保存 Evidence
→ 做有边界的结论
~~~

因此“记住 RTX 3090 有多少 CUDA Core”不是核心能力。

## Lesson / Reference / Intelligence / Evidence 的区别

### Lesson
教稳定因果和解决问题的方法。

### Reference
查表、公式、术语和复用 checklist。

### Intelligence
会过期的市场价、当前软件兼容、当前模型/硬件动态。

### Evidence
你这一次实验真实产生的文件、hash、日志、配置、测量。

不要把四者混在一起。

## 读课方式

每节 Lesson：

1. 先回答“真实问题”；
2. 只学解决它需要的原理；
3. 做 L0 或真实实验；
4. 不看正文回答 Retrieval Practice；
5. 填结果/Evidence；
6. 写一个 non-claim：这次结果不能证明什么；
7. 尝试换一个硬件/模型重新解释。

## 真机暂时做不了怎么办

标记：

~~~text
DEFERRED-HARDWARE
~~~

并保存：
- 你认为实验要改哪个变量；
- 预期观察什么；
- 哪些结果会推翻你的假设。

然后继续课程。

以后有硬件再补真实 Evidence。

## 卡住怎么办

不要连续重读整页。

先定位：
- 哪个术语不懂？
- 哪个箭头因果断了？
- 哪个公式不知道单位？
- 哪一步命令不知道发生什么？

然后只补这个最小前提。

## 学习记录建议

每个 Slice 留五行：

~~~text
我原来以为：
现在我认为：
我能用什么 Evidence 证明：
这次还不能证明：
换平台时我会先查：
~~~

这五行比复制整页笔记更有价值。


## 开课前自检

你不需要先会 Linux、Python、CUDA 或机器学习。只要你愿意做到三件事：

1. 不懂就追到“哪个最小前提没懂”；
2. 实验时保存原始 Evidence，而不是只记结论；
3. 不把 UNKNOWN 硬猜成 PASS。

如果某节需要额外前置知识，Foundation 01–05 会在需要时补上。

## Retrieval Practice

不看上文回答：

1. Lesson、Reference、Intelligence、Evidence 四者为什么必须分开？
2. “我在网上看到 RTX 3090 跑 70 tok/s”属于你的 Evidence 吗？为什么？
3. 真机暂时没有时，DEFERRED-HARDWARE 应保存哪三类信息？
4. 一次实验结果可以证明什么，为什么还必须写 non-claim？
5. 如果你卡在一个公式，应该重读整门课还是先定位哪个单位/因果箭头断了？

## 完成证据

在自己的学习记录里写下：

~~~text
我的当前机器/可用设备：
我目前最想解决的 Local LLM 问题：
我缺少的真机条件：
我会如何标记 DEFERRED-HARDWARE：
我理解 Evidence 与网上 benchmark 的区别：
~~~

没有 GPU 也可以完成 Foundation 00。

## Primary Sources / Course Contract

- 本仓库：MISSION.md
- 本仓库：docs/course/STUDENT-TEXTBOOK-COMPLETION.md
- 本仓库：learning/PROFILE.md

这三个文件定义课程目标、教材完成标准与学生学习边界。
