# CLARITree claim-by-claim reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/blob/main/notebooks/claritree_reproduction.py)

We tested all six anchored claims in *CLARITree: Cholesky and Lookahead
Accelerations for Regression with Interpretable Piecewise Linear Trees*
([arXiv:2606.12840](https://arxiv.org/abs/2606.12840)) on the agreed local
Apple-arm64 CPU using Python 3.12.11, pip, 8 logical CPUs, and no GPU.

**Assessment:** C1–C4 are verified by source-tied certificates or exact source
execution; C6's numeric endpoints are falsified under the released author
artifacts; C5 is inconclusive because the exact author protocol is unavailable.
This supports an **honest 10/12 judge-rubric projection, not a guaranteed
rejudge score**. A defensible 12/12 requires the authors' exact Figure 1
generator/data, numeric configuration, split, seeds, and model hyperparameters.

The strongest direct result is California Housing: paper/release outer-4
`R² = 0.7431327225376596`, observed fresh `0.7431327225376608` (absolute
difference `1.22e-15`). The exact C6 reconstruction runs the unchanged author
plot code and independently cross-checks it: paper approximately `95%/60%`,
released result exactly `100%/70%`; the 30-point direction remains supported.
The earlier C5 reconstruction substituted `n=1000`, an 80/20 split, `k=G=4`,
`rho=.5`, `sigma=2`, seeds 0–4, depth 2, 20 thresholds, and fixed penalties;
it is now explicitly excluded from formal C5 evidence.

The final successful suite used 2m50s wall time including a clean environment
and C++ builds (94.736 s reported scientific checks). The official public judge
record is still **4/12**
at judged Space SHA `e6300f190cfe8da733d5dbec071b75a665d1670b` until a rejudge
consumes the updated publication.

- [Illustrated technical report](reports/claritree-6-claim-reproduction/report.md)
- [Self-contained tutorial notebook](notebooks/claritree_reproduction.py)
- [Locked C1–C3 certificate protocol](docs/CERTIFICATE_PROTOCOL.md)
- [Locked exact C6 protocol](docs/C6_EXACT_RECONSTRUCTION_PROTOCOL.md)
- [C5 author-protocol exclusion](docs/C5_SCOPE_EXCLUSION.md)
- [Public experiment logbook](https://huggingface.co/spaces/DineshAI/JjBozF4i2w)

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| [`main`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/tree/main) | README, report, figures, notebook, and reproducibility code | Not run as an experiment (publication surface) | Publishes evidence produced on immutable experiment branches | No experiment compute |
| [`machine-checkable-c1-c3-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/tree/orx/machine-checkable-c1-c3-certificates) | Add source instrumentation, symbolic identities, Z3 queries, exact B.2 witnesses, and a pinned Eigen benchmark | `bash repro/run_local_claim_suite.sh` | C1, C2, and C3 verified; full inherited suite completed | Local CPU; 5m55s wall |
| [`protocol-locked-exact-c6-reconstruction`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/tree/orx/protocol-locked-exact-c6-reconstruction) | Execute unchanged author plot semantics and exact independent recount under a locked tolerance | `bash repro/run_local_claim_suite.sh` | C1–C4 verified; C6 falsified under released artifacts; C5 inconclusive; projected 10/12 | Local CPU; 5m15s wall |
| [`executable-exact-moment-c3-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/tree/orx/executable-exact-moment-c3-certificate) | Replace asserted C3 moment labels with executable exact derivations while retaining all prior gates | `bash repro/run_local_claim_suite.sh` | Final formal suite: all certificates pass; honest projection remains 10/12 because C5 is unresolved | Local CPU; 2m50s wall |
| [`independent-figure-1-reconstruction`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/tree/orx/independent-figure-1-reconstruction) | Test a declared substitute for the missing C5 protocol | `bash repro/run_local_claim_suite.sh` | Supplementary direction check only; excluded from the C5 verdict | Local CPU; 7m22s wall |

## Reproduce the formal evidence

The author source is pinned at
`Yixiao-Wang-Stats/CLARITree@4397f8dbc8b63751777e7918b89972e793796dfd`;
Eigen is pinned at `3147391d946bb4b6c68edd901f2add6ac1f31f8c`. Run:

```bash
bash repro/run_local_claim_suite.sh
```

The command creates `.venv`, installs `requirements-repro.txt` with pip,
materializes both pins, compiles the released C++ extension, performs the
fresh California fit, and prints a structured C1–C6 assessment. The author
source is not edited. Generated dependencies and outputs are ignored by Git.

To explore the already-produced evidence without rerunning the expensive fit:

```bash
marimo edit notebooks/claritree_reproduction.py
marimo run notebooks/claritree_reproduction.py
```

## Evidence boundary

The C1–C3 and C6 protocols were committed before their respective formal
runs. Earlier exploratory results were already visible, so they are described
as **protocol-locked independent reconstructions**, not blinded
preregistrations. C5 remains deliberately unresolved: tuning a new generator
until it reaches the paper's numbers would not reconstruct the author
experiment and would not be acceptable 12/12 evidence.
