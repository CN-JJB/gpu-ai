# Experiment 37 — Max Sticker Price from Total Budget

硬件等级：L0

## 默认 synthetic scenario

```
total ownership budget = 8000
platform extra         = 400
PSU/cooling            = 350
energy horizon         = 500
repair reserve         = 500
maintenance reserve    = 250
expected resale        = 1200
```

Then:

```
max sticker
= 8000 - 400 - 350 - 500 - 500 - 250 + 1200
= 7200
```

## Candidates

Synthetic:

- A ask 6800, hard gates PASS, evidence strong → BUY-CANDIDATE
- B ask 6500, hard gates PASS, evidence weak → NEEDS EVIDENCE
- C ask 7600, hard gates PASS → WATCH
- D ask 4000, FIT FAIL → SKIP

## Run

```bash
python3 evaluate_watchlist.py
```

All values are synthetic and do not represent real GPUs.