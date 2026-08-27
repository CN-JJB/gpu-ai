# Intelligence Catalog Schema v1

The normative design is in:

~~~text
docs/specs/0002-intelligence-stations-data-contract.md
~~~

## Files

~~~text
intelligence/catalog/hardware.jsonl
intelligence/catalog/models.jsonl
intelligence/catalog/runtimes.jsonl
intelligence/catalog/market.jsonl
intelligence/catalog/compatibility.jsonl
intelligence/catalog/benchmarks.jsonl
~~~

Each line is one JSON object.

## Common fields

~~~json
{
  "schema_version": 1,
  "record_type": "hardware|model|runtime|market|compatibility|benchmark",
  "record_id": "opaque-stable-id",
  "source": {
    "evidence_class": "OFFICIAL|MEASURED|DERIVED|SECONDARY|SELLER|SYNTHETIC",
    "url": "https://... or repo-relative path",
    "observed_at": "YYYY-MM-DD"
  }
}
~~~

A source may also contain source_path, captured_at and notes.

Dynamic observations may add:

~~~json
"revalidate_after": "YYYY-MM-DD"
~~~

## Hardware

~~~json
{
  "hardware_id": "hw:...",
  "canonical_name": "...",
  "vendor": "...",
  "accelerator_kind": "discrete-gpu",
  "memory_gib": 24,
  "architecture": "Ampere"
}
~~~

## Model

~~~json
{
  "model_id": "model:...",
  "canonical_name": "...",
  "repository": "...",
  "architecture": "...",
  "license": "..."
}
~~~

## Runtime

~~~json
{
  "runtime_id": "runtime:...",
  "canonical_name": "llama.cpp",
  "repository": "ggml-org/llama.cpp"
}
~~~

## Compatibility

~~~json
{
  "hardware_id": "hw:...",
  "model_id": "model:...",
  "runtime_id": "runtime:...",
  "backend": "CUDA",
  "status": "DOCUMENTED_SUPPORTED",
  "observed_at": "2026-08-27",
  "scope": {
    "representation": "llama.cpp-compatible GGUF required",
    "measurement_required": true
  }
}
~~~

Compatibility statuses:

~~~text
MEASURED_SUPPORTED
DOCUMENTED_SUPPORTED
PARTIAL
EXPERIMENTAL
DOCUMENTED_UNSUPPORTED
UNKNOWN
~~~

See docs/specs/0003-intelligence-compatibility-preflight.md.

## Market

~~~json
{
  "hardware_id": "hw:...",
  "geography": "CN",
  "channel": "secondary-summary",
  "cohort": "used-consumer",
  "condition": "working-unverified",
  "price_state": "SECONDARY_REPORTED",
  "price": {
    "currency": "CNY",
    "value": 7400
  },
  "observed_at": "2026-08-22"
}
~~~

## Benchmark

~~~json
{
  "hardware_id": "hw:...",
  "model_id": "model:...",
  "artifact": {
    "sha256": "...",
    "bytes": 123,
    "quant": "Q4_K_M"
  },
  "runtime": {
    "name": "llama.cpp",
    "runtime_identity": "...",
    "backend": "CUDA",
    "build_identity": "..."
  },
  "workload": {
    "pp_tokens": 512,
    "tg_tokens": 128,
    "repetitions": 5,
    "context": 32768,
    "sequences": 1
  },
  "metrics": {
    "pp_tok_s": 0.0,
    "tg_tok_s": 0.0
  },
  "evidence": {
    "manifest_source": "...",
    "raw_result_source": "...",
    "packet_source": "..."
  },
  "synthetic": false
}
~~~

## Validation

~~~bash
python3 tools/intelligence/validate_catalog.py intelligence/catalog
~~~

Synthetic fixtures:

~~~bash
python3 tools/intelligence/validate_catalog.py tools/intelligence/fixtures/catalog --allow-synthetic
~~~