# Spec 0011 — Intelligence Freshness / Revalidation Queue

Status: implemented  
Date: 2026-08-28

## Problem

Dynamic intelligence becomes dangerous when dated observations remain queryable but their freshness boundary is invisible.

I10 turns revalidate_after into an operational queue.

## Input

The tool scans all machine-readable catalog files:

~~~text
hardware
models
runtimes
market
compatibility
benchmarks
~~~

Records without revalidate_after remain visible as unscheduled metadata when requested.

## States

~~~text
STALE
DUE-TODAY
DUE-SOON
FRESH
~~~

Definitions are relative to:
- --as-of;
- --within-days.

## Semantics

~~~text
STALE
→ revalidate before a current decision

DUE-SOON
→ queue for refresh

FRESH
→ outside the selected refresh window
~~~

Stale does not automatically mean false.

It means:

> the observation must not be silently treated as current.

## Production example

At:

~~~text
as_of = 2026-08-28
within_days = 1
~~~

the 2026-08-22 RTX 3090 secondary market observation is due soon because its revalidate_after is 2026-08-29.

At:

~~~text
as_of = 2026-09-29
~~~

the current runtime, market and four cross-vendor compatibility observations are stale and require revalidation.

## Non-goals

This tool does not:
- fetch fresh sources;
- decide whether an old observation became false;
- auto-update records;
- hide stale data;
- convert freshness into a performance/recommendation score.