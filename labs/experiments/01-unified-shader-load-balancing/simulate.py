#!/usr/bin/env python3

TOTAL_UNITS = 128
FIXED_VERTEX_UNITS = 64
FIXED_PIXEL_UNITS = 64
UNIFIED_OVERHEAD = 1.05

SCENARIOS = {
    "vertex-heavy": (8000, 2000),
    "balanced": (5000, 5000),
    "pixel-heavy": (2000, 8000),
}

def fixed_pipeline(vertex_work: float, pixel_work: float):
    vertex_time = vertex_work / FIXED_VERTEX_UNITS
    pixel_time = pixel_work / FIXED_PIXEL_UNITS
    total_time = max(vertex_time, pixel_time)
    utilization = (vertex_work + pixel_work) / (TOTAL_UNITS * total_time)
    return total_time, utilization

def unified_pool(vertex_work: float, pixel_work: float):
    ideal_time = (vertex_work + pixel_work) / TOTAL_UNITS
    total_time = ideal_time * UNIFIED_OVERHEAD
    utilization = (vertex_work + pixel_work) / (TOTAL_UNITS * total_time)
    return total_time, utilization

def main():
    print("Concept model: fixed 64/64 partition vs unified 128-unit pool")
    print("Unified scheduling/generalization overhead: 5%\n")
    print(f"{'scenario':<14} {'fixed time':>12} {'fixed util':>12} {'unified time':>14} {'unified util':>14} {'speedup':>10}")
    print("-" * 82)
    for name, (vertex, pixel) in SCENARIOS.items():
        fixed_time, fixed_util = fixed_pipeline(vertex, pixel)
        unified_time, unified_util = unified_pool(vertex, pixel)
        speedup = fixed_time / unified_time
        print(f"{name:<14} {fixed_time:>12.2f} {fixed_util:>11.1%} {unified_time:>14.2f} {unified_util:>13.1%} {speedup:>9.2f}x")

if __name__ == "__main__":
    main()
