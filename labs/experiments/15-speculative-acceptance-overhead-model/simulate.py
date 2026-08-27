#!/usr/bin/env python3

import argparse


DEFAULT_PS = [0.30, 0.60, 0.90]
DEFAULT_DRAFT_LENGTHS = [1, 2, 4, 8]


def expected_accepted(p, draft_len):
    return sum(p ** k for k in range(1, draft_len + 1))


def expected_progress(p, draft_len):
    return 1.0 + expected_accepted(p, draft_len)


def spec_round_cost(
    draft_len,
    draft_cost,
    verify_base,
    verify_per_draft,
):
    return (
        draft_len * draft_cost
        + verify_base
        + draft_len * verify_per_draft
    )


def speedup(
    p,
    draft_len,
    draft_cost,
    verify_base,
    verify_per_draft,
):
    progress = expected_progress(p, draft_len)
    cost = spec_round_cost(
        draft_len,
        draft_cost,
        verify_base,
        verify_per_draft,
    )
    return progress / cost


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Synthetic speculative-decoding acceptance/overhead model."
        )
    )
    parser.add_argument("--draft-cost", type=float, default=0.08)
    parser.add_argument("--verify-base", type=float, default=1.08)
    parser.add_argument(
        "--verify-per-draft",
        type=float,
        default=0.04,
    )
    args = parser.parse_args()

    print(
        "Synthetic cost model; baseline target serial step = 1.0. "
        "Not a real runtime predictor."
    )
    print(
        f"draft_cost/token={args.draft_cost:.3f}, "
        f"verify_cost={args.verify_base:.3f} + "
        f"{args.verify_per_draft:.3f}*D"
    )
    print()

    print(
        f"{'accept':>8} "
        f"{'D':>4} "
        f"{'E accepted':>12} "
        f"{'E progress':>12} "
        f"{'round cost':>11} "
        f"{'speedup':>9}"
    )
    print("-" * 64)

    for p in DEFAULT_PS:
        for draft_len in DEFAULT_DRAFT_LENGTHS:
            accepted = expected_accepted(p, draft_len)
            progress = expected_progress(p, draft_len)
            cost = spec_round_cost(
                draft_len,
                args.draft_cost,
                args.verify_base,
                args.verify_per_draft,
            )
            ratio = progress / cost

            print(
                f"{p * 100:>7.0f}% "
                f"{draft_len:>4} "
                f"{accepted:>12.4f} "
                f"{progress:>12.4f} "
                f"{cost:>11.4f} "
                f"{ratio:>8.3f}x"
            )

        print()


if __name__ == "__main__":
    main()
