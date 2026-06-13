#!/usr/bin/env python3
"""Small phones: double-height top/bottom bars; overflow icons in dropdown menus."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

MARKER = "HRMM-MOBILE-DOUBLE-BARS-v2"
INDEX = Path("public/index.html")

TOPBAR_ANCHOR = '        <button class="btn-logout" id="logoutBtn" onclick="doLogout()" data-i18n="topbar.logout">Logout</button>\n      </div>\n    </div>'

BNAV_FN = "window.bnav = function(page) {"
BNAV_SECTION = "// ===== BOTTOM NAVIGATION BAR ====="


def _load_fragments():
    frag_path = Path(__file__).resolve().parent / "_mobile_double_bars_v1_fragments.py"
    spec = importlib.util.spec_from_file_location("_mobile_double_bars_v1_fragments", frag_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Missing fragments: {frag_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _replace(content: str, old: str, new: str, label: str) -> str:
    if old not in content:
        if new.split("\n", 1)[0] in content:
            return content
        raise SystemExit(f"Could not apply {label}")
    return content.replace(old, new, 1)


def _strip_old_css(content: str) -> str:
    return re.sub(
        r"\n\s*/\* HRMM mobile double bars[\s\S]*?/\* HRMM-MOBILE-DOUBLE-BARS-v\d+ \*/\n",
        "\n",
        content,
        count=1,
    )


def _strip_old_js(content: str) -> str:
    start = content.find("window.closeTopbarMoreMenu = function()")
    if start < 0:
        return content
    sec = content.rfind(BNAV_SECTION)
    end = content.find(BNAV_FN, sec if sec >= 0 else start)
    if end < 0:
        return content
    return content[:start] + content[end:]


def _inject_bnav_js(content: str, js: str) -> str:
    sec = content.rfind(BNAV_SECTION)
    idx = content.find(BNAV_FN, sec if sec >= 0 else 0)
    if idx < 0:
        raise SystemExit("Could not apply bottom nav more menu JS")
    if js.strip() in content:
        return content
    return content[:idx] + js.strip() + "\n\n" + content[idx:]


def _strip_old_topbar_more(content: str) -> str:
    if 'id="topbarMoreBtn"' not in content:
        return content
    content = re.sub(
        r'\n\s*<button type="button" class="btn-lang topbar-more-btn"[\s\S]*?'
        r'<div class="mobile-locale-list" id="mobileLocaleList"></div>\s*</div>',
        "",
        content,
        count=1,
    )
    if 'id="topbarMoreBtn"' in content:
        content = re.sub(
            r'\n\s*<button type="button" class="btn-lang topbar-more-btn"[\s\S]*?'
            r'</div>\s*</div>\s*\n\s*<div class="content">',
            '\n    </div>\n    <div class="content">',
            content,
            count=1,
        )
    return content


def patch(content: str) -> str:
    frag = _load_fragments()

    if MARKER in content and "window.openMobileLocalePopup" in content and "window.toggleBnavMoreMenu" in content:
        print(f"Already patched {MARKER} — skipping")
        return content

    content = re.sub(r"<!-- HRMM-MOBILE-DOUBLE-BARS-v\d+ -->", f"<!-- {MARKER} -->", content)
    if MARKER not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )

    content = _strip_old_css(content)
    content = _strip_old_js(content)
    content = _strip_old_topbar_more(content)

    if "  </style>" in content:
        content = content.replace("  </style>", frag.DOUBLE_BARS_CSS + "  </style>", 1)
    else:
        content = content.replace("</style>", frag.DOUBLE_BARS_CSS + "</style>", 1)

    topbar_new = (
        '        <button class="btn-logout" id="logoutBtn" onclick="doLogout()" data-i18n="topbar.logout">Logout</button>\n'
        "      </div>\n"
        + frag.TOPBAR_MORE_HTML.strip()
        + "\n    </div>"
    )
    content = _replace(content, TOPBAR_ANCHOR, topbar_new, "topbar more menu")

    content = _inject_bnav_js(content, frag.DOUBLE_BARS_JS)

    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — double-height mobile bars + QR visible + locale popup")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
