# Expected — Experiment 29

```bash
python3 check_lineage.py
```

Expected:

```
score: 10/10
```

## Key lessons

- EU / XVE / Xe-Core are not CUDA-core aliases.
- XMX is matrix acceleration, but backend mapping is still required.
- Arc A-series = Alchemist/Xe-HPG.
- Arc B-series = Battlemage/Xe2.
- SLM is on-chip scratchpad, not VRAM.
- subgroup width is not one universal Intel number.
- Level Zero is software API/runtime layer.
