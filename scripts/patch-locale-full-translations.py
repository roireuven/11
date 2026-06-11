#!/usr/bin/env python3
"""Apply full locale translations from doc/i18n/locale-full-translations.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "public" / "assets" / "locales"
KEYS_FILE = ROOT / "doc" / "i18n" / "locale-full-translations.json"
MARKER = "hrmm-locale-full-translations-v1"


def patch_locale_file(path: Path, block: dict) -> bool:
    if not block:
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for section, entries in block.items():
        if section == "_meta" or not isinstance(entries, dict):
            continue
        if section not in data or not isinstance(data[section], dict):
            data[section] = data.get(section) or {}
        for key, val in entries.items():
            if val and data[section].get(key) != val:
                data[section][key] = val
                changed = True
    meta = data.setdefault("_meta", {})
    if meta.get("localeFullTranslations") != MARKER:
        meta["localeFullTranslations"] = MARKER
        changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    if not LOCALES_DIR.is_dir():
        print(f"Skip — missing {LOCALES_DIR}", file=sys.stderr)
        return 0
    if not KEYS_FILE.is_file():
        print(f"Skip — missing {KEYS_FILE} (run generate-locale-full-translations.py)", file=sys.stderr)
        return 0

    all_keys = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
    count = 0
    for path in sorted(LOCALES_DIR.glob("*.json")):
        code = path.stem
        if code == "en":
            continue
        if patch_locale_file(path, all_keys.get(code, {})):
            count += 1
            print(f"Patched {path.name}")
    print(f"Locale full translations: {count} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
