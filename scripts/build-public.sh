#!/usr/bin/env bash
# Build public/ for Firebase deploy: production app + doc site at /doc/
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PUBLIC="$ROOT/public"
DOC_SRC="$ROOT/doc"

bash "$ROOT/scripts/sync-from-production.sh"

echo "Patching mobile top bar..."
python3 "$ROOT/scripts/patch-app-mobile-menu.py"

echo "Embedding documentation into app..."
python3 "$ROOT/scripts/patch-app-embed-docs.py"

echo "Copying documentation site to public/doc/..."
rm -rf "$PUBLIC/doc"
mkdir -p "$PUBLIC/doc"
cp "$DOC_SRC/index.html" "$DOC_SRC/_sidebar.md" "$PUBLIC/doc/"
cp "$DOC_SRC"/*.md "$PUBLIC/doc/"

echo "Build complete."
echo "  App:  $PUBLIC/index.html (Documentation button + sidebar page)"
echo "  Docs: $PUBLIC/doc/ ($(find "$PUBLIC/doc" -type f | wc -l) files at /doc/)"
echo ""
echo "  npm run verify   — check bundle"
echo "  npm run deploy   — build + verify + upload to Firebase"
