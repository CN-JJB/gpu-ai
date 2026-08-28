# Intelligence I29 — quality execution intake gate

Date: 2026-08-28

## Goal

Make the I28 execution-evidence chain a mandatory admission condition for real, non-synthetic Experiment 61 intake.

## Admission contract

A real intake now needs the I22–I27 evidence plus:

~~~text
--quality-command-record
--quality-stdout
--quality-stderr
--quality-packet
~~~

The four I29 arguments are verified against the already-required:
- local model artifact;
- I26 quality corpus;
- I27 quality identity manifest.

## Dedicated negative test

The test:
1. creates a complete non-synthetic-style fixture;
2. proves the old I27 evidence set is now blocked without I28 execution evidence;
3. supplies a valid separate quality packet and reaches READY;
4. changes quality argv `-f` to a different same-size corpus;
5. recomputes the quality packet;
6. proves intake is still blocked.

## Synthetic fixture boundary

All values used by the self-test are explicitly synthetic test fixtures.

No PPL or GPU performance number from this test is production evidence.
