#!/usr/bin/env python3

import argparse
import concurrent.futures
import json
import statistics
import threading
import time
import urllib.error
import urllib.request


METRIC_NAMES = {
    "prompt_tokens": "llamacpp:prompt_tokens_total",
    "prompt_seconds": "llamacpp:prompt_seconds_total",
    "predicted_tokens": "llamacpp:tokens_predicted_total",
    "predicted_seconds": "llamacpp:tokens_predicted_seconds_total",
    "processing": "llamacpp:requests_processing",
    "deferred": "llamacpp:requests_deferred",
    "busy_slots_per_decode": "llamacpp:n_busy_slots_per_decode",
}


def percentile(values, q):
    if not values:
        return None

    data = sorted(values)

    if len(data) == 1:
        return data[0]

    pos = (len(data) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(data) - 1)
    frac = pos - lo

    return data[lo] * (1.0 - frac) + data[hi] * frac


def parse_prometheus(text):
    metrics = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split()

        if len(parts) < 2:
            continue

        name = parts[0].split("{", 1)[0]

        try:
            value = float(parts[-1])
        except ValueError:
            continue

        metrics[name] = value

    return metrics


def get_text(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_metrics(base_url, timeout):
    text = get_text(base_url.rstrip("/") + "/metrics", timeout)
    return parse_prometheus(text)


def metric_value(metrics, key):
    return metrics.get(METRIC_NAMES[key])


def metric_delta(before, after, key):
    a = metric_value(before, key)
    b = metric_value(after, key)

    if a is None or b is None:
        return None

    return b - a


def useful_delta(delta):
    if not isinstance(delta, dict):
        return ""

    parts = []

    for key in ("content", "reasoning_content"):
        value = delta.get(key)

        if isinstance(value, str) and value:
            parts.append(value)

    return "".join(parts)


def run_request(index, args, start_event):
    payload = {
        "messages": [
            {
                "role": "user",
                "content": args.prompt,
            }
        ],
        "max_tokens": args.max_tokens,
        "temperature": 0,
        "stream": True,
    }

    if args.model:
        payload["model"] = args.model

    if args.seed is not None:
        payload["seed"] = args.seed

    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        args.url.rstrip("/") + "/v1/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        method="POST",
    )

    start_event.wait()
    started = time.perf_counter()

    event_times = []
    usage = None
    timings = None
    error = None
    status = None

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            status = getattr(response, "status", 200)

            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()

                if not line.startswith("data:"):
                    continue

                data = line[5:].strip()

                if not data or data == "[DONE]":
                    continue

                try:
                    obj = json.loads(data)
                except json.JSONDecodeError:
                    continue

                if isinstance(obj.get("usage"), dict):
                    usage = obj["usage"]

                if isinstance(obj.get("timings"), dict):
                    timings = obj["timings"]

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
        error = f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')[:500]}"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"

    finished = time.perf_counter()

    ttft = None

    if event_times:
        ttft = event_times[0] - started

    gaps = [
        event_times[i] - event_times[i - 1]
        for i in range(1, len(event_times))
    ]

    return {
        "request_index": index,
        "ok": error is None,
        "http_status": status,
        "ttft_s": ttft,
        "latency_s": finished - started,
        "stream_events": len(event_times),
        "mean_stream_gap_s": statistics.mean(gaps) if gaps else None,
        "usage": usage,
        "timings": timings,
        "error": error,
    }


def monitor_metrics(base_url, timeout, interval, stop_event, samples, errors):
    while not stop_event.is_set():
        try:
            metrics = fetch_metrics(base_url, timeout)
            samples.append(
                {
                    "t": time.time(),
                    "processing": metric_value(metrics, "processing"),
                    "deferred": metric_value(metrics, "deferred"),
                    "busy_slots_per_decode": metric_value(
                        metrics, "busy_slots_per_decode"
                    ),
                }
            )
        except Exception as exc:
            if not errors:
                errors.append(f"{type(exc).__name__}: {exc}")

        stop_event.wait(interval)


