# Source manifest

| Component | Pin | Purpose |
|---|---|---|
| Author implementation | `Yixiao-Wang-Stats/CLARITree@4397f8dbc8b63751777e7918b89972e793796dfd` | C++ algorithm, Python drivers, five-fold data splits, raw result tables |
| C++ header dependency | `eigen@3147391d946bb4b6c68edd901f2add6ac1f31f8c` (tag `3.4.0`) | Required by the upstream Makefile/CMake source |
| Paper source | arXiv `2606.12840` | Exact claim/protocol audit |

The upstream checkout must remain clean. The Eigen checkout is a build-only
dependency in `repro/vendor/eigen`; it is not copied into or patched into the
author source tree.

The source-protocol decision for the unreleased synthetic headline is recorded
in [C5_SCOPE_EXCLUSION.md](C5_SCOPE_EXCLUSION.md).

The distinction between the native CPU feasibility calibration and the C4
fixed-split protocol is recorded in [CALIBRATION_SCOPE.md](CALIBRATION_SCOPE.md).
