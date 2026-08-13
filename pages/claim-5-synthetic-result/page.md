# Claim 5 — Synthetic result

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_c5_contract", "created_at": "2026-08-02T10:52:18+00:00", "title": "Literal claim and blocker"}
-->
**Claim.** On a synthetic dataset, CLARITree reports test MSE `4.03` (`R²=0.97`) versus MSE `15.41` (`R²=0.88`) for a standard greedy tree ([Figure 1](https://ar5iv.labs.arxiv.org/html/2606.12840#S1.F1)). **Result: inconclusive — essential material unavailable.** A faithful check requires the author's exact generator or generated data, sample size, feature/group counts, correlation and noise values, train/test split, seeds, and model hyperparameters.

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_deba80a52fb1", "created_at": "2026-07-22T10:45:03+00:00", "title": "Excluded source protocol"}
-->
The public release has no Figure 1 generator, configuration, seeds, raw artifact, or enough numeric data-generating-process parameters. The complete eight-commit source history contains neither a Figure 1 generation path nor the headline strings `4.03` and `15.41`. Appendix B.2 is a different theorem construction, not the Figure 1 experiment. Any reconstruction would substitute unidentified choices and is supplementary only, never an author-source rerun.

---
<!-- trackio-cell
{"type": "code", "id": "cell_clari_c5_audit", "created_at": "2026-08-02T10:52:18+00:00", "title": "Fail-closed source-history audit", "command": ["git", "-C", "upstream", "log", "-S4.03", "--all", "--oneline"], "exit_code": 0, "duration_s": 0.1}
-->
````bash
$ git -C upstream rev-list --all --count
8
$ git -C upstream log -S'4.03' --all --oneline
$ git -C upstream log -S'15.41' --all --oneline
$ find upstream -type f | grep -Ei 'figure.?1|synthetic.*(csv|json|npy)|generator'
````

````output
No matching commit, raw artifact, generator, or Figure 1 protocol path.
Official source HEAD and pinned audit SHA are both:
4397f8dbc8b63751777e7918b89972e793796dfd
````

The official repository audited is [Yixiao-Wang-Stats/CLARITree](https://github.com/Yixiao-Wang-Stats/CLARITree/tree/4397f8dbc8b63751777e7918b89972e793796dfd). The exclusion policy is documented in [`docs/C5_SCOPE_EXCLUSION.md`](https://github.com/MachineLearning-Nerd/icml26-claritree/blob/main/docs/C5_SCOPE_EXCLUSION.md).

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_c5_stop", "created_at": "2026-08-02T10:52:18+00:00", "title": "Why tuning was stopped"}
-->
An earlier independent five-seed reconstruction produced MSE `4.630` versus `4.722`, but every missing numeric choice was supplied by the reproducer. It is deliberately excluded from verdict evidence. Claim 5 can be resolved only if the authors release the generator/data plus exact configuration and split, or an equivalent machine-checkable artifact; local hyperparameter tuning cannot identify the unpublished experiment.
