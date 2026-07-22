"""Materialize and build the immutable author dependencies for an orx run."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "upstream"
EIGEN = ROOT / "repro" / "vendor" / "eigen"
EIGEN_BUILD = ROOT / "outputs" / "eigen-cmake"
EIGEN_INSTALL = ROOT / "outputs" / "eigen-install"

SOURCES = {
    UPSTREAM: (
        "https://github.com/Yixiao-Wang-Stats/CLARITree.git",
        "4397f8dbc8b63751777e7918b89972e793796dfd",
    ),
    EIGEN: (
        "https://gitlab.com/libeigen/eigen.git",
        "3147391d946bb4b6c68edd901f2add6ac1f31f8c",
    ),
}


def run(*command: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def checkout(directory: Path, url: str, commit: str) -> None:
    if not (directory / ".git").is_dir():
        directory.parent.mkdir(parents=True, exist_ok=True)
        run("git", "clone", "--filter=blob:none", url, str(directory))
    run("git", "fetch", "origin", commit, cwd=directory)
    run("git", "checkout", "--detach", commit, cwd=directory)
    observed = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=directory, text=True
    ).strip()
    dirty = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=directory, text=True
    ).strip()
    if observed != commit or dirty:
        raise RuntimeError(f"source pin mismatch for {directory}: {observed}, dirty={bool(dirty)}")


def main() -> None:
    for directory, (url, commit) in SOURCES.items():
        checkout(directory, url, commit)

    run(
        "cmake",
        "-S",
        str(EIGEN),
        "-B",
        str(EIGEN_BUILD),
        "-DCMAKE_BUILD_TYPE=Release",
        f"-DCMAKE_INSTALL_PREFIX={EIGEN_INSTALL}",
    )
    run("cmake", "--install", str(EIGEN_BUILD))

    pybind11_cmake = subprocess.check_output(
        [sys.executable, "-m", "pybind11", "--cmakedir"], text=True
    ).strip()
    if not Path(pybind11_cmake).is_dir():
        raise RuntimeError(f"pybind11 CMake directory not found: {pybind11_cmake}")

    build_env = os.environ.copy()
    build_env["CMAKE_ARGS"] = (
        f"-DCMAKE_PREFIX_PATH={EIGEN_INSTALL} "
        f"-Dpybind11_DIR={pybind11_cmake}"
    )
    run(
        sys.executable,
        "-m",
        "pip",
        "install",
        "--no-build-isolation",
        "--editable",
        str(UPSTREAM),
        env=build_env,
    )
    run(sys.executable, "-c", "import clari_tree; print('clari_tree import: ok')")


if __name__ == "__main__":
    main()
