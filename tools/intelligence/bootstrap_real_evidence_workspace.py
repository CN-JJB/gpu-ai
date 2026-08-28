#!/usr/bin/env python3
import argparse
import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXP61 = ROOT / "labs" / "experiments" / "61-real-benchmark-evidence-packet"
EXP59 = ROOT / "labs" / "experiments" / "59-real-quality-gate"
CATALOG = ROOT / "intelligence" / "catalog"

PROFILES = {
    "generic": {
        "session": "real-evidence-session.template.json",
        "probes": "semantic-source-probes.template.json",
    },
    "rtx3090-qwen3-8b-llamacpp": {
        "session": "real-evidence-session.rtx3090-qwen3-8b-llamacpp.skeleton.json",
        "probes": "semantic-source-probes.rtx3090-llamacpp.json",
    },
}

MODEL_PLACEHOLDERS = {
    "/absolute/path/to/model.gguf",
    "REPLACE_WITH_ABSOLUTE_GGUF_PATH",
}
CORPUS_PLACEHOLDERS = {
    "/absolute/path/to/quality-corpus.txt",
    "REPLACE_WITH_ABSOLUTE_QUALITY_CORPUS_PATH",
}


def fail(message):
    raise SystemExit(f"REAL WORKSPACE BOOTSTRAP: FAIL\n{message}")


def ensure_file(path, label):
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        fail(f"{label} is not a file: {path}")
    return path


def ensure_empty_dir(path):
    path = Path(path).expanduser().resolve()
    if path.exists():
        if not path.is_dir():
            fail(f"out-dir is not a directory: {path}")
        if any(path.iterdir()):
            fail(f"out-dir is not empty: {path}")
    else:
        path.mkdir(parents=True)
    return path


def load_json(path, label):
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{label}: invalid JSON: {exc}")
    if not isinstance(obj, dict):
        fail(f"{label}: expected one JSON object")
    return obj


