#!/usr/bin/env bash
# Cloud Agent install: headless PI ATE checks (no GPIB, no PySide2 GUI).
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo apt-get install -y -qq python3-pip python3-venv git
fi
python3 -m pip install --user -q openpyxl pandas pyvisa numpy

# Git push from Cloud Agent when Cursor injects GITHUB_TOKEN (new runs only).
if [ -n "${GITHUB_TOKEN:-}" ]; then
  git config --global credential.helper store
  printf 'https://x-access-token:%s@github.com\n' "$GITHUB_TOKEN" >"$HOME/.git-credentials"
  chmod 600 "$HOME/.git-credentials"
  git config --global url."https://github.com/".insteadOf "git@github.com:"
fi
