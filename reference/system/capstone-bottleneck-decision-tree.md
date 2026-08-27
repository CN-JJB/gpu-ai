# Capstone Bottleneck Decision Tree

## 0. Freeze identity

Before optimization:

- hardware
- runtime/build
- model SHA256
- workload
- baseline config

## 1. Does target workload fit?

### No / barely
Look at:
- weights
- KV
- workspace
- offload/spill
- concurrency

Candidate variable:
- quant
- context
- KV type
- memory capacity/sharding

### Yes
Continue.

## 2. What is slow?

### TG / decode
Ask:
- near bandwidth roof?
- model fully resident?
- weight bytes/token large?
- KV/context large?

Candidate:
- quant/backend
- KV/context
- speculative decoding

### PP / prefill
Ask:
- matrix hardware actually used?
- FA/backend available?
- large attention/GEMM workload?

Candidate:
- FlashAttention
- backend/kernel
- matrix datatype/layout

### Service TTFT / concurrency
Ask:
- queueing?
- slots?
- batching?
- repeated prefix?

Candidate:
- slots/batching
- prefix cache

### Multi-GPU
Ask:
- capacity goal or speed goal?
- P2P bandwidth?
- split mode?
- imbalance?

Candidate:
- layer/tensor split
- device placement
- one larger GPU

## 3. One variable only

Write:

```
baseline:
candidate:
intentional difference:
everything else frozen:
```

## 4. Measure

At minimum:
- PP
- TG
- memory
- thermal/power if available
- raw logs

## 5. Interpret

Use:

```
metric moved
→ mechanism
→ whether hypothesis survived
```

## 6. Next experiment

Never end with:
```
"optimized"
```

End with:
```
next unknown:
next variable:
expected result:
```
