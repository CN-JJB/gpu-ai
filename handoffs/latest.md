# Handoff — GPU × Local LLM Course / Intelligence Stations

## Repo

~~~text
CN-JJB/gpu-ai
branch: main
~~~

## Stable course

~~~text
Slices 01–49
Experiments 01–93
v1 stable mainline complete
~~~

## Phase 4 frontier

~~~text
I01–I51 implemented
latest implementation CI: run #165 success
~~~

CI identity:

~~~text
run id 33189475466
head ba1ddf6a3c88d07721eefd30b7e452a8e93c42c6
job id 98910975890
~~~

## Production boundary

~~~text
real production benchmark rows = 0
~~~

Do not promote synthetic benchmark, PPL, market, acceptance, price-policy or readiness fixtures into production evidence.

## Real benchmark / quality admission

Non-synthetic Experiment 61 admission requires:
- manifest + raw result + benchmark PACKET;
- canonical hardware/model/runtime IDs;
- exact local model artifact;
- benchmark command record;
- hardware profile;
- Experiment 57 prompt evidence;
- concrete quality corpus;
- quality identity schema v2;
- sealed quality execution command/raw streams + quality PACKET;
- exact evaluation argv;
- independently reproducible PPL metric.

Only then may `verify_real_intake.py` return `INTAKE: READY`.

## Verified tradeoff lanes

~~~text
model:
I33 → I36 → I37 → I38

execution variable:
I35 → I39 → I40 → I41

routing:
I42
variant.model* → I38
variant.execution.* → I41
other → BLOCKED
~~~

No tradeoff artifact is a recommendation.

## Decision-readiness lane

I43 independently checks:
- verified tradeoff route;
- real MEASURED benchmark provenance;
- exact current MEASURED_SUPPORTED compatibility;
- current M2/M3 market evidence;
- Experiment 90 whole-machine feasibility;
- I44 real used-GPU ACCEPT;
- I46 explicit performance target PASS;
- I48 explicit price result WITHIN-CEILING using the same market record;
- I50 C3/C4 condition provenance.

Output is only:

~~~text
BLOCKED
or
READY-FOR-HUMAN-REVIEW
~~~

and always:

~~~text
automatic_purchase_decision = NOT-PERMITTED
~~~

## Condition evidence contract

I50 introduced the first stable C0–C4 definition because Experiment 38 previously referenced C3/C4 without defining them.

~~~text
C0 no production-usable evidence / synthetic
C1 seller/listing claim only
C2 current external evidence without learner-owned reproducible acceptance
C3 learner-owned PACKET-bound independently reproducible I44 evidence
C4 reserved: C3 + independent corroborating inspection provenance
~~~

Evidence strength is separate from technical health:

~~~text
C3 + ACCEPT → both condition-related gates can pass
C3 + REJECT → strong evidence, but used_gpu_acceptance blocks
~~~

I50 does not emit C4.

## Price policy contract

I48 does not infer fair value.

The learner supplies:
- exact market record;
- hardware ID;
- currency;
- personal max sticker;
- watch band.

Neutral outputs:

~~~text
WITHIN-CEILING
WATCH-BAND
ABOVE-BAND
~~~

Only real WITHIN-CEILING can satisfy the I49 price component. It is still not BUY.

## Performance policy contract

I46 uses only explicit hard thresholds:
- min candidate PP;
- min candidate TG;
- optional max candidate PPL;
- optional max PPL percent change.

No weighted score is used.

## Next work

1. Acquire first learner-owned real Experiment 61 packet.
2. Acquire first real Experiment 87/I44 acceptance packet for the same candidate hardware.
3. Create explicit I46 and I48 policies for the learner's workload/budget.
4. Run I43 and close only evidence-specific blockers.
5. Refresh market evidence when newer/stronger provenance exists.
6. Do not build a recommendation leaderboard before real evidence exists.

No auto-purchase, no unsafe hardware modification.
