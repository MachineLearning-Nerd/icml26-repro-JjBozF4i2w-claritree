# Reproduction status

## Paper

- **Title:** CLARITree: Cholesky and Lookahead Accelerations for Regression with Interpretable Piecewise Linear Trees
- **Authors:** Yixiao Wang, Hayden McTavish, Varun Babbar, Margo Seltzer, and Cynthia Rudin
- **arXiv:** [2606.12840](https://arxiv.org/abs/2606.12840)
- **OpenReview:** [JjBozF4i2w](https://openreview.net/forum?id=JjBozF4i2w)

## Decision

- **Overall paper-level status:** `INCONCLUSIVE`
- **Scoped local evidence gate:** `PASS`
- **C1–C3:** source-tied conditional certificates pass
- **C4:** scoped California Housing reproduction passes
- **C5:** `INCONCLUSIVE_SOURCE_MISSING`
- **C6:** `FALSIFIED_AS_RELEASED`
- **Judge projection:** 10/12 under the documented rubric; not a guaranteed score

The unresolved C5 protocol is the main blocker. The C6 result is a faithful audit of the released author artifacts, not a claim that the authors’ intended un-released experiment has been disproved.

## Evidence

- Generated scoped gate: [`outputs/publication_gate.json`](outputs/publication_gate.json)
- Conservative interpretation: [`publication_gate.json`](publication_gate.json)
- Full claim report: [`reports/claritree-6-claim-reproduction/report.md`](reports/claritree-6-claim-reproduction/report.md)
- Source pins: [`docs/SOURCE_MANIFEST.md`](docs/SOURCE_MANIFEST.md)
- C5 boundary: [`docs/C5_SCOPE_EXCLUSION.md`](docs/C5_SCOPE_EXCLUSION.md)
- C6 protocol: [`docs/C6_EXACT_RECONSTRUCTION_PROTOCOL.md`](docs/C6_EXACT_RECONSTRUCTION_PROTOCOL.md)

## Source and compute

- Author source: `Yixiao-Wang-Stats/CLARITree@4397f8dbc8b63751777e7918b89972e793796dfd`
- Eigen: `3.4.0@3147391d946bb4b6c68edd901f2add6ac1f31f8c`
- Formal environment: Python 3.12.11 on Apple arm64, 8 logical CPUs, no GPU
- Full suite: `bash repro/run_local_claim_suite.sh`
- Bounded tests: `python -m pytest -q repro/tests`

## Repository policy

- **Maintainer identity:** MachineLearning-Nerd
- **Canonical branch:** `main`
- **Historical branch roles:** [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md)
- **Official implementation:** [Yixiao-Wang-Stats/CLARITree](https://github.com/Yixiao-Wang-Stats/CLARITree)
- **This repository:** independent reproduction and audit, not an official author release

## Required next evidence

To resolve C5, the authors would need to release the Figure 1 generator or generated data, sample size, feature/group counts, correlation and noise parameters, train/test split, seeds, model hyperparameters, and evaluation path—or an equivalent machine-checkable artifact containing those values.
