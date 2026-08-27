# Expected structural outcomes

Experiment 14 has no fixed milliseconds or token/s values.

## Cold exact request

For a unique long prefix, the first request should have relatively little reusable prefix state beyond any common server/chat-template context.

Expected shape:

~~~text
cache_n lower
prompt_n higher
prompt_ms higher
~~~

Exact values depend on current runtime/cache state.

## Warm exact repeat

The second identical request should have a strong opportunity to reuse previously computed prompt KV.

Expected shape:

~~~text
cache_n ↑
prompt_n ↓
prompt_ms ↓
~~~

If this does not happen:

- verify prompt cache is enabled；
- use one slot；
- confirm prompts are byte/token identical；
- increase prefix length；
- inspect current llama.cpp cache behavior；
- make sure server was not restarted between pair requests。

## Predicted/decode timing

Do not require:

~~~text
predicted_ms warm << predicted_ms cold
~~~

Prefix cache does not remove the need to generate new output tokens.

Small differences are normal from runtime variance.

## TTFT pair

Warm exact repeat often has lower TTFT opportunity because less prompt prefill is required.

But TTFT can be dominated by:

- short prefixes；
- HTTP/client overhead；
- CPU scheduling；
- GPU launch overhead；
- cache policy；
- model-specific behavior。

Therefore the lab records actual cold/warm TTFT instead of promising a fixed speedup.

## Near miss

An early changed marker should reduce exact prefix reuse relative to warm exact repeat.

It may still reuse:
- chat template tokens；
- common tokens before the divergence；
- implementation-aligned blocks。

So near-miss cache_n does not need to equal zero.

## Valid unexpected results

- warm cache_n remains small；
- warm prompt_ms does not improve；
- cache disabled still shows small common-prefix reuse evidence；
- TTFT barely changes while prompt_ms drops；
- predicted_ms changes more than expected；
- near miss reuses a large prefix；
- a cache capacity setting evicts the earlier prefix。

All are valuable if runtime/model/config are fully captured.
