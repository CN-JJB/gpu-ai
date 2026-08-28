# Spec 0020 — Market Refresh Helper

Status: implemented and CI verified  
Date: 2026-08-28

## Problem

I18 defined append-only market lineage, but refreshes still required manual JSONL editing.

Manual editing is error-prone because a refresh must preserve history while enforcing:

- one active lineage tail;
- reciprocal `superseded_by` / `supersedes`;
- the same `hardware_id`;
- a strictly newer `observed_at`;
- a unique new `record_id`;
- complete new provenance and revalidation metadata.

## Decision

Add:

```text
tools/intelligence/market_refresh.py
```

The helper takes:

```text
catalog
+ old market record id
+ one complete candidate observation JSON object
→ append-only refreshed market.jsonl
```

It never invents a new price, evidence grade, source, or observation.

The candidate must already contain the new evidence claim.

## Safety rules

A refresh is rejected when:

1. the old record is already superseded;
2. the candidate record id already exists;
3. hardware identity changes;
4. the candidate date is not later;
5. the candidate already points to another lineage tail;
6. required refresh fields are missing.

The old record is retained and receives:

```text
old.superseded_by = new.record_id
```

The new record receives:

```text
new.supersedes = old.record_id
```

## Write behavior

`--check-only` validates the proposed lineage without writing.

`--out` is required.

It may point to the existing `market.jsonl`; replacement is performed through a temporary file plus atomic `os.replace`.

Reviewing the candidate provenance before write remains the operator's responsibility.

## Validation boundary

The helper only owns refresh-lineage mechanics.

The resulting catalog must still pass:

```bash
python tools/intelligence/validate_catalog.py intelligence/catalog
```

Evidence-grade semantics remain owned by the catalog validator and market evidence gate.

## Self-test

```text
tools/intelligence/market_refresh_selftest.py
```

The self-test proves:

- old observation remains present;
- reciprocal lineage is created;
- the generated catalog passes the production validator;
- already-superseded history cannot fork;
- cross-hardware lineage is rejected;
- equal/older timestamps are rejected.

## RTX 3090 current boundary

As of 2026-08-28, the current public China-side RTX 3090 signal remains the 2026-08-22 secondary report around 7400 CNY.

No stronger auditable direct-listing or confirmed-transaction source was found in this pass.

Therefore this implementation does not fabricate an RTX 3090 refresh and does not promote M1 to M2/M3.

## CI

GitHub Actions:

```text
run #67
run id 33154549739
head 8ab1d5435e867570c2a5c2a48cc94d45c533179f
job id 98794100639
conclusion success
```

The job compiled every Intelligence Python tool, ran the existing full self-test, then ran `market_refresh_selftest.py`.

Both passed.
