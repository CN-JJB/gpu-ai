# Intelligence Layer

动态情报与稳定课程内容物理分离。

稳定原则见：
- docs/adr/0002-separate-stable-knowledge-from-dynamic-intelligence.md

机器可读契约：
- docs/specs/0002-intelligence-stations-data-contract.md
- docs/specs/0003-intelligence-compatibility-preflight.md
- intelligence/schema/README.md

## Human-readable snapshots

### Hardware / GPU
GPU/平台规格、国内二手价格、全球参考、驱动/框架兼容、已知故障、改造项目。

### Models / LLM
模型家族、架构、参数、上下文、License、量化、后端兼容、质量与适用场景。

### Market
价格与交易状态必须保留渠道、cohort、condition 和 evidence class。

## Machine-readable catalog

~~~text
hardware entity
model entity
runtime entity
market observation
compatibility observation
benchmark observation
~~~

Files:

~~~text
intelligence/catalog/
~~~

Validate:

~~~bash
python3 tools/intelligence/validate_catalog.py intelligence/catalog
~~~

## Benchmark bridge

Benchmark intelligence must preserve:

~~~text
hardware
+ model artifact
+ runtime/backend/build
+ workload
+ metrics
+ raw Evidence
~~~

Preferred path:

~~~text
Experiment 61
→ tools/intelligence/ingest_llama_bench.py
→ benchmark observation
~~~

Do not manually create a second tok/s truth source.

## Compatibility preflight

Compatibility is not boolean.

~~~text
DOCUMENTED_SUPPORTED → NEEDS-TEST
MEASURED_SUPPORTED → PASS-MEASURED
PARTIAL / EXPERIMENTAL → REVIEW
DOCUMENTED_UNSUPPORTED → FAIL
UNKNOWN → BLOCKED
stale → STALE-REVALIDATE
~~~

## Derived metrics

Future tokens/s/元、VRAM/元、J/token、TCO views must:
- explicitly select compatible observations;
- preserve workload identity;
- preserve price cohort/evidence state;
- never average away a hard gate.

任何动态条目都应记录来源、采集日期、版本/测试环境、可复现性与置信信息。
