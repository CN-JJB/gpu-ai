# Experiment 31 — Scenario-Specific Hardware Decision Model

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/hardware-decision-gates.svg" alt="硬件选择按 Fit → Support → Roofs → Evidence → TCO 逐层过 gate；前面的硬门槛不过，后面的跑分优势没有决策意义。">
  <figcaption>硬件选择按 Fit → Support → Roofs → Evidence → TCO 逐层过 gate；前面的硬门槛不过，后面的跑分优势没有决策意义。</figcaption>
</figure>

## 目标

证明：

```
同一组候选硬件
在不同 workload 下
可以得到不同排序
```

而且：

```
不通过 capacity/software hard gate
→ 不应该靠其他高分“补回来”
```

## 数据

`candidates.json` 里的候选全部是 synthetic。

它们故意代表不同 tradeoff：

- A：新、快、内存小；
- B：内存大、较老、软件需要 pinned stack；
- C：大统一内存、低风险但价格高；
- D：大显存/带宽好、软件成熟度中等。

不对应任何真实品牌/SKU。

## Workloads

### interactive

```
required safe memory = 18 GiB
support must be official-current or official-pinned
priority:
TG > cost > PP > risk/evidence
```

### long_context

```
required safe memory = 22 GiB
priority:
memory margin > TG > support/risk > cost
```

## 运行

```bash
python3 evaluate.py --scenario interactive
python3 evaluate.py --scenario long_context
```

## 模型

Hard gates：

```
capacity_pass
software_pass
```

Only candidates that pass are normalized/ranked.

Soft metrics：
- memory margin；
- synthetic TG roof；
- synthetic PP index；
- TCO；
- risk；
- evidence quality。

## 为什么这不是“显卡天梯”

所有数值都是 teaching units。

脚本训练的是决策顺序，而不是输出真实推荐。

## Why this experiment

“哪张卡最好”本身是个错误问题。硬件价值必须绑定 workload、容量、软件约束和个人成本。本实验让同一组 synthetic candidate 在两个场景中产生不同合法排序。

## Hypothesis

Hard gate 不通过的候选应先被淘汰；剩余候选才按场景权重比较。interactive 与 long_context 的优先级不同，因此排序可以变化。

## Fixed variables

候选数据固定，只改变 scenario。不要为某个候选临时修改 gate 或权重。

## What to observe

1. 哪些候选先因 capacity/software gate 被排除。
2. 进入 soft ranking 的候选集合。
3. interactive 与 long_context 排序为什么不同。
4. memory margin、TG、TCO、risk/evidence 如何影响结果。
5. hard gate 为什么不能被 soft score 抵消。

## Troubleshooting

- synthetic TG/PP 只是 teaching units。
- normalized score 只在同一 scenario 内有意义。
- scenario constraint 要先写，再看 candidate。
- 如果 support state 是 community-enabled，是否可接受由你的 workload policy 决定。

## Evidence to save

保存两个 scenario 输出，写一张“同一 candidate 在两个场景为什么名次变化”的解释表。

## What this proves

你会先做 feasibility，再做场景化 tradeoff 排序。

## What this does NOT prove

它不是显卡天梯，也不推荐任何真实品牌/SKU。

## No-hardware path

完整 L0。

## Transfer question

如果你的 workload 从短对话变成 64k context，为什么原本排名第一的 16GiB 新卡可能直接从排名里消失？
