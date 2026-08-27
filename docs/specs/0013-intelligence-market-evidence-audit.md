# Spec 0013 — Market Evidence Audit

Status: implemented  
Date: 2026-08-28

## Problem

A market observation with only:

```text
GPU
price
date
```

is too easy to over-interpret.

I12 preserves enough methodology metadata to expose:
- active sample size;
- middle-half asking-price range;
- source export time;
- ask-vs-sale semantics;
- freshness.

## Sample metadata

For the current GLOBAL-EBAY MEDIAN_ASK cohort:

```json
{
  "active_listings": 47,
  "range_kind": "middle-half-asking-price",
  "range_low": 1400,
  "range_high": 1520,
  "methodology": "filtered-live-ebay-asking",
  "confirmed_sale": false
}
```

The source export timestamp is also preserved.

## Descriptive sample bands

The audit tool uses non-probabilistic labels:

```text
1–9   → SMALL-SAMPLE
10–29 → LIMITED-SAMPLE
30+   → BROAD-SAMPLE
```

These are operational labels only.

They are not confidence intervals and do not claim statistical representativeness.

## Ask semantics

For MEDIAN_ASK:

```text
ASK-ONLY
NOT-CONFIRMED-SALE
```

must remain visible.

A delisted listing that the source assumes sold is not promoted to a confirmed sale record.

## Current production cohort

Source snapshot:

```text
RTX 3090
active=47
median ask=1499 USD
middle-half range=1400–1520

RX 7900 XTX
active=23
median ask=1020 USD
middle-half range=997–1080

Arc A770 16GB
active=8
median ask=330 USD
middle-half range=325–347
```

Therefore the descriptive sample bands are:

```text
RTX 3090      → BROAD-SAMPLE
RX 7900 XTX   → LIMITED-SAMPLE
Arc A770 16GB → SMALL-SAMPLE
```

## Query

```bash
python3 tools/intelligence/market_evidence_audit.py intelligence/catalog \
  --geography GLOBAL-EBAY \
  --channel secondary-aggregated-ebay-active \
  --cohort used-consumer \
  --condition used \
  --price-state MEDIAN_ASK \
  --currency USD \
  --as-of 2026-08-28
```

## Guardrail

The audit does not:
- calculate a confidence score;
- infer confirmed sales;
- declare a fair-value target;
- recommend a purchase;
- erase the difference between a sample of 8 and a sample of 47.

## Source

Dynamic source snapshot:
- RigPrice live used-GPU pages;
- exported 2026-08-25 through 2026-08-27;
- asking prices from filtered live eBay listings.

These observations remain SECONDARY evidence.