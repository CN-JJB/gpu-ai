#!/usr/bin/env python3
import json
from pathlib import Path

EXPECTED = {
    "classic_gcn_primary_wave_size": 64,
    "rdna_supports_only_wave32": False,
    "rdna_wgp_groups_two_cus": True,
    "infinity_cache_is_extra_vram": False,
    "rdna_and_cdna_are_one_sequential_line": False,
    "cdna_mfma_is_matrix_acceleration": True,
    "rdna3_dual_issue_guarantees_2x": False,
    "mi300a_and_mi300x_same_package": False,
    "rdna4_fp8_int4_guarantees_q4_native_llm": False,
    "rocm_support_can_be_decided_by_architecture_name_only": False,
    "cdna5_currently_uses_wgp_wave32_direction": True,
    "rocm_7_14_standard_matrix_lists_cdna5_as_supported": False,
}

WHY = {
    "classic_gcn_primary_wave_size": "Classic GCN executes wave64; documented 16-wide SIMD handles the wave over multiple cycles.",
    "rdna_supports_only_wave32": "RDNA makes Wave32 primary but supports Wave64 compatibility/current ISA modes.",
    "rdna_wgp_groups_two_cus": "RDNA WGP organizes two closely coupled CUs and shared higher-level resources.",
    "infinity_cache_is_extra_vram": "Infinity Cache is on-die cache, not addressable model-capacity VRAM.",
    "rdna_and_cdna_are_one_sequential_line": "RDNA is graphics/latency branch; CDNA is dedicated compute/HPC/AI branch.",
    "cdna_mfma_is_matrix_acceleration": "MFMA is AMD Matrix Fused Multiply-Add hardware/instruction family.",
    "rdna3_dual_issue_guarantees_2x": "VOPD needs Wave32, independent ops, legal operands/register banks, and compiler pairing.",
    "mi300a_and_mi300x_same_package": "MI300A includes CPU chiplets/coherent shared HBM; MI300X is GPU-focused.",
    "rdna4_fp8_int4_guarantees_q4_native_llm": "Hardware datatype support and model storage/backend kernel mapping are separate.",
    "rocm_support_can_be_decided_by_architecture_name_only": "Official support is exact SKU/gfx target/OS/component specific.",
    "cdna5_currently_uses_wgp_wave32_direction": "AMD's current CDNA5 page describes a new WGP architecture and Wave32 execution.",
    "rocm_7_14_standard_matrix_lists_cdna5_as_supported": "The current ROCm 7.14 standard support table captured here lists Instinct through CDNA4.",
}

def main():
    path = Path(__file__).with_name("student_answers.json")
    got = json.loads(path.read_text(encoding="utf-8"))
    passed = 0
    for key, expected in EXPECTED.items():
        value = got.get(key, "<missing>")
        ok = value == expected
        passed += int(ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {key}: got={value!r}, expected={expected!r}")
        print(f"       {WHY[key]}")
    print()
    print(f"score: {passed}/{len(EXPECTED)}")
    raise SystemExit(0 if passed == len(EXPECTED) else 1)

if __name__ == "__main__":
    main()
