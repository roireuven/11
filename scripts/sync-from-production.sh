#!/usr/bin/env bash
# Download the live app from Firebase Hosting into public/
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PUBLIC="$ROOT/public"
BASE="https://hotel-restaurant-minimart.firebaseapp.com"

mkdir -p "$PUBLIC/assets/data" "$PUBLIC/assets/locales"

echo "Syncing app index.html..."
curl -fsSL "$BASE/" -o "$PUBLIC/index.html"

echo "Syncing data assets..."
curl -fsSL "$BASE/assets/data/embedded-sample.js" -o "$PUBLIC/assets/data/embedded-sample.js"
curl -fsSL "$BASE/assets/data/nisha1-menu-dataset.js" -o "$PUBLIC/assets/data/nisha1-menu-dataset.js"

LOCALES=(en es fr de ja ko ar hi th vi id tr ru it nl pl he lo pt-BR zh-Hans zh-Hant)
echo "Syncing ${#LOCALES[@]} locale files..."
for loc in "${LOCALES[@]}"; do
  curl -fsSL "$BASE/assets/locales/${loc}.json" -o "$PUBLIC/assets/locales/${loc}.json"
done

echo "App sync done."
