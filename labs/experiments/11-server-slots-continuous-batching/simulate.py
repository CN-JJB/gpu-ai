#!/usr/bin/env python3

from statistics import mean

REQUESTS = 8
TOKENS_PER_REQUEST = 32
SLOT_SWEEP = [1, 2, 4, 8, 16]
MIXED_LENGTHS = [8, 32, 8, 32, 8, 32]


def step_time(active_requests: int) -> float:
    if active_requests <= 0:
        raise ValueError("active_requests must be positive")
    return 1.0 + 0.22 * (active_requests - 1)


def simulate_continuous(lengths, slots):
    remaining = list(lengths)
    first_token = [None] * len(lengths)
    active = []
    next_index = 0
    now = 0.0

    while next_index < len(remaining) and len(active) < slots:
        active.append(next_index)
        next_index += 1

    while active:
        dt = step_time(len(active))
        now += dt

        finished = []

        for idx in active:
            if first_token[idx] is None:
                first_token[idx] = now

            remaining[idx] -= 1

            if remaining[idx] == 0:
                finished.append(idx)

        active = [idx for idx in active if idx not in finished]

        while next_index < len(remaining) and len(active) < slots:
            active.append(next_index)
            next_index += 1

    return {
        "makespan": now,
        "aggregate_tpu": sum(lengths) / now,
        "avg_first": mean(first_token),
        "max_first": max(first_token),
        "first": first_token,
    }


def simulate_static_groups(lengths, slots):
    remaining = list(lengths)
    first_token = [None] * len(lengths)
    now = 0.0

    for group_start in range(0, len(remaining), slots):
        active = list(
            range(group_start, min(group_start + slots, len(remaining)))
        )

        while active:
            dt = step_time(len(active))
            now += dt
            finished = []

            for idx in active:
                if first_token[idx] is None:
                    first_token[idx] = now

                remaining[idx] -= 1

                if remaining[idx] == 0:
                    finished.append(idx)

            active = [idx for idx in active if idx not in finished]

    return {
        "makespan": now,
        "aggregate_tpu": sum(lengths) / now,
        "avg_first": mean(first_token),
        "max_first": max(first_token),
        "first": first_token,
    }


def part_a():
    print("Part A — 8 equal requests, 32 output tokens each")
    print(
        f"{'slots':>6} "
        f"{'active step':>12} "
        f"{'makespan':>10} "
        f"{'agg tok/u':>10} "
        f"{'avg first':>10} "
        f"{'max first':>10}"
    )
    print("-" * 68)

    lengths = [TOKENS_PER_REQUEST] * REQUESTS

    for slots in SLOT_SWEEP:
        result = simulate_continuous(lengths, slots)
        active = min(slots, REQUESTS)

        print(
            f"{slots:>6} "
            f"{step_time(active):>12.2f} "
            f"{result['makespan']:>10.2f} "
            f"{result['aggregate_tpu']:>10.3f} "
            f"{result['avg_first']:>10.2f} "
            f"{result['max_first']:>10.2f}"
        )


def part_b():
    print()
    print("Part B — mixed lengths, slots=2")
    print("lengths:", ", ".join(str(x) for x in MIXED_LENGTHS))
    print(
        f"{'strategy':>12} "
        f"{'makespan':>10} "
        f"{'agg tok/u':>10} "
        f"{'avg first':>10} "
        f"{'max first':>10}"
    )
    print("-" * 58)

    for name, fn in [
        ("static", simulate_static_groups),
        ("continuous", simulate_continuous),
    ]:
        result = fn(MIXED_LENGTHS, 2)

        print(
            f"{name:>12} "
            f"{result['makespan']:>10.2f} "
            f"{result['aggregate_tpu']:>10.3f} "
            f"{result['avg_first']:>10.2f} "
            f"{result['max_first']:>10.2f}"
        )


def main():
    print(
        "Abstract server model; units are synthetic and do not represent "
        "llama.cpp or any real GPU."
    )
    print()
    part_a()
    part_b()


if __name__ == "__main__":
    main()
