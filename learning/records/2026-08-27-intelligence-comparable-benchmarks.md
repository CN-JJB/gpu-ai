# Learning / Build Record — 2026-08-27 Comparable Benchmark View

## Frontier

Phase 4 Intelligence Stations — I04.

## Implemented

Spec:
- docs/specs/0005-intelligence-comparable-benchmark-view.md

Tool:
- tools/intelligence/comparable_benchmarks.py

Fixtures:
- second synthetic hardware entity;
- second benchmark observation using the same artifact/workload.

Self-test now verifies:
- one comparable group;
- two observations;
- descriptive-only status;
- no cross-group ranking.

## Stable rule

~~~text
same tok/s unit
!=
comparable benchmark
~~~

Comparison requires the same model artifact, quant and workload identity.