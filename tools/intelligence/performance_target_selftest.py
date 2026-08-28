#!/usr/bin/env python3
import json
import sys
import tempfile
from pathlib import Path

from joint_tradeoff_selftest import run
from unified_tradeoff_route_selftest import build_model_fixture


HERE = Path(__file__).resolve().parent
PY = sys.executable


def base_args(fixture, policy, result):
    return [
        "--policy",
        str(policy),
        "--joint-tradeoff",
        str(fixture["joint"]),
        "--baseline-manifest",
        str(fixture["bm"]),
        "--candidate-manifest",
        str(fixture["cm"]),
        "--baseline-benchmark",
        str(fixture["bb"]),
        "--candidate-benchmark",
        str(fixture["cb"]),
        "--quality-comparison",
        str(fixture["comparison"]),
        "--baseline-quality-dir",
        str(fixture["bq"]),
        "--candidate-quality-dir",
        str(fixture["cq"]),
        "--baseline-model-artifact",
        str(fixture["baseline_model"]),
        "--candidate-model-artifact",
        str(fixture["candidate_model"]),
        "--quality-corpus",
        str(fixture["corpus"]),
        "--out",
        str(result),
    ]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        fixture = build_model_fixture(td)

        policy = td / "policy.json"
        policy.write_text(
            json.dumps(
                {
                    "performance_target_policy_schema_version": 1,
                    "policy_id": "synthetic-i46-pass",
                    "comparison_id": "fixture-i42-model",
                    "requirements": {
                        "min_pp_tok_s": 1100,
                        "min_tg_tok_s": 55,
                        "max_candidate_ppl": 11,
                        "max_ppl_percent_change": 10,
                    },
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        result = td / "result.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_performance_target.py"),
                *base_args(fixture, policy, result),
            ]
        )
        assert "PERFORMANCE TARGET: PASS" in out
        obj = json.loads(result.read_text(encoding="utf-8"))
        assert obj["decision"] == "PASS"
        assert obj["synthetic_input"] is True
        assert len(obj["checks"]) == 4

        verify_args = base_args(fixture, policy, result)
        verify_args = verify_args[:-2]
        out = run(
            [
                PY,
                str(HERE / "verify_performance_target.py"),
                "--result",
                str(result),
                *verify_args,
            ]
        )
        assert "PERFORMANCE TARGET ARTIFACT: PASS" in out

        fail_policy = td / "fail-policy.json"
        fail_policy.write_text(
            json.dumps(
                {
                    "performance_target_policy_schema_version": 1,
                    "policy_id": "synthetic-i46-fail",
                    "comparison_id": "fixture-i42-model",
                    "requirements": {
                        "min_tg_tok_s": 1000
                    },
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        fail_result = td / "fail-result.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_performance_target.py"),
                *base_args(fixture, fail_policy, fail_result),
            ]
        )
        assert "PERFORMANCE TARGET: FAIL" in out

        tampered = td / "tampered.json"
        bad = json.loads(fail_result.read_text(encoding="utf-8"))
        bad["decision"] = "PASS"
        bad["checks"][0]["status"] = "PASS"
        tampered.write_text(
            json.dumps(bad, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        verify_fail_args = base_args(fixture, fail_policy, fail_result)[:-2]
        out = run(
            [
                PY,
                str(HERE / "verify_performance_target.py"),
                "--result",
                str(tampered),
                *verify_fail_args,
            ],
            expect=2,
        )
        assert "does not exactly match independently rebuilt" in out
        assert "PERFORMANCE TARGET ARTIFACT: BLOCKED" in out

        wrong_policy = td / "wrong-comparison.json"
        wrong_policy.write_text(
            json.dumps(
                {
                    "performance_target_policy_schema_version": 1,
                    "policy_id": "synthetic-i46-wrong",
                    "comparison_id": "not-the-comparison",
                    "requirements": {"min_tg_tok_s": 1},
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        blocked = td / "blocked.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_performance_target.py"),
                *base_args(fixture, wrong_policy, blocked),
            ],
            expect=2,
        )
        assert "comparison_id does not match verified tradeoff" in out
        assert not blocked.exists()

    print("PERFORMANCE TARGET SELFTEST: PASS")
    print("- explicit PP/TG/PPL thresholds evaluate without weighting")
    print("- result is independently reproducible")
    print("- failing target cannot be edited into PASS")
    print("- comparison_id mismatch is blocked")
    print("- synthetic tradeoff remains labeled synthetic_input=true")


if __name__ == "__main__":
    main()
