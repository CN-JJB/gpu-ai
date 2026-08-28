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
I01–I41 implemented and CI verified
~~~

## Latest CI

~~~text
workflow: Intelligence Self-Test
run #152
run id 33171494742
head 82b834197062216e33bde05c1ddc00f3fecd0027
job id 98849501909
conclusion success
~~~

Every Intelligence Python tool compiled and every historical + I41 dedicated self-test passed.

## Production evidence boundary

~~~text
real production benchmark rows = 0
~~~

Do not promote synthetic PP/TG/PPL fixtures into production evidence.

Current market evidence remains unchanged from I18/I19. RTX 3090 China remains M1 SECONDARY_REPORTED around 7400 CNY from the existing observation; no stronger direct/confirmed transaction evidence has been acquired.

## Real intake chain

Non-synthetic Experiment 61 admission requires:
- manifest + raw result + benchmark PACKET;
- canonical hardware/model/runtime IDs;
- local exact model artifact;
- benchmark command record bound to `-m/--model`;
- hardware profile;
- Experiment 57 prompt evidence;
- concrete quality corpus;
- quality identity schema v2;
- sealed quality execution command/raw streams + quality PACKET;
- exact evaluation argv binding;
- independently reproducible machine PPL metric.

Only then may `verify_real_intake.py` return `INTAKE: READY`.

## Model-artifact A/B lane

~~~text
I33
exact tokenizer/corpus/fixture/evaluation argv/parser/executable contract
→ descriptive PPL comparison

I36
quality-comparison.json independently rebuilt from sealed quality bundles

I37
I36 reproduction required before binding PPL to Experiment 61 PP/TG

I38
entire model joint tradeoff independently rebuilt
~~~

Model joint tradeoff remains descriptive only.

## Execution-variable A/B lane

~~~text
I35
quality-variable-contract.json
manifest value ↔ exact executed quality argv

I39
schema-v2 execution-variable quality comparison
+ variable-contract SHA
+ metric SHAs
+ independent full reconstruction

I40
I39-reproduced PPL bound to matching Experiment 61 PP/TG

I41
entire execution joint tradeoff independently rebuilt
~~~

Current scope is `variant.execution.*` only.

The model artifact and quality executable must remain the same across the execution-variable quality A/B.

The declared flag semantics are not independently inferred from upstream; they remain explicit auditable assumptions.

## Fail-closed properties

The current lane blocks:
- missing real evidence;
- PACKET-only tampering;
- model/corpus/identity/argv drift;
- unsupported/ambiguous PPL raw output;
- edited metric artifacts;
- edited quality-comparison artifacts;
- edited joint tradeoff artifacts;
- undeclared Experiment 61 semantic drift;
- using the model-quality path for execution-variable attribution;
- changed executable in the execution-variable quality path.

Even coherently recomputed delta/ratio/percent fields are blocked if they do not reproduce source evidence.

## Next work

1. I42: unified verified-tradeoff routing gate:
   - `variant.model*` → I38;
   - `variant.execution.*` → I41;
   - runtime/hardware/system or unsupported variables → BLOCKED.
2. Acquire the first learner-owned real Experiment 61 packet.
3. Refresh market evidence only with auditable stronger/newer provenance.
4. No recommendation leaderboard yet.

No auto-purchase or unsafe hardware modification.
