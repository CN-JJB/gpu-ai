# Student Textbook Completion Standard

Status: active authoring contract

## Purpose

The course is not considered student-ready merely because every slice, experiment, and HTML file exists.

The learner will start only after the stable teaching material is authored as a complete self-study textbook. Real learner-owned benchmark results are intentionally deferred until the learner reaches the corresponding experiment; missing real measurements must never block authoring of explanations, procedures, expected observations, troubleshooting, or decision frameworks.

## Required lesson contract

Every stable lesson must let a PC enthusiast with no Linux, Python, CUDA, ML, or math prerequisite answer four questions:

1. What problem is this concept solving?
2. What is the smallest mental model that explains it?
3. What should I observe when I test it?
4. How does this change a local-LLM hardware or software decision?

A student-complete lesson therefore contains all of the following, either directly in the lesson or through an adjacent first-party experiment/reference link:

- **Prerequisite Check** — what the learner must already understand, with a fallback explanation when possible.
- **Real problem** — a concrete local-LLM or GPU decision that creates a reason to learn the concept.
- **Mental model** — plain-language intuition before vendor vocabulary.
- **Mechanism** — enough technical detail to reason about cause and effect rather than memorize terms.
- **Worked example** — numbers, diagrams, command/output anatomy, or a concrete scenario where appropriate.
- **Boundary / misconception correction** — what the model does not prove.
- **Why it matters** — explicit connection to capacity, speed, latency, quality, compatibility, power, cost, reliability, or safety.
- **Experiment path** — a minimum practical exercise plus the evidence the learner should retain.
- **Expected observations** — qualitative or formula-derived expectations that can be authored without fabricating real hardware results.
- **Troubleshooting** — common failure modes and how to distinguish them.
- **No-hardware fallback** — for hardware-dependent lessons, a read-only, trace, worksheet, fixture, or calculation path that preserves the learning objective.
- **Retrieval Practice** — questions that require explanation and transfer, not recognition.
- **Decision rule** — what the learner may and may not conclude after the lesson.
- **Transfer** — how the same reasoning applies to another vendor, model, runtime, or future generation.
- **Primary sources** — stable first-party or primary references for factual claims.

## Experiment contract

An experiment may legitimately have no real result before the learner runs it. It must still be fully teachable.

Each experiment should explain:

- purpose and hypothesis;
- hardware level and safety boundary;
- exact inputs to hold fixed;
- procedure or command shape;
- what to record;
- expected *patterns*, not invented values;
- interpretation branches;
- common invalid comparisons;
- failure recovery;
- no-hardware fallback when the concept can be learned without the target hardware;
- evidence required for completion.

Synthetic fixtures may demonstrate tooling behavior only. They must never be presented as real GPU, model-quality, market, or card-health evidence.

## Depth rule

Byte count is not a quality metric, but very short lessons are a useful audit signal. A short page must not pass merely because it contains the required headings.

Authoring review should prioritize:

1. pages under roughly 8 KiB;
2. architecture/vendor survey pages that currently read like notes rather than explanations;
3. decision and operations pages where missing examples can cause expensive mistakes;
4. capstones that assume knowledge without showing how to integrate it.

## Completion state

The project now distinguishes:

- **STRUCTURALLY COMPLETE** — slice/experiment exists and links are valid;
- **TEXTBOOK COMPLETE** — substantive lesson/experiment contract above is satisfied;
- **LEARNER VERIFIED** — the student later demonstrates mastery with real evidence.

The authoring phase must finish **TEXTBOOK COMPLETE** before the learner begins the course.

Real learner-owned Experiment 61 / Experiment 93 evidence belongs to the later **LEARNER VERIFIED** phase and is not an authoring blocker.