def dump_json(path, obj):
    Path(path).write_text(
        json.dumps(obj, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def bind_tokens(argv, placeholders, real_path):
    if not isinstance(argv, list):
        fail("session argv must be a JSON list")
    return [real_path if token in placeholders else token for token in argv]


def bind_real_paths(session, model_artifact=None, quality_corpus=None):
    if model_artifact is not None:
        model = str(model_artifact)
        session["model_artifact"] = model
        session["benchmark_argv"] = bind_tokens(
            session.get("benchmark_argv"), MODEL_PLACEHOLDERS, model
        )
        session["quality_argv"] = bind_tokens(
            session.get("quality_argv"), MODEL_PLACEHOLDERS, model
        )

    if quality_corpus is not None:
        corpus = str(quality_corpus)
        session["quality_corpus"] = corpus
        session["quality_argv"] = bind_tokens(
            session.get("quality_argv"), CORPUS_PLACEHOLDERS, corpus
        )


def render_runbook(workspace):
    tool_dir = ROOT / "tools" / "intelligence"
    return f"""# First Real Experiment 61 Workspace

This workspace is an operator convenience layer. It is not a new Intelligence gate and it creates no production evidence by itself.

## Bound repository paths

- repository: `{ROOT}`
- production catalog: `{CATALOG}`
- workspace: `{workspace}`

## Files created from templates

~~~text
baseline-manifest.json
quality-identity.json
real-session.json
semantic-probes.json
prompt-evidence/
workspace.json
~~~

The bootstrap deliberately did **not** create:

~~~text
model GGUF
profile.txt
prompt-evidence/manifest.json
quality corpus
benchmark output
quality output
~~~

Those must come from real artifacts or real capture.

## 1. Put real source artifacts in place

Required before I53:

~~~text
profile.txt
prompt-evidence/manifest.json
real model GGUF at the path in real-session.json
real quality corpus at the path in real-session.json
~~~

Fill `quality-identity.json`, `baseline-manifest.json`, and `real-session.json` deliberately.

## 2. Capture same-machine semantic sources (I54)

Review every argv in `semantic-probes.json` first.

~~~bash
python3 "{tool_dir / 'capture_semantic_sources.py'}" \
  "{workspace / 'semantic-probes.json'}" \
  --out-dir "{workspace / 'semantic-source-evidence'}"
~~~

Require:

~~~text
SEMANTIC SOURCE CAPTURE: READY-FOR-SEMANTIC-REVIEW
~~~

Review the raw streams before filling semantic manifest fields.

## 3. Materialize byte-derived identity (I53)

~~~bash
python3 "{tool_dir / 'prepare_real_evidence_session.py'}" \
  "{workspace / 'real-session.json'}" \
  --out-dir "{workspace / 'prepared-session'}"
~~~

Require:

~~~text
REAL SESSION PREPARE: READY-TO-RUN-I52
~~~

## 4. Execute and seal benchmark + quality (I52)

~~~bash
python3 "{tool_dir / 'run_real_evidence_session.py'}" \
  "{workspace / 'prepared-session' / 'session.json'}" \
  --out-dir "{workspace / 'real-session-output'}"
~~~

Require:

~~~text
REAL SESSION: READY
~~~

## 5. Human review remains mandatory

Do not ingest automatically. Review exact hardware/runtime/model/execution identity and raw benchmark/quality evidence first.

~~~text
automatic_benchmark_launch = NOT-PERMITTED by bootstrap
automatic_catalog_ingestion = NOT-PERMITTED
automatic_purchase_decision = NOT-PERMITTED
~~~
"""


def main():
    p = argparse.ArgumentParser(
        description=(
            "Create a clean first-real Experiment 61 workspace from repository templates. "
            "No hardware/model/runtime semantics are inferred and no benchmark is launched."
        )
    )
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument(
        "--profile",
        choices=sorted(PROFILES),
        default="generic",
        help="Template profile only; it does not assert observed hardware.",
    )
    p.add_argument(
        "--model-artifact",
        type=Path,
        help="Optional existing GGUF path to bind into session paths/argv.",
    )
    p.add_argument(
        "--quality-corpus",
        type=Path,
        help="Optional existing corpus path to bind into session paths/argv.",
    )
    p.add_argument(
        "--observed-at",
        help="Optional explicit YYYY-MM-DD observation date. Omitted means leave the template placeholder.",
    )
    a = p.parse_args()

    profile = PROFILES[a.profile]
    session_src = ensure_file(EXP61 / profile["session"], "session template")
    probes_src = ensure_file(EXP61 / profile["probes"], "semantic probe template")
    manifest_src = ensure_file(EXP61 / "manifest.template.json", "manifest template")
    quality_src = ensure_file(
        EXP59 / "quality-identity.template.json", "quality identity template"
    )
    if not CATALOG.is_dir():
        fail(f"production catalog is not a directory: {CATALOG}")

    model = ensure_file(a.model_artifact, "model artifact") if a.model_artifact else None
    corpus = ensure_file(a.quality_corpus, "quality corpus") if a.quality_corpus else None

    if a.observed_at is not None:
        try:
            date.fromisoformat(a.observed_at)
        except ValueError:
            fail(f"observed-at must be YYYY-MM-DD: {a.observed_at!r}")

    workspace = ensure_empty_dir(a.out_dir)
    prompt_dir = workspace / "prompt-evidence"
    prompt_dir.mkdir()

    shutil.copy2(manifest_src, workspace / "baseline-manifest.json")
    shutil.copy2(quality_src, workspace / "quality-identity.json")
    shutil.copy2(probes_src, workspace / "semantic-probes.json")

    probes = load_json(workspace / "semantic-probes.json", "semantic probe template")
    probes["working_directory"] = str(workspace)
    dump_json(workspace / "semantic-probes.json", probes)

    session = load_json(session_src, "session template")
    session["working_directory"] = str(workspace)
    session["catalog"] = str(CATALOG.resolve())
    session["manifest"] = str((workspace / "baseline-manifest.json").resolve())
    session["hardware_profile"] = str((workspace / "profile.txt").resolve())
    session["prompt_manifest"] = str((prompt_dir / "manifest.json").resolve())
    session["quality_identity"] = str((workspace / "quality-identity.json").resolve())
    if a.observed_at is not None:
        session["observed_at"] = a.observed_at

    bind_real_paths(session, model_artifact=model, quality_corpus=corpus)
    dump_json(workspace / "real-session.json", session)

    state = {
        "real_workspace_schema_version": 1,
        "status": "NEEDS-REAL-INPUTS",
        "profile": a.profile,
        "repo_root": str(ROOT),
        "catalog": str(CATALOG.resolve()),
        "workspace": str(workspace),
        "generated_from_templates": [
            str(manifest_src.relative_to(ROOT)),
            str(quality_src.relative_to(ROOT)),
            str(session_src.relative_to(ROOT)),
            str(probes_src.relative_to(ROOT)),
        ],
        "bound_real_inputs": {
            "model_artifact": str(model) if model else None,
            "quality_corpus": str(corpus) if corpus else None,
            "observed_at": a.observed_at,
        },
        "required_real_inputs_not_generated": [
            "profile.txt",
            "prompt-evidence/manifest.json",
            "real model GGUF",
            "real quality corpus",
            "explicit semantic manifest values",
            "exact benchmark argv",
            "exact quality argv",
        ],
        "next_stage": "I54 semantic-source capture and human review",
        "automatic_benchmark_launch": "NOT-PERMITTED",
        "automatic_catalog_ingestion": "NOT-PERMITTED",
        "automatic_purchase_decision": "NOT-PERMITTED",
    }
    dump_json(workspace / "workspace.json", state)
    (workspace / "RUN.md").write_text(render_runbook(workspace), encoding="utf-8")

    print(f"workspace={workspace}")
    print(f"profile={a.profile}")
    print("status=NEEDS-REAL-INPUTS")
    print("next=review RUN.md, then capture I54 semantic sources")
    print("REAL WORKSPACE BOOTSTRAP: READY")


if __name__ == "__main__":
    main()
