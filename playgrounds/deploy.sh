#!/usr/bin/env bash
# Deploy each built playground to its repository's gh-pages branch.
# Usage: playgrounds/deploy.sh "commit message"   (run only after the finish review ships)
set -euo pipefail
MSG="${1:-design: new world}"
declare -A REPO=( [pulsehttp]=PulseHTTP [gitengine]=GitEngine [jsonlp]=JSON-Lexer-Parser-From-Scratch [wcgo]=wc-Go )
HERE="$(cd "$(dirname "$0")" && pwd)"
for site in pulsehttp gitengine jsonlp wcgo; do
  repo="$HOME/Coding/${REPO[$site]}"
  wt="$(mktemp -d)"
  git -C "$repo" worktree add -q "$wt" gh-pages
  cp "$HERE/$site/index.html" "$wt/index.html"
  git -C "$wt" add index.html
  if git -C "$wt" diff --cached --quiet; then echo "unchanged: $site"; else git -C "$wt" commit -q -m "$MSG" && git -C "$wt" push -q origin gh-pages && echo "deployed: $site"; fi
  git -C "$repo" worktree remove --force "$wt"
done
