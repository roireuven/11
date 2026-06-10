#!/usr/bin/env python3
"""Pay QR scan orders from floor tiles, bill modals, and QR orders report."""
from __future__ import annotations

import sys
from pathlib import Path

from _qr_order_pay_v17_fragments import (
    GUEST_QR_GRID_COL_NEW,
    GUEST_QR_GRID_COL_OLD,
    GUEST_QR_SLOTS_NEW,
    GUEST_QR_SLOTS_OLD,
    MARKER,
    MART_BILL_MODAL_NEW,
    MART_BILL_MODAL_OLD,
    POS_BILL_MODAL_NEW,
    POS_BILL_MODAL_OLD,
    QR_PAY_CSS,
    QR_PAY_HELPERS,
    REST_BILL_MODAL_NEW,
    REST_BILL_MODAL_OLD,
)

INDEX = Path("public/index.html")
HELPERS_ANCHOR = "function guestQrCollectOrders(dept) {"


def _replace(content: str, old: str, new: str) -> str:
    if old not in content:
        return content
    return content.replace(old, new, 1)


def patch(content: str) -> str:
    already = MARKER in content

    if not already:
        if ".guest-qr-slot-free" in content and "guest-qr-slot-payable" not in content:
            content = content.replace(
                ".guest-qr-slot-free { color: var(--text-light); font-size: 0.58rem; }",
                ".guest-qr-slot-free { color: var(--text-light); font-size: 0.58rem; }\n"
                + QR_PAY_CSS.replace("/* __HRMM_QR_ORDER_PAY_MARKER__ */", f"/* {MARKER} */"),
                1,
            )
        elif "guest-qr-slot-payable" not in content:
            content = content.replace("</style>", QR_PAY_CSS.replace("/* __HRMM_QR_ORDER_PAY_MARKER__ */", f"/* {MARKER} */") + "</style>", 1)

    if "function guestQrSlotIsPayable" not in content and HELPERS_ANCHOR in content:
        content = content.replace(HELPERS_ANCHOR, QR_PAY_HELPERS + HELPERS_ANCHOR, 1)

    content = _replace(content, REST_BILL_MODAL_OLD, REST_BILL_MODAL_NEW)
    content = _replace(content, MART_BILL_MODAL_OLD, MART_BILL_MODAL_NEW)
    content = _replace(content, POS_BILL_MODAL_OLD, POS_BILL_MODAL_NEW)
    content = _replace(content, GUEST_QR_SLOTS_OLD, GUEST_QR_SLOTS_NEW)
    content = _replace(content, GUEST_QR_GRID_COL_OLD, GUEST_QR_GRID_COL_NEW)

    # Repair login-breaking unescaped quotes from earlier QR pay patch.
    content = content.replace(
        "restPayActiveOrdersTotal('Cash')",
        "restPayActiveOrdersTotal(\\'Cash\\')",
    )
    content = content.replace(
        "restPayActiveOrdersTotal('Credit Card')",
        "restPayActiveOrdersTotal(\\'Credit Card\\')",
    )
    content = content.replace(
        "martPayTotalBar('Cash')",
        "martPayTotalBar(\\'Cash\\')",
    )
    content = content.replace(
        "martPayTotalBar('Credit Card')",
        "martPayTotalBar(\\'Credit Card\\')",
    )
    content = content.replace(
        "guestQrPayMartOpenBill('' + idS + '','Cash')",
        "guestQrPayMartOpenBill(\\'' + idS + '\\',\\'Cash\\')",
    )
    content = content.replace(
        "guestQrPayMartOpenBill('' + idS + '','Credit Card')",
        "guestQrPayMartOpenBill(\\'' + idS + '\\',\\'Credit Card\\')",
    )

    return content


def main() -> int:
    if not INDEX.is_file():
        print(f"error: {INDEX} not found", file=sys.stderr)
        return 1
    content = INDEX.read_text(encoding="utf-8")
    patched = patch(content)
    if patched == content and MARKER not in content:
        print("warn: QR order pay patch made no changes", file=sys.stderr)
    INDEX.write_text(patched, encoding="utf-8")
    print(f"patched {INDEX} ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
