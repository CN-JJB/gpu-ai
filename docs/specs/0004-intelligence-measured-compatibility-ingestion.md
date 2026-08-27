# Spec 0004 — Measured Compatibility Ingestion

Status: implemented foundation  
Date: 2026-08-27

## Problem

I02 can say:

~~~text
DOCUMENTED_SUPPORTED
→ NEEDS-TEST
~~~

The next step is to upgrade an exact path to:

~~~text
MEASURED_SUPPORTED
→ PASS-MEASURED
~~~

only after real Evidence exists.

## Evidence input

Preferred input is an already-ingested benchmark observation produced from:

~~~text
Experiment 61 manifest
+ raw llama-bench result
+ Evidence Packet
→ benchmark record
~~~

Measured compatibility is derived from that benchmark record.

## Exact scope

A MEASURED_SUPPORTED observation must preserve:
- hardware_id;
- model_id;
- runtime_id;
- backend;
- exact artifact SHA;
- exact quant;
- exact runtime identity;
- exact build identity;
- exact device/profile identity where available;
- benchmark record ID;
- raw run source;
- packet source.

## Meaning

MEASURED_SUPPORTED means:

~~~text
this recorded path executed successfully enough
to produce a positive benchmark observation
under these recorded conditions
~~~

It does not mean:
- every quant works;
- every context works;
- every driver/runtime version works;
- every GPU of the same family works;
- serving SLO passes;
- quality is acceptable;
- long-term stability is proven.

## Ingestion gate

Production measured compatibility may only be generated from a benchmark observation whose source evidence class is MEASURED.

Synthetic benchmark fixtures require an explicit synthetic mode and remain outside production.

## Preflight preference

When an exact artifact/build is supplied, compatibility preflight should prefer the most specific matching observation.

Example:

~~~text
generic DOCUMENTED_SUPPORTED
+
exact MEASURED_SUPPORTED for artifact A / build B
→ PASS-MEASURED for A/B
~~~

A different artifact/build remains:

~~~text
NEEDS-TEST
~~~

unless its own measured observation exists.

## Freshness

Measured compatibility can also become stale.

A stale exact run becomes:

~~~text
STALE-REVALIDATE
~~~

for current deployment/purchase decisions.

## Non-goals

This ingestion does not:
- rerun the benchmark;
- certify model quality;
- certify all workloads;
- infer compatibility from a positive number copied from prose;
- promote family-wide support.

## Next

After exact measured ingestion:
1. add more backend/vendor documented observations;
2. ingest real measured paths as Evidence becomes available;
3. build compatibility coverage views that preserve exact-vs-generic scope.