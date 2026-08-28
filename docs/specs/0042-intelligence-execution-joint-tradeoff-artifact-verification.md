# Spec 0042 — Intelligence reproducible execution-variable joint tradeoff artifact

Status: implemented in I41.

## Problem

I40 produces a joint execution-variable PP/TG × PPL artifact.

Like every derived artifact in this lane, it must not be trusted merely because its arithmetic is self-consistent.

## Independent verifier

I41 adds `verify_execution_joint_tradeoff.py`.

It rebuilds the complete I40 object from:
- baseline/candidate Experiment 61 manifests;
- baseline/candidate benchmark records;
- I39 quality comparison;
- baseline/candidate sealed quality bundles;
- baseline/candidate exact model artifacts;
- shared corpus;
- quality-variable contract.

The supplied joint JSON must exactly equal the rebuilt object.

## Tamper model

The dedicated self-test replaces:
- PP baseline/candidate/delta/ratio/percent;
- TG baseline/candidate/delta/ratio/percent;
- PPL baseline/candidate/delta/ratio/percent;

with coherent arithmetic.

Verification still blocks because the edited values cannot be reproduced from the evidence roots.

## Symmetry

After I41:

~~~text
model-artifact path:
I33 → I36 → I37 → I38

execution-variable path:
I35 → I39 → I40 → I41
~~~

Both paths now have:
- sealed metric roots;
- independently reproducible comparison artifacts;
- performance-quality binding;
- independently reproducible joint artifacts.

## Trust boundary

I41 closes the derived-artifact provenance gap for execution-variable joint evidence.

It does not create a score, significance claim, SLO proof or purchase recommendation.
