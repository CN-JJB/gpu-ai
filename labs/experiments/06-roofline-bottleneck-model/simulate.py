#!/usr/bin/env python3

PROFILES = {
    "GPU A": {
        "compute_tflops": 20.0,
        "bandwidth_gbs": 500.0,
        "note": "base",
    },
    "GPU B": {
        "compute_tflops": 40.0,
        "bandwidth_gbs": 500.0,
        "note": "2x compute, same bandwidth",
    },
    "GPU C": {
        "compute_tflops": 20.0,
        "bandwidth_gbs": 1000.0,
        "note": "same compute, 2x bandwidth",
    },
}

ARITHMETIC_INTENSITIES = [0.25, 1.0, 4.0, 16.0, 40.0, 80.0, 160.0]


def ridge_point(compute_tflops: float, bandwidth_gbs: float) -> float:
    return compute_tflops * 1000.0 / bandwidth_gbs


def roofline_ceiling(
    compute_tflops: float,
    bandwidth_gbs: float,
    arithmetic_intensity: float,
):
    memory_roof_tflops = bandwidth_gbs * arithmetic_intensity / 1000.0
    ceiling = min(compute_tflops, memory_roof_tflops)

    if abs(memory_roof_tflops - compute_tflops) < 1e-12:
        bound = "ridge"
    elif memory_roof_tflops < compute_tflops:
        bound = "memory"
    else:
        bound = "compute"

    return ceiling, bound


def main():
    print("Abstract Roofline model; these are not real GPUs.\n")

    for name, profile in PROFILES.items():
        compute = profile["compute_tflops"]
        bandwidth = profile["bandwidth_gbs"]
        ridge = ridge_point(compute, bandwidth)

        print(
            f"{name}: {compute:.0f} TFLOP/s, {bandwidth:.0f} GB/s, "
            f"ridge={ridge:.1f} FLOP/B ({profile['note']})"
        )

        for ai in ARITHMETIC_INTENSITIES:
            ceiling, bound = roofline_ceiling(compute, bandwidth, ai)
            label = {
                "memory": "memory-bound",
                "compute": "compute-bound",
                "ridge": "ridge/compute ceiling",
            }[bound]

            print(
                f"  AI={ai:>6.2f} -> {ceiling:>7.3f} TFLOP/s  {label}"
            )

        print()


if __name__ == "__main__":
    main()
