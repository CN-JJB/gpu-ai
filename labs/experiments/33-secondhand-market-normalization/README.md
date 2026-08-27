# Experiment 33 — Normalize a Messy Secondhand GPU Search

硬件等级：L0

## 问题

搜索“3090”得到 10 个价格：

```
1598
400
3000
7200
7300
7400
7500
7600
7800
9500
```

能不能直接算平均值？

不能。

这些记录里故意混了：

- multi-SKU bait；
- cooler-only；
- broken card；
- stock 3090 24G；
- 3090 48G VRAM mod。

## 运行

```bash
python3 normalize_market.py sample_listings.csv
```

脚本默认只统计：

```
exact_model = RTX 3090
vram_gib = 24
cohort = STOCK
condition = WORKING
```

并把：

```
ASK
SOLD-CONFIRMED
```

分开。

## 目标

学会：

```
search result
!= market sample
```

只有 normalization 后才有 price distribution。

## 完成标准

能解释每条 excluded row 为什么不能进入 stock 3090 24G working-price sample。