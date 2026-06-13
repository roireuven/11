#!/usr/bin/env python3
"""Apply modal form i18n keys to all locale JSON files."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "public" / "assets" / "locales"
KEYS_FILE = ROOT / "doc" / "i18n" / "modal-form-keys.json"
MARKER = "hrmm-modal-form-keys-v1"


def patch_locale_file(path: Path, all_keys: dict) -> bool:
    code = path.stem
    block = all_keys.get(code) or all_keys["en"]
    data = json.loads(path.read_text(encoding="utf-8"))
    modal = data.setdefault("modal", {})
    changed = False
    for key, val in block.items():
        if val and modal.get(key) != val:
            modal[key] = val
            changed = True
    # Ensure g.iconLabel / g.phIcon exist (used by menu modals)
    g = data.setdefault("g", {})
    msg = data.get("msg") or {}
    for gk in ("iconLabel", "phIcon"):
        src = msg.get(gk) or (all_keys.get("en", {}).get("modal", {}) if False else None)
        if msg.get(gk) and g.get(gk) != msg[gk]:
            g[gk] = msg[gk]
            changed = True
        elif not g.get(gk) and block.get("modal") is None:
            pass
    if msg.get("iconLabel") and g.get("iconLabel") != msg["iconLabel"]:
        g["iconLabel"] = msg["iconLabel"]
        changed = True
    if msg.get("phIcon") and g.get("phIcon") != msg["phIcon"]:
        g["phIcon"] = msg["phIcon"]
        changed = True
    meta = data.setdefault("_meta", {})
    if meta.get("modalFormKeys") != MARKER:
        meta["modalFormKeys"] = MARKER
        changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    if not LOCALES_DIR.is_dir() or not KEYS_FILE.is_file():
        print(f"Skip — need build + {KEYS_FILE}", file=sys.stderr)
        return 0
    all_keys = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
    count = sum(1 for p in sorted(LOCALES_DIR.glob("*.json")) if patch_locale_file(p, all_keys))
    print(f"Locale modal form keys: {count} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