def max_present(samples, key):
    values = [
        sample[key]
        for sample in samples
        if sample.get(key) is not None
    ]

    return max(values) if values else None


def make_summary(args, results, wall_s, before, after, monitor_samples):
    successful = [result for result in results if result["ok"]]
    ttfts = [
        result["ttft_s"]
        for result in successful
        if result["ttft_s"] is not None
    ]
    latencies = [result["latency_s"] for result in successful]
    stream_gaps = [
        result["mean_stream_gap_s"]
        for result in successful
        if result["mean_stream_gap_s"] is not None
    ]

    pred_tokens = metric_delta(before, after, "predicted_tokens")
    pred_seconds = metric_delta(before, after, "predicted_seconds")
    prompt_tokens = metric_delta(before, after, "prompt_tokens")
    prompt_seconds = metric_delta(before, after, "prompt_seconds")

    return {
        "requests_total": len(results),
        "requests_ok": len(successful),
        "experiment_wall_s": wall_s,
        "request_throughput_rps": (
            len(successful) / wall_s if wall_s > 0 else None
        ),
        "ttft_mean_s": statistics.mean(ttfts) if ttfts else None,
        "ttft_p50_s": percentile(ttfts, 0.50),
        "ttft_p95_s": percentile(ttfts, 0.95),
        "ttft_max_s": max(ttfts) if ttfts else None,
        "latency_mean_s": statistics.mean(latencies) if latencies else None,
        "latency_p95_s": percentile(latencies, 0.95),
        "latency_max_s": max(latencies) if latencies else None,
        "mean_stream_gap_s": (
            statistics.mean(stream_gaps) if stream_gaps else None
        ),
        "server_prompt_tokens_delta": prompt_tokens,
        "server_predicted_tokens_delta": pred_tokens,
        "server_prompt_tps_from_deltas": (
            prompt_tokens / prompt_seconds
            if prompt_tokens is not None
            and prompt_seconds is not None
            and prompt_seconds > 0
            else None
        ),
        "server_predicted_tps_from_deltas": (
            pred_tokens / pred_seconds
            if pred_tokens is not None
            and pred_seconds is not None
            and pred_seconds > 0
            else None
        ),
        "wall_aggregate_predicted_tps": (
            pred_tokens / wall_s
            if pred_tokens is not None and wall_s > 0
            else None
        ),
        "peak_requests_processing": max_present(
            monitor_samples, "processing"
        ),
        "peak_requests_deferred": max_present(
            monitor_samples, "deferred"
        ),
        "max_observed_busy_slots_per_decode": max_present(
            monitor_samples, "busy_slots_per_decode"
        ),
        "busy_slots_per_decode_after": metric_value(
            after, "busy_slots_per_decode"
        ),
        "concurrency": args.concurrency,
        "max_tokens": args.max_tokens,
    }


