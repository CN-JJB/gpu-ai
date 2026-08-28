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


def write_identity(path, corpus, evaluation_args):
    path.write_text(
        json.dumps(
            {
                "quality_identity_schema_version": 2,
                "tokenizer_identity": "fixture-tokenizer-i33",
                "corpus_sha256": sha256_bytes(corpus.read_bytes()),
                "fixture_revision": "fixture-i33",
                "evaluation_args": evaluation_args,
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
        "ppl = 12.0 if data.startswith(b'baseline') else 12.6\n"
        "print('[1]99.0000,[2]%.4f,' % ppl)\n"
        "print('Final estimate: PPL = %.4f +/- 0.20000' % ppl)\n",
        encoding="utf-8",
    )
    path.chmod(0o755)


def capture(root, fake, model, corpus, identity, eval_args):
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
            *eval_args,
        ]
    )
    assert "QUALITY CAPTURE: SEALED" in out

    metric = root / "quality-metric.json"
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
            str(metric),
        ]
    )
    assert "QUALITY METRIC: EXTRACTED" in out


def compare_args(base, cand, baseline_model, candidate_model, corpus, out):
    return [
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
        str(out),
    ]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"same i33 quality corpus\n")

        baseline_model = td / "baseline.gguf"
        baseline_model.write_bytes(b"baseline-model-i33\n")
        candidate_model = td / "candidate.gguf"
        candidate_model.write_bytes(b"candidate-model-i33\n")

        fake = td / "fake-quality"
        write_fake(fake)

        eval_args = ["--fixture-mode", "strict"]
        baseline_identity = td / "baseline-identity.json"
        candidate_identity = td / "candidate-identity.json"
        write_identity(baseline_identity, corpus, eval_args)
        write_identity(candidate_identity, corpus, eval_args)

        base = td / "baseline-run"
        cand = td / "candidate-run"
        capture(base, fake, baseline_model, corpus, baseline_identity, eval_args)
        capture(cand, fake, candidate_model, corpus, candidate_identity, eval_args)

        comparison = td / "comparison.json"
        out = run(
            compare_args(
                base,
                cand,
                baseline_model,
                candidate_model,
                corpus,
                comparison,
            )
        )
        assert "QUALITY COMPARISON: PASS" in out

        obj = json.loads(comparison.read_text(encoding="utf-8"))
        assert obj["quality_comparison_schema_version"] == 1
        assert obj["baseline"]["value"] == 12.0
        assert obj["candidate"]["value"] == 12.6
        assert abs(obj["delta_candidate_minus_baseline"] - 0.6) < 1e-9
        assert abs(obj["ratio_candidate_to_baseline"] - 1.05) < 1e-9
        assert abs(obj["percent_change"] - 5.0) < 1e-9

        loose_args = ["--fixture-mode", "loose"]
        loose_identity = td / "loose-identity.json"
        write_identity(loose_identity, corpus, loose_args)
        loose = td / "loose-run"
        capture(
            loose,
            fake,
            candidate_model,
            corpus,
            loose_identity,
            loose_args,
        )

        blocked = td / "blocked.json"
        out = run(
            compare_args(
                base,
                loose,
                baseline_model,
                candidate_model,
                corpus,
                blocked,
            ),
            expect=2,
        )
        assert "quality identity mismatch for evaluation_args" in out
        assert "QUALITY COMPARISON: BLOCKED" in out
        assert not blocked.exists()

        fake2 = td / "fake-quality-2"
        fake2.write_bytes(fake.read_bytes() + b"\n# different executable bytes\n")
        fake2.chmod(0o755)
        different_build = td / "different-build-run"
        capture(
            different_build,
            fake2,
            candidate_model,
            corpus,
            candidate_identity,
            eval_args,
        )

        build_blocked = td / "build-blocked.json"
        out = run(
            compare_args(
                base,
                different_build,
                baseline_model,
                candidate_model,
                corpus,
                build_blocked,
            ),
            expect=2,
        )
        assert "quality executable SHA256 differs" in out
        assert "QUALITY COMPARISON: BLOCKED" in out
        assert not build_blocked.exists()

    print("QUALITY COMPARISON SELFTEST: PASS")
    print("- both sides independently pass sealed metric verification")
    print("- exact identity/build contract permits descriptive PPL delta and ratio")
    print("- changed evaluation argv blocks comparison")
    print("- changed quality executable bytes block comparison")
    print("- synthetic PPL values exercise arithmetic only and are not real model results")


if __name__ == "__main__":
    main()
