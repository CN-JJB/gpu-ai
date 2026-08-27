#!/usr/bin/env python3

import argparse
from dataclasses import dataclass

GIB = 1024 ** 3
KIB = 1024


@dataclass
class Budget:
    weight_gib: float
    attention_type: str
    kv_bytes_per_token: int
    kv_gib_per_sequence: float
    kv_total_gib: float
    reserve_gib: float
    total_gib: float
    headroom_gib: float | None
    headroom_percent: float | None
    status: str


def attention_type(attention_heads: int, kv_heads: int) -> str:
    if kv_heads == attention_heads:
        return "MHA"
    if kv_heads == 1:
        return "MQA"
    return "GQA"


def calculate(
    params_b: float,
    weight_bpw: float,
    layers: int,
    attention_heads: int,
    kv_heads: int,
    head_dim: int,
    kv_bits: int,
    context: int,
    concurrency: int,
    reserve_gib: float,
    vram_gib: float | None,
) -> Budget:
    if min(params_b, weight_bpw, layers, attention_heads, kv_heads,
           head_dim, kv_bits, context, concurrency) <= 0:
        raise ValueError("All model/cache dimensions must be positive.")

    if kv_heads > attention_heads:
        raise ValueError("kv_heads cannot exceed attention_heads in this baseline.")

    weight_bytes = params_b * 1e9 * weight_bpw / 8.0
    weight_gib = weight_bytes / GIB

    kv_bytes_per_element = kv_bits / 8.0
    kv_bytes_per_token_float = (
        2
        * layers
        * kv_heads
        * head_dim
        * kv_bytes_per_element
    )

    if not kv_bytes_per_token_float.is_integer():
        raise ValueError(
            "This simple calculator expects KV bits to produce whole bytes."
        )

    kv_bytes_per_token = int(kv_bytes_per_token_float)
    kv_gib_per_sequence = kv_bytes_per_token * context / GIB
    kv_total_gib = kv_gib_per_sequence * concurrency
    total_gib = weight_gib + kv_total_gib + reserve_gib

    headroom_gib = None
    headroom_percent = None
    status = "NO_VRAM_TARGET"

    if vram_gib is not None:
        headroom_gib = vram_gib - total_gib
        headroom_percent = 100.0 * headroom_gib / vram_gib

        if headroom_gib < 0:
            status = "OVER"
        elif headroom_percent < 10.0:
            status = "TIGHT"
        else:
            status = "ROOMY"

    return Budget(
        weight_gib=weight_gib,
        attention_type=attention_type(attention_heads, kv_heads),
        kv_bytes_per_token=kv_bytes_per_token,
        kv_gib_per_sequence=kv_gib_per_sequence,
        kv_total_gib=kv_total_gib,
        reserve_gib=reserve_gib,
        total_gib=total_gib,
        headroom_gib=headroom_gib,
        headroom_percent=headroom_percent,
        status=status,
    )


def print_budget(budget: Budget, context: int, concurrency: int):
    print(f"attention type: {budget.attention_type}")
    print(f"weight baseline: {budget.weight_gib:.3f} GiB")
    print(
        f"KV per token / sequence: "
        f"{budget.kv_bytes_per_token:,} bytes "
        f"({budget.kv_bytes_per_token / KIB:.1f} KiB)"
    )
    print(
        f"KV per sequence @ {context:,} tokens: "
        f"{budget.kv_gib_per_sequence:.3f} GiB"
    )
    print(
        f"KV total @ concurrency {concurrency}: "
        f"{budget.kv_total_gib:.3f} GiB"
    )
    print(f"runtime reserve: {budget.reserve_gib:.3f} GiB")
    print(f"preflight total: {budget.total_gib:.3f} GiB")

    if budget.headroom_gib is not None:
        print(
            f"headroom: {budget.headroom_gib:.3f} GiB "
            f"({budget.headroom_percent:.1f}%)"
        )

    print(f"status: {budget.status}")


