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
