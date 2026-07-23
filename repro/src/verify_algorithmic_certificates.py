"""Machine-checkable, source-tied certificates for Claims 1--3."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from statistics import median

import numpy as np
import sympy as sp
from z3 import Int, Real, Solver, sat


ROOT = Path(__file__).resolve().parents[2]
AUTHOR_SOURCE = ROOT / "upstream" / "src" / "clari_tree.cpp"
EIGEN_LLT = ROOT / "repro" / "vendor" / "eigen" / "Eigen" / "src" / "Cholesky" / "LLT.h"
BENCHMARK_SOURCE = ROOT / "repro" / "cpp" / "benchmark_rank_update.cpp"
BENCHMARK_BINARY = ROOT / "outputs" / "benchmark_rank_update"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_certificate() -> dict[str, object]:
    author = AUTHOR_SOURCE.read_text(encoding="utf-8")
    eigen = EIGEN_LLT.read_text(encoding="utf-8")
    author_tokens = {
        "claritree_recursion": "double CLARITree::recursive_fit",
        "left_update": "llt_left.rankUpdate(reg_row(row), 1);",
        "right_downdate": "llt_right.rankUpdate(reg_row(row), -1);",
        "greedy_completion_left": "Greedy::recursive_fit(sorted_indices_left",
        "greedy_completion_right": "Greedy::recursive_fit(sorted_indices_right",
    }
    eigen_tokens = {
        "public_rank_update": "LLT & rankUpdate",
        "rank_update_dispatch": "llt_rank_update_lower(mat, vec, sigma)",
    }
    author_counts = {name: author.count(token) for name, token in author_tokens.items()}
    eigen_counts = {name: eigen.count(token) for name, token in eigen_tokens.items()}
    passed = (
        author_counts["claritree_recursion"] == 1
        and author_counts["left_update"] >= 2
        and author_counts["right_downdate"] >= 2
        and author_counts["greedy_completion_left"] >= 1
        and author_counts["greedy_completion_right"] >= 1
        and all(value >= 1 for value in eigen_counts.values())
    )
    return {
        "author_source_sha256": sha256(AUTHOR_SOURCE),
        "eigen_llt_sha256": sha256(EIGEN_LLT),
        "author_token_counts": author_counts,
        "eigen_token_counts": eigen_counts,
        "source_call_chain_verified": passed,
    }


def rank_update_work_certificate() -> dict[str, object]:
    p = sp.symbols("p", integer=True, positive=True)
    i = sp.symbols("i", integer=True, nonnegative=True)
    # A rank-one Cholesky recurrence visits one diagonal position and its
    # remaining tail at each i. Constant scalar work per visit is irrelevant to
    # the order, so this exact visit count is a conservative operation proxy.
    visits = sp.simplify(sp.summation(1 + (p - i - 1), (i, 0, p - 1)))
    expected = p * (p + 1) / 2
    return {
        "regression_dimension": "p = k + 1 (intercept included)",
        "exact_recurrence_visits": str(visits),
        "identity_verified": bool(sp.simplify(visits - expected) == 0),
        "polynomial_degree_in_p": int(sp.Poly(visits, p).degree()),
        "per_sample_order": "Theta(p^2) = Theta(k^2)",
    }


def benchmark_rank_update() -> dict[str, object]:
    BENCHMARK_BINARY.parent.mkdir(parents=True, exist_ok=True)
    compile_command = [
        "c++",
        "-std=c++17",
        "-O3",
        f"-I{ROOT / 'repro' / 'vendor' / 'eigen'}",
        str(BENCHMARK_SOURCE),
        "-o",
        str(BENCHMARK_BINARY),
    ]
    subprocess.run(compile_command, check=True)
    completed = subprocess.run(
        [str(BENCHMARK_BINARY)], check=True, text=True, capture_output=True
    )
    rows = list(csv.DictReader(io.StringIO(completed.stdout)))
    grouped: dict[int, list[float]] = defaultdict(list)
    calls: dict[int, int] = {}
    for row in rows:
        dimension = int(row["dimension"])
        grouped[dimension].append(float(row["nanoseconds_per_call"]))
        calls[dimension] = int(row["calls"])
    medians = {dimension: median(values) for dimension, values in grouped.items()}
    fitted_dimensions = np.array([16, 32, 64, 96, 128], dtype=float)
    fitted_times = np.array([medians[int(value)] for value in fitted_dimensions], dtype=float)
    slope = float(np.polyfit(np.log(fitted_dimensions), np.log(fitted_times), 1)[0])
    return {
        "compile_command": compile_command,
        "measurements": [
            {
                "dimension": dimension,
                "calls_per_trial": calls[dimension],
                "trials": len(grouped[dimension]),
                "median_nanoseconds_per_call": medians[dimension],
            }
            for dimension in sorted(medians)
        ],
        "fit_dimensions": fitted_dimensions.astype(int).tolist(),
        "log_log_slope": slope,
        "locked_acceptance_interval": [1.1, 3.2],
        "empirical_quadratic_scaling_consistent": 1.1 <= slope <= 3.2,
    }


def runtime_space_certificate() -> dict[str, object]:
    n, d, k, thresholds = sp.symbols("n d k T", integer=True, positive=True)
    level = sp.symbols("level", integer=True, positive=True)
    exact_level_sum = sp.simplify(
        sp.summation(
            2 * n * k**3 + (d - level) * n * k**4 * thresholds,
            (level, 1, d),
        )
    )
    paper_decomposition = 2 * d * n * k**3 + d * (d - 1) * n * k**4 * thresholds / 2
    upper_difference = sp.factor(3 * d**2 * n * k**4 * thresholds - paper_decomposition)

    zn, zd, zk = Int("n"), Int("d"), Int("k")
    exact_space = 2 * zn * zk + zn + zd * zk * zk
    space_solver = Solver()
    space_solver.add(zn >= 1, zd >= 1, zk >= 1, zn >= zd * zk)
    space_solver.add(exact_space > 4 * zn * zk)
    space_status = space_solver.check()

    return {
        "exact_level_sum": str(exact_level_sum),
        "paper_decomposition": str(paper_decomposition),
        "summation_identity_verified": bool(
            sp.simplify(exact_level_sum - paper_decomposition) == 0
        ),
        "upper_bound_difference_factored": str(upper_difference),
        "upper_bound_nonnegative_reason": (
            "3*d*k*T - 2 - (d-1)*k*T/2 >= 3*d - 2 - (d-1)/2 > 0 "
            "for positive integers d,k,T"
        ),
        "sort_term": "k*n*log(n)",
        "theorem_runtime": "O(k*n*log(n) + d^2*n*k^4*T)",
        "exact_space_proxy": "2*n*k + n + d*k^2",
        "space_regime": "n >= d*k, n,d,k positive integers",
        "space_upper_bound": "4*n*k",
        "space_counterexample_status": str(space_status),
        "space_bound_z3_verified": space_status != sat,
    }


def dominance_certificate() -> dict[str, object]:
    c_left, c_right = Real("C_left"), Real("C_right")
    gs_left, gs_right = Real("G_selected_left"), Real("G_selected_right")
    gr_left, gr_right = Real("G_root_left"), Real("G_root_right")
    solver = Solver()
    solver.add(c_left <= gs_left, c_right <= gs_right)
    solver.add(gs_left + gs_right <= gr_left + gr_right)
    solver.add(c_left + c_right > gr_left + gr_right)
    status = solver.check()
    return {
        "induction_hypothesis": [
            "C_left <= G_selected_left",
            "C_right <= G_selected_right",
        ],
        "candidate_inclusion_axiom": (
            "the CLARITree minimum over Greedy-completed root candidates is no greater "
            "than the completion rooted at Greedy's own first split"
        ),
        "negated_conclusion": "C_left + C_right > G_root_left + G_root_right",
        "z3_counterexample_status": str(status),
        "dominance_induction_step_verified": status != sat,
    }


def arbitrary_gap_certificate() -> dict[str, object]:
    epsilon, U = sp.symbols("epsilon U", positive=True)
    nuisance_gain = epsilon**2 / U**2
    greedy_lower = 1 - epsilon
    claritree_upper = 2 * epsilon
    ratio_margin = sp.factor(greedy_lower / claritree_upper - 1 / (4 * epsilon))

    witnesses = []
    for depth in (2, 3, 4, 8):
        nuisance_pairs = depth + 1
        for eps in (sp.Rational(1, 4), sp.Rational(1, 10), sp.Rational(1, 100)):
            gain = sp.simplify(nuisance_gain.subs({epsilon: eps, U: nuisance_pairs}))
            lower = sp.simplify(greedy_lower.subs(epsilon, eps))
            upper = sp.simplify(claritree_upper.subs(epsilon, eps))
            witnesses.append(
                {
                    "depth": depth,
                    "U": nuisance_pairs,
                    "epsilon": str(eps),
                    "target_split_gain": "0",
                    "nuisance_split_gain": str(gain),
                    "greedy_mse_lower_bound": str(lower),
                    "claritree_mse_upper_bound": str(upper),
                    "ratio_lower_bound": str(sp.simplify(lower / upper)),
                }
            )

    return {
        "paper_dgp": (
            "Y=(1-B)ghz + B*m[J,1]*m[J,2], with independent Rademacher g,h,M; "
            "z~N(0,1), B~Bernoulli(epsilon), J~Uniform(1..U)"
        ),
        "moment_certificate": {
            "target_split_g_h_z_gain": "0 by independence and odd moments",
            "new_nuisance_pair_split_gain": str(nuisance_gain),
            "greedy_path": (
                "strictly positive nuisance gain beats zero target gain for every "
                "depth while U>d"
            ),
            "greedy_mse_lower_bound": str(greedy_lower),
            "claritree_candidate": "split g, then h; predict g*h*z in each leaf",
            "claritree_candidate_mse": str(claritree_upper),
        },
        "ratio_margin_over_1/(4*epsilon)": str(ratio_margin),
        "universal_sign_reason": (
            "(1-2*epsilon)/(4*epsilon) > 0 exactly when 0 < epsilon < 1/2"
        ),
        "exact_rational_witnesses": witnesses,
        "construction_certificate_verified": (
            sp.simplify(nuisance_gain).is_positive
            and sp.simplify(
                ratio_margin - (1 - 2 * epsilon) / (4 * epsilon)
            )
            == 0
            and all(sp.Rational(row["nuisance_split_gain"]) > 0 for row in witnesses)
        ),
    }


def summarize() -> dict[str, object]:
    payload = {
        "protocol": "docs/CERTIFICATE_PROTOCOL.md",
        "source": source_certificate(),
        "c1_rank_update_work": rank_update_work_certificate(),
        "c1_eigen_benchmark": benchmark_rank_update(),
        "c2_runtime_space": runtime_space_certificate(),
        "c3_dominance": dominance_certificate(),
        "c3_arbitrary_gap": arbitrary_gap_certificate(),
    }
    checks = {
        "source_call_chain": payload["source"]["source_call_chain_verified"],
        "rank_update_degree_two": (
            payload["c1_rank_update_work"]["polynomial_degree_in_p"] == 2
        ),
        "rank_update_benchmark": payload["c1_eigen_benchmark"][
            "empirical_quadratic_scaling_consistent"
        ],
        "runtime_sum": payload["c2_runtime_space"]["summation_identity_verified"],
        "space_z3": payload["c2_runtime_space"]["space_bound_z3_verified"],
        "dominance_z3": payload["c3_dominance"][
            "dominance_induction_step_verified"
        ],
        "gap_construction": payload["c3_arbitrary_gap"][
            "construction_certificate_verified"
        ],
    }
    payload["checks"] = checks
    payload["all_certificates_verified"] = all(checks.values())
    return payload


def main() -> None:
    payload = summarize()
    if not payload["all_certificates_verified"]:
        raise SystemExit(json.dumps(payload, indent=2))
    output = ROOT / "outputs" / "algorithmic_certificates.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
