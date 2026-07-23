# Current status

## Current step

`judge_ready_evidence:publication_in_progress`

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
- Ran the matching fixed-split author-driver calibration on CPU-upgrade job
  `6a609dfd13e6ef894d54b655`: the selected outer-4 configuration exactly
  reproduced committed test R2 `0.7431327225376596`.
- Created and pinned the Trackio logbook with pages for every anchored claim,
  controls, methods, and conclusion.
- Created and pushed the public GitHub handoff:
  `MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree@7b261a2`.
- Added protocol-locked, machine-checkable C1--C3 certificates. The pinned
  source call chain and exact rank-update recurrence verify C1; SymPy and Z3
  verify the C2 level sum and space implication; Z3 plus exact Appendix B.2
  moments and rational witnesses verify C3.
- Executed the exact C6 author plot path under a locked tolerance. The
  unchanged author code and independent recount agree on CLARITree `100%`
  (880/880) and STreeD `70%` (1232/1760). The 10-point STreeD discrepancy
  exceeds the locked +/-5-point tolerance, so C6 is falsified under the
  released author artifacts while its directional advantage is supported.
- Exhaustively audited the public C5 release surface. The exact Figure 1
  protocol remains unavailable, so the supplementary reconstruction is
  excluded under the require-author-protocol rule.

## Next actions

1. Publish the updated GitHub report/notebook and synchronize the judge-facing
   Hugging Face logbook.
2. Request the exact Figure 1 protocol from the authors. This is the only known
   path from the honest 10/12 projection to defensible 12/12 evidence.

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

The current evidence resolves C1--C4 as verified and C6 as falsified under the
released author artifacts. C5 remains inconclusive because it is not a
runnable author protocol. This projects to 10/12 under the judge rubric; it is
not a guaranteed score until a new judge record is issued.

FULL_GATE_READY: JjBozF4i2w

The atomic canonical-backlog handoff completed on 2026-07-22 after the public
GitHub push at `04ba48c8ebf2050a2287bc148db719ecbd155579`. The shared drain is
the sole Hugging Face publisher; do not create a competing Space manually.

## Scope guard

The paper specifies a *family* for C5's synthetic DGP, but the pinned author
release contains no generator, configuration, seed, raw synthetic artifact, or
enough headline parameters to recreate the reported MSEs. The full
under-specification audit is in `docs/C5_SCOPE_EXCLUSION.md`. Treat any
reconstruction as an independent supplementary check only, not source rerun
evidence. No Hugging Face GPU is authorized or used.
