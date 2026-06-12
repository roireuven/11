#!/usr/bin/env python3
"""Small phones: double-height top/bottom bars; overflow icons in dropdown menus."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

MARKER = "HRMM-MOBILE-DOUBLE-BARS-v1"
INDEX = Path("public/index.html")

TOPBAR_ANCHOR = '        <button class="btn-logout" id="logoutBtn" onclick="doLogout()" data-i18n="topbar.logout">Logout</button>\n      </div>\n    </div>'

BNAV_ANCHOR = """

window.bnav = function(page) {"""


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


def patch(content: str) -> str:
    frag = _load_fragments()

    if MARKER in content and "window.toggleTopbarMoreMenu" in content and "window.toggleBnavMoreMenu" in content:
        print(f"Already patched {MARKER} — skipping")
        return content

    if MARKER not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )

    if "/* HRMM mobile double bars" not in content:
        if "  </style>" in content:
            content = content.replace("  </style>", frag.DOUBLE_BARS_CSS + "  </style>", 1)
        else:
            content = content.replace("</style>", frag.DOUBLE_BARS_CSS + "</style>", 1)

    if 'id="topbarMoreBtn"' not in content:
        topbar_new = (
            '        <button class="btn-logout" id="logoutBtn" onclick="doLogout()" data-i18n="topbar.logout">Logout</button>\n'
            "      </div>\n"
            + frag.TOPBAR_MORE_HTML.strip()
            + "\n    </div>"
        )
        content = _replace(content, TOPBAR_ANCHOR, topbar_new, "topbar more menu")

    if "window.toggleTopbarMoreMenu" not in content:
        bnav_new = "\n" + frag.DOUBLE_BARS_JS.strip() + BNAV_ANCHOR
        content = _replace(content, BNAV_ANCHOR, bnav_new, "bottom nav more menu JS")

    content = re.sub(r"<!-- HRMM-MOBILE-DOUBLE-BARS-v\d+ -->", f"<!-- {MARKER} -->", content)
    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — double-height mobile bars + overflow menus")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
