# Experiment 34 — Real Secondhand Market Snapshot Builder

硬件等级：L0

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