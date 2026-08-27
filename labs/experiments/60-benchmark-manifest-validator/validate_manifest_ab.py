#!/usr/bin/env python3
import json
import sys
from pathlib import Path

IGNORED_PREFIXES = ("label", "audit")
PLACEHOLDERS = {"REPLACE", "TBD", "TODO"}

REQUIRED_PATHS = [
    "schema_version",
    "comparison_id",
    "intentional_variable",
    "fixed.protocol.pp_tokens",
    "fixed.protocol.tg_tokens",
    "fixed.protocol.repetitions",
    "fixed.quality_eval.tokenizer_identity",
    "fixed.quality_eval.corpus_sha256",
    "variant.hardware.device_identity",
    "variant.runtime.runtime_identity",
    "variant.model.artifact_sha256",
    "variant.execution.context",
    "variant.prompt.token_ids_sha256",
    "variant.prompt.token_count",
    "variant.sampler.mode",
]

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def get_path(obj, dotted):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur

def walk(prefix, obj):
    if isinstance(obj, dict):
        if not obj:
            yield prefix, obj
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else k
            yield from walk(p, v)
    elif isinstance(obj, list):
        if not obj:
            yield prefix, obj
        for i, v in enumerate(obj):
            yield from walk(f"{prefix}[{i}]", v)
    else:
        yield prefix, obj

def diff_paths(a, b, prefix=""):
    if type(a) is not type(b):
        return [prefix or "<root>"]

    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            p = f"{prefix}.{k}" if prefix else k
            if k not in a or k not in b:
                out.append(p)
            else:
                out.extend(diff_paths(a[k], b[k], p))
        return out

    if isinstance(a, list):
        if len(a) != len(b):
            return [prefix]
        out = []
        for i, (av, bv) in enumerate(zip(a, b)):
            out.extend(diff_paths(av, bv, f"{prefix}[{i}]"))
        return out

    return [] if a == b else [prefix]

def ignored(path):
    return any(
        path == p or path.startswith(p + ".") or path.startswith(p + "[")
        for p in IGNORED_PREFIXES
    )

def under(path, parent):
    return (
        path == parent
        or path.startswith(parent + ".")
        or path.startswith(parent + "[")
    )

def main():
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: validate_manifest_ab.py baseline.json candidate.json"
        )

    a, b = map(load, sys.argv[1:])
    errors = []

    for name, obj in [("baseline", a), ("candidate", b)]:
        for req in REQUIRED_PATHS:
            if get_path(obj, req) is None:
                errors.append(f"{name}: missing required path {req}")

        for path, value in walk("", obj):
            if (
                isinstance(value, str)
                and value.strip().upper() in PLACEHOLDERS
            ):
                errors.append(f"{name}: placeholder at {path}")

    if a.get("schema_version") != b.get("schema_version"):
        errors.append("schema_version differs")

    if a.get("comparison_id") != b.get("comparison_id"):
        errors.append("comparison_id differs")

    declared_a = a.get("intentional_variable")
    declared_b = b.get("intentional_variable")

    if declared_a != declared_b:
        errors.append(
            "intentional_variable differs: "
            f"{declared_a!r} vs {declared_b!r}"
        )
        declared = None
    else:
        declared = declared_a

    if (
        not isinstance(declared, str)
        or not declared.startswith("variant.")
    ):
        errors.append(
            "intentional_variable must be a dotted path under variant.*"
        )

    semantic_diffs = [
        p for p in diff_paths(a, b)
        if not ignored(p) and p != "intentional_variable"
    ]

    if isinstance(declared, str) and declared.startswith("variant."):
        declared_diffs = [
            p for p in semantic_diffs
            if under(p, declared)
        ]
        undeclared = [
            p for p in semantic_diffs
            if not under(p, declared)
        ]

        if not declared_diffs:
            errors.append(
                f"declared variable {declared} did not actually change"
            )

        if undeclared:
            errors.append(
                "undeclared differences: " + ", ".join(undeclared)
            )

    print("MANIFEST CONTRACT")
    print(f"- comparison_id: {a.get('comparison_id')!r}")
    print(f"- intentional_variable: {declared!r}")
    print(
        "- semantic differences: "
        f"{semantic_diffs if semantic_diffs else 'NONE'}"
    )

    if errors:
        print("VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("VALIDATION: PASS")
    print("- only the declared semantic variable changed")
    print("- required identity fields are present")
    print("- no REPLACE/TBD/TODO placeholders found")

if __name__ == "__main__":
    main()
