# Handoff — GPU × Local LLM Course / Intelligence Stations

## Repo

- CN-JJB/gpu-ai
- main

## Stable course

~~~text
Slices 01–49
Experiments 01–93
v1 stable mainline complete
~~~

## Phase 4 frontier

~~~text
I01–I22 implemented and CI verified
~~~

## Latest CI

~~~text
run #86
run id 33155742355
head 99dc1d9326e2daca9095a249cf5fe06c4e25c542
job id 98797950974
full SELFTEST: PASS
market refresh SELFTEST: PASS
~~~

## Benchmark boundary

Production benchmark catalog remains empty.

Required:

~~~text
manifest + raw result + PACKET + canonical IDs
→ I07 READY
→ ingest
→ validate
→ exact MEASURED_SUPPORTED
~~~

## Market evidence

~~~text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
~~~

Current active signals:

~~~text
eBay asks:
3090 1499
7900 XTX 1020
A770 330 USD

OfferUp SOLD-marked displayed medians:
3090 950
7900 XTX 700
A770 200 USD

China secondary:
3090 7400
A770 1400 CNY
~~~

## A770 append-only refresh

Historical:

~~~text
2026-08-21
1450 CNY
~~~

Current:

~~~text
2026-08-25
1400 CNY
revalidate_after=2026-09-01
~~~

Lineage:

~~~text
old.superseded_by = new
new.supersedes = old
~~~

The old row remains audit history but is not current purchase evidence.

## Active-view semantics

~~~text
market_matrix
→ hides superseded by default

freshness_report
→ SUPERSEDED, not active stale queue

market_evidence_gate
→ SUPERSEDED-USE-NEWER-OBSERVATION
~~~

Use --include-superseded for audit history.

## Watchlist freshness

~~~text
CURRENT + M2/M3 → ELIGIBLE
DUE/STALE/INVALID → not purchase-eligible
~~~

Experiment 38 cannot emit BUY-CANDIDATE from stale/due/invalid market evidence.

## I19 reusable refresh helper

```text
tools/intelligence/market_refresh.py
```

Use a complete new observation candidate plus the active old record.

The helper creates reciprocal append-only lineage and rejects:
- already-superseded forks;
- cross-hardware links;
- non-newer observations.

CI run #67 verifies the helper and keeps the original full self-test green.

## I20 raw benchmark identity gate

```text
verify_real_intake.py
→ PACKET hash/bytes
+ exact PP/TG protocol rows
+ manifest ↔ raw llama-bench identity/config agreement
→ RAW IDENTITY: PASS
→ INTAKE: READY
```

The verifier now blocks a recomputed, hash-consistent packet when the manifest claims a different GPU/backend/build/model/config than the raw benchmark evidence.

Implementation checkpoint: run #74.  
Final documented head: run #76, success.

## I21 capture/seal helper

```text
capture_real_benchmark.py
→ explicit argv, shell=False
→ stdout + stderr + command identity + exit code
→ optional evidence copies
→ PACKET.json
→ CAPTURE: SEALED
```

`SEALED` is not admission.

The sealed bundle must still pass I07/I20.

CI run #81 keeps the full suite, I21 capture self-test and I19 refresh self-test green.

## I22 local model artifact gate

For non-synthetic intake:

```text
--model-artifact MODEL.gguf
→ local bytes + SHA256
↔ manifest artifact_bytes + artifact_sha256
↔ I20 raw llama-bench model_size
→ MODEL ARTIFACT status=PASS
```

CI run #86 keeps full, capture, artifact and refresh tests green.

## Next work

1. Bind I21 command argv to the I22-verified artifact.
2. Acquire the first learner-owned real Experiment 61 packet through I21 → I07/I20/I22.
3. Use the market refresh helper for due/stale evidence and stronger RTX 3090 China evidence when auditable.
4. No recommendation leaderboard yet.

No auto-purchase or unsafe hardware modification.
