#!/usr/bin/env python3
import copy
import json
import sys
import tempfile
from pathlib import Path

from execution_joint_tradeoff_selftest import bind_args as execution_bind_args
from joint_tradeoff_selftest import (
    benchmark,
    bind_args as model_bind_args,
    capture_quality,
    make_quality_comparison,
    manifest as model_manifest,
    run,
    sha256_bytes,
    write,
    write_fake,
    write_identity,
)
from quality_execution_variable_selftest import (
    capture as execution_capture,
    compare_args as execution_compare_args,
    fake_executable,
    identity as execution_identity,
    manifest as execution_manifest,
)


HERE = Path(__file__).resolve().parent
PY = sys.executable


def route_args(
    joint,
    bm,
    cm,
    bb,
    cb,
    comparison,
    base_q,
    cand_q,
    baseline_model,
    candidate_model,
    corpus,
    out,
    variable_contract=None,
):
    args = [
        PY,
        str(HERE / "verify_tradeoff_route.py"),
        "--joint-tradeoff",
        str(joint),
        "--baseline-manifest",
        str(bm),
        "--candidate-manifest",
        str(cm),
        "--baseline-benchmark",
        str(bb),
        "--candidate-benchmark",
        str(cb),
        "--quality-comparison",
        str(comparison),
        "--baseline-quality-dir",
        str(base_q),
        "--candidate-quality-dir",
        str(cand_q),
        "--baseline-model-artifact",
        str(baseline_model),
        "--candidate-model-artifact",
        str(candidate_model),
        "--quality-corpus",
        str(corpus),
        "--out",
        str(out),
    ]
    if variable_contract is not None:
        args.extend(["--variable-contract", str(variable_contract)])
    return args


def build_model_fixture(td):
    corpus = td / "model-corpus.txt"
    corpus.write_bytes(b"i42 model corpus\n")
    corpus_sha = sha256_bytes(corpus.read_bytes())

    baseline_model = td / "model-baseline.gguf"
    baseline_model.write_bytes(b"baseline-i42-model\n")
    candidate_model = td / "model-candidate.gguf"
    candidate_model.write_bytes(b"candidate-i42-model\n")

    bm = model_manifest(
        "baseline",
        sha256_bytes(baseline_model.read_bytes()),
        baseline_model.stat().st_size,
        "Q8_0",
        corpus_sha,
    )
    cm = model_manifest(
        "candidate",
        sha256_bytes(candidate_model.read_bytes()),
        candidate_model.stat().st_size,
        "Q4_K_M",
        corpus_sha,
    )
    bm["comparison_id"] = "fixture-i42-model"
    cm["comparison_id"] = "fixture-i42-model"

    bm_path = td / "model-baseline-manifest.json"
    cm_path = td / "model-candidate-manifest.json"
    bb_path = td / "model-baseline-benchmark.json"
    cb_path = td / "model-candidate-benchmark.json"
    write(bm_path, bm)
    write(cm_path, cm)
    write(bb_path, benchmark(bm, 1000.0, 50.0))
    write(cb_path, benchmark(cm, 1200.0, 60.0))

    bi = td / "model-baseline-identity.json"
    ci = td / "model-candidate-identity.json"
    write_identity(bi, corpus_sha)
    write_identity(ci, corpus_sha)

    fake = td / "model-fake-quality"
    write_fake(fake)
    bq = td / "model-baseline-quality"
    cq = td / "model-candidate-quality"
    capture_quality(bq, fake, baseline_model, corpus, bi)
    capture_quality(cq, fake, candidate_model, corpus, ci)

    comparison = td / "model-quality-comparison.json"
    make_quality_comparison(
        bq, cq, baseline_model, candidate_model, corpus, comparison
    )

    joint = td / "model-joint.json"
    out = run(
        model_bind_args(
            bm_path,
            cm_path,
            bb_path,
            cb_path,
            comparison,
            bq,
            cq,
            baseline_model,
            candidate_model,
            corpus,
            joint,
        )
    )
    assert "JOINT TRADEOFF: PASS" in out

    return {
        "corpus": corpus,
        "baseline_model": baseline_model,
        "candidate_model": candidate_model,
        "bm": bm_path,
        "cm": cm_path,
        "bb": bb_path,
        "cb": cb_path,
        "bq": bq,
        "cq": cq,
        "comparison": comparison,
        "joint": joint,
        "bm_obj": bm,
        "cm_obj": cm,
    }


