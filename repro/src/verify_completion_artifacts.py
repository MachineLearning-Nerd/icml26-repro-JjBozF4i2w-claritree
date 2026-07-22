"""Read the C6 completion endpoint exactly as the released plot script does.

The paper describes its 20-threshold endpoint as roughly 95% for CLARITree and
60% for STreeD.  This verifier deliberately does not round or substitute those
numbers: it reads the pinned release's ``results/final.csv`` using the same
``outer == 'mean'``, depth-four, 20-threshold selection as
``scripts/images/plot_completion_rate.py`` and records its actual endpoint.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FINAL_CSV = ROOT / "upstream/results/final.csv"
TIME_LIMIT_S = 590.0
METHODS = ("claritree", "streed")


def source_plot_rows() -> pd.DataFrame:
    """Implement the release plot's load/filter logic without importing it."""
    rows = pd.read_csv(FINAL_CSV)
    return rows[
        rows["outer"].eq("mean")
        & rows["depth"].eq(4)
        & rows["n_thresholds"].eq(20)
        & rows["method"].isin(METHODS)
    ].copy()


def endpoint(rows: pd.DataFrame, method: str) -> dict[str, float | int]:
    times = rows.loc[rows["method"].eq(method), "train_time_s"].dropna()
    times = times[times > 0]
    if times.empty:
        raise ValueError(f"no positive training times for {method}")
    completed = int((times <= TIME_LIMIT_S).sum())
    total = int(times.size)
    return {
        "records": total,
        "completed": completed,
        "completion_rate_percent": float(100.0 * completed / total),
        "minimum_train_time_s": float(times.min()),
        "maximum_train_time_s": float(times.max()),
    }


def summarize() -> dict[str, object]:
    rows = source_plot_rows()
    claritree = endpoint(rows, "claritree")
    streed = endpoint(rows, "streed")
    return {
        "source": str(FINAL_CSV.relative_to(ROOT)),
        "selection": {
            "outer": "mean",
            "depth": 4,
            "n_thresholds": 20,
            "time_limit_s": TIME_LIMIT_S,
        },
        "claritree": claritree,
        "streed": streed,
        "completion_advantage_percentage_points": (
            claritree["completion_rate_percent"] - streed["completion_rate_percent"]
        ),
        "source_backed_direction_verified": (
            claritree["completion_rate_percent"] > streed["completion_rate_percent"]
        ),
        "paper_rounded_endpoint_percent": {"claritree": 95.0, "streed": 60.0},
        "paper_rounded_endpoint_exactly_reproduced": False,
        "interpretation": (
            "The release supports the completion-rate advantage, but its exact "
            "plot-input endpoint is retained as evidence rather than relabelled "
            "as the paper's rounded 95%/60% values."
        ),
    }


def main() -> None:
    payload = summarize()
    if not payload["source_backed_direction_verified"]:
        raise SystemExit(json.dumps(payload, indent=2))
    output = ROOT / "outputs" / "completion_artifact_readback.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
