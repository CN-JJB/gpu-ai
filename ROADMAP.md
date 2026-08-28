# Roadmap

## Phase 0 — Requirements
Status: frozen v1

## Phase 1 — Learning/Repo Architecture
Status: validated by first real slice

- [x] Mission
- [x] Course map
- [x] Domain glossary
- [x] Agent rules
- [x] Matt Pocock skill registry/workflows
- [x] Learning state/evidence templates
- [x] Research/experiment templates
- [x] Stable vs dynamic data separation

## Phase 2 — First Vertical Slice
Status: validated

- [x] Spec
- [x] Primary-source research
- [x] Stable reference
- [x] HTML lesson + shared assets
- [x] L0 experiment
- [x] Expected result
- [x] Example Experiment Card
- [x] Learning/build record

## Phase 3 — Mainline
Status: v1 stable mainline complete

Slices 01–49 now cover GPU/LLM foundations, serving, four GPU ecosystems, secondhand decision/validation, platform power/thermal/memory/storage, whole-machine feasibility and the graduation Machine Design Capstone.

Next validation step: complete Experiment 93 against a real learner-owned target and feed only demonstrated gaps back into stable lessons.

## Phase 4 — Intelligence Stations
Status: active

Verified foundations:
- [x] I01 canonical Hardware / Model catalog + Market / Benchmark observations
- [x] I01 Experiment 61 → llama-bench benchmark ingester
- [x] I01 Hardware ↔ Model ↔ Benchmark query bridge
- [x] I01 provenance/freshness/synthetic validation
- [x] I02 Runtime entities + compatibility observations
- [x] I02 DOCUMENTED vs MEASURED support preflight
- [x] I03 exact measured compatibility ingestion
- [x] I04 same-artifact/workload comparable benchmark view
- [x] I05 explicit same-cohort price/performance view
- [x] I06 evidence-linked TCO scenario worksheet
- [x] I07 real benchmark Evidence intake gate
- [x] I08 NVIDIA / AMD / Apple / Intel documented compatibility coverage
- [x] I09 cross-vendor compatibility coverage matrix
- [x] I10 freshness / revalidation queue
- [x] I11 explicit real used-GPU MEDIAN_ASK cohort
- [x] I12 market sample/method evidence audit + MEDIAN_ASK validator gate
- [x] I13 sold-marked listing cohort + transaction-certainty guardrail
- [x] I14 explicit cross-market signal comparison
- [x] I15 China SECONDARY_REPORTED watch signals + semantic validator
- [x] I16 stable M0–M3 market evidence selection gate + Experiment 38 bridge
- [x] I17 freshness-aware market/watchlist gate; stale evidence cannot remain BUY-CANDIDATE
- [x] I18 append-only market refresh lineage; superseded observations leave active views
- [x] I01–I18 GitHub Actions Python compile + end-to-end self-test
- [x] I19 append-only market refresh helper + lineage self-test
- [x] I20–I32 real benchmark/model/profile/prompt/quality admission chain
- [x] I33–I42 reproducible performance × quality tradeoff paths + automatic route selection
- [x] I43–I51 explicit decision-readiness evidence contracts without auto-purchase
- [x] I52 real Experiment 61 benchmark/quality session orchestration
- [x] I53 byte-derived real-session materializer / preflight
- [x] I54 raw semantic-source capture with no automatic manifest update

Next:
- [ ] on the actual benchmark machine, bootstrap a clean real workspace, then run I54 → assemble `profile.txt` → human semantic review/fill → I53 → I52 to acquire the first real Experiment 61 Evidence Packet;
- [ ] pass it through I07 intake and derive exact MEASURED_SUPPORTED;
- [ ] add stronger direct-listing / confirmed-transaction evidence without mixing cohorts;
- [ ] refresh observations when I10 marks them due/stale;
- [x] close full Python verification debt via GitHub Actions run #48;
- [x] make watchlist eligibility freshness-aware so stale market evidence cannot remain purchase-eligible;
- [x] refresh A770 with newer source semantics without overwriting history;
- [ ] apply the same append-only refresh discipline to future due/stale observations;
- [ ] recommendation views only after feasibility/support/quality gates and real comparable Evidence.

Dynamic prices, current compatibility, model releases and benchmark observations belong here rather than being written into stable lessons.

## Phase 5 — Challenge Labs
Special hardware, repair, source-level optimization, distributed junkyard cluster, community contribution.
