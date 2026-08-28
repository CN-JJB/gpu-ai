# Intelligence Layer

动态情报与稳定课程内容物理分离。

稳定原则：
- docs/adr/0002-separate-stable-knowledge-from-dynamic-intelligence.md

Phase 4 specs：
- docs/specs/0002-intelligence-stations-data-contract.md
- docs/specs/0003-intelligence-compatibility-preflight.md
- docs/specs/0004-intelligence-measured-compatibility-ingestion.md
- docs/specs/0005-intelligence-comparable-benchmark-view.md
- docs/specs/0006-intelligence-explicit-price-performance.md
- docs/specs/0007-intelligence-tco-worksheet.md
- docs/specs/0008-intelligence-real-benchmark-intake.md
- docs/specs/0009-intelligence-cross-vendor-documented-coverage.md
- docs/specs/0010-intelligence-compatibility-coverage-matrix.md
- docs/specs/0011-intelligence-freshness-revalidation-queue.md
- docs/specs/0012-intelligence-market-cohort-coverage.md
- docs/specs/0013-intelligence-market-evidence-audit.md
- docs/specs/0014-intelligence-sold-marked-listing-evidence.md
- docs/specs/0015-intelligence-cross-market-signal-comparison.md
- docs/specs/0016-intelligence-cn-secondary-watch-signals.md
- docs/specs/0017-intelligence-market-evidence-selection-gate.md
- docs/specs/0018-intelligence-freshness-aware-watchlist-gate.md

Schema：
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

## Benchmark Evidence bridge

Benchmark intelligence preserves:

~~~text
hardware ID
+ model ID / exact artifact
+ runtime ID / backend / build
+ workload
+ metrics
+ raw Evidence
~~~

Preferred path:

~~~text
Experiment 61
→ tools/intelligence/verify_real_intake.py
→ INTAKE: READY
→ tools/intelligence/ingest_llama_bench.py
→ benchmark observation
→ tools/intelligence/ingest_measured_compatibility.py
→ exact MEASURED_SUPPORTED observation
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

Exact measured Evidence only applies to the scope it actually proves.

## Cross-vendor compatibility coverage

Current production documented paths for Qwen3-8B + llama.cpp:

~~~text
NVIDIA RTX 3090 → CUDA  → NEEDS-TEST
AMD RX 7900 XTX → HIP  → NEEDS-TEST
Apple M4 Max    → Metal → NEEDS-TEST
Intel Arc A770  → SYCL  → NEEDS-TEST
~~~

Query:

~~~bash
python3 tools/intelligence/compatibility_matrix.py intelligence/catalog   --model-id model:qwen:qwen3-8b   --runtime-id runtime:ggml-org:llama.cpp   --as-of 2026-08-28
~~~

Coverage is not a performance ranking.

## Freshness / revalidation

Dynamic observations with revalidate_after enter an operational refresh queue:

~~~bash
python3 tools/intelligence/freshness_report.py intelligence/catalog   --as-of YYYY-MM-DD   --within-days 30
~~~

States:

~~~text
STALE
DUE-TODAY
DUE-SOON
FRESH
~~~

STALE means revalidate before a current decision; it does not automatically mean false.

## Real market cohort

Current same-contract used-GPU asking observations:

~~~text
GLOBAL-EBAY
secondary-aggregated-ebay-active
used-consumer
used
MEDIAN_ASK
USD
~~~

Current rows:
- RTX 3090 24GB;
- RX 7900 XTX 24GB;
- Arc A770 16GB.

Query:

~~~bash
python3 tools/intelligence/market_matrix.py intelligence/catalog   --geography GLOBAL-EBAY   --channel secondary-aggregated-ebay-active   --cohort used-consumer   --condition used   --price-state MEDIAN_ASK   --currency USD   --as-of 2026-08-28
~~~

These are asking prices, not confirmed sales.

## Market evidence audit

Production MEDIAN_ASK rows preserve:
- active listing count;
- middle-half asking range;
- source methodology;
- source export timestamp;
- confirmed_sale=false.

Audit:

~~~bash
python3 tools/intelligence/market_evidence_audit.py intelligence/catalog   --geography GLOBAL-EBAY   --channel secondary-aggregated-ebay-active   --cohort used-consumer   --condition used   --price-state MEDIAN_ASK   --currency USD   --as-of 2026-08-28
~~~

Current descriptive sample bands:

~~~text
RTX 3090      → BROAD-SAMPLE
RX 7900 XTX   → LIMITED-SAMPLE
Arc A770 16GB → SMALL-SAMPLE
~~~

These labels are operational heuristics, not statistical confidence scores.

## Sold-marked listing evidence

A separate US peer-to-peer cohort preserves marketplace pages marked SOLD:

~~~text
US
offerup-sold-marked-listing
used-consumer
used
SOLD_MARKED_LISTING_PRICE
USD
~~~

Important:

~~~text
SOLD page label
!=
confirmed negotiated transaction amount
~~~

Current descriptive displayed-price medians:

