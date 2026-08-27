# Evidence — Intelligence I03: Exact Measured Compatibility

Status: exact-path measured compatibility ingestion implemented.

## Claim

A successful benchmark Evidence record may upgrade only the exact recorded path from documented support to measured support.

## Input chain

~~~text
Experiment 61
→ benchmark observation
→ ingest_measured_compatibility.py
→ MEASURED_SUPPORTED observation
~~~

## Exact scope preserved

The measured compatibility record keeps:
- hardware_id;
- model_id;
- runtime_id;
- backend;
- artifact SHA;
- quant;
- runtime identity/build;
- device/profile identity;
- workload;
- raw run source;
- manifest source;
- packet source.

## Decision behavior

For the exact artifact/build:

~~~text
DOCUMENTED_SUPPORTED
+
MEASURED_SUPPORTED
→ PASS-MEASURED
~~~

For another artifact/build without exact measured Evidence:

~~~text
generic DOCUMENTED_SUPPORTED
→ NEEDS-TEST
~~~

## Important non-claim

One positive benchmark does not prove:
- all quantizations;
- all contexts;
- all runtime versions;
- serving SLO;
- model quality;
- long-term stability;
- family-wide compatibility.

## Canonical runtime join

Benchmark observations now require runtime_id in addition to hardware_id and model_id.

This closes the join:

~~~text
hardware
↔ model
↔ runtime
↔ benchmark
↔ compatibility
~~~

## Synthetic proof

The self-test generates a synthetic benchmark record, derives an exact MEASURED_SUPPORTED observation, and checks:
- exact artifact/build → PASS-MEASURED;
- different artifact → NEEDS-TEST.

Synthetic values remain non-performance claims.