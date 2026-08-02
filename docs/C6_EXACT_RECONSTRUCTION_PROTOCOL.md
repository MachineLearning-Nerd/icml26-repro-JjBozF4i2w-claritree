# Protocol lock: exact Claim 6 reconstruction

This protocol is fixed before the new formal run. Because the released endpoint
was already inspected in an earlier exploratory run, this is a **prospective
protocol lock for the independent rerun**, not a blinded pre-registration.

## Claim and immutable evidence

- Anchored numeric claim: approximately `95%` CLARITree versus `60%` STreeD
  completion by the displayed 600-second budget.
- Author source: `Yixiao-Wang-Stats/CLARITree` commit
  `4397f8dbc8b63751777e7918b89972e793796dfd`.
- Plot program: `scripts/images/plot_completion_rate.py`, executed unchanged.
- Plot input: `results/final.csv` from the same commit.

## Locked reconstruction semantics

The author program is the protocol authority:

- keep rows with `outer == "mean"`;
- keep depth `4`;
- keep `n_thresholds == 20`;
- use methods `claritree` and `streed`;
- discard missing and non-positive `train_time_s` values;
- count a run complete when `train_time_s <= 590` seconds;
- display that internal cutoff as the paper's 600-second limit;
- divide completed records by all retained positive-time records for each
  method.

The reconstruction must execute the unmodified author script in an isolated
temporary directory, parse its printed counts, independently recompute the same
counts, and require exact equality between the two paths. A no-op headless
`matplotlib` API shim may replace rendering only; it must not alter pandas,
NumPy, source constants, filtering, completion counting, or printed output.

## Decision rule

The tolerance is fixed at **5 percentage points per method**, inclusive, to
operationalize the paper's word “approximately.”

- **Verified:** both reconstructed endpoints are within 5 points of `95%/60%`.
- **Falsified under the released author artifacts:** either endpoint is more
  than 5 points away, provided the unchanged author script and independent
  implementation agree exactly.
- **Inconclusive:** source execution fails, the two implementations disagree,
  or the pinned input is unavailable.

Direction (`CLARITree > STreeD`) is reported separately and cannot override the
numeric decision rule.

## Post-judgment boundary audit

This audit was added after the judge objected that 590 seconds differs from the
claim's displayed 600-second budget. The release itself defines both constants:
`TIME_LIMIT = 590` and `DISPLAY_TIME_LIMIT = 600`. Its table generator also
marks every result above 590 seconds with the documented timeout symbol.

The repair therefore retains two counts. The author-protocol count uses 590 and
must agree exactly with the unchanged plot script. A condition-relaxing control
naively counts every recorded time at or below 600. That control is expected to
misclassify the solver's capped 599.x-second rows as completions; the number of
such rows is reported explicitly rather than hidden.
