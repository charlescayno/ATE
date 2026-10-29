#!/usr/bin/env bash
# Cloud Agent install: headless PI ATE checks (no GPIB, no PySide2 GUI).
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo apt-get install -y -qq python3-pip python3-venv git
fi
python3 -m pip install --user -q openpyxl pandas pyvisa numpy
