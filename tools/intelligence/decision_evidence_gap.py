#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

from bind_performance_quality_ab import load_object
from compatibility_preflight import load as load_jsonl
from market_evidence_gate import (
    expected_grade,
    freshness,
    watchlist_gate,
)
from verify_tradeoff_route import verify_tradeoff_route


def evaluate_real_benchmark(label, record):
    errors = []
    if record.get("record_type") != "benchmark":
        errors.append(f"{label}: record_type must be benchmark")
    if record.get("synthetic", False):
        errors.append(f"{label}: synthetic benchmark is not production decision evidence")
    source = record.get("source") or {}
    if source.get("evidence_class") != "MEASURED":
        errors.append(
            f"{label}: source.evidence_class must be MEASURED for production readiness"
        )
    evidence = record.get("evidence") or {}
    if not evidence.get("packet_source"):
        errors.append(f"{label}: benchmark is missing packet_source")
    return errors


def exact_measured_compatibility(catalog, benchmark, as_of):
    hardware_id = benchmark.get("hardware_id")
    model_id = benchmark.get("model_id")
    runtime_id = benchmark.get("runtime_id")
    runtime = benchmark.get("runtime") or {}
    artifact = benchmark.get("artifact") or {}
    backend = str(runtime.get("backend") or "").upper()
    artifact_sha = artifact.get("sha256")
    runtime_build = runtime.get("build_identity")

    candidates = []
    for record in load_jsonl(Path(catalog) / "compatibility.jsonl"):
        if record.get("synthetic", False):
            continue
        if record.get("hardware_id") != hardware_id:
            continue
        if record.get("model_id") != model_id:
            continue
        if record.get("runtime_id") != runtime_id:
            continue
        if str(record.get("backend") or "").upper() != backend:
            continue
        scope = record.get("scope") or {}
        if scope.get("artifact_sha256") != artifact_sha:
            continue
        if scope.get("runtime_build") != runtime_build:
            continue
        candidates.append(record)

    if not candidates:
        return {
            "status": "BLOCKED",
            "reason": "no exact non-synthetic MEASURED_SUPPORTED compatibility record",
            "record_id": None,
        }

    candidates.sort(key=lambda x: str(x.get("observed_at") or ""), reverse=True)
    record = candidates[0]
    if str(record.get("status") or "").upper() != "MEASURED_SUPPORTED":
        return {
            "status": "BLOCKED",
            "reason": f"exact compatibility status is {record.get('status')!r}, not MEASURED_SUPPORTED",
            "record_id": record.get("record_id"),
        }

    revalidate = record.get("revalidate_after")
    if not revalidate:
        return {
            "status": "BLOCKED",
            "reason": "exact compatibility record has no revalidate_after",
            "record_id": record.get("record_id"),
        }
    try:
        revalidate_date = date.fromisoformat(str(revalidate))
    except ValueError:
        return {
            "status": "BLOCKED",
            "reason": "exact compatibility revalidate_after is invalid",
            "record_id": record.get("record_id"),
        }

    if revalidate_date < as_of:
        return {
            "status": "BLOCKED",
            "reason": "exact measured compatibility is stale",
            "record_id": record.get("record_id"),
        }

    return {
        "status": "PASS",
        "reason": "exact non-synthetic MEASURED_SUPPORTED compatibility is current",
        "record_id": record.get("record_id"),
    }


def evaluate_market(catalog, record_id, hardware_id, as_of):
    rows = [
        x
        for x in load_jsonl(Path(catalog) / "market.jsonl")
        if x.get("record_id") == record_id
    ]
    if not rows:
        return {
            "status": "BLOCKED",
            "reason": f"market record not found: {record_id}",
            "record_id": record_id,
        }
    if len(rows) != 1:
        return {
            "status": "BLOCKED",
            "reason": f"market record ID is not unique: {record_id}",
            "record_id": record_id,
        }

    record = rows[0]
    if record.get("synthetic", False):
        return {
            "status": "BLOCKED",
            "reason": "synthetic market observation is not production purchase evidence",
            "record_id": record_id,
        }
    if record.get("hardware_id") != hardware_id:
        return {
            "status": "BLOCKED",
            "reason": "market observation hardware_id does not match candidate benchmark",
            "record_id": record_id,
        }

    grade = str(record.get("market_evidence_grade") or "").upper()
    expected = expected_grade(record)
    if expected is None or grade != expected:
        return {
            "status": "BLOCKED",
            "reason": f"market evidence grade mismatch: actual={grade!r} expected={expected!r}",
            "record_id": record_id,
        }

    fresh = freshness(record, as_of)
    gate = watchlist_gate(grade, fresh)
    if gate != "ELIGIBLE":
        return {
            "status": "BLOCKED",
            "reason": f"Experiment 38 market component is {gate}",
            "record_id": record_id,
            "grade": grade,
            "freshness": fresh,
        }

    return {
        "status": "PASS",
        "reason": "current M2/M3 market evidence may satisfy only the Experiment 38 market component",
        "record_id": record_id,
        "grade": grade,
        "freshness": fresh,
        "transaction_amount_proven": (
            str(record.get("price_state") or "").upper() == "SOLD_CONFIRMED"
            and (record.get("transaction") or {}).get("confirmed_price") is True
        ),
    }


