# Evidence — Experiment 19: China Secondhand GPU Market

状态：stable market methodology complete; L0 normalization verified; real snapshot builder ready; dated low/medium-confidence market intelligence captured.

## Claim

> Secondhand GPU price is not one scalar. A reproducible market decision must normalize exact SKU, VRAM, modification/repair cohort, condition and transaction state before computing a price distribution.

## Stable evidence model

Each price row requires:
- exact model;
- VRAM;
- cohort;
- condition;
- price state;
- date;
- source;
- seller type;
- evidence grade.

Price states:
- ASK;
- SOLD-CONFIRMED;
- DELISTED-ASSUMED;
- MERCHANT-QUOTE;
- BUYBACK;
- UNKNOWN.

## Experiment 33

Synthetic raw rows:
```
10
```

Target:
```
RTX 3090
24 GiB
STOCK
WORKING
```

Accepted:
```
6
```

Excluded:
```
4
```

Excluded categories:
- multi-SKU teaser;
- cooler-only;
- 48G VRAM-modified card;
- broken card.

Target ASK values:
```
7200
7400
7500
7600
7800
```

Verified:
```
ASK n=5
median=7500
Q1=7400
Q3=7600
range=7200-7800
```

One synthetic confirmed sale:
```
7300
```

The point is not the synthetic price. The point is that the normalization changes the meaning of the dataset.

## Experiment 34

The untouched real-market template contains one excluded placeholder.

Expected:

```
raw rows=1
normalized rows=0
excluded=1
```

The tool correctly refuses to invent a distribution.

## Current 2026 evidence

Dated snapshot:
`intelligence/market/china-used-gpu-market-2026-08-27.md`

It deliberately separates:
- M1 secondary consumer-market signals;
- M3 merchant quotes;
- missing direct Xianyu sold-price evidence.

Examples:
- secondary RTX 3090 24G August signal around ¥7,400;
- secondary A770 16G range ¥1,200–1,600;
- direct merchant V100 32G PCIe dismantled quote ¥3,100 pre-tax.

None is called a universal fair value.

## Platform inspection evidence

Current published Xianyu inspection agreement confirms third-party inspection is scope/standard based and produces a transaction reference report.

Therefore:
```
inspection service
!=
full AI-GPU memory/compute/thermal qualification
```

## Learner should reject

- search-page minimum = market price;
- multi-SKU displayed price = exact GPU price;
- asking = sold;
- delisted = confirmed sold;
- “non-mining” = verified low risk;
- modified VRAM = stock cohort;
- broken-card minimum belongs in working-card distribution;
- merchant quote = peer-to-peer fair value;
- third-party inspection replaces workload testing;
- one current article = M3 market evidence.
