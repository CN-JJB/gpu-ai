# Evidence — Intelligence I02: Compatibility Preflight

Status: runtime entity + compatibility observation + preflight decision path implemented.

## Claim

Compatibility intelligence must distinguish documented support from measured support.

~~~text
DOCUMENTED_SUPPORTED
!=
MEASURED_SUPPORTED
~~~

## Status vocabulary

~~~text
MEASURED_SUPPORTED
DOCUMENTED_SUPPORTED
PARTIAL
EXPERIMENTAL
DOCUMENTED_UNSUPPORTED
UNKNOWN
~~~

These are not booleans.

## Preflight decisions

~~~text
MEASURED_SUPPORTED → PASS-MEASURED
DOCUMENTED_SUPPORTED → NEEDS-TEST
PARTIAL / EXPERIMENTAL → REVIEW
DOCUMENTED_UNSUPPORTED → FAIL
UNKNOWN / missing observation → BLOCKED
stale observation → STALE-REVALIDATE
~~~

## Production seed path

The first exact production path joins:

~~~text
hw:nvidia:geforce-rtx-3090:24g
+
model:qwen:qwen3-8b
+
runtime:ggml-org:llama.cpp
+
CUDA
~~~

Current upstream evidence documents:
- llama.cpp CUDA backend targeting NVIDIA GPUs;
- current Qwen3 model implementation in llama.cpp source;
- current CUDA build architecture handling for RTX 30-series / compute capability 8.6.

The catalog therefore stores:

~~~text
status = DOCUMENTED_SUPPORTED
measurement_required = true
~~~

Preflight result:

~~~text
NEEDS-TEST
~~~

not PASS-MEASURED.

## Why this matters

The documentation does not prove:
- a specific GGUF artifact loads;
- the selected quant kernel works;
- the local build flags are correct;
- the installed driver/toolkit stack works;
- performance or quality is acceptable.

A real run should create MEASURED evidence later.

## Validator rules

The catalog validator now checks:
- runtime canonical IDs;
- compatibility hardware/model/runtime references;
- compatibility status vocabulary;
- source/date/scope;
- documented support provenance;
- measured-support evidence requirements;
- freshness.

## Synthetic test

The fixture uses DOCUMENTED_SUPPORTED and must return:

~~~text
PREFLIGHT: NEEDS-TEST
~~~

This demonstrates the semantic boundary without claiming real performance.

## Next

Intelligence I03:
- ingest a measured compatibility observation from a real runtime test;
- add other vendor/backend paths;
- build support freshness views;
- keep exact artifact/quant constraints attached to evidence.