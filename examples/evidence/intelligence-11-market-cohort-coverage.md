# Evidence — Intelligence I11: Explicit Real Market Cohort

Date: 2026-08-28  
Status: implemented; exact-blob contract verified

## Claim

Real dynamic market observations can be added without mixing incompatible price semantics.

## Production cohort

```text
GLOBAL-EBAY
secondary-aggregated-ebay-active
used-consumer
used
MEDIAN_ASK
USD
```

Rows:

```text
RTX 3090      1499 USD
RX 7900 XTX   1020 USD
Arc A770 16G   330 USD
```

## Exact-blob verification

Verified against latest main blobs:

```text
hardware.jsonl
6be5c312e68023fc2f952c324f5e3af27d7c29e0

market.jsonl
00e492a9026f11ad97070c272606de6a668c5201

selftest.py
e2f168dbaccd1af23978e02b70d50245a9499f00
```

Contract-equivalent execution confirmed:
- market rows = 3;
- unique market contracts = 1;
- all hardware IDs resolve;
- values = 330 / 1020 / 1499 USD;
- all three were current as of 2026-08-28;
- I11 self-test assertions were present.

## Important semantics

```text
MEDIAN_ASK
!=
SOLD-CONFIRMED
```

The source itself states that these are asking prices, not sale prices.

## Full Python test boundary

The full I01–I10 Python self-test had already passed before I11.

During the I11 checkpoint, the local execution environment timed out/rate-limited before a fresh complete repository run could be repeated.

Therefore this record claims exact-main contract verification for I11, not a new full-Python PASS.

## Source snapshot

See:
- intelligence/market/ebay-used-gpu-asking-cohort-2026-08-28.md