# Claim 4 — California Housing

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_c4_contract", "created_at": "2026-08-02T10:52:18+00:00", "title": "Literal claim and preserved verdict"}
-->
**Claim.** On California Housing, CLARITree achieves test `R²=0.75`, versus `0.70` for STreeD ([Table 2](https://ar5iv.labs.arxiv.org/html/2606.12840#S6.T2)). **Result: verified.** This page preserves the judged five-fold artifact readback and exact source-entrypoint outer-fold rerun without weakening or changing the evidence.

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_d9374bcfd13b", "created_at": "2026-07-22T10:45:03+00:00", "title": "California fixed-split result"}
-->
Released five-fold aggregation gives CLARITree `R²=0.7499375 ± 0.0100611` versus STreeD `0.7048455 ± 0.0080266`. A fresh local CPU fit through the pinned author's `scripts.run_ours_outer.fit_eval` on released outer fold 4 produced `0.7431327225376608`, differing from the released selected row `0.7431327225376596` by `1.22×10⁻¹⁵`.

---
<!-- trackio-cell
{"type": "code", "id": "cell_fe6cc6a0e437", "created_at": "2026-07-22T10:45:18+00:00", "title": "C4 raw-fold readback", "command": ["python", "repro/src/verify_california_artifacts.py"], "exit_code": 0, "duration_s": 0.42}
-->
````bash
$ python repro/src/verify_california_artifacts.py
````

````output
selection: mean validation R² over five released outer folds
CLARITree parameters: lambda=0.001, kappa=0.00001
CLARITree mean test R²: 0.7499375138107127
CLARITree sample std: 0.01006107119945698
STreeD parameters: cost_complexity=0.0001, ridge=0.00001, lasso=0.001
STreeD mean test R²: 0.7048454539571957
STreeD sample std: 0.008026604151455525
R² advantage: 0.04509205985351705
source claim verified: true
````

The full fail-closed readback is [`verify_california_artifacts.py`](https://github.com/MachineLearning-Nerd/icml26-claritree/blob/main/repro/src/verify_california_artifacts.py), and the released author source/data are pinned at [`4397f8d`](https://github.com/Yixiao-Wang-Stats/CLARITree/tree/4397f8dbc8b63751777e7918b89972e793796dfd).

---
<!-- trackio-cell
{"type": "code", "id": "cell_clari_c4_fresh", "created_at": "2026-08-02T10:52:18+00:00", "title": "Fresh author-entrypoint outer-fold execution", "command": ["python", "repro/src/run_local_claim_suite.py"], "exit_code": 0, "duration_s": 55.0}
-->
````output
dataset: california_housing
outer: 4
depth: 4
lambda: 0.001
kappa: 0.00001
n_thresholds: 20
threshold strategy: quantile
selection: released configuration; no new cross-validation
fresh test R²: 0.7431327225376608
released row test R²: 0.7431327225376596
absolute difference: 1.2212453270876722e-15
exact release-row match (<1e-6): true
````

The control is fail-closed: changing or removing the retained fixed-split calibration makes the publication gate fail. No GPU or remote job was used.
