# China Used-GPU Market Snapshot — 2026-08-27

Purpose: dated market intelligence for the stable methodology in Slice 19.

## Confidence warning

This snapshot does **not** publish a direct Xianyu/Goofish sold-price median.

Reason:

```
current web-accessible evidence
does not expose a sufficiently large,
normalized, item-level confirmed-sale sample
for the target GPUs
```

Therefore this file separates:

- direct merchant quotes;
- current secondary market summaries;
- platform-policy evidence;
- missing direct peer-to-peer evidence.

Do not convert secondary claims into M3 direct market evidence.

---

# 1. August 2026 market direction

Multiple current Chinese hardware-market secondary sources describe a rising secondhand GPU market in August 2026, with especially visible movement in popular mid-range and large-VRAM cards.

A Bilibili creator with recurring monthly secondhand-GPU market videos published:
- 2026-08-01 August market update;
- 2026-08-16 mid-month update described as 黄鱼行情价格.

These are useful market signals but do not expose the full raw listing dataset in searchable text.

Market evidence:
```
M1/M2 secondary signal
```

Do not use the video title alone as a precise price source.

---

# 2. Current secondary price signals

Source:
https://post.smzdm.com/p/a825vp66/

Published:
```
2026-08-22
```

The article reports early-August secondhand-market statistics and explicitly labels the numbers as volatile reference values.

| GPU | reported August price | reported change | evidence |
|---|---:|---:|---|
| RTX 3060 12G | ¥1,650 | +¥300 | M1 secondary |
| RTX 4060 Ti 16G | ¥3,200 | +¥420 | M1 secondary |
| RTX 5060 Ti 16G | ¥4,000 | +¥695 | M1 secondary |
| RTX 3090 24G | ¥7,400 | +¥1,200 | M1 secondary |
| RTX 4090 24G | ¥18,200 | +¥2,050 | M1 secondary |
| RTX 5090 32G | ¥30,000 | +¥2,450 | M1 secondary |

Why only M1?

The article says the figures come from secondhand-platform real-time transaction statistics, but the underlying normalized item-level records are not provided.

Use these values as:

```
market direction / rough anchor
```

not:

```
verified Xianyu sold median
```

---

# 3. Intel Arc current secondary signals

Source:
https://post.smzdm.com/p/agg4xrq3/

Published:
```
2026-08-25
```

Reported current August ranges:

| GPU | reported range | evidence |
|---|---:|---|
| Arc A770 8G | ¥900–1,000 | M1 secondary |
| Arc A770 16G | ¥1,200–1,600 | M1 secondary |
| Arc B570 | ~¥1,200 | M1 secondary |
| Arc B580 12G | ¥1,400–1,800 | M1 secondary |

Another current article:
https://post.smzdm.com/p/axklwq32/

Published:
```
2026-08-21
```

reports A770 16G moving from roughly ¥1,150 to around ¥1,450 during the recent local-AI demand spike.

Course interpretation:

```
A770 16G has become a hot local-AI value target
→ price is moving
→ old price memories are unsafe
```

Still secondary evidence.

---

# 4. 3090 multi-SKU / teaser-price trap

Current search aggregation example:
https://www.xing73.com/taobao-xl-AM5AzMh2Y5_ip5Lmo5MqL5.html

The page includes listings such as:

```
"3050/3060/3070/3080Ti/3090"
display price ¥1,598
```

and another multi-generation listing displaying ¥2,050.

The same page also shows 3090-specific merchant items around:
- ¥7,900;
- ¥8,500.

This is a perfect normalization lesson.

The ¥1,598 / ¥2,050 figures must **not** enter a 3090 sample because the exact selected option is unknown.

Even the ¥7,900 / ¥8,500 entries remain:
```
ASK / merchant secondary aggregation
```
not confirmed peer-to-peer sales.

Evidence:
```
M1
```

---

# 5. Direct Chinese merchant quotes — separate cohort

Current direct source:
https://www.cplight.com/

Observed around:
```
2026-08-24 to 2026-08-27
```

