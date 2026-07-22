# Claim C4


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_d9374bcfd13b", "created_at": "2026-07-22T10:45:03+00:00", "title": "California fixed-split result"}
-->
Released five-fold aggregation gives CLARITree R2 0.74994 +/- 0.01006 versus STreeD 0.70485 +/- 0.00803. CPU-upgrade fixed outer-4 source driver reproduces test R2 0.7431327225376596 exactly.


---
<!-- trackio-cell
{"type": "code", "id": "cell_fe6cc6a0e437", "created_at": "2026-07-22T10:45:18+00:00", "title": "C4 raw-fold readback", "command": ["python", "repro/src/verify_california_artifacts.py"], "exit_code": 0, "duration_s": 0.419}
-->
````bash
$ python repro/src/verify_california_artifacts.py
````

exit 0 · 0.4s


````python title=verify_california_artifacts.py
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

````


````output
{
  "claritree": {
    "parameters": {
      "lambda": 0.001,
      "kappa": 1e-05
    },
    "mean_validation_r2": 0.7478730375384298,
    "mean_test_r2": 0.7499375138107127,
    "std_test_r2": 0.01006107119945698,
    "mean_train_time_s": 69.51568279266357,
    "max_train_time_s": 72.01430749893188,
    "selected_folds": [
      {
        "outer": "outer_0",
        "val_r2": 0.7501668552429583,
        "test_r2": 0.7379695012837046,
        "train_time_s": 72.01430749893188
      },
      {
        "outer": "outer_1",
        "val_r2": 0.7455145901443112,
        "test_r2": 0.7487050779042377,
        "train_time_s": 67.24123215675354
      },
      {
        "outer": "outer_2",
        "val_r2": 0.739716643425082,
        "test_r2": 0.7625610495806185,
        "train_time_s": 69.6990795135498
      },
      {
        "outer": "outer_3",
        "val_r2": 0.7480328895457488,
        "test_r2": 0.7573192177473433,
        "train_time_s": 70.14826273918152
      },
      {
        "outer": "outer_4",
        "val_r2": 0.7559342093340485,
        "test_r2": 0.7431327225376596,
        "train_time_s": 68.47553205490112
      }
    ]
  },
  "streed": {
    "parameters": {
      "cost_complexity": 0.0001,
      "ridge_penalty": 1e-05,
      "lasso_penalty": 0.001
    },
    "mean_validation_r2": 0.7153275999946037,
    "mean_test_r2": 0.7048454539571957,
    "std_test_r2": 0.008026604151455525,
    "mean_train_time_s": 599.7037266731262,
    "max_train_time_s": 599.7139205932617,
    "selected_folds": [
      {
        "outer": "outer_0",
        "val_r2": 0.7156274341197477,
        "test_r2": 0.6917992989829506,
        "train_time_s": 599.7139205932617
      },
      {
        "outer": "outer_1",
        "val_r2": 0.7159829155292723,
        "test_r2": 0.7081818799216981,
        "train_time_s": 599.7025208473206
      },
      {
        "outer": "outer_2",
        "val_r2": 0.7153878507633188,
        "test_r2": 0.7106973674942862,
        "train_time_s": 599.7097795009613
      },
      {
        "outer": "outer_3",
        "val_r2": 0.7138418992842356,
        "test_r2": 0.7109388146487083,
        "train_time_s": 599.692351102829
      },
      {
        "outer": "outer_4",
        "val_r2": 0.7157979002764442,
        "test_r2": 0.7026099087383352,
        "train_time_s": 599.7000613212585
      }
    ]
  },
  "r2_advantage": 0.04509205985351705,
  "source_claim_c4_verified": true
}

````
