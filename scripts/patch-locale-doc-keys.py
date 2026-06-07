#!/usr/bin/env python3
"""Add documentation i18n keys to all app locale JSON files in public/assets/locales/."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "public" / "assets" / "locales"
MESSAGES = ROOT / "doc" / "i18n" / "messages.json"
MARKER = "hrmm-doc-keys-v1"

# Keys in messages.json used for app UI
APP_KEY_MAP = {
    ("nav", "sectionHelp"): "nav_help",
    ("nav", "documentation"): "doc_label",
    ("topbar", "documentation"): "doc_label",
    ("topbar", "documentationTitle"): "nav_topbar_action",
    ("bnav", "documentation"): "bnav_docs",
    ("doc", "toolbarTitle"): "home_title",
    ("doc", "openNewTab"): "ui_open_tab",
    ("doc", "loginLink"): "doc_label",
}


def load_messages() -> dict:
    return json.loads(MESSAGES.read_text(encoding="utf-8"))


def patch_locale_file(path: Path, messages: dict) -> bool:
    code = path.stem
    data = json.loads(path.read_text(encoding="utf-8"))
    block = messages.get(code) or messages["en"]
    changed = False

    for (section, key), msg_key in APP_KEY_MAP.items():
        if section not in data or not isinstance(data[section], dict):
            data[section] = data.get(section) or {}
        val = block.get(msg_key) or messages["en"].get(msg_key)
        if val and data[section].get(key) != val:
            data[section][key] = val
            changed = True

    meta = data.setdefault("_meta", {})
    if meta.get("docKeys") != MARKER:
        meta["docKeys"] = MARKER
        changed = True

    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    if not LOCALES_DIR.is_dir():
        print(f"Skip locale patch — missing {LOCALES_DIR}", file=sys.stderr)
        return 0
    if not MESSAGES.is_file():
        print(f"Missing {MESSAGES}", file=sys.stderr)
        return 1

    messages = load_messages()
    count = 0
    for path in sorted(LOCALES_DIR.glob("*.json")):
        if patch_locale_file(path, messages):
            count += 1
            print(f"Patched {path.name}")
    print(f"Locale doc keys: {count} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
