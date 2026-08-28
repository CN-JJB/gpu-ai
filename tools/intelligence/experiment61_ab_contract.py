#!/usr/bin/env python3
"""Shared Experiment 61 baseline/candidate one-variable contract."""

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
    "fixed.quality_eval.fixture_revision",
    "fixed.quality_eval.evaluation_args",
    "variant.hardware.device_identity",
    "variant.hardware.profile_sha256",
    "variant.runtime.runtime_identity",
    "variant.runtime.backend",
    "variant.runtime.build_identity",
    "variant.model.artifact_sha256",
    "variant.model.artifact_bytes",
    "variant.model.quant",
    "variant.model.source_revision",
    "variant.execution.context",
    "variant.execution.sequences",
    "variant.prompt.token_ids_sha256",
    "variant.prompt.token_count",
    "variant.sampler.mode",
]


def get_path(obj, dotted, missing=None):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return missing
        cur = cur[part]
    return cur


def walk(prefix, obj):
    if isinstance(obj, dict):
        if not obj:
            yield prefix, obj
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            yield from walk(path, value)
    elif isinstance(obj, list):
        if not obj:
            yield prefix, obj
        for index, value in enumerate(obj):
            yield from walk(f"{prefix}[{index}]", value)
    else:
        yield prefix, obj


def diff_paths(a, b, prefix=""):
    if type(a) is not type(b):
        return [prefix or "<root>"]

    if isinstance(a, dict):
        out = []
        for key in sorted(set(a) | set(b)):
            path = f"{prefix}.{key}" if prefix else key
            if key not in a or key not in b:
                out.append(path)
            else:
                out.extend(diff_paths(a[key], b[key], path))
        return out

    if isinstance(a, list):
        if len(a) != len(b):
            return [prefix]
        out = []
        for index, (left, right) in enumerate(zip(a, b)):
            out.extend(diff_paths(left, right, f"{prefix}[{index}]"))
        return out

    return [] if a == b else [prefix]


def ignored(path):
    return (
        path == "label"
        or path.startswith("label.")
        or path.startswith("label[")
        or path == "audit"
        or path.startswith("audit.")
        or path.startswith("audit[")
    )


def under(path, parent):
    return (
        path == parent
        or path.startswith(parent + ".")
        or path.startswith(parent + "[")
    )


def validate_manifest_pair(baseline, candidate):
    errors = []
    missing = object()

    for name, obj in (("baseline", baseline), ("candidate", candidate)):
        if not isinstance(obj, dict):
            errors.append(f"{name}: manifest must be one JSON object")
            continue

        for req in REQUIRED_PATHS:
            if get_path(obj, req, missing) is missing:
                errors.append(f"{name}: missing required path {req}")

        for path, value in walk("", obj):
            if isinstance(value, str) and value.strip().upper() in PLACEHOLDERS:
                errors.append(f"{name}: placeholder at {path}")

    if not isinstance(baseline, dict) or not isinstance(candidate, dict):
        return {
            "errors": errors,
            "comparison_id": None,
            "intentional_variable": None,
            "semantic_differences": [],
        }

    if baseline.get("schema_version") != candidate.get("schema_version"):
        errors.append("schema_version differs")

    if baseline.get("comparison_id") != candidate.get("comparison_id"):
        errors.append("comparison_id differs")

    declared_a = baseline.get("intentional_variable")
    declared_b = candidate.get("intentional_variable")

    if declared_a != declared_b:
        errors.append(
            "intentional_variable differs: "
            f"{declared_a!r} vs {declared_b!r}"
        )
        declared = None
    else:
        declared = declared_a

    if not isinstance(declared, str) or not declared.startswith("variant."):
        errors.append("intentional_variable must be a dotted path under variant.*")

    semantic_differences = [
        path
        for path in diff_paths(baseline, candidate)
        if not ignored(path) and path != "intentional_variable"
    ]

    if isinstance(declared, str) and declared.startswith("variant."):
        declared_diffs = [
            path for path in semantic_differences if under(path, declared)
        ]
        undeclared = [
            path for path in semantic_differences if not under(path, declared)
        ]

        if not declared_diffs:
            errors.append(f"declared variable {declared} did not actually change")
        if undeclared:
            errors.append("undeclared differences: " + ", ".join(undeclared))

    return {
        "errors": errors,
        "comparison_id": baseline.get("comparison_id"),
        "intentional_variable": declared,
        "semantic_differences": semantic_differences,
    }
