# Negative controls


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_6590ad8fa9bc", "created_at": "2026-07-22T10:45:04+00:00", "title": "Controls"}
-->
Shuffled-target CLARITree control reaches only train R2 0.3203. The gate rejects an absent/mismatched fixed-split calibration artifact.


---
<!-- trackio-cell
{"type": "code", "id": "cell_238cbb78697a", "created_at": "2026-07-22T10:45:24+00:00", "title": "Verification tests", "command": ["python", "-m", "pytest", "-q", "repro/tests"], "exit_code": 0, "duration_s": 0.699}
-->
````bash
$ python -m pytest -q repro/tests
````

exit 0 · 0.7s


````output
.........                                                                [100%]
9 passed in 0.43s

````
