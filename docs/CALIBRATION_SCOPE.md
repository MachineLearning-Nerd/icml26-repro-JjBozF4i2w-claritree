# CPU calibration scope

`outputs/california_outer4_cpp.json` is an authenticated `cpu-upgrade` Job
log record for the pinned C++ `src/main.cpp` command. It confirms that the
unmodified native implementation builds and completes a California-sized fit in
`76.21` seconds with `463,796 KB` peak child RSS.

It is a feasibility calibration, not a C4 score rerun. The `main.cpp` CLI
loads one CSV and then creates its own shuffled 80/20 split with RNG seed 42.
The C4 table instead uses the released fixed `outer_4/train.csv` and
`outer_4/test.csv` files plus cross-validation through
`scripts/run_ours_outer.py`. Those protocols necessarily produce different
held-out scores.

The publication gate therefore requires a second artifact,
`outputs/california_outer4_fixed_split.json`, produced by the author driver's
`fit_eval` function on the fixed selected configuration. It must match the
committed outer-4 row before it can support C4.