def evaluate_feasibility_case(path):
    if path is None:
        return {
            "status": "BLOCKED",
            "decision": "MISSING",
            "reason": "no Experiment 90 feasibility case supplied",
        }

    path = Path(path)
    if not path.is_file():
        return {
            "status": "BLOCKED",
            "decision": "MISSING",
            "reason": f"feasibility case is not a file: {path}",
        }

    try:
        c = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "status": "BLOCKED",
            "decision": "INVALID",
            "reason": f"invalid feasibility JSON: {exc}",
        }

    fail = []
    blocked = []

    def gate(name, value, reason):
        if value is False:
            fail.append(f"{name}: {reason}")
        elif value is None:
            blocked.append(f"{name}: UNKNOWN — {reason}")

    try:
        req = float(c["model"]["required_runtime_vram_gib"])
        avail = float(c["gpu"]["runtime_available_vram_gib"])
        gate("model_vram", avail >= req, f"required={req:g} available={avail:g}")

        gate(
            "runtime_backend",
            c["software"].get("target_backend_supported"),
            "exact target runtime/backend support",
        )

        if c["gpu"].get("multi_gpu"):
            gate(
                "multi_gpu_topology",
                c["gpu"].get("topology_validated"),
                "split/topology/P2P/lane evidence",
            )

        ram_req = float(c["host"]["required_ram_gib"])
        ram_avail = float(c["host"]["available_ram_gib"])
        gate("host_ram", ram_avail >= ram_req, f"required={ram_req:g} available={ram_avail:g}")

        storage_req = float(c["storage"]["required_free_gib"])
        storage_avail = float(c["storage"]["available_free_gib"])
        gate(
            "storage",
            storage_avail >= storage_req,
            f"required={storage_req:g} available={storage_avail:g}",
        )

        gate(
            "psu_capacity",
            c["psu"].get("capacity_policy_pass"),
            "PSU continuous/headroom policy",
        )
        gate(
            "psu_cables",
            c["psu"].get("cable_compatibility_confirmed"),
            "exact modular/auxiliary cable compatibility",
        )
        gate(
            "sustained_thermal",
            c["thermal"].get("sustained_target_pass"),
            "sustained workload/thermal target",
        )

        if c["serving"].get("required"):
            gate(
                "serving_slo",
                c["serving"].get("slo_pass"),
                "declared TTFT/ITL/throughput SLO",
            )

        if c["network"].get("wider_than_loopback"):
            gate(
                "network_controls",
                c["network"].get("controls_pass"),
                "declared auth/TLS/exposure policy",
            )

        budget = float(c["budget"]["max_total"])
        cost = float(c["budget"]["estimated_total"])
        gate("budget", cost <= budget, f"max={budget:g} estimated={cost:g}")
    except Exception as exc:
        return {
            "status": "BLOCKED",
            "decision": "INVALID",
            "reason": f"invalid Experiment 90 case structure: {exc}",
        }

    if blocked:
        decision = "BLOCKED"
    elif fail:
        decision = "REVISE"
    else:
        decision = "ACCEPT"

    return {
        "status": "PASS" if decision == "ACCEPT" else "BLOCKED",
        "decision": decision,
        "reason": (
            "Experiment 90 hard gates accept the declared whole-machine case"
            if decision == "ACCEPT"
            else "Experiment 90 case is not ACCEPT"
        ),
        "unknowns": blocked,
        "known_failures": fail,
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Report which evidence domains are machine-ready before any human purchase "
            "decision. This tool intentionally does not emit BUY/WATCH/REJECT."
        )
    )
    p.add_argument("catalog", type=Path)
    p.add_argument("--joint-tradeoff", type=Path, required=True)
    p.add_argument("--baseline-manifest", type=Path, required=True)
    p.add_argument("--candidate-manifest", type=Path, required=True)
    p.add_argument("--baseline-benchmark", type=Path, required=True)
    p.add_argument("--candidate-benchmark", type=Path, required=True)
    p.add_argument("--quality-comparison", type=Path, required=True)
    p.add_argument("--baseline-quality-dir", type=Path, required=True)
    p.add_argument("--candidate-quality-dir", type=Path, required=True)
    p.add_argument("--baseline-model-artifact", type=Path, required=True)
    p.add_argument("--candidate-model-artifact", type=Path, required=True)
    p.add_argument("--quality-corpus", type=Path, required=True)
    p.add_argument("--variable-contract", type=Path)
    p.add_argument("--market-record-id", required=True)
    p.add_argument("--feasibility-case", type=Path)
    p.add_argument("--as-of", default=date.today().isoformat())
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    as_of = date.fromisoformat(a.as_of)

    route = verify_tradeoff_route(
        a.joint_tradeoff,
        a.baseline_manifest,
        a.candidate_manifest,
        a.baseline_benchmark,
        a.candidate_benchmark,
        a.quality_comparison,
        a.baseline_quality_dir,
        a.candidate_quality_dir,
        a.baseline_model_artifact,
        a.candidate_model_artifact,
        a.quality_corpus,
        a.variable_contract,
    )

    route_component = {
        "status": "PASS" if not route["errors"] else "BLOCKED",
        "reason": (
            f"verified through {route['route']}"
            if not route["errors"]
            else "; ".join(route["errors"])
        ),
        "route": route["route"],
    }

    errors = []
    baseline = load_object(a.baseline_benchmark, "baseline benchmark", errors)
    candidate = load_object(a.candidate_benchmark, "candidate benchmark", errors)

    benchmark_errors = []
    if baseline:
        benchmark_errors.extend(evaluate_real_benchmark("baseline", baseline))
    if candidate:
        benchmark_errors.extend(evaluate_real_benchmark("candidate", candidate))
    benchmark_errors.extend(errors)

    benchmark_component = {
        "status": "PASS" if not benchmark_errors else "BLOCKED",
        "reason": (
            "both benchmark records are non-synthetic MEASURED evidence with packet roots"
            if not benchmark_errors
            else "; ".join(benchmark_errors)
        ),
    }

    compatibility_component = {
        "status": "BLOCKED",
        "reason": "candidate benchmark unavailable",
        "record_id": None,
    }
    market_component = {
        "status": "BLOCKED",
        "reason": "candidate benchmark unavailable",
        "record_id": a.market_record_id,
    }
    if candidate:
        compatibility_component = exact_measured_compatibility(
            a.catalog, candidate, as_of
        )
        market_component = evaluate_market(
            a.catalog,
            a.market_record_id,
            candidate.get("hardware_id"),
            as_of,
        )

    feasibility_component = evaluate_feasibility_case(a.feasibility_case)

    unresolved = {
        "condition_acceptance": {
            "status": "BLOCKED",
            "reason": (
                "Experiment 38 requires C3/C4 condition evidence, but Intelligence "
                "does not yet have a machine-readable C0–C4 condition gate"
            ),
            "next_evidence": "Experiment 87 real used-GPU acceptance packet",
        },
        "performance_target": {
            "status": "BLOCKED",
            "reason": (
                "verified PP/TG/PPL comparison does not prove the candidate meets a "
                "declared target performance/SLO threshold"
            ),
            "next_evidence": "explicit target/SLO policy tied to measured candidate metrics",
        },
        "price_ceiling": {
            "status": "BLOCKED",
            "reason": (
                "Experiment 38 personal max sticker / watch-band policy is not supplied "
                "to this evidence-only gate"
            ),
            "next_evidence": "explicit personal price-ceiling policy",
        },
    }

    components = {
        "verified_tradeoff": route_component,
        "real_benchmark_provenance": benchmark_component,
        "exact_measured_compatibility": compatibility_component,
        "current_market_evidence": market_component,
        "whole_machine_feasibility": feasibility_component,
        **unresolved,
    }

    blockers = [
        name
        for name, component in components.items()
        if component.get("status") != "PASS"
    ]

    report = {
        "decision_evidence_gap_schema_version": 1,
        "as_of": a.as_of,
        "comparison_id": (
            route["contract"].get("comparison_id")
            if route["contract"] is not None
            else None
        ),
        "intentional_variable": (
            route["contract"].get("intentional_variable")
            if route["contract"] is not None
            else None
        ),
        "components": components,
        "blockers": blockers,
        "decision_readiness": (
            "READY-FOR-HUMAN-REVIEW" if not blockers else "BLOCKED"
        ),
        "automatic_purchase_decision": "NOT-PERMITTED",
    }

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("DECISION EVIDENCE GAP MATRIX")
    for name, component in components.items():
        print(
            f"- {name}: {component.get('status')} | "
            f"{component.get('reason')}"
        )
    print(f"blockers={','.join(blockers) if blockers else 'NONE'}")
    print(f"DECISION READINESS: {report['decision_readiness']}")
    print("AUTOMATIC PURCHASE DECISION: NOT-PERMITTED")
    print(f"out={a.out}")


if __name__ == "__main__":
    main()
