#!/usr/bin/env python3
"""Shrink the top-bar hamburger menu so the header fits phone screens."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "HRMM-MOBILE-MENU-v1"
INDEX = Path("public/index.html")

MENU_OLD = (
    ".menu-toggle { display: block; background: rgba(255,255,255,0.15); border: none; "
    "font-size: 1.3rem; cursor: pointer; padding: 0.4rem 0.6rem; border-radius: 8px; "
    "color: #fff; flex-shrink: 0; }"
)

MENU_NEW = (
    ".menu-toggle { display: flex; align-items: center; justify-content: center; "
    "background: rgba(255,255,255,0.15); border: none; font-size: 1.05rem; line-height: 1; "
    "cursor: pointer; padding: 0.28rem 0.42rem; border-radius: 7px; color: #fff; "
    "flex-shrink: 0; min-width: 34px; min-height: 34px; }"
)

MOBILE_CSS = """
    /* HRMM mobile hamburger menu */
    @media (max-width: 600px) {
      .topbar { padding: 0 0.5rem; }
      .topbar-left { gap: 0.4rem; }
      .topbar h1 { font-size: 1rem; }
      .menu-toggle { font-size: 0.9rem; min-width: 30px; min-height: 30px; padding: 0.15rem 0.32rem; border-radius: 6px; }
    }
    @media (max-width: 380px) {
      .menu-toggle { font-size: 0.85rem; min-width: 28px; min-height: 28px; padding: 0.12rem 0.28rem; }
    }
    /* HRMM-MOBILE-MENU-v1 */
"""


def patch(content: str) -> str:
    if MARKER in content:
        print("Mobile menu already patched — skipping")
        return content

    if MENU_OLD in content:
        content = content.replace(MENU_OLD, MENU_NEW, 1)
    elif "min-width: 34px; min-height: 34px;" not in content:
        raise SystemExit("Could not find .menu-toggle rule to patch")

    content = content.replace(
        "  </style>\n</head>",
        MOBILE_CSS + "  </style>\n</head>",
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
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — smaller hamburger menu for phones")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
