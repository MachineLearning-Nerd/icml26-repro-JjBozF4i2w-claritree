"""Independent readback of the released California Housing C4 raw folds."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "upstream/results"
SPECS = {
    "claritree": {
        "path": RESULTS / "ours/claritree/linear_regression_tree_depth4_threshold_20/california_housing",
        "keys": ["lambda", "kappa"],
    },
    "streed": {
        "path": RESULTS / "baseline/streed/linear_regression_tree_depth4_threshold_20/california_housing",
        "keys": ["cost_complexity", "ridge_penalty", "lasso_penalty"],
    },
}


def read_folds(path: Path) -> pd.DataFrame:
    files = sorted(path.glob("outer*/california_housing_outer*_d4.csv"))
    if len(files) != 5:
        raise ValueError(f"expected five raw fold files under {path}, found {len(files)}")
    result = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)
    if set(result["outer"].astype(str)) != {f"outer_{index}" for index in range(5)}:
        raise ValueError("raw result folds do not cover outer_0 through outer_4")
    return result


def select_by_validation(rows: pd.DataFrame, keys: list[str]) -> tuple[dict[str, float], pd.DataFrame]:
    averaged = rows.groupby(keys, as_index=False, dropna=False)["val_r2"].mean()
    best = averaged.sort_values("val_r2", ascending=False, kind="stable").iloc[0]
    selected = rows.copy()
    for key in keys:
        selected = selected[selected[key].eq(best[key])]
    if len(selected) != 5:
        raise ValueError(f"expected one selected row per outer fold, found {len(selected)}")
    return {key: float(best[key]) for key in keys}, selected


def summarize(name: str) -> dict[str, object]:
    spec = SPECS[name]
    rows = read_folds(spec["path"])
    selected_parameters, selected = select_by_validation(rows, spec["keys"])
    return {
        "parameters": selected_parameters,
        "mean_validation_r2": float(selected["val_r2"].mean()),
        "mean_test_r2": float(selected["test_r2"].mean()),
        "std_test_r2": float(selected["test_r2"].std(ddof=1)),
        "mean_train_time_s": float(selected["train_time_s"].mean()),
        "max_train_time_s": float(selected["train_time_s"].max()),
        "selected_folds": selected[["outer", "val_r2", "test_r2", "train_time_s"]].to_dict(orient="records"),
    }


def main() -> None:
    claritree = summarize("claritree")
    streed = summarize("streed")
    payload = {
        "claritree": claritree,
        "streed": streed,
        "r2_advantage": claritree["mean_test_r2"] - streed["mean_test_r2"],
        "source_claim_c4_verified": claritree["mean_test_r2"] >= 0.745 and streed["mean_test_r2"] <= 0.71,
    }
    if not payload["source_claim_c4_verified"]:
        raise SystemExit(json.dumps(payload, indent=2))
    output = ROOT / "outputs" / "california_artifact_readback.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
