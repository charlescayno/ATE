#!/usr/bin/env bash
# Run manually in a Cloud Agent shell after GITHUB_TOKEN is available (or via install-deps.sh).
set -euo pipefail
if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "[git] GITHUB_TOKEN is not set in this session."
  echo "      Add secret GITHUB_TOKEN in Cloud Agents → Environments, then start a NEW agent run."
  exit 1
fi
git config --global credential.helper store
printf 'https://x-access-token:%s@github.com\n' "$GITHUB_TOKEN" >"$HOME/.git-credentials"
chmod 600 "$HOME/.git-credentials"
echo "[git] GitHub HTTPS credentials configured for this session."
git ls-remote origin HEAD >/dev/null && echo "[git] origin reachable."
