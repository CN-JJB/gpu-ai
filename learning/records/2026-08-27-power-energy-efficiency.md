# Learning / Build Record — 2026-08-27 Power / Energy Efficiency

## Slice

42 — Watts, joules, J/token, tokens/J, board-vs-wall measurement and electricity/TCO connection.

## Production output

Research:
- `research/llm/0024-power-energy-efficiency.md`

Reference:
- `reference/llm/power-energy-efficiency.md`

Lesson:
- `lessons/42-power-energy/01-watts-joules-per-token.html`

Labs:
- `labs/experiments/78-power-energy-model/`
- `labs/experiments/79-real-nvidia-energy/`

Evidence:
- `examples/evidence/experiment-42-power-energy-efficiency.md`

## Verified L0

```
300W @ 60 tok/s
→ 5.0 J/token

220W @ 50 tok/s
→ 4.4 J/token

180W @ 42 tok/s
→ 4.285714 J/token
```

The fastest synthetic configuration is not the most energy-efficient.

## Integration verification

```
100→120→140W over 2s
→ 240J
→ avg 120W

50W idle baseline
→ 140J incremental
```

## Stable skill

Learner can separate:
```
watts
energy
speed
energy efficiency
electricity cost
```

and label GPU-board vs whole-system measurement.

## Next

Storage/model loading:
- GGUF bytes on disk;
- sequential read bandwidth;
- mmap/page cache;
- cold vs warm model load;
- storage speed vs GPU inference speed;
- why a slow disk can hurt startup without changing steady TG.
