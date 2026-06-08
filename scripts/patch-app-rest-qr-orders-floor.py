#!/usr/bin/env python3
"""Restaurant POS — QR order numbers 1–60 floor (third order type beside Table and Room Service)."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _load_fragments():
    frag_path = Path(__file__).resolve().parent / "_rest_qr_orders_floor_v15_fragments.py"
    spec = importlib.util.spec_from_file_location("_rest_qr_orders_floor_v15_fragments", frag_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Missing fragments: {frag_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


frag = _load_fragments()
MARKER = "HRMM-REST-QR-ORDERS-FLOOR-v1"
INDEX = Path("public/index.html")
JS_ANCHOR = "function renderRestaurant() {"


def _replace(content: str, old: str, new: str, label: str) -> str:
    if old not in content:
        if new.split("\n", 1)[0] in content:
            return content
        raise SystemExit(f"Could not apply {label}")
    return content.replace(old, new, 1)


def _repair_duplicates(content: str) -> str:
    """Each deploy re-synced from hosting and re-ran state injection — dedupe before patch."""
    block = (
        r"(?:/\*\* QR order slot 1–60 — focus like table floor\. \*/\s*"
        r"let restOrderNum = '';\s*"
        r"let restFocusAllOrderNums = true;\s*)+"
    )
    once = frag.REST_ORDER_NUM_STATE.strip() + "\n"
    content = re.sub(block, once, content, count=1)
    if content.count("let restOrderNum = '';") > 1:
        # Fallback: keep first declaration block only
        first = content.find("let restOrderNum = '';")
        while True:
            second = content.find("let restOrderNum = '';", first + 1)
            if second < 0:
                break
            end = content.find("let restFocusAllOrderNums = true;", second)
            if end < 0:
                break
            end = content.find("\n", end) + 1
            # include preceding comment if present
            start = content.rfind("/** QR order slot", 0, second)
            if start < 0 or start < first:
                start = second
            content = content[:start] + content[end:]

    dup_empty = (
        "  else if (restOrderType === 'QR Orders' && !restFocusAllOrderNums) emptyActMsg = "
        "t('restaurant.emptyActiveForOrderNum', { n: String(restOrderNum || '') });\n"
        "  else if (restOrderType === 'QR Orders') emptyActMsg = t('restaurant.emptyActiveAnyOrderNum');\n"
    )
    while content.count(dup_empty) > 1:
        content = content.replace(dup_empty, "", 1)
    return content


def _ensure_order_num_state(content: str) -> str:
    if "let restOrderNum = '';" in content:
        return content
    return _replace(content, frag.FOCUS_ALL_TABLES_OLD, frag.FOCUS_ALL_TABLES_NEW, "rest order num state")


def patch(content: str) -> str:
    content = _repair_duplicates(content)
    if MARKER in content and "restRenderOrderNumFloorHtml" in content:
        print(f"Already patched {MARKER} — running integrity repair")
    else:
        if MARKER not in content:
            content = content.replace(
                "<title>HotelRestaurantMini-MartManagement</title>",
                f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
                1,
            )

    content = _ensure_order_num_state(content)

    if "function restGetOrdersForOrderNum" not in content:
        content = content.replace(
            "function restGetTableFloorState(tableLabel) {",
            frag.REST_ORDER_NUM_HELPERS + "\nfunction restGetTableFloorState(tableLabel) {",
            1,
        )

    if "/* HRMM rest QR order numbers floor */" not in content:
        content = content.replace(
            "    /* HRMM guest QR restaurant order */",
            "    /* HRMM guest QR restaurant order */\n" + frag.REST_ORDER_NUM_CSS,
            1,
        )

    content = _replace(content, frag.ORDER_TYPE_HTML_OLD, frag.ORDER_TYPE_HTML_NEW, "order type buttons")
    content = _replace(content, frag.SEL_HTML_BRANCH_OLD, frag.SEL_HTML_BRANCH_NEW, "QR orders floor branch")
    content = _replace(content, frag.REST_APPLY_FILTER_OLD, frag.REST_APPLY_FILTER_NEW, "active order filter")
    content = _replace(content, frag.REST_SET_ORDER_TYPE_OLD, frag.REST_SET_ORDER_TYPE_NEW, "restSetOrderType")
    content = _replace(content, frag.REST_SEND_KITCHEN_ELSE_OLD, frag.REST_SEND_KITCHEN_ELSE_NEW, "restSendToKitchen")
    if frag.REST_SEND_ROOM_ELSE_OLD in content:
        content = content.replace(frag.REST_SEND_ROOM_ELSE_OLD, frag.REST_SEND_ROOM_ELSE_NEW, 1)
    content = content.replace(frag.SHOW_ALL_OLD, frag.SHOW_ALL_NEW)
    content = _replace(content, frag.FILTER_LABEL_TABLE_OLD, frag.FILTER_LABEL_TABLE_NEW, "filter label")
    content = _replace(content, frag.SCOPE_HINT_TABLE_OLD, frag.SCOPE_HINT_TABLE_NEW, "scope hint")
    content = _replace(content, frag.EMPTY_ACT_TABLE_OLD, frag.EMPTY_ACT_TABLE_NEW, "empty active msg")

    if frag.GUEST_MERGE_TARGET_OLD in content:
        content = content.replace(frag.GUEST_MERGE_TARGET_OLD, frag.GUEST_MERGE_TARGET_NEW, 1)
    if frag.GUEST_MERGE_META_OLD in content:
        content = content.replace(frag.GUEST_MERGE_META_OLD, frag.GUEST_MERGE_META_NEW, 1)
    if frag.GUEST_NOTIFY_OLD in content:
        content = content.replace(frag.GUEST_NOTIFY_OLD, frag.GUEST_NOTIFY_NEW, 1)

    if getattr(frag, "SHOW_ALL_BROKEN", None):
        content = content.replace(frag.SHOW_ALL_BROKEN, frag.SHOW_ALL_NEW)

    content = re.sub(r"<!-- HRMM-REST-QR-ORDERS-FLOOR-v\d+ -->", f"<!-- {MARKER} -->", content)
    return _repair_duplicates(content)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — restaurant QR order numbers 1–60 floor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
