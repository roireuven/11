#!/usr/bin/env bash
# Build public/ for Firebase deploy: production app + doc site at /doc/
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PUBLIC="$ROOT/public"
DOC_SRC="$ROOT/doc"

bash "$ROOT/scripts/sync-from-production.sh"

echo "Embedding documentation into app..."
python3 "$ROOT/scripts/patch-app-embed-docs.py"

echo "Copying documentation site to public/doc/..."
rm -rf "$PUBLIC/doc"
mkdir -p "$PUBLIC/doc"
cp "$DOC_SRC/index.html" "$DOC_SRC/_sidebar.md" "$PUBLIC/doc/"
cp "$DOC_SRC"/*.md "$PUBLIC/doc/"

echo "Build complete."
echo "  App:  $PUBLIC/index.html"
echo "  Docs: $PUBLIC/doc/index.html ($(find "$PUBLIC/doc" -type f | wc -l) files)"
echo ""
echo "Deploy: npm run deploy"
echo "Local:  npm run serve  → http://127.0.0.1:5000/doc/"
