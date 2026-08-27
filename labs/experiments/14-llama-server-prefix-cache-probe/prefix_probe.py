#!/usr/bin/env python3

import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
import uuid


def make_prompt(tag, repeat):
    sentence = (
        "GPU memory capacity tells us how much state can stay resident, "
        "while memory bandwidth tells us how quickly bytes can move. "
        "These are different hardware constraints. "
    )

    body = sentence * repeat

    return (
        f"Cache probe key: {tag}. "
        f"{body}"
        "Question: summarize the main distinction in one concise sentence."
    )


def request_json(base_url, model, prompt, max_tokens, seed, timeout):
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0,
        "stream": False,
    }

    if model:
        payload["model"] = model

    if seed is not None:
        payload["seed"] = seed

    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        base_url.rstrip("/") + "/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    started = time.perf_counter()

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            latency = time.perf_counter() - started
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {text[:500]}") from exc

    timings = data.get("timings") or {}
    usage = data.get("usage") or {}

    return {
        "latency_s": latency,
        "cache_n": timings.get("cache_n"),
        "prompt_n": timings.get("prompt_n"),
        "prompt_ms": timings.get("prompt_ms"),
        "prompt_per_second": timings.get("prompt_per_second"),
        "predicted_n": timings.get("predicted_n"),
        "predicted_ms": timings.get("predicted_ms"),
        "predicted_per_second": timings.get("predicted_per_second"),
        "usage": usage,
        "timings": timings,
    }


def useful_delta(delta):
    if not isinstance(delta, dict):
        return ""

    parts = []

    for key in ("content", "reasoning_content"):
        value = delta.get(key)

        if isinstance(value, str) and value:
            parts.append(value)

    return "".join(parts)


def request_stream(base_url, model, prompt, max_tokens, seed, timeout):
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0,
        "stream": True,
    }

    if model:
        payload["model"] = model

    if seed is not None:
        payload["seed"] = seed

    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        base_url.rstrip("/") + "/v1/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        method="POST",
    )

    started = time.perf_counter()
    event_times = []
    final_timings = None
    final_usage = None

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            for raw_line in response:
                line = raw_line.decode(
                    "utf-8", errors="replace"
                ).strip()

                if not line.startswith("data:"):
                    continue

                raw = line[5:].strip()

                if not raw or raw == "[DONE]":
                    continue

                try:
                    obj = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                if isinstance(obj.get("timings"), dict):
                    final_timings = obj["timings"]

                if isinstance(obj.get("usage"), dict):
                    final_usage = obj["usage"]

                choices = obj.get("choices")

                if not isinstance(choices, list) or not choices:
                    continue

                choice = choices[0]

                if not isinstance(choice, dict):
                    continue

                delta = choice.get("delta")

                if isinstance(delta, dict) and useful_delta(delta):
                    event_times.append(time.perf_counter())

    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {text[:500]}") from exc

    finished = time.perf_counter()

    gaps = [
        event_times[i] - event_times[i - 1]
        for i in range(1, len(event_times))
    ]

    return {
        "ttft_s": event_times[0] - started if event_times else None,
        "latency_s": finished - started,
        "stream_events": len(event_times),
        "mean_stream_gap_s": statistics.mean(gaps) if gaps else None,
        "timings_if_present": final_timings,
        "usage_if_present": final_usage,
    }


def ratio(warm, cold):
    if warm is None or cold is None or cold == 0:
        return None
    return warm / cold


