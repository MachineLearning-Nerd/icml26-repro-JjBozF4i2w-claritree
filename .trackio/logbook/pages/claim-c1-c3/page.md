# Claim C1-C3


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_06a9336d54b7", "created_at": "2026-07-22T10:45:02+00:00", "title": "Algorithm and theory evidence"}
-->
C1 source structure has CLARITree recursion, greedy lookahead, and paired rank-one Cholesky updates. Independent NumPy threshold checks and ten deterministic CLARITree-vs-Greedy cases pass. C2/C3 retain the exact runtime expression and displayed gap inequality checks.


---
<!-- trackio-cell
{"type": "code", "id": "cell_8ec10951901a", "created_at": "2026-07-22T10:45:15+00:00", "title": "C1-C3 independent verifier", "command": ["python", "repro/src/verify_source_structure.py"], "exit_code": 0, "duration_s": 0.058}
-->
````bash
$ python repro/src/verify_source_structure.py
````

exit 0 · 0.1s


````python title=verify_source_structure.py
"""Fail-closed structural audit of the pinned C++ implementation for C1."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTATION = ROOT / "upstream/src/clari_tree.cpp"


def summarize() -> dict[str, object]:
    source = IMPLEMENTATION.read_text(encoding="utf-8")
    requirements = {
        "claritree_recursive_fit": "CLARITree::recursive_fit",
        "greedy_lookahead_call": "Greedy::recursive_fit",
        "left_rank_one_update": "llt_left.rankUpdate(",
        "right_rank_one_update": "llt_right.rankUpdate(",
        "quantile_threshold_builder": "make_quantile_thresholds",
    }
    matches = {name: token in source for name, token in requirements.items()}
    return {
        "source": str(IMPLEMENTATION.relative_to(ROOT)),
        "requirements": requirements,
        "matches": matches,
        "source_structure_verified": all(matches.values()),
        "interpretation": (
            "The pinned implementation contains CLARITree recursion, its greedy "
            "lookahead subroutine, and both streaming rank-one Cholesky updates."
        ),
    }


def main() -> None:
    payload = summarize()
    if not payload["source_structure_verified"]:
        raise SystemExit(json.dumps(payload, indent=2))
    output = ROOT / "outputs" / "source_structure.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

````


````output
{
  "source": "upstream/src/clari_tree.cpp",
  "requirements": {
    "claritree_recursive_fit": "CLARITree::recursive_fit",
    "greedy_lookahead_call": "Greedy::recursive_fit",
    "left_rank_one_update": "llt_left.rankUpdate(",
    "right_rank_one_update": "llt_right.rankUpdate(",
    "quantile_threshold_builder": "make_quantile_thresholds"
  },
  "matches": {
    "claritree_recursive_fit": true,
    "greedy_lookahead_call": true,
    "left_rank_one_update": true,
    "right_rank_one_update": true,
    "quantile_threshold_builder": true
  },
  "source_structure_verified": true,
  "interpretation": "The pinned implementation contains CLARITree recursion, its greedy lookahead subroutine, and both streaming rank-one Cholesky updates."
}

````


---
<!-- trackio-cell
{"type": "code", "id": "cell_441f70b358be", "created_at": "2026-07-22T10:45:16+00:00", "title": "C1-C3 dynamic verifier", "command": ["python", "repro/src/verify_core_claims.py"], "exit_code": 0, "duration_s": 0.165}
-->
````bash
$ python repro/src/verify_core_claims.py
````

exit 0 · 0.2s


````python title=verify_core_claims.py
"""Independent CPU checks for CLARITree's source-level algorithmic claims.

This verifier does not modify the author tree.  It validates the released
quantile threshold contract independently, then asks the pinned C++ extension
to fit matched CLARITree/Greedy pairs on deterministic nonlinear data.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from clari_tree import CLARITree, Greedy


ROOT = Path(__file__).resolve().parents[2]


def expected_quantiles(values: np.ndarray, count: int) -> list[float]:
    """Independent NumPy implementation of the source's linear quantiles."""
    return [float(np.quantile(values, index / (count + 1), method="linear")) for index in range(1, count + 1)]


def options() -> dict[str, object]:
    return {
        "kappa": 1e-3,
        "depth": 3,
        "lambda_": 1e-3,
        "n_thresholds": 7,
        "thresholds_strategy": "quantile",
        "verbose": False,
        "min_leaf_node_size": 0,
    }


def make_data(seed: int, *, shuffled: bool = False) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    features = rng.normal(size=(72, 4))
    target = 1.7 * features[:, 0] - 0.8 * features[:, 1] * features[:, 2] + rng.normal(scale=0.1, size=72)
    if shuffled:
        target = rng.permutation(target)
    return features, target


