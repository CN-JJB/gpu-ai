#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
PY = sys.executable


def run(args, expect=0):
    proc = subprocess.run(args, text=True, capture_output=True)
    out = proc.stdout + proc.stderr
    if proc.returncode != expect:
        print(out)
        raise AssertionError(
            f"expected return code {expect}, got {proc.returncode}: {args}"
        )
    return out


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def write_identity(path, corpus):
    path.write_text(
        json.dumps(
            {
                "quality_identity_schema_version": 2,
                "tokenizer_identity": "fixture-tokenizer-i36",
                "corpus_sha256": sha256_bytes(corpus.read_bytes()),
                "fixture_revision": "fixture-i36",
                "evaluation_args": ["--fixture-mode", "strict"],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def write_fake(path):
    path.write_text(
        "#!/usr/bin/env python3\n"
        "import argparse\n"
        "from pathlib import Path\n"
        "p = argparse.ArgumentParser()\n"
        "p.add_argument('-m', '--model', required=True)\n"
        "p.add_argument('-f', '--file', required=True)\n"
        "p.add_argument('--fixture-mode', required=True)\n"
        "a = p.parse_args()\n"
        "data = Path(a.model).read_bytes()\n"
        "ppl = 8.0 if data.startswith(b'baseline') else 8.4\n"
        "print('Final estimate: PPL = %.4f +/- 0.10000' % ppl)\n",
        encoding="utf-8",
    )
    path.chmod(0o755)


def capture(root, fake, model, corpus, identity):
    out = run(
        [
            PY,
            str(HERE / "capture_quality_eval.py"),
            "--out-dir",
            str(root),
            "--model-artifact",
            str(model),
            "--quality-corpus",
            str(corpus),
            "--quality-manifest",
            str(identity),
            "--",
            str(fake),
            "-m",
            str(model),
            "-f",
            str(corpus),
            "--fixture-mode",
            "strict",
        ]
    )
    assert "QUALITY CAPTURE: SEALED" in out

    out = run(
        [
            PY,
            str(HERE / "extract_quality_metric.py"),
            "--quality-command-record",
            str(root / "quality-command.json"),
            "--stdout",
            str(root / "stdout.txt"),
            "--stderr",
            str(root / "stderr.txt"),
            "--packet",
            str(root / "PACKET.json"),
            "--model-artifact",
            str(model),
            "--quality-corpus",
            str(corpus),
            "--quality-manifest",
            str(root / "quality-identity.json"),
            "--out",
            str(root / "quality-metric.json"),
        ]
    )
    assert "QUALITY METRIC: EXTRACTED" in out


def verify_args(comparison, base, cand, bm, cm, corpus):
    return [
        PY,
        str(HERE / "verify_quality_comparison.py"),
        "--quality-comparison",
        str(comparison),
        "--baseline-dir",
        str(base),
        "--candidate-dir",
        str(cand),
        "--baseline-model",
        str(bm),
        "--candidate-model",
        str(cm),
        "--quality-corpus",
        str(corpus),
    ]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"same i36 corpus\n")

        baseline_model = td / "baseline.gguf"
        baseline_model.write_bytes(b"baseline-i36-model\n")
        candidate_model = td / "candidate.gguf"
        candidate_model.write_bytes(b"candidate-i36-model\n")

        baseline_identity = td / "baseline-identity.json"
        candidate_identity = td / "candidate-identity.json"
        write_identity(baseline_identity, corpus)
        write_identity(candidate_identity, corpus)

        fake = td / "fake-quality"
        write_fake(fake)

        base = td / "baseline-run"
        cand = td / "candidate-run"
        capture(base, fake, baseline_model, corpus, baseline_identity)
        capture(cand, fake, candidate_model, corpus, candidate_identity)

        comparison = td / "quality-comparison.json"
        out = run(
            [
                PY,
                str(HERE / "compare_quality_metrics.py"),
                "--baseline-dir",
                str(base),
                "--candidate-dir",
                str(cand),
                "--baseline-model",
                str(baseline_model),
                "--candidate-model",
                str(candidate_model),
                "--quality-corpus",
                str(corpus),
                "--out",
                str(comparison),
            ]
        )
        assert "QUALITY COMPARISON: PASS" in out

        out = run(
            verify_args(
                comparison,
                base,
                cand,
                baseline_model,
                candidate_model,
                corpus,
            )
        )
        assert "QUALITY COMPARISON ARTIFACT: PASS" in out

        tampered = td / "tampered-comparison.json"
        obj = json.loads(comparison.read_text(encoding="utf-8"))
        obj["baseline"]["value"] = 9.0
        obj["candidate"]["value"] = 9.45
        obj["delta_candidate_minus_baseline"] = 0.45
        obj["ratio_candidate_to_baseline"] = 1.05
        obj["percent_change"] = 5.0
        tampered.write_text(
            json.dumps(obj, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        out = run(
            verify_args(
                tampered,
                base,
                cand,
                baseline_model,
                candidate_model,
                corpus,
            ),
            expect=2,
        )
        assert "does not exactly match independently recomputed quality bundles" in out
        assert "QUALITY COMPARISON ARTIFACT: BLOCKED" in out

    print("QUALITY COMPARISON ARTIFACT SELFTEST: PASS")
    print("- valid I33 comparison is independently reproducible from both sealed bundles")
    print("- coherently edited PPL values/delta/ratio/percent are still blocked")
    print("- no comparison JSON is trusted merely because its arithmetic is self-consistent")
    print("- synthetic PPL values are provenance fixtures only")


if __name__ == "__main__":
    main()