~~~text
RTX 3090      → 950 USD
RX 7900 XTX   → 700 USD
Arc A770 16GB → 200 USD
~~~

Tool:

~~~bash
python3 tools/intelligence/sold_marked_market.py intelligence/catalog
~~~

Every record keeps confirmed_transaction_price=false.

## Cross-market signal comparison

Explicit comparison of the two USD contracts currently shows:

~~~text
RTX 3090      1499 ask vs 950 sold-marked display  → -36.6%
RX 7900 XTX   1020 ask vs 700 sold-marked display  → -31.4%
Arc A770 16GB  330 ask vs 200 sold-marked display  → -39.4%
~~~

Tool:

~~~bash
python3 tools/intelligence/compare_market_contracts.py intelligence/catalog   --left-geography GLOBAL-EBAY   --left-channel secondary-aggregated-ebay-active   --left-cohort used-consumer   --left-condition used   --left-price-state MEDIAN_ASK   --left-currency USD   --right-geography US   --right-channel offerup-sold-marked-listing   --right-cohort used-consumer   --right-condition used   --right-price-state SOLD_MARKED_LISTING_PRICE   --right-currency USD
~~~

This is a cross-contract signal gap, not a confirmed transaction discount or fair-value discount.

## China secondary watch

Current CN watch contract:

~~~text
CN
secondary-summary
used-consumer
working-unverified
SECONDARY_REPORTED
CNY
~~~

Current rows:

~~~text
RTX 3090 → 7400 CNY
Arc A770 → 1450 CNY
~~~

Both preserve:

~~~text
direct_listing_capture=false
confirmed_sale=false
~~~

The A770 record is due for revalidation on 2026-08-28.

## Market evidence selection gate

The Intelligence catalog reuses the stable Slice 19 grading system:

~~~text
M3 direct normalized platform evidence
M2 current transparent secondary aggregation
M1 weak/article summary
M0 unknown
~~~

Current production mapping:

~~~text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
~~~

Tool:

~~~bash
python3 tools/intelligence/market_evidence_gate.py intelligence/catalog
~~~

Experiment 38 bridge:

~~~text
M0/M1 → NEEDS-STRONGER-MARKET-EVIDENCE
M2/M3 → market-evidence sub-gate ELIGIBLE
~~~

M3 remains claim-scoped. Current SOLD-marked M3 rows do not prove the negotiated transaction amount.

## Freshness-aware purchase use

Market grade and freshness are separate gates.

~~~text
CURRENT + M2/M3 → ELIGIBLE
DUE-TODAY → REVALIDATE-NOW
STALE → STALE-REVALIDATE
UNSCHEDULED / INVALID → REVALIDATION-SCHEDULE-REQUIRED
~~~

Every real market observation must now carry revalidate_after.

Experiment 38 also blocks due-today, stale, unknown and invalid market evidence from BUY-CANDIDATE.

GitHub Actions run #54 verifies this behavior.

## Comparable benchmark view

~~~text
same model
+ same artifact SHA
+ same quant
+ same workload
→ descriptive comparison group
~~~

No cross-group tok/s leaderboard.

## Price/performance

Implemented only when:
- one comparable benchmark group is selected;
- exact market records are explicitly selected;
- market contracts match.

No automatic latest-price join.

## TCO

Implemented as an evidence-linked scenario:

~~~text
purchase
+ platform delta
+ electricity
+ risk reserve
- resale estimate
→ TCO
~~~

TCO does not override:
- capacity;
- compatibility;
- safety;
- quality/SLO hard gates.

## Verification

I01–I17 GitHub Actions compile and end-to-end self-test:

~~~text
run #54
head bbf624e44579cbc765974bf8b5070330002f294e
SELFTEST: PASS
~~~

Evidence:
- examples/evidence/intelligence-i01-i06-selftest-verification.md
- examples/evidence/intelligence-08-cross-vendor-documented-coverage.md
- examples/evidence/intelligence-09-compatibility-coverage-matrix.md
- examples/evidence/intelligence-10-freshness-revalidation.md
- examples/evidence/intelligence-11-market-cohort-coverage.md
- examples/evidence/intelligence-12-market-evidence-audit.md
- examples/evidence/intelligence-13-sold-marked-listings.md
- examples/evidence/intelligence-14-cross-market-signal.md
- examples/evidence/intelligence-15-cn-secondary-watch.md
- examples/evidence/intelligence-16-market-evidence-selection-gate.md
- examples/evidence/intelligence-i01-i16-ci-selftest.md
- examples/evidence/intelligence-17-freshness-aware-watchlist.md

The previous I11–I16 verification split is closed: GitHub Actions run #48 executed py_compile and the complete selftest successfully.

## Current production-data boundary

The production benchmark catalog is intentionally empty until a real Experiment 61 Evidence Packet is ingested.

Missing Evidence stays missing; synthetic fixture results remain under tools/intelligence/fixtures/.

任何动态条目都应记录来源、采集日期、版本/测试环境、可复现性与置信信息。