def build_execution_fixture(td):
    corpus = td / "execution-corpus.txt"
    corpus.write_bytes(b"i42 execution corpus\n")
    corpus_sha = sha256_bytes(corpus.read_bytes())

    model = td / "execution-model.gguf"
    model.write_bytes(b"same-i42-execution-model\n")
    model_sha = sha256_bytes(model.read_bytes())
    model_bytes = model.stat().st_size

    bm = execution_manifest("baseline", "f16")
    cm = execution_manifest("candidate", "q8_0")
    bm["comparison_id"] = "fixture-i42-execution"
    cm["comparison_id"] = "fixture-i42-execution"
    for obj in (bm, cm):
        obj["variant"]["model"]["artifact_sha256"] = model_sha
        obj["variant"]["model"]["artifact_bytes"] = model_bytes
        obj["fixed"]["quality_eval"]["corpus_sha256"] = corpus_sha

    bm_path = td / "execution-baseline-manifest.json"
    cm_path = td / "execution-candidate-manifest.json"
    bb_path = td / "execution-baseline-benchmark.json"
    cb_path = td / "execution-candidate-benchmark.json"
    write(bm_path, bm)
    write(cm_path, cm)
    write(bb_path, benchmark(bm, 1000.0, 50.0))
    write(cb_path, benchmark(cm, 1100.0, 52.5))

    baseline_args = ["--fixture-kv-k", "f16"]
    candidate_args = ["--fixture-kv-k", "q8_0"]
    bi = td / "execution-baseline-identity.json"
    ci = td / "execution-candidate-identity.json"
    execution_identity(bi, corpus, baseline_args)
    execution_identity(ci, corpus, candidate_args)

    fake = td / "execution-fake-quality"
    fake_executable(fake)
    bq = td / "execution-baseline-quality"
    cq = td / "execution-candidate-quality"
    execution_capture(bq, fake, model, corpus, bi, baseline_args)
    execution_capture(cq, fake, model, corpus, ci, candidate_args)

    variable_contract = {
        "quality_variable_contract_schema_version": 1,
        "comparison_id": "fixture-i42-execution",
        "intentional_variable": "variant.execution.kv_k",
        "baseline": {
            "manifest_value": "f16",
            "evaluation_args": baseline_args,
        },
        "candidate": {
            "manifest_value": "q8_0",
            "evaluation_args": candidate_args,
        },
    }
    contract_path = td / "execution-variable-contract.json"
    write(contract_path, variable_contract)

    comparison = td / "execution-quality-comparison.json"
    out = run(
        execution_compare_args(
            bm_path,
            cm_path,
            bq,
            cq,
            model,
            corpus,
            contract_path,
            comparison,
        )
    )
    assert "QUALITY VARIABLE COMPARISON: PASS" in out

    joint = td / "execution-joint.json"
    out = run(
        execution_bind_args(
            bm_path,
            cm_path,
            bb_path,
            cb_path,
            comparison,
            bq,
            cq,
            model,
            corpus,
            contract_path,
            joint,
        )
    )
    assert "EXECUTION JOINT TRADEOFF: PASS" in out

    return {
        "corpus": corpus,
        "model": model,
        "bm": bm_path,
        "cm": cm_path,
        "bb": bb_path,
        "cb": cb_path,
        "bq": bq,
        "cq": cq,
        "comparison": comparison,
        "joint": joint,
        "contract": contract_path,
        "bm_obj": bm,
        "cm_obj": cm,
    }


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        model = build_model_fixture(td)
        model_envelope = td / "model-envelope.json"
        out = run(
            route_args(
                model["joint"],
                model["bm"],
                model["cm"],
                model["bb"],
                model["cb"],
                model["comparison"],
                model["bq"],
                model["cq"],
                model["baseline_model"],
                model["candidate_model"],
                model["corpus"],
                model_envelope,
            )
        )
        assert "route=MODEL_ARTIFACT_I38" in out
        assert "verifier=I38" in out
        assert "VERIFIED TRADEOFF ROUTE: PASS" in out
        obj = json.loads(model_envelope.read_text(encoding="utf-8"))
        assert obj["route"] == "MODEL_ARTIFACT_I38"
        assert obj["scope"] == "DESCRIPTIVE_ONLY"

        execution = build_execution_fixture(td)
        execution_envelope = td / "execution-envelope.json"
        out = run(
            route_args(
                execution["joint"],
                execution["bm"],
                execution["cm"],
                execution["bb"],
                execution["cb"],
                execution["comparison"],
                execution["bq"],
                execution["cq"],
                execution["model"],
                execution["model"],
                execution["corpus"],
                execution_envelope,
                execution["contract"],
            )
        )
        assert "route=EXECUTION_VARIABLE_I41" in out
        assert "verifier=I41" in out
        assert "VERIFIED TRADEOFF ROUTE: PASS" in out
        obj = json.loads(execution_envelope.read_text(encoding="utf-8"))
        assert obj["route"] == "EXECUTION_VARIABLE_I41"
        assert obj["sources"]["variable_contract_sha256"]

        missing_contract = td / "missing-contract-envelope.json"
        out = run(
            route_args(
                execution["joint"],
                execution["bm"],
                execution["cm"],
                execution["bb"],
                execution["cb"],
                execution["comparison"],
                execution["bq"],
                execution["cq"],
                execution["model"],
                execution["model"],
                execution["corpus"],
                missing_contract,
            ),
            expect=2,
        )
        assert "execution-variable tradeoff route requires --variable-contract" in out
        assert "VERIFIED TRADEOFF ROUTE: BLOCKED" in out
        assert not missing_contract.exists()

        wrong_extra = td / "wrong-extra-envelope.json"
        out = run(
            route_args(
                model["joint"],
                model["bm"],
                model["cm"],
                model["bb"],
                model["cb"],
                model["comparison"],
                model["bq"],
                model["cq"],
                model["baseline_model"],
                model["candidate_model"],
                model["corpus"],
                wrong_extra,
                execution["contract"],
            ),
            expect=2,
        )
        assert "model-artifact tradeoff route does not accept --variable-contract" in out
        assert not wrong_extra.exists()

        unsupported_bm = copy.deepcopy(execution["bm_obj"])
        unsupported_cm = copy.deepcopy(execution["bm_obj"])
        unsupported_bm["comparison_id"] = "fixture-i42-runtime"
        unsupported_cm["comparison_id"] = "fixture-i42-runtime"
        unsupported_bm["label"] = "baseline"
        unsupported_cm["label"] = "candidate"
        unsupported_bm["intentional_variable"] = "variant.runtime.backend"
        unsupported_cm["intentional_variable"] = "variant.runtime.backend"
        unsupported_cm["variant"]["runtime"]["backend"] = "OTHER"
        ubm = td / "unsupported-baseline.json"
        ucm = td / "unsupported-candidate.json"
        write(ubm, unsupported_bm)
        write(ucm, unsupported_cm)

        unsupported_out = td / "unsupported-envelope.json"
        out = run(
            route_args(
                execution["joint"],
                ubm,
                ucm,
                execution["bb"],
                execution["cb"],
                execution["comparison"],
                execution["bq"],
                execution["cq"],
                execution["model"],
                execution["model"],
                execution["corpus"],
                unsupported_out,
            ),
            expect=2,
        )
        assert "unsupported tradeoff route" in out
        assert "variant.runtime.backend" in out
        assert "VERIFIED TRADEOFF ROUTE: BLOCKED" in out
        assert not unsupported_out.exists()

        tampered_joint = td / "tampered-model-joint.json"
        bad = json.loads(model["joint"].read_text(encoding="utf-8"))
        bad["performance"]["tg_tok_s"]["candidate"] = 999.0
        write(tampered_joint, bad)
        tampered_out = td / "tampered-envelope.json"
        out = run(
            route_args(
                tampered_joint,
                model["bm"],
                model["cm"],
                model["bb"],
                model["cb"],
                model["comparison"],
                model["bq"],
                model["cq"],
                model["baseline_model"],
                model["candidate_model"],
                model["corpus"],
                tampered_out,
            ),
            expect=2,
        )
        assert "I38 model route:" in out
        assert "joint tradeoff artifact does not exactly match" in out
        assert not tampered_out.exists()

    print("UNIFIED TRADEOFF ROUTE SELFTEST: PASS")
    print("- variant.model* auto-routes to I38")
    print("- variant.execution.* auto-routes to I41 and requires variable contract")
    print("- unsupported runtime route is blocked")
    print("- callers cannot force a route with a route argument")
    print("- tampered joint evidence is blocked by the selected underlying verifier")
    print("- envelope is descriptive verification metadata only")


if __name__ == "__main__":
    main()
