# Research Note 0015 — Workload-Specific Max Buy Price / Watchlist

日期：2026-08-27

## Problem

A market snapshot tells you:

```
what sellers are asking
```

It does not tell you:

```
what you should pay
```

The useful decision is:

> Given my exact workload, system budget, extra platform cost, risk tolerance and evidence quality, what is the maximum sticker price I should accept for this exact candidate?

This is not a universal GPU fair-value formula.

It is a **personal purchase ceiling**.

---

# Part I — Hard gates still come first

A candidate cannot enter BUY-CANDIDATE state unless:

## Fit gate
```
target workload fits
```

## Software gate
```
support path is acceptable
```

## Performance gate
If the learner has a minimum target:

```
PP >= minimum
TG >= minimum
```

or marked:
```
performance unknown
→ NEEDS EVIDENCE
```

No low price rescues a failed hard gate.

---

# Part II — Start from total-system budget, not GPU price

User defines:

```
B_total
```

= maximum total ownership budget for the chosen horizon.

Then reserve non-GPU costs:

```
platform_extra
PSU/cooling
cables/adapters
storage/RAM if required
expected energy
repair reserve
software/maintenance reserve
```

Expected resale can reduce net TCO if the learner wants to model it.

A simple sticker-price ceiling:

```
max_sticker
=
B_total
- platform_extra
- PSU/cooling
- energy
- repair reserve
- maintenance reserve
+ expected resale
```

This is a budget ceiling, not a claim about market value.

---

# Part III — Risk reserve must be explicit

Do not hide risk in a vague score.

Examples:

## Low-risk retail card
Maybe use a small repair reserve.

## Old datacenter card
Reserve for:
- cooling adaptation;
- host compatibility;
- support lifespan;
- uncertain history.

## Repaired/modded card
Reserve more for:
- failure probability;
- resale discount;
- debugging time.

The learner chooses the reserve.

The course does not invent a universal percentage.

---

# Part IV — Evidence confidence can block the alert

Even if:

```
asking price <= max_sticker
```

the candidate should remain:

```
NEEDS EVIDENCE
```

when critical fields are weak:

- identity E0/E1;
- software E0/E1;
- condition C0/C1;
- benchmark E0/E1 when performance is important.

This prevents a fake-low scam listing from triggering BUY-CANDIDATE.

---

# Part V — Market relationship

Once a candidate ceiling exists, compare it to normalized market evidence.

## Candidate cheap relative to your ceiling

```
ask <= max_sticker
```

Then:
- if evidence sufficient → BUY-CANDIDATE;
- if evidence weak → NEEDS EVIDENCE.

## Slightly above ceiling

```
max_sticker < ask <= watch_band
```

→ WATCH

The card may become interesting after negotiation or market movement.

## Far above ceiling

→ OVERPRICED FOR THIS WORKLOAD

This does not mean the market is irrational.
It means the candidate is too expensive **for your scenario**.

---

# Part VI — Why market median is not your ceiling

Suppose market median:

```
¥7,400
```

but your total-system budget leaves:

```
max_sticker = ¥6,600
```

Then the right decision is:

```
WAIT / choose another architecture
```

not:

```
"everyone pays 7400 so I should"
```

Conversely, if your workload strongly values a unique 32 GB capacity tier, a higher price may still be rational.

---

# Part VII — Watchlist status vocabulary

Use:

### SKIP
Hard gate fails.

### NEEDS EVIDENCE
Potentially viable, but critical evidence is missing.

### WATCH
Viable, but ask is above current personal ceiling.

### BUY-CANDIDATE
Hard gates pass, evidence sufficient, ask <= ceiling.

### OWNED / KEEP
Current hardware remains better than replacing under the scenario.

No automatic purchase action.

---

# Part VIII — Staleness

A watchlist must record:

- observed_at;
- price state;
- source;
- evidence grade;
- expiration.

For fast-moving used markets:

```
price observation older than 7 days
→ stale by default
```

for hot common SKUs.

Rare datacenter cards can use a longer window if supply is sparse, but confidence should reflect it.

---

# Part IX — Negotiation target

The ceiling is not the opening offer.

Three different numbers:

```
market anchor
negotiation target
absolute ceiling
```

Example:

```
normalized ASK median = 7400
your desired entry    = 6500
your absolute ceiling = 6800
```

Do not reveal the absolute ceiling automatically.

---

# Part X — Candidate portfolio

A good watchlist contains alternatives.

Example classes:

```
24 GB mature CUDA
16 GB cheap alternative
32 GB old datacenter
large unified-memory Mac
dual-card capacity option
```

This prevents emotional anchoring on one “dream card”.

---

# Part XI — Upgrade vs keep

The best used-GPU deal may still be worse than keeping current hardware.

Calculate:

```
incremental cost
=
new TCO
- current hardware resale/value
```

Then ask what it buys:

- +VRAM;
- +TG;
- +PP;
- +software lifespan;
- -power;
- -risk.

If the improvement does not matter to your workload:

```
KEEP
```

can be the best garbage-hardware decision.

---

# Stable claims to avoid

- “market median = fair price for me”;
- “cheap enough means buy”;
- “risk can be summarized by one generic 10% discount”;
- “benchmark unknown but specs imply performance”;
- “watchlist means auto-buy”;
- “old price observations remain valid indefinitely”;
- “one candidate should be watched without alternatives”.
