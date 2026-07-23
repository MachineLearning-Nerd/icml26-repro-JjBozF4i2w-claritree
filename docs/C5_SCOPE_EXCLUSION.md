# C5 source-protocol exclusion

Anchored C5 is the headline synthetic result: CLARITree test MSE `4.03`
(`R2=0.97`) versus Greedy test MSE `15.41` (`R2=0.88`). It is not included in
the source-execution gate.

The paper source specifies only the *family* of the synthetic DGP: correlated
Gaussian covariates, empirical-quantile group membership on the first feature,
group-specific random coefficients, and Gaussian response noise. Its released
implementation (`Yixiao-Wang-Stats/CLARITree@4397f8dbc8b63751777e7918b89972e793796dfd`)
has no synthetic generator, configuration, train/test seed, generated data, or
raw headline-result table. The DGP description also leaves the headline run's
`k`, `G`, `rho`, `sigma`, sample size, split fraction, random seeds, and model
hyperparameters unspecified. The separate theory-gap illustration specifies
only `U=8`, depth `4`, and `n=1000`; it is not the Figure 1 headline protocol.

Consequently, selecting those values now would be a new implementation and a
new experimental protocol. It may be useful as clearly-labelled supplementary
work, but must never be presented as an unmodified author-source reproduction
or used to claim exact parity with `4.03`/`15.41`.

## Release audit and decision rule

The audit covered the pinned `main` commit, the repository's complete public
commit history, its `release/pypi` branch, tag `v0.1.1`, public releases and
assets, the sole public fork and all of its branches, the paper source, and
targeted public searches for the headline values and generator. The released
`scripts/images/teaser/teaser_summary.csv` is a real-dataset teaser summary,
not the Figure 1 synthetic experiment. No exact protocol or headline artifact
was found.

Under the user-selected **require author protocol** rule, C5 remains
`inconclusive` and the independent reconstruction is excluded from scoring.
The claim can move to verified or falsified only if the authors provide either:

1. executable generator code plus all numeric parameters, train/test split,
   seeds, CLARITree/Greedy settings, and evaluation code; or
2. the generated train/test data and raw predictions with enough metadata to
   machine-check the reported MSE and R² values.

Retrofitting missing values to match the published result is not admissible.

Paper-source audit hashes (arXiv `2606.12840` source):

| File | SHA-256 |
|---|---|
| `1_intro.tex` | `a158f5bce2b67ff10635de4fb657f37630e9d213a3718a311f00449525dfa3f8` |
| `5_analysis.tex` | `95ee71cbd4c2e68e7d6545839789098360e6b8c7aff3935b79f481b8d8a13e7b` |
| `8_4_appendix_experiment_details.tex` | `da75d4c53f096f86769e05950230cc8aedfb2eebe1e3cadf18e23fc2c24bae56` |
