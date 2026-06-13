#!/usr/bin/env python3
"""Add missing app UI i18n keys to all locale JSON files in public/assets/locales/."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "public" / "assets" / "locales"
KEYS_FILE = ROOT / "doc" / "i18n" / "locale-gap-keys.json"
MARKER = "hrmm-locale-gap-keys-v1"
SECTIONS = (
    "dashboard",
    "g",
    "grid",
    "minimart",
    "msg",
    "orderHistory",
    "restaurant",
    "settings",
)


def load_keys() -> dict:
    return json.loads(KEYS_FILE.read_text(encoding="utf-8"))


def patch_locale_file(path: Path, all_keys: dict) -> bool:
    code = path.stem
    block = all_keys.get(code) or all_keys["en"]
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False

    for section in SECTIONS:
        entries = block.get(section) or {}
        if not entries:
            continue
        if section not in data or not isinstance(data[section], dict):
            data[section] = data.get(section) or {}
        for key, val in entries.items():
            if val and data[section].get(key) != val:
                data[section][key] = val
                changed = True

    meta = data.setdefault("_meta", {})
    if meta.get("localeGapKeys") != MARKER:
        meta["localeGapKeys"] = MARKER
        changed = True

    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    if not LOCALES_DIR.is_dir():
        print(f"Skip locale patch — missing {LOCALES_DIR}", file=sys.stderr)
        return 0
    if not KEYS_FILE.is_file():
        print(f"Missing {KEYS_FILE}", file=sys.stderr)
        return 1

    all_keys = load_keys()
    count = 0
    for path in sorted(LOCALES_DIR.glob("*.json")):
        if patch_locale_file(path, all_keys):
            count += 1
            print(f"Patched {path.name}")
    print(f"Locale gap keys: {count} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
