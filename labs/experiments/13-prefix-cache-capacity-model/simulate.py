#!/usr/bin/env python3

from collections import OrderedDict

REQUESTS = ["A", "B", "A", "C", "A", "B"]
PREFIX_TOKENS = 1024
UNIQUE_SUFFIX_TOKENS = 64
DECODE_TOKENS_PER_REQUEST = 128
CAPACITIES = [0, 1, 2, 3]


def simulate(capacity):
    cache = OrderedDict()
    hits = 0
    evictions = 0
    prompt_processed = 0
    reused_tokens = 0
    trace = []

    for index, prefix_id in enumerate(REQUESTS, start=1):
        hit = capacity > 0 and prefix_id in cache
        evicted = None

        if hit:
            hits += 1
            reused_tokens += PREFIX_TOKENS
            prompt_processed += UNIQUE_SUFFIX_TOKENS
            cache.move_to_end(prefix_id)
        else:
            prompt_processed += PREFIX_TOKENS + UNIQUE_SUFFIX_TOKENS

            if capacity > 0:
                if len(cache) >= capacity:
                    evicted, _ = cache.popitem(last=False)
                    evictions += 1

                cache[prefix_id] = True

        trace.append(
            {
                "request": index,
                "prefix": prefix_id,
                "hit": hit,
                "evicted": evicted,
                "cache": list(cache.keys()),
            }
        )

    baseline_prompt = len(REQUESTS) * (
        PREFIX_TOKENS + UNIQUE_SUFFIX_TOKENS
    )
    decode_total = len(REQUESTS) * DECODE_TOKENS_PER_REQUEST

    return {
        "capacity": capacity,
        "hits": hits,
        "hit_rate": hits / len(REQUESTS),
        "evictions": evictions,
        "prompt_processed": prompt_processed,
        "reused_tokens": reused_tokens,
        "prompt_saved": baseline_prompt - prompt_processed,
        "decode_total": decode_total,
        "trace": trace,
    }


def main():
    print(
        "Synthetic prefix-cache model; capacity is whole-prefix entries, "
        "not real KV blocks."
    )
    print(
        f"requests={','.join(REQUESTS)}, "
        f"prefix={PREFIX_TOKENS}, suffix={UNIQUE_SUFFIX_TOKENS}, "
        f"decode/request={DECODE_TOKENS_PER_REQUEST}"
    )
    print()

    print(
        f"{'capacity':>8} "
        f"{'hits':>6} "
        f"{'hit rate':>10} "
        f"{'evict':>7} "
        f"{'prompt proc':>12} "
        f"{'reused':>10} "
        f"{'saved':>10} "
        f"{'decode':>8}"
    )
    print("-" * 84)

    results = []

    for capacity in CAPACITIES:
        result = simulate(capacity)
        results.append(result)

        print(
            f"{capacity:>8} "
            f"{result['hits']:>6} "
            f"{result['hit_rate'] * 100:>9.1f}% "
            f"{result['evictions']:>7} "
            f"{result['prompt_processed']:>12} "
            f"{result['reused_tokens']:>10} "
            f"{result['prompt_saved']:>10} "
            f"{result['decode_total']:>8}"
        )

    print()
    print("capacity=2 trace")

    result = next(item for item in results if item["capacity"] == 2)

    for item in result["trace"]:
        status = "HIT" if item["hit"] else "MISS"
        evicted = item["evicted"] if item["evicted"] is not None else "-"
        cache = ",".join(item["cache"]) or "-"

        print(
            f"  req {item['request']}: prefix={item['prefix']} "
            f"{status:>4} evict={evicted} cache=[{cache}]"
        )


if __name__ == "__main__":
    main()
