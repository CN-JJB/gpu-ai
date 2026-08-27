# Evidence — Intelligence I09: Compatibility Coverage Matrix

Date: 2026-08-28  
Status: verified

## Claim

A cross-vendor compatibility view must preserve:
- vendor;
- hardware;
- backend;
- documented vs measured status;
- generic vs exact scope;
- freshness;
- evidence class.

It must not become a performance leaderboard.

## Production query

~~~bash
python3 tools/intelligence/compatibility_matrix.py intelligence/catalog \
  --model-id model:qwen:qwen3-8b \
  --runtime-id runtime:ggml-org:llama.cpp \
  --as-of 2026-08-28
~~~

## Verified result

The production matrix contains four observations:

~~~text
NVIDIA / CUDA
AMD / HIP
Apple / METAL
Intel / SYCL
~~~

Decision count:

~~~text
NEEDS-TEST=4
~~~

Coverage status:

~~~text
COVERAGE: PRESENT
~~~

## Scope discipline

The tool distinguishes:

~~~text
GENERIC
EXACT
~~~

A future exact MEASURED_SUPPORTED record will remain scoped to its artifact/build/profile.

It will not silently promote the entire hardware family.

## Guardrail

The tool explicitly states:

~~~text
Coverage is not a performance ranking.
~~~

## Verification

The full intelligence self-test remains:

~~~text
SELFTEST: PASS
~~~