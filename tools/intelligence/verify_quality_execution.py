#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN", "N/A"}


def present(value):
    return str(value if value is not None else "").strip().upper() not in PLACEHOLDERS


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_object(path, label, errors):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid {label} JSON: {exc}")
        return {}
    if not isinstance(obj, dict):
        errors.append(f"{label} must be one JSON object")
        return {}
    return obj


def extract_path_arg(argv, short_flag, long_flag, label):
    if not isinstance(argv, list) or not all(isinstance(x, str) for x in argv):
        raise ValueError("quality command argv must be a list of strings")
    matches = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in (short_flag, long_flag):
            if i + 1 >= len(argv):
                raise ValueError(f"{arg} is missing its {label} path")
            matches.append(argv[i + 1])
            i += 2
            continue
        prefix = long_flag + "="
        if arg.startswith(prefix):
            matches.append(arg.split("=", 1)[1])
        i += 1
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one {short_flag}/{long_flag} path for {label}; found {len(matches)}"
        )
    return matches[0]


def resolve_recorded_path(value, cwd):
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path(cwd) / path
    return path.resolve()


def packet_match(packet, path):
    digest = sha256_file(path)
    size = path.stat().st_size
    matches = []
    for item in packet.get("files", []):
        if isinstance(item, dict) and item.get("sha256") == digest:
            matches.append(item)
    if not matches:
        return False, f"{path}: SHA256 not indexed by packet"
    if any(item.get("bytes") == size for item in matches):
        return True, None
    return False, f"{path}: packet SHA matches but byte count does not"


def check_binding(record, actual_path, label, errors):
    ok = True
    if not isinstance(record, dict):
        errors.append(f"quality command record missing {label} binding")
        return False
    actual_sha = sha256_file(actual_path)
    actual_bytes = actual_path.stat().st_size
    if record.get("sha256") != actual_sha:
        errors.append(f"quality command {label} SHA256 does not match supplied artifact")
        ok = False
    if record.get("bytes") != actual_bytes:
        errors.append(f"quality command {label} byte count does not match supplied artifact")
        ok = False
    return ok


