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

## Substantive contract spot review

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

### New substantive defect found

The older serving/operations lesson style can be content-rich while still missing explicit opening contract sections.

Confirmed examples:

~~~text
lessons/34-serving-slo/01-ttft-itl-tail-throughput.html
lessons/35-serving-capacity/01-littles-law-slots-kv.html
lessons/36-overload-admission/01-queue-reject-retry.html
~~~

These pages contain strong mechanisms, worked examples, experiments, retrieval practice, completion evidence and decision guidance, but do not currently expose explicit:

~~~text
Prerequisite Check
真实问题
~~~

The lesson title itself is often phrased as a question, but the new textbook contract calls for an explicit prerequisite recovery path. Treat this as a real textbook-completion defect.

## Next authoring actions

1. Audit lessons 34–49 for explicit prerequisite recovery and real-problem framing.
2. Add tailored `Prerequisite Check` sections where missing; do not add empty compliance headings.
3. Add/clarify `真实问题` framing where the learner motivation is only implicit.
4. Finish the 338-file local-link scan or obtain an observable `Course Readiness` workflow PASS on the exact teaching head.
5. Perform substantive spot review across the repaired serving/operations group after edits.
6. Only then consider freezing `TEXTBOOK COMPLETE`.

## Boundaries preserved

~~~text
real production benchmark rows = 0
synthetic evidence is not production evidence
automatic purchase decision = NOT-PERMITTED
unsafe hardware modification is not required for the stable course
~~~

Real Experiment 61/93 learner-owned evidence remains a later learning-phase activity and is not an authoring blocker.
