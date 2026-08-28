# Spec 0037 — Intelligence reproducible quality comparison artifact

Status: implemented in I36.

## Problem

I31/I32 make each machine PPL independently reproducible.

I33 then writes `quality-comparison.json`.

Before I36, someone could edit both PPL values and recompute delta/ratio/percent so the comparison JSON remained internally self-consistent.

A downstream tool that saw only that JSON could not distinguish the edit from the original I33 output.

## Reusable reconstruction

I36 refactors I33 so the exact comparison object is built by a reusable function from:
- verified baseline quality bundle;
- verified candidate quality bundle;
- exact local baseline/candidate model artifacts;
- shared corpus.

The reconstruction includes:
- each machine PPL and reported uncertainty;
- each model SHA/bytes;
- each metric artifact SHA;
- fixed quality identity;
- quality executable SHA/bytes;
- PPL delta/ratio/percent.

## Independent verifier

`verify_quality_comparison.py`:
1. reruns I31/I32 verification for both sides;
2. reapplies the I33 exact comparability contract;
3. rebuilds the entire expected comparison object;
4. requires exact JSON-object equality with the supplied `quality-comparison.json`.

## Tamper model

The dedicated test changes:
- baseline PPL;
- candidate PPL;
- delta;
- ratio;
- percent change;

so all copied arithmetic is coherent.

Verification still blocks because the values do not reproduce the sealed metric bundles.

## Trust boundary

I36 closes the comparison-artifact provenance gap for the I33 exact model-quality path.

It does not yet make I34 automatically reverify the comparison bundle; that integration is a later gate.

It does not create a quality verdict or purchase recommendation.
