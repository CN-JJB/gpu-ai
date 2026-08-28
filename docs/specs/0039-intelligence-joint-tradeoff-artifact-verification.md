# Spec 0039 — Intelligence independently reproducible joint tradeoff artifact

Status: implemented in I38.

## Problem

I37 makes the PPL side of the joint artifact independently reproducible, but the emitted `joint.json` itself remains another derived artifact.

A consumer could edit PP/TG and PPL values together and keep every ratio/percent internally consistent.

Without replaying the source chain, that tamper is not detectable from arithmetic alone.

## Reusable builder

I38 refactors the I37 joint logic into:

~~~text
build_joint_tradeoff_evidence(...)
~~~

The builder:
- reloads both Experiment 61 manifests;
- validates the one-variable contract;
- binds both benchmark records to their manifests;
- invokes I36 to reproduce the I33 quality comparison;
- rebuilds the complete schema-v2 joint object.

## Independent verifier

`verify_joint_tradeoff.py` receives:
- supplied joint artifact;
- baseline/candidate manifests;
- baseline/candidate benchmark records;
- I33 quality comparison;
- baseline/candidate sealed quality bundles;
- baseline/candidate model artifacts;
- shared corpus.

It rebuilds the expected joint object and requires exact JSON-object equality.

## Tamper model

The dedicated test edits:
- PP baseline/candidate/delta/ratio/percent;
- TG baseline/candidate/delta/ratio/percent;
- PPL baseline/candidate/delta/ratio/percent;

while keeping each block arithmetically coherent.

Verification still blocks because none of those edited values reproduce the original evidence roots.

## Trust boundary

I38 proves the entire I37 joint artifact is reproducible.

It does not add:
- statistical significance;
- a weighted score;
- ACCEPT/REJECT;
- deployment SLO proof;
- purchase recommendation.
