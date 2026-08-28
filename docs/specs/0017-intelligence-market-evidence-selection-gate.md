# Spec 0017 — Market Evidence Selection Gate

Status: implemented  
Date: 2026-08-28

## Goal

Bridge the stable Slice 19 / Experiment 38 market-evidence grades into the dynamic Intelligence catalog.

Do not invent a second grading system.

## Stable grades reused

From the stable secondhand-market methodology:

```text
M3 — direct normalized platform evidence
M2 — current transparent secondary aggregation
M1 — weak / article / unattributed summary
M0 — unknown
```

The grade describes evidence strength for the **specific claim recorded**.

It is not a universal trust score for the seller, GPU, or price.

## Current Intelligence mapping

### SECONDARY_REPORTED

```text
→ M1
```

Reason:
- current article/report signal;
- no raw direct listing sample;
- no confirmed transaction record.

Current examples:
- China RTX 3090 7400 CNY watch signal;
- China Arc A770 1450 CNY watch signal.

### MEDIAN_ASK

```text
→ M2
```

For the current production rows this means:
- transparent secondary aggregation;
- current dated source;
- active sample size;
- middle-half asking range;
- source methodology/export time.

This is stronger than one article, but still:

```text
asking price != sale price
```

### SOLD_MARKED_LISTING_PRICE

```text
→ M3
```

because the current records preserve direct platform pages with:
- exact hardware identity;
- direct URL;
- page status = SOLD;
- displayed listing price;
- location/title;
- current capture.

But M3 is **claim-scoped**.

For these rows M3 proves:

```text
direct page marked SOLD
+ displayed listing price
```

It does not prove:

```text
displayed price = negotiated transaction amount
```

Every current row therefore still keeps:

```text
confirmed_transaction_price=false
```

## Experiment 38 bridge

Experiment 38 currently accepts:

```text
market evidence M2/M3
```

as one prerequisite for BUY-CANDIDATE.

I16 maps Intelligence observations into that field.

Semantics:

```text
M0/M1
→ NEEDS-STRONGER-MARKET-EVIDENCE

M2/M3
→ ELIGIBLE
```

ELIGIBLE means only:

> this observation may satisfy Experiment 38's market-evidence component.

It does not satisfy:
- FIT;
- SOFTWARE;
- PERFORMANCE;
- condition C3/C4;
- price ceiling;
- freshness.

## Machine-readable fields

Every production market row carries:

```json
{
  "market_evidence_grade": "M1|M2|M3",
  "market_evidence_scope": "what this grade actually supports"
}
```

Synthetic fixtures use M0.

## Validator

Current production states are constrained:

```text
SECONDARY_REPORTED          → M1
MEDIAN_ASK                  → M2
SOLD_MARKED_LISTING_PRICE   → M3
synthetic fixture           → M0
```

A mismatched grade or missing claim scope fails catalog validation.

## Query

```bash
python3 tools/intelligence/market_evidence_gate.py intelligence/catalog
```

Or inspect selected records:

```bash
python3 tools/intelligence/market_evidence_gate.py intelligence/catalog \
  --record-id market:...
```

## Guardrails

Do not infer:

```text
M3
→ confirmed sale amount
```

Do not infer:

```text
M2/M3
→ BUY
```

Market evidence remains only one input to the complete purchase decision.
