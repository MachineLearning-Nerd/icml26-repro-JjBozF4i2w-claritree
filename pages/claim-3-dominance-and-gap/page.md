# Claim 3 — Dominance and arbitrary gap

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_c3_contract", "created_at": "2026-08-02T10:52:18+00:00", "title": "Literal claim and verdict contract"}
-->
**Claim.** CLARITree's objective is no worse than a greedy Cholesky-based tree ([Theorem 5.3](https://ar5iv.labs.arxiv.org/html/2606.12840#S5.SS2)), and the greedy-to-CLARITree MSE ratio can be at least `1/(4ε)` ([Theorem 5.4 and Appendix B.2](https://ar5iv.labs.arxiv.org/html/2606.12840#A2.SS2)). Verification required the universal dominance induction obligation and an independent exact-moment audit of every step of the gap construction, plus controls outside `0<ε<1/2` and `U>d`.

**Result: verified.** Z3 finds the negated dominance conclusion unsatisfiable given the two child hypotheses and candidate inclusion. An exact polynomial-moment evaluator derives zero target-split gain, nuisance gain `ε²/U²`, greedy risk at least `1−ε`, and a `g`-then-`h` CLARITree candidate risk `2ε`; hence `(1−ε)/(2ε) > 1/(4ε)` precisely when `0<ε<1/2`.

---
<!-- trackio-cell
{"type": "code", "id": "cell_clari_c3_certificate", "created_at": "2026-08-02T10:52:18+00:00", "title": "C3 induction and Appendix B.2 exact-moment certificate", "command": ["python", "repro/src/verify_algorithmic_certificates.py"], "exit_code": 0, "duration_s": 4.2}
-->
````python title=c3_certificate_core.py
# Dominance induction obligation.
s = Solver()
s.add(C_left <= G_selected_left, C_right <= G_selected_right)
s.add(G_selected_left + G_selected_right <= G_root_left + G_root_right)
s.add(C_left + C_right > G_root_left + G_root_right)
assert s.check() == unsat

# Appendix B.2 consequences independently derived from exact moments.
assert target_split_gain == 0
assert nuisance_pair_gain == epsilon**2 / U**2
assert greedy_mse_lower == 1 - epsilon
assert claritree_candidate_mse == 2 * epsilon
ratio_margin = (1 - epsilon)/(2*epsilon) - 1/(4*epsilon)
assert simplify(ratio_margin) == (1 - 2*epsilon)/(4*epsilon)
````

````output
dominance negated conclusion: unsat — PASS
target/basis cross moments: {1:0, g:0, h:0, z:0, nuisance:0}
target split gains after g, h, or arbitrary z threshold: 0
matched J moment: s; unmatched J moment: 0
derived nuisance-pair gain: epsilon**2/U**2
unresolved-pair counterexample query under U>d: unsat
greedy MSE lower bound: 1-epsilon
CLARITree candidate MSE: 2*epsilon
ratio margin over 1/(4*epsilon): (1-2*epsilon)/(4*epsilon)
exact rational witnesses: depths {2,3,4,8}, U=d+1, epsilon {1/4,1/10,1/100}
construction certificate: PASS

CONTROL epsilon=3/4: ratio margin = -1/6; strict bound fails — PASS
CONTROL depth=4,U=4: no unresolved nuisance pair remains; greedy-path guarantee lost — PASS
````

The executable evaluator is [`verify_algorithmic_certificates.py`](https://github.com/MachineLearning-Nerd/icml26-claritree/blob/main/repro/src/verify_algorithmic_certificates.py), with its full 12 exact-rational witnesses in [`algorithmic_certificates.json`](https://github.com/MachineLearning-Nerd/icml26-claritree/blob/main/outputs/algorithmic_certificates.json). It uses symbolic marginal moments rather than inserting expected labels.

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_441f70b358be", "created_at": "2026-07-22T10:45:16+00:00", "title": "Previously judged dynamic evidence retained"}
-->
The earlier ten deterministic fits remain a smoke test: CLARITree loss never exceeded Greedy, with strict improvement in four cases and minimum slack zero. The shuffled-target control reached only train `R²=0.3203`. Those finite examples did not establish the universal theorem; the induction and exact construction certificates above now supply the primary evidence.

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_c3_scope", "created_at": "2026-08-02T10:52:18+00:00", "title": "Scope and proof status"}
-->
The checker audits the stated construction and induction step under the paper's assumptions; it does not claim that numerical or SMT evaluation replaces the human-readable proof. Reproduce with `python repro/src/verify_algorithmic_certificates.py` or the full suite. Both condition-relaxing controls must fail in the predicted way or the verifier exits nonzero.
