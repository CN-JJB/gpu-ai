# Current State

## Source of truth

- Repo: CN-JJB/gpu-ai
- Branch: main
- Stable course and dynamic intelligence are separate layers.

## Historical archive

Stable-course history through Slice 45 is preserved at:

~~~text
learning/archive/CURRENT-through-slice45-2026-08-27.md
~~~

Detailed records:
- learning/records/
- examples/evidence/

## Stable course frontier

~~~text
Slices 01–49 implemented
Experiments 01–93 exist
Stable v1 mainline complete
~~~

The stable course ends in:
- whole-machine feasibility;
- Graduation Machine Design Capstone;
- ACCEPT / REVISE / BLOCKED evidence semantics;
- packet completeness independent from machine feasibility.

Do not extend the stable mainline just to add volatile current data.

## Active frontier — Phase 4 Intelligence Stations

Verified implementation:

~~~text
I01 catalog + benchmark bridge
I02 compatibility preflight
I03 exact measured compatibility ingestion
I04 comparable benchmark view
I05 explicit price/performance
I06 evidence-linked TCO worksheet
I07 real benchmark intake gate
~~~

### I01 — Catalog foundation

Machine-readable entities/observations:

~~~text
hardware
model
runtime
market
compatibility
benchmark
~~~

Production files live under:

~~~text
intelligence/catalog/
~~~

Core rule:

~~~text
ENTITY
+
dated/source-bound OBSERVATION
~~~

Do not put volatile price/support/performance into stable hardware identity.

### I02 — Compatibility preflight

Statuses:

~~~text
MEASURED_SUPPORTED
DOCUMENTED_SUPPORTED
PARTIAL
EXPERIMENTAL
DOCUMENTED_UNSUPPORTED
UNKNOWN
~~~

Decision semantics:

~~~text
MEASURED_SUPPORTED → PASS-MEASURED
DOCUMENTED_SUPPORTED → NEEDS-TEST
PARTIAL / EXPERIMENTAL → REVIEW
DOCUMENTED_UNSUPPORTED → FAIL
UNKNOWN / no match → BLOCKED
stale → STALE-REVALIDATE
~~~

Explicit UNKNOWN is a valid state.

### I03 — Exact measured compatibility

Preferred chain:

~~~text
Experiment 61
→ benchmark observation
→ measured compatibility observation
~~~

One successful exact path does not prove family-wide compatibility.

Exact artifact/build/device scope remains attached to the observation.

### I04 — Comparable benchmarks

Comparison requires:

~~~text
same model_id
+ same artifact SHA
+ same quant
+ same workload
~~~

Rows inside one group are descriptive system comparisons.

No cross-workload leaderboard.

### I05 — Price/performance

Requires:
- one comparable benchmark group;
- explicitly selected market records;
- same geography/channel/cohort/condition/price-state/currency.

No automatic latest-price join.

### I06 — TCO

Scenario:

~~~text
purchase
+ platform delta
+ electricity
+ risk reserve
- resale estimate
→ TCO
~~~

Every material assumption requires an evidence/source note.

TCO is not a feasibility gate and cannot override a hard failure.

### I07 — Real benchmark intake gate

Before production ingestion:

~~~text
manifest
+ raw result
+ PACKET.json
+ canonical hardware/model/runtime IDs
→ intake verification
~~~

The gate checks:
- required manifest identity;
- positive PP/TG raw metrics;
- packet SHA256 and byte counts;
- canonical IDs.

~~~text
INTAKE: READY
~~~

means the bundle is internally complete enough to ingest.

It does not prove benchmark truth or purchase suitability.

Repository search found no existing real Experiment 61-compatible packet/result bundle, so production benchmark data remains empty.

## Verification status

On 2026-08-27 the latest I01–I07 scripts and catalog/fixture files were reconstructed into a local test tree and checked against main by Git blob SHA.

Executed:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

Result:

~~~text
SELFTEST: PASS
~~~

Verification caught and fixed:
- literal \n written into Python source;
- missing runtime-index initialization;
- legal UNKNOWN status incorrectly treated as a placeholder.

Evidence:

~~~text
examples/evidence/intelligence-i01-i06-selftest-verification.md
~~~

A GitHub Actions self-test workflow exists, but the available connector did not surface a workflow run for this checkpoint. Do not claim CI success merely because the workflow file exists.

## Production-data status

Current production catalog contains:
- one hardware seed;
- one model seed;
- one runtime seed;
- one dated secondary market observation;
- one documented compatibility observation;
- zero real benchmark observations.

The empty production benchmark file is intentional.

~~~text
no real Experiment 61 Evidence
→ no production benchmark row
~~~

## Next actions

1. Acquire or receive a real Experiment 61 benchmark Evidence Packet.
2. Require I07 INTAKE: READY before production ingestion.
3. When real benchmark Evidence exists:
   - ingest benchmark;
   - validate;
   - derive exact MEASURED_SUPPORTED;
   - re-run self-test/production validation.
4. Expand current vendor/backend observations only from dated auditable sources.
5. Build recommendation views only after feasibility, support and quality/SLO gates.
