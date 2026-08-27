# Evidence — Intelligence I12: Market Evidence Audit

Date: 2026-08-28  
Status: implemented; exact-blob contract verified

## Claim

A market price should expose its sample/method boundary rather than appearing as an unexplained scalar.

## Production sample metadata

```text
RTX 3090
active=47
range=1400–1520
→ BROAD-SAMPLE

RX 7900 XTX
active=23
range=997–1080
→ LIMITED-SAMPLE

Arc A770 16GB
active=8
range=325–347
→ SMALL-SAMPLE
```

All are:

```text
ASK-ONLY
NOT-CONFIRMED-SALE
```

## Validator gate

Production MEDIAN_ASK now requires:
- sample object;
- active_listings > 0;
- range_kind;
- range_low/range_high;
- methodology;
- confirmed_sale=false;
- source.data_exported_at;
- median price inside the recorded range.

A MEDIAN_ASK row without sample metadata must fail catalog validation.

## Exact-blob verification

Latest main blobs:

```text
market.jsonl
8c7bc0e007c881829d9dbb1128398ba0ee194c3e

validate_catalog.py
80d39e27a5bd2c3449323122c6425ee99712d8d2

market_evidence_audit.py
756408820746a249156730cf7a74a555414c9b9f

selftest.py
c9ccf703c52cd29c623c9539aa2c7548c5edec14
```

Contract verification confirmed:
- 3 cohort rows;
- 1 BROAD / 1 LIMITED / 1 SMALL sample;
- every median lies inside its recorded range;
- every row has confirmed_sale=false;
- validator gate is present;
- malformed sample-removal rejection assertion is present in self-test.

## Non-claim

The sample bands are operational heuristics.

They are not statistical confidence scores.

A sample of 47 asks is not automatically a representative sale-price distribution.