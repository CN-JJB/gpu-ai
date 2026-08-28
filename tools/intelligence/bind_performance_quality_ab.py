#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
from pathlib import Path

from experiment61_ab_contract import get_path, validate_manifest_pair
from verify_quality_comparison import verify_exact_quality_comparison_evidence


TRADEOFF_CONTRACT = "experiment61-model-performance-quality-v2"
QUALITY_COMPARISON_CONTRACT = "ppl-exact-quality-identity-v1"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_object(path, label, errors):
    try:
        text = path.read_text(encoding="utf-8").strip()
    except Exception as exc:
        errors.append(f"{label}: cannot read {path}: {exc}")
        return {}

    if not text:
        errors.append(f"{label}: empty file: {path}")
        return {}

    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        rows = []
        try:
            for line in text.splitlines():
                if line.strip():
                    rows.append(json.loads(line))
        except Exception as exc:
            errors.append(f"{label}: invalid JSON/JSONL: {exc}")
            return {}
        if len(rows) != 1:
            errors.append(
                f"{label}: expected exactly one record, found {len(rows)}"
            )
            return {}
        obj = rows[0]

    if not isinstance(obj, dict):
        errors.append(f"{label}: expected one JSON object")
        return {}
    return obj


def compare_field(actual, expected, label, errors):
    if actual != expected:
        errors.append(f"{label} mismatch: actual={actual!r} expected={expected!r}")


def bind_benchmark(label, manifest, benchmark, errors):
    variant = manifest.get("variant", {})
    fixed = manifest.get("fixed", {})
    protocol = fixed.get("protocol", {})
    hardware = variant.get("hardware", {})
    runtime = variant.get("runtime", {})
    model = variant.get("model", {})
    execution = variant.get("execution", {})
    prompt = variant.get("prompt", {})

    artifact = benchmark.get("artifact") or {}
    bench_runtime = benchmark.get("runtime") or {}
    bench_hardware = benchmark.get("hardware_evidence") or {}
    workload = benchmark.get("workload") or {}
    metrics = benchmark.get("metrics") or {}

    for actual, expected, field in (
        (artifact.get("sha256"), model.get("artifact_sha256"), "artifact.sha256"),
        (artifact.get("bytes"), model.get("artifact_bytes"), "artifact.bytes"),
        (artifact.get("quant"), model.get("quant"), "artifact.quant"),
        (
            artifact.get("source_revision"),
            model.get("source_revision"),
            "artifact.source_revision",
        ),
        (
            bench_runtime.get("runtime_identity"),
            runtime.get("runtime_identity"),
            "runtime.runtime_identity",
        ),
        (bench_runtime.get("backend"), runtime.get("backend"), "runtime.backend"),
        (
            bench_runtime.get("build_identity"),
            runtime.get("build_identity"),
            "runtime.build_identity",
        ),
        (
            bench_hardware.get("device_identity"),
            hardware.get("device_identity"),
            "hardware_evidence.device_identity",
        ),
        (
            bench_hardware.get("profile_sha256"),
            hardware.get("profile_sha256"),
            "hardware_evidence.profile_sha256",
        ),
        (workload.get("pp_tokens"), protocol.get("pp_tokens"), "workload.pp_tokens"),
        (workload.get("tg_tokens"), protocol.get("tg_tokens"), "workload.tg_tokens"),
        (
            workload.get("repetitions"),
            protocol.get("repetitions"),
            "workload.repetitions",
        ),
        (
            workload.get("warmup_runs"),
            protocol.get("warmup_runs", 0) or 0,
            "workload.warmup_runs",
        ),
        (workload.get("context"), execution.get("context"), "workload.context"),
        (
            workload.get("sequences"),
            execution.get("sequences"),
            "workload.sequences",
        ),
        (
            workload.get("gpu_layers"),
            execution.get("gpu_layers"),
            "workload.gpu_layers",
        ),
        (
            workload.get("flash_attention"),
            execution.get("flash_attention"),
            "workload.flash_attention",
        ),
        (workload.get("kv_k"), execution.get("kv_k"), "workload.kv_k"),
        (workload.get("kv_v"), execution.get("kv_v"), "workload.kv_v"),
        (
            workload.get("split_mode"),
            execution.get("split_mode"),
            "workload.split_mode",
        ),
        (
            workload.get("tensor_split"),
            execution.get("tensor_split"),
            "workload.tensor_split",
        ),
        (workload.get("threads"), execution.get("threads"), "workload.threads"),
        (
            workload.get("prompt_token_ids_sha256"),
            prompt.get("token_ids_sha256"),
            "workload.prompt_token_ids_sha256",
        ),
    ):
        compare_field(actual, expected, f"{label} {field}", errors)

    values = {}
    for metric_name in ("pp_tok_s", "tg_tok_s"):
        value = metrics.get(metric_name)
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(float(value))
            or value <= 0
        ):
            errors.append(f"{label} benchmark {metric_name} must be finite and > 0")
        else:
            values[metric_name] = float(value)

    return values


def validate_quality_comparison(
    quality,
    baseline_manifest,
    candidate_manifest,
    errors,
):
    if quality.get("quality_comparison_schema_version") != 1:
        errors.append("quality comparison schema version must be 1")
    if quality.get("comparison_contract") != QUALITY_COMPARISON_CONTRACT:
        errors.append(
            f"quality comparison contract must be {QUALITY_COMPARISON_CONTRACT!r}"
        )
    if quality.get("metric") != "PPL":
        errors.append("quality comparison metric must be PPL")
    if quality.get("lower_is_better") is not True:
        errors.append("quality comparison must declare lower_is_better=true")

    fixed_quality = quality.get("fixed_quality_identity")
    baseline_fixed = get_path(baseline_manifest, "fixed.quality_eval")
    candidate_fixed = get_path(candidate_manifest, "fixed.quality_eval")
    compare_field(
        fixed_quality,
        baseline_fixed,
        "quality fixed identity vs baseline manifest",
        errors,
    )
    compare_field(
        fixed_quality,
        candidate_fixed,
        "quality fixed identity vs candidate manifest",
        errors,
    )

    for side, manifest in (
        ("baseline", baseline_manifest),
        ("candidate", candidate_manifest),
    ):
        quality_side = quality.get(side) or {}
        model = get_path(manifest, "variant.model") or {}
        compare_field(
            quality_side.get("model_sha256"),
            model.get("artifact_sha256"),
            f"quality {side} model_sha256",
            errors,
        )
        compare_field(
            quality_side.get("model_bytes"),
            model.get("artifact_bytes"),
            f"quality {side} model_bytes",
            errors,
        )

    baseline = quality.get("baseline") or {}
    candidate = quality.get("candidate") or {}
    bppl = baseline.get("value")
    cppl = candidate.get("value")
    if not (
        isinstance(bppl, (int, float))
        and not isinstance(bppl, bool)
        and math.isfinite(float(bppl))
        and bppl > 0
        and isinstance(cppl, (int, float))
        and not isinstance(cppl, bool)
        and math.isfinite(float(cppl))
        and cppl > 0
    ):
        errors.append("quality comparison baseline/candidate PPL must be finite and > 0")
        return None

    bppl = float(bppl)
    cppl = float(cppl)
    expected_delta = cppl - bppl
    expected_ratio = cppl / bppl
    expected_percent = (expected_ratio - 1.0) * 100.0

    for actual, expected, label in (
        (
            quality.get("delta_candidate_minus_baseline"),
            expected_delta,
            "quality delta_candidate_minus_baseline",
        ),
        (
            quality.get("ratio_candidate_to_baseline"),
            expected_ratio,
            "quality ratio_candidate_to_baseline",
        ),
        (quality.get("percent_change"), expected_percent, "quality percent_change"),
    ):
        if (
            not isinstance(actual, (int, float))
            or isinstance(actual, bool)
            or not math.isclose(float(actual), expected, rel_tol=1e-12, abs_tol=1e-12)
        ):
            errors.append(
                f"{label} does not reproduce baseline/candidate PPL arithmetic"
            )

    return {
        "baseline_ppl": bppl,
        "candidate_ppl": cppl,
        "delta": expected_delta,
        "ratio": expected_ratio,
        "percent_change": expected_percent,
        "baseline_uncertainty": baseline.get("reported_uncertainty"),
        "candidate_uncertainty": candidate.get("reported_uncertainty"),
    }


