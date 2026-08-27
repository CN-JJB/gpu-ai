#!/usr/bin/env python3

N = 1024
BYTES_PER_FLOAT = 4
TILES = [4, 8, 16, 32]


def naive(n: int):
    input_loads = 2 * n**3
    output_stores = n**2
    total_bytes = BYTES_PER_FLOAT * (input_loads + output_stores)
    flops = 2 * n**3
    arithmetic_intensity = flops / total_bytes
    return {
        "input_loads": input_loads,
        "output_stores": output_stores,
        "bytes": total_bytes,
        "ai": arithmetic_intensity,
    }


def tiled(n: int, tile: int):
    if n % tile != 0:
        raise ValueError("This concept model requires N to be divisible by tile.")

    blocks = (n // tile) ** 2
    k_tiles = n // tile

    input_loads = blocks * k_tiles * (2 * tile * tile)
    output_stores = n**2
    total_bytes = BYTES_PER_FLOAT * (input_loads + output_stores)
    flops = 2 * n**3

    return {
        "input_loads": input_loads,
        "output_stores": output_stores,
        "bytes": total_bytes,
        "ai": flops / total_bytes,
        "shared_bytes": 2 * tile * tile * BYTES_PER_FLOAT,
        "threads_per_block": tile * tile,
    }


def main():
    baseline = naive(N)

    print(
        f"N={N}, FP32 concept model; counts algorithmic global element requests "
        "and ignores cache/broadcast effects"
    )
    print(
        f"naive: input-load requests={baseline['input_loads']:,}, "
        f"approx bytes={baseline['bytes'] / 1024**3:.3f} GiB, "
        f"arithmetic intensity={baseline['ai']:.3f} FLOP/B"
    )
    print()

    print(
        f"{'tile':>6} "
        f"{'threads/block':>14} "
        f"{'shared/block':>14} "
        f"{'input loads':>16} "
        f"{'load reduction':>15} "
        f"{'approx GiB':>12} "
        f"{'AI FLOP/B':>12}"
    )
    print("-" * 100)

    for tile in TILES:
        result = tiled(N, tile)
        reduction = baseline["input_loads"] / result["input_loads"]

        print(
            f"{tile:>6} "
            f"{result['threads_per_block']:>14} "
            f"{result['shared_bytes'] / 1024:>12.2f} KiB "
            f"{result['input_loads']:>16,} "
            f"{reduction:>14.1f}x "
            f"{result['bytes'] / 1024**3:>12.3f} "
            f"{result['ai']:>12.3f}"
        )


if __name__ == "__main__":
    main()
