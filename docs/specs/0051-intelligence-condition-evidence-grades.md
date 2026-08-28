# Spec 0051 — Intelligence condition-evidence provenance grades

Status: implemented in I50.

## Why this exists

Experiment 38 already requires C3/C4 condition evidence, but the repository had no stable C0–C4 definition.

I50 introduces the definition explicitly rather than pretending an older mapping existed.

## Separation of axes

Condition evidence has two independent axes:

~~~text
provenance strength:
C0 C1 C2 C3 C4

technical acceptance:
ACCEPT REVIEW REJECT
~~~

A strong, reproducible REJECT is still strong evidence.

Therefore ACCEPT is not the definition of C3.

## I50 production mapping

A non-synthetic, independently reproducible I44 acceptance packet maps to:

~~~text
C3
LEARNER-OWNED-PACKET-BOUND-REPRODUCIBLE-I44
~~~

The underlying acceptance decision remains a separate field.

Synthetic I44 fixtures map to C0.

## C4

C4 is reserved for C3 plus independent corroborating inspection provenance.

I50 does not emit it.

## Reproducibility

The condition-grade artifact is independently rebuilt from:
- I44 acceptance artifact;
- acceptance case;
- acceptance PACKET.

Changing a synthetic C0 artifact to C3 without changing the evidence roots is blocked.

## Trust boundary

C3 proves evidence provenance strength, not card health and not purchase suitability.
