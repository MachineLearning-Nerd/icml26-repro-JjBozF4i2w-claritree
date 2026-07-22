# Current status

## Current step

`in_progress:source-build-and-protocol-audit`

## Completed

- Claimed OpenReview `JjBozF4i2w` in the shared coordination registry.
- Pinned the author release at
  `Yixiao-Wang-Stats/CLARITree@4397f8dbc8b63751777e7918b89972e793796dfd`.
- Pinned Eigen `3.4.0@3147391d946bb4b6c68edd901f2add6ac1f31f8c` as the
  documented C++ header dependency without altering `upstream/`.
- Built and ran the unmodified C++ source on released Auction outer-0 data.
  CLARITree test R² was `0.937706`; Greedy was `0.919556`.
- Built the released Python extension in the project-local Python 3.12
  environment. The source tree remains clean.
- Independently re-aggregated the released California Housing raw folds for
  C4: CLARITree `0.74994 +/- 0.01006` test R2 versus STreeD
  `0.70485 +/- 0.00803`, after validation-only hyperparameter selection.
- Reproduced the C6 plot-input selection from the released `results/final.csv`.
  Its exact 590-second endpoint is CLARITree `100.0%` (880/880 records) versus
  STreeD `70.0%` (1232/1760). This supports the completion advantage but does
  not exactly reproduce the paper's rounded `95%`/`60%` wording; both values
  are retained transparently.
- Added fail-closed source-structure and theorem-consequence verifiers for the
  C1--C3 audit: source recursion/lookahead/rank-one-update tokens are present,
  the released quantile pool matches independent NumPy, ten deterministic
  C++-extension comparisons never make CLARITree worse than Greedy, and the
  displayed C3 final inequality is checked over 200 epsilon values.
- Ran exact source C++ California outer-4 calibration on the authorized
  CPU-only HF `cpu-upgrade` flavor: job `6a609a58d09dc1f57c6c1d62`. The source
  calculation completed in `76.21s` at `463,796 KB` peak RSS; its authenticated
  job-log payload is retained in `outputs/california_outer4_cpp.json`. The job
  subsequently returned ERROR only because the supplied token lacked permission
  to create the private artifact dataset; no computation result was lost.

## Next actions

1. Re-run the fail-closed gate covering pins, C1--C4 checks, C6 readback,
   source smoke, and explicit C5 scope exclusion.
2. Decide whether the documented C5 and C6 limitations permit publication.

## Gate state

`repro/src/run_publication_gate.py` now writes a fail-closed gate proof. The
retained CLI run is a memory/CPU feasibility calibration only: its `main.cpp`
entrypoint randomly re-splits input, so it is not comparable to the fixed
outer-fold table. The gate separately requires a retained fixed-split run
through `scripts.run_ours_outer.fit_eval` whose outer-4 `test_r2` matches the
committed table.

That fixed-split run is complete: CPU job `6a609dfd13e6ef894d54b655` used the
pinned driver entrypoint and exactly reproduced outer-4 `test_r2`
`0.7431327225376596` in `62.04s` fit / `88.53s` elapsed. The setup-only retry
`6a609d9713e6ef894d54b64f` failed before fitting because it invoked absent
`pip` rather than UV's installer; it is not evidence.

## Scope guard

The paper specifies a *family* for C5's synthetic DGP, but the pinned author
release contains no generator, configuration, seed, raw synthetic artifact, or
enough headline parameters to recreate the reported MSEs. The full
under-specification audit is in `docs/C5_SCOPE_EXCLUSION.md`. Treat any
reconstruction as an independent supplementary check only, not source rerun
evidence. No Hugging Face GPU is authorized or used.
