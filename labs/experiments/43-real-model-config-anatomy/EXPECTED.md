# Expected — Experiment 43

There is no one correct model output.

A successful inspection identifies enough architecture fields to explain:

```
hidden width
+ layers
+ query/KV head relation
+ head dimension
+ FFN size
→ attention/MLP shapes
→ KV baseline
```

## Valid warning

If the config exposes:
- MoE;
- sliding attention;
- per-layer attention types;
- unusual head dimensions;

the correct result is to flag the simple homogeneous baseline as incomplete.

Do **not** force every modern config into a Llama-2-like dense architecture.
