#!/usr/bin/env python3
"""Add restaurant QR order floor i18n keys to all app locale JSON files."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "public" / "assets" / "locales"
MARKER = "hrmm-rest-qr-floor-keys-v1"

EN_KEYS = {
    "orderTypeQrOrders": "QR Orders",
    "orderNumFloorTitle": "QR order numbers — status at a glance",
    "orderNumFloorGroup": "Restaurant QR order number tiles",
    "orderNumFloorHelp": "Colors show state for each QR order slot (1–60): {free} = take a new order; {live} = kitchen in progress (tap opens bill); {pay} = check ready, settle payment.",
    "allOrderNums": "All QR orders (1–60)",
    "orderNumWord": "Order #",
    "emptyActiveForOrderNum": "No active orders for Order #{n}",
    "emptyActiveAnyOrderNum": "No active orders on any QR order number",
    "tileTitleOrderAvail": "Order #{n} — available, no bill",
    "tileTitleOrderPay": "Order #{n} — payment pending, tap to close",
    "tileTitleOrderLive": "Order #{n} — open order, tap for bill",
    "showAllOrdersTitle": "Show every open QR order (all numbers 1–60)",
}


def patch_locale_file(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    rest = data.setdefault("restaurant", {})
    changed = False
    for key, val in EN_KEYS.items():
        if rest.get(key) != val:
            rest[key] = val
            changed = True
    meta = data.setdefault("_meta", {})
    if meta.get("restQrFloorKeys") != MARKER:
        meta["restQrFloorKeys"] = MARKER
        changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    if not LOCALES_DIR.is_dir():
        print(f"Skip — missing {LOCALES_DIR}", file=sys.stderr)
        return 0
    count = sum(1 for p in sorted(LOCALES_DIR.glob("*.json")) if patch_locale_file(p))
    print(f"Locale rest QR floor keys: {count} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
