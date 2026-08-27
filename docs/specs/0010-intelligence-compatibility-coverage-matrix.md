# Spec 0010 — Compatibility Coverage Matrix

Status: implemented  
Date: 2026-08-28

## Goal

Provide one auditable query over the compatibility catalog without collapsing:
- vendors;
- backends;
- freshness;
- documented vs measured support;
- generic vs exact scope.

## Query

~~~bash
python3 tools/intelligence/compatibility_matrix.py intelligence/catalog \
  --model-id model:qwen:qwen3-8b \
  --runtime-id runtime:ggml-org:llama.cpp \
  --as-of 2026-08-28
~~~

## Output row

Each observation shows:
- vendor;
- hardware;
- backend;
- catalog status;
- preflight decision;
- scope kind;
- observed date;
- revalidation date;
- evidence class;
- record ID.

## Scope semantics

~~~text
GENERIC
→ product/backend/model documented observation

EXACT
→ artifact/build/profile-scoped measured observation
~~~

The matrix does not let one exact measured result silently become family-wide support.

## Decision semantics

Same as I02:

~~~text
MEASURED_SUPPORTED → PASS-MEASURED
DOCUMENTED_SUPPORTED → NEEDS-TEST
PARTIAL / EXPERIMENTAL → REVIEW
DOCUMENTED_UNSUPPORTED → FAIL
UNKNOWN → BLOCKED
stale → STALE-REVALIDATE
~~~

## Current production expectation

For Qwen3-8B + llama.cpp on 2026-08-28:

~~~text
NVIDIA/CUDA → NEEDS-TEST
AMD/HIP → NEEDS-TEST
Apple/Metal → NEEDS-TEST
Intel/SYCL → NEEDS-TEST
~~~

No performance ordering is produced.

## Non-goals

This matrix is not:
- a fastest-GPU table;
- a price ranking;
- a TCO ranking;
- a universal support guarantee;
- a replacement for exact measured Evidence.