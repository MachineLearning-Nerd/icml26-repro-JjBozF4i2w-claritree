# Executive summary

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_exec_20260802", "created_at": "2026-08-02T10:52:18+00:00", "title": "Executive summary", "pinned": true, "pinned_at": "2026-08-02T10:52:18+00:00"}
-->
This CPU-only audit resolves five of six official claims against the paper and author release pinned at [`4397f8d`](https://github.com/Yixiao-Wang-Stats/CLARITree/tree/4397f8dbc8b63751777e7918b89972e793796dfd). Exact symbolic and source-tied certificates verify Claims 1–3; released folds plus a fresh author-entrypoint fit preserve the existing verification of Claim 4. Claim 5 remains inconclusive because the Figure 1 generator, data, and numeric protocol are absent from the complete public source history. The released artifacts falsify Claim 6's approximate 95%/60% endpoints under a locked ±5-point rule: the unchanged author code and an independent recount agree on 100%/70%, while retaining its 600-second display convention and 590-second operational timeout rule.

| | This reproduction | Full replication |
| --- | --- | --- |
| Scope | All six official claims; exact author-source path where released | Figure 1 plus all datasets and repeated training runs |
| Hardware | Apple arm64 CPU, 8 logical CPUs; no GPU | Author reports a 48-core, 768 GB environment |
| Compute time | Scientific checks about 95 s; clean environment and builds under 3 min | Up to 600 s per method/problem, plus missing Figure 1 protocol |
| Cost | Local CPU, $0 incremental cloud cost | Not estimated from the released materials |
| Outcome | C1–C4 verified; C6 falsified; C5 inconclusive | Not claimed |

Provenance: [paper](https://ar5iv.labs.arxiv.org/html/2606.12840), [public reproduction repository](https://github.com/MachineLearning-Nerd/icml26-claritree), [existing Hugging Face Space](https://huggingface.co/spaces/DineshAI/JjBozF4i2w). The protocol used local CPU only; no Hugging Face Job, Bucket, model, or dataset repository was created.

---
<!-- trackio-cell
{"type": "figure", "id": "cell_clari_poster_20260802", "created_at": "2026-08-02T10:52:18+00:00", "title": "Reproduction poster", "pinned": true, "pinned_at": "2026-08-02T10:52:18+00:00", "poster": true}
-->
````html
<!-- poster_embed.html -->
<iframe src="poster_embed.html" title="CLARITree six-claim reproduction poster" width="100%" height="1120" loading="lazy"></iframe>
````

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_clari_protocol_20260802", "created_at": "2026-08-02T10:52:18+00:00", "title": "Pinned protocol and no-regression lineage"}
-->
The deterministic entrypoint is `bash repro/run_local_claim_suite.sh`. It creates a project-local Python 3.12 environment, checks out the author source and Eigen 3.4.0 at exact SHAs, compiles the released extension, runs the source, symbolic, artifact, and control checks, then repeats California outer fold 4 through `scripts.run_ours_outer.fit_eval`. The previous judged Space's Methods and Negative-controls evidence is retained here and on the relevant claim pages; its historical hash routes redirect to the corresponding canonical pages.
