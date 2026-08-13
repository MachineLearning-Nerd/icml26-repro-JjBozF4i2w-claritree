# ICML 2026 — CLARITree

Independent reproduction and claim audit for [*CLARITree: Cholesky and Lookahead Accelerations for Regression with Interpretable Piecewise Linear Trees*](https://arxiv.org/abs/2606.12840) ([OpenReview](https://openreview.net/forum?id=JjBozF4i2w)).

## Status at a glance

**Paper-level assessment: INCONCLUSIVE.** The released source supports strong, scoped evidence for Claims 1–4; Claim 6 is falsified under the released author artifacts and a locked tolerance; Claim 5 cannot be adjudicated because the exact Figure 1 protocol is not public. The generated local gate passes its checks, but that is a scoped reproduction gate—not proof that every paper claim is verified.

| Claim | Paper statement | Evidence status | Result producer |
|---|---|---|---|
| C1 — Algorithm 1/2 | Streaming rank-one Cholesky updates enable $O(k^2)$ per-sample work | **VERIFIED_CONDITIONAL** | Pinned author-to-Eigen call-chain audit, exact recurrence, benchmark, and cubic-refactorization control |
| C2 — Theorem 5.1 | Runtime $O(kn\log n+d^2nk^4T)$ and stated $O(nk)$ space regime | **VERIFIED_CONDITIONAL** | SymPy exact level sum, Z3 regime query, and out-of-regime counterexample |
| C3 — Theorems 5.3/5.4 | No-worse dominance and an arbitrarily large greedy-to-CLARITree gap | **VERIFIED_CONDITIONAL** | Z3 induction obligation, executable exact-moment evaluator, rational witnesses, and relaxed-assumption controls |
| C4 — Table 2 | California Housing test $R^2\approx0.75$ vs STreeD $\approx0.70$ | **REPRODUCED_SCOPED** | Released five-fold artifacts plus fresh pinned-author outer-4 execution |
| C5 — Figure 1 | Synthetic MSE 4.03 vs 15.41 headline | **INCONCLUSIVE_SOURCE_MISSING** | Fail-closed source-history audit; no exact generator, data, split, seeds, or model configuration |
| C6 — Figure 3a | Approximately 95% vs 60% completion by the displayed 600-second budget | **FALSIFIED_AS_RELEASED** | Unchanged author plot path and independent recount agree on 100% vs 70% at the release’s 590-second operational cutoff |

The raw scoped run is recorded in [`outputs/publication_gate.json`](outputs/publication_gate.json). The conservative interpretation is in [`publication_gate.json`](publication_gate.json), with the full claim ledger in [`STATUS.md`](STATUS.md).

## What the paper does

CLARITree combines a one-step lookahead search for piecewise-linear regression trees with streaming rank-one Cholesky updates. The paper argues that the lookahead improves the objective relative to a greedy tree, that the update strategy has favorable runtime and memory behavior, and that the method scales to real regression benchmarks while retaining interpretability.

## How each claim is produced

| Claim | Producer path | Raw evidence | Boundary or control |
|---|---|---|---|
| C1 | `repro/src/verify_source_structure.py` checks the pinned source call chain; `repro/src/verify_algorithmic_certificates.py` derives (p(p+1)/2) update visits and runs the pinned Eigen benchmark | [`outputs/source_structure.json`](outputs/source_structure.json), [`outputs/algorithmic_certificates.json`](outputs/algorithmic_certificates.json) | Replacing rank-one updates with full refactorization changes the work proxy from degree 2 to degree 3; timing is supporting evidence, not the universal proof |
| C2 | `verify_algorithmic_certificates.py` uses SymPy to derive the exact level sum and Z3 to check the $n\ge dk$ space regime | [`outputs/algorithmic_certificates.json`](outputs/algorithmic_certificates.json), [`outputs/theorem_consequences.json`](outputs/theorem_consequences.json) | The explicit witness $(n=1,d=2,k=2)$ violates the space bound when the theorem’s regime is removed |
| C3 | The same certificate verifier proves the dominance induction step and independently derives the Appendix B.2 moments, gains, risks, and ratio | [`outputs/algorithmic_certificates.json`](outputs/algorithmic_certificates.json) | Controls at $\epsilon=3/4$ and $U=d$ fail as predicted; the checker audits encoded proof obligations and does not replace the paper’s human proof |
| C4 | `repro/src/verify_california_artifacts.py` reads released folds; `repro/src/run_local_claim_suite.py` calls the pinned author driver on outer fold 4 | [`outputs/california_artifact_readback.json`](outputs/california_artifact_readback.json), [`outputs/california_outer4_fixed_split.json`](outputs/california_outer4_fixed_split.json) | Mean test $R^2$: CLARITree 0.74994, STreeD 0.70485; fresh outer-4 result differs from the released row by $1.22\times10^{-15}$ |
| C5 | `repro/src/verify_source_structure.py` and the source-history audit inspect the complete public author release; the supplementary reconstruction is kept outside the gate | [`docs/C5_SCOPE_EXCLUSION.md`](docs/C5_SCOPE_EXCLUSION.md), [`pages/claim-5-synthetic-result/page.md`](pages/claim-5-synthetic-result/page.md) | Missing $(n,k,G,\rho,\sigma)$, split, seeds, hyperparameters, generator, and raw data make exact author-protocol reproduction impossible; tuning substitutes is not admissible |
| C6 | `repro/src/verify_completion_artifacts.py` executes the unchanged author plot semantics and independently recomputes the counts | [`outputs/completion_artifact_readback.json`](outputs/completion_artifact_readback.json) | Release code uses a 590-second operational timeout while displaying 600 seconds; exact counts are 880/880 = 100% and 1232/1760 = 70%; the directional 30-point advantage remains supported |

The suite entrypoint is [`repro/run_local_claim_suite.sh`](repro/run_local_claim_suite.sh). It pins the author source and Eigen, builds the released extension, runs the source and symbolic checks, performs the California artifact audit, and fails closed if a required check is absent.

## Key results and limitations

### C1–C3: source-tied certificates

- C1 traces `CLARITree::recursive_fit` and both `LLT::rankUpdate` paths into the pinned Eigen implementation. The exact recurrence is quadratic in (p=k+1); the benchmark slope over dimensions 16–128 is supporting evidence only.
- C2 derives the paper’s exact level sum $2dnk^3 + d(d-1)nk^4T/2$, then checks the stated asymptotic decomposition and the $n\ge dk$ memory regime.
- C3 checks the universal induction step and the Appendix B.2 gap construction with executable exact moments and rational witnesses across depths 2, 3, 4, and 8.

These are conditional audits of the paper’s stated proof obligations. They are not claims that SMT or symbolic scripts replace a peer-reviewed proof.

### C4: California Housing

The released five-fold readback gives mean test $R^2=0.7499375$ for CLARITree and $0.7048455$ for STreeD. A fresh run through the pinned author entrypoint on released outer fold 4 produces $0.7431327225376608$, matching the committed row to floating-point precision. This is the strongest direct numerical reproduction in the repository.

### C5: protocol boundary

The reported Figure 1 headline is CLARITree MSE 4.03 ($R^2=0.97$) versus Greedy MSE 15.41 ($R^2=0.88$). The public author release contains no exact generator, synthetic dataset, headline table, or complete numeric configuration. A prior five-seed reconstruction is retained only as supplementary context because it chose the missing parameters; it is not evidence for or against the paper’s exact Figure 1 claim.

### C6: released-artifact falsification

The unchanged author plot program and an independent implementation agree exactly at the release’s operational cutoff: CLARITree completes 880/880 records (100%) and STreeD 1232/1760 (70%). The paper’s approximate endpoints are 95%/60%; with the pre-fixed inclusive ±5-point tolerance, STreeD misses by 10 points. A literal 600-second recount is a negative control because it misclassifies 528 capped timeout rows. The direction of the completion advantage is not disputed.

## Historical branch roles

The full branch map is in [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md). These are historical experiment stages; after cleanup, only `main` remains as the supported reader-facing branch.

| Historical branch | Role | Outcome |
|---|---|---|
| `orx/pinned-source-baseline-c1-c4-and-c6` | Initial pinned author/Eigen setup and local C1–C4/C6 suite | Foundation; ancestor of the release surface |
| `orx/machine-checkable-c1-c3-certificates` | Source structure, SymPy/Z3 certificates, exact C1–C3 controls | Strengthened theorem evidence; branch-only stage |
| `orx/protocol-locked-exact-c6-reconstruction` | Unchanged author plot execution and exact C6 recount | Established the released-artifact mismatch; branch-only stage |
| `orx/independent-figure-1-reconstruction` | Declared substitute for missing C5 protocol | Supplementary direction check; excluded from formal C5 verdict |
| `orx/resolve-pip-build-paths` | Fixed pybind11/CMake paths for reproducible builds | Build-support stage; branch-only stage |
| `orx/executable-exact-moment-c3-certificate` | Replaced asserted C3 moment labels with executable exact derivations | Final C3 evidence hardening; branch-only stage |
| `publish/judge-ready-exact-evidence` | Publication handoff and exact C3 evidence integration | Ancestor of the current publication surface |
| `main` | README, reports, pages, raw JSON, protocols, and release metadata | Canonical branch after cleanup |

## Reproduce

The full pinned suite is CPU-only and takes about one minute after environment setup:

```bash
bash repro/run_local_claim_suite.sh
```

For the bounded test suite:

```bash
python -m pytest -q repro/tests
```

The bootstrap uses the author source at `Yixiao-Wang-Stats/CLARITree@4397f8dbc8b63751777e7918b89972e793796dfd` and Eigen at `3147391d946bb4b6c68edd901f2add6ac1f31f8c`. No GPU or remote compute is required.

## Citation

```bibtex
@misc{wang2026claritree,
  author        = {Yixiao Wang and Hayden McTavish and Varun Babbar and
                   Margo Seltzer and Cynthia Rudin},
  title         = {CLARITree: Cholesky and Lookahead Accelerations for
                   Regression with Interpretable Piecewise Linear Trees},
  year          = {2026},
  eprint        = {2606.12840},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2606.12840}
}
```

If this audit or its certificates are useful, please cite the paper and the relevant raw evidence files. This repository is an independent reproduction maintained by **MachineLearning-Nerd**; it is not the authors’ official implementation.

## Thank you

Thank you to **Yixiao Wang, Hayden McTavish, Varun Babbar, Margo Seltzer, and Cynthia Rudin** for developing CLARITree and releasing source code, data folds, and implementation details that make substantial parts of the work auditable. The reproduction is intended as a respectful companion to the paper: it records both the claims supported by the released artifacts and the two places where the evidence stops.

The official author implementation is [Yixiao-Wang-Stats/CLARITree](https://github.com/Yixiao-Wang-Stats/CLARITree). The code here pins that release but adds independent certificates and audits; it should not be mistaken for an official release.

## Maintainer

Repository and publication-surface commits are maintained under the **MachineLearning-Nerd** GitHub identity. See [`STATUS.md`](STATUS.md) and [`publication_gate.json`](publication_gate.json) for the current decision and provenance.
