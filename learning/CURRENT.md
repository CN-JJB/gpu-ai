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
I01–I19  catalog / compatibility / market evidence / refresh
I20–I32  real benchmark + artifact + prompt + sealed quality admission
I33–I41  reproducible model/execution performance × quality tradeoff paths
I42       automatic verified tradeoff routing
I43       decision evidence gap matrix
I44–I45  packet-bound used-GPU acceptance + readiness bridge
I46–I47  explicit performance-target policy + readiness bridge
I48–I49  explicit personal price-ceiling policy + readiness bridge
I50–I51  condition-evidence provenance grades + readiness bridge
~~~

## Structural status

All currently defined Experiment 38 / Intelligence decision-readiness domains now have machine contracts:

~~~text
verified tradeoff
real benchmark provenance
exact measured compatibility
current market evidence
whole-machine feasibility
used-GPU technical acceptance
explicit performance target
explicit personal price ceiling
condition-evidence provenance
~~~

I43 returns:

~~~text
READY-FOR-HUMAN-REVIEW
~~~

only when every component passes.

It always records:

~~~text
automatic_purchase_decision = NOT-PERMITTED
~~~

No BUY action is automated.

## Benchmark boundary

~~~text
real production benchmark rows = 0
~~~

No synthetic PP/TG/PPL value is production evidence.

Real non-synthetic Experiment 61 intake still requires:

~~~text
manifest
+ raw llama-bench
+ benchmark PACKET
+ canonical IDs
+ exact model artifact
+ benchmark command record
+ hardware profile
+ prompt evidence
+ concrete quality corpus
+ quality identity schema v2
+ sealed quality command/raw streams
+ quality PACKET
+ exact evaluation argv
+ machine-readable PPL metric
→ I07/I20/I22/I23/I24/I25/I26/I27/I29/I30/I32 READY
~~~

## Tradeoff provenance

### Model-artifact lane

~~~text
I33 exact quality A/B
→ I36 reproduce quality comparison
→ I37 bind PP/TG × PPL
→ I38 reproduce full joint artifact
~~~

### Execution-variable lane

~~~text
I35 explicit manifest-value ↔ quality argv contract
→ I39 reproduce execution-variable quality comparison
→ I40 bind PP/TG × PPL
→ I41 reproduce full joint artifact
~~~

### Unified route

~~~text
variant.model*      → I38
variant.execution.* → I41
other variables     → BLOCKED
~~~

I42 chooses the route from the validated manifests; callers cannot force it.

## Decision-readiness lane

~~~text
I43 gap matrix
I44 packet-bound ACCEPT / REVIEW / REJECT
I45 acceptance bridge
I46 explicit PP/TG/PPL hard thresholds
I47 performance-target bridge
I48 explicit max sticker + watch band
I49 price bridge using the same market record
I50 C0–C4 condition-evidence provenance contract
I51 condition provenance bridge
~~~

Condition has two separate axes:

~~~text
evidence strength: C0 C1 C2 C3 C4
technical health: ACCEPT REVIEW REJECT
~~~

Current production condition rule:
- real, learner-owned, PACKET-bound, independently reproducible I44 evidence → C3 provenance;
- synthetic evidence → C0;
- C4 is reserved and not emitted.

A C3 REJECT is strong evidence but still fails the separate used-GPU ACCEPT gate.

## Market evidence

Stable mapping:

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

OfferUp SOLD-marked displayed examples/medians:
RTX 3090       950 USD
RX 7900 XTX    700 USD
Arc A770       200 USD

China secondary:
RTX 3090      7400 CNY
Arc A770      1400 CNY
~~~

OfferUp rows still preserve `confirmed_transaction_price=false`.

China rows remain M1 secondary signals, not confirmed transactions.

## Latest implementation CI

~~~text
workflow: Intelligence Self-Test
run #165
run id 33189475466
head ba1ddf6a3c88d07721eefd30b7e452a8e93c42c6
job id 98910975890
conclusion success
~~~

The complete suite passed through I51.

## Newest evidence

- examples/evidence/intelligence-42-unified-tradeoff-routing.md
- examples/evidence/intelligence-43-decision-evidence-gap-matrix.md
- examples/evidence/intelligence-44-used-gpu-acceptance-artifact.md
- examples/evidence/intelligence-45-used-gpu-acceptance-readiness-bridge.md
- examples/evidence/intelligence-46-performance-target-policy.md
- examples/evidence/intelligence-47-performance-target-readiness-bridge.md
- examples/evidence/intelligence-48-price-ceiling-policy.md
- examples/evidence/intelligence-49-price-ceiling-readiness-bridge.md
- examples/evidence/intelligence-50-condition-evidence-grades.md
- examples/evidence/intelligence-51-condition-evidence-readiness-bridge.md

## Next

1. Stop expanding decision gates by default.
2. Acquire the first learner-owned real Experiment 61 benchmark + quality packet.
3. Derive exact `MEASURED_SUPPORTED` compatibility from that real path.
4. Acquire the first real Experiment 87 / I44 used-GPU acceptance packet for a candidate.
5. Fill explicit I46 performance-target and I48 price-ceiling policies.
6. Run I43 and inspect the remaining real blockers.
7. Refresh market evidence only when stronger/newer auditable provenance exists.
8. Keep ranking/recommendation blocked until real candidate evidence exists.

No auto-purchase or unsafe hardware modification.
