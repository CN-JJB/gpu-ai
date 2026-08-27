# Learning / Build Record — 2026-08-27 China Secondhand GPU Market

## Slice

19 — China secondhand GPU market methodology.

## Production output

Research:
- `research/market/0001-china-secondhand-gpu-market-methodology.md`

Reference:
- `reference/market/china-secondhand-gpu-sampling-card.md`

Lesson:
- `lessons/19-secondhand-market/01-price-is-not-a-number.html`

Labs:
- `labs/experiments/33-secondhand-market-normalization/`
- `labs/experiments/34-real-secondhand-market-snapshot/`

Evidence/intelligence:
- `examples/evidence/experiment-19-china-secondhand-market.md`
- `intelligence/market/china-used-gpu-market-2026-08-27.md`

## Stable market model

```
raw listing
→ exact SKU/VRAM
→ stock/mod/repair cohort
→ condition evidence
→ ASK/SOLD/QUOTE state
→ deduplicate
→ median/Q1-Q3
→ evidence grade
→ candidate dossier
```

## Key result

Price evidence can be weak even when a number looks precise.

Current direct Xianyu sold-data coverage is insufficient for a high-confidence median, so the snapshot preserves secondary signals without upgrading them to M3.

## L0 result

Synthetic 3090 search:
- raw 10;
- normalized target 6;
- excluded 4;
- ASK median 7500 synthetic CNY.

The lab demonstrates why search-result averages are invalid.

## Current market lesson

August 2026 is volatile.

Current secondary signals show:
- large-VRAM NVIDIA cards higher than prior month;
- Arc A770 16G rapidly repriced by local-AI demand.

Market snapshot lifetime should therefore be short.

## Next work

Build the transaction/inspection practical slice:

```
seller conversation
→ photo/serial evidence
→ remote proof request
→ safe in-person/receipt workflow
→ post-arrival identity
→ memory/compute/thermal tests
→ accept / dispute / return evidence packet
```

Then connect live candidates to a price-threshold watchlist.
