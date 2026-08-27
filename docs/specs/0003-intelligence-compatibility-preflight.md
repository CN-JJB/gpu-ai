# Spec 0003 — Compatibility Observation + Preflight

Status: implemented foundation  
Date: 2026-08-27

## Problem

Statements such as:

~~~text
CUDA supports NVIDIA
llama.cpp supports Qwen3
4-bit works
~~~

are not equivalent to:

~~~text
this exact model artifact
on this exact GPU
with this exact runtime build
has been measured successfully
~~~

Phase 4 needs compatibility intelligence that preserves this distinction.

## Runtime entity

Add a canonical runtime entity:

~~~text
runtime:ggml-org:llama.cpp
~~~

Runtime identity is separate from a particular benchmark build/commit.

A benchmark still records the exact build identity.

## Compatibility observation

A compatibility observation links:

~~~text
hardware_id
+ model_id
+ runtime_id
+ backend
+ dated support status
+ source
+ scope/constraints
~~~

## Status vocabulary

v1 statuses:

- MEASURED_SUPPORTED
- DOCUMENTED_SUPPORTED
- PARTIAL
- EXPERIMENTAL
- DOCUMENTED_UNSUPPORTED
- UNKNOWN

These are intentionally not booleans.

## Decision semantics

Preflight output:

~~~text
MEASURED_SUPPORTED
→ PASS-MEASURED

DOCUMENTED_SUPPORTED
→ NEEDS-TEST

PARTIAL / EXPERIMENTAL
→ REVIEW

DOCUMENTED_UNSUPPORTED
→ FAIL

UNKNOWN / no observation
→ BLOCKED
~~~

If the observation is stale:

~~~text
→ STALE-REVALIDATE
~~~

before a purchase/deployment decision.

## Why DOCUMENTED_SUPPORTED is not PASS

Official documentation can establish that a mechanism exists.

It does not prove:
- the exact artifact loads;
- the exact quant kernels exist;
- the chosen build flags are correct;
- the driver/runtime stack works on this machine;
- performance/quality is acceptable.

Therefore a documented path still needs a tiny real test.

## Evidence-class rules

For v1:
- DOCUMENTED_SUPPORTED / DOCUMENTED_UNSUPPORTED should normally use OFFICIAL evidence;
- MEASURED_SUPPORTED must use MEASURED evidence and preserve a run/evidence source;
- UNKNOWN is never promoted to supported;
- secondary/community evidence may create REVIEW/UNKNOWN intelligence but not silently become measured support.

## Seeded production observation

The initial production observation is deliberately narrow:

~~~text
NVIDIA GeForce RTX 3090
+ Qwen3-8B architecture identity
+ llama.cpp
+ CUDA backend
→ DOCUMENTED_SUPPORTED
→ NEEDS-TEST
~~~

The scope explicitly requires a llama.cpp-compatible artifact and a real runtime test before deployment.

## Freshness

Compatibility observations are dynamic.

Revalidate when:
- runtime major behavior changes;
- backend support changes;
- model architecture loader changes;
- CUDA/driver support boundary changes;
- a real deployment is imminent;
- the record reaches revalidate_after.

## Non-goals

The preflight does not:
- install a runtime;
- build CUDA;
- download model weights;
- run a benchmark;
- infer support from VRAM alone;
- convert an old support record into current truth.

## Next

I03 should ingest:
- measured compatibility results from real Experiment 61 / runtime preflight evidence;
- additional backends/vendors;
- exact artifact/quant constraints where official/current evidence exists.