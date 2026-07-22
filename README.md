# CLARITree reproducibility workspace

OpenReview: `JjBozF4i2w`
Paper: *CLARITree: Cholesky and Lookahead Accelerations for Regression with
Interpretable Piecewise Linear Trees*

## Status

Active CPU-only reproduction. The author release is pinned at
`Yixiao-Wang-Stats/CLARITree@4397f8dbc8b63751777e7918b89972e793796dfd`.

The release contains the C++ implementation, five-fold data splits, experiment
runners, baseline drivers, and raw result tables. The first exact C++ smoke run
on the released Auction outer-0 split succeeded: CLARITree test R² `0.937706`
versus greedy `0.919556`.

`repro/vendor/eigen` is Eigen `3.4.0` at
`3147391d946bb4b6c68edd901f2add6ac1f31f8c`, supplied only to satisfy the
author release's documented header dependency; the upstream tree is not edited.

## Scope

The full source-backed gate covers anchored C1--C4 and C6. Anchored C5's
synthetic data generator is specified in the paper but absent from the release;
any independent reconstruction is kept separately and is never labelled an
unmodified author-source rerun.

For C6, the release's own plot-input selection currently reads as `100.0%`
completion for CLARITree and `70.0%` for STreeD at its 590-second cutoff. That
validates the direction of the reported advantage, while preserving the
distinction from the paper's rounded `95%`/`60%` description.

## Quick source check

Run from this directory:

```bash
python repro/src/build_and_smoke.py
python repro/src/verify_source_pins.py
python repro/src/run_publication_gate.py
```

The publication gate intentionally exits nonzero until the CPU-only
California outer-4 calibration result has been retrieved from the private
Hugging Face job artifact store. It writes `outputs/publication_gate.json` on
every run, including when fail-closed checks are incomplete.

## Rebuild from a fresh checkout

The author release and Eigen are deliberately excluded from this repository
because they are independently versioned upstream dependencies. Clone exactly
the pins in [docs/SOURCE_MANIFEST.md](docs/SOURCE_MANIFEST.md), then use Python
3.12 and a project-local environment:

```bash
git clone https://github.com/Yixiao-Wang-Stats/CLARITree.git upstream
git -C upstream checkout --detach 4397f8dbc8b63751777e7918b89972e793796dfd
git clone --branch 3.4.0 --depth 1 https://gitlab.com/libeigen/eigen.git repro/vendor/eigen
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python cmake pytest
.venv/bin/cmake -S repro/vendor/eigen -B outputs/eigen-cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$PWD/outputs/eigen-install"
.venv/bin/cmake --install outputs/eigen-cmake
CMAKE_ARGS="-DCMAKE_PREFIX_PATH=$PWD/outputs/eigen-install" uv pip install --python .venv/bin/python -e upstream
.venv/bin/python repro/src/run_publication_gate.py
```

The two retained CPU-only Job log records are small JSON evidence files in
`outputs/`: one confirms California-sized native-source memory feasibility and
one exactly reproduces the fixed outer-4 C4 score with the author experiment
driver. See [docs/CALIBRATION_SCOPE.md](docs/CALIBRATION_SCOPE.md).
