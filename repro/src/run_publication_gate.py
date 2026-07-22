"""Run the local CLARITree gate and fail closed until CPU calibration is retained.

The five evaluated claims are C1, C2, C3, C4, and C6.  C5 is deliberately
excluded by ``docs/C5_SCOPE_EXCLUSION.md`` because the author release does not
provide a runnable or fully parameterised headline synthetic protocol.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PYTHON = ROOT / ".venv/bin/python"
OUTPUTS = ROOT / "outputs"
DEMO_CALIBRATION = OUTPUTS / "california_outer4_cpp.json"
FIXED_SPLIT_CALIBRATION = OUTPUTS / "california_outer4_fixed_split.json"


def run(relative: str) -> tuple[bool, str]:
    completed = subprocess.run(
        [str(PYTHON), relative], cwd=ROOT, text=True, capture_output=True
    )
    detail = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0, detail[-2000:]


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def scalar_values(value: object) -> list[object]:
    if isinstance(value, dict):
        return [item for child in value.values() for item in scalar_values(child)]
    if isinstance(value, list):
        return [item for child in value for item in scalar_values(child)]
    return [value]


def calibration_is_valid(path: Path) -> tuple[bool, str]:
    if not path.is_file():
        return False, (
            f"missing retained CPU calibration artifact: {path.relative_to(ROOT)}"
        )
    try:
        record = read_json(path)
    except (OSError, json.JSONDecodeError) as error:
        return False, f"unreadable calibration artifact: {error}"
    expected_commit = "4397f8dbc8b63751777e7918b89972e793796dfd"
    source = record.get("source_pins", record)
    if expected_commit not in scalar_values(source):
        return False, "calibration does not retain the pinned author commit"
    elapsed = record.get("elapsed_seconds", record.get("elapsed_s"))
    if not isinstance(elapsed, (float, int)) or elapsed <= 0:
        return False, "calibration has no positive elapsed_seconds/elapsed_s"
    command = record.get("command")
    if not isinstance(command, (str, list)):
        return False, "calibration has no retained source command"
    if record.get("result") != "completed":
        return False, f"calibration result is not completed: {record.get('result')!r}"
    return True, "retained pinned CPU calibration artifact is valid"


def fixed_split_is_valid() -> tuple[bool, str]:
    valid, detail = calibration_is_valid(FIXED_SPLIT_CALIBRATION)
    if not valid:
        return valid, detail
    record = read_json(FIXED_SPLIT_CALIBRATION)
    if record.get("source_entrypoint") != "scripts.run_ours_outer.fit_eval":
        return False, "fixed-split calibration did not use the author experiment entrypoint"
    metrics = record.get("metrics")
    if not isinstance(metrics, dict) or not isinstance(metrics.get("test_r2"), (float, int)):
        return False, "fixed-split calibration has no numeric test_r2"
    committed = read_json(OUTPUTS / "california_artifact_readback.json")
    expected = next(
        row["test_r2"]
        for row in committed["claritree"]["selected_folds"]
        if row["outer"] == "outer_4"
    )
    observed = float(metrics["test_r2"])
    if abs(observed - float(expected)) > 1e-6:
        return False, f"fixed-split test_r2 mismatch: observed={observed}, committed={expected}"
    return True, f"fixed-split test_r2 matches committed outer_4 result ({observed:.9f})"


def main() -> None:
    checks: dict[str, dict[str, object]] = {}
    for name, script in {
        "source_pins": "repro/src/verify_source_pins.py",
        "source_structure_c1": "repro/src/verify_source_structure.py",
        "core_claims_c1_c3": "repro/src/verify_core_claims.py",
        "theorem_consequences_c2_c3": "repro/src/verify_theorem_consequences.py",
        "california_c4": "repro/src/verify_california_artifacts.py",
        "completion_c6": "repro/src/verify_completion_artifacts.py",
    }.items():
        passed, detail = run(script)
        checks[name] = {"passed": passed, "detail": detail}

    tests = subprocess.run(
        [str(PYTHON), "-m", "pytest", "-q", "repro/tests"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    checks["tests"] = {
        "passed": tests.returncode == 0,
        "detail": (tests.stdout + tests.stderr).strip()[-2000:],
    }
    demo_ok, demo_detail = calibration_is_valid(DEMO_CALIBRATION)
    checks["cpu_demo_memory_calibration"] = {"passed": demo_ok, "detail": demo_detail}
    fixed_ok, fixed_detail = fixed_split_is_valid()
    checks["cpu_fixed_split_c4_calibration"] = {"passed": fixed_ok, "detail": fixed_detail}

    c6 = read_json(OUTPUTS / "completion_artifact_readback.json")
    c5_scope = ROOT / "docs/C5_SCOPE_EXCLUSION.md"
    scope_ok = c5_scope.is_file() and "must never be presented" in c5_scope.read_text(encoding="utf-8")
    checks["c5_scope_exclusion"] = {"passed": scope_ok, "detail": str(c5_scope.relative_to(ROOT))}

    local_checks_passed = all(bool(check["passed"]) for check in checks.values())
    payload = {
        "paper": "JjBozF4i2w",
        "selected_anchored_claims": ["C1", "C2", "C3", "C4", "C6"],
        "excluded_anchored_claims": {"C5": "source protocol missing; see docs/C5_SCOPE_EXCLUSION.md"},
        "c6_disclosure": {
            "exact_release_endpoint_percent": {
                "claritree": c6["claritree"]["completion_rate_percent"],
                "streed": c6["streed"]["completion_rate_percent"],
            },
            "paper_rounded_endpoint_percent": c6["paper_rounded_endpoint_percent"],
            "exact_parity": c6["paper_rounded_endpoint_exactly_reproduced"],
            "direction_verified": c6["source_backed_direction_verified"],
        },
        "checks": checks,
        "tests_passed": bool(checks["tests"]["passed"]),
        "publication_gate_passed": local_checks_passed,
    }
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    (OUTPUTS / "publication_gate.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    if not local_checks_passed:
        raise SystemExit("publication gate is not ready")


if __name__ == "__main__":
    main()
