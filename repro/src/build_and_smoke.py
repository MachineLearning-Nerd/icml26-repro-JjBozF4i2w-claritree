"""Build unmodified CLARITree C++ sources with the pinned Eigen headers and smoke-run it."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "upstream"
BINARY = ROOT / "outputs" / "run_tree"


def main() -> None:
    BINARY.parent.mkdir(parents=True, exist_ok=True)
    compile_command = [
        "g++", "-std=gnu++17", "-O3", "-fopenmp",
        f"-I{ROOT / 'repro/vendor/eigen'}", f"-I{UPSTREAM / 'include'}",
        str(UPSTREAM / "src/clari_tree.cpp"),
        str(UPSTREAM / "src/clari_tree_const.cpp"),
        str(UPSTREAM / "src/main.cpp"),
        "-o", str(BINARY),
    ]
    subprocess.run(compile_command, check=True)
    subprocess.run(
        [
            str(BINARY),
            str(UPSTREAM / "data/auction/splits/outer_0/train.csv"),
            "4.0", "0.001", "0.001", "20", "quantile",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
