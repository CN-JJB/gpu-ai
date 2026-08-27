# Evidence — Intelligence I01–I06 Execution Verification

Date: 2026-08-27  
Status: PASS

## Purpose

Verify that the Phase 4 Intelligence foundation actually executes after the I01–I06 contract changes.

This checkpoint covers:
- catalog validation;
- benchmark ingestion;
- compatibility preflight;
- exact measured compatibility upgrade;
- comparable benchmark grouping;
- explicit price/performance;
- TCO scenario arithmetic;
- broken-reference rejection.

## Exact-content verification

A local verification tree was reconstructed from the latest files on:

~~~text
CN-JJB/gpu-ai
branch: main
~~~

Before execution, Git blob SHA-1 values were compared between the local verification tree and GitHub for:
- 9 Python intelligence tools;
- 6 production catalog files;
- 6 synthetic catalog fixture files;
- Experiment 61 manifest/result fixtures;
- TCO fixture.

The checked content matched the corresponding GitHub blobs before the final run.

Key script blob examples:

~~~text
validate_catalog.py              d89ee0135a09a4a94faa79adb4ed47579000b011
selftest.py                      9aeaf0778df78937b6fa196d48cb9619843ac82b
compatibility_preflight.py       fa84e0551d0882af21eb966f248e1143b7acec41
ingest_llama_bench.py            c07af2506d0408dbd46b03550eac32f9a2212302
ingest_measured_compatibility.py 535ade6f732d304dc836b1b9f617e7e64eecb54b
comparable_benchmarks.py         62d994a1facf9247d273093762eb49aa3a40c872
price_performance.py             7c7f56325a643dfe465e3e9496d55924626dbf93
tco_worksheet.py                 c481012ff4cc1929e7d8f6161cf53dcfa13b854b
query_bridge.py                  14886616b3977b33b51237b778362338dc7d8362
~~~

## Commands executed

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

## Result

~~~text
SELFTEST: PASS
- production catalog validates
- synthetic catalog validates only with explicit allowance
- Hardware ↔ Model ↔ Benchmark bridge returns the fixture observation
- same artifact/workload observations form one descriptive comparison group
- explicit same-cohort market rows enable descriptive price/performance
- evidence-linked TCO fixture reproduces the expected scenario arithmetic
- documented compatibility returns NEEDS-TEST, not measured PASS
- explicit UNKNOWN remains valid and returns BLOCKED
- Experiment 61 importer reproduces PP/TG
- exact benchmark Evidence upgrades only the matching path to PASS-MEASURED
- a different artifact falls back to NEEDS-TEST
- broken canonical hardware reference is rejected
~~~

## Bugs found during verification

Verification caught and fixed:
1. a literal \`\\n\` accidentally written into Python source;
2. missing \`runtimes = {}\` initialization in the catalog validator;
3. compatibility \`UNKNOWN\` being incorrectly rejected by the generic placeholder rule.

The final PASS occurred after these fixes.

## Important boundaries

The self-test proves tool behavior and internal data-contract consistency.

It does not prove:
- synthetic PP/TG values are real performance;
- the production RTX 3090 path has been measured;
- current market observations are fresh forever;
- documented support equals deployment success;
- lower price/performance or TCO means a hardware candidate is feasible.

The production benchmark catalog remains intentionally empty until real Evidence is ingested.

## CI note

A GitHub Actions workflow exists at:

~~~text
.github/workflows/intelligence-selftest.yml
~~~

The available GitHub connector did not surface a workflow run for this checkpoint, so this evidence records the exact-content local execution rather than claiming CI success.