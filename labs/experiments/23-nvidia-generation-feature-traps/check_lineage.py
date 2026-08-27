#!/usr/bin/env python3
import json
from pathlib import Path

EXPECTED = {
    "first_tensor_core": "Volta",
    "first_independent_thread_scheduling": "Volta",
    "first_async_global_to_shared_copy": "Ampere",
    "first_tma_and_thread_block_cluster": "Hopper",
    "all_pascal_has_hbm2": False,
    "all_pascal_has_gp100_fast_fp16": False,
    "all_ampere_has_identical_fp32_sm": False,
    "hopper_is_geforce_successor_to_ampere": False,
    "all_blackwell_is_dual_die": False,
    "q4_gguf_on_blackwell_guarantees_native_fp4": False,
}

WHY = {
    "first_tensor_core": "Volta GV100 introduced Tensor Cores.",
    "first_independent_thread_scheduling": "Volta changed warp-level thread scheduling semantics.",
    "first_async_global_to_shared_copy": "Ampere added hardware-accelerated async global→shared copy.",
    "first_tma_and_thread_block_cluster": "Hopper added TMA and thread-block clusters.",
    "all_pascal_has_hbm2": "GP100 uses HBM2; GP10x consumer variants do not all share that memory system.",
    "all_pascal_has_gp100_fast_fp16": "Pascal variants have radically different FP16/INT8 priorities.",
    "all_ampere_has_identical_fp32_sm": "GA100 cc8.0 and GA10x cc8.6 differ; NVIDIA documents different FP32 ops/cycle behavior.",
    "hopper_is_geforce_successor_to_ampere": "Hopper is mainly datacenter; Ada is the contemporary RTX/workstation branch.",
    "all_blackwell_is_dual_die": "Datacenter and RTX Blackwell are different implementations; RTX Blackwell is not defined by flagship datacenter package topology.",
    "q4_gguf_on_blackwell_guarantees_native_fp4": "Storage/quant format and matrix instruction datatype are separate layers.",
}

def main():
    path = Path(__file__).with_name("student_answers.json")
    got = json.loads(path.read_text(encoding="utf-8"))
    passed = 0
    for key, expected in EXPECTED.items():
        value = got.get(key, "<missing>")
        ok = value == expected
        passed += int(ok)
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {key}: got={value!r}, expected={expected!r}")
        print(f"       {WHY[key]}")
    print()
    print(f"score: {passed}/{len(EXPECTED)}")
    raise SystemExit(0 if passed == len(EXPECTED) else 1)

if __name__ == "__main__":
    main()
