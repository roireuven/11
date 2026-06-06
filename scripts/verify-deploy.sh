#!/usr/bin/env bash
# Verify public/ is ready for Firebase deploy (app + embedded docs + /doc/ site)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PUBLIC="$ROOT/public"

fail() { echo "verify-deploy: $1" >&2; exit 1; }

[[ -f "$PUBLIC/index.html" ]] || fail "missing public/index.html"
[[ -f "$PUBLIC/doc/index.html" ]] || fail "missing public/doc/index.html"

grep -q 'id="topbarDocBtn"' "$PUBLIC/index.html" || fail "app missing top bar Documentation button"
grep -q 'renderDocumentation' "$PUBLIC/index.html" || fail "app missing documentation page"
grep -q 'data-page="documentation"' "$PUBLIC/index.html" || fail "app missing sidebar Documentation link"

DOC_COUNT=$(find "$PUBLIC/doc" -name '*.md' | wc -l)
[[ "$DOC_COUNT" -ge 20 ]] || fail "expected 20+ doc files, found $DOC_COUNT"

echo "Deploy bundle OK — app + documentation ready for Firebase Hosting"
echo "  App:  $PUBLIC/index.html"
echo "  Docs: $PUBLIC/doc/ ($DOC_COUNT guides)"
