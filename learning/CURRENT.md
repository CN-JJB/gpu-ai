# Current State

## Source of truth

- Repo: CN-JJB/gpu-ai
- Branch: main
- Stable course and dynamic intelligence remain separate.

## Stable course

~~~text
Slices 01–49 implemented
Experiments 01–93 exist
Stable v1 mainline complete
~~~

## Active Phase 4 frontier

~~~text
I01 catalog + benchmark bridge
I02 compatibility preflight
I03 exact measured compatibility
I04 comparable benchmark view
I05 explicit price/performance
I06 evidence-linked TCO
I07 real benchmark intake
I08 four-ecosystem documented compatibility
I09 compatibility matrix
I10 freshness queue
I11 real MEDIAN_ASK cohort
I12 market evidence audit
I13 sold-marked listing cohort
I14 cross-market signal comparison
I15 China secondary watch
I16 stable M0–M3 market evidence selection gate
I17 freshness-aware watchlist gate
I18 append-only market refresh lineage
I19 reusable market refresh helper + CI self-test
I20 manifest ↔ raw llama-bench identity/config cross-check
I21 explicit-argv real benchmark capture/seal helper
I22 non-synthetic local model artifact SHA256/bytes admission gate
I23 exact benchmark argv ↔ verified model artifact binding
~~~

## Benchmark boundary

~~~text
real production benchmark rows = 0
~~~

Required admission:

~~~text
Experiment 61 manifest
+ raw result
+ PACKET.json
+ canonical IDs
→ I07 READY
→ ingest
→ validate
→ exact MEASURED_SUPPORTED
~~~

## Market evidence grades

~~~text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
~~~

Current production count after I18:

~~~text
M1=3
M2=3
M3=9
market observations=15
~~~

One M1 A770 record is historical/superseded.

## Current active market signals

### eBay active asks

~~~text
RTX 3090      1499 USD
RX 7900 XTX   1020 USD
Arc A770       330 USD
~~~

### OfferUp SOLD-marked displayed medians

~~~text
RTX 3090      950 USD
RX 7900 XTX   700 USD
Arc A770      200 USD
~~~

Every OfferUp row remains:

~~~text
confirmed_transaction_price=false
~~~

### China secondary watch

Current active records:

~~~text
RTX 3090 → 7400 CNY
Arc A770 → 1400 CNY
~~~

Historical A770 record:

~~~text
2026-08-21 → 1450 CNY
superseded_by
2026-08-25 → 1400 CNY
~~~

The current 1400 CNY observation is still M1 secondary evidence:
- direct_listing_capture=false;
- confirmed_sale=false;
- revalidate_after=2026-09-01.

## I17 freshness-aware purchase use

~~~text
CURRENT + M2/M3 → ELIGIBLE
CURRENT + M0/M1 → NEEDS-STRONGER-MARKET-EVIDENCE
DUE-TODAY → REVALIDATE-NOW
STALE → STALE-REVALIDATE
UNSCHEDULED / INVALID → REVALIDATION-SCHEDULE-REQUIRED
~~~

Experiment 38 blocks due-today/stale/unknown/invalid market evidence from BUY-CANDIDATE.

## I18 append-only refresh

Refresh does not overwrite old market evidence.

Lineage:

~~~text
old.superseded_by = new
new.supersedes = old
~~~

Default behavior:
- market_matrix hides superseded rows;
- freshness_report removes superseded rows from active revalidation queue;
- market_evidence_gate returns SUPERSEDED-USE-NEWER-OBSERVATION.

Audit history remains available with:

~~~text
--include-superseded
~~~

Validator checks:
- reference existence;
- reciprocal lineage;
- same hardware_id;
- newer timestamp;
- no self-reference;
- no cycle.

## Latest CI

GitHub Actions:

~~~text
workflow: Intelligence Self-Test
run #141
run id 33169970758
head 2070476cd272f904476dff4100779a12ec534f59
job id 98844439875
conclusion success
~~~

Result:

~~~text
SELFTEST: PASS
~~~

Log/steps explicitly confirm:
- every Intelligence Python tool compiles;
- the full Intelligence self-test passes;
- I21–I32 evidence capture/admission tests remain green;
- I33 independently verifies both quality bundles before any PPL arithmetic;
- tokenizer/corpus/fixture/evaluation argv/parser/metric/executable hash+bytes must match exactly;
- changed quality executable bytes or evaluation argv block A/B comparison;
- only exact-contract comparisons emit descriptive PPL delta/ratio/percent change;
- no significance, causality or recommendation is inferred;
- the main benchmark PACKET and quality PACKET remain separate integrity domains;
- the dedicated I19 market refresh self-test remains green.

Evidence:
- examples/evidence/intelligence-17-freshness-aware-watchlist.md
- examples/evidence/intelligence-18-append-only-market-refresh.md
- examples/evidence/intelligence-19-market-refresh-helper.md
- examples/evidence/intelligence-20-real-benchmark-raw-identity.md
- examples/evidence/intelligence-21-real-benchmark-capture-seal.md
- examples/evidence/intelligence-22-real-model-artifact-gate.md
- examples/evidence/intelligence-23-command-model-artifact-binding.md
- examples/evidence/intelligence-24-hardware-profile-artifact-gate.md
- examples/evidence/intelligence-25-prompt-evidence-manifest-gate.md
- examples/evidence/intelligence-26-quality-corpus-artifact-gate.md
- examples/evidence/intelligence-27-quality-identity-manifest-gate.md
- examples/evidence/intelligence-28-quality-execution-evidence.md
- examples/evidence/intelligence-29-quality-execution-intake-gate.md
- examples/evidence/intelligence-30-quality-evaluation-argv-binding.md
- examples/evidence/intelligence-31-quality-metric-extraction.md
- examples/evidence/intelligence-32-quality-metric-intake-gate.md
- examples/evidence/intelligence-33-quality-ab-comparability.md

## Next

1. Bind the quality A/B result to the paired performance A/B manifest/one-variable contract before any speed-vs-quality tradeoff decision (I34).
2. Acquire the first learner-owned real Experiment 61 packet through I21 + I07/I20/I22/I23/I24/I25/I26/I27/I29/I30/I32.
3. Use market_refresh.py for due/stale observations; refresh RTX 3090 China evidence only when stronger/newer provenance exists.
4. Add stronger direct/confirmed transaction evidence only when auditable.
5. Delay recommendation/ranking until real benchmark + quality/SLO + feasibility evidence exists.
