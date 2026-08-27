#!/usr/bin/env python3

import argparse
import json
import time
import urllib.error
import urllib.request


METRICS = {
    "predicted_tokens": "llamacpp:tokens_predicted_total",
    "predicted_seconds": "llamacpp:tokens_predicted_seconds_total",
    "decode_calls": "llamacpp:n_decode_total",
    "draft_tokens": "llamacpp:spec_decode_num_draft_tokens_total",
    "accepted_tokens": "llamacpp:spec_decode_num_accepted_tokens_total",
    "drafts": "llamacpp:spec_decode_num_drafts_total",
}


def parse_prometheus(text):
    result = {}

    for raw in text.splitlines():
        line = raw.strip()

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

        if "{" not in parts[0]:
            result[name] = value

    return result


def get_text(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def get_metrics(base_url, timeout):
    return parse_prometheus(
        get_text(base_url.rstrip("/") + "/metrics", timeout)
    )


def value(metrics, key):
    return metrics.get(METRICS[key])


def delta(before, after, key):
    a = value(before, key)
    b = value(after, key)

    if a is None or b is None:
        return None

    return b - a


def run_request(args, prompt):
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "stream": False,
    }

    if args.model:
        payload["model"] = args.model

    if args.seed is not None:
        payload["seed"] = args.seed

    request = urllib.request.Request(
        args.url.rstrip("/") + "/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    started = time.perf_counter()

    try:
        with urllib.request.urlopen(
            request,
            timeout=args.timeout,
        ) as response:
            obj = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {exc.code}: {body[:500]}"
        ) from exc

    wall_s = time.perf_counter() - started

    return {
        "wall_s": wall_s,
        "usage": obj.get("usage"),
        "timings": obj.get("timings"),
        "finish_reason": (
            obj.get("choices", [{}])[0].get("finish_reason")
            if isinstance(obj.get("choices"), list)
            and obj.get("choices")
            else None
        ),
    }


def safe_ratio(a, b):
    if a is None or b is None or b == 0:
        return None

    return a / b


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Probe one running llama-server and collect speculative "
            "decoding metric deltas."
        )
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8080",
    )
    parser.add_argument("--model", default=None)
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    with open(args.prompt_file, "r", encoding="utf-8") as handle:
        prompt = handle.read()

    before = get_metrics(args.url, min(args.timeout, 10.0))
    response = run_request(args, prompt)
    after = get_metrics(args.url, min(args.timeout, 10.0))

    d = {
        key: delta(before, after, key)
        for key in METRICS
    }

    acceptance = safe_ratio(
        d["accepted_tokens"],
        d["draft_tokens"],
    )
    accepted_per_draft = safe_ratio(
        d["accepted_tokens"],
        d["drafts"],
    )
    server_tps = safe_ratio(
        d["predicted_tokens"],
        d["predicted_seconds"],
    )
    wall_tps = safe_ratio(
        d["predicted_tokens"],
        response["wall_s"],
    )

    result = {
        "config": {
            "url": args.url,
            "model": args.model,
            "prompt_file": args.prompt_file,
            "prompt_chars": len(prompt),
            "max_tokens": args.max_tokens,
            "temperature": args.temperature,
            "seed": args.seed,
        },
        "response": response,
        "metric_deltas": d,
        "summary": {
            "acceptance_rate": acceptance,
            "accepted_tokens_per_draft_round": accepted_per_draft,
            "server_predicted_tps": server_tps,
            "wall_predicted_tps": wall_tps,
            "decode_calls_per_output_token": safe_ratio(
                d["decode_calls"],
                d["predicted_tokens"],
            ),
        },
        "metrics_before": before,
        "metrics_after": after,
    }

    def fmt(x):
        if x is None:
            return "n/a"
        return f"{x:.4f}"

    print(f"wall latency: {response['wall_s']:.4f} s")
    print(f"predicted tokens: {d['predicted_tokens']}")
    print(f"decode calls: {d['decode_calls']}")
    print(f"draft tokens: {d['draft_tokens']}")
    print(f"accepted tokens: {d['accepted_tokens']}")
    print(f"draft rounds: {d['drafts']}")
    print(f"acceptance: {fmt(acceptance)}")
    print(f"accepted/draft-round: {fmt(accepted_per_draft)}")
    print(f"server predicted t/s: {fmt(server_tps)}")
    print(f"wall predicted t/s: {fmt(wall_tps)}")
    print(
        "decode calls/output token: "
        f"{fmt(result['summary']['decode_calls_per_output_token'])}"
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)

        print(f"wrote: {args.output}")


if __name__ == "__main__":
    main()
