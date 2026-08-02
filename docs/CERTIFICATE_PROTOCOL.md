# Locked protocol for the C1--C3 proof certificates

This protocol was committed before launching the new certificate experiment.
The earlier exploratory suite and its outputs were already visible, so this is
a **protocol lock for an independent rerun**, not a claim of blinded
pre-registration.

## Immutable inputs

- Paper: arXiv `2606.12840`.
- Author source: `Yixiao-Wang-Stats/CLARITree` commit
  `4397f8dbc8b63751777e7918b89972e793796dfd`.
- Eigen: commit `3147391d946bb4b6c68edd901f2add6ac1f31f8c`
  (3.4.0), the implementation invoked by the author's `LLT::rankUpdate` calls.
- Compute: the agreed local CPU backend and the fixed command
  `bash repro/run_local_claim_suite.sh`.

## Acceptance rules fixed before the run

1. **C1:** the pinned CLARITree candidate loop must contain one left update,
   one right downdate, and a Greedy completion call. The pinned Eigen routine
   must be called directly by a compiled microbenchmark. The symbolic update
   work must have polynomial degree two, and the measured log--log slope over
   dimensions 16--128 must lie in the deliberately broad implementation-noise
   interval `[1.1, 3.2]`. Correctness is separately guarded by the existing
   direct-fit and quantile checks.
2. **C2:** SymPy must derive the paper's exact level-sum expression and prove
   its difference from a constant multiple of
   `d^2 n k^4 T` is nonnegative under positive integer parameters. Z3 must find
   no counterexample to the `O(nk)` space reduction under the paper's stated
   regime `n >= d k`.
3. **C3 dominance:** Z3 must find no counterexample to the induction step when
   (a) child CLARITree objectives are no worse than their Greedy counterparts
   and (b) the lookahead candidate set includes the Greedy root split.
4. **C3 gap:** exact rational/symbolic checks must instantiate the paper's B.2
   DGP, including zero gain for `g`, `h`, and `z`, positive nuisance gain
   `epsilon^2/U^2`, Greedy risk at least `1-epsilon`, and the explicit
   `g`-then-`h` CLARITree tree risk at most `2 epsilon`. The certificate must
   prove the ratio lower bound for arbitrary `0 < epsilon < 1/2`, `d >= 2`,
   and integer `U > d`; a floating-point seed sweep is not sufficient.

The C3 gap check must derive these values from an executable independent-moment
evaluator: Rademacher, Bernoulli, standard-normal, matched-`J`, and
unmatched-`J` moments are explicit inputs. Merely placing the paper's moment
identities in output strings does not satisfy this protocol. The verifier must
also derive the optimal child coefficient by differentiating the exact loss
quadratic and derive the `g`-then-`h` leaf risk from the mixture response.

Any failed assertion makes the run fail closed. Empirical timings are evidence
about the pinned implementation on this machine; the symbolic certificates are
the evidence for the universal statements.

## Post-judgment repair controls

These controls were added after the 2026-07-24 judge feedback and are not part
of the earlier protocol lock. They test that each certificate can fail when a
claim condition or mechanism is removed:

- replacing C1's rank update with a full Cholesky refactorization changes the
  exact work proxy from degree two to degree three;
- removing C2's `n >= d*k` space regime admits the explicit counterexample
  `n=1, d=2, k=2`, where the proxy is 13 but `4*n*k` is 8;
- setting C3's `epsilon=3/4` makes the claimed strict ratio margin negative,
  and setting `U=d=4` removes the guaranteed unresolved nuisance pair.
