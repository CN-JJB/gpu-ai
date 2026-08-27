# Handoff — GPU × Local LLM Course / Intelligence Stations

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Stable course state

~~~text
Slices 01–49 implemented
Experiments 01–93 exist
Stable v1 mainline complete
~~~

The stable mainline ends with:
- Experiment 91 whole-machine dossier;
- Slice 49 Graduation Machine Design Capstone;
- Experiment 92 synthetic final-review validator;
- Experiment 93 real graduation report workflow.

Stable machine-decision semantics remain:

~~~text
known required FAIL → REVISE
critical UNKNOWN / missing required evidence → BLOCKED
all required gates PASS → ACCEPT
~~~

No weighted score may average away a hard gate.

## Active Phase 4 frontier

Verified:

~~~text
I01 catalog / benchmark bridge
I02 compatibility preflight
I03 exact measured compatibility ingestion
I04 comparable benchmark view
I05 explicit price/performance
I06 evidence-linked TCO worksheet
~~~

These are Intelligence Stations, not Slice 50–55.

## I01 data contract

Production catalog:

~~~text
intelligence/catalog/hardware.jsonl
intelligence/catalog/models.jsonl
intelligence/catalog/runtimes.jsonl
intelligence/catalog/market.jsonl
intelligence/catalog/compatibility.jsonl
intelligence/catalog/benchmarks.jsonl
~~~

Use canonical entities plus dated observations.

## I02 compatibility semantics

~~~text
DOCUMENTED_SUPPORTED → NEEDS-TEST
MEASURED_SUPPORTED → PASS-MEASURED
PARTIAL / EXPERIMENTAL → REVIEW
DOCUMENTED_UNSUPPORTED → FAIL
UNKNOWN → BLOCKED
stale → STALE-REVALIDATE
~~~

Do not promote documentation to measured PASS.

## I03 measured ingestion

Preferred path:

~~~text
Experiment 61 manifest
+ raw llama-bench
+ Evidence Packet
→ ingest_llama_bench.py
→ benchmark observation
→ ingest_measured_compatibility.py
→ exact MEASURED_SUPPORTED
~~~

Measured support remains exact-path scoped.

## I04 comparable benchmark rule

~~~text
same model
+ same artifact SHA
+ same quant
+ same workload
→ comparable descriptive group
~~~

Do not rank across groups.

## I05 price/performance rule

Explicit market records only.

Selected market observations must share:
- geography;
- channel;
- cohort;
- condition;
- price state;
- currency.

No automatic latest-price denominator.

## I06 TCO rule

~~~text
purchase
+ platform delta
+ electricity
+ risk reserve
- resale
→ scenario TCO
~~~

TCO does not rescue an infeasible/unsupported/unsafe design.

## Verification

Exact-content local verification was completed on 2026-08-27.

The checked local files matched main-branch Git blob SHAs for the intelligence scripts/catalog/fixtures used in the run.

Executed:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

Result:

~~~text
SELFTEST: PASS
~~~

Evidence:
- examples/evidence/intelligence-i01-i06-selftest-verification.md
- learning/records/2026-08-27-intelligence-i01-i06-verification.md

Defects caught/fixed:
- literal backslash-n source corruption;
- missing runtime dictionary initialization;
- UNKNOWN incorrectly rejected as placeholder.

GitHub Actions workflow:
- .github/workflows/intelligence-selftest.yml

The connector did not surface a workflow run for the checkpoint, so do not claim CI success.

## Current production-data boundary

Production benchmark catalog remains empty by design.

No real benchmark Evidence has yet been admitted through I01–I03.

## Next work

1. Search existing repository Evidence for a real Experiment 61-compatible packet/result.
2. Ingest it only if hardware/model/runtime/artifact/workload identity is complete and auditable.
3. Otherwise leave production benchmark data empty and prepare a real-run intake checklist.
4. Expand dated compatibility observations across NVIDIA / AMD / Apple / Intel.
5. Delay recommendation/ranking until real comparable Evidence exists.

No auto-purchase or unsafe hardware modification is part of this workflow.
