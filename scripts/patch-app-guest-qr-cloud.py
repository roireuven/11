#!/usr/bin/env python3
"""Guest QR cloud sync — Firestore push from guest phones, staff ingest to local orders."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

MARKER = "HRMM-GUEST-QR-CLOUD-v1"
INDEX = Path("public/index.html")


def _load_fragments():
    frag_path = Path(__file__).resolve().parent / "_guest_qr_cloud_v13_fragments.py"
    spec = importlib.util.spec_from_file_location("_guest_qr_cloud_v13_fragments", frag_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Missing guest QR cloud fragments: {frag_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MOD = _load_fragments()


def patch(content: str) -> str:
    if MARKER in content and "guestQrCloudStartStaffSync" in content:
        return content

    if "firebase-app-compat.js" not in content:
        content = content.replace(
            '<meta charset="UTF-8">',
            '<meta charset="UTF-8">\n' + MOD.FIREBASE_SDK_SCRIPTS,
            1,
        )

    anchor = "/* HRMM guest QR restaurant order */"
    if anchor in content and "guestQrCloudStartStaffSync" not in content:
        content = content.replace(anchor, anchor + "\n" + MOD.GUEST_QR_CLOUD_JS_V13.strip(), 1)
    elif "guestQrCloudStartStaffSync" not in content:
        autologin = "/* Autologin after all data and i18n helpers are ready. Never show login on top of the first-time setup overlay. */"
        if autologin in content:
            content = content.replace(autologin, MOD.GUEST_QR_CLOUD_JS_V13.strip() + "\n\n" + autologin, 1)

    if MOD.BUILD_GUEST_ORDER_URL_PROPERTY_NS_OLD in content and "params.set('propertyNs'" not in content:
        content = content.replace(
            MOD.BUILD_GUEST_ORDER_URL_PROPERTY_NS_OLD,
            MOD.BUILD_GUEST_ORDER_URL_PROPERTY_NS_NEW,
            1,
        )

    if MOD.PARSE_GUEST_ORDER_PARAMS_PROPERTY_NS_OLD in content:
        content = content.replace(
            MOD.PARSE_GUEST_ORDER_PARAMS_PROPERTY_NS_OLD,
            MOD.PARSE_GUEST_ORDER_PARAMS_PROPERTY_NS_NEW,
            1,
        )

    content = content.replace(MOD.GUEST_CTX_PROPERTY_NS_OLD, MOD.GUEST_CTX_PROPERTY_NS_NEW)
    content = content.replace(MOD.GUEST_MART_CTX_PROPERTY_NS_OLD, MOD.GUEST_MART_CTX_PROPERTY_NS_NEW)

    if MOD.SHOW_GUEST_ORDER_CTX_OLD in content:
        content = content.replace(MOD.SHOW_GUEST_ORDER_CTX_OLD, MOD.SHOW_GUEST_ORDER_CTX_NEW, 1)

    if MOD.GUEST_REST_SUBMIT_CLOUD_TAIL_OLD in content:
        content = content.replace(MOD.GUEST_REST_SUBMIT_CLOUD_TAIL_OLD, MOD.GUEST_REST_SUBMIT_CLOUD_TAIL_NEW, 1)

    if MOD.GUEST_MART_SUBMIT_CLOUD_OLD in content:
        content = content.replace(MOD.GUEST_MART_SUBMIT_CLOUD_OLD, MOD.GUEST_MART_SUBMIT_CLOUD_NEW, 1)

    if MOD.LOGIN_SUCCESS_CLOUD_HOOK_OLD in content:
        content = content.replace(MOD.LOGIN_SUCCESS_CLOUD_HOOK_OLD, MOD.LOGIN_SUCCESS_CLOUD_HOOK_NEW, 1)

    if MOD.AUTOLOGIN_UI_CLOUD_HOOK_OLD in content:
        content = content.replace(MOD.AUTOLOGIN_UI_CLOUD_HOOK_OLD, MOD.AUTOLOGIN_UI_CLOUD_HOOK_NEW, 1)

    if MOD.GUEST_QR_OPEN_CUSTOMER_PROPERTY_NS_OLD in content:
        content = content.replace(
            MOD.GUEST_QR_OPEN_CUSTOMER_PROPERTY_NS_OLD,
            MOD.GUEST_QR_OPEN_CUSTOMER_PROPERTY_NS_NEW,
            1,
        )

    # showGuestOrderScreen from URL boot — propertyNs flows via parseGuestOrderParams

    if f"<!-- {MARKER} -->" not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )

    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    out = patch(text)
    if MARKER not in out or "guestQrCloudStartStaffSync" not in out:
        print("Guest QR cloud patch failed — missing markers", file=sys.stderr)
        return 1
    index.write_text(out, encoding="utf-8")
    print(f"Patched {index} — guest QR cloud sync (Firestore)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
