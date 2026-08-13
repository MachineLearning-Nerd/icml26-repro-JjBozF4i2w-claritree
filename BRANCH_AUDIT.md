# Branch audit

This file records the role of every source branch observed before cleanup. The old `orx/*` and `publish/*` names are historical experiment labels, not supported user workflows. The listed commit IDs are pre-cleanup source refs; identity normalization may rewrite their hashes. Some branch tips are divergent from the final `main`, so their role is preserved here while the release artifacts and conclusions remain on the publication surface.

## Source branch map

| Source ref | Tip observed before cleanup | Relation to `main` | Role and outcome |
|---|---:|---|---|
| `orx/pinned-source-baseline-c1-c4-and-c6` | `ba38144` | Ancestor | Pinned the author source and Eigen, established the local suite, and carried the initial C1–C4/C6 evidence |
| `orx/machine-checkable-c1-c3-certificates` | `619c53e` | Divergent | Added source-structure checks, SymPy/Z3 proof obligations, exact rank-update controls, and C1–C3 certificates |
| `orx/protocol-locked-exact-c6-reconstruction` | `8230e65` | Divergent | Executed the unchanged author completion plot path, independently recounted it, and locked the C6 released-artifact assessment |
| `orx/independent-figure-1-reconstruction` | `8e2c3e3` | Divergent | Tested a declared substitute for missing Figure 1 protocol; supplementary only and excluded from C5 scoring |
| `orx/resolve-pip-build-paths` | `311de42` | Divergent | Repaired pybind11/CMake paths so the pinned source could build reproducibly |
| `orx/executable-exact-moment-c3-certificate` | `1d27b35` | Divergent | Replaced asserted C3 moment labels with executable exact moment derivations and rational witnesses |
| `publish/judge-ready-exact-evidence` | `15127fb` | Ancestor | Publication handoff that integrated the strengthened exact C3 evidence into the release surface |
| `main` | `39241b4` | Canonical | Reader-facing README, reports, notebooks, protocols, raw JSON, and source manifests |

## Cleanup policy

1. Preserve the branch roles and source refs in this file.
2. Rename the repository to `icml26-claritree`.
3. Keep `main` as the default and only supported branch.
4. Remove stale `master`, `orx/*`, and `publish/*` remote refs after the documented release surface is pushed.
5. Normalize all reachable commits on the retained history to the `MachineLearning-Nerd` GitHub identity.

This is a namespace cleanup of supported entry points. The committed claim pages, reports, raw evidence, source pins, C5 exclusion, and C6 protocol remain available on `main`; branch-only experiment tips are represented by their role and source ref above.
