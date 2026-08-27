# Result — Experiment 51

## Model identity

- repository:
- revision:
- config source:
- model_type:

## MoE fields

- layers:
- hidden size:
- routed experts:
- top-k:
- shared experts:
- expert FFN size:
- dense-first/MoE frequency:
- routing/scoring fields:

## Per-layer baseline

- one expert weights:
- one expert storage proxy:
- all routed experts/layer:
- active routed experts/token/layer:
- shared expert active baseline:

## Four quantities

### Total parameters

### Active parameters/token

### Resident placement

### Expected weight/interconnect traffic

## Prefill

- token count:
- likely expert batch sizes:
- weight reuse opportunity:
- imbalance risk:

## Decode

- active experts/token:
- expert weight-streaming risk:
- offload/interconnect risk:

## Conclusion

Why does the model's published active-parameter number fail to answer "will it fit my GPU?"
