# Graduation Machine Design Capstone Card

<figure>
  <img src="../../assets/diagrams/graduation-design-review.svg" alt="Graduation Machine Design Capstone Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Graduation Machine Design Capstone Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## 1. Freeze the target

- use case:
- model/artifact identity:
- quant/backend:
- context/concurrency:
- quality target:
- PP/TG or serving SLO:
- privacy/network scope:
- budget/TCO horizon:

Do not rank hardware before the target is frozen.

## 2. Link the Slice 48 / Experiment 91 dossier

- target SHA:
- dossier path/hash:
- dossier decision:

Decision semantics remain:

~~~text
FAIL → REVISE
critical UNKNOWN / missing evidence → BLOCKED
all required PASS → ACCEPT
~~~

## 3. Architecture narrative

Explain why each component exists:
- GPU(s);
- runtime/backend;
- RAM;
- storage;
- PCIe/topology;
- PSU/cables;
- cooling/chassis;
- network/service scope.

## 4. Material-claim Evidence index

| Claim ID | Material claim | Evidence | Type | Conditions / scope |
|---|---|---|---|---|
| | | | | |

Evidence type examples:
- MEASURED;
- DERIVED;
- OFFICIAL;
- SELLER/COMMUNITY.

Never silently promote seller/community information to measured truth.

## 5. Performance / quality / SLO

Record only metrics whose workload identity is frozen.

- prompt processing:
- token generation:
- TTFT / ITL / tails:
- quality gate:
- sustained drift:
- energy / J-token:

## 6. Revision alternatives

For each alternative:

| Change | Failed gate / pressure addressed | New evidence required | New cost/risk |
|---|---|---|---|
| | | | |

Common families:
- smaller model/quant;
- lower context/concurrency;
- different GPU;
- multi-GPU;
- PSU/platform upgrade;
- cooling/service-policy revision.

## 7. Upgrade roadmap

Use evidence-triggered stages:

~~~text
NOW
→ required to meet current target

NEXT
→ trigger + next capability

LATER
→ optional measured-bottleneck response
~~~

No speculative shopping list.

## 8. Explicit non-claims

State what the report does not prove.

Minimum:
- not universal optimality;
- not future compatibility;
- not hidden-defect proof;
- not long-term reliability unless longitudinal evidence exists.

## 9. Final decision

- ACCEPT
- REVISE
- BLOCKED

The decision must match the linked gate evidence.

## 10. Graduation proof

A strong report demonstrates:
- causal reasoning;
- traceable evidence;
- correct uncertainty handling;
- a revision path;
- transfer to a new machine/workload.