# Experiment 38 — Real Candidate Watchlist

硬件等级：L0

## Goal

Maintain a manual, auditable watchlist for actual used-hardware candidates.

## Files

- `watchlist-template.csv`
- `evaluate_watchlist.py`
- `RESULT-TEMPLATE.md`

## Workflow

1. Define one workload card.
2. Calculate one scenario max sticker price.
3. Add multiple candidate alternatives.
4. For each row record:
   - exact model；
   - ask；
   - price state；
   - observed_at；
   - market evidence；
   - condition evidence；
   - fit/software/performance state。
5. Run evaluator.
6. Refresh stale price observations before paying.

## Intelligence bridge

If the candidate price comes from the Phase 4 Intelligence catalog, use:

- `INTELLIGENCE-BRIDGE.md`
- `tools/intelligence/market_evidence_gate.py`

Copy the catalog's claim-scoped `market_evidence_grade` into this lab's `market_evidence` field.

Do not infer a stronger grade from words such as "SOLD".

## No scraping requirement

Manual entries are acceptable and often safer than brittle scraping.

The evaluator never buys anything.

## Suggested refresh

For hot consumer GPUs:
```
7 days
```

For an imminent purchase:
```
refresh within 24–48h
```

when practical.

## Intelligence decision-readiness path

Experiment 38 now has machine-readable Phase 4 companions.

### Performance target

Copy:

~~~text
performance-target-policy.template.json
~~~

Then use I46/I47 to evaluate explicit PP/TG/PPL hard thresholds.

No weighted score is used.

### Personal price ceiling

Copy:

~~~text
price-ceiling-policy.template.json
~~~

I48 preserves the existing max-sticker/watch-band arithmetic but uses neutral outputs:

~~~text
WITHIN-CEILING
WATCH-BAND
ABOVE-BAND
~~~

WITHIN-CEILING is not BUY.

### Condition evidence

Stable C-grade semantics now live in:

~~~text
reference/hardware/condition-evidence-grades.md
~~~

I50 defines C3 as learner-owned, PACKET-bound, independently reproducible I44 technical evidence.

The evidence grade is separate from the card-health decision:

~~~text
C3 provenance
+
I44 ACCEPT
~~~

are separate requirements.

### Final evidence matrix

I43 combines the independent evidence components and may return:

~~~text
READY-FOR-HUMAN-REVIEW
~~~

It never performs a purchase.


## Why this experiment

Watchlist 的作用不是不停刷新最低价，而是把**当前价格证据、个人最高买入价、硬件 fit、软件、性能和 condition evidence**放在同一个可审计表里。

## Hypothesis

低于个人 ceiling 只代表价格条件可能满足；只要 fit/software/performance/condition 任一关键证据不足，就不能升级成购买结论。

## Fixed variables

先冻结 workload card、max sticker policy、目标 evidence 要求，再添加候选。不要为某条便宜 listing 临时降低验收标准。

## What to observe

- observed_at 与 freshness；
- ASK/SOLD/其他 price state；
- market evidence grade；
- condition evidence grade；
- fit/software/performance state；
- WITHIN-CEILING 与 BUY 之间的明确边界。

## Troubleshooting

- SOLD 字样不能自动提高 evidence grade。
- stale price 在付款前需要刷新。
- 手工录入可以，但必须保留 listing provenance。
- I43 READY-FOR-HUMAN-REVIEW 也不是自动 BUY。

## Evidence to save

保存 workload card、ceiling policy、watchlist CSV、listing snapshots/evidence 和 evaluator 输出。

## What this proves

你能维护一个真实、人工可复核的候选观察表，并把价格与技术证据分离。

## What this does NOT prove

它不预测未来价格，也不执行购买。

## No-hardware path

完整 L0，购买前即可做。

## Transfer question

某候选价格今天跌到 ceiling 以下，但 condition evidence 只有 C1。为什么你应该更新 watchlist，而不是立即下单？
