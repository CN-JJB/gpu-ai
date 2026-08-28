#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
from datetime import date
from pathlib import Path

from capture_quality_eval import parse_quality_argv
from capture_real_benchmark import extract_model_arg, resolve_recorded_path


PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN", "N/A", "..."}
SESSION_SCHEMA = 1


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_object(path, label):
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"REAL SESSION PREPARE: FAIL\n{label}: invalid JSON: {exc}")
    if not isinstance(obj, dict):
        raise SystemExit(f"REAL SESSION PREPARE: FAIL\n{label}: expected one JSON object")
    return obj


def resolve_path(value, base, label):
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(
            f"REAL SESSION PREPARE: FAIL\nsession field {label} must be a non-empty path string"
        )
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def require_file(path, label):
    if not path.is_file():
        raise SystemExit(f"REAL SESSION PREPARE: FAIL\n{label} is not a file: {path}")


def require_dir(path, label):
    if not path.is_dir():
        raise SystemExit(f"REAL SESSION PREPARE: FAIL\n{label} is not a directory: {path}")


def placeholder(value):
    return str(value if value is not None else "").strip().upper() in PLACEHOLDERS


def dotted_get(obj, dotted):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def load_jsonl(path):
    if not path.is_file():
        return []
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except Exception as exc:
            raise SystemExit(
                f"REAL SESSION PREPARE: FAIL\n{path} line {lineno}: invalid JSON: {exc}"
            )
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def canonical_record(catalog, filename, key, value, allow_synthetic):
    rows = [x for x in load_jsonl(catalog / filename) if x.get(key) == value]
    if len(rows) != 1:
        raise SystemExit(
            f"REAL SESSION PREPARE: FAIL\nexpected exactly one canonical {key}={value!r}, found {len(rows)}"
        )
    row = rows[0]
    if row.get("synthetic", False) and not allow_synthetic:
        raise SystemExit(
            f"REAL SESSION PREPARE: FAIL\nsynthetic canonical {key} requires --allow-synthetic: {value}"
        )
    return row


def require_string(obj, key):
    value = obj.get(key)
    if not isinstance(value, str) or placeholder(value):
        raise SystemExit(
            f"REAL SESSION PREPARE: FAIL\nsession field {key} must be a real non-placeholder string"
        )
    return value.strip()


def require_argv(obj, key):
    value = obj.get(key)
    if not (
        isinstance(value, list)
        and value
        and all(isinstance(x, str) and x != "" for x in value)
    ):
        raise SystemExit(
            f"REAL SESSION PREPARE: FAIL\nsession field {key} must be a non-empty JSON argv list"
        )
    for token in value:
        if token.strip().upper() in PLACEHOLDERS:
            raise SystemExit(
                f"REAL SESSION PREPARE: FAIL\nsession field {key} contains placeholder token {token!r}"
            )
    return list(value)


def validate_semantic_manifest(manifest):
    errors = []

    required = [
        "comparison_id",
        "intentional_variable",
        "variant.hardware.device_identity",
        "variant.runtime.runtime_identity",
        "variant.runtime.backend",
        "variant.runtime.build_identity",
        "variant.model.quant",
        "variant.model.source_revision",
        "variant.execution.gpu_layers",
        "variant.execution.kv_k",
        "variant.execution.kv_v",
        "variant.execution.split_mode",
        "variant.execution.threads",
    ]
    for dotted in required:
        value = dotted_get(manifest, dotted)
        if placeholder(value):
            errors.append(f"semantic field still missing/placeholder: {dotted}")

    for dotted in (
        "fixed.protocol.pp_tokens",
        "fixed.protocol.tg_tokens",
        "fixed.protocol.repetitions",
        "variant.execution.context",
        "variant.execution.sequences",
    ):
        value = dotted_get(manifest, dotted)
        if not (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and value > 0
        ):
            errors.append(f"semantic field must be > 0: {dotted}")

    flash = dotted_get(manifest, "variant.execution.flash_attention")
    if not isinstance(flash, bool):
        errors.append("semantic field must be boolean: variant.execution.flash_attention")

    tensor_split = dotted_get(manifest, "variant.execution.tensor_split")
    if tensor_split is None:
        errors.append("semantic field is missing: variant.execution.tensor_split")
    elif str(tensor_split).strip().upper() in {"TODO", "TBD", "REPLACE", "UNKNOWN", "N/A", "..."}:
        errors.append("semantic field still placeholder: variant.execution.tensor_split")

    return errors


def ensure_empty_dir(path):
    if path.exists():
        if not path.is_dir():
            raise SystemExit(f"REAL SESSION PREPARE: FAIL\nout-dir is not a directory: {path}")
        if any(path.iterdir()):
            raise SystemExit(f"REAL SESSION PREPARE: FAIL\nout-dir is not empty: {path}")
    else:
        path.mkdir(parents=True)


