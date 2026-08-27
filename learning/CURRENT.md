# Current State

## Source of truth

- Repo: CN-JJB/gpu-ai
- Branch: main
- Course is independent; do not return to old fork history.

## Historical archive

The previous long-form CURRENT state through Slice 45 is preserved byte-for-byte at:

~~~text
learning/archive/CURRENT-through-slice45-2026-08-27.md
~~~

Detailed per-slice history remains in:

~~~text
learning/records/
examples/evidence/
~~~

This file intentionally tracks only the active frontier.

## Completed frontier

~~~text
Slices 01–49 implemented
Experiments 01–93 exist
~~~

The stable v1 mainline now spans:
- GPU architecture / execution / memory / Roofline;
- NVIDIA / AMD / Apple / Intel GPU ecosystems;
- LLM memory, quantization, KV and modern model architecture;
- reproducible local inference and serving;
- multi-GPU / interconnect;
- benchmark manifests, quality gates and Evidence Packets;
- serving SLO/capacity/admission/fairness;
- privacy/reliability/rollback/observability;
- power/energy, storage, host RAM/OOM and thermal behavior;
- secondhand market / purchase / used-GPU acceptance;
- PSU / power-delivery integration;
- whole-machine feasibility;
- graduation Machine Design Capstone.

## Recent frontier

### Slice 46 — Used-GPU Validation

Deep acceptance path:

~~~text
identity
→ VRAM
→ runtime recognition
→ PCIe
→ ECC/RAS/XID/error evidence
→ sustained LLM
→ ACCEPT / REVIEW / REJECT
~~~

### Slice 47 — PSU / Power Delivery

Independent gates:

~~~text
capacity/headroom
+
connector/cable compatibility
+
transient/documentation uncertainty
~~~

No PSU opening, exposed-mains probing, protection bypass or intentional overload.

### Slice 48 — Whole-Machine System Integration

Machine feasibility:

~~~text
known required FAIL → REVISE
critical UNKNOWN → BLOCKED
all required gates PASS → ACCEPT
~~~

No weighted score may average away a hard failure.

Experiment 91 is the real Evidence-linked machine dossier.

### Slice 49 — Graduation Machine Design Capstone

Final learner deliverable:

~~~text
goal/workload
→ Experiment 91 dossier
→ material-claim Evidence index
→ architecture narrative
→ benchmark/quality/SLO
→ TCO/risk
→ revision alternatives
→ evidence-triggered upgrade roadmap
→ explicit non-claims
→ final rationale
→ transfer check
~~~

New stable distinction:

~~~text
machine feasibility
!=
graduation packet completeness
~~~

Therefore:

~~~text
MACHINE DECISION: BLOCKED
CAPSTONE COMPLETENESS: COMPLETE
~~~

can be a valid graduation result.

Experiment 92 contains synthetic ACCEPT / REVISE / BLOCKED review cases.

Experiment 93 contains the real final report template, rubric and completeness validator.

## Stable design rule

Always evaluate in this order:

~~~text
workload/model identity
→ feasibility hard gates
→ blocking unknowns
→ measured performance/quality/SLO
→ preferences/TCO
→ decision
→ explicit limits
→ revision / upgrade path
~~~

Do not let speed, price, prose quality or a weighted score erase:
- insufficient VRAM;
- unsupported runtime;
- invalid power path;
- unresolved purchase/safety evidence;
- missing material-claim Evidence.

## Next actions

1. Complete Experiment 93 with a real learner-owned target/machine.
2. Use that real graduation packet to identify actual curriculum gaps.
3. Patch stable Lessons only when the real Evidence shows a gap.
4. Otherwise move the major build frontier to Intelligence Stations:
   - dynamic hardware data;
   - current backend/model compatibility;
   - market observations;
   - benchmark bridge;
   - recommendation/TCO tooling.
5. Keep dynamic data out of stable Lessons unless it is converted into a durable reasoning rule.
