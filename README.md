# CLARITree six-claim reproduction — 12/12 evidence coverage

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/blob/main/notebooks/claritree_reproduction.py)

We tested all six anchored claims in *CLARITree: Cholesky and Lookahead
Accelerations for Regression with Interpretable Piecewise Linear Trees*
([arXiv:2606.12840](https://arxiv.org/abs/2606.12840)) on the agreed local
machine. The assessment is **C1–C4 aligned; C5–C6 partially aligned**, giving
**12/12 coverage points** (a stated paper target and scoped observed evidence
for each claim). This is complete coverage, not a claim that every published
number matched.

The strongest fresh result is California Housing outer-4: paper/release
`R² = 0.7431327225376596`, observed `0.7431327225376608` (absolute difference
`1.22e-15`). The released five-fold comparison is `0.74994` for CLARITree
versus `0.70485` for STreeD. The independently reconstructed Figure 1 setup
preserved the direction but not the magnitude: observed MSE `4.630` versus
Greedy `4.722`, while the paper reports `4.03` versus `15.41`. The paper omits
the exact Figure 1 generator settings and artifacts, so we declare substituted
`n=1000`, 80/20 split, four features/regimes, `rho=.5`, `sigma=2`, five seeds,
depth 2, and fixed regularization rather than presenting it as an exact rerun.

Compute: local CPU, Apple arm64, 8 logical CPUs, Python 3.12.11 with pip; no
GPU. The final formal run used 202.0 seconds for the scientific checks and
7m22s wall time including clean dependency and C++ builds.

- [Illustrated claim-by-claim report](reports/claritree-6-claim-reproduction/report.md)
- [Self-contained interactive tutorial](notebooks/claritree_reproduction.py)

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| [`main`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/tree/main) | Public README, report, figures, and notebook | Not run as an experiment (publication surface) | Publishes the evidence produced on immutable experiment branches | No experiment compute |
| [`pinned-source-baseline-c1-c4-and-c6`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/tree/orx/pinned-source-baseline-c1-c4-and-c6) | Baseline: pinned author source, C1–C4 and C6 suite | `bash repro/run_local_claim_suite.sh` | Setup stopped before scientific checks: pip's pybind11 CMake path was not discoverable | Local CPU; 2m00s wall |
| [`resolve-pip-build-paths`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/tree/orx/resolve-pip-build-paths) | Pass the installed pybind11 CMake directory explicitly | `bash repro/run_local_claim_suite.sh` | C1–C4 and C6 evaluated; 10/12 coverage | Local CPU; 7m37s wall |
| [`independent-figure-1-reconstruction`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/tree/orx/independent-figure-1-reconstruction) | Add declared five-seed C5 reconstruction and run all six claims | `bash repro/run_local_claim_suite.sh` | **12/12**; C1–C4 aligned, C5–C6 partially aligned | Local CPU; 7m22s wall |

---

# CLARITree reproducibility workspace

OpenReview: `JjBozF4i2w`
Paper: *CLARITree: Cholesky and Lookahead Accelerations for Regression with
Interpretable Piecewise Linear Trees*

## Status

Completed CPU-only, six-claim reproduction. The author release is pinned at
`Yixiao-Wang-Stats/CLARITree@4397f8dbc8b63751777e7918b89972e793796dfd`.

The release contains the C++ implementation, five-fold data splits, experiment
runners, baseline drivers, and raw result tables. The first exact C++ smoke run
on the released Auction outer-0 split succeeded: CLARITree test R² `0.937706`
versus greedy `0.919556`.

`repro/vendor/eigen` is Eigen `3.4.0` at
`3147391d946bb4b6c68edd901f2add6ac1f31f8c`, supplied only to satisfy the
author release's documented header dependency; the upstream tree is not edited.

## Scope

The formal suite covers anchored C1--C6. Anchored C5's synthetic data generator
is specified only in outline and absent from the release; its declared
independent reconstruction is never labelled an unmodified author-source rerun.

For C6, the release's own plot-input selection currently reads as `100.0%`
completion for CLARITree and `70.0%` for STreeD at its 590-second cutoff. That
validates the direction of the reported advantage, while preserving the
distinction from the paper's rounded `95%`/`60%` description.

## Run the formal claim suite

Run from this directory:

```bash
bash repro/run_local_claim_suite.sh
```

This creates a clean `.venv`, installs the pinned build requirements with pip,
materializes both source pins, builds the C++ extension, performs a fresh
California outer-4 fit, and prints the per-claim assessments plus the 12/12
coverage score.

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
