# Evidence — Intelligence I01–I16 GitHub Actions Self-Test

Date: 2026-08-28  
Status: CI verified

## Run identity

```text
workflow: Intelligence Self-Test
run number: 48
run id: 33137329016
head sha: 097c8d4839314851e1f4b07267b3c7b2102d50e0
job: selftest
job id: 98740118394
event: push
conclusion: success
```

## Runner

```text
Ubuntu 24.04.4 LTS
Python 3.12.14
```

## Executed

```bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
```

Both workflow steps concluded:

```text
success
```

## Self-test result

The job log contains:

```text
SELFTEST: PASS
```

and explicitly confirms:
- production catalog validation;
- synthetic catalog isolation;
- benchmark bridge;
- comparable benchmark grouping;
- explicit price/performance;
- TCO arithmetic;
- documented-vs-measured compatibility;
- four-ecosystem NEEDS-TEST coverage;
- compatibility matrix;
- freshness queue;
- GLOBAL-EBAY MEDIAN_ASK cohort;
- market sample audit;
- MEDIAN_ASK negative validation;
- OfferUp SOLD-marked semantics;
- false confirmed-transaction rejection;
- cross-market signal comparison;
- China secondary watch semantics;
- false secondary-sale rejection;
- M1/M2/M3 market evidence selection gate;
- mismatched market evidence grade rejection;
- UNKNOWN compatibility blocking;
- real benchmark packet intake positive/negative cases;
- Experiment 61 importer;
- exact measured compatibility upgrade;
- artifact mismatch fallback;
- broken canonical reference rejection.

## Verification frontier

This run closes the previous split verification state.

Before this run:

```text
I01–I10 full Python
I11–I16 exact-main contract verification
```

After run #48:

```text
I01–I16
→ full GitHub Actions Python verification
→ SELFTEST: PASS
```

## Scope

The workflow checks repository code/catalog behavior.

It does not prove:
- external marketplace source truth;
- real GPU benchmark performance;
- purchase suitability;
- real transaction amounts.

Production benchmark observations remain empty until a real Experiment 61 Evidence Packet is admitted.
