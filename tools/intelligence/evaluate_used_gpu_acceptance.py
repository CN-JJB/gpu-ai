#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
from pathlib import Path


MODEL_CONTRACT = "experiment86-used-gpu-acceptance-compatible-v1"


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_object(path, label, errors):
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{label}: invalid JSON: {exc}")
        return {}
    if not isinstance(obj, dict):
        errors.append(f"{label}: expected one JSON object")
        return {}
    return obj


def verify_packet(packet_path, case_path, errors):
    packet_path = Path(packet_path)
    case_path = Path(case_path)
    if not packet_path.is_file():
        errors.append(f"PACKET is not a file: {packet_path}")
        return None
    packet = load_object(packet_path, "PACKET", errors)
    if not packet:
        return None
    if packet.get("packet_schema_version") != 1:
        errors.append("PACKET packet_schema_version must be 1")
    files = packet.get("files")
    if not isinstance(files, list):
        errors.append("PACKET files must be a list")
        return packet
    if packet.get("file_count") != len(files):
        errors.append("PACKET file_count does not equal len(files)")

    root = packet_path.parent.resolve()
    seen = set()
    case_resolved = case_path.resolve()
    case_covered = False
    for item in files:
        if not isinstance(item, dict):
            errors.append("PACKET file entry must be an object")
            continue
        rel = item.get("path")
        if not isinstance(rel, str) or not rel:
            errors.append("PACKET file entry path must be non-empty")
            continue
        if rel in seen:
            errors.append(f"PACKET duplicate path: {rel}")
            continue
        seen.add(rel)

        candidate = (root / rel).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            errors.append(f"PACKET path escapes packet directory: {rel}")
            continue
        if not candidate.is_file():
            errors.append(f"PACKET indexed file is missing: {rel}")
            continue
        actual_bytes = candidate.stat().st_size
        actual_sha = sha256_file(candidate)
        if item.get("bytes") != actual_bytes:
            errors.append(f"PACKET byte count mismatch: {rel}")
        if item.get("sha256") != actual_sha:
            errors.append(f"PACKET SHA256 mismatch: {rel}")
        if candidate == case_resolved:
            case_covered = True

    if not case_covered:
        errors.append("acceptance case is not indexed by PACKET")
    return packet


def finite_positive(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and float(value) > 0
    )


def evaluate_case(case, errors):
    required = (
        "acceptance_case_schema_version",
        "case_id",
        "hardware_id",
        "synthetic",
        "claim",
        "observed",
        "workload",
        "errors",
        "pcie",
        "physical",
    )
    for field in required:
        if field not in case:
            errors.append(f"acceptance case missing {field}")
    if errors:
        return None

    if case.get("acceptance_case_schema_version") != 1:
        errors.append("acceptance_case_schema_version must be 1")
    if not isinstance(case.get("case_id"), str) or not case.get("case_id"):
        errors.append("case_id must be non-empty")
    if not isinstance(case.get("hardware_id"), str) or not case.get("hardware_id"):
        errors.append("hardware_id must be non-empty")
    if not isinstance(case.get("synthetic"), bool):
        errors.append("synthetic must be boolean")

    claim = case.get("claim") or {}
    observed = case.get("observed") or {}
    workload = case.get("workload") or {}
    error_state = case.get("errors") or {}
    pcie = case.get("pcie") or {}
    physical = case.get("physical") or {}

    claimed = claim.get("vram_gib")
    observed_vram = observed.get("vram_gib")
    tg_first = workload.get("tg_first")
    tg_last = workload.get("tg_last")
    for label, value in (
        ("claim.vram_gib", claimed),
        ("observed.vram_gib", observed_vram),
        ("workload.tg_first", tg_first),
        ("workload.tg_last", tg_last),
    ):
        if not finite_positive(value):
            errors.append(f"{label} must be finite and > 0")

    for label, value in (
        ("observed.driver_recognized", observed.get("driver_recognized")),
        (
            "observed.target_runtime_recognized",
            observed.get("target_runtime_recognized"),
        ),
        ("workload.sustained_completed", workload.get("sustained_completed")),
        ("pcie.observed_under_load", pcie.get("observed_under_load")),
        ("physical.display_required", physical.get("display_required")),
        (
            "physical.display_outputs_tested",
            physical.get("display_outputs_tested"),
        ),
    ):
        if not isinstance(value, bool):
            errors.append(f"{label} must be boolean")

    if errors:
        return None

    reject = []
    review = []
    info = []

    claimed = float(claimed)
    observed_vram = float(observed_vram)
    frac = observed_vram / claimed
    if frac < 0.90 or frac > 1.10:
        reject.append(
            "purchase-critical VRAM mismatch: "
            f"claimed={claimed:g} GiB observed={observed_vram:g} GiB"
        )

    if observed.get("driver_recognized") is not True:
        reject.append("vendor driver does not recognize target GPU")
    if observed.get("target_runtime_recognized") is not True:
        reject.append("target compute/runtime does not recognize GPU")
    if workload.get("sustained_completed") is not True:
        reject.append("ordinary sustained target workload did not complete")

    uncorr = error_state.get("uncorrectable")
    if uncorr is None:
        info.append("uncorrectable-error telemetry unsupported/unknown")
    elif not isinstance(uncorr, (int, float)) or isinstance(uncorr, bool) or not math.isfinite(float(uncorr)):
        errors.append("errors.uncorrectable must be finite numeric or null")
    elif float(uncorr) > 0:
        reject.append(f"observed uncorrectable errors: {uncorr}")

    max_width = pcie.get("max_width")
    current_width = pcie.get("current_width")
    expected_width = pcie.get("expected_platform_width")
    under_load = pcie.get("observed_under_load")

    for label, value in (
        ("pcie.max_width", max_width),
        ("pcie.current_width", current_width),
        ("pcie.expected_platform_width", expected_width),
    ):
        if value is not None and (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(float(value))
            or float(value) <= 0
        ):
            errors.append(f"{label} must be finite > 0 or null")

    if errors:
        return None

    if max_width and expected_width and float(max_width) < float(expected_width):
        review.append(
            f"reported max card/link width {max_width} below expected platform width "
            f"{expected_width}; inspect platform/card identity"
        )

    if current_width and expected_width and float(current_width) < float(expected_width):
        if under_load:
            review.append(
                f"under-load current PCIe width x{current_width} below expected "
                f"x{expected_width}; check slot/lanes/riser/card"
            )
        else:
            review.append(
                f"idle current PCIe width x{current_width} below expected "
                f"x{expected_width}; do not reject without under-load/platform check"
            )

    tg_first = float(tg_first)
    tg_last = float(tg_last)
    drift = (tg_last / tg_first) - 1.0
    info.append(f"sustained TG drift: {drift * 100:.3f}%")
    if drift < -0.15:
        review.append(
            f"sustained TG fell {abs(drift) * 100:.1f}% — investigate thermal/power/other limiter"
        )

    if physical.get("display_required") and not physical.get(
        "display_outputs_tested"
    ):
        review.append("display output required but not tested")

    if reject:
        decision = "REJECT"
    elif review:
        decision = "REVIEW"
    else:
        decision = "ACCEPT"

    return {
        "decision": decision,
        "info": info,
        "review": review,
        "reject": reject,
    }


