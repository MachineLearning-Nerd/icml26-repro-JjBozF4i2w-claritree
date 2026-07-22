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
