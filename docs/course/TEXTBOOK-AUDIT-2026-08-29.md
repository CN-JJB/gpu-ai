# Textbook Completion Audit — 2026-08-29

Status: ACTIVE — do not declare TEXTBOOK COMPLETE yet

## Scope

This audit follows `docs/course/STUDENT-TEXTBOOK-COMPLETION.md` and deliberately separates mechanical readiness from substantive teaching quality.

## Verified in this authoring pass

### Structural inventory

~~~text
lesson slices = 49
lesson HTML = 62
experiments = 93
challenge labs = 12
foundations = 6
~~~

Verified:
- Experiment 01–93 directories have required README/EXPECTED files.
- Real-experiment directories have a recognized result/report template.
- Challenge 01–12 have README/EXPECTED and required completion markers.
- Foundation 00–05 files exist.
- `curriculum/README.md` and `labs/challenges/CHALLENGE-CARD.md` exist.

### Thin-page audit

After the current authoring pass:

~~~text
stable lessons/*.html under 8 KiB = 0
~~~

This is only an audit signal. It is not proof of textbook quality.

### Lesson completion marker contract

The Course Readiness script requires every stable lesson to contain:
- `Retrieval Practice`
- `完成证据`
- `Primary Sources`
- complete HTML closing tags

A contract debt was found in lessons 14–18 and 20–33: many pages already had substantive Experiment Evidence / worksheets, but did not contain the literal `完成证据` heading.

This was repaired in commit:

~~~text
a9c24e4011817848c556d4898104b117bfb7ddc5
course: add lesson completion evidence contract
~~~

Manual re-check of the repaired 14–33 range found no remaining missing required marker in that range. Earlier/later lesson groups were already marker-compliant in the same audit.

### Content passes completed before this audit

- Experiment instruction textbook pass
- Foundation 00–05 learner-contract pass
- Challenge 01–12 teaching closure
- architecture/vendor thin-page pass
- Transformer/model-internals thin-page pass
- benchmark/quality/decision thin-page pass
- operations/power/used-GPU/whole-machine thin-page pass

Recent additions emphasize:
- causal mental models;
- worked examples and calculations;
- Experiment Evidence / Packet outputs;
- interpretation branches;
- failure recovery;
- no-hardware fallback;
- decision rules and non-claims;
- human-review boundaries for purchase/release decisions.

## Course Readiness execution boundary

The repository contains:

~~~text
.github/workflows/course-readiness.yml
tools/course/audit_student_readiness.py
~~~

However, commits written through the current GitHub connector did not produce an observable GitHub Actions run, and the execution container cannot clone GitHub because outbound DNS/network access is unavailable.

Therefore:

~~~text
Course Readiness CI PASS = NOT YET OBSERVED on the current head
~~~

Do not convert “no CI failure appeared” into PASS.

## Local-link audit frontier

The readiness script also validates every local Markdown/HTML link under lessons, curriculum, challenges and experiments.

Current corpus size:

~~~text
338 Markdown/HTML files
~~~

A direct connector-based scan has begun. The first 60 files checked using the same relative-link resolution rules had:

~~~text
broken local links = 0
~~~

The remaining link corpus is not yet fully re-scanned in this authoring session. The current pass did not intentionally add new local relative links to the repaired lesson completion sections.

## Substantive contract review

### PASS examples

Foundation 00 has:
- real problem;
- explicit mental model;
- worked example;
- no-hardware path;
- troubleshooting guidance;
- decision rule;
- transfer;
- retrieval practice;
- completion evidence;
- course-contract references.

Vendor Capstone NVIDIA has:
- prerequisite check;
- real problem;
- evidence chain;
- mechanism;
- worked troubleshooting example;
- no-hardware path;
- decision rule;
- transfer;
- completion evidence;
- primary sources.

### Opening-contract remediation complete: lessons 34–49

A systematic opening-contract defect was confirmed across lessons 34–49: the pages were content-rich, but all 16 previously entered numbered technical sections without an explicit prerequisite-recovery block or an explicit real-problem section.

The remediation is now complete across all four batches:

~~~text
Batch A — 34–38 serving / capacity / overload / fairness / exposure
Batch B — 39–42 reliability / upgrade / observability / power
Batch C — 43–47 storage / host RAM / thermal / used GPU / PSU
Batch D — 48–49 integration / graduation capstone
~~~

Each page now opens with:
- a topic-specific `Prerequisite Check`;
- a fallback/recovery explanation that does not require owning target hardware;
- an explicit `真实问题` tied to a local-LLM decision, SLO, failure mode, purchase risk or deployment risk.

A direct post-remediation re-check of all 16 pages found:

~~~text
Prerequisite Check = 16 / 16
真实问题 = 16 / 16
Retrieval Practice = 16 / 16
完成证据 = 16 / 16
Primary Sources = 16 / 16
~~~

No fabricated measurements were added. No lesson requires buying hardware, exposing a service to the public Internet, modifying PSU wiring, flashing a GPU, or performing another unsafe hardware modification.

## Next authoring actions

1. Finish the 338-file local-link scan or obtain an observable `Course Readiness` workflow PASS on the exact teaching head.
2. Re-run a substantive contract spot review across Foundations, vendor capstones, Transformer internals, serving/operations, used-GPU acceptance and whole-machine integration.
3. Fix any remaining integrity or learner-flow defect discovered by those checks.
4. Only then consider freezing `TEXTBOOK COMPLETE`.

## Boundaries preserved

~~~text
real production benchmark rows = 0
synthetic evidence is not production evidence
automatic purchase decision = NOT-PERMITTED
unsafe hardware modification is not required for the stable course
~~~

Real Experiment 61/93 learner-owned evidence remains a later learning-phase activity and is not an authoring blocker.
