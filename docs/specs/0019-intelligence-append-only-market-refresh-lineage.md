# Spec 0019 — Append-Only Market Refresh Lineage

Status: implemented and CI verified  
Date: 2026-08-28

## Problem

Dynamic market intelligence must be refreshed without deleting history.

Before I18, an expired observation had only two bad choices:
- overwrite the old record and lose audit history;
- keep both records active and let the stale one remain forever in refresh/watchlist views.

## Correct model

Use append-only observation lineage:

```text
older observation
  superseded_by
        ↓
newer observation
  supersedes
```

The old record remains in the catalog.

It is not treated as current purchase evidence.

## A770 refresh

Older observation:

```text
record: market:cn:a770-16g:secondary:2026-08-21
value: 1450 CNY
evidence: M1 secondary
revalidate_after: 2026-08-28
```

Newer observation:

```text
record: market:cn:a770-16g:secondary:2026-08-25
value: 1400 CNY
evidence: M1 secondary
revalidate_after: 2026-09-01
```

The newer source describes a current Xianyu A770 16GB asking/listing signal around 1400 CNY after being around 1200 CNY.

This remains secondary evidence.

It is not:
- a direct listing sample;
- a confirmed sale;
- a normalized sold-price median.

## Why no range schema was added

An earlier internal snapshot described the newer A770 source as a 1200–1600 CNY range.

Re-checking the current source page showed that the supported current claim is closer to:

```text
roughly 1200 → roughly 1400 asking/listing signal
```

Therefore I18 does not invent a range-valued record merely to preserve an earlier summary.

Evidence source:
- https://post.smzdm.com/p/agg4xrq3/

## Active-view semantics

### market_matrix.py

Default:

```text
superseded observations hidden
```

Audit mode:

```bash
--include-superseded
```

### freshness_report.py

Superseded records enter:

```text
SUPERSEDED
```

They do not remain in the active revalidation queue.

### market_evidence_gate.py

Superseded records return:

```text
SUPERSEDED-USE-NEWER-OBSERVATION
```

They cannot satisfy active watchlist market evidence.

## Validator

Lineage must satisfy:
- referenced record exists;
- forward/back references agree;
- hardware_id stays the same;
- newer observed_at is later;
- no self-reference;
- no supersession cycle.

## Stable semantics

```text
SUPERSEDED
!=
FALSE
```

It means a newer observation should be used for current decisions.

The old record remains useful for:
- history;
- market movement;
- audit;
- provenance review.

## CI

GitHub Actions run #62 verifies:
- current CN matrix shows 7400 / 1400, not old 1450;
- --include-superseded restores old 1450 for audit;
- freshness reports SUPERSEDED;
- watchlist gate blocks superseded evidence;
- broken lineage is rejected.
