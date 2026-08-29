# Experiment 93 — Real Graduation Machine Design Report

硬件等级：L1–L3，取决于你的目标和已有机器。

## Goal

Produce the final human-readable Local-LLM machine design report from existing course Evidence.

This experiment:
- does not auto-purchase hardware;
- does not flash firmware;
- does not change PSU wiring;
- does not require the final machine decision to be ACCEPT.

A complete graduation packet may end in:

~~~text
ACCEPT
REVISE
BLOCKED
~~~

## Prerequisite

Complete Experiment 91 first.

You need:
- frozen target;
- Experiment 91 dossier;
- its ACCEPT / REVISE / BLOCKED decision;
- raw Evidence paths/hashes for material claims.

## 1. Copy templates

~~~bash
cp CAPSTONE-REPORT-TEMPLATE.md my-machine-report.md
cp capstone.template.json capstone.json
~~~

Do not overwrite the template in place.

## 2. Link, do not duplicate, Experiment 91

In capstone.json record:
- target identity/hash;
- Experiment 91 dossier path/hash;
- Experiment 91 machine decision.

The final report must not silently change the machine decision without new Evidence and a new dossier run.

## 3. Build the material-claim index

Every claim that can change:
- feasibility;
- purchase;
- safety;
- quality;
- performance/SLO;
- TCO;
- upgrade timing

needs:
- evidence reference;
- evidence type;
- scope/conditions.

Use Experiment 61 for the final Evidence Packet index when applicable.

## 4. Write the report

Fill CAPSTONE-REPORT-TEMPLATE.md.

Required narrative:
- goal/workload;
- model identity;
- architecture;
- hard-gate summary;
- benchmark/quality/SLO;
- TCO/risk;
- unknowns;
- revisions;
- upgrade roadmap;
- explicit non-claims;
- final rationale.

## 5. Validate completeness

~~~bash
python3 validate_capstone.py capstone.json
~~~

The validator returns two independent outputs:

~~~text
MACHINE DECISION: ACCEPT / REVISE / BLOCKED
CAPSTONE COMPLETENESS: COMPLETE / INCOMPLETE
~~~

A BLOCKED machine can still have a COMPLETE graduation packet.

## 6. Review against rubric

Use RUBRIC.md.

Graduation quality is based on:
- traceability;
- causal reasoning;
- uncertainty discipline;
- revision quality;
- transfer.

It is not based on buying expensive hardware.

## 7. Stop conditions

Do not proceed with purchase or modification when:
- the linked machine decision is BLOCKED;
- a safety/power-path claim is unresolved;
- the target identity changed and Experiment 91 has not been rerun.

## Final Evidence

Keep:
- final report;
- capstone.json;
- Experiment 91 dossier;
- Evidence Packet index/hash;
- raw benchmark/quality/SLO evidence;
- any redaction notes needed before publishing the report.

## Why this experiment

这是学生阶段的最终整合：不是再做一个新 benchmark，而是把已经产生的真实 Evidence 组织成一份别人可以复核的机器设计报告。

## Hypothesis

只要目标、Experiment 91 decision、material claims、raw evidence、revision 与 non-claims 全部可追踪，哪怕机器结论是 BLOCKED，这份毕业报告仍可达到 COMPLETE。

## Fixed variables

final report 必须绑定已冻结的 target 与 Experiment 91 dossier。没有新证据时不得在报告里私自改变 machine decision。

## What to observe

- claim index 是否覆盖会影响 feasibility/purchase/safety/quality/performance/TCO 的 material claims；
- 每个 claim 是否有 evidence type、scope/conditions；
- unknown/non-claims 是否显式；
- revision 是否回应 failed/unknown gates；
- validator 的 MACHINE DECISION 与 CAPSTONE COMPLETENESS 是否被正确区分。

## Troubleshooting

- COMPLETE 不等于 ACCEPT。
- evidence link 有路径不等于内容可信，仍需人工 review。
- target identity 改变必须重跑 Experiment 91。
- 发布报告前清理 secret/private prompt/个人识别信息。

## Evidence to save

保存 final report、capstone.json、Experiment 91 dossier、Packet index/hash、raw benchmark/quality/SLO 和 redaction notes。

## What this proves

完成后你证明的是：能独立设计、测量、解释、修订并审查一个 Local LLM 系统。

## What this does NOT prove

它不要求买最贵硬件，也不允许用缺失真实证据的漂亮文字代替验证。

## No-hardware fallback

在当前作者阶段不运行；未来上课时以你实际拥有/计划的系统完成。教材完整性不依赖预先伪造结果。

## Transfer question

毕业报告是 BLOCKED，但清楚指出唯一缺口、证据来源和下一步。为什么这仍可能比一个无证据的 ACCEPT 更优秀？
