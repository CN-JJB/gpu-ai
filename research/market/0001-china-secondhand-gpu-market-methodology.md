# Research Note 0013 — China Secondhand GPU Market Methodology

日期：2026-08-27

## Research question

二手 GPU 市场里最常见的错误不是“不会砍价”，而是把不同含义的数据混成一个价格：

```
挂牌价
最低变体引流价
成交价
商家回收价
坏卡/维修卡价格
魔改卡价格
整机拆分价格
```

本课程要建立一个可复现的市场调查方法，使价格情报能进入 Slice 18 的：

```
FIT
→ SOFTWARE
→ PP/TG
→ TCO
→ RISK
→ BUY IF PRICE <= X
```

而不是做“今天某卡多少钱”的口播。

---

# Part I — Price identity

Every price record must answer:

1. exact GPU?
2. exact VRAM?
3. exact board/variant if relevant?
4. working condition?
5. original or modified?
6. bare card or bundle/system?
7. asking or sold?
8. date?
9. marketplace?
10. seller type?
11. evidence URL/screenshot/raw record?

Without these fields, the price is not normalized market evidence.

## Price states

Use one of:

### ASK
Active asking price.

### SOLD-CONFIRMED
Platform explicitly marks a completed sale at a known price.

### DELISTED-ASSUMED
Listing disappeared or an external tracker assumes sale.

### MERCHANT-QUOTE
Dealer/wholesale/repair-market quote.

### BUYBACK
Dealer purchase/buyback offer.

### UNKNOWN
Price exists but transaction state is unclear.

Do not collapse them.

---

# Part II — Exact-SKU normalization

## Multi-SKU listing trap

A listing titled:

```
RTX3050 / 3060 / 3070 / 3080Ti / 3090
¥1598
```

does not mean RTX 3090 costs ¥1598.

The displayed number may be:
- cheapest variant;
- deposit;
- accessory;
- out-of-stock bait option;
- repaired/bare-board option.

Rule:

```
multi-SKU listing
→ reject from price sample
unless exact option price is captured
```

## VRAM variants

Never mix:
- A770 8 GB and 16 GB;
- 4060 Ti 8 GB and 16 GB;
- 5060 Ti 8 GB and 16 GB;
- MI50 16 GB and 32 GB;
- V100 16 GB and 32 GB;
- A100 40 GB and 80 GB.

For local LLM, VRAM is often a first-order decision variable.

## Modified VRAM

Create a separate cohort:

```
stock
modified-VRAM
repair/reball
engineering-sample
OEM/custom
```

A 2080 Ti 22 GB mod is not the same product as a stock 2080 Ti 11 GB.

---

# Part III — Condition normalization

Use a structured condition state.

## C0 — Unknown
No credible test/condition evidence.

## C1 — Powers on / seller claim
Basic seller statement only.

## C2 — Functional evidence
Current video or screenshots show:
- device identity;
- driver;
- VRAM;
- benchmark/stress run.

## C3 — Strong pre-sale evidence
C2 plus:
- memory test;
- sustained load;
- temperatures;
- no artifact/driver reset;
- serial/board photos;
- current timestamp/order-specific proof.

## C4 — Third-party inspection / local verification
Independent inspection or buyer's own test before final payment.

Condition score is not a warranty.
It only describes evidence strength.

---

# Part IV — Seller-claim vocabulary

Seller text should be stored separately from verified facts.

Examples:

```
"个人自用"
"非矿"
"网吧拆机"
"工作室退役"
"服务器拆机"
"无修"
"换过硅脂"
"换过显存"
"显存升级"
"包过测试"
```

Each is:

```
seller_claim
```

until independently verified.

Do not translate:

```
"非矿"
→ low risk
```

or:

```
"服务器拆机"
→ bad
```

The real question is current board condition and testability.

---

# Part V — Asking price vs transaction price

## Asking price

Useful for:
- current seller expectations;
- supply depth;
- outlier detection;
- negotiation starting points.

Not equal to:
- actual market clearing price.

## Sold-confirmed

Stronger for:
- actual willingness to pay.

But still normalize:
- condition;
- seller reputation;
- shipping;
- accessories;
- warranty;
- exact variant.

## Delisted assumed sold

Use lower confidence.

A delisted item may have:
- sold elsewhere;
- been withdrawn;
- repriced/relisted;
- been removed by platform.

---

# Part VI — Sample construction

## Recommended window

For a fast-moving GPU market:

```
7-day snapshot
+ 30-day trend
```

Do not combine six-month-old prices with current listings without labeling time.

## Minimum useful sample

For a rough price band:

```
n >= 10 normalized records
```

Preferred:

```
n >= 20
```

for a common SKU.

Rare datacenter/modded cards may have smaller samples; confidence must fall accordingly.

## Duplicate removal

Remove:
- same seller relisting same serial/board;
- mirrored merchant feeds;
- identical photos/description;
- aggregator duplicate pages.

---

# Part VII — Outlier handling

Do not simply take minimum and maximum.

For normalized samples:

1. inspect obviously invalid listings;
2. remove non-product bait/accessories;
3. compute median;
4. compute quartiles / IQR;
5. retain a visible observed range;
6. explain exclusions.

Useful outputs:

```
n
median ASK
Q1-Q3 ASK
confirmed SOLD median if available
observed min/max
excluded count
```

## Why median

A few:
- fake-low listings;
- premium sealed cards;
- repair shops;
- collector variants;

can distort the mean.

---

# Part VIII — Market evidence grading

## M3 — Strong market evidence
- direct platform listing/transaction record;
- exact SKU/condition captured;
- current date;
- sample raw data preserved.

## M2 — Useful secondary
- reputable current market tracker;
- transparent aggregation methodology;
- current dated community price sheet with reproducible source.

## M1 — Weak
- single video/article anecdote;
- unattributed “闲鱼均价”;
- seller quote;
- search-engine snippet without exact option.

## M0 — Unknown
No source/provenance.

A dated intelligence snapshot must show its market evidence grade.

---

# Part IX — Platform protection is not a substitute for GPU testing

Current Xianyu/Goofish inspection-service agreement describes a third-party inspection process for eligible goods.

Important limits in the agreement:
- coverage depends on category/service page;
- inspection uses a defined scope/standard;
- report is a transaction reference;
- some properties can be outside inspection scope;
- buyer still needs to compare the result and make the purchase decision;
- report has an effective period;
- after confirmation, return rules are constrained by the transaction agreement.

Course rule:

```
inspection service
!= full GPU engineering validation
```

For a local-LLM GPU, you still care about:
- exact VRAM;
- memory errors;
- sustained compute;
- thermals;
- driver resets;
- power behavior;
- BIOS;
- repair/modification.

---

# Part X — Pre-payment GPU verification

For a normal dGPU candidate, request/capture:

## Identity

```
GPU-Z / nvidia-smi / rocminfo / sycl device
exact board photos
serial label
VRAM size
BIOS version/hash if unusual
```

## Functional

```
display output if applicable
driver installs
benchmark completes
no artifacts
no resets
```

## Sustained load

At least one meaningful sustained run:
- graphics load;
- compute load;
- memory-heavy load.

Do not prescribe one universal “3-hour FurMark proves good” rule.

A graphics-only stress test may miss memory/compute-specific failures.

## Memory

For high-value AI cards:
- run a GPU memory test where available;
- record ECC counters for datacenter cards;
- test close to full VRAM allocation if safe and practical.

## Thermals

Record:
- core temperature;
- hotspot if exposed;
- memory junction if exposed;
- fan behavior;
- throttling.

---

# Part XI — Risk cohorts

Separate market cohorts because risk changes required discount.

### Retail normal
Stock consumer/workstation board.

### Datacenter retired
P40/P100/V100/A-series/Instinct/etc.
May need:
- passive cooling solution;
- EPS/PCIe power knowledge;
- no display output;
- server history.

### Mining/workstation heavy-use
History itself is not a verdict.
Condition evidence matters.

### Repair/reball
Requires larger discount and stronger testing.

### Modified VRAM
Treat as a custom product.
Need:
- modder reputation;
- memory topology;
- BIOS/driver behavior;
- full-VRAM tests;
- workload proof.

### Engineering sample / odd OEM
Software/BIOS/repairability risk can dominate.

---

# Part XII — Buy threshold

Instead of:

> “This card is worth ¥X.”

Compute a personal threshold.

```
max_buy_price
= value of target capability
- platform extras
- repair reserve
- software-maintenance discount
- risk discount
```

Then compare with normalized market evidence.

Decision:

```
market median > threshold
→ SKIP / WAIT

good listing <= threshold
+ hard gates pass
+ evidence strong enough
→ BUY candidate
```

---

# Part XIII — Current-market snapshot belongs elsewhere

Stable methodology:
`research/market/0001-china-secondhand-gpu-market-methodology.md`

Dated prices:
`intelligence/market/china-used-gpu-market-YYYY-MM-DD.md`

Never freeze a 2026 price inside a stable lesson.