def check_threshold_pool() -> dict[str, object]:
    features, target = make_data(17)
    model = CLARITree(**options())
    model.fit(features, target)
    observed = model.get_threshold_pool()
    checks = []
    # Bindings expose source's post-intercept feature numbering, so raw column j
    # is at key j + 1.
    for raw_feature in range(features.shape[1]):
        expected = expected_quantiles(np.sort(features[:, raw_feature]), 7)
        actual = [float(value) for value in observed[raw_feature + 1]]
        maximum_error = max(abs(left - right) for left, right in zip(expected, actual))
        checks.append({"feature": raw_feature, "max_abs_error": maximum_error, "count": len(actual)})
    return {"all_match": all(row["count"] == 7 and row["max_abs_error"] < 1e-12 for row in checks), "features": checks}


def check_dominance() -> list[dict[str, object]]:
    records = []
    for seed in range(10):
        features, target = make_data(seed)
        greedy = Greedy(**options())
        claritree = CLARITree(**options())
        greedy_loss = float(greedy.fit(features, target))
        claritree_loss = float(claritree.fit(features, target))
        records.append(
            {
                "seed": seed,
                "greedy_loss": greedy_loss,
                "claritree_loss": claritree_loss,
                "slack": greedy_loss - claritree_loss,
                "greedy_leaves": int(greedy.n_leaves()),
                "claritree_leaves": int(claritree.n_leaves()),
            }
        )
    return records


def check_negative_control() -> dict[str, float]:
    features, target = make_data(3, shuffled=True)
    model = CLARITree(**options())
    model.fit(features, target)
    predictions = np.asarray(model.predict(features))
    baseline = float(np.sum((target - target.mean()) ** 2))
    mse = float(np.mean((target - predictions) ** 2))
    r2 = 1.0 - float(np.sum((target - predictions) ** 2)) / baseline
    return {"train_mse": mse, "train_r2": r2}


def main() -> None:
    threshold = check_threshold_pool()
    dominance = check_dominance()
    negative = check_negative_control()
    payload = {
        "threshold_pool": threshold,
        "dominance": dominance,
        "dominance_min_slack": min(float(row["slack"]) for row in dominance),
        "dominance_strict_cases": sum(float(row["slack"]) > 1e-10 for row in dominance),
        "negative_control": negative,
    }
    if not threshold["all_match"] or payload["dominance_min_slack"] < -1e-10:
        raise SystemExit(json.dumps(payload, indent=2))
    output = ROOT / "outputs" / "core_claims.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

````


````output
{
  "threshold_pool": {
    "all_match": true,
    "features": [
      {
        "feature": 0,
        "max_abs_error": 0.0,
        "count": 7
      },
      {
        "feature": 1,
        "max_abs_error": 0.0,
        "count": 7
      },
      {
        "feature": 2,
        "max_abs_error": 0.0,
        "count": 7
      },
      {
        "feature": 3,
        "max_abs_error": 0.0,
        "count": 7
      }
    ]
  },
  "dominance": [
    {
      "seed": 0,
      "greedy_loss": 5.029315203703277,
      "claritree_loss": 5.029315203703277,
      "slack": 0.0,
      "greedy_leaves": 3,
      "claritree_leaves": 3
    },
    {
      "seed": 1,
      "greedy_loss": 6.250154451494475,
      "claritree_loss": 5.337291036434288,
      "slack": 0.9128634150601869,
      "greedy_leaves": 3,
      "claritree_leaves": 3
    },
    {
      "seed": 2,
      "greedy_loss": 6.2092615832929265,
      "claritree_loss": 4.438526944045815,
      "slack": 1.7707346392471113,
      "greedy_leaves": 2,
      "claritree_leaves": 3
    },
    {
      "seed": 3,
      "greedy_loss": 14.315211662856228,
      "claritree_loss": 8.998303035057635,
      "slack": 5.316908627798593,
      "greedy_leaves": 2,
      "claritree_leaves": 3
    },
    {
      "seed": 4,
      "greedy_loss": 4.962750652429148,
      "claritree_loss": 4.962750652429148,
      "slack": 0.0,
      "greedy_leaves": 3,
      "claritree_leaves": 3
    },
    {
      "seed": 5,
      "greedy_loss": 16.82344814208143,
      "claritree_loss": 8.592157962775442,
      "slack": 8.231290179305986,
      "greedy_leaves": 2,
      "claritree_leaves": 3
    },
    {
      "seed": 6,
      "greedy_loss": 7.4233039254025535,
      "claritree_loss": 7.4233039254025535,
      "slack": 0.0,
      "greedy_leaves": 3,
      "claritree_leaves": 3
    },
    {
      "seed": 7,
      "greedy_loss": 8.505540623237662,
      "claritree_loss": 8.505540623237662,
      "slack": 0.0,
      "greedy_leaves": 3,
      "claritree_leaves": 3
    },
    {
      "seed": 8,
      "greedy_loss": 5.534629443249699,
      "claritree_loss": 5.534629443249699,
      "slack": 0.0,
      "greedy_leaves": 3,
      "claritree_leaves": 3
    },
    {
      "seed": 9,
      "greedy_loss": 7.330555327496852,
      "claritree_loss": 7.330555327496852,
      "slack": 0.0,
      "greedy_leaves": 3,
      "claritree_leaves": 3
    }
  ],
  "dominance_min_slack": 0.0,
  "dominance_strict_cases": 4,
  "negative_control": {
    "train_mse": 2.824527186410159,
    "train_r2": 0.3202856212898849
  }
}

