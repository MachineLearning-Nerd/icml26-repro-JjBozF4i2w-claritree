# Primary source map

## Paper and implementation sources

| Source | Use in this audit |
|---|---|
| [arXiv record](https://arxiv.org/abs/2606.12840) | Canonical title, authors, identifier, abstract, and paper source |
| [OpenReview record](https://openreview.net/forum?id=JjBozF4i2w) | ICML submission and discussion context |
| [Official author repository](https://github.com/Yixiao-Wang-Stats/CLARITree) | Pinned implementation, data folds, and released scripts |
| [Pinned author commit](https://github.com/Yixiao-Wang-Stats/CLARITree/tree/4397f8dbc8b63751777e7918b89972e793796dfd) | Immutable source boundary used by the suite |
| [Pinned Eigen commit](https://gitlab.com/libeigen/eigen/-/tree/3147391d946bb4b6c68edd901f2add6ac1f31f8c) | Build dependency and exact `LLT::rankUpdate` implementation |

The claim statements and equation/figure anchors are transcribed in the committed pages under `pages/claim-*` and mirrored in `.trackio/logbook/pages/claim-*`. Those pages are audit records; the paper and pinned source above remain the primary external sources.

## Local producer map

| Evidence layer | Producer | Consumed by |
|---|---|---|
| Source structure | `repro/src/verify_source_structure.py` | C1 and the source-boundary audit |
| Exact certificates | `repro/src/verify_algorithmic_certificates.py` | C1, C2, and C3 |
| Theorem consequences | `repro/src/verify_theorem_consequences.py` | C2/C3 runtime and gap checks |
| Released California artifacts | `repro/src/verify_california_artifacts.py` | C4 five-fold readback |
| Fresh fixed-split fit | `repro/src/run_local_claim_suite.py` | C4 outer-4 exact source-entrypoint check |
| C5 scope audit | `docs/C5_SCOPE_EXCLUSION.md` and source-history checks | C5 fail-closed exclusion |
| C6 author/independent recount | `repro/src/verify_completion_artifacts.py` | C6 timeout contract, exact count cross-check, and falsification |
| Suite gate | `repro/src/run_publication_gate.py` | Regenerates `outputs/publication_gate.json` |

## Evidence files

- `outputs/algorithmic_certificates.json`: exact C1–C3 certificates and controls.
- `outputs/california_artifact_readback.json`: released five-fold C4 rows.
- `outputs/california_outer4_fixed_split.json`: fresh fixed-split C4 calibration.
- `outputs/completion_artifact_readback.json`: C6 source execution and independent recount.
- `outputs/judge_ready_summary.json`: claim-by-claim summary and rubric projection.
- `outputs/publication_gate.json`: generated scoped run output; root `publication_gate.json` applies the conservative paper-level interpretation.

## Provenance boundary

The local gate answers whether the pinned source, certificates, released artifacts, controls, and C5/C6 protocols execute consistently. It does not convert a missing C5 author protocol into a result, and it does not claim that a symbolic/SMT certificate replaces the paper’s proof. The paper-level status therefore remains `INCONCLUSIVE`.
