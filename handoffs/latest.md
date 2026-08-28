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
I01–I52 implemented
latest implementation CI: run #170 success
~~~

CI identity:

~~~text
run id 33190099651
head 29e23bca982989b31597de61eb3be43ec25c01f7
job id 98913094544
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

## I52 real evidence session runner

Use:

~~~text
labs/experiments/61-real-benchmark-evidence-packet/real-evidence-session.template.json
tools/intelligence/run_real_evidence_session.py
~~~

The session runner orchestrates only existing gates:

~~~text
benchmark capture
→ quality capture
→ PPL extraction
→ verify_real_intake
~~~

It accepts explicit argv arrays and uses no shell.

On success it emits `REAL SESSION: READY`, `session-summary.json`, and `intake-args.json`.

Do not ingest automatically. Review the real evidence first.

## Next work

1. Fill the I52 real-evidence session template on the actual benchmark machine.
2. Run I52 and require `REAL SESSION: READY`; manually review before ingestion.
3. After reviewed ingestion, derive exact measured compatibility.
4. Acquire the first real Experiment 87/I44 acceptance packet for the same candidate hardware.
5. Create explicit I46/I48 policies and run I43.
6. Refresh market evidence only with newer/stronger provenance; no leaderboard before real evidence.

No auto-purchase, no unsafe hardware modification.
