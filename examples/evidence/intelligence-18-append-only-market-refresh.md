# Evidence — Intelligence I18: Append-Only Market Refresh Lineage

Date: 2026-08-28  
Status: CI verified

## Claim

A newer market observation can replace an older observation for current decision use without deleting historical evidence.

## Production refresh

Old:

```text
market:cn:a770-16g:secondary:2026-08-21
1450 CNY
M1
```

New:

```text
market:cn:a770-16g:secondary:2026-08-25
1400 CNY
M1
```

Lineage:

```text
old.superseded_by = new
new.supersedes = old
```

## Active behavior

Current CN market query:

```text
RTX 3090 → 7400 CNY
Arc A770 → 1400 CNY
```

The old 1450 row is hidden by default.

Audit query with:

```text
--include-superseded
```

shows all three CN rows including the old A770 observation.

## Freshness behavior

The old A770 row is:

```text
SUPERSEDED
```

not:

```text
DUE-TODAY
STALE
```

for active refresh purposes.

It remains visible in the dedicated superseded section.

## Watchlist behavior

Old record:

```text
SUPERSEDED-USE-NEWER-OBSERVATION
```

New record remains M1 and therefore:

```text
NEEDS-STRONGER-MARKET-EVIDENCE
```

for Experiment 38.

## Validator behavior

Broken lineage is rejected.

Test mutation:

```text
new.supersedes = market:missing
```

Expected:

```text
VALIDATION: FAIL
```

## CI

GitHub Actions:

```text
run #62
run id 33137884125
head 373b2ff6dd78f7018fd026e76b9714519204fbbe
job id 98741901113
conclusion success
```

Log:

```text
SELFTEST: PASS
- append-only A770 refresh supersedes the old observation without deleting audit history
- superseded observations leave active market/freshness/watchlist views by default
- broken market refresh lineage is rejected
```

## Migration note

Runs #57–61 failed during the staged migration because data/tool behavior changed before the final self-test expectations were updated.

Run #62 is the completion checkpoint.

Those intermediate failures are not hidden; they are part of the migration history.