def build_acceptance_artifact(case_path, packet_path):
    case_path = Path(case_path)
    packet_path = Path(packet_path)
    errors = []
    if not case_path.is_file():
        errors.append(f"acceptance case is not a file: {case_path}")
        case = {}
    else:
        case = load_object(case_path, "acceptance case", errors)

    verify_packet(packet_path, case_path, errors)

    evaluation = None
    if case:
        evaluation = evaluate_case(case, errors)

    artifact = None
    if not errors and evaluation is not None:
        artifact = {
            "used_gpu_acceptance_schema_version": 1,
            "acceptance_model": MODEL_CONTRACT,
            "case_id": case["case_id"],
            "hardware_id": case["hardware_id"],
            "synthetic": case["synthetic"],
            "decision": evaluation["decision"],
            "info": evaluation["info"],
            "review": evaluation["review"],
            "reject": evaluation["reject"],
            "evidence": {
                "case_sha256": sha256_file(case_path),
                "case_bytes": case_path.stat().st_size,
                "packet_sha256": sha256_file(packet_path),
                "packet_bytes": packet_path.stat().st_size,
            },
            "condition_grade_mapping": "UNDEFINED",
            "scope": (
                "Experiment 86-compatible used-GPU acceptance decision; "
                "not a hardware certificate"
            ),
        }

    return {"errors": errors, "artifact": artifact}


def main():
    p = argparse.ArgumentParser(
        description=(
            "Build a packet-bound machine-readable used-GPU ACCEPT/REVIEW/REJECT "
            "artifact using Experiment 86-compatible semantics."
        )
    )
    p.add_argument("--case", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    result = build_acceptance_artifact(a.case, a.packet)

    print("USED GPU ACCEPTANCE")
    print("ERRORS")
    for error in result["errors"]:
        print("- " + error)

    if result["errors"] or result["artifact"] is None:
        print("USED GPU ACCEPTANCE: BLOCKED")
        raise SystemExit(2)

    artifact = result["artifact"]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"decision={artifact['decision']}")
    print(f"condition_grade_mapping={artifact['condition_grade_mapping']}")
    print(f"out={a.out}")
    print("USED GPU ACCEPTANCE: PASS")
    print(
        "PASS means the Experiment 86-compatible decision is reproducible from a "
        "PACKET-bound case summary. It is not a C3/C4 grade or hardware certificate."
    )


if __name__ == "__main__":
    main()
