#!/usr/bin/env python3
"""Apply vehicle rental i18n keys to locale JSON files."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "public" / "assets" / "locales"
KEYS_FILE = ROOT / "doc" / "i18n" / "vehicle-rental-keys.json"


def apply_keys(data: dict, flat: dict) -> bool:
    changed = False
    for full_key, val in flat.items():
        if not val:
            continue
        parts = full_key.split(".", 1)
        if len(parts) != 2:
            continue
        sec, key = parts
        block = data.setdefault(sec, {})
        if block.get(key) != val:
            block[key] = val
            changed = True
    return changed


def main() -> int:
    if not LOCALES_DIR.is_dir() or not KEYS_FILE.is_file():
        print("Skip vehicle rental locale keys")
        return 0
    all_keys = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
    count = 0
    for path in sorted(LOCALES_DIR.glob("*.json")):
        code = path.stem
        flat = all_keys.get(code) or all_keys["en"]
        data = json.loads(path.read_text(encoding="utf-8"))
        if apply_keys(data, flat):
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            count += 1
    print(f"Locale vehicle rental keys: {count} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
