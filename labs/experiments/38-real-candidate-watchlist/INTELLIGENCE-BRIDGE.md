# Experiment 38 — Intelligence Market Evidence Bridge

Use this bridge when a real watchlist candidate references a record from:

```text
intelligence/catalog/market.jsonl
```

## Copy the grade, not your impression

Run:

```bash
python3 tools/intelligence/market_evidence_gate.py intelligence/catalog \
  --record-id market:...
```

Then copy:

```text
market_evidence_grade
```

into Experiment 38's:

```text
market_evidence
```

field.

## Current mapping

```text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
```

The grade is claim-scoped.

### M1

Current article/report signal.

Useful for:
- watch direction;
- rough anchor;
- deciding what to sample next.

It does not satisfy Experiment 38's current M2/M3 market-evidence threshold.

### M2

Current transparent secondary aggregation with methodology/sample evidence.

It may satisfy the market-evidence component.

It still does not prove:
- confirmed transaction price;
- condition;
- fit;
- software support;
- performance.

### M3

Direct normalized platform evidence for the exact claim captured.

For current OfferUp rows, M3 means:

```text
direct page
+ SOLD status
+ displayed listing price
```

It does **not** mean:

```text
displayed price = negotiated transaction amount
```

## Experiment 38 decision remains unchanged

A candidate can only become BUY-CANDIDATE when:

```text
FIT PASS
+ SOFTWARE PASS
+ PERFORMANCE PASS
+ market evidence M2/M3
+ condition evidence C3/C4
+ ask <= personal max sticker
```

Therefore:

```text
M2/M3
!=
BUY-CANDIDATE
```

## Keep source identity

In the watchlist row also preserve:
- exact market record ID;
- price state;
- observed_at;
- source URL;
- notes about claim scope;
- freshness.

Do not translate one Intelligence observation into a timeless "fair price".


## Freshness is a second gate

A copied M2/M3 grade is not enough.

Run the Intelligence gate with the decision date:

```bash
python3 tools/intelligence/market_evidence_gate.py intelligence/catalog \
  --record-id market:... \
  --as-of YYYY-MM-DD
```

For purchase use:

```text
M2/M3 + CURRENT
→ market-evidence component ELIGIBLE

DUE-TODAY
→ REVALIDATE-NOW

STALE
→ STALE-REVALIDATE
```

The watchlist CSV now includes:

```text
revalidate_after
```

When present, Experiment 38 treats it as authoritative.

A stale or due-today market record must not produce BUY-CANDIDATE.


## Condition / performance / price companions

The market bridge is only one component.

For the remaining Phase 4 evidence:

~~~text
condition provenance:
reference/hardware/condition-evidence-grades.md
I44 → I50 → I51

performance target:
I46 → I47

personal price ceiling:
I48 → I49
~~~

I49 requires the exact same market record used by the market-evidence component.

Do not use one market record for M2/M3 eligibility and another cheaper record for the price ceiling.

I43 combines these domains and still emits only BLOCKED or READY-FOR-HUMAN-REVIEW.
