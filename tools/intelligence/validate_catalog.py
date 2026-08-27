#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

EVIDENCE_CLASSES = {"OFFICIAL", "MEASURED", "DERIVED", "SECONDARY", "SELLER", "SYNTHETIC"}
PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN", "N/A"}
FILES = ("hardware.jsonl", "models.jsonl", "market.jsonl", "benchmarks.jsonl")


def present(value):
    return str(value if value is not None else "").strip().upper() not in PLACEHOLDERS


def parse_date(value, label, errors):
    try:
        return date.fromisoformat(str(value))
    except Exception:
        errors.append(f"{label}: invalid date {value!r}")
        return None


def load_jsonl(path, errors):
    records = []
    if not path.exists():
        return records
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"{path}:{lineno}: invalid JSON: {e}")
            continue
        if not isinstance(obj, dict):
            errors.append(f"{path}:{lineno}: record must be an object")
            continue
        obj["_location"] = f"{path}:{lineno}"
        records.append(obj)
    return records


def source_ok(record, errors):
    loc = record["_location"]
    src = record.get("source")
    if not isinstance(src, dict):
        errors.append(f"{loc}: missing source object")
        return
    evidence_class = str(src.get("evidence_class", "")).upper()
    if evidence_class not in EVIDENCE_CLASSES:
        errors.append(f"{loc}: invalid source.evidence_class {evidence_class!r}")
    if not (present(src.get("url")) or present(src.get("source_path"))):
        errors.append(f"{loc}: source needs url or source_path")
    if not present(src.get("observed_at")):
        errors.append(f"{loc}: source.observed_at missing")
    else:
        parse_date(src.get("observed_at"), f"{loc} source.observed_at", errors)


def req(record, field, errors):
    if not present(record.get(field)):
        errors.append(f"{record['_location']}: missing {field}")


def positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalog", type=Path)
    p.add_argument("--allow-synthetic", action="store_true")
    p.add_argument("--as-of", default=date.today().isoformat())
    a = p.parse_args()

    errors = []
    warnings = []
    as_of = parse_date(a.as_of, "--as-of", errors)

    records = []
    for name in FILES:
        records.extend(load_jsonl(a.catalog / name, errors))

    ids = {}
    for r in records:
        loc = r["_location"]
        if r.get("schema_version") != 1:
            errors.append(f"{loc}: schema_version must be 1")
        req(r, "record_type", errors)
        req(r, "record_id", errors)
        source_ok(r, errors)

        rid = str(r.get("record_id", "")).strip()
        if rid:
            if rid in ids:
                errors.append(f"{loc}: duplicate record_id {rid!r}; first at {ids[rid]}")
            else:
                ids[rid] = loc

        src_class = str((r.get("source") or {}).get("evidence_class", "")).upper()
        synthetic = bool(r.get("synthetic", False)) or src_class == "SYNTHETIC"
        if synthetic and not a.allow_synthetic:
            errors.append(f"{loc}: synthetic record rejected from production validation")

        if r.get("revalidate_after") is not None and as_of is not None:
            d = parse_date(r.get("revalidate_after"), f"{loc} revalidate_after", errors)
            if d is not None and d < as_of:
                warnings.append(f"{loc}: STALE since {d.isoformat()}")

    hardware = {}
    models = {}

    for r in records:
        t = r.get("record_type")
        loc = r["_location"]

        if t == "hardware":
            for f in ("hardware_id", "canonical_name", "vendor", "accelerator_kind"):
                req(r, f, errors)
            hid = str(r.get("hardware_id", "")).strip()
            if hid and hid != str(r.get("record_id", "")).strip():
                errors.append(f"{loc}: hardware record_id must equal hardware_id")
            if r.get("memory_gib") is not None and not positive_number(r.get("memory_gib")):
                errors.append(f"{loc}: memory_gib must be > 0")
            if hid:
                hardware[hid] = r

        elif t == "model":
            for f in ("model_id", "canonical_name", "repository", "architecture"):
                req(r, f, errors)
            mid = str(r.get("model_id", "")).strip()
            if mid and mid != str(r.get("record_id", "")).strip():
                errors.append(f"{loc}: model record_id must equal model_id")
            if mid:
                models[mid] = r

    for r in records:
        t = r.get("record_type")
        loc = r["_location"]

        if t == "market":
            req(r, "hardware_id", errors)
            if r.get("hardware_id") not in hardware:
                errors.append(f"{loc}: unknown hardware_id {r.get('hardware_id')!r}")
            for f in ("geography", "channel", "cohort", "condition", "price_state", "observed_at"):
                req(r, f, errors)
            if present(r.get("observed_at")):
                parse_date(r.get("observed_at"), f"{loc} observed_at", errors)
            price = r.get("price")
            if not isinstance(price, dict):
                errors.append(f"{loc}: missing price object")
            else:
                if not present(price.get("currency")):
                    errors.append(f"{loc}: price.currency missing")
                if not positive_number(price.get("value")):
                    errors.append(f"{loc}: price.value must be > 0")

        elif t == "benchmark":
            req(r, "hardware_id", errors)
            req(r, "model_id", errors)
            if r.get("hardware_id") not in hardware:
                errors.append(f"{loc}: unknown hardware_id {r.get('hardware_id')!r}")
            if r.get("model_id") not in models:
                errors.append(f"{loc}: unknown model_id {r.get('model_id')!r}")

            artifact = r.get("artifact")
            if not isinstance(artifact, dict):
                errors.append(f"{loc}: missing artifact object")
            else:
                for f in ("sha256", "quant"):
                    if not present(artifact.get(f)):
                        errors.append(f"{loc}: artifact.{f} missing")
                sha = str(artifact.get("sha256", "")).strip()
                if present(sha) and len(sha) != 64:
                    errors.append(f"{loc}: artifact.sha256 must be 64 hex chars")
                if not positive_number(artifact.get("bytes")):
                    errors.append(f"{loc}: artifact.bytes must be > 0")

            runtime = r.get("runtime")
            if not isinstance(runtime, dict):
                errors.append(f"{loc}: missing runtime object")
            else:
                for f in ("name", "runtime_identity", "backend", "build_identity"):
                    if not present(runtime.get(f)):
                        errors.append(f"{loc}: runtime.{f} missing")

            workload = r.get("workload")
            if not isinstance(workload, dict):
                errors.append(f"{loc}: missing workload object")
            else:
                for f in ("pp_tokens", "tg_tokens", "repetitions", "context", "sequences"):
                    if not positive_number(workload.get(f)):
                        errors.append(f"{loc}: workload.{f} must be > 0")

            metrics = r.get("metrics")
            if not isinstance(metrics, dict):
                errors.append(f"{loc}: missing metrics object")
            else:
                vals = [metrics.get("pp_tok_s"), metrics.get("tg_tok_s")]
                if not any(positive_number(x) for x in vals):
                    errors.append(f"{loc}: at least one positive PP/TG metric is required")

            evidence = r.get("evidence")
            if not isinstance(evidence, dict):
                errors.append(f"{loc}: missing evidence object")
            else:
                for f in ("manifest_source", "raw_result_source"):
                    if not present(evidence.get(f)):
                        errors.append(f"{loc}: evidence.{f} missing")
                if not present(evidence.get("packet_source")):
                    warnings.append(f"{loc}: packet_source missing; Experiment 61 packet preferred")

        elif t not in {"hardware", "model", "market", "benchmark"}:
            errors.append(f"{loc}: unknown record_type {t!r}")

    print(f"CATALOG: {a.catalog}")
    print(f"records={len(records)} hardware={len(hardware)} models={len(models)}")
    print("WARNINGS")
    for x in warnings:
        print("- " + x)
    print("ERRORS")
    for x in errors:
        print("- " + x)

    if errors:
        print("VALIDATION: FAIL")
        raise SystemExit(2)

    print("VALIDATION: PASS")


if __name__ == "__main__":
    main()
