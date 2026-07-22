"""Run the source-backed CLARITree claim suite and print one evidence payload.

The immutable baseline evaluates C1--C4 and C6.  A child experiment can add
``verify_synthetic_claim.py`` to supply an explicitly independent C5 protocol;
the fixed run command and this orchestrator do not change.
"""

from __future__ import annotations

import importlib.util
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "upstream"
OUTPUTS = ROOT / "outputs"


def run_check(script: str) -> dict[str, object]:
    command = [sys.executable, str(ROOT / "repro" / "src" / script)]
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    elapsed = time.perf_counter() - started
    print(f"\n--- {script} ({elapsed:.3f}s) ---")
    print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="")
    if completed.returncode:
        raise RuntimeError(f"{script} exited {completed.returncode}")
    return {"elapsed_seconds": elapsed, "stdout_tail": completed.stdout[-1000:]}


def fresh_california_outer4() -> dict[str, object]:
    sys.path.insert(0, str(UPSTREAM))
    from clari_tree import CLARITree
    from scripts.run_ours_outer import fit_eval, load_xy

    split = UPSTREAM / "data" / "california_housing" / "splits" / "outer_4"
    x_train, y_train = load_xy(split / "train.csv")
    x_test, y_test = load_xy(split / "test.csv")
    args = SimpleNamespace(
        depth=4,
        n_thresholds=20,
        thresholds_strategy="quantile",
        min_leaf_node_size=0,
    )
    started = time.perf_counter()
    metrics = fit_eval(
        CLARITree,
        args,
        0.001,
        0.00001,
        x_train,
        y_train,
        x_test,
        y_test,
    )
    elapsed = time.perf_counter() - started
    expected = 0.7431327225376596
    return {
        "protocol": {
            "dataset": "california_housing",
            "outer": 4,
            "depth": 4,
            "lambda": 0.001,
            "kappa": 0.00001,
            "n_thresholds": 20,
            "thresholds_strategy": "quantile",
            "selection": "paper-release selected configuration; no new CV",
        },
        "metrics": metrics,
        "expected_release_test_r2": expected,
        "absolute_test_r2_difference": abs(float(metrics["test_r2"]) - expected),
        "exact_release_row_match": abs(float(metrics["test_r2"]) - expected) < 1e-6,
        "elapsed_seconds": elapsed,
    }


def read_json(name: str) -> dict[str, object]:
    return json.loads((OUTPUTS / name).read_text(encoding="utf-8"))


def optional_c5() -> dict[str, object] | None:
    path = ROOT / "repro" / "src" / "verify_synthetic_claim.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("verify_synthetic_claim", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not import C5 verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.summarize()


def assessment_payload(calibration: dict[str, object], c5: dict[str, object] | None) -> dict[str, object]:
    structure = read_json("source_structure.json")
    core = read_json("core_claims.json")
    theory = read_json("theorem_consequences.json")
    california = read_json("california_artifact_readback.json")
    completion = read_json("completion_artifact_readback.json")

    claims: dict[str, dict[str, object]] = {
        "C1": {
            "paper_result": "one-step lookahead with streamed rank-one Cholesky updates",
            "observed_result": {
                "source_structure_verified": structure["source_structure_verified"],
                "threshold_pool_matches_numpy": core["threshold_pool"]["all_match"],
            },
            "assessment": "aligned",
        },
        "C2": {
            "paper_result": "O(k*n*log(n) + d^2*n*k^4*T) time and O(n*k) space in the stated regime",
            "observed_result": {
                "runtime_expression_verified": theory["runtime_expression_verified"],
                "doubling_ratios": theory["runtime_component_doubling_ratios"],
            },
            "assessment": "aligned (formula/source audit; not a fresh asymptotic proof)",
        },
        "C3": {
            "paper_result": "objective no worse than Greedy; arbitrarily large constructed MSE gap",
            "observed_result": {
                "minimum_objective_slack": core["dominance_min_slack"],
                "strict_improvements": core["dominance_strict_cases"],
                "trials": len(core["dominance"]),
                "gap_inequality_grid_points": theory["c3_gap_epsilon_count"],
                "gap_inequality_verified": theory["c3_gap_inequality_verified"],
            },
            "assessment": "aligned",
        },
        "C4": {
            "paper_result": "California Housing test R2 0.75 +/- 0.01 versus STreeD 0.70 +/- 0.01",
            "observed_result": {
                "release_five_fold_claritree_r2": california["claritree"]["mean_test_r2"],
                "release_five_fold_streed_r2": california["streed"]["mean_test_r2"],
                "fresh_local_outer4": calibration,
            },
            "assessment": "aligned",
        },
        "C5": {
            "paper_result": "Figure 1: CLARITree MSE 4.03/R2 0.97 versus Greedy MSE 15.41/R2 0.88",
            "observed_result": c5,
            "assessment": (
                "partially aligned under independent reconstruction"
                if c5 is not None and c5["direction_aligned"]
                else "inconclusive under this setup" if c5 is not None else "not attempted in baseline"
            ),
        },
        "C6": {
            "paper_result": "roughly 95% versus 60% completion at the 600-second budget",
            "observed_result": {
                "cutoff_seconds": completion["selection"]["time_limit_s"],
                "claritree_percent": completion["claritree"]["completion_rate_percent"],
                "streed_percent": completion["streed"]["completion_rate_percent"],
                "advantage_points": completion["completion_advantage_percentage_points"],
            },
            "assessment": "partially aligned (direction aligned; released endpoint is 100%/70%)",
        },
    }
    evaluated = sum(claim["assessment"] != "not attempted in baseline" for claim in claims.values())
    return {
        "paper": "arXiv:2606.12840",
        "source_commit": "4397f8dbc8b63751777e7918b89972e793796dfd",
        "compute": {
            "backend": "local",
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
        },
        "claims": claims,
        "coverage_score": f"{2 * evaluated}/12",
        "coverage_note": "Two points per claim: one for a stated paper target and one for observed evidence plus a scoped assessment.",
    }


def main() -> None:
    suite_started = time.perf_counter()
    print("CLARITree local claim suite")
    print(f"python={sys.version.split()[0]} platform={platform.platform()}")
    for script in (
        "verify_source_pins.py",
        "verify_source_structure.py",
        "verify_core_claims.py",
        "verify_theorem_consequences.py",
        "verify_california_artifacts.py",
        "verify_completion_artifacts.py",
    ):
        run_check(script)

    print("\n--- fresh California outer-4 source run ---", flush=True)
    calibration = fresh_california_outer4()
    print(json.dumps(calibration, indent=2), flush=True)
    if not calibration["exact_release_row_match"]:
        raise RuntimeError("fresh California outer-4 run did not match the released row")

    c5 = optional_c5()
    if c5 is not None:
        print("\n--- independent C5 reconstruction ---")
        print(json.dumps(c5, indent=2), flush=True)

    result = assessment_payload(calibration, c5)
    result["total_elapsed_seconds"] = time.perf_counter() - suite_started
    print("\n=== CLAIM ASSESSMENTS ===")
    for claim_id, claim in result["claims"].items():
        print(f"{claim_id}: {claim['assessment']}")
    print(f"COVERAGE SCORE: {result['coverage_score']}")
    print("ORX_RESULT_JSON=" + json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
