# Textbook Completion Audit — 2026-08-29

Status: COMPLETE — TEXTBOOK COMPLETE checkpoint accepted

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

## Full-lesson substantive signal audit

After the 34–49 opening remediation, the full stable lesson corpus was re-scanned for three learner-contract signals across all 62 HTML lessons:

~~~text
no-hardware fallback / hardware-independent path = 62 / 62
troubleshooting / failure-recovery guidance = 62 / 62
decision boundary / decision rule = 62 / 62
~~~

The first pass narrowed five pages for manual review. Lesson 37 already contained a substantive starvation troubleshooting path. Lessons 38, 45, 47 and 48 were strengthened with concrete troubleshooting flows covering:
- service exposure and trust-boundary diagnosis;
- sustained thermal/performance drift diagnosis;
- PSU/power-delivery failure handling with explicit safe-stop boundaries;
- blocked whole-machine dossier / unknown-closure diagnosis.

A separate opening-marker scan found one older page, Lesson 13 matrix units, that had a real problem but no explicit `Prerequisite Check`. That page was repaired. Across the stable lesson corpus, every page now contains both prerequisite-recovery semantics and a real-problem framing, although older templates do not always use the same exact HTML heading level.

These scans are substantive audit signals, not a substitute for the repository-integrity/link audit.

## Course Readiness execution boundary

The repository contains:

~~~text
.github/workflows/course-readiness.yml
tools/course/audit_student_readiness.py
~~~

The GitHub connector still does not expose an observable push-triggered Course Readiness run for the current teaching head, and the execution container cannot clone GitHub because outbound DNS/network access is unavailable.

That CI limitation is now separated from repository readiness itself. The checks implemented by `audit_student_readiness.py` were reproduced through the repository connector:

~~~text
lesson slices = 49
lesson HTML = 62
experiments = 93
challenges = 12
foundations = 6
required lesson markers = verified
required challenge markers = verified
experiment README/EXPECTED = verified
recognized real-experiment result/report templates = verified
local-link corpus = 338 / 338 checked
broken local links = 0
repo-escaping local links = 0
~~~

Therefore:

~~~text
connector-equivalent Course Readiness audit = PASS
GitHub Actions exact-head CI PASS = NOT OBSERVED
~~~

The second line is an observability/tooling boundary, not an unresolved textbook defect.

## Local-link audit complete

The readiness script validates every local Markdown/HTML link under lessons, curriculum, challenges and experiments.

The full corpus was checked using the same rules as `audit_student_readiness.py`: ignore anchors and remote schemes, strip query/fragment, URL-decode the relative target, reject repo escapes, and require the resolved target to exist.

~~~text
Markdown/HTML corpus = 338 / 338
broken local links = 0
repo-escaping local links = 0
~~~

The first 60 files are curriculum/early-lab files and were unchanged by the later lesson remediations. Files 60–337 were re-scanned on the remediated teaching tree. The final Lesson 46/49 troubleshooting edits added no new local links, and their existing local targets were re-checked individually.

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

## Final substantive spot review

High-risk learner transitions were spot-reviewed after the full-corpus signal scan:
- Foundation 00 — complete learner-flow exemplar;
- NVIDIA vendor capstone — prerequisite → evidence chain → troubleshooting → decision;
- Lesson 29 model dossier — config/artifact/KV hypothesis path with worked example, no-hardware transfer and non-claims;
- serving/operations 34–45 — explicit prerequisite/real-problem remediation plus failure recovery;
- Lesson 46 used-GPU acceptance — identity/link/load/sustained evidence plus explicit conflict troubleshooting;
- Lesson 48 system integration — hard gates, unknown debt and blocked-dossier troubleshooting;
- Lesson 49 graduation capstone — Evidence → Design Review with explicit review-failure recovery.

No remaining authoring blocker was found.

## TEXTBOOK COMPLETE checkpoint

The stable textbook is frozen as complete for the learner-start boundary.

~~~text
teaching-content checkpoint head = f514db1733f0e26a06e82e596e70922ab2458915
status = TEXTBOOK COMPLETE
next phase = learner Lesson 01
~~~

This checkpoint does **not** claim that future real learner benchmarks already exist. Experiment 61/93 real evidence remains learner-owned work performed later in the course.

## Boundaries preserved

~~~text
real production benchmark rows = 0
synthetic evidence is not production evidence
automatic purchase decision = NOT-PERMITTED
unsafe hardware modification is not required for the stable course
~~~

Real Experiment 61/93 learner-owned evidence remains a later learning-phase activity and is not an authoring blocker.
