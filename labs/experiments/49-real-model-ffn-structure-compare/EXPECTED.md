# Expected — Experiment 49

No universal real-model output.

A valid dense-model comparison derives:
```
attention projection baseline
vs
3 × hidden_size × intermediate_size
```

and records the chosen effective storage bits.

If MoE fields are present, the output must be treated as incomplete for the FFN/expert portion.

The script compares structure, not benchmark performance or model quality.
