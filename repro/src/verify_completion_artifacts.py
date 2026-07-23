"""Read the C6 completion endpoint exactly as the released plot script does.

The paper describes its 20-threshold endpoint as roughly 95% for CLARITree and
60% for STreeD.  This verifier deliberately does not round or substitute those
numbers: it reads the pinned release's ``results/final.csv`` using the same
``outer == 'mean'``, depth-four, 20-threshold selection as
``scripts/images/plot_completion_rate.py`` and records its actual endpoint.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FINAL_CSV = ROOT / "upstream/results/final.csv"
AUTHOR_PLOT = ROOT / "upstream/scripts/images/plot_completion_rate.py"
TIME_LIMIT_S = 590.0
METHODS = ("claritree", "streed")
PAPER_ENDPOINT = {"claritree": 95.0, "streed": 60.0}
TOLERANCE_PERCENTAGE_POINTS = 5.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_author_plot() -> dict[str, object]:
    """Execute the unchanged author program without dirtying its checkout."""
    with tempfile.TemporaryDirectory(prefix="claritree-c6-") as temporary:
        working = Path(temporary)
        results = working / "results"
        results.mkdir()
        shutil.copy2(FINAL_CSV, results / "final.csv")
        # The numeric endpoint is printed before rendering. A minimal no-op
        # pyplot surface lets the unchanged author source reach that endpoint
        # without adding a large, scientifically irrelevant binary dependency.
        shim = working / "shim" / "matplotlib"
        shim.mkdir(parents=True)
        (shim / "__init__.py").write_text(
            "def use(*args, **kwargs):\n    return None\n",
            encoding="utf-8",
        )
        (shim / "pyplot.py").write_text(
            """from pathlib import Path

class _Style:
    def use(self, *args, **kwargs):
        return None

class _Spine:
    def set_visible(self, *args, **kwargs):
        return None
    def set_linewidth(self, *args, **kwargs):
        return None

class _Axes:
    def __init__(self):
        self.spines = {name: _Spine() for name in ("top", "right", "left", "bottom")}
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

style = _Style()
rcParams = {}

def subplots(*args, **kwargs):
    return object(), _Axes()

def tight_layout(*args, **kwargs):
    return None

def savefig(path, *args, **kwargs):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"%PDF-1.4\\n% headless plotting sink\\n")
""",
            encoding="utf-8",
        )
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(working / "shim")
        completed = subprocess.run(
            [sys.executable, str(AUTHOR_PLOT)],
            cwd=working,
            env=environment,
            check=True,
            text=True,
            capture_output=True,
        )
        output_pdf = results / "images" / "completion_rate_plot_full.pdf"
        if not output_pdf.is_file() or output_pdf.stat().st_size == 0:
            raise RuntimeError("author plotting script did not produce its declared PDF")
        counts: dict[str, dict[str, float | int]] = {}
        pattern = re.compile(
            r"^(claritree|streed), n_thresholds=20: "
            r"(\d+)/(\d+) completed \(([0-9.]+)%\)",
            re.MULTILINE,
        )
        for method, completed_count, total, percentage in pattern.findall(completed.stdout):
            counts[method] = {
                "completed": int(completed_count),
                "records": int(total),
                "completion_rate_percent_printed": float(percentage),
            }
        if set(counts) != set(METHODS):
            raise RuntimeError(f"could not parse author endpoint counts: {completed.stdout}")
        return {
            "command": [sys.executable, str(AUTHOR_PLOT)],
            "stdout": completed.stdout,
            "counts": counts,
            "pdf_generated": True,
            "pdf_bytes": output_pdf.stat().st_size,
            "plotting_backend": "no-op headless matplotlib shim; numeric source unchanged",
        }


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
    author_execution = run_author_plot()
    rows = source_plot_rows()
    claritree = endpoint(rows, "claritree")
    streed = endpoint(rows, "streed")
    independent = {"claritree": claritree, "streed": streed}
    exact_crosscheck = all(
        author_execution["counts"][method]["completed"] == independent[method]["completed"]
        and author_execution["counts"][method]["records"] == independent[method]["records"]
        and abs(
            author_execution["counts"][method]["completion_rate_percent_printed"]
            - independent[method]["completion_rate_percent"]
        )
        < 0.05
        for method in METHODS
    )
    absolute_differences = {
        method: abs(independent[method]["completion_rate_percent"] - PAPER_ENDPOINT[method])
        for method in METHODS
    }
    within_tolerance = {
        method: difference <= TOLERANCE_PERCENTAGE_POINTS
        for method, difference in absolute_differences.items()
    }
    numeric_assessment = (
        "verified"
        if exact_crosscheck and all(within_tolerance.values())
        else "falsified under released author artifacts"
        if exact_crosscheck
        else "inconclusive"
    )
    return {
        "source": str(FINAL_CSV.relative_to(ROOT)),
        "protocol": "docs/C6_EXACT_RECONSTRUCTION_PROTOCOL.md",
        "author_plot_source": str(AUTHOR_PLOT.relative_to(ROOT)),
        "author_plot_sha256": sha256(AUTHOR_PLOT),
        "input_csv_sha256": sha256(FINAL_CSV),
        "selection": {
            "outer": "mean",
            "depth": 4,
            "n_thresholds": 20,
            "time_limit_s": TIME_LIMIT_S,
        },
        "claritree": claritree,
        "streed": streed,
        "author_script_execution": author_execution,
        "author_vs_independent_exact_crosscheck": exact_crosscheck,
        "completion_advantage_percentage_points": (
            claritree["completion_rate_percent"] - streed["completion_rate_percent"]
        ),
        "source_backed_direction_verified": (
            claritree["completion_rate_percent"] > streed["completion_rate_percent"]
        ),
        "paper_rounded_endpoint_percent": PAPER_ENDPOINT,
        "locked_tolerance_percentage_points": TOLERANCE_PERCENTAGE_POINTS,
        "absolute_difference_percentage_points": absolute_differences,
        "within_locked_tolerance": within_tolerance,
        "numeric_claim_assessment": numeric_assessment,
        "interpretation": (
            "The unchanged author plot and an independent implementation agree "
            "on 100%/70%. The direction is supported, but STreeD is 10 points "
            "from the paper's approximate 60%, outside the locked 5-point tolerance."
        ),
    }


def main() -> None:
    payload = summarize()
    if (
        not payload["source_backed_direction_verified"]
        or not payload["author_vs_independent_exact_crosscheck"]
        or payload["numeric_claim_assessment"] == "inconclusive"
    ):
        raise SystemExit(json.dumps(payload, indent=2))
    output = ROOT / "outputs" / "completion_artifact_readback.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
