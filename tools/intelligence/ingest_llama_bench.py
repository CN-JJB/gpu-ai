#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN"}


def present(value):
    return str(value if value is not None else "").strip().upper() not in PLACEHOLDERS


def load_rows(path):
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        rows = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            rows.extend(obj if isinstance(obj, list) else [obj])
        return rows


def kind(row):
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


def extract_metrics(path):
    vals = {}
    for row in load_rows(path):
        k = kind(row)
        if k and isinstance(row.get("avg_ts"), (int, float)) and row["avg_ts"] > 0:
            vals.setdefault(k, []).append(float(row["avg_ts"]))
    return {
        "pp_tok_s": (sum(vals["PP"]) / len(vals["PP"])) if vals.get("PP") else None,
        "tg_tok_s": (sum(vals["TG"]) / len(vals["TG"])) if vals.get("TG") else None,
    }


def need(obj, path):
    cur = obj
    for part in path.split("."):
        if not isinstance(cur, dict):
            raise SystemExit(f"manifest missing {path}")
        cur = cur.get(part)
    if not present(cur):
        raise SystemExit(f"manifest missing/placeholder {path}")
    return cur


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--result", type=Path, required=True)
    p.add_argument("--hardware-id", required=True)
    p.add_argument("--model-id", required=True)
    p.add_argument("--record-id", required=True)
    p.add_argument("--observed-at", required=True)
    p.add_argument("--packet-source", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--append", action="store_true")
    p.add_argument("--synthetic", action="store_true")
    a = p.parse_args()

    manifest = json.loads(a.manifest.read_text(encoding="utf-8"))
    fixed = manifest.get("fixed", {})
    protocol = fixed.get("protocol", {})
    variant = manifest.get("variant", {})
    hardware = variant.get("hardware", {})
    runtime = variant.get("runtime", {})
    model = variant.get("model", {})
    execution = variant.get("execution", {})
    prompt = variant.get("prompt", {})

    need(manifest, "variant.hardware.device_identity")
    need(manifest, "variant.hardware.profile_sha256")
    need(manifest, "variant.runtime.runtime_identity")
    need(manifest, "variant.runtime.backend")
    need(manifest, "variant.runtime.build_identity")
    need(manifest, "variant.model.artifact_sha256")
    need(manifest, "variant.model.quant")
    need(manifest, "variant.model.source_revision")

    artifact_bytes = model.get("artifact_bytes")
    if not isinstance(artifact_bytes, (int, float)) or artifact_bytes <= 0:
        raise SystemExit("manifest variant.model.artifact_bytes must be > 0")

    for name in ("pp_tokens", "tg_tokens", "repetitions"):
        if not isinstance(protocol.get(name), (int, float)) or protocol[name] <= 0:
            raise SystemExit(f"manifest fixed.protocol.{name} must be > 0")

    for name in ("context", "sequences"):
        if not isinstance(execution.get(name), (int, float)) or execution[name] <= 0:
            raise SystemExit(f"manifest variant.execution.{name} must be > 0")

    metrics = extract_metrics(a.result)
    if metrics["pp_tok_s"] is None and metrics["tg_tok_s"] is None:
        raise SystemExit("raw result contains no positive PP/TG avg_ts metrics")

    source_class = "SYNTHETIC" if a.synthetic else "MEASURED"

    record = {
        "schema_version": 1,
        "record_type": "benchmark",
        "record_id": a.record_id,
        "hardware_id": a.hardware_id,
        "model_id": a.model_id,
        "observed_at": a.observed_at,
        "artifact": {
            "sha256": model["artifact_sha256"],
            "bytes": int(artifact_bytes),
            "quant": model["quant"],
            "source_revision": model["source_revision"],
        },
        "runtime": {
            "name": str(runtime.get("runtime_identity")).split()[0],
            "runtime_identity": runtime["runtime_identity"],
            "backend": runtime["backend"],
            "build_identity": runtime["build_identity"],
        },
        "hardware_evidence": {
            "device_identity": hardware["device_identity"],
            "profile_sha256": hardware["profile_sha256"],
        },
        "workload": {
            "pp_tokens": int(protocol["pp_tokens"]),
            "tg_tokens": int(protocol["tg_tokens"]),
            "repetitions": int(protocol["repetitions"]),
            "warmup_runs": int(protocol.get("warmup_runs", 0) or 0),
            "context": int(execution["context"]),
            "sequences": int(execution["sequences"]),
            "gpu_layers": execution.get("gpu_layers"),
            "flash_attention": execution.get("flash_attention"),
            "kv_k": execution.get("kv_k"),
            "kv_v": execution.get("kv_v"),
            "split_mode": execution.get("split_mode"),
            "tensor_split": execution.get("tensor_split"),
            "threads": execution.get("threads"),
            "prompt_token_ids_sha256": prompt.get("token_ids_sha256"),
        },
        "metrics": metrics,
        "evidence": {
            "manifest_source": str(a.manifest),
            "raw_result_source": str(a.result),
            "packet_source": a.packet_source,
        },
        "source": {
            "evidence_class": source_class,
            "source_path": str(a.result),
            "observed_at": a.observed_at,
        },
        "synthetic": bool(a.synthetic),
    }

    text = json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
    mode = "a" if a.append else "w"
    with a.out.open(mode, encoding="utf-8") as f:
        f.write(text)

    print(f"wrote {a.record_id} to {a.out}")
    print(f"PP={metrics['pp_tok_s']} TG={metrics['tg_tok_s']}")
    print("Review before appending to the production intelligence catalog.")


if __name__ == "__main__":
    main()
