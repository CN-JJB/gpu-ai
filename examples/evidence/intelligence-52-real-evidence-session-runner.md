# Intelligence I52 — real evidence session runner

Date: 2026-08-28

## Added

~~~text
tools/intelligence/run_real_evidence_session.py
tools/intelligence/real_evidence_session_selftest.py
labs/experiments/61-real-benchmark-evidence-packet/real-evidence-session.template.json
docs/specs/0053-intelligence-real-evidence-session-runner.md
~~~

## Purpose

Operationally compose the existing real-evidence chain without weakening it:

~~~text
benchmark seal
→ quality seal
→ PPL extraction
→ real intake
~~~

The runner accepts exact argv arrays and uses no shell.

## PACKET detail

The benchmark PACKET includes profile, prompt manifest, corpus and quality identity so the existing I24–I27 gates can authenticate them.

## Boundary

Synthetic selftests require explicit allowance and are not ingested into production.

A READY session is ready for deliberate review/ingestion, not a purchase decision.
