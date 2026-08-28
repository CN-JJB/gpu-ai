# Intelligence I50 — condition-evidence provenance contract

Date: 2026-08-28

## Added

~~~text
reference/hardware/condition-evidence-grades.md
tools/intelligence/derive_condition_evidence_grade.py
tools/intelligence/verify_condition_evidence_grade.py
tools/intelligence/condition_evidence_grade_selftest.py
docs/specs/0051-intelligence-condition-evidence-grades.md
~~~

## Core rule

~~~text
real independently reproducible I44 packet
→ C3 provenance

synthetic fixture
→ C0
~~~

ACCEPT/REVIEW/REJECT stays separate.

C4 is reserved and not emitted.

Tampered C0 → C3 artifacts are blocked by independent reconstruction.
