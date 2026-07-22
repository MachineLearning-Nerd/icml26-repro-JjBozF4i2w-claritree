#!/usr/bin/env bash
set -euo pipefail

BASE_PYTHON="/Users/dineshjinjala/Documents/AllCode/ICMLPapers/papers/.repro-venv/bin/python"

"${BASE_PYTHON}" -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -r requirements-repro.txt
.venv/bin/python repro/src/bootstrap_sources.py
.venv/bin/python repro/src/run_local_claim_suite.py
