# Expected — Experiment 51

No universal real-model numbers.

A valid result identifies:
- N routed experts;
- top-k where available;
- shared experts where available;
- expert dimensions;
- architecture-specific caveats.

The script's `3*d*d_ff` output is explicitly a common SwiGLU-like baseline.

If layer patterns or expert structures differ, do not multiply the per-layer baseline across all layers without inspecting the architecture.