def main():
    p = argparse.ArgumentParser(
        description=(
            "Materialize only byte-derived Experiment 61 identity into a prepared "
            "real-evidence session. Runtime/device/execution semantics are never invented."
        )
    )
    p.add_argument("session", type=Path)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument(
        "--allow-synthetic",
        action="store_true",
        help="Test-only: permit synthetic canonical IDs for the dedicated self-test.",
    )
    a = p.parse_args()

    session_path = a.session.expanduser().resolve()
    require_file(session_path, "session")
    session = load_object(session_path, "session")
    if session.get("real_evidence_session_schema_version") != SESSION_SCHEMA:
        raise SystemExit(
            "REAL SESSION PREPARE: FAIL\nreal_evidence_session_schema_version must be 1"
        )

    base = session_path.parent
    working_directory = resolve_path(
        session.get("working_directory", "."), base, "working_directory"
    )
    require_dir(working_directory, "working_directory")
    catalog = resolve_path(session.get("catalog"), base, "catalog")
    require_dir(catalog, "catalog")

    manifest_path = resolve_path(session.get("manifest"), base, "manifest")
    model = resolve_path(session.get("model_artifact"), base, "model_artifact")
    profile = resolve_path(session.get("hardware_profile"), base, "hardware_profile")
    prompt = resolve_path(session.get("prompt_manifest"), base, "prompt_manifest")
    corpus = resolve_path(session.get("quality_corpus"), base, "quality_corpus")
    quality_identity_path = resolve_path(
        session.get("quality_identity"), base, "quality_identity"
    )
    for label, path in (
        ("manifest", manifest_path),
        ("model_artifact", model),
        ("hardware_profile", profile),
        ("prompt_manifest", prompt),
        ("quality_corpus", corpus),
        ("quality_identity", quality_identity_path),
    ):
        require_file(path, label)

    hardware_id = require_string(session, "hardware_id")
    model_id = require_string(session, "model_id")
    runtime_id = require_string(session, "runtime_id")
    observed_at = require_string(session, "observed_at")
    try:
        date.fromisoformat(observed_at)
    except ValueError:
        raise SystemExit(
            f"REAL SESSION PREPARE: FAIL\nobserved_at must be YYYY-MM-DD: {observed_at!r}"
        )

    canonical_record(
        catalog, "hardware.jsonl", "hardware_id", hardware_id, a.allow_synthetic
    )
    canonical_record(
        catalog, "models.jsonl", "model_id", model_id, a.allow_synthetic
    )
    canonical_record(
        catalog, "runtimes.jsonl", "runtime_id", runtime_id, a.allow_synthetic
    )

    benchmark_argv = require_argv(session, "benchmark_argv")
    quality_argv = require_argv(session, "quality_argv")

    try:
        benchmark_model = extract_model_arg(benchmark_argv)
    except SystemExit as exc:
        raise SystemExit(
            "REAL SESSION PREPARE: FAIL\nbenchmark argv model binding is invalid: "
            + str(exc)
        )
    if resolve_recorded_path(benchmark_model, working_directory) != model:
        raise SystemExit(
            "REAL SESSION PREPARE: FAIL\nbenchmark argv model path does not match model_artifact"
        )

    try:
        quality_model, quality_corpus, executed_eval_args = parse_quality_argv(
            quality_argv
        )
    except ValueError as exc:
        raise SystemExit(f"REAL SESSION PREPARE: FAIL\nquality argv: {exc}")
    if resolve_recorded_path(quality_model, working_directory) != model:
        raise SystemExit(
            "REAL SESSION PREPARE: FAIL\nquality argv model path does not match model_artifact"
        )
    if resolve_recorded_path(quality_corpus, working_directory) != corpus:
        raise SystemExit(
            "REAL SESSION PREPARE: FAIL\nquality argv corpus path does not match quality_corpus"
        )

    manifest = load_object(manifest_path, "manifest")
    quality_identity = load_object(quality_identity_path, "quality identity")
    prompt_identity = load_object(prompt, "prompt manifest")

    if manifest.get("schema_version") != 1:
        raise SystemExit("REAL SESSION PREPARE: FAIL\nmanifest schema_version must be 1")
    if quality_identity.get("quality_identity_schema_version") != 2:
        raise SystemExit(
            "REAL SESSION PREPARE: FAIL\nquality_identity_schema_version must be 2"
        )

    for field in ("tokenizer_identity", "fixture_revision"):
        if placeholder(quality_identity.get(field)):
            raise SystemExit(
                f"REAL SESSION PREPARE: FAIL\nquality identity {field} must be explicitly filled"
            )

    declared_eval_args = quality_identity.get("evaluation_args")
    if not (
        isinstance(declared_eval_args, list)
        and all(isinstance(x, str) and x != "" for x in declared_eval_args)
    ):
        raise SystemExit(
            "REAL SESSION PREPARE: FAIL\nquality identity evaluation_args must be a JSON list of non-empty strings"
        )
    if executed_eval_args != declared_eval_args:
        raise SystemExit(
            "REAL SESSION PREPARE: FAIL\nquality argv evaluation args do not exactly match quality identity"
        )

    prompt_fields = (
        "messages_sha256",
        "chat_template_sha256",
        "rendered_sha256",
        "token_ids_sha256",
        "token_count",
    )
    for field in prompt_fields:
        if field not in prompt_identity:
            raise SystemExit(
                f"REAL SESSION PREPARE: FAIL\nprompt manifest missing {field}"
            )
    for field in prompt_fields[:-1]:
        if placeholder(prompt_identity.get(field)):
            raise SystemExit(
                f"REAL SESSION PREPARE: FAIL\nprompt manifest {field} is placeholder"
            )
    if not (
        isinstance(prompt_identity.get("token_count"), int)
        and prompt_identity["token_count"] > 0
    ):
        raise SystemExit(
            "REAL SESSION PREPARE: FAIL\nprompt manifest token_count must be a positive integer"
        )

    prepared_manifest = copy.deepcopy(manifest)
    prepared_identity = copy.deepcopy(quality_identity)

    corpus_sha = sha256_file(corpus)
    prepared_identity["corpus_sha256"] = corpus_sha

    prepared_manifest.setdefault("fixed", {}).setdefault("quality_eval", {})
    prepared_manifest["fixed"]["quality_eval"] = {
        "tokenizer_identity": prepared_identity["tokenizer_identity"],
        "corpus_sha256": corpus_sha,
        "fixture_revision": prepared_identity["fixture_revision"],
        "evaluation_args": copy.deepcopy(prepared_identity["evaluation_args"]),
    }

    prepared_manifest.setdefault("variant", {}).setdefault("hardware", {})
    prepared_manifest["variant"]["hardware"]["profile_sha256"] = sha256_file(profile)

    prepared_manifest["variant"].setdefault("model", {})
    prepared_manifest["variant"]["model"]["artifact_sha256"] = sha256_file(model)
    prepared_manifest["variant"]["model"]["artifact_bytes"] = model.stat().st_size

    prepared_manifest["variant"]["prompt"] = {
        field: copy.deepcopy(prompt_identity[field]) for field in prompt_fields
    }

    semantic_errors = validate_semantic_manifest(prepared_manifest)
    if semantic_errors:
        print("REAL SESSION PREPARE")
        print("SEMANTIC FIELDS STILL REQUIRED")
        for error in semantic_errors:
            print("- " + error)
        print("REAL SESSION PREPARE: BLOCKED")
        raise SystemExit(2)

    out_dir = a.out_dir.expanduser().resolve()
    ensure_empty_dir(out_dir)

    manifest_out = out_dir / "manifest.json"
    identity_out = out_dir / "quality-identity.json"
    session_out = out_dir / "session.json"
    report_out = out_dir / "preflight.json"

    manifest_out.write_text(
        json.dumps(prepared_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    identity_out.write_text(
        json.dumps(prepared_identity, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    prepared_session = copy.deepcopy(session)
    prepared_session.update(
        {
            "working_directory": str(working_directory),
            "catalog": str(catalog),
            "manifest": str(manifest_out),
            "model_artifact": str(model),
            "hardware_profile": str(profile),
            "prompt_manifest": str(prompt),
            "quality_corpus": str(corpus),
            "quality_identity": str(identity_out),
            "hardware_id": hardware_id,
            "model_id": model_id,
            "runtime_id": runtime_id,
            "observed_at": observed_at,
            "benchmark_argv": benchmark_argv,
            "quality_argv": quality_argv,
        }
    )
    session_out.write_text(
        json.dumps(prepared_session, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    report = {
        "real_evidence_preflight_schema_version": 1,
        "status": "READY-TO-RUN-I52",
        "source_session": str(session_path),
        "prepared_session": str(session_out),
        "materialized_fields": {
            "variant.hardware.profile_sha256": prepared_manifest["variant"]["hardware"]["profile_sha256"],
            "variant.model.artifact_sha256": prepared_manifest["variant"]["model"]["artifact_sha256"],
            "variant.model.artifact_bytes": prepared_manifest["variant"]["model"]["artifact_bytes"],
            "fixed.quality_eval": prepared_manifest["fixed"]["quality_eval"],
            "variant.prompt": prepared_manifest["variant"]["prompt"],
            "quality_identity.corpus_sha256": corpus_sha,
        },
        "semantic_fields_preserved": [
            "comparison_id",
            "intentional_variable",
            "variant.hardware.device_identity",
            "variant.runtime.*",
            "variant.model.quant",
            "variant.model.source_revision",
            "variant.execution.*",
        ],
        "boundary": (
            "READY-TO-RUN-I52 means local byte-derived identity and explicit semantic "
            "fields are prepared. No benchmark or quality metric has been produced."
        ),
    }
    report_out.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("REAL SESSION PREPARE")
    print(f"prepared_manifest={manifest_out}")
    print(f"prepared_quality_identity={identity_out}")
    print(f"prepared_session={session_out}")
    print(f"preflight={report_out}")
    print("REAL SESSION PREPARE: READY-TO-RUN-I52")
    print(
        "Only byte-derived identity was materialized. Runtime/device/model-source/"
        "execution semantics were preserved from explicit input and never inferred."
    )


if __name__ == "__main__":
    main()
