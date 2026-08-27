# Experiment 31 — Scenario-Specific Hardware Decision Model

硬件等级：L0

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