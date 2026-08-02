# Claim 1 — Rank-one Cholesky updates

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_c1_contract", "created_at": "2026-08-02T10:52:18+00:00", "title": "Literal claim and verdict contract"}
-->
**Claim.** CLARITree combines recursive lookahead split selection (Algorithm 1) with streaming split enumeration maintained by rank-one Cholesky updates (Algorithm 2), at `O(k²)` per sample ([paper §4](https://ar5iv.labs.arxiv.org/html/2606.12840#S4), [Algorithms 1–2](https://ar5iv.labs.arxiv.org/html/2606.12840#S4.SS2)). Verification required the exact author-to-Eigen call chain, a symbolic operation recurrence of degree two, a compiled timing check, and a control that loses the quadratic property.

**Result: verified.** At the pinned author SHA, both left updates and right downdates reach Eigen `LLT::rankUpdate`. The independent recurrence visits `p(p+1)/2` positions for `p=k+1`; replacing the update by a full refactorization changes the work proxy to degree three. The compiled pinned-Eigen benchmark is supporting evidence, not the proof.

---
<!-- trackio-cell
{"type": "code", "id": "cell_clari_c1_certificate", "created_at": "2026-08-02T10:52:18+00:00", "title": "C1 source-tied exact certificate", "command": ["python", "repro/src/verify_algorithmic_certificates.py"], "exit_code": 0, "duration_s": 4.2}
-->
````bash
$ python repro/src/verify_algorithmic_certificates.py
````

The complete deterministic verifier is [`repro/src/verify_algorithmic_certificates.py`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/blob/main/repro/src/verify_algorithmic_certificates.py); the compiled source is [`benchmark_rank_update.cpp`](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree/blob/main/repro/cpp/benchmark_rank_update.cpp).

````python title=c1_certificate_core.py
# Exact independent recurrence used by the verifier.
p, i = symbols("p i", integer=True, positive=True)
rank_update_visits = summation(1 + (p - i - 1), (i, 0, p - 1))
assert simplify(rank_update_visits - p * (p + 1) / 2) == 0
assert Poly(rank_update_visits, p).degree() == 2

# Condition-relaxing control: dense refactorization after each sample.
full_refactor = summation((p - i) ** 2, (i, 0, p - 1))
assert Poly(full_refactor, p).degree() == 3
````

````output
author source sha256: df81b36d7f932752ad55657cad7dd3faf066a93e79cb3b91167628fc3bca2821
Eigen LLT sha256: 362fe6b080c9b67d11106f821f926fa84ed24b2120fbdba2a09efb0869eef1ec
source call chain: PASS
author token counts: recursion=1, left update=2, right downdate=2,
  Greedy completion left=4, Greedy completion right=4
exact recurrence visits: p*(p + 1)/2
polynomial degree: 2
control full-refactor proxy: p*(2*p**2 + 3*p + 1)/6
control polynomial degree: 3 — quadratic property lost: true
pinned Eigen dimensions fitted: [16, 32, 64, 96, 128]
measured log-log slope: 1.329557364548925
locked supporting interval: [1.1, 3.2] — PASS
all C1 certificate checks: PASS
````

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_06a9336d54b7", "created_at": "2026-07-22T10:45:02+00:00", "title": "Previously judged C1 evidence retained"}
-->
The earlier candidate's source-structure evidence remains true: the pinned implementation contains `CLARITree::recursive_fit`, its `Greedy::recursive_fit` completion calls, both `llt_left.rankUpdate(..., +1)` and `llt_right.rankUpdate(..., -1)`, and quantile-threshold construction. Its deterministic ten-seed CLARITree-versus-Greedy comparison is retained as a finite smoke test; the exact recurrence and condition-relaxing control above replace that toy comparison as the claim's primary evidence.

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_c1_reproduce", "created_at": "2026-08-02T10:52:18+00:00", "title": "Reproduce and provenance"}
-->
Run `bash repro/run_local_claim_suite.sh` from the [public reproduction repository](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree). The bootstrap pins [CLARITree `4397f8d`](https://github.com/Yixiao-Wang-Stats/CLARITree/tree/4397f8dbc8b63751777e7918b89972e793796dfd) and [Eigen `3147391`](https://gitlab.com/libeigen/eigen/-/tree/3147391d946bb4b6c68edd901f2add6ac1f31f8c). No GPU or remote job is used.
