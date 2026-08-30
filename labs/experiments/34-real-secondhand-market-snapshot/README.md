# Experiment 34 — Real Secondhand Market Snapshot Builder

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/market-observation-cohort.svg" alt="真实市场 snapshot 要固定观察时间、候选定义和异常值处理，避免把零散最低价当成稳定市场价。">
  <figcaption>真实市场 snapshot 要固定观察时间、候选定义和异常值处理，避免把零散最低价当成稳定市场价。</figcaption>
</figure>

## Goal

Turn manually captured marketplace observations into a reproducible snapshot without scraping or inventing data.

## Why manual capture first?

Marketplace pages:
- change frequently；
- may require login；
- can expose multiple option prices；
- can have anti-bot controls；
- may not expose confirmed sold prices publicly。

For a course, a small raw CSV with provenance is better than a brittle scraper that silently records wrong prices.

## Step 1 — copy template

```bash
cp market-sample-template.csv market-2026-XX-XX.csv
```

## Step 2 — capture at least 10 normalized records per common SKU

Fields include:
- timestamp；
- marketplace；
- listing_id/url；
- exact model；
- VRAM；
- cohort；
- condition；
- seller type；
- price state；
- asking/sold price；
- condition evidence；
- market evidence grade；
- notes。

## Step 3 — reject bad rows explicitly

Set:

```
include_normalized = false
```

and fill `exclude_reason`.

Never delete the row just because it is inconvenient.

Examples:
- multi-SKU；
- accessory；
- broken；
- modded VRAM；
- duplicate；
- bundle；
- unknown exact price。

## Step 4 — summarize

```bash
python3 summarize_market.py market-2026-XX-XX.csv
```

The script reports per exact normalized cohort:
- n；
- median；
- Q1-Q3；
- observed range；
- price state。

## Step 5 — publish only with limitations

Snapshot must state:
- date/window；
- source；
- sample size；
- direct vs secondary；
- asking vs sold；
- excluded count；
- missing channels。

## Important

If you only have ASK prices, say:

```
ASK median
```

not:

```
market transaction price
```

If a secondary article says “闲鱼成交均价” but raw platform records are unavailable, grade it M1/M2 and describe it as a secondary claim.

## Why this experiment

“市场价”必须绑定时间、平台、cohort、condition 和 price state。这个实验训练你把手工观察变成可重算 snapshot，同时保留被排除的脏数据和原因。

## Hypothesis

只有 exact normalized cohort 内的记录才可以组成分布；ASK、SOLD-marked、confirmed transaction 等不同 price state 必须分开，不能混成一个“成交价”。

## Fixed variables

开始采集前先写明 SKU/cohort、时间窗口、平台、币种与 inclusion rule。采集过程中不要因为某条价格太高/太低临时改变规则。

## What to observe

1. included/excluded 数量。
2. 每个 exclude_reason。
3. ASK 与其他 price state 的样本数和分布。
4. median/Q1/Q3 对极端值的敏感度。
5. sample size 与缺失渠道对结论可信度的限制。

## Troubleshooting

- 多 SKU 页面必须确认 exact option price。
- bundle/accessory/broken/modded 不应混进 stock working cohort。
- “已售”展示价格不自动等于最终成交金额。
- 同一 listing 重复抓取要去重，但保留 provenance。

## Evidence to save

保存原始 CSV、采集日期/规则、summarizer 输出、excluded rows 与 limitations。不要只保存最终中位数。

## What this proves

你会建立一个时间限定、定义明确、可复算的真实市场 snapshot。

## What this does NOT prove

它不产生永久“公允价格”，也不证明未公开的成交金额。

## No-hardware path

完整主路径，不需要拥有 GPU。

## Transfer question

同一天两个平台的 RTX 3090 ASK median 差很多，你应该直接平均，还是先检查 cohort、地区、卖家类型和 price state？
