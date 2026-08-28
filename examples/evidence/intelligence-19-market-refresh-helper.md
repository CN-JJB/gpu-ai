# Evidence — Intelligence I19: Reusable Market Refresh Helper

Date: 2026-08-28  
Status: CI verified

## Claim

Append-only market refresh lineage can now be produced through a reusable helper instead of hand-editing both ends of the lineage.

## Implementation

```text
tools/intelligence/market_refresh.py
tools/intelligence/market_refresh_selftest.py
docs/specs/0020-intelligence-market-refresh-helper.md
```

Input contract:

```text
catalog
+ active old market record id
+ complete new observation candidate
→ refreshed market.jsonl
```

The helper does not invent:
- price;
- evidence grade;
- source;
- provenance;
- revalidation date.

Those must already exist in the candidate observation.

## Positive behavior

For a valid refresh:

```text
old.superseded_by = new.record_id
new.supersedes = old.record_id
```

The old record stays in the catalog.

The new record becomes the active tail.

The self-test also runs the generated catalog through:

```text
validate_catalog.py
```

and requires:

```text
VALIDATION: PASS
```

## Negative behavior

The dedicated self-test proves rejection of:

```text
already-superseded old tail
cross-hardware lineage
equal/older observed_at
```

These fail before a refresh output is accepted.

## Local preflight performed before push

The helper and dedicated self-test were compiled and executed locally in an isolated fixture:

```text
MARKET REFRESH SELFTEST: PASS
```

## GitHub Actions

```text
workflow: Intelligence Self-Test
run #67
run id 33154549739
head 8ab1d5435e867570c2a5c2a48cc94d45c533179f
job id 98794100639
conclusion success
```

Successful steps include:

```text
Compile intelligence tools
Run intelligence self-test
Run market refresh self-test
```

All three completed successfully.

## RTX 3090 boundary in this pass

The current China-side RTX 3090 observation remains:

```text
market:cn:rtx3090:secondary:2026-08-22
7400 CNY
M1 SECONDARY_REPORTED
```

A newer/stronger auditable direct listing or confirmed transaction source was not found in this pass.

Therefore no fake refresh was appended and the claim was not promoted to M2/M3.

## Result

I19 changes the operational workflow from:

```text
find newer evidence
→ manually edit old JSON
→ manually add new JSON
→ hope reciprocal lineage is correct
```

to:

```text
find newer evidence
→ author one complete candidate
→ market_refresh.py preflight/write
→ validate_catalog.py
→ active-view/freshness/watchlist checks
```

The append-only evidence model remains unchanged; only the refresh operation is now repeatable and testable.
