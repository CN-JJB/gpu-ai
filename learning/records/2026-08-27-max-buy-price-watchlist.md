# Learning / Build Record — 2026-08-27 Max Buy Price / Watchlist

## Slice

21 — Workload-specific max-buy-price and candidate watchlist.

## Production output

Research:
- `research/market/0002-max-buy-price-watchlist.md`

Reference:
- `reference/market/max-buy-price-watchlist-card.md`

Lesson:
- `lessons/21-watchlist/01-max-buy-price.html`

Labs:
- `labs/experiments/37-max-buy-price-model/`
- `labs/experiments/38-real-candidate-watchlist/`

Evidence:
- `examples/evidence/experiment-21-max-buy-price-watchlist.md`

## Stable logic

```
hard gates
→ total budget
→ non-GPU TCO
→ risk/maintenance reserve
→ sticker ceiling
→ market evidence
→ condition evidence
→ status
```

Statuses:
- SKIP
- NEEDS EVIDENCE
- WATCH
- BUY-CANDIDATE
- KEEP

No automatic purchase.

## L0 result

Synthetic max sticker:
```
7200
```

The lab proves:
```
cheapest != best candidate
```

because fit/evidence can block the decision.

## Practical completion

The course now has a continuous hardware acquisition chain:

```
architecture
→ workload sizing
→ cross-vendor decision
→ China market normalization
→ transaction acceptance
→ price ceiling/watchlist
```

## Next production direction

Return to practical local-LLM systems work with a selected hardware profile.

Recommended next slice:

```
hardware profile
→ reproducible runtime build
→ model artifact
→ baseline PP/TG
→ telemetry
→ bottleneck diagnosis
→ one controlled optimization
→ before/after Evidence
```

This should become a capstone loop that reuses Slices 01–21.
