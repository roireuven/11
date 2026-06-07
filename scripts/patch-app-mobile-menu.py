#!/usr/bin/env python3
"""Shrink top bar and sidebar hamburger menu for small phone screens."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-MOBILE-MENU-v2"
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
    /* HRMM mobile hamburger menu — top bar + sidebar drawer */
    @media (max-width: 600px) {
      .topbar { padding: 0 0.35rem; height: 50px; }
      .topbar-left { gap: 0.28rem; min-width: 0; overflow: hidden; flex: 1 1 auto; }
      .topbar h1 { font-size: 0.92rem; max-width: min(42vw, 9.5rem); flex: 1 1 auto; }
      .menu-toggle { font-size: 0.9rem; min-width: 30px; min-height: 30px; padding: 0.15rem 0.32rem; border-radius: 6px; }
      .topbar .btn-back { min-width: 30px; min-height: 30px; padding: 0.15rem 0.35rem; font-size: 0.95rem; }
      .topbar .btn-lang { min-height: 30px; min-width: 30px; padding: 0.18rem 0.38rem; font-size: 0.72rem; gap: 0; }
      .topbar .btn-lang span:not(.lang-btn-ico) { display: none !important; }
      .topbar-right { gap: 0.22rem; flex-shrink: 0; min-width: 0; }
      .topbar-user > div:first-child { display: none; }
      .topbar .avatar { width: 28px; height: 28px; font-size: 0.72rem; border-width: 1px; }
      .topbar .btn-logout { padding: 0.22rem 0.42rem; font-size: 0.65rem; min-height: 30px; letter-spacing: 0; }
      .topbar .dark-toggle { width: 30px; height: 30px; min-width: 30px; padding: 0; font-size: 0.95rem; flex-shrink: 0; border: none; background: rgba(255,255,255,0.15); border-radius: 7px; color: #fff; cursor: pointer; }
      .content { height: calc(100vh - 50px); }
      .sidebar { width: min(280px, 92vw); max-width: 100vw; }
      .sidebar-header { padding: 0.85rem 0.75rem; gap: 0.5rem; align-items: flex-start; }
      .sidebar-header h2 { font-size: 0.88rem; line-height: 1.2; word-break: break-word; hyphens: auto; }
      .sidebar-header span { font-size: 0.62rem; line-height: 1.25; }
      .sidebar-header .logo { width: 34px !important; height: 34px !important; font-size: 1.15rem !important; flex-shrink: 0; }
      .sidebar-nav { padding-bottom: 4.5rem; }
      .sidebar-nav a { padding: 0.52rem 0.85rem; gap: 0.5rem; font-size: 0.78rem; }
      .sidebar-nav a .icon { font-size: 1rem; width: 22px; flex-shrink: 0; }
      .sidebar-nav a .nav-txt { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .sidebar-nav .nav-section { padding: 0.35rem 0.85rem 0.12rem; font-size: 0.6rem; margin-top: 0.35rem; }
      .bottom-nav { height: 50px; }
      .bottom-nav-item { font-size: 0.56rem; gap: 1px; padding: 0 1px; min-width: 0; }
      .bottom-nav-item .bnav-icon { font-size: 1rem; }
      .bottom-nav-item .bnav-label { max-width: 3.2rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .content { padding-bottom: 58px; }
      .toast { bottom: 58px; }
      .fab { bottom: 66px; }
    }
    @media (max-width: 380px) {
      .topbar { padding: 0 0.25rem; height: 48px; }
      .topbar h1 { font-size: 0.82rem; max-width: min(36vw, 7.5rem); }
      .menu-toggle { font-size: 0.85rem; min-width: 28px; min-height: 28px; padding: 0.12rem 0.28rem; }
      .topbar .btn-logout { padding: 0.18rem 0.32rem; font-size: 0.58rem; }
      .sidebar { width: min(260px, 94vw); }
      .sidebar-nav a { padding: 0.48rem 0.7rem; font-size: 0.74rem; }
      .bottom-nav-item { font-size: 0.52rem; }
      .bottom-nav-item .bnav-label { max-width: 2.75rem; }
    }
    @media (max-width: 340px) {
      #topbarLangMenuWrap { display: none !important; }
      #topbarDocBtn { display: none !important; }
      .topbar h1 { max-width: min(52vw, 9rem); }
      .topbar .btn-logout { padding: 0.15rem 0.28rem; font-size: 0.52rem; }
    }
    /* __HRMM_MOBILE_MARKER__ */
"""


def _mobile_css() -> str:
    return MOBILE_CSS.replace("__HRMM_MOBILE_MARKER__", MARKER)


def _strip_old_mobile_css(content: str) -> str:
    content = re.sub(
        r"\n\s*/\* HRMM mobile hamburger menu.*?\*/ HRMM-MOBILE-MENU-v\d+ \*/\n",
        "\n",
        content,
        flags=re.DOTALL,
    )
    return content


def patch(content: str) -> str:
    if MARKER in content:
        print(f"Mobile menu already patched {MARKER} — skipping")
        return content

    content = _strip_old_mobile_css(content)

    if MENU_OLD in content:
        content = content.replace(MENU_OLD, MENU_NEW, 1)
    elif "min-width: 34px; min-height: 34px;" not in content:
        raise SystemExit("Could not find .menu-toggle rule to patch")

    content = content.replace(
        "  </style>\n</head>",
        _mobile_css() + "  </style>\n</head>",
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
    print(f"Patched {index} — compact hamburger top bar and sidebar for small phones")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
