import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div style="font-family:system-ui;padding:24px;border-radius:16px;background:#17213b;color:white">
          <div style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#a9c5e8">CLARITree · arXiv:2606.12840</div>
          <h1 style="margin:.25em 0">Six claims, checked claim by claim</h1>
          <div style="display:flex;gap:24px;align-items:end">
            <div style="font-size:54px;font-weight:750;line-height:1">12/12</div>
            <div style="padding-bottom:5px">evidence coverage<br><b style="color:#6ee7a7">4 aligned</b> · <b style="color:#f8c35c">2 partially aligned</b></div>
          </div>
          <p style="margin-bottom:0;color:#d9e2f0">Strongest exact result: fresh California outer-4 test R²
          <b>0.7431327225376608</b>, matching the released row within 1.2×10⁻¹⁵.</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A tutorial reproduction of CLARITree

    CLARITree is a piecewise-linear regression tree. A Greedy tree chooses
    the best split visible now; CLARITree evaluates a split together with
    the next greedy split below it. The paper's key engineering idea is to
    stream rank-one Cholesky updates while evaluating candidates, making
    this one-step lookahead practical.

    This notebook contains the already-produced evidence, so opening it
    does **not** rerun the expensive C++ build or California fit. The formal
    run used pinned author source, Python 3.12.11, and an 8-logical-CPU Apple
    arm64 local machine. Select a claim below to inspect its result.
    """)
    return


@app.cell
def _():
    claim_rows = {
        "C1 · Algorithm": {
            "paper": "One-step lookahead with streamed rank-one Cholesky updates.",
            "observed": "Pinned C++ contains CLARITree recursion, its Greedy lookahead call, and both left/right rankUpdate paths; threshold pools matched NumPy.",
            "assessment": "Aligned",
        },
        "C2 · Complexity": {
            "paper": "O(k n log n + d² n k⁴ T) time and O(n k) space in the stated regime.",
            "observed": "Formula/source audit: doubling n,d,k,T yielded component ratios 2×, 4×, 16×, 2×.",
            "assessment": "Aligned under audit; no fresh asymptotic proof",
        },
        "C3 · Dominance": {
            "paper": "Objective no worse than Greedy, with an arbitrarily large constructed MSE gap.",
            "observed": "Minimum objective slack 0 in 10 trials; four strict wins. The displayed gap inequality held on 200 epsilon values.",
            "assessment": "Aligned",
        },
        "C4 · California": {
            "paper": "Test R² 0.75±0.01 versus STreeD 0.70±0.01.",
            "observed": "Released means 0.74994 vs 0.70485. Fresh outer-4 0.7431327225376608 matched its released row within 1.2e-15.",
            "assessment": "Aligned",
        },
        "C5 · Synthetic": {
            "paper": "MSE 4.03/R² .97 versus Greedy 15.41/.88.",
            "observed": "Declared 5-seed reconstruction: MSE 4.630 vs 4.722 and R² .271 vs .256; four wins and one tie.",
            "assessment": "Partially aligned; direction only",
        },
        "C6 · Completion": {
            "paper": "Roughly 95% versus 60% completed by 600 seconds.",
            "observed": "Released plot input at 590 seconds is exactly 100% versus 70%.",
            "assessment": "Partially aligned; endpoints differ",
        },
    }
    return (claim_rows,)


@app.cell
def _(claim_rows, mo):
    claim_picker = mo.ui.dropdown(
        options=list(claim_rows), value="C4 · California", label="Claim"
    )
    claim_picker
    return (claim_picker,)


@app.cell(hide_code=True)
def _(claim_picker, claim_rows, mo):
    selected_claim = claim_rows[claim_picker.value]
    status_color = "#2a9d68" if selected_claim["assessment"].startswith("Aligned") else "#d99b22"
    mo.Html(
        f"""
        <div style="border:1px solid #d9deea;border-left:6px solid {status_color};padding:18px;border-radius:10px">
          <h3 style="margin-top:0">{claim_picker.value}</h3>
          <p><b>Paper:</b> {selected_claim['paper']}</p>
          <p><b>Observed:</b> {selected_claim['observed']}</p>
          <p style="margin-bottom:0;color:{status_color}"><b>{selected_claim['assessment']}</b></p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The direct numerical check

    | Model/evidence | California test $R^2$ |
    |---|---:|
    | CLARITree released five-fold mean | 0.74994 |
    | CLARITree fresh outer-4 | 0.7431327225376608 |
    | STreeD released five-fold mean | 0.70485 |

    The fresh fit used the released outer-4 split and selected configuration
    (depth 4, 20 quantile thresholds, $\lambda=.001$, $\kappa=10^{-5}$).
    It took 135.54 seconds and matched the release row within floating-point
    precision. This is stronger than merely reading a result table.

    ## A transparent limitation: Figure 1

    The paper does not publish the numerical generator configuration or raw
    artifacts for its synthetic headline. The independent reconstruction
    fixes all missing choices up front: $n=1000$, an 80/20 split, four
    features and regimes, $\rho=.5$, $\sigma=2$, depth 2, 20 thresholds,
    $\lambda=\kappa=.001$, and seeds 0–4.

    | Seed | Greedy MSE | CLARITree MSE | Improvement |
    |---:|---:|---:|---:|
    | 0 | 4.282 | 4.195 | 0.086 |
    | 1 | 5.159 | 5.048 | 0.111 |
    | 2 | 3.913 | 3.831 | 0.082 |
    | 3 | 4.996 | 4.996 | 0.000 |
    | 4 | 5.262 | 5.078 | 0.183 |
    | **Mean** | **4.722** | **4.630** | **0.093** |

    This aligns with the direction but is much weaker than the paper's
    reported MSE gap. The responsible assessment is therefore **partial**.

    ## Reproduce the formal evidence

    From a checkout, the experiment command is:

    ```bash
    bash repro/run_local_claim_suite.sh
    ```

    It creates a clean pip environment, builds pinned Eigen and the pinned
    author extension, and prints one structured result covering C1–C6.
    The detailed illustrated report in `reports/claritree-6-claim-reproduction/`
    explains the implementation and every substitution.
    """)
    return


if __name__ == "__main__":
    app.run()
