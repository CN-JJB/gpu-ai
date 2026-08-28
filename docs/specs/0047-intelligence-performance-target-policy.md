# Spec 0047 — Intelligence explicit performance target policy

Status: implemented in I46.

## Problem

A verified PP/TG × PPL tradeoff is descriptive.

It does not prove the candidate meets the learner's target.

I43 therefore keeps `performance_target` blocked.

## Explicit policy

I46 introduces a no-weight threshold policy:

~~~json
{
  "performance_target_policy_schema_version": 1,
  "policy_id": "...",
  "comparison_id": "...",
  "requirements": {
    "min_pp_tok_s": 1000,
    "min_tg_tok_s": 50,
    "max_candidate_ppl": null,
    "max_ppl_percent_change": 5
  }
}
~~~

All fields are optional individually, but at least one must be active.

## Verified source

Before evaluating the thresholds, I46 reruns I42.

The policy comparison_id must equal the verified Experiment 61 comparison.

The candidate PP/TG/PPL values come only from the verified joint artifact.

## Semantics

Each active requirement is an independent hard check:

~~~text
candidate PP >= min_pp_tok_s
candidate TG >= min_tg_tok_s
candidate PPL <= max_candidate_ppl
PPL percent change <= max_ppl_percent_change
~~~

No weights, normalization or composite score are used.

## Reproducible result

The output records:
- policy ID and SHA;
- joint artifact SHA;
- verified route;
- actual candidate metrics;
- exact checks;
- PASS/FAIL;
- whether either benchmark input is synthetic.

An independent verifier rebuilds the object exactly.

## Synthetic boundary

Synthetic fixtures may exercise the policy engine and can produce a synthetic PASS.

The output preserves:

~~~text
synthetic_input = true
~~~

A later production-readiness bridge must reject that as real purchase evidence.

## Trust boundary

I46 proves whether a verified tradeoff satisfies an explicit threshold policy.

It does not choose the thresholds or turn PASS into a purchase recommendation.
