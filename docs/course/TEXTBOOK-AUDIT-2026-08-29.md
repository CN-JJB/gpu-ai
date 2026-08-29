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

### Confirmed systematic opening-contract defect: lessons 34–49

The older serving/operations/whole-machine lesson style is content-rich but predates the current explicit opening contract.

All sixteen lessons in the following range were inspected at their opening sections:

~~~text
34 serving SLO
35 serving capacity
36 overload / admission
37 multi-tenant fairness
38 service exposure / privacy
39 operational reliability
40 safe upgrade / rollback
41 observability / diagnosis
42 power / energy
43 storage / model loading
44 host memory / swap / OOM
45 thermal / sustained performance
46 used-GPU validation
47 PSU / power delivery
48 whole-machine integration
49 graduation machine-design capstone
~~~

Confirmed result:

~~~text
lessons 34–49 with explicit Prerequisite Check at opening = 0 / 16
lessons 34–49 with explicit 真实问题 section at opening = 0 / 16
~~~

This is not a thin-content problem. These pages already contain substantial mechanisms, worked examples, experiments, retrieval practice, completion evidence, decision guidance and primary references. Their `<h1>` titles are often already phrased as the motivating question.

The defect is that the learner is not explicitly told:
- what minimum prior knowledge is assumed;
- what to do if that prerequisite is missing;
- which concrete local-LLM decision or failure creates the need for the lesson before entering numbered technical sections.

The new textbook contract requires prerequisite recovery rather than relying on sequence memory. Treat the entire 34–49 opening style as a real textbook-completion defect.

### Remediation batches

Apply tailored openings rather than empty compliance headings:

~~~text
Batch A — Serving
34 TTFT / ITL / tail / throughput
35 Little's Law / slots / KV
36 overload / admission / retry
37 fairness / quotas / borrowing
38 exposure / bind / auth / TLS / privacy

Batch B — Operations
39 readiness / restart / recovery
40 release gates / rollback
41 observability / incident diagnosis
42 power / energy efficiency

Batch C — Host / hardware reliability
43 storage / mmap / page cache / startup
44 host RAM / available / swap / OOM
45 thermal / clocks / sustained drift
46 used-GPU validation
47 PSU / connectors / headroom

Batch D — Integration
48 whole-machine hard gates / unknowns
49 graduation Evidence → design review
~~~

Each remediation should add:
1. a topic-specific `Prerequisite Check` with a fallback pointer or one-paragraph recovery;
2. an explicit `真实问题` that ties the concept to a local-LLM decision, SLO, failure mode, purchase risk or deployment risk;
3. no fabricated measurement and no new requirement to own hardware.

## Next authoring actions

1. Remediate Batch A (34–38) openings and re-review the full learner flow.
2. Remediate Batch B (39–42).
3. Remediate Batch C (43–47).
4. Remediate Batch D (48–49).
5. Finish the 338-file local-link scan or obtain an observable `Course Readiness` workflow PASS on the exact teaching head.
6. Re-run a substantive contract spot review across Foundations, vendor capstones, Transformer internals, serving/operations, used-GPU acceptance and whole-machine integration.
7. Only then consider freezing `TEXTBOOK COMPLETE`.

## Boundaries preserved

~~~text
real production benchmark rows = 0
synthetic evidence is not production evidence
automatic purchase decision = NOT-PERMITTED
unsafe hardware modification is not required for the stable course
~~~

Real Experiment 61/93 learner-owned evidence remains a later learning-phase activity and is not an authoring blocker.
