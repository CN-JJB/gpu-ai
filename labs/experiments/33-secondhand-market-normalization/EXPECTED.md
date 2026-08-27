# Expected — Experiment 33

```bash
python3 normalize_market.py sample_listings.csv
```

Expected core result:

```text
SYNTHETIC MARKET DATA ONLY
raw rows: 10
accepted target cohort: 6
excluded: 4

[ASK] n=5 median=7500 CNY Q1=7400 Q3=7600 range=7200-7800
[SOLD-CONFIRMED] n=1 median=7300 CNY Q1=7300 Q3=7300 range=7300-7300
```

Excluded:
- multi-SKU ¥1598；
- cooler-only ¥400；
- 48G modified card ¥9500；
- broken ¥3000。

## Key lesson

If you naïvely average all ten numbers, the result is meaningless.

The correct market object is not:

```
"3090 search results"
```

but:

```
exact RTX 3090
+ 24 GiB
+ stock
+ working
+ same price state
```

All data in this lab is synthetic.