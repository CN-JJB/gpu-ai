#!/usr/bin/env python3

RESIDENT_GROUPS = [1, 2, 4, 8, 16, 32]
ROUNDS = 20
COMPUTE_INSTRUCTIONS = 4
MEMORY_WAIT_CYCLES = 20


def simulate(group_count: int):
    step_in_round = [0] * group_count
    rounds_done = [0] * group_count
    ready_at = [0] * group_count

    cycle = 0
    issued = 0
    next_group = 0

    while any(done < ROUNDS for done in rounds_done):
        chosen = None

        for offset in range(group_count):
            group = (next_group + offset) % group_count
            if rounds_done[group] < ROUNDS and ready_at[group] <= cycle:
                chosen = group
                break

        if chosen is None:
            cycle += 1
            continue

        group = chosen
        issued += 1

        if step_in_round[group] < COMPUTE_INSTRUCTIONS:
            step_in_round[group] += 1
        else:
            step_in_round[group] = 0
            rounds_done[group] += 1

            if rounds_done[group] < ROUNDS:
                ready_at[group] = cycle + MEMORY_WAIT_CYCLES + 1

        next_group = (group + 1) % group_count
        cycle += 1

    return {
        "cycles": cycle,
        "issued": issued,
        "issue_utilization": issued / cycle,
        "idle_cycles": cycle - issued,
    }


def main():
    print("Concept model: one scheduler, one issue slot per cycle")
    print(
        f"Each group: {COMPUTE_INSTRUCTIONS} compute instructions + "
        f"1 memory instruction, then wait {MEMORY_WAIT_CYCLES} cycles"
    )
    print(f"Rounds per group: {ROUNDS}\n")

    print(
        f"{'resident groups':>15} "
        f"{'cycles':>10} "
        f"{'issued':>10} "
        f"{'idle':>10} "
        f"{'issue util':>12}"
    )
    print("-" * 63)

    for groups in RESIDENT_GROUPS:
        result = simulate(groups)
        print(
            f"{groups:>15} "
            f"{result['cycles']:>10} "
            f"{result['issued']:>10} "
            f"{result['idle_cycles']:>10} "
            f"{result['issue_utilization']:>11.1%}"
        )


if __name__ == "__main__":
    main()
