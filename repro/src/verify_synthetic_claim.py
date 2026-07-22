"""Independent reconstruction of the under-specified Figure 1 DGP.

This is intentionally not an exact author-source rerun. Section D.3 specifies
the distribution family but omits the numerical configuration and releases no
generator. Every substituted value is therefore declared in ``PROTOCOL``.
"""

from __future__ import annotations

import time

import numpy as np

from clari_tree import CLARITree, Greedy


PROTOCOL: dict[str, object] = {
    "status": "independent reconstruction; not an author-source rerun",
    "total_samples": 1000,
    "train_fraction": 0.8,
    "features_k": 4,
    "groups_g": 4,
    "correlation_rho": 0.5,
    "noise_sigma": 2.0,
    "depth": 2,
    "lambda": 0.001,
    "kappa": 0.001,
    "thresholds": 20,
    "threshold_strategy": "quantile",
    "seeds": [0, 1, 2, 3, 4],
    "substitutions": (
        "n, split, k, G, rho, sigma, seeds, and model hyperparameters are absent "
        "from the Figure 1 protocol. sigma=2 places the irreducible variance on "
        "the paper headline's MSE scale; no parameter was fit to an observed run."
    ),
}


def r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    residual = float(np.sum((y_true - y_pred) ** 2))
    total = float(np.sum((y_true - np.mean(y_true)) ** 2))
    return 1.0 - residual / total


def make_data(seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = int(PROTOCOL["total_samples"])
    k = int(PROTOCOL["features_k"])
    groups = int(PROTOCOL["groups_g"])
    rho = float(PROTOCOL["correlation_rho"])
    sigma = float(PROTOCOL["noise_sigma"])

    indices = np.arange(k)
    covariance = rho ** np.abs(indices[:, None] - indices[None, :])
    features = rng.multivariate_normal(np.zeros(k), covariance, size=n)
    boundaries = np.quantile(
        features[:, 0], [group / groups for group in range(1, groups)]
    )
    memberships = np.searchsorted(boundaries, features[:, 0], side="right")

    decay = np.exp(-2.0 * np.arange(k) / max(k - 1, 1))
    base_coefficients = rng.normal(size=(groups, k))
    scales = 1.0 + 0.5 * np.arange(groups)
    coefficients = scales[:, None] * decay[None, :] * base_coefficients
    target = np.einsum("ij,ij->i", features, coefficients[memberships])
    target += rng.normal(scale=sigma, size=n)

    order = rng.permutation(n)
    train_size = int(float(PROTOCOL["train_fraction"]) * n)
    train, test = order[:train_size], order[train_size:]
    return features[train], target[train], features[test], target[test]


def evaluate(seed: int) -> dict[str, float | int]:
    x_train, y_train, x_test, y_test = make_data(seed)
    options = {
        "depth": int(PROTOCOL["depth"]),
        "lambda_": float(PROTOCOL["lambda"]),
        "kappa": float(PROTOCOL["kappa"]),
        "n_thresholds": int(PROTOCOL["thresholds"]),
        "thresholds_strategy": str(PROTOCOL["threshold_strategy"]),
        "min_leaf_node_size": 0,
        "verbose": False,
    }
    record: dict[str, float | int] = {"seed": seed}
    for name, model_type in (("greedy", Greedy), ("claritree", CLARITree)):
        model = model_type(**options)
        started = time.perf_counter()
        model.fit(x_train, y_train)
        elapsed = time.perf_counter() - started
        prediction = np.asarray(model.predict(x_test))
        record[f"{name}_test_mse"] = float(np.mean((y_test - prediction) ** 2))
        record[f"{name}_test_r2"] = r2(y_test, prediction)
        record[f"{name}_train_seconds"] = elapsed
        record[f"{name}_leaves"] = int(model.n_leaves())
    record["mse_improvement"] = float(record["greedy_test_mse"]) - float(
        record["claritree_test_mse"]
    )
    return record


def summarize() -> dict[str, object]:
    records = [evaluate(seed) for seed in PROTOCOL["seeds"]]
    greedy_mse = np.array([float(row["greedy_test_mse"]) for row in records])
    claritree_mse = np.array([float(row["claritree_test_mse"]) for row in records])
    greedy_r2 = np.array([float(row["greedy_test_r2"]) for row in records])
    claritree_r2 = np.array([float(row["claritree_test_r2"]) for row in records])
    return {
        "protocol": PROTOCOL,
        "per_seed": records,
        "mean": {
            "greedy_test_mse": float(greedy_mse.mean()),
            "claritree_test_mse": float(claritree_mse.mean()),
            "greedy_test_r2": float(greedy_r2.mean()),
            "claritree_test_r2": float(claritree_r2.mean()),
            "paired_mse_improvement": float((greedy_mse - claritree_mse).mean()),
        },
        "claritree_lower_mse_seeds": int(np.sum(claritree_mse < greedy_mse - 1e-12)),
        "tied_seeds": int(np.sum(np.abs(claritree_mse - greedy_mse) <= 1e-12)),
        "direction_aligned": bool(claritree_mse.mean() < greedy_mse.mean()),
        "paper_headline": {
            "greedy_test_mse": 15.41,
            "claritree_test_mse": 4.03,
            "greedy_test_r2": 0.88,
            "claritree_test_r2": 0.97,
        },
        "exact_headline_protocol_available": False,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(summarize(), indent=2))
