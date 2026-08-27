# Capstone Card

## Question

What exact bottleneck do I think limits this workload on this hardware, and does changing one variable move the expected metric?

## Hardware

- system:
- accelerator:
- VRAM / unified memory:
- memory bandwidth source/value:
- topology if relevant:
- thermal/power mode:

## Runtime

- OS:
- driver:
- llama.cpp version/commit:
- backend:
- build source/options:

## Model

- source/repository:
- revision:
- filename:
- bytes:
- SHA256:
- architecture:
- params:
- quant:

## Frozen workload

- PP tokens:
- TG tokens:
- repetitions:
- context/depth:
- KV type:
- threads:
- device/offload:
- serving concurrency if relevant:

## Baseline

- exact command:
- PP:
- TG:
- memory:
- temperature:
- power:
- raw JSON:
- startup log:

## Bottleneck hypothesis

Choose/describe:
- CAPACITY
- TG_BANDWIDTH
- PP_KERNEL
- KV_CONTEXT
- SERVING_QUEUE
- PREFIX_REUSE
- SPECULATIVE_OPPORTUNITY
- INTERCONNECT
- OTHER

Evidence:

## One intentional variable

- field:
- baseline value:
- candidate value:
- expected affected metric:
- success criterion:

Everything intentionally frozen:

## Candidate

- exact command:
- PP:
- TG:
- memory:
- temperature:
- power:
- raw JSON:
- startup log:

## A/B discipline

Paste output of:
```
python3 validate_ab.py baseline-manifest.json candidate-manifest.json
```

## Comparison

Paste output of:
```
python3 compare_bench.py baseline.json candidate.json
```

Additional:
- memory delta:
- power delta:
- temperature delta:

## Interpretation

1. Did the predicted metric move?
2. Did an unexpected metric move?
3. Does the result support or reject the bottleneck hypothesis?
4. Is the improvement practically meaningful?
5. What tradeoff appeared?

## Negative result

If candidate is worse, explain why that is still useful evidence.

## Next experiment

- next unknown:
- next single variable:
- expected result:

## Transfer

How would the hypothesis change on:
- NVIDIA:
- AMD:
- Apple:
- Intel:

Only answer ecosystems you can justify.
