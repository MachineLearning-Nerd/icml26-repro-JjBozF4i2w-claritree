#!/usr/bin/env bash
set -euo pipefail

uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements-repro.txt pip
PIP_USER=0 .venv/bin/python repro/src/bootstrap_sources.py
PIP_USER=0 .venv/bin/python repro/src/run_local_claim_suite.py
