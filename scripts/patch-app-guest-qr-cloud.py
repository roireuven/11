#!/usr/bin/env python3
"""Guest QR cloud sync — Firestore push from guest phones, staff ingest to local orders."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

MARKER = "HRMM-GUEST-QR-CLOUD-v1"
INDEX = Path("public/index.html")
CLOUD_BLOCK_START = "/* HRMM guest QR cloud sync v13 */"
CLOUD_BLOCK_END = "window.guestQrCloudPullPendingOnce = guestQrCloudPullPendingOnce;"
AUTOLOGIN_ANCHOR = (
    "/* Autologin after all data and i18n helpers are ready. "
    "Never show login on top of the first-time setup overlay. */"
)

CLOUD_BLOCK_RE = re.compile(
    r"/\* HRMM guest QR cloud sync v13 \*/\s*.*?window\.guestQrCloudPullPendingOnce = guestQrCloudPullPendingOnce;",
    re.DOTALL,
)


def _load_fragments():
    cloud_path = Path(__file__).resolve().parent / "_guest_qr_cloud_v13_fragments.py"
    menu_path = Path(__file__).resolve().parent / "_guest_qr_guest_menu_v14_fragments.py"
    for path in (cloud_path, menu_path):
        if not path.is_file():
            raise SystemExit(f"Missing fragments: {path}")
    spec_c = importlib.util.spec_from_file_location("_guest_qr_cloud_v13_fragments", cloud_path)
    spec_m = importlib.util.spec_from_file_location("_guest_qr_guest_menu_v14_fragments", menu_path)
    if spec_c is None or spec_c.loader is None or spec_m is None or spec_m.loader is None:
        raise SystemExit("Failed to load guest QR cloud fragments")
    mod_c = importlib.util.module_from_spec(spec_c)
    mod_m = importlib.util.module_from_spec(spec_m)
    spec_c.loader.exec_module(mod_c)
    spec_m.loader.exec_module(mod_m)
    return mod_c, mod_m


MOD, MENU = _load_fragments()


def _cloud_js_inside_style(content: str) -> bool:
    pos = content.find(CLOUD_BLOCK_START)
    if pos < 0:
        return False
    style_end = content.find("</style>")
    return style_end >= 0 and pos < style_end


def _cloud_js_in_script(content: str) -> bool:
    pos = content.find(CLOUD_BLOCK_START)
    if pos < 0:
        return False
    style_end = content.find("</style>")
    return style_end >= 0 and pos > style_end


def _repair_cloud_js_placement(content: str) -> str:
    """Move cloud JS out of <style> if a prior patch injected it there."""
    if not _cloud_js_inside_style(content):
        return content
    match = CLOUD_BLOCK_RE.search(content)
    if not match:
        return content
    cloud_js = match.group(0).strip()
    content = CLOUD_BLOCK_RE.sub("", content, count=1)
    if cloud_js not in content and AUTOLOGIN_ANCHOR in content:
        content = content.replace(AUTOLOGIN_ANCHOR, cloud_js + "\n\n" + AUTOLOGIN_ANCHOR, 1)
    return content


def _ensure_cloud_js_script(content: str) -> str:
    if _cloud_js_in_script(content):
        return content
    if AUTOLOGIN_ANCHOR not in content:
        return content
    return content.replace(
        AUTOLOGIN_ANCHOR,
        MOD.GUEST_QR_CLOUD_JS_V13.strip() + "\n\n" + AUTOLOGIN_ANCHOR,
        1,
    )


def _apply_menu_fixes(content: str) -> str:
    if MENU.ENSURE_GUEST_MENU_LOAD_OLD in content:
        content = content.replace(MENU.ENSURE_GUEST_MENU_LOAD_OLD, MENU.ENSURE_GUEST_MENU_LOAD_NEW, 1)
    if MENU.GUEST_REST_CATEGORIES_OLD in content:
        content = content.replace(MENU.GUEST_REST_CATEGORIES_OLD, MENU.GUEST_REST_CATEGORIES_NEW, 1)
    if MENU.GUEST_REST_FILTER_OLD in content:
        content = content.replace(MENU.GUEST_REST_FILTER_OLD, MENU.GUEST_REST_FILTER_NEW, 1)
    if MENU.GUEST_REST_CSS_SCROLL_OLD in content and "guest-rest-layout .guest-rest-panel:first-child" not in content:
        content = content.replace(MENU.GUEST_REST_CSS_SCROLL_OLD, MENU.GUEST_REST_CSS_SCROLL_NEW, 1)
    return content


def patch(content: str) -> str:
    content = _repair_cloud_js_placement(content)

    if "firebase-app-compat.js" not in content:
        content = content.replace(
            '<meta charset="UTF-8">',
            '<meta charset="UTF-8">\n' + MOD.FIREBASE_SDK_SCRIPTS,
            1,
        )

    content = _ensure_cloud_js_script(content)

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

    content = _apply_menu_fixes(content)

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
    if _cloud_js_inside_style(out):
        print("Guest QR cloud patch failed — JS still inside <style>", file=sys.stderr)
        return 1
    if "guestRestGetMenuCategories" not in out:
        print("Guest QR menu patch failed — missing guestRestGetMenuCategories", file=sys.stderr)
        return 1
    index.write_text(out, encoding="utf-8")
    print(f"Patched {index} — guest QR cloud sync + guest menu fullscreen fix")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
