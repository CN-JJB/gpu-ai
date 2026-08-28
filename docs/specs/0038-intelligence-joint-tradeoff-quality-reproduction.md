# Spec 0038 — Intelligence mandatory quality-comparison reproduction in joint tradeoff

Status: implemented in I37.

## Problem

I36 can independently verify `quality-comparison.json`, but I34 still accepts that file directly.

That leaves a downstream trust gap: the verifier exists, yet the joint PP/TG × PPL tool does not require it.

## Decision

I37 makes I36 reproduction mandatory inside `bind_performance_quality_ab.py`.

The joint tool now requires:

~~~text
--quality-comparison
--baseline-quality-dir
--candidate-quality-dir
--baseline-model-artifact
--candidate-model-artifact
--quality-corpus
~~~

before it will inspect the Experiment 61 model A/B.

## Admission chain

~~~text
baseline sealed quality bundle
candidate sealed quality bundle
+ exact local model artifacts
+ shared corpus
→ I31/I32 metric verification
→ I33 exact quality comparison reconstruction
→ I36 exact comparison-object equality
→ Experiment 61 manifest/benchmark binding
→ JOINT TRADEOFF: PASS
~~~

A self-consistent edited comparison JSON is no longer sufficient.

## Joint schema v2

I37 upgrades the output to:

~~~text
joint_tradeoff_schema_version = 2
tradeoff_contract = experiment61-model-performance-quality-v2
~~~

and adds:

~~~text
quality_evidence.comparison_sha256
quality_evidence.comparison_contract
quality_evidence.baseline_metric_sha256
quality_evidence.candidate_metric_sha256
quality_evidence.verification = INDEPENDENTLY-REPRODUCED-I36
~~~

## Fail-closed test

The dedicated joint self-test changes both PPL values and recomputes delta/ratio/percent so the comparison remains arithmetically coherent.

I37 still blocks before producing joint evidence because I36 reconstruction disagrees with the sealed quality bundles.

## Scope

This remains the I33 model-artifact quality path.

Execution-variable quality evidence uses I35 and is not silently admitted into this I33 joint path.

## Trust boundary

I37 proves that the PPL side of a joint model A/B is independently rooted in sealed quality evidence.

It still does not prove:
- significance;
- deployment SLO fitness;
- universal task quality;
- causal superiority beyond the declared one-variable contract;
- purchase suitability.
