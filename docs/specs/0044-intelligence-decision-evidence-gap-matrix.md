# Spec 0044 — Intelligence decision evidence gap matrix

Status: implemented in I43.

## Problem

I42 can prove that a supported model/execution tradeoff went through the correct verified provenance route.

That is still far from a purchase decision.

Experiment 38 requires independent fit, software, performance, market, condition and price-policy evidence.

Experiment 90 separately models whole-machine feasibility.

A verified PP/TG × PPL comparison must not silently stand in for those missing domains.

## I43 matrix

I43 reruns I42 from the source roots and reports separate components:

~~~text
verified_tradeoff
real_benchmark_provenance
exact_measured_compatibility
current_market_evidence
whole_machine_feasibility
condition_acceptance
performance_target
price_ceiling
~~~

No weighted score is used.

## Automated checks

### Verified tradeoff

The full I42 route is rerun.

### Real benchmark provenance

Both benchmark records must be:
- record_type=benchmark;
- non-synthetic;
- source.evidence_class=MEASURED;
- linked to packet evidence.

### Exact measured compatibility

The candidate path requires a current, non-synthetic:

~~~text
MEASURED_SUPPORTED
~~~

record matching:
- hardware_id;
- model_id;
- runtime_id;
- backend;
- exact artifact SHA;
- exact runtime build.

A general documented support observation is not enough.

### Market evidence

The selected market record must:
- be non-synthetic;
- match candidate hardware_id;
- carry the expected stable M0–M3 grade;
- be CURRENT;
- satisfy the existing Experiment 38 market component, currently M2/M3.

This does not claim a confirmed transaction amount unless that exact amount is independently proven.

### Whole-machine feasibility

If supplied, the Experiment 90 case is evaluated with the same no-weighted-score hard-gate semantics.

Only ACCEPT satisfies this component.

## Deliberate blockers

I43 explicitly does **not** invent missing contracts.

Until later slices, these remain BLOCKED:
- machine-readable Experiment 38 C3/C4 condition acceptance;
- explicit target performance/SLO threshold tied to measured candidate metrics;
- personal sticker-price ceiling/watch-band policy.

Therefore current production readiness remains BLOCKED.

## Output

~~~text
decision_evidence_gap_schema_version = 1
components = independent status/reason objects
blockers = [...]
decision_readiness = BLOCKED | READY-FOR-HUMAN-REVIEW
automatic_purchase_decision = NOT-PERMITTED
~~~

Even READY-FOR-HUMAN-REVIEW would not mean BUY.

## Synthetic boundary

The dedicated self-test deliberately supplies synthetic tradeoff, compatibility and market fixtures.

I43 must keep them BLOCKED as production decision evidence while allowing the synthetic Experiment 90 case to exercise only feasibility logic.

## Trust boundary

I43 is a missing-evidence reporter.

It does not rank hardware, set price ceilings, infer condition grades, or purchase anything.
