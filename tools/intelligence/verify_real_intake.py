#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN", "N/A"}


def present(value):
    return str(value if value is not None else "").strip().upper() not in PLACEHOLDERS


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path):
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def need(obj, dotted, errors):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict):
            errors.append(f"manifest missing {dotted}")
            return None
        cur = cur.get(part)
    if not present(cur):
        errors.append(f"manifest missing/placeholder {dotted}")
    return cur


def positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def load_result_rows(path):
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        rows = []
        for line in text.splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            rows.extend(obj if isinstance(obj, list) else [obj])
        return rows


def result_kind(row):
    test = str(row.get("test", "")).lower()
    nprompt = row.get("n_prompt")
    ngen = row.get("n_gen")
    if test.startswith("pp") or (
        isinstance(nprompt, (int, float)) and nprompt > 0 and (not ngen or ngen == 0)
    ):
        return "PP"
    if test.startswith("tg") or (
        isinstance(ngen, (int, float)) and ngen > 0 and (not nprompt or nprompt == 0)
    ):
        return "TG"
    return None


def packet_match(packet, path):
    digest = sha256(path)
    size = path.stat().st_size
    matches = []
    for item in packet.get("files", []):
        if not isinstance(item, dict):
            continue
        if item.get("sha256") == digest:
            matches.append(item)

    if not matches:
        return False, f"{path}: SHA256 not indexed by packet"

    for item in matches:
        if item.get("bytes") == size:
            return True, None

    return False, f"{path}: packet SHA matches but byte count does not"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalog", type=Path)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--result", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--hardware-id", required=True)
    p.add_argument("--model-id", required=True)
    p.add_argument("--runtime-id", required=True)
    p.add_argument("--observed-at", required=True)
    p.add_argument("--allow-synthetic", action="store_true")
    a = p.parse_args()

    errors = []

    hardware = {x["hardware_id"]: x for x in load_jsonl(a.catalog / "hardware.jsonl")}
    models = {x["model_id"]: x for x in load_jsonl(a.catalog / "models.jsonl")}
    runtimes = {x["runtime_id"]: x for x in load_jsonl(a.catalog / "runtimes.jsonl")}

    for label, value, table in (
        ("hardware_id", a.hardware_id, hardware),
        ("model_id", a.model_id, models),
        ("runtime_id", a.runtime_id, runtimes),
    ):
        if value not in table:
            errors.append(f"unknown {label}: {value}")
        elif table[value].get("synthetic", False) and not a.allow_synthetic:
            errors.append(f"synthetic {label} requires --allow-synthetic: {value}")

    for label, path in (
        ("manifest", a.manifest),
        ("result", a.result),
        ("packet", a.packet),
    ):
        if not path.is_file():
            errors.append(f"{label} is not a file: {path}")

    manifest = {}
    packet = {}
    if a.manifest.is_file():
        try:
            manifest = json.loads(a.manifest.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"invalid manifest JSON: {e}")

    if a.packet.is_file():
        try:
            packet = json.loads(a.packet.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"invalid packet JSON: {e}")

    required_manifest = (
        "variant.hardware.device_identity",
        "variant.hardware.profile_sha256",
        "variant.runtime.runtime_identity",
        "variant.runtime.backend",
        "variant.runtime.build_identity",
        "variant.model.artifact_sha256",
        "variant.model.quant",
        "variant.model.source_revision",
        "variant.prompt.token_ids_sha256",
        "fixed.quality_eval.tokenizer_identity",
        "fixed.quality_eval.corpus_sha256",
        "fixed.quality_eval.fixture_revision",
    )
    for field in required_manifest:
        need(manifest, field, errors)

    artifact_bytes = (
        manifest.get("variant", {})
        .get("model", {})
        .get("artifact_bytes")
    )
    if not positive_number(artifact_bytes):
        errors.append("manifest variant.model.artifact_bytes must be > 0")

    protocol = manifest.get("fixed", {}).get("protocol", {})
    for field in ("pp_tokens", "tg_tokens", "repetitions"):
        if not positive_number(protocol.get(field)):
            errors.append(f"manifest fixed.protocol.{field} must be > 0")

    execution = manifest.get("variant", {}).get("execution", {})
    for field in ("context", "sequences"):
        if not positive_number(execution.get(field)):
            errors.append(f"manifest variant.execution.{field} must be > 0")

    positive_metrics = []
    if a.result.is_file():
        try:
            for row in load_result_rows(a.result):
                kind = result_kind(row)
                avg = row.get("avg_ts")
                if kind and positive_number(avg):
                    positive_metrics.append((kind, float(avg)))
        except Exception as e:
            errors.append(f"invalid raw result: {e}")

    if not positive_metrics:
        errors.append("raw result contains no positive PP/TG avg_ts")

    if packet:
        if packet.get("packet_schema_version") != 1:
            errors.append("packet_schema_version must be 1")
        if not isinstance(packet.get("files"), list):
            errors.append("packet.files must be a list")
        else:
            for path in (a.manifest, a.result):
                if path.is_file():
                    ok, message = packet_match(packet, path)
                    if not ok:
                        errors.append(message)

    print("REAL BENCHMARK INTAKE")
    print(f"hardware_id={a.hardware_id}")
    print(f"model_id={a.model_id}")
    print(f"runtime_id={a.runtime_id}")
    print(f"observed_at={a.observed_at}")
    print("METRICS")
    for kind, value in positive_metrics:
        print(f"- {kind}={value}")

    print("ERRORS")
    for x in errors:
        print("- " + x)

    if errors:
        print("INTAKE: BLOCKED")
        raise SystemExit(2)

    print("INTAKE: READY")
    print("Next: run ingest_llama_bench.py, validate the catalog diff, then derive exact measured compatibility.")
    print("READY is an evidence-completeness gate, not a benchmark-truth or purchase claim.")


if __name__ == "__main__":
    main()