def perf_delta(baseline, candidate):
    ratio = candidate / baseline
    return {
        "baseline": baseline,
        "candidate": candidate,
        "delta_candidate_minus_baseline": candidate - baseline,
        "ratio_candidate_to_baseline": ratio,
        "percent_change": (ratio - 1.0) * 100.0,
        "higher_is_better": True,
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Bind an independently reproducible I33 model-quality A/B to the same "
            "Experiment 61 one-variable performance A/B."
        )
    )
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
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    errors = []
    baseline_manifest = load_object(a.baseline_manifest, "baseline manifest", errors)
    candidate_manifest = load_object(a.candidate_manifest, "candidate manifest", errors)
    baseline_benchmark = load_object(a.baseline_benchmark, "baseline benchmark", errors)
    candidate_benchmark = load_object(a.candidate_benchmark, "candidate benchmark", errors)

    quality_result = verify_exact_quality_comparison_evidence(
        a.quality_comparison,
        a.baseline_quality_dir,
        a.candidate_quality_dir,
        a.baseline_model_artifact,
        a.candidate_model_artifact,
        a.quality_corpus,
    )
    errors.extend(
        "quality comparison evidence: " + error
        for error in quality_result["errors"]
    )
    quality = quality_result["comparison"] if not quality_result["errors"] else {}

    contract = None
    if baseline_manifest and candidate_manifest:
        contract = validate_manifest_pair(baseline_manifest, candidate_manifest)
        errors.extend("manifest contract: " + x for x in contract["errors"])

        declared = contract.get("intentional_variable")
        if isinstance(declared, str) and not (
            declared == "variant.model" or declared.startswith("variant.model.")
        ):
            errors.append(
                "I33 quality comparison currently binds only model-artifact A/B; "
                f"cannot attribute quality delta to intentional_variable={declared!r}"
            )

    baseline_metrics = {}
    candidate_metrics = {}
    if baseline_manifest and baseline_benchmark:
        baseline_metrics = bind_benchmark(
            "baseline", baseline_manifest, baseline_benchmark, errors
        )
    if candidate_manifest and candidate_benchmark:
        candidate_metrics = bind_benchmark(
            "candidate", candidate_manifest, candidate_benchmark, errors
        )

    quality_metrics = None
    if quality and baseline_manifest and candidate_manifest:
        quality_metrics = validate_quality_comparison(
            quality, baseline_manifest, candidate_manifest, errors
        )

    output = None
    if (
        not errors
        and contract is not None
        and quality_metrics is not None
        and all(key in baseline_metrics for key in ("pp_tok_s", "tg_tok_s"))
        and all(key in candidate_metrics for key in ("pp_tok_s", "tg_tok_s"))
    ):
        output = {
            "joint_tradeoff_schema_version": 2,
            "tradeoff_contract": TRADEOFF_CONTRACT,
            "comparison_id": contract["comparison_id"],
            "intentional_variable": contract["intentional_variable"],
            "semantic_differences": contract["semantic_differences"],
            "models": {
                "baseline_sha256": get_path(
                    baseline_manifest, "variant.model.artifact_sha256"
                ),
                "candidate_sha256": get_path(
                    candidate_manifest, "variant.model.artifact_sha256"
                ),
            },
            "performance": {
                "pp_tok_s": perf_delta(
                    baseline_metrics["pp_tok_s"],
                    candidate_metrics["pp_tok_s"],
                ),
                "tg_tok_s": perf_delta(
                    baseline_metrics["tg_tok_s"],
                    candidate_metrics["tg_tok_s"],
                ),
            },
            "quality": {
                "metric": "PPL",
                "lower_is_better": True,
                "baseline": quality_metrics["baseline_ppl"],
                "candidate": quality_metrics["candidate_ppl"],
                "delta_candidate_minus_baseline": quality_metrics["delta"],
                "ratio_candidate_to_baseline": quality_metrics["ratio"],
                "percent_change": quality_metrics["percent_change"],
                "baseline_reported_uncertainty": quality_metrics[
                    "baseline_uncertainty"
                ],
                "candidate_reported_uncertainty": quality_metrics[
                    "candidate_uncertainty"
                ],
            },
            "quality_evidence": {
                "comparison_sha256": sha256_file(a.quality_comparison),
                "comparison_contract": quality.get("comparison_contract"),
                "baseline_metric_sha256": (quality.get("baseline") or {}).get(
                    "metric_sha256"
                ),
                "candidate_metric_sha256": (quality.get("candidate") or {}).get(
                    "metric_sha256"
                ),
                "verification": "INDEPENDENTLY-REPRODUCED-I36",
            },
        }

    print("PERFORMANCE × QUALITY A/B BINDING")
    if contract is not None:
        print(f"comparison_id={contract.get('comparison_id')}")
        print(f"intentional_variable={contract.get('intentional_variable')}")
        print(f"semantic_differences={contract.get('semantic_differences')}")
    print("ERRORS")
    for error in errors:
        print("- " + error)

    if errors or output is None:
        print("JOINT TRADEOFF: BLOCKED")
        raise SystemExit(2)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        f"PP percent_change={output['performance']['pp_tok_s']['percent_change']}"
    )
    print(
        f"TG percent_change={output['performance']['tg_tok_s']['percent_change']}"
    )
    print(f"PPL percent_change={output['quality']['percent_change']}")
    print("quality_comparison_verification=INDEPENDENTLY-REPRODUCED-I36")
    print(f"out={a.out}")
    print("JOINT TRADEOFF: PASS")
    print(
        "PASS is a descriptive binding of one Experiment 61 model A/B across performance "
        "and independently reproduced PPL evidence. It is not an ACCEPT/REJECT or purchase recommendation."
    )


if __name__ == "__main__":
    main()
