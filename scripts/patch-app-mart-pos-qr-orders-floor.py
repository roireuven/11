#!/usr/bin/env python3
"""Mini-Mart + POS — Room Service and QR order numbers 1–60 floor."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _load_fragments():
    frag_path = Path(__file__).resolve().parent / "_mart_pos_qr_orders_floor_v16_fragments.py"
    spec = importlib.util.spec_from_file_location("_mart_pos_qr_orders_floor_v16_fragments", frag_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Missing fragments: {frag_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


frag = _load_fragments()
MARKER = "HRMM-MART-POS-QR-ORDERS-FLOOR-v1"
INDEX = Path("public/index.html")


def _replace(content: str, old: str, new: str, label: str) -> str:
    if old not in content:
        if new.split("\n", 1)[0] in content or new[:60] in content:
            return content
        raise SystemExit(f"Could not apply {label}")
    return content.replace(old, new, 1)


def _ensure_state(content: str) -> str:
    if "let martOrderType = 'Room Service';" in content:
        return content
    anchor = "let martCart = [];"
    if anchor not in content:
        raise SystemExit("Could not find martCart anchor for state injection")
    return content.replace(anchor, anchor + "\n" + frag.MART_POS_STATE.strip(), 1)


def _ensure_helpers(content: str) -> str:
    if "function martGetOrdersForOrderNum" in content:
        return content
    return content.replace(
        "function martGetOpenInScope() {",
        frag.MART_POS_HELPERS + "\nfunction martGetOpenInScope() {",
        1,
    )


def patch(content: str) -> str:
    if MARKER not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )

    content = _ensure_state(content)
    content = _ensure_helpers(content)

    content = _replace(content, frag.MART_GET_OPEN_OLD, frag.MART_GET_OPEN_NEW, "martGetOpenInScope")
    content = _replace(content, frag.POS_GET_OPEN_OLD, frag.POS_GET_OPEN_NEW, "posGetOpenInScope")
    content = _replace(content, frag.MART_NEW_ORDER_CARD_OLD, frag.MART_NEW_ORDER_CARD_NEW, "mart new order card")
    content = _replace(content, frag.MART_PUT_BILL_START_OLD, frag.MART_PUT_BILL_START_NEW, "martPutBillOnCustomer")
    content = _replace(content, frag.MART_CHECKOUT_CTX_OLD, frag.MART_CHECKOUT_CTX_NEW, "martCheckout")
    content = _replace(content, frag.MART_FILTER_LABEL_OLD, frag.MART_FILTER_LABEL_NEW, "mart filter label")
    content = _replace(content, frag.MART_SCOPE_HINT_OLD, frag.MART_SCOPE_HINT_NEW, "mart scope hint")
    content = content.replace(frag.MART_SHOW_ALL_OLD, frag.MART_SHOW_ALL_NEW)
    content = _replace(content, frag.MART_CAN_CHARGE_OLD, frag.MART_CAN_CHARGE_NEW, "mart canChargeRoom")
    content = _replace(content, frag.MART_EMPTY_ACT_OLD, frag.MART_EMPTY_ACT_NEW, "mart empty active")
    content = _replace(content, frag.POS_TOP_OLD, frag.POS_TOP_NEW, "pos top panel")
    content = _replace(content, frag.POS_PUT_BILL_START_OLD, frag.POS_PUT_BILL_START_NEW, "posPutBillOnRoom")
    content = _replace(content, frag.POS_CHECKOUT_CTX_OLD, frag.POS_CHECKOUT_CTX_NEW, "posCheckout")
    content = _replace(content, frag.POS_NAME_PART_OLD, frag.POS_NAME_PART_NEW, "pos name part")
    content = _replace(content, frag.POS_SCOPE_HINT_OLD, frag.POS_SCOPE_HINT_NEW, "pos scope hint")
    content = content.replace(frag.POS_SHOW_ALL_OLD, frag.POS_SHOW_ALL_NEW)
    content = _replace(content, frag.POS_CAN_CHARGE_OLD, frag.POS_CAN_CHARGE_NEW, "pos canChargeRoom")
    content = _replace(content, frag.POS_HAS_CONTACT_OLD, frag.POS_HAS_CONTACT_NEW, "pos hasPosContact")
    content = _replace(content, frag.POS_EMPTY_ACT_OLD, frag.POS_EMPTY_ACT_NEW, "pos empty active")

    if frag.GUEST_MART_SUBMIT_OLD in content:
        content = content.replace(frag.GUEST_MART_SUBMIT_OLD, frag.GUEST_MART_SUBMIT_NEW, 1)
    if frag.GUEST_MART_CTX_SHOW_OLD in content:
        content = content.replace(frag.GUEST_MART_CTX_SHOW_OLD, frag.GUEST_MART_CTX_SHOW_NEW, 1)
    if frag.CLOUD_INGEST_MART_OLD in content:
        content = content.replace(frag.CLOUD_INGEST_MART_OLD, frag.CLOUD_INGEST_MART_NEW, 1)

    # Mart active grid row — first occurrence in renderMiniMart
    if frag.MART_CART_ROW_TABLE_OLD in content:
        content = content.replace(frag.MART_CART_ROW_TABLE_OLD, frag.MART_CART_ROW_TABLE_NEW, 1)

    # POS active grid row — in renderPOS (after mart already patched)
    pos_chunk = content.split("function renderPOS()", 1)
    if len(pos_chunk) > 1 and frag.MART_CART_ROW_TABLE_OLD in pos_chunk[1]:
        pos_chunk[1] = pos_chunk[1].replace(frag.MART_CART_ROW_TABLE_OLD, frag.MART_CART_ROW_TABLE_NEW, 1)
        content = pos_chunk[0] + "function renderPOS()" + pos_chunk[1]

    content = re.sub(r"<!-- HRMM-MART-POS-QR-ORDERS-FLOOR-v\d+ -->", f"<!-- {MARKER} -->", content)
    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — Mini-Mart + POS QR order numbers floor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
