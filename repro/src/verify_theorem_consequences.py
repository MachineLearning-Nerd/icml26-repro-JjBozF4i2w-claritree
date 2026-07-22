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
