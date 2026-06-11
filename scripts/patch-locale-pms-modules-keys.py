#!/usr/bin/env python3
"""PMS module form labels (21 locales) under pms.* in public/assets/locales/*.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "public" / "assets" / "locales"
KEYS_FILE = ROOT / "doc" / "i18n" / "pms-modules-keys.json"
MARKER = "hrmm-pms-modules-keys-v1"


def load_keys() -> dict:
    return json.loads(KEYS_FILE.read_text(encoding="utf-8"))


def patch_locale_file(path: Path, all_keys: dict) -> bool:
    code = path.stem
    block = all_keys.get(code) or all_keys["en"]
    data = json.loads(path.read_text(encoding="utf-8"))
    pms = data.setdefault("pms", {})
    changed = False

    for key, val in block.items():
        if val and pms.get(key) != val:
            pms[key] = val
            changed = True

    meta = data.setdefault("_meta", {})
    if meta.get("pmsModulesKeys") != MARKER:
        meta["pmsModulesKeys"] = MARKER
        changed = True

    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    if not LOCALES_DIR.is_dir():
        print(f"Skip — missing {LOCALES_DIR}", file=sys.stderr)
        return 0
    if not KEYS_FILE.is_file():
        print(f"Missing {KEYS_FILE} — run scripts/generate-pms-modules-keys.py", file=sys.stderr)
        return 1

    all_keys = load_keys()
    count = sum(1 for p in sorted(LOCALES_DIR.glob("*.json")) if patch_locale_file(p, all_keys))
    print(f"Locale PMS module keys: {count} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