def fmt(value):
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return str(value)
    return f"{value:.4f}"


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Probe llama-server prompt/prefix cache using cold/warm "
            "exact-repeat requests."
        )
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8080",
    )
    parser.add_argument("--model", default=None)
    parser.add_argument("--prefix-repeat", type=int, default=64)
    parser.add_argument("--max-tokens", type=int, default=16)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--timeout", type=float, default=300.0)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.prefix_repeat < 1:
        raise SystemExit("--prefix-repeat must be >= 1")

    if args.max_tokens < 1:
        raise SystemExit("--max-tokens must be >= 1")

    run_id = args.run_id or uuid.uuid4().hex[:12]

    timing_tag = f"{run_id}-timing"
    timing_prompt = make_prompt(timing_tag, args.prefix_repeat)

    cold = request_json(
        args.url,
        args.model,
        timing_prompt,
        args.max_tokens,
        args.seed,
        args.timeout,
    )

    warm = request_json(
        args.url,
        args.model,
        timing_prompt,
        args.max_tokens,
        args.seed,
        args.timeout,
    )

    near_prompt = make_prompt(
        f"{run_id}-near-miss",
        args.prefix_repeat,
    )

    near = request_json(
        args.url,
        args.model,
        near_prompt,
        args.max_tokens,
        args.seed,
        args.timeout,
    )

    stream_tag = f"{run_id}-stream"
    stream_prompt = make_prompt(stream_tag, args.prefix_repeat)

    stream_cold = request_stream(
        args.url,
        args.model,
        stream_prompt,
        args.max_tokens,
        args.seed,
        args.timeout,
    )

    stream_warm = request_stream(
        args.url,
        args.model,
        stream_prompt,
        args.max_tokens,
        args.seed,
        args.timeout,
    )

    summary = {
        "cache_n_delta_warm_minus_cold": (
            warm["cache_n"] - cold["cache_n"]
            if isinstance(warm["cache_n"], (int, float))
            and isinstance(cold["cache_n"], (int, float))
            else None
        ),
        "prompt_n_warm_over_cold": ratio(
            warm["prompt_n"], cold["prompt_n"]
        ),
        "prompt_ms_warm_over_cold": ratio(
            warm["prompt_ms"], cold["prompt_ms"]
        ),
        "predicted_ms_warm_over_cold": ratio(
            warm["predicted_ms"], cold["predicted_ms"]
        ),
        "ttft_warm_over_cold": ratio(
            stream_warm["ttft_s"], stream_cold["ttft_s"]
        ),
    }

    output = {
        "config": {
            "url": args.url,
            "model": args.model,
            "prefix_repeat": args.prefix_repeat,
            "max_tokens": args.max_tokens,
            "seed": args.seed,
            "run_id": run_id,
        },
        "timing_pair": {
            "cold": cold,
            "warm": warm,
            "near_miss": near,
        },
        "stream_ttft_pair": {
            "cold": stream_cold,
            "warm": stream_warm,
        },
        "summary": summary,
    }

    print("timing pair")
    print(
        f"  cold cache_n={fmt(cold['cache_n'])} "
        f"prompt_n={fmt(cold['prompt_n'])} "
        f"prompt_ms={fmt(cold['prompt_ms'])} "
        f"predicted_ms={fmt(cold['predicted_ms'])}"
    )
    print(
        f"  warm cache_n={fmt(warm['cache_n'])} "
        f"prompt_n={fmt(warm['prompt_n'])} "
        f"prompt_ms={fmt(warm['prompt_ms'])} "
        f"predicted_ms={fmt(warm['predicted_ms'])}"
    )
    print(
        f"  near cache_n={fmt(near['cache_n'])} "
        f"prompt_n={fmt(near['prompt_n'])} "
        f"prompt_ms={fmt(near['prompt_ms'])}"
    )
    print()
    print("stream TTFT pair")
    print(
        f"  cold TTFT={fmt(stream_cold['ttft_s'])} s "
        f"E2E={fmt(stream_cold['latency_s'])} s"
    )
    print(
        f"  warm TTFT={fmt(stream_warm['ttft_s'])} s "
        f"E2E={fmt(stream_warm['latency_s'])} s"
    )
    print()
    print("ratios warm/cold")
    print(
        f"  prompt_n={fmt(summary['prompt_n_warm_over_cold'])}"
    )
    print(
        f"  prompt_ms={fmt(summary['prompt_ms_warm_over_cold'])}"
    )
    print(
        f"  predicted_ms={fmt(summary['predicted_ms_warm_over_cold'])}"
    )
    print(
        f"  TTFT={fmt(summary['ttft_warm_over_cold'])}"
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(output, handle, ensure_ascii=False, indent=2)

        print(f"wrote: {args.output}")


if __name__ == "__main__":
    main()
