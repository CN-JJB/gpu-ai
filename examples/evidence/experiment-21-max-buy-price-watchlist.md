# Evidence — Experiment 21: Max Buy Price / Candidate Watchlist

状态：stable watchlist model complete; synthetic max-sticker logic ready; real manual watchlist template ready.

## Claim

> A buyer should derive a workload-specific sticker-price ceiling from total ownership constraints, not treat market median as a personal fair price. Price can only trigger BUY-CANDIDATE after hard gates and evidence gates pass.

## Max sticker model

```
max_sticker
=
total ownership budget
- platform extra
- PSU/cooling
- energy horizon
- repair reserve
- maintenance reserve
+ expected resale
```

This is:
```
personal budget ceiling
```

not:
```
objective GPU market value
```

## Experiment 37

Synthetic budget:

```
total             8000
platform           400
PSU/cooling        350
energy             500
repair reserve     500
maintenance        250
resale            1200
```

Verified:

```
max_sticker = 7200
watch_limit = 7920
```

Expected statuses:

```
A ask 6800 → BUY-CANDIDATE
B ask 6500 → NEEDS EVIDENCE
C ask 7600 → WATCH
D ask 4000 → SKIP
```

Key result:
- B is cheaper than A but evidence is insufficient;
- D is much cheaper but FIT fails;
- price alone cannot rescue the candidate.

## Experiment 38

Real watchlist requires:
- exact model;
- ask/price state;
- observed timestamp;
- hard-gate states;
- market evidence;
- condition evidence;
- personal ceiling.

The untouched template remains:
```
NEEDS EVIDENCE
```

by design.

## Evidence gate

Current default BUY-CANDIDATE rule in the lab requires:
- FIT PASS;
- SOFTWARE PASS;
- PERFORMANCE PASS;
- market evidence M2/M3;
- condition evidence C3/C4;
- ask <= max sticker.

This is intentionally conservative.

Learners may change evidence thresholds for their own risk tolerance, but must document the change.

## Staleness

The real evaluator marks common price observations older than seven days as stale by default.

Staleness does not prove the price is wrong.
It means:
```
refresh before relying on it
```

## Learner should reject

- market median = my fair value;
- cheap listing = buy;
- unknown performance can be inferred from specs;
- weak seller evidence should trigger alert;
- watchlist = auto-buy;
- one candidate without alternatives is sufficient;
- stale price can be used unchanged during a volatile market.