Examples:

### RTX 4090 24G blower dismantled
```
¥25,500
```

State:
```
MERCHANT-QUOTE
```

### RTX 5090 32G blower dismantled
```
¥39,990
```

State:
```
MERCHANT-QUOTE
```

### A10 24G new
```
¥25,500
```

State:
```
MERCHANT-QUOTE / NEW
```

These are not peer-to-peer Xianyu prices.

They are useful for:
- enterprise/dealer replacement cost;
- unusual blower/datacenter supply;
- cross-channel spread.

They must not be averaged with personal used listings.

Evidence:
```
M3 for the quoted listing state
```

not M3 for “market fair value”.

---

# 6. V100 32G direct merchant observation

Current source:
https://www.cplight.com/category/data-center-gpu-tesla

Observed:
```
V100 32G PCIe original dismantled
¥3,100
pre-tax
```

State:
```
MERCHANT-QUOTE
```

This is particularly relevant for the course because:
- 32 GiB HBM capacity is attractive;
- Volta is now a pinned/legacy CUDA-stack purchase;
- datacenter cooling/power/host compatibility matters;
- merchant quote is not equivalent to a tested personal-sale unit.

Before calling it a “deal”, run Slice 18:
```
FIT
→ SOFTWARE
→ TG/PP
→ platform cost
→ condition
→ TCO
```

---

# 7. P40: deliberately no China price published here

Current global trackers show P40 24G asking prices around the low hundreds of USD, but that is not China-market evidence.

This snapshot did not obtain a sufficiently strong current China item-level P40 sample.

Therefore:

```
P40 China fair price = NOT ESTABLISHED
```

Do not reuse:
- an old March article;
- eBay median;
- a single AliExpress listing;

as a current Xianyu CNY median.

This missing value is intentional evidence discipline.

---

# 8. Current Xianyu inspection-service boundary

Official published buyer agreement:
https://terms.alicdn.com/legal-agreement/terms/product/20221213134628952/20221213134628952.html

The agreement describes:
- third-party inspection for eligible items;
- category-specific inspection scope/standards;
- buyer review of the inspection result;
- cases outside inspection scope;
- a validity period for the report;
- transaction/return conditions after buyer confirmation.

Course interpretation:

```
验货宝
= transaction-risk reduction tool
!= full GPU engineering validation
```

For an AI GPU still request/perform:
- exact device/VRAM identity;
- sustained workload;
- memory errors;
- thermal behavior;
- BIOS/modification history;
- driver stability.

---

# 9. Current market-risk signal

Current August 2026 secondary sources describe:
- rising used-GPU prices;
- strong local-AI demand for larger VRAM;
- especially active ¥1,000–2,000 segment;
- rapidly moving Arc A770 16G pricing.

Implication:

```
price snapshot half-life is short
```

For a purchase:
- capture direct listings on the purchase day;
- do not rely on this file alone.

---

# 10. Current provisional anchors

These are **not buy recommendations**.

| candidate | current signal | use |
|---|---:|---|
| RTX 3090 24G | ~¥7,400 secondary August signal | rough consumer large-VRAM anchor |
| Arc A770 16G | ¥1,200–1,600 secondary range | low-cost 16G Intel watchlist |
| Arc B580 12G | ¥1,400–1,800 secondary range | current Intel alternative |
| V100 32G PCIe | ¥3,100 pre-tax merchant quote | legacy 32G datacenter watchlist |
| RTX 4090 24G blower dismantled | ¥25,500 merchant quote | special dealer/blower cohort |

Never compare these rows directly without:
- condition;
- support;
- workload;
- price state;
- tax/warranty;
- platform cost.

---

# 11. Revalidation triggers

Refresh when:
- 7 days pass during a volatile market;
- direct Xianyu normalized data becomes available;
- a target purchase is within 48 hours;
- DRAM/GDDR pricing changes materially;
- new local-LLM releases increase VRAM demand;
- driver/toolkit support changes old-card value;
- major new GPU launches shift used supply.
