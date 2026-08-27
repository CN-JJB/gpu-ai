# Evidence — Intelligence I10: Freshness / Revalidation Queue

Date: 2026-08-28  
Status: verified

## Claim

Dynamic intelligence must surface its refresh boundary instead of silently aging into timeless truth.

## Tool

~~~bash
python3 tools/intelligence/freshness_report.py intelligence/catalog \
  --as-of YYYY-MM-DD \
  --within-days N
~~~

## States

~~~text
STALE
DUE-TODAY
DUE-SOON
FRESH
~~~

Records without revalidate_after can be shown separately with --show-unscheduled.

## Verified current-window case

At as_of=2026-08-28 and within_days=1:

~~~text
STALE=0
DUE-SOON=1
FRESHNESS: REVALIDATION-QUEUE-PRESENT
~~~

The due-soon record is:

~~~text
market:cn:rtx3090:secondary:2026-08-22
revalidate_after=2026-08-29
~~~

## Verified future-stale case

At as_of=2026-09-29 and within_days=30:

~~~text
STALE=6
FRESHNESS: STALE-REVALIDATION-REQUIRED
~~~

The stale set consists of the current runtime, market observation and four documented compatibility observations whose revalidation dates have passed.

## Execution verification

The local verification tree used exact main-branch blobs:

~~~text
freshness_report.py
c13326fb6348ec4fc1009dfda2db8cd23a7487ff

selftest.py
c9aaa99a9ba245fd38699466cf3bd65879cd0a8d
~~~

Executed:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

Result:

~~~text
SELFTEST: PASS
~~~

## Important boundary

~~~text
STALE != FALSE
~~~

STALE means the observation must be revalidated before being used as current decision evidence.

The tool does not automatically fetch, overwrite or hide stale data.
