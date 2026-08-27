# Local-LLM Graduation Machine Design Report

## Executive decision

Machine decision:
- ACCEPT / REVISE / BLOCKED

Graduation packet:
- COMPLETE / INCOMPLETE

One-paragraph rationale:

## 1. Goal / workload

- use case:
- model/artifact:
- model hash:
- quant/backend:
- context:
- concurrency:
- quality target:
- PP/TG or serving SLO:
- privacy/network scope:
- budget:
- TCO horizon:

Why these targets matter:

## 2. Proposed machine architecture

### GPU(s)
- identity:
- VRAM:
- topology:
- why selected:

### Runtime/backend
- exact version/commit:
- why selected:

### Host platform
- CPU role only as needed for this workload:
- RAM:
- motherboard / PCIe:
- storage:
- PSU / cable topology:
- cooling / chassis:
- network / service exposure:

## 3. Experiment 91 link

- target SHA256:
- dossier path:
- dossier hash:
- dossier machine decision:

Do not rewrite PASS/FAIL/UNKNOWN by hand without rerunning the dossier.

## 4. Hard-gate summary

| Gate | Requirement | Status | Evidence | Why sufficient for this claim |
|---|---|---|---|---|
| model/capacity | | | | |
| runtime/backend | | | | |
| topology | | | | |
| host RAM | | | | |
| storage | | | | |
| PSU capacity | | | | |
| PSU cables | | | | |
| thermal/sustained | | | | |
| quality | | | | |
| serving/SLO | | | | |
| privacy/network | | | | |
| budget | | | | |

## 5. Material-claim Evidence index

| Claim ID | Claim | Evidence type | Source/path/hash | Scope / conditions |
|---|---|---|---|---|
| C1 | | | | |

Evidence type:
- MEASURED;
- DERIVED;
- OFFICIAL;
- SELLER/COMMUNITY.

## 6. Performance / quality / SLO

### Workload identity
- manifest:
- prompt/input:
- output target:
- concurrency:
- backend/config:

### Results
- PP:
- TG:
- TTFT:
- ITL:
- tail latency:
- quality gate:
- sustained drift:
- power / energy:

### Interpretation

What is the measured bottleneck or current headroom?

## 7. TCO / operational risk

- purchase price:
- mandatory platform upgrades:
- energy estimate:
- cooling/noise:
- repair/risk reserve:
- driver/runtime maintenance:
- resale uncertainty:
- downtime/recovery implications:

## 8. Unknowns / blockers

For each unknown:
1. exact claim;
2. why it matters;
3. current evidence;
4. how to resolve;
5. whether purchase/use is blocked.

## 9. Revision alternatives

| Revision | Failed gate / pressure addressed | Variable changed | New evidence required | New cost/risk |
|---|---|---|---|---|
| R1 | | | | |

Do not write only “buy a better GPU.”

## 10. Upgrade roadmap

### NOW
What must be done for the current declared target?

### NEXT
For each item:
- evidence trigger:
- action:
- new validation required:

### LATER
For each item:
- evidence trigger:
- optional action:
- why it is not justified yet:

## 11. What this Evidence does NOT prove

Minimum explicit statements:
1.
2.
3.
4.

Consider:
- universal optimality;
- future runtime compatibility;
- hidden hardware defects;
- long-term reliability;
- future resale/market price;
- quality on tasks outside the evaluation set.

## 12. Evidence Packet

- packet index path:
- packet SHA256:
- raw evidence paths:
- redactions:
- publication-safe copy:

## 13. Final rationale

Explain:
- why the machine decision follows from the evidence;
- why no failed gate is averaged away;
- why each UNKNOWN remains UNKNOWN;
- what revision would be tested first if needed;
- what would make you change this decision.

## 14. Transfer check

Pick one unseen alternative machine or changed workload.

Explain:
- which gates change;
- which evidence can be reused;
- which evidence must be collected again;
- whether the final decision could change and why.