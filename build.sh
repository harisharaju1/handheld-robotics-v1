#!/usr/bin/env bash
# Regenerate all CAD exports, then commit and push.
set -euo pipefail
cd "$(dirname "$0")"
source ~/venvs/cad/bin/activate
python cad/build.py "$@"
git add -A
if ! git diff --cached --quiet; then
  git commit -q -m "CAD: regenerate base v1 parts and exports" \
    -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" \
    -m "Claude-Session: https://claude.ai/code/session_013jxudpWso4YogE98cbKK81"
  git push -u origin main
fi
echo "Done. Exports in ./exports"
