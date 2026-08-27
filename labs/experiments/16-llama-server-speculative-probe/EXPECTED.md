# Expected structural outcomes

There are no fixed performance numbers.

## Baseline server

With speculative decoding disabled, current metrics should show approximately:

~~~text
draft tokens delta = 0
accepted tokens delta = 0
draft rounds delta = 0
~~~

If current metric semantics changed, inspect current docs rather than hard-coding zero.

## Speculative server

If the proposer generates drafts:

~~~text
draft tokens > 0
draft rounds > 0
~~~

Accepted tokens may be anywhere from near zero to a large fraction.

## Useful speculative run

A strong result can show:

~~~text
accepted tokens > 0
decode calls/output token ↓
server predicted t/s ↑
wall latency ↓
~~~

Not every field must improve identically.

## Low acceptance

A valid result is:

~~~text
draft tokens high
accepted tokens low
decode speed <= baseline
~~~

This is not a correctness failure.

It means proposal overhead did not buy enough accepted progress.

## Repetitive vs novel workload

For history/n-gram proposers it is reasonable to expect higher opportunity on repetitive/copy-heavy text.

Do not promise it:
the model still has to generate patterns the proposer can match.

## Two-model draft

A valid regression can occur even with good acceptance if:

- draft model is too slow；
- draft consumes memory；
- target offload changes；
- verifier batch is inefficient on the hardware；
- baseline target was already well batched。

## High concurrency

Speculative speedup may shrink as baseline target batching/utilization improves.

This is an expected systems interaction, not evidence that speculative decoding is fake.

## Correctness

Do not compare stochastic runs byte-for-byte and conclude losslessness failed.

Record exact sampling settings and understand the verifier/rejection-sampling guarantee.
