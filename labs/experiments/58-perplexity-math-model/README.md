# Experiment 58 — Cross-Entropy / Perplexity Toy Model

硬件等级：L0

## Goal

Compute quality metrics from correct-next-token probabilities without ML libraries.

Default:

Baseline:
```
[0.5, 0.25, 0.125, 0.5]
```

Candidate:
```
[0.48, 0.22, 0.10, 0.45]
```

## Run

```bash
python3 ppl.py
```

## Expected

Baseline:
```
CE ≈ 1.213007566
PPL ≈ 3.363585661
```

Candidate:
```
CE ≈ 1.337297424
PPL ≈ 3.808736185
```

```
PPL ratio ≈ 1.132344
ΔCE ≈ 0.124290
```

The candidate is worse on this synthetic token stream.

## Try

Change only one probability to 0.001.

Observe how strongly a confidently bad prediction affects NLL.
