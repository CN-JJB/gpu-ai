# Learning / Build Record — 2026-08-27 Benchmark / Workload Manifest

## Slice

33 — Unified benchmark identity and Evidence Packet.

## Why

Earlier experiments separately tracked:
- hardware/runtime/model;
- prompt/token identity;
- quality.

This slice joins them into one machine-readable comparison contract.

## Core model

```
fixed
+
variant
+
audit
```

One declared semantic path beneath:

```
variant.*
```

may change.

## Semantic block insight

Quantization A/B legitimately changes:
- artifact SHA;
- bytes;
- quant label.

Therefore:

```
intentional_variable = variant.model
```

is valid.

This is stricter and more useful than the false rule:
```
model SHA must always be identical
```

## Validator self-check

Synthetic valid quant A/B:
- model block changed;
- prompt fixed;
- PASS.

Synthetic invalid candidate:
- model changed;
- prompt token hash also changed;
- FAIL with undeclared prompt difference.

## Artifacts

Reference:
- `reference/system/benchmark-workload-manifest.md`

Lesson:
- `lessons/33-benchmark-manifest/01-one-semantic-variable.html`

Labs:
- `labs/experiments/60-benchmark-manifest-validator/`
- `labs/experiments/61-real-benchmark-evidence-packet/`

## Next

Integrate serving workloads:
- TTFT;
- ITL;
- request throughput;
- concurrency;
- prompt-length/output-length distributions;
- latency percentiles;
- SLO tradeoffs.
