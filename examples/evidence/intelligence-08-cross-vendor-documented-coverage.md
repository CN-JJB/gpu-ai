# Evidence — Intelligence I08: Cross-Vendor Documented Coverage

Date: 2026-08-28  
Status: verified

## Added production hardware entities

~~~text
hw:amd:radeon-rx-7900-xtx:24g
hw:apple:mac-studio-m4-max-40gpu:64g
hw:intel:arc-a770:16g
~~~

The existing NVIDIA RTX 3090 entity remains the NVIDIA seed.

## Added production compatibility observations

~~~text
RX 7900 XTX + Qwen3-8B + llama.cpp + HIP
→ DOCUMENTED_SUPPORTED

M4 Max 40-core / 64GB + Qwen3-8B + llama.cpp + METAL
→ DOCUMENTED_SUPPORTED

Arc A770 16GB + Qwen3-8B + llama.cpp + SYCL
→ DOCUMENTED_SUPPORTED
~~~

All use:

~~~text
measurement_required = true
~~~

## Four-ecosystem preflight

The production self-test now checks:

~~~text
NVIDIA / CUDA
AMD / HIP
Apple / METAL
Intel / SYCL
~~~

Expected for all four:

~~~text
PREFLIGHT: NEEDS-TEST
~~~

Final execution result:

~~~text
SELFTEST: PASS
~~~

## No fabricated performance

No PP/TG values were added to production.

The production benchmark catalog remains empty.

## Evidence boundary

The observations mean:
- the current backend path is documented;
- the concrete hardware is documented;
- Qwen3 loader support exists upstream.

They do not mean the exact local build/artifact has been measured.

## Source snapshot

See:
- intelligence/gpu/llama-cpp-cross-vendor-qwen3-2026-08-28.md