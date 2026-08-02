# Conclusion

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_conclusion_20260802", "created_at": "2026-08-02T10:52:18+00:00", "title": "Overall findings"}
-->
Claims 1–3 are verified by source-tied exact certificates with controls that break outside the relevant assumptions. Claim 4 remains verified by all five released folds and a fresh author-entrypoint outer-fold fit. Claim 6 is fully resolved by falsification: released author artifacts consistently yield 100%/70%, not approximately 95%/60% under the locked ±5-point rule. Claim 5 remains honestly inconclusive because its Figure 1 protocol and data are absent; the reproducible ceiling is therefore five resolved claims, not a claim of perfect coverage.

All formal work used local CPU, fixed source SHAs, deterministic regenerators, and no GPU. The exact command is `bash repro/run_local_claim_suite.sh`; cheap claim tests are `python -m pytest -q repro/tests`. [Paper](https://ar5iv.labs.arxiv.org/html/2606.12840) · [author source pin](https://github.com/Yixiao-Wang-Stats/CLARITree/tree/4397f8dbc8b63751777e7918b89972e793796dfd) · [reproduction repository](https://github.com/MachineLearning-Nerd/icml26-repro-JjBozF4i2w-claritree) · [Hugging Face Space](https://huggingface.co/spaces/DineshAI/JjBozF4i2w).

---
<!-- trackio-cell
{"type": "code", "id": "cell_a78fe585d440", "created_at": "2026-07-22T10:45:22+00:00", "title": "Fail-closed publication gate", "command": ["python", "repro/src/run_publication_gate.py"], "exit_code": 0, "duration_s": 2.1, "pinned": true, "pinned_at": "2026-08-02T10:52:18+00:00"}
-->
````bash
$ python repro/src/run_publication_gate.py
````

````output
source pins: PASS
C1 source call chain + exact degree-two recurrence + degree-three control: PASS
C2 exact level sum + Z3 regime/control pair: PASS
C3 dominance + Appendix B.2 moments + relaxed-assumption controls: PASS
C4 released five folds + retained fresh outer-4 calibration: PASS
C5 fail-closed protocol exclusion: PASS
C6 author script + independent counts + timeout/display contract + 600 s control: PASS
targeted tests: PASS
publication gate: PASS
````

The gate preserves failures rather than rewriting them as successes: C5 remains excluded, and C6 must remain labelled falsified under released artifacts.