def main():
    p = argparse.ArgumentParser(
        description=(
            "Verify sealed quality execution evidence against the exact model, corpus, "
            "quality identity artifact, raw streams, and packet."
        )
    )
    p.add_argument("--quality-command-record", type=Path, required=True)
    p.add_argument("--stdout", type=Path, required=True)
    p.add_argument("--stderr", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--model-artifact", type=Path, required=True)
    p.add_argument("--quality-corpus", type=Path, required=True)
    p.add_argument("--quality-manifest", type=Path, required=True)
    a = p.parse_args()

    errors = []
    for label, path in (
        ("quality command record", a.quality_command_record),
        ("stdout", a.stdout),
        ("stderr", a.stderr),
        ("packet", a.packet),
        ("model artifact", a.model_artifact),
        ("quality corpus", a.quality_corpus),
        ("quality manifest", a.quality_manifest),
    ):
        if not path.is_file():
            errors.append(f"{label} is not a file: {path}")

    command_obj = {}
    quality_obj = {}
    packet = {}
    if a.quality_command_record.is_file():
        command_obj = load_object(a.quality_command_record, "quality command record", errors)
    if a.quality_manifest.is_file():
        quality_obj = load_object(a.quality_manifest, "quality manifest", errors)
    if a.packet.is_file():
        packet = load_object(a.packet, "packet", errors)

    model_ok = a.model_artifact.is_file()
    corpus_ok = a.quality_corpus.is_file()
    identity_ok = bool(quality_obj)
    raw_ok = a.stdout.is_file() and a.stderr.is_file()
    packet_ok = bool(packet)
    command_ok = bool(command_obj)

    if quality_obj:
        if quality_obj.get("quality_identity_schema_version") != 1:
            errors.append("quality_identity_schema_version must be 1")
            identity_ok = False
        for field in ("tokenizer_identity", "corpus_sha256", "fixture_revision", "evaluation_args"):
            if not present(quality_obj.get(field)):
                errors.append(f"quality manifest missing/placeholder {field}")
                identity_ok = False
        if a.quality_corpus.is_file():
            actual_corpus_sha = sha256_file(a.quality_corpus)
            expected = str(quality_obj.get("corpus_sha256", "")).strip().lower()
            if actual_corpus_sha.lower() != expected:
                errors.append(
                    "quality manifest corpus_sha256 does not match supplied quality corpus: "
                    f"{expected} vs {actual_corpus_sha}"
                )
                identity_ok = False
                corpus_ok = False

    if command_obj:
        if command_obj.get("quality_capture_schema_version") != 1:
            errors.append("quality command quality_capture_schema_version must be 1")
            command_ok = False
        if command_obj.get("exit_code") != 0:
            errors.append(
                f"quality command exit_code must be 0, got {command_obj.get('exit_code')!r}"
            )
            command_ok = False
        if command_obj.get("launch_error"):
            errors.append(
                f"quality command contains launch_error: {command_obj.get('launch_error')!r}"
            )
            command_ok = False

        if a.model_artifact.is_file():
            if not check_binding(
                command_obj.get("model_artifact"),
                a.model_artifact,
                "model artifact",
                errors,
            ):
                model_ok = False
                command_ok = False

        if a.quality_corpus.is_file():
            if not check_binding(
                command_obj.get("quality_corpus"),
                a.quality_corpus,
                "quality corpus",
                errors,
            ):
                corpus_ok = False
                command_ok = False

        identity_record = command_obj.get("quality_identity")
        if not isinstance(identity_record, dict):
            errors.append("quality command record missing quality_identity binding")
            identity_ok = False
            command_ok = False
        elif a.quality_manifest.is_file():
            actual_identity_sha = sha256_file(a.quality_manifest)
            actual_identity_bytes = a.quality_manifest.stat().st_size
            if identity_record.get("sha256") != actual_identity_sha:
                errors.append(
                    "quality command quality_identity SHA256 does not match supplied quality manifest"
                )
                identity_ok = False
                command_ok = False
            if identity_record.get("bytes") != actual_identity_bytes:
                errors.append(
                    "quality command quality_identity byte count does not match supplied quality manifest"
                )
                identity_ok = False
                command_ok = False

        try:
            cwd = command_obj.get("cwd")
            if not present(cwd):
                raise ValueError("quality command cwd is missing")
            argv = command_obj.get("argv")
            argv_model = extract_path_arg(argv, "-m", "--model", "model")
            argv_corpus = extract_path_arg(argv, "-f", "--file", "quality corpus")
            if a.model_artifact.is_file():
                if resolve_recorded_path(argv_model, cwd) != a.model_artifact.expanduser().resolve():
                    raise ValueError(
                        "quality command model path does not match --model-artifact"
                    )
            if a.quality_corpus.is_file():
                if resolve_recorded_path(argv_corpus, cwd) != a.quality_corpus.expanduser().resolve():
                    raise ValueError(
                        "quality command corpus path does not match --quality-corpus"
                    )
        except Exception as exc:
            errors.append(str(exc))
            command_ok = False

    if raw_ok:
        if a.stdout.stat().st_size == 0 and a.stderr.stat().st_size == 0:
            errors.append("quality execution has no raw stdout/stderr evidence")
            raw_ok = False

    if packet:
        if packet.get("packet_schema_version") != 1:
            errors.append("packet_schema_version must be 1")
            packet_ok = False
        files = packet.get("files")
        if not isinstance(files, list):
            errors.append("packet.files must be a list")
            packet_ok = False
        else:
            if packet.get("file_count") != len(files):
                errors.append("packet.file_count does not equal len(packet.files)")
                packet_ok = False
            for path in (
                a.quality_command_record,
                a.stdout,
                a.stderr,
                a.quality_manifest,
            ):
                if path.is_file():
                    ok, message = packet_match(packet, path)
                    if not ok:
                        errors.append(message)
                        packet_ok = False

    print("QUALITY EXECUTION EVIDENCE")
    print(f"model_binding={'PASS' if model_ok else 'BLOCKED'}")
    print(f"corpus_binding={'PASS' if corpus_ok else 'BLOCKED'}")
    print(f"quality_identity_binding={'PASS' if identity_ok else 'BLOCKED'}")
    print(f"command_binding={'PASS' if command_ok else 'BLOCKED'}")
    print(f"raw_output={'PASS' if raw_ok else 'BLOCKED'}")
    print(f"packet={'PASS' if packet_ok else 'BLOCKED'}")
    print("ERRORS")
    for error in errors:
        print("- " + error)

    if errors:
        print("QUALITY EXECUTION: BLOCKED")
        raise SystemExit(2)

    print("QUALITY EXECUTION: PASS")
    print(
        "PASS proves the sealed command/result evidence is internally bound to the supplied "
        "model, corpus, and quality identity artifact."
    )
    print(
        "It does not prove the PPL parser, metric interpretation, task quality, or causal comparison."
    )


if __name__ == "__main__":
    main()