````


---
<!-- trackio-cell
{"type": "code", "id": "cell_260648758b3c", "created_at": "2026-07-22T10:45:17+00:00", "title": "C2-C3 theorem consequences", "command": ["python", "repro/src/verify_theorem_consequences.py"], "exit_code": 0, "duration_s": 0.168}
-->
````bash
$ python repro/src/verify_theorem_consequences.py
````

exit 0 · 0.2s


````python title=verify_theorem_consequences.py
"""Independent arithmetic checks for the explicit C2/C3 theorem consequences.

This is intentionally not presented as a fresh proof of the paper's theorems.
It validates the stated runtime decomposition and the final C3 gap inequality
used in the paper's proof over a wide deterministic epsilon grid.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]


def runtime_bound(n: int, d: int, k: int, thresholds: int) -> int:
    """Theorem 5.1's non-logarithmic operation-count expression."""
    return d * d * n * k**4 * thresholds


def summarize() -> dict[str, object]:
    epsilons = np.geomspace(1e-8, 0.49, 200)
    ratios = (1.0 - epsilons) / (2.0 * epsilons)
    claimed_lower_bounds = 1.0 / (4.0 * epsilons)
    gap_margin = ratios - claimed_lower_bounds

    # Positive integer monotonicity checks guard the d^2*n*k^4*T component
    # against transcription mistakes in the independent evaluator.
    base = runtime_bound(n=10, d=2, k=2, thresholds=3)
    doubled = {
        "n": runtime_bound(n=20, d=2, k=2, thresholds=3) / base,
        "d": runtime_bound(n=10, d=4, k=2, thresholds=3) / base,
        "k": runtime_bound(n=10, d=2, k=4, thresholds=3) / base,
        "thresholds": runtime_bound(n=10, d=2, k=2, thresholds=6) / base,
    }
    return {
        "theorem_5_1_runtime_expression": "O(k*n*log(n) + d^2*n*k^4*T)",
        "runtime_component_doubling_ratios": doubled,
        "runtime_expression_verified": doubled == {"n": 2.0, "d": 4.0, "k": 16.0, "thresholds": 2.0},
        "c3_gap_epsilon_count": int(epsilons.size),
        "c3_smallest_gap_margin": float(gap_margin.min()),
        "c3_gap_inequality_verified": bool(np.all(gap_margin > 0.0)),
        "interpretation": (
            "For every tested epsilon in (0, 1/2), the proof's displayed "
            "(1-epsilon)/(2epsilon) lower ratio strictly exceeds 1/(4epsilon)."
        ),
    }


def main() -> None:
    payload = summarize()
    if not payload["runtime_expression_verified"] or not payload["c3_gap_inequality_verified"]:
        raise SystemExit(json.dumps(payload, indent=2))
    output = ROOT / "outputs" / "theorem_consequences.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

````


````output
{
  "theorem_5_1_runtime_expression": "O(k*n*log(n) + d^2*n*k^4*T)",
  "runtime_component_doubling_ratios": {
    "n": 2.0,
    "d": 4.0,
    "k": 16.0,
    "thresholds": 2.0
  },
  "runtime_expression_verified": true,
  "c3_gap_epsilon_count": 200,
  "c3_smallest_gap_margin": 0.010204081632653073,
  "c3_gap_inequality_verified": true,
  "interpretation": "For every tested epsilon in (0, 1/2), the proof's displayed (1-epsilon)/(2epsilon) lower ratio strictly exceeds 1/(4epsilon)."
}

````
