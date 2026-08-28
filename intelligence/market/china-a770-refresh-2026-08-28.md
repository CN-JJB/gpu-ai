# China A770 Market Refresh — 2026-08-28

Purpose: preserve the evidence behind the append-only A770 market refresh.

## Previous production observation

```text
record:
market:cn:a770-16g:secondary:2026-08-21

reported value:
1450 CNY

source:
https://post.smzdm.com/p/axklwq32/
```

This record remains in the catalog as history.

It now points to:

```text
market:cn:a770-16g:secondary:2026-08-25
```

through `superseded_by`.

## Refreshed observation

Source:
- https://post.smzdm.com/p/agg4xrq3/

Observed:
- 2026-08-25

Captured:
- 2026-08-28

Current supported secondary claim:

```text
A770 16GB Xianyu asking/listing signal
roughly 1400 CNY
after being around 1200 CNY
```

Production record:

```text
market:cn:a770-16g:secondary:2026-08-25
price = 1400 CNY
market evidence = M1
revalidate_after = 2026-09-01
```

## Evidence boundary

This is:

```text
SECONDARY_REPORTED
```

with:

```text
direct_listing_capture=false
confirmed_sale=false
```

Do not call it:
- direct Xianyu median;
- confirmed sale price;
- current fair value.

## Lineage

```text
2026-08-21 / 1450
        ↓ superseded_by
2026-08-25 / 1400
```

This does not claim a precise -50 CNY market move.

The two sources are weak secondary observations with different wording/sample context.

The lineage only establishes which dated observation is newer for current watch use.
