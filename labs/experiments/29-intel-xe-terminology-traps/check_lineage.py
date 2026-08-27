#!/usr/bin/env python3
import json
from pathlib import Path

EXPECTED = {
  "eu_equals_cuda_core_1_to_1": False,
  "xe_core_equals_vector_engine": False,
  "xmx_is_matrix_acceleration": True,
  "xe_lp_has_same_arc_class_xmx_path": False,
  "alchemist_is_xe_hpg": True,
  "battlemage_is_xe2": True,
  "intel_subgroup_always_32": False,
  "slm_is_extra_vram": False,
  "level_zero_is_hardware_architecture": False,
  "xmx_guarantees_q4_gguf_native_path": False,
}

WHY = {
  "eu_equals_cuda_core_1_to_1": "EU/Vector Engine and CUDA core are different architectural granularities.",
  "xe_core_equals_vector_engine": "Xe-Core contains multiple Vector Engines and, on relevant families, XMX plus shared resources.",
  "xmx_is_matrix_acceleration": "XMX is Intel's matrix/dot-product acceleration path.",
  "xe_lp_has_same_arc_class_xmx_path": "Xe-LP integrated graphics is not the same Xe-HPG XMX organization as Arc Alchemist.",
  "alchemist_is_xe_hpg": "Arc A-series Alchemist is Xe-HPG.",
  "battlemage_is_xe2": "Arc B-series Battlemage uses Xe2.",
  "intel_subgroup_always_32": "Supported subgroup sizes vary by architecture/product.",
  "slm_is_extra_vram": "SLM is small on-chip shared local memory, not model-capacity VRAM.",
  "level_zero_is_hardware_architecture": "Level Zero is a low-level software/device interface.",
  "xmx_guarantees_q4_gguf_native_path": "Quant storage, backend kernel, reorder/dequant and matrix instruction are separate layers.",
}

def main():
    got = json.loads(Path(__file__).with_name("student_answers.json").read_text())
    passed = 0
    for k, expected in EXPECTED.items():
        value = got.get(k, "<missing>")
        ok = value == expected
        passed += int(ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {k}: got={value!r} expected={expected!r}")
        print(f"       {WHY[k]}")
    print()
    print(f"score: {passed}/{len(EXPECTED)}")
    raise SystemExit(0 if passed == len(EXPECTED) else 1)

if __name__ == "__main__":
    main()