def fmt(value, digits=3):
    if value is None:
        return "n/a"

    if isinstance(value, (int, str)):
        return str(value)

    return f"{value:.{digits}f}"


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Small llama-server concurrency probe. "
            "Measures client-visible streaming latency plus server /metrics."
        )
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8080",
        help="llama-server base URL",
    )
    parser.add_argument("--model", default=None)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--requests", type=int, default=8)
    parser.add_argument("--max-tokens", type=int, default=64)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument(
        "--prompt",
        default=(
            "Explain in concise plain language why GPU memory capacity "
            "and memory bandwidth are different. Use several short sentences."
        ),
    )
    parser.add_argument("--timeout", type=float, default=300.0)
    parser.add_argument("--monitor-interval", type=float, default=0.05)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.concurrency < 1:
        raise SystemExit("--concurrency must be >= 1")

    if args.requests < 1:
        raise SystemExit("--requests must be >= 1")

    if args.max_tokens < 1:
        raise SystemExit("--max-tokens must be >= 1")

    base_url = args.url.rstrip("/")

    try:
        metrics_before = fetch_metrics(base_url, min(args.timeout, 10.0))
    except Exception as exc:
        raise SystemExit(
            "Cannot read /metrics. Start llama-server with --metrics. "
            f"Error: {type(exc).__name__}: {exc}"
        )

    start_event = threading.Event()
    stop_monitor = threading.Event()
    monitor_samples = []
    monitor_errors = []

    monitor = threading.Thread(
        target=monitor_metrics,
        args=(
            base_url,
            min(args.timeout, 10.0),
            args.monitor_interval,
            stop_monitor,
            monitor_samples,
            monitor_errors,
        ),
        daemon=True,
    )
    monitor.start()

    results = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.concurrency
    ) as executor:
        futures = [
            executor.submit(run_request, i, args, start_event)
            for i in range(args.requests)
        ]

        wall_start = time.perf_counter()
        start_event.set()

        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

        wall_s = time.perf_counter() - wall_start

    stop_monitor.set()
    monitor.join(timeout=2.0)

    try:
        metrics_after = fetch_metrics(base_url, min(args.timeout, 10.0))
    except Exception as exc:
        raise SystemExit(
            f"Requests completed but final /metrics failed: "
            f"{type(exc).__name__}: {exc}"
        )

    results.sort(key=lambda item: item["request_index"])

    summary = make_summary(
        args,
        results,
        wall_s,
        metrics_before,
        metrics_after,
        monitor_samples,
    )

    output = {
        "config": {
            "url": base_url,
            "model": args.model,
            "concurrency": args.concurrency,
            "requests": args.requests,
            "max_tokens": args.max_tokens,
            "seed": args.seed,
            "prompt": args.prompt,
            "monitor_interval_s": args.monitor_interval,
        },
        "summary": summary,
        "requests": results,
        "metrics_before": metrics_before,
        "metrics_after": metrics_after,
        "monitor_samples": monitor_samples,
        "monitor_errors": monitor_errors,
    }

    print(
        f"requests: {summary['requests_ok']}/{summary['requests_total']} ok"
    )
    print(f"wall: {fmt(summary['experiment_wall_s'])} s")
    print(f"request throughput: {fmt(summary['request_throughput_rps'])} req/s")
    print(
        "TTFT mean/p50/p95/max: "
        f"{fmt(summary['ttft_mean_s'])} / "
        f"{fmt(summary['ttft_p50_s'])} / "
        f"{fmt(summary['ttft_p95_s'])} / "
        f"{fmt(summary['ttft_max_s'])} s"
    )
    print(
        "E2E mean/p95/max: "
        f"{fmt(summary['latency_mean_s'])} / "
        f"{fmt(summary['latency_p95_s'])} / "
        f"{fmt(summary['latency_max_s'])} s"
    )
    print(
        "mean stream-gap proxy: "
        f"{fmt(summary['mean_stream_gap_s'])} s"
    )
    print(
        "server prompt t/s: "
        f"{fmt(summary['server_prompt_tps_from_deltas'])}"
    )
    print(
        "server predicted t/s: "
        f"{fmt(summary['server_predicted_tps_from_deltas'])}"
    )
    print(
        "wall aggregate predicted t/s: "
        f"{fmt(summary['wall_aggregate_predicted_tps'])}"
    )
    print(
        "peak processing / deferred: "
        f"{fmt(summary['peak_requests_processing'])} / "
        f"{fmt(summary['peak_requests_deferred'])}"
    )
    print(
        "busy slots/decode after run: "
        f"{fmt(summary['busy_slots_per_decode_after'])}"
    )

    failed = [result for result in results if not result["ok"]]

    if failed:
        print()
        print("Failures:")
        for result in failed:
            print(
                f"  request {result['request_index']}: "
                f"{result['error']}"
            )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(output, handle, ensure_ascii=False, indent=2)

        print(f"wrote: {args.output}")


if __name__ == "__main__":
    main()
