# Max-Buy-Price / Watchlist Card

<figure>
  <img src="../../assets/diagrams/hardware-decision-gates.svg" alt="Max-Buy-Price / Watchlist Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Max-Buy-Price / Watchlist Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## Workload

- model:
- quant:
- context:
- concurrency:
- runtime:
- minimum PP:
- minimum TG:

## Hard gates

- FIT: PASS / FAIL / UNKNOWN
- SOFTWARE: PASS / FAIL / UNKNOWN
- PERFORMANCE: PASS / FAIL / UNKNOWN

## Total budget

```
B_total:
platform_extra:
PSU/cooling:
energy_horizon:
repair_reserve:
maintenance_reserve:
expected_resale:
```

## Sticker ceiling

```
max_sticker =
B_total
- platform_extra
- PSU/cooling
- energy
- repair_reserve
- maintenance_reserve
+ expected_resale
```

## Candidate

- exact model:
- VRAM:
- condition cohort:
- ask:
- price state:
- observed_at:
- source:
- market evidence:
- seller evidence C0-C4:

## Status

- SKIP
- NEEDS EVIDENCE
- WATCH
- BUY-CANDIDATE
- KEEP

## Keep three prices separate

- market anchor:
- negotiation target:
- absolute ceiling:

## Expiry

For hot common SKUs, refresh price evidence after ~7 days by default.