def run_demo():
    print("Abstract 7B-like GQA demo; not a real checkpoint/runtime guarantee.")
    print(
        "7B params, 4.5 effective bpw, 32 layers, 32 Q heads, "
        "8 KV heads, head_dim=128, FP16 KV, context=4096, "
        "reserve=1.5 GiB, VRAM=8 GiB"
    )
    print()

    print(
        f"{'conc':>5} "
        f"{'weights':>10} "
        f"{'KV':>10} "
        f"{'reserve':>10} "
        f"{'total':>10} "
        f"{'headroom':>10} "
        f"{'status':>8}"
    )
    print("-" * 72)

    for concurrency in [1, 2, 4, 8]:
        b = calculate(
            params_b=7,
            weight_bpw=4.5,
            layers=32,
            attention_heads=32,
            kv_heads=8,
            head_dim=128,
            kv_bits=16,
            context=4096,
            concurrency=concurrency,
            reserve_gib=1.5,
            vram_gib=8,
        )

        print(
            f"{concurrency:>5} "
            f"{b.weight_gib:>9.3f}G "
            f"{b.kv_total_gib:>9.3f}G "
            f"{b.reserve_gib:>9.3f}G "
            f"{b.total_gib:>9.3f}G "
            f"{b.headroom_gib:>9.3f}G "
            f"{b.status:>8}"
        )

    print()
    print("KV architecture comparison @ 4096 tokens, FP16, 32 layers:")
    print(f"{'type':>6} {'kv heads':>9} {'KiB/token':>12} {'GiB/seq':>10}")
    print("-" * 44)

    for kv_heads in [32, 8, 1]:
        b = calculate(
            params_b=7,
            weight_bpw=4.5,
            layers=32,
            attention_heads=32,
            kv_heads=kv_heads,
            head_dim=128,
            kv_bits=16,
            context=4096,
            concurrency=1,
            reserve_gib=0,
            vram_gib=None,
        )
        print(
            f"{b.attention_type:>6} "
            f"{kv_heads:>9} "
            f"{b.kv_bytes_per_token / KIB:>12.1f} "
            f"{b.kv_gib_per_sequence:>10.4f}"
        )


def parse_args():
    p = argparse.ArgumentParser(
        description="Baseline local-LLM VRAM budget calculator."
    )
    p.add_argument("--demo", action="store_true")
    p.add_argument("--params-b", type=float)
    p.add_argument("--weight-bpw", type=float)
    p.add_argument("--layers", type=int)
    p.add_argument("--attention-heads", type=int)
    p.add_argument("--kv-heads", type=int)
    p.add_argument("--head-dim", type=int)
    p.add_argument("--kv-bits", type=int, default=16)
    p.add_argument("--context", type=int)
    p.add_argument("--concurrency", type=int, default=1)
    p.add_argument("--reserve-gib", type=float, default=1.0)
    p.add_argument("--vram-gib", type=float)
    return p.parse_args()


def main():
    args = parse_args()

    if args.demo:
        run_demo()
        return

    required = {
        "--params-b": args.params_b,
        "--weight-bpw": args.weight_bpw,
        "--layers": args.layers,
        "--attention-heads": args.attention_heads,
        "--kv-heads": args.kv_heads,
        "--head-dim": args.head_dim,
        "--context": args.context,
    }

    missing = [name for name, value in required.items() if value is None]

    if missing:
        raise SystemExit("Missing required arguments: " + ", ".join(missing))

    budget = calculate(
        params_b=args.params_b,
        weight_bpw=args.weight_bpw,
        layers=args.layers,
        attention_heads=args.attention_heads,
        kv_heads=args.kv_heads,
        head_dim=args.head_dim,
        kv_bits=args.kv_bits,
        context=args.context,
        concurrency=args.concurrency,
        reserve_gib=args.reserve_gib,
        vram_gib=args.vram_gib,
    )

    print_budget(budget, args.context, args.concurrency)


if __name__ == "__main__":
    main()
