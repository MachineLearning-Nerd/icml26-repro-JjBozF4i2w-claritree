# Claim 2 — Runtime bound

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_c2_contract", "created_at": "2026-08-02T10:52:18+00:00", "title": "Literal claim and verdict contract"}
-->
**Claim.** CLARITree runtime is `O(k n log n + d² n k⁴ T)` ([Theorem 5.1](https://ar5iv.labs.arxiv.org/html/2606.12840#S5.SS1)). Verification required an independent symbolic sum over all lookahead levels, its asymptotic upper bound under the theorem's positive-integer assumptions, and a meaningful assumption-relaxing control. Timing exponent arithmetic alone was not accepted.

**Result: verified.** SymPy derives the paper's exact decomposition `2 d n k³ + d(d−1)n k⁴T/2`, whose threshold-evaluation term is bounded by `O(d² n k⁴T)`; the presort term is `O(k n log n)`. A related memory obligation in the proof is also checked by Z3 under `n ≥ dk`, and deliberately fails when that regime is removed.

---
<!-- trackio-cell
{"type": "code", "id": "cell_clari_c2_certificate", "created_at": "2026-08-02T10:52:18+00:00", "title": "C2 symbolic level sum and assumption control", "command": ["python", "repro/src/verify_algorithmic_certificates.py"], "exit_code": 0, "duration_s": 4.2}
-->
````python title=c2_certificate_core.py
n, d, k, T, level = symbols("n d k T level", integer=True, positive=True)
level_sum = summation(2*n*k**3 + (d-level)*n*k**4*T, (level, 1, d))
paper = 2*d*n*k**3 + d*(d-1)*n*k**4*T/2
assert simplify(level_sum - paper) == 0

# Proof-side space regime and control.
exact_space = 2*n*k + n + d*k**2
# Z3: no exact_space > 4*n*k witness when n >= d*k.
# Removing n >= d*k yields n=1,d=2,k=2: exact 13 > 4nk=8.
````

````output
exact level sum: d*k**3*n*(T*d*k - T*k + 4)/2
paper decomposition: T*d*k**4*n*(d - 1)/2 + 2*d*k**3*n
summation identity: PASS
upper-bound difference: d*k**3*n*(5*T*d*k + T*k - 4)/2
theorem runtime: O(k*n*log(n) + d^2*n*k^4*T)
space regime: n >= d*k, positive integers
space counterexample query: unsat — PASS
condition-relaxing control: n=1,d=2,k=2 gives 13 > 8, query sat — PASS
````

The exact code and raw JSON are in [`verify_algorithmic_certificates.py`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/blob/main/repro/src/verify_algorithmic_certificates.py) and [`outputs/algorithmic_certificates.json`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/blob/main/outputs/algorithmic_certificates.json). This is a machine-checked audit of the theorem's derivation, not a replacement for the paper's proof.

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_c2_reproduce", "created_at": "2026-08-02T10:52:18+00:00", "title": "Reproduce and negative-control interpretation"}
-->
Run `python repro/src/verify_algorithmic_certificates.py` after the pinned bootstrap, or run the full `bash repro/run_local_claim_suite.sh`. The old candidate merely doubled individual variables in the displayed expression; the current certificate instead derives the exact finite level sum. The out-of-regime memory witness proves the solver is not hard-wired to return success and documents exactly where the auxiliary `O(nk)` simplification depends on `n ≥ dk`.
