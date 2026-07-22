"""Fail closed if the pinned author implementation or Eigen dependency changed."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    "upstream": "4397f8dbc8b63751777e7918b89972e793796dfd",
    "repro/vendor/eigen": "3147391d946bb4b6c68edd901f2add6ac1f31f8c",
}


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def main() -> None:
    records: dict[str, dict[str, str]] = {}
    for relative, expected in EXPECTED.items():
        directory = ROOT / relative
        commit = git(directory, "rev-parse", "HEAD")
        dirty = git(directory, "status", "--porcelain")
        if commit != expected or dirty:
            raise SystemExit(
                f"source pin failed for {relative}: commit={commit}, dirty={bool(dirty)}"
            )
        records[relative] = {"commit": commit, "dirty": "false"}
    output = ROOT / "outputs" / "source_pins.json"
    output.write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
