# Current State

## Source of truth

- Repo: CN-JJB/gpu-ai
- Branch: main
- Stable course and dynamic Intelligence lane remain separate.

## Stable course

~~~text
Slices 01–49 implemented
Experiments 01–93 exist
Stable v1 mainline complete
~~~

## Active Phase 4 frontier

~~~text
I01–I19 catalog / compatibility / market evidence / refresh
I20–I27 benchmark + artifact + prompt + quality identity admission
I28–I32 sealed quality execution + exact argv + machine PPL + mandatory metric
I33 exact model-quality A/B
I34 performance × quality model A/B binding
I35 declared execution-variable quality contract
I36 reproducible model-quality comparison artifact
I37 mandatory I36 reproduction inside model joint tradeoff
I38 reproducible model joint tradeoff artifact
I39 reproducible execution-variable quality comparison artifact
I40 execution-variable performance × quality binding
I41 reproducible execution-variable joint tradeoff artifact
~~~

## Benchmark boundary

~~~text
real production benchmark rows = 0
~~~

No synthetic PP/TG/PPL value is production evidence.

Real non-synthetic intake still requires the strengthened chain:

~~~text
Experiment 61 manifest
+ raw llama-bench result
+ benchmark PACKET
+ canonical IDs
+ local model artifact
+ benchmark command record
+ hardware profile
+ prompt evidence
+ concrete quality corpus
+ quality identity
+ sealed quality command/raw streams
+ quality PACKET
+ machine-readable quality metric
→ I07/I20/I22/I23/I24/I25/I26/I27/I29/I30/I32 READY
→ ingest
→ validate
→ exact MEASURED_SUPPORTED
~~~

## Quality / tradeoff provenance

### Model-artifact path

~~~text
I33 exact model-quality A/B
→ I36 independently reproduce quality-comparison.json
→ I37 bind reproduced PPL to Experiment 61 PP/TG
→ I38 independently reproduce the full joint artifact
~~~

### Execution-variable path

~~~text
I35 explicit manifest-value ↔ quality-argv contract
→ I39 independently reproduce execution-variable quality comparison
→ I40 bind reproduced PPL to matching Experiment 61 PP/TG
→ I41 independently reproduce the full execution joint artifact
~~~

Current I35/I39/I40/I41 scope:
- only `variant.execution.*`;
- same model artifact;
- same quality executable;
- explicit per-side evaluation argv;
- declared argv semantics are auditable declarations, not independently proven upstream semantics.

Neither path emits:
- significance;
- a universal quality score;
- weighted recommendation score;
- ACCEPT/REJECT;
- purchase recommendation.

## Market evidence grades

~~~text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
~~~

Current production count remains:

~~~text
M1=3
M2=3
M3=9
market observations=15
~~~

Current active signals remain:

~~~text
GLOBAL-EBAY asks:
RTX 3090      1499 USD
RX 7900 XTX   1020 USD
Arc A770       330 USD

OfferUp SOLD-marked displayed medians:
RTX 3090       950 USD
RX 7900 XTX    700 USD
Arc A770       200 USD

China secondary:
RTX 3090      7400 CNY
Arc A770      1400 CNY
~~~

OfferUp rows remain `confirmed_transaction_price=false`.

The current China rows remain M1 secondary evidence, not confirmed transactions.

## Latest CI

GitHub Actions:

~~~text
workflow: Intelligence Self-Test
run #152
run id 33171494742
head 82b834197062216e33bde05c1ddc00f3fecd0027
job id 98849501909
conclusion success
~~~

The successful job explicitly passed:
- compile all Intelligence Python tools;
- full historical Intelligence self-test;
- benchmark capture / artifact / prompt / quality admission gates;
- quality execution + exact argv;
- quality metric extraction;
- model-quality comparison + artifact reproduction;
- model performance-quality binding + joint artifact reproduction;
- execution-variable comparison + artifact reproduction;
- execution performance-quality binding + joint artifact reproduction;
- quality execution + metric intake;
- market refresh.

## Evidence frontier

Newest evidence:
- examples/evidence/intelligence-34-performance-quality-ab-binding.md
- examples/evidence/intelligence-35-quality-execution-variable-contract.md
- examples/evidence/intelligence-36-quality-comparison-artifact-verification.md
- examples/evidence/intelligence-37-joint-tradeoff-quality-reproduction.md
- examples/evidence/intelligence-38-joint-tradeoff-artifact-verification.md
- examples/evidence/intelligence-39-quality-execution-variable-artifact-verification.md
- examples/evidence/intelligence-40-execution-performance-quality-binding.md
- examples/evidence/intelligence-41-execution-joint-tradeoff-artifact-verification.md

## Next

1. I42: add a unified tradeoff routing/admission gate that selects the verified model path (I38) or execution path (I41) from `intentional_variable`, and blocks unsupported runtime/hardware/system variables.
2. Acquire the first learner-owned real Experiment 61 packet through the real intake chain.
3. Refresh market evidence only when stronger/newer auditable provenance exists.
4. Keep recommendation/ranking blocked until real benchmark + quality/SLO + feasibility evidence exists.
