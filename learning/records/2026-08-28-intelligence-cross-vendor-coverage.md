# Learning / Build Record — 2026-08-28 Cross-Vendor Documented Compatibility

## Frontier

Phase 4 Intelligence Stations — I08.

## Implemented

Spec:
- docs/specs/0009-intelligence-cross-vendor-documented-coverage.md

Dynamic snapshot:
- intelligence/gpu/llama-cpp-cross-vendor-qwen3-2026-08-28.md

Production catalog additions:
- AMD Radeon RX 7900 XTX 24GB;
- Apple Mac Studio M4 Max 40-core GPU / 64GB unified memory;
- Intel Arc A770 16GB;
- corresponding HIP / Metal / SYCL DOCUMENTED_SUPPORTED observations.

Evidence:
- examples/evidence/intelligence-08-cross-vendor-documented-coverage.md

## Verification

Production catalog validation and the full intelligence self-test pass.

The self-test explicitly confirms:

~~~text
NVIDIA/CUDA → NEEDS-TEST
AMD/HIP → NEEDS-TEST
Apple/Metal → NEEDS-TEST
Intel/SYCL → NEEDS-TEST
~~~

## Stable rule

~~~text
four ecosystems documented
!=
four ecosystems benchmarked
~~~

Production benchmarks remain empty until real Evidence passes I07 intake.