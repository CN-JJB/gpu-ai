#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

from verify_quality_execution import verify_quality_execution_evidence

PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN", "N/A"}
RAW_SHARED_FIELDS = (
    "build_commit",
    "gpu_info",
    "backends",
    "model_size",
    "n_threads",
    "type_k",
    "type_v",
    "n_gpu_layers",
    "split_mode",
    "flash_attn",
    "tensor_split",
)


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


def norm_text(value):
    return " ".join(str(value if value is not None else "").strip().lower().split())


def int_like(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    try:
        text = str(value).strip()
        if text:
            return int(text)
    except Exception:
        pass
    return None


def bool_like(value):
    if isinstance(value, bool):
        return value
    if value in (0, 1):
        return bool(value)
    text = norm_text(value)
    if text in {"0", "false", "off", "no"}:
        return False
    if text in {"1", "true", "on", "yes"}:
        return True
    return None


def gpu_layers_match(manifest_value, raw_value):
    raw_int = int_like(raw_value)
    m = norm_text(manifest_value)
    if m in {"all", "-1"}:
        return raw_int == -1
    manifest_int = int_like(manifest_value)
    return manifest_int is not None and raw_int == manifest_int


def tensor_split_match(manifest_value, raw_value):
    m = norm_text(manifest_value).replace(" ", "")
    r = norm_text(raw_value).replace(" ", "")
    if m == r:
        return True
    zeroish = {"", "0", "0.0", "0.00", "none"}
    return m in zeroish and r in zeroish


def text_identity_match(manifest_value, raw_value):
    m = norm_text(manifest_value)
    r = norm_text(raw_value)
    return bool(m and r and (m == r or m in r or r in m))


def extract_model_arg(argv):
    if not isinstance(argv, list) or not all(isinstance(x, str) for x in argv):
        raise ValueError("command argv must be a list of strings")

    matches = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("-m", "--model"):
            if i + 1 >= len(argv):
                raise ValueError(f"{arg} is missing its model path")
            matches.append(argv[i + 1])
            i += 2
            continue
        if arg.startswith("--model="):
            matches.append(arg.split("=", 1)[1])
        i += 1

    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one -m/--model path in command argv; found {len(matches)}"
        )
    return matches[0]


def resolve_recorded_path(value, cwd):
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path(cwd) / path
    return path.resolve()


def raw_protocol_rows(rows, protocol, errors):
    pp_tokens = int_like(protocol.get("pp_tokens"))
    tg_tokens = int_like(protocol.get("tg_tokens"))
    selected = {"PP": [], "TG": []}

    for row in rows:
        if not isinstance(row, dict):
            continue
        kind = result_kind(row)
        if kind == "PP":
            if int_like(row.get("n_prompt")) == pp_tokens and int_like(row.get("n_gen") or 0) == 0:
                selected["PP"].append(row)
        elif kind == "TG":
            if int_like(row.get("n_gen")) == tg_tokens and int_like(row.get("n_prompt") or 0) == 0:
                selected["TG"].append(row)

    if not selected["PP"]:
        errors.append(f"raw result missing PP row for n_prompt={pp_tokens}")
    if not selected["TG"]:
        errors.append(f"raw result missing TG row for n_gen={tg_tokens}")

    if len(selected["PP"]) > 1:
        errors.append(f"raw result has multiple PP rows for n_prompt={pp_tokens}; expected one protocol row")
    if len(selected["TG"]) > 1:
        errors.append(f"raw result has multiple TG rows for n_gen={tg_tokens}; expected one protocol row")

    pp = [selected["PP"][0]] if len(selected["PP"]) == 1 else []
    tg = [selected["TG"][0]] if len(selected["TG"]) == 1 else []
    return pp, tg


def require_raw_fields(rows, errors):
    for label, row in rows:
        for field in RAW_SHARED_FIELDS:
            if row.get(field) is None or str(row.get(field)).strip() == "":
                errors.append(f"raw {label} row missing {field}")
        samples = row.get("samples_ts")
        if not isinstance(samples, list) or not samples:
            errors.append(f"raw {label} row missing non-empty samples_ts")


def cross_check_raw_identity(manifest, rows, errors):
    fixed = manifest.get("fixed", {})
    protocol = fixed.get("protocol", {})
    variant = manifest.get("variant", {})
    hardware = variant.get("hardware", {})
    runtime = variant.get("runtime", {})
    model = variant.get("model", {})
    execution = variant.get("execution", {})

    pp_rows, tg_rows = raw_protocol_rows(rows, protocol, errors)
    selected = []
    if pp_rows:
        selected.append(("PP", pp_rows[0]))
    if tg_rows:
        selected.append(("TG", tg_rows[0]))
    if len(selected) != 2:
        return

    require_raw_fields(selected, errors)

    pp = selected[0][1]
    tg = selected[1][1]
    for field in RAW_SHARED_FIELDS:
        if field in pp and field in tg and pp.get(field) != tg.get(field):
            errors.append(
                f"raw PP/TG identity mismatch for {field}: {pp.get(field)!r} vs {tg.get(field)!r}"
            )

    for label, row in selected:
        if row.get("gpu_info") is not None and not text_identity_match(
            hardware.get("device_identity"), row.get("gpu_info")
        ):
            errors.append(
                f"raw {label} gpu_info does not match manifest device_identity: "
                f"{row.get('gpu_info')!r} vs {hardware.get('device_identity')!r}"
            )

        backend = norm_text(runtime.get("backend"))
        raw_backends = norm_text(row.get("backends"))
        if backend and raw_backends and backend not in raw_backends:
            errors.append(
                f"raw {label} backends does not contain manifest backend: "
                f"{row.get('backends')!r} vs {runtime.get('backend')!r}"
            )

        commit = norm_text(row.get("build_commit"))
        runtime_identity = norm_text(runtime.get("runtime_identity"))
        build_identity = norm_text(runtime.get("build_identity"))
        if commit and commit not in runtime_identity and commit not in build_identity:
            errors.append(
                f"raw {label} build_commit is absent from manifest runtime/build identity: "
                f"{row.get('build_commit')!r}"
            )

        if int_like(row.get("model_size")) != int_like(model.get("artifact_bytes")):
            errors.append(
                f"raw {label} model_size != manifest artifact_bytes: "
                f"{row.get('model_size')!r} vs {model.get('artifact_bytes')!r}"
            )

        if int_like(row.get("n_threads")) != int_like(execution.get("threads")):
            errors.append(
                f"raw {label} n_threads != manifest execution.threads: "
                f"{row.get('n_threads')!r} vs {execution.get('threads')!r}"
            )

        if norm_text(row.get("type_k")) != norm_text(execution.get("kv_k")):
            errors.append(
                f"raw {label} type_k != manifest execution.kv_k: "
                f"{row.get('type_k')!r} vs {execution.get('kv_k')!r}"
            )
        if norm_text(row.get("type_v")) != norm_text(execution.get("kv_v")):
            errors.append(
                f"raw {label} type_v != manifest execution.kv_v: "
                f"{row.get('type_v')!r} vs {execution.get('kv_v')!r}"
            )

        if not gpu_layers_match(execution.get("gpu_layers"), row.get("n_gpu_layers")):
            errors.append(
                f"raw {label} n_gpu_layers != manifest execution.gpu_layers: "
                f"{row.get('n_gpu_layers')!r} vs {execution.get('gpu_layers')!r}"
            )

        if norm_text(row.get("split_mode")) != norm_text(execution.get("split_mode")):
            errors.append(
                f"raw {label} split_mode != manifest execution.split_mode: "
                f"{row.get('split_mode')!r} vs {execution.get('split_mode')!r}"
            )

        raw_fa = bool_like(row.get("flash_attn"))
        manifest_fa = bool_like(execution.get("flash_attention"))
        if raw_fa is None or manifest_fa is None or raw_fa != manifest_fa:
            errors.append(
                f"raw {label} flash_attn != manifest execution.flash_attention: "
                f"{row.get('flash_attn')!r} vs {execution.get('flash_attention')!r}"
            )

        if not tensor_split_match(execution.get("tensor_split"), row.get("tensor_split")):
            errors.append(
                f"raw {label} tensor_split != manifest execution.tensor_split: "
                f"{row.get('tensor_split')!r} vs {execution.get('tensor_split')!r}"
            )

        samples = row.get("samples_ts")
        repetitions = int_like(protocol.get("repetitions"))
        if isinstance(samples, list) and repetitions is not None and len(samples) != repetitions:
            errors.append(
                f"raw {label} samples_ts count != manifest repetitions: "
                f"{len(samples)} vs {repetitions}"
            )


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
    p.add_argument("--model-artifact", type=Path, help="Local model artifact to hash/size-check against the manifest")
    p.add_argument("--hardware-profile", type=Path, help="Hardware profile artifact to SHA-check against manifest variant.hardware.profile_sha256")
    p.add_argument("--prompt-manifest", type=Path, help="Experiment 57 prompt evidence manifest to bind variant.prompt identity")
    p.add_argument("--quality-corpus", type=Path, help="Quality-evaluation corpus to SHA-check against fixed.quality_eval.corpus_sha256")
    p.add_argument("--quality-manifest", type=Path, help="Experiment 59 quality identity manifest to bind fixed.quality_eval identity")
    p.add_argument("--command-record", type=Path, help="I21 command.json to bind exact argv to the verified model artifact")
    p.add_argument("--quality-command-record", type=Path, help="I28 quality-command.json for executed quality evidence")
    p.add_argument("--quality-stdout", type=Path, help="I28 raw quality stdout.txt")
    p.add_argument("--quality-stderr", type=Path, help="I28 raw quality stderr.txt")
    p.add_argument("--quality-packet", type=Path, help="I28 quality PACKET.json")
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

    hardware_record = hardware.get(a.hardware_id)
    profile_status = "NOT-CHECKED"
    profile_actual_sha256 = None
    profile_actual_bytes = None
    if a.hardware_profile is not None:
        if not a.hardware_profile.is_file():
            errors.append(f"hardware profile is not a file: {a.hardware_profile}")
            profile_status = "BLOCKED"
        else:
            profile_actual_bytes = a.hardware_profile.stat().st_size
            profile_actual_sha256 = sha256(a.hardware_profile)
            expected_profile_sha256 = str(
                manifest.get("variant", {})
                .get("hardware", {})
                .get("profile_sha256", "")
            ).strip().lower()

            if expected_profile_sha256 and profile_actual_sha256.lower() != expected_profile_sha256:
                errors.append(
                    "hardware profile SHA256 != manifest variant.hardware.profile_sha256: "
                    f"{profile_actual_sha256} vs {expected_profile_sha256}"
                )
                profile_status = "BLOCKED"

            if profile_status != "BLOCKED":
                profile_status = "PASS"
    elif hardware_record is not None and hardware_record.get("synthetic", False):
        if a.allow_synthetic:
            profile_status = "SKIPPED-SYNTHETIC"
    elif hardware_record is not None:
        errors.append(
            "non-synthetic hardware intake requires --hardware-profile so manifest profile_sha256 has a real artifact"
        )
        profile_status = "BLOCKED"

    model_record = models.get(a.model_id)
    quality_corpus_status = "NOT-CHECKED"
    quality_corpus_sha256 = None
    quality_corpus_bytes = None
    if a.quality_corpus is not None:
        if not a.quality_corpus.is_file():
            errors.append(f"quality corpus is not a file: {a.quality_corpus}")
            quality_corpus_status = "BLOCKED"
        else:
            quality_corpus_bytes = a.quality_corpus.stat().st_size
            quality_corpus_sha256 = sha256(a.quality_corpus)
            expected_corpus_sha256 = str(
                manifest.get("fixed", {})
                .get("quality_eval", {})
                .get("corpus_sha256", "")
            ).strip().lower()

            if expected_corpus_sha256 and quality_corpus_sha256.lower() != expected_corpus_sha256:
                errors.append(
                    "quality corpus SHA256 != manifest fixed.quality_eval.corpus_sha256: "
                    f"{quality_corpus_sha256} vs {expected_corpus_sha256}"
                )
                quality_corpus_status = "BLOCKED"

            if quality_corpus_status != "BLOCKED":
                quality_corpus_status = "PASS"
    elif model_record is not None and model_record.get("synthetic", False):
        if a.allow_synthetic:
            quality_corpus_status = "SKIPPED-SYNTHETIC"
    elif model_record is not None:
        errors.append(
            "non-synthetic intake requires --quality-corpus so fixed.quality_eval.corpus_sha256 has a real artifact"
        )
        quality_corpus_status = "BLOCKED"

    quality_identity_status = "NOT-CHECKED"
    quality_identity_obj = {}
    if a.quality_manifest is not None:
        if not a.quality_manifest.is_file():
            errors.append(f"quality manifest is not a file: {a.quality_manifest}")
            quality_identity_status = "BLOCKED"
        else:
            try:
                quality_identity_obj = json.loads(a.quality_manifest.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"invalid quality manifest JSON: {exc}")
                quality_identity_status = "BLOCKED"

            if quality_identity_obj and not isinstance(quality_identity_obj, dict):
                errors.append("quality manifest must be one JSON object")
                quality_identity_status = "BLOCKED"
                quality_identity_obj = {}

            if quality_identity_obj:
                if quality_identity_obj.get("quality_identity_schema_version") != 2:
                    errors.append("quality_identity_schema_version must be 2")
                    quality_identity_status = "BLOCKED"

                for field in (
                    "tokenizer_identity",
                    "corpus_sha256",
                    "fixture_revision",
                ):
                    if not present(quality_identity_obj.get(field)):
                        errors.append(f"quality manifest missing/placeholder {field}")
                        quality_identity_status = "BLOCKED"

                evaluation_args = quality_identity_obj.get("evaluation_args")
                if not (
                    isinstance(evaluation_args, list)
                    and all(
                        isinstance(item, str) and item != ""
                        for item in evaluation_args
                    )
                ):
                    errors.append(
                        "quality manifest evaluation_args must be a JSON list "
                        "of non-empty strings"
                    )
                    quality_identity_status = "BLOCKED"

                manifest_quality = manifest.get("fixed", {}).get("quality_eval", {})
                for field in (
                    "tokenizer_identity",
                    "corpus_sha256",
                    "fixture_revision",
                    "evaluation_args",
                ):
                    expected = manifest_quality.get(field)
                    actual = quality_identity_obj.get(field)
                    if actual != expected:
                        errors.append(
                            f"quality manifest {field} != Experiment 61 manifest: "
                            f"{actual!r} vs {expected!r}"
                        )
                        quality_identity_status = "BLOCKED"

                if quality_identity_status != "BLOCKED":
                    quality_identity_status = "PASS"
    elif model_record is not None and model_record.get("synthetic", False):
        if a.allow_synthetic:
            quality_identity_status = "SKIPPED-SYNTHETIC"
    elif model_record is not None:
        errors.append(
            "non-synthetic intake requires --quality-manifest so fixed.quality_eval identity has a machine-readable evidence artifact"
        )
        quality_identity_status = "BLOCKED"

    prompt_status = "NOT-CHECKED"
    prompt_obj = {}
    if a.prompt_manifest is not None:
        if not a.prompt_manifest.is_file():
            errors.append(f"prompt manifest is not a file: {a.prompt_manifest}")
            prompt_status = "BLOCKED"
        else:
            try:
                prompt_obj = json.loads(a.prompt_manifest.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"invalid prompt manifest JSON: {exc}")
                prompt_status = "BLOCKED"

            if prompt_obj and not isinstance(prompt_obj, dict):
                errors.append("prompt manifest must be one JSON object")
                prompt_status = "BLOCKED"
                prompt_obj = {}

            if prompt_obj:
                manifest_prompt = manifest.get("variant", {}).get("prompt", {})
                for field in (
                    "messages_sha256",
                    "chat_template_sha256",
                    "rendered_sha256",
                    "token_ids_sha256",
                    "token_count",
                ):
                    expected = manifest_prompt.get(field)
                    actual = prompt_obj.get(field)
                    if actual != expected:
                        errors.append(
                            f"prompt manifest {field} != Experiment 61 manifest: "
                            f"{actual!r} vs {expected!r}"
                        )
                        prompt_status = "BLOCKED"
                if prompt_status != "BLOCKED":
                    prompt_status = "PASS"
    elif model_record is not None and model_record.get("synthetic", False):
        if a.allow_synthetic:
            prompt_status = "SKIPPED-SYNTHETIC"
    elif model_record is not None:
        errors.append(
            "non-synthetic intake requires --prompt-manifest so variant.prompt identity is backed by Experiment 57 evidence"
        )
        prompt_status = "BLOCKED"

    artifact_status = "NOT-CHECKED"
    artifact_actual_sha256 = None
    artifact_actual_bytes = None
    if a.model_artifact is not None:
        if not a.model_artifact.is_file():
            errors.append(f"model artifact is not a file: {a.model_artifact}")
            artifact_status = "BLOCKED"
        else:
            artifact_actual_bytes = a.model_artifact.stat().st_size
            artifact_actual_sha256 = sha256(a.model_artifact)
            expected_sha256 = str(
                manifest.get("variant", {})
                .get("model", {})
                .get("artifact_sha256", "")
            ).strip().lower()

            if positive_number(artifact_bytes) and artifact_actual_bytes != int(artifact_bytes):
                errors.append(
                    "local model artifact bytes != manifest artifact_bytes: "
                    f"{artifact_actual_bytes} vs {artifact_bytes}"
                )
                artifact_status = "BLOCKED"

            if expected_sha256 and artifact_actual_sha256.lower() != expected_sha256:
                errors.append(
                    "local model artifact SHA256 != manifest artifact_sha256: "
                    f"{artifact_actual_sha256} vs {expected_sha256}"
                )
                artifact_status = "BLOCKED"

            if artifact_status != "BLOCKED":
                artifact_status = "PASS"
    elif model_record is not None and model_record.get("synthetic", False):
        if a.allow_synthetic:
            artifact_status = "SKIPPED-SYNTHETIC"
    elif model_record is not None:
        errors.append(
            "non-synthetic model intake requires --model-artifact so the local artifact SHA256/bytes can be verified"
        )
        artifact_status = "BLOCKED"

    command_status = "NOT-CHECKED"
    command_obj = {}
    if a.command_record is not None:
        if not a.command_record.is_file():
            errors.append(f"command record is not a file: {a.command_record}")
            command_status = "BLOCKED"
        else:
            try:
                command_obj = json.loads(a.command_record.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"invalid command record JSON: {exc}")
                command_status = "BLOCKED"

            if command_obj and not isinstance(command_obj, dict):
                errors.append("command record must be one JSON object")
                command_status = "BLOCKED"
                command_obj = {}

            if command_obj:
                if command_obj.get("capture_schema_version") != 1:
                    errors.append("command record capture_schema_version must be 1")
                    command_status = "BLOCKED"
                if command_obj.get("exit_code") != 0:
                    errors.append(
                        f"command record exit_code must be 0, got {command_obj.get('exit_code')!r}"
                    )
                    command_status = "BLOCKED"
                if command_obj.get("launch_error"):
                    errors.append(
                        f"command record contains launch_error: {command_obj.get('launch_error')!r}"
                    )
                    command_status = "BLOCKED"

                manifest_record = command_obj.get("manifest")
                if not isinstance(manifest_record, dict):
                    errors.append("command record missing manifest identity")
                    command_status = "BLOCKED"
                elif a.manifest.is_file():
                    actual_manifest_sha = sha256(a.manifest)
                    actual_manifest_bytes = a.manifest.stat().st_size
                    if manifest_record.get("sha256") != actual_manifest_sha:
                        errors.append(
                            "command record manifest SHA256 does not match supplied manifest"
                        )
                        command_status = "BLOCKED"
                    if manifest_record.get("bytes") != actual_manifest_bytes:
                        errors.append(
                            "command record manifest byte count does not match supplied manifest"
                        )
                        command_status = "BLOCKED"

                bound_artifact = command_obj.get("model_artifact")
                if not isinstance(bound_artifact, dict):
                    errors.append("command record missing model_artifact binding")
                    command_status = "BLOCKED"
                elif artifact_actual_sha256 is not None and artifact_actual_bytes is not None:
                    if bound_artifact.get("sha256") != artifact_actual_sha256:
                        errors.append(
                            "command record model artifact SHA256 does not match supplied local artifact"
                        )
                        command_status = "BLOCKED"
                    if bound_artifact.get("bytes") != artifact_actual_bytes:
                        errors.append(
                            "command record model artifact byte count does not match supplied local artifact"
                        )
                        command_status = "BLOCKED"

                try:
                    argv_model = extract_model_arg(command_obj.get("argv"))
                    cwd = command_obj.get("cwd")
                    if not present(cwd):
                        raise ValueError("command record cwd is missing")
                    argv_model_resolved = resolve_recorded_path(argv_model, cwd)
                    if a.model_artifact is None:
                        raise ValueError(
                            "cannot bind command argv without --model-artifact"
                        )
                    supplied_model_resolved = a.model_artifact.expanduser().resolve()
                    if argv_model_resolved != supplied_model_resolved:
                        raise ValueError(
                            "command model path does not match --model-artifact: "
                            f"argv={argv_model_resolved} supplied={supplied_model_resolved}"
                        )
                except Exception as exc:
                    errors.append(str(exc))
                    command_status = "BLOCKED"

                if command_status != "BLOCKED":
                    command_status = "PASS"
    elif model_record is not None and model_record.get("synthetic", False):
        if a.allow_synthetic:
            command_status = "SKIPPED-SYNTHETIC"
    elif model_record is not None:
        errors.append(
            "non-synthetic model intake requires --command-record so exact benchmark argv can be bound to the verified artifact"
        )
        command_status = "BLOCKED"

    quality_execution_status = "NOT-CHECKED"
    quality_exec_args = (
        a.quality_command_record,
        a.quality_stdout,
        a.quality_stderr,
        a.quality_packet,
    )
    supplied_quality_exec = [x is not None for x in quality_exec_args]

    if any(supplied_quality_exec):
        if not all(supplied_quality_exec):
            errors.append(
                "quality execution evidence is partial; supply all of "
                "--quality-command-record, --quality-stdout, --quality-stderr, --quality-packet"
            )
            quality_execution_status = "BLOCKED"
        elif (
            a.model_artifact is None
            or a.quality_corpus is None
            or a.quality_manifest is None
        ):
            errors.append(
                "quality execution evidence requires --model-artifact, --quality-corpus, "
                "and --quality-manifest anchors"
            )
            quality_execution_status = "BLOCKED"
        else:
            quality_exec_result = verify_quality_execution_evidence(
                a.quality_command_record,
                a.quality_stdout,
                a.quality_stderr,
                a.quality_packet,
                a.model_artifact,
                a.quality_corpus,
                a.quality_manifest,
            )
            if quality_exec_result["errors"]:
                errors.extend(
                    "quality execution: " + error
                    for error in quality_exec_result["errors"]
                )
                quality_execution_status = "BLOCKED"
            else:
                quality_execution_status = "PASS"
    elif model_record is not None and model_record.get("synthetic", False):
        if a.allow_synthetic:
            quality_execution_status = "SKIPPED-SYNTHETIC"
    elif model_record is not None:
        errors.append(
            "non-synthetic intake requires quality execution evidence: "
            "--quality-command-record, --quality-stdout, --quality-stderr, --quality-packet"
        )
        quality_execution_status = "BLOCKED"

    protocol = manifest.get("fixed", {}).get("protocol", {})
    for field in ("pp_tokens", "tg_tokens", "repetitions"):
        if not positive_number(protocol.get(field)):
            errors.append(f"manifest fixed.protocol.{field} must be > 0")

    execution = manifest.get("variant", {}).get("execution", {})
    for field in ("context", "sequences"):
        if not positive_number(execution.get(field)):
            errors.append(f"manifest variant.execution.{field} must be > 0")

    positive_metrics = []
    result_rows = []
    if a.result.is_file():
        try:
            result_rows = load_result_rows(a.result)
            for row in result_rows:
                kind = result_kind(row)
                avg = row.get("avg_ts")
                if kind and positive_number(avg):
                    positive_metrics.append((kind, float(avg)))
        except Exception as e:
            errors.append(f"invalid raw result: {e}")

    if not positive_metrics:
        errors.append("raw result contains no positive PP/TG avg_ts")
    elif manifest:
        cross_check_raw_identity(manifest, result_rows, errors)

    if packet:
        if packet.get("packet_schema_version") != 1:
            errors.append("packet_schema_version must be 1")
        if not isinstance(packet.get("files"), list):
            errors.append("packet.files must be a list")
        else:
            packet_paths = [a.manifest, a.result]
            if a.hardware_profile is not None:
                packet_paths.append(a.hardware_profile)
            if a.prompt_manifest is not None:
                packet_paths.append(a.prompt_manifest)
            if a.quality_corpus is not None:
                packet_paths.append(a.quality_corpus)
            if a.quality_manifest is not None:
                packet_paths.append(a.quality_manifest)
            if a.command_record is not None:
                packet_paths.append(a.command_record)
            for path in packet_paths:
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
    print("RAW IDENTITY CROSS-CHECK")
    print("- manifest/runtime/device/model/execution fields are checked against selected PP/TG rows")
    print("HARDWARE PROFILE")
    print(f"- status={profile_status}")
    if a.hardware_profile is not None:
        print(f"- path={a.hardware_profile}")
    if profile_actual_bytes is not None:
        print(f"- bytes={profile_actual_bytes}")
    if profile_actual_sha256 is not None:
        print(f"- sha256={profile_actual_sha256}")
    print("QUALITY IDENTITY")
    print(f"- status={quality_identity_status}")
    if a.quality_manifest is not None:
        print(f"- quality_manifest={a.quality_manifest}")
    print("QUALITY CORPUS")
    print(f"- status={quality_corpus_status}")
    if a.quality_corpus is not None:
        print(f"- path={a.quality_corpus}")
    if quality_corpus_bytes is not None:
        print(f"- bytes={quality_corpus_bytes}")
    if quality_corpus_sha256 is not None:
        print(f"- sha256={quality_corpus_sha256}")
    print("PROMPT EVIDENCE")
    print(f"- status={prompt_status}")
    if a.prompt_manifest is not None:
        print(f"- prompt_manifest={a.prompt_manifest}")
    print("MODEL ARTIFACT")
    print(f"- status={artifact_status}")
    if a.model_artifact is not None:
        print(f"- path={a.model_artifact}")
    if artifact_actual_bytes is not None:
        print(f"- bytes={artifact_actual_bytes}")
    if artifact_actual_sha256 is not None:
        print(f"- sha256={artifact_actual_sha256}")
    print("COMMAND ↔ ARTIFACT BINDING")
    print(f"- status={command_status}")
    if a.command_record is not None:
        print(f"- command_record={a.command_record}")
    print("QUALITY EXECUTION")
    print(f"- status={quality_execution_status}")
    if a.quality_command_record is not None:
        print(f"- quality_command_record={a.quality_command_record}")
    if a.quality_stdout is not None:
        print(f"- stdout={a.quality_stdout}")
    if a.quality_stderr is not None:
        print(f"- stderr={a.quality_stderr}")
    if a.quality_packet is not None:
        print(f"- packet={a.quality_packet}")

    print("ERRORS")
    for x in errors:
        print("- " + x)

    if errors:
        print("INTAKE: BLOCKED")
        raise SystemExit(2)

    print("RAW IDENTITY: PASS")
    print("INTAKE: READY")
    print("Next: run ingest_llama_bench.py, validate the catalog diff, then derive exact measured compatibility.")
    print("READY is an evidence-completeness and internal-consistency gate, not a benchmark-truth or purchase claim.")


if __name__ == "__main__":
    main()
