# Spec 0008 — Real Benchmark Intake Gate

Status: implemented foundation  
Date: 2026-08-27

## Problem

The production intelligence benchmark catalog must not accept a benchmark merely because a JSON file contains a tok/s number.

Before ingestion, the repository needs a preflight that proves the submitted Evidence chain is internally complete enough to enter the I01–I03 pipeline.

## Required inputs

The intake gate receives:

~~~text
production catalog
+ Experiment 61 manifest
+ raw benchmark result
+ PACKET.json
+ hardware_id
+ model_id
+ runtime_id
+ observed_at
~~~

It does not modify the production catalog.

## Canonical identity gate

The supplied:
- hardware_id;
- model_id;
- runtime_id

must already exist in the selected catalog.

Unknown canonical IDs block intake.

## Manifest gate

Required Experiment 61 identity includes:
- hardware device identity;
- hardware profile SHA;
- runtime identity;
- backend;
- build identity;
- model artifact SHA;
- artifact bytes;
- quant;
- source revision;
- context;
- sequences;
- PP tokens;
- TG tokens;
- repetitions;
- prompt token-ID SHA;
- tokenizer identity;
- quality corpus SHA;
- fixture revision.

Placeholder values block intake.

## Raw result gate

The raw benchmark result must contain at least one positive:
- PP avg_ts;
- TG avg_ts.

The intake gate does not fabricate missing metrics.

## Packet integrity gate

PACKET.json must index the exact supplied:
- manifest file;
- raw result file.

For each, the packet entry must match:
- SHA256;
- byte count.

A matching filename with a wrong hash is blocked.

A matching hash with a different byte count is blocked.

## Synthetic boundary

Synthetic fixtures are rejected by default.

The test suite may use:

~~~text
--allow-synthetic
~~~

Production intake must omit that flag.

## READY semantics

~~~text
INTAKE: READY
~~~

means only:

> the submitted evidence bundle is internally complete enough to pass to the benchmark ingester.

It does not prove:
- the benchmark was honestly executed;
- the hardware is healthy;
- the result is statistically representative;
- model quality passes;
- the system meets serving SLO;
- the candidate should be purchased.

## Next step

After READY:

~~~text
ingest_llama_bench.py
→ validate_catalog.py
→ ingest_measured_compatibility.py
→ validate_catalog.py
~~~

All resulting production changes should remain reviewable diffs.