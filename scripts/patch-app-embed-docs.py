#!/usr/bin/env python3
"""Embed documentation inside HotelRestaurantMini-MartManagement (public/index.html)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-DOCS-EMBED-v6"
INDEX = Path("public/index.html")

SIDEBAR_LINK = """
      <a data-page="documentation" class="hrmm-doc-nav"><span class="icon">&#128214;</span><span class="nav-txt" data-i18n="nav.documentation">Documentation</span></a>"""

SIDEBAR_HELP_BLOCK = """
      <div class="nav-section" data-i18n="nav.sectionHelp">Help</div>""" + SIDEBAR_LINK

SIDEBAR_NAV_OPEN = '    <nav class="sidebar-nav" id="sidebarNav">'

TOPBAR_BTN = """
        <button type="button" class="btn-lang" id="topbarDocBtn" onclick="navToPage('documentation')" data-i18n-title="topbar.documentationTitle" title="Documentation" aria-label="Documentation">
          <span class="lang-btn-ico" aria-hidden="true">&#128214;</span>
          <span data-i18n="topbar.documentation">Documentation</span>
        </button>"""

PAGE_DIV = '      <div class="page" id="page-documentation"></div>\n'

CSS = """
    /* HRMM embedded documentation — full in-app panel (not a separate site) */
    .doc-embed-wrap { display: flex; flex-direction: column; height: calc(100vh - 4.5rem); min-height: 420px; margin: -0.5rem -0.75rem 0; }
    .doc-embed-frame { flex: 1; width: 100%; border: none; background: var(--card-bg, #fff); min-height: 360px; }
    body.dark-mode .doc-embed-frame { background: #1a1a2e; }
    #topbarDocBtn { flex-shrink: 0; }
    .bottom-nav-item[data-bnav="documentation"] .bnav-label { max-width: 3.5rem; }
    @media (max-width: 600px) {
      .bottom-nav { height: 52px; }
      .bottom-nav-item { font-size: 0.58rem; gap: 1px; }
      .bottom-nav-item .bnav-icon { font-size: 1.05rem; }
    }
"""

RENDER_FN = """
function getDocUiLocale() {
  try {
    if (typeof getCurrentUiLocale === 'function') return getCurrentUiLocale();
    var keys = Object.keys(localStorage || {});
    for (var i = 0; i < keys.length; i++) {
      if (keys[i].indexOf('uiLocale') >= 0) {
        var v = localStorage.getItem(keys[i]);
        if (v) return v;
      }
    }
  } catch (e) {}
  return 'en';
}
function renderDocumentation() {
  var el = document.getElementById('page-documentation');
  if (!el) return;
  var loc = getDocUiLocale() || 'en';
  var src = 'doc/?lang=' + encodeURIComponent(loc) + '&embed=1#/README';
  el.innerHTML =
    '<div class="doc-embed-wrap">' +
      '<iframe class="doc-embed-frame" title="Documentation" src="' + src + '" loading="lazy"></iframe>' +
    '</div>';
}
window.openDocumentation = function() { navToPage('documentation'); };
"""

RBAC_OLD = """    'Manager': ['dashboard','rooms','bookings','guests','housekeeping','maintenance','services','invoices','reports','inventory','guestportal','restaurant','minimart','menuitems','storeitems','orderhistory'],
    'Receptionist': ['dashboard','rooms','bookings','guests','services','invoices','guestportal','restaurant','minimart','menuitems','inventory'],
    'Housekeeper': ['dashboard','housekeeping','maintenance'],
    'Restaurant': ['restaurant','menuitems','inventory'],
    'Kitchen': ['restaurant'],"""

RBAC_NEW = """    'Manager': ['dashboard','rooms','bookings','guests','housekeeping','maintenance','services','invoices','reports','inventory','guestportal','restaurant','minimart','menuitems','storeitems','orderhistory','documentation'],
    'Receptionist': ['dashboard','rooms','bookings','guests','services','invoices','guestportal','restaurant','minimart','menuitems','inventory','documentation'],
    'Housekeeper': ['dashboard','housekeeping','maintenance','documentation'],
    'Restaurant': ['restaurant','menuitems','inventory','documentation'],
    'Kitchen': ['restaurant','documentation'],"""

RENDER_MAP_OLD = "dropdowns:renderDropdowns};"
RENDER_MAP_NEW = "dropdowns:renderDropdowns,documentation:renderDocumentation};"

TITLE_FN_OLD = "function getPageTitleString(page) {"
TITLE_FN_NEW = """function getPageTitleString(page) {
  if (page === 'documentation') return (typeof t === 'function' && t('nav.documentation') !== 'nav.documentation') ? t('nav.documentation') : 'Documentation';"""

TOPBAR_ANCHOR = '        <h1 id="pageTitle">Dashboard</h1>'

DASHBOARD_NAV = '      <a class="active" data-page="dashboard"><span class="icon">&#128202;</span><span class="nav-txt" data-i18n="nav.dashboard">Dashboard</span></a>'
DASHBOARD_NAV_LOOSE = re.compile(
    r'(\s*<a[^>]*data-page="dashboard"[^>]*>.*?</a>)',
    re.DOTALL,
)

BOTTOM_NAV_OLD = """    <button class="bottom-nav-item" data-bnav="menu" onclick="toggleSidebarFromNav()"><span class="bnav-icon">&#9776;</span><span class="bnav-label" data-i18n="bnav.menu">Menu</span></button>
  `;"""

BOTTOM_NAV_NEW = """    <button class="bottom-nav-item" data-bnav="documentation" onclick="bnav('documentation')"><span class="bnav-icon">&#128214;</span><span class="bnav-label" data-i18n="bnav.documentation">Docs</span></button>
    <button class="bottom-nav-item" data-bnav="menu" onclick="toggleSidebarFromNav()"><span class="bnav-icon">&#9776;</span><span class="bnav-label" data-i18n="bnav.menu">Menu</span></button>
  `;"""

BNAV_KITCHEN_OLD = "if (currentRole === 'Kitchen' && page !== 'restaurant') {"
BNAV_KITCHEN_NEW = "if (currentRole === 'Kitchen' && page !== 'restaurant' && page !== 'documentation') {"

BNAV_ACTIVE_OLD = "const match = p === page || (p === 'pos' && page === 'minimart');"
BNAV_ACTIVE_NEW = "const match = p === page || (p === 'pos' && page === 'minimart') || (p === 'documentation' && page === 'documentation');"


def _insert_topbar_btn(content: str) -> str:
    if 'id="topbarDocBtn"' in content:
        return content
    if TOPBAR_ANCHOR not in content:
        raise SystemExit("Could not find pageTitle anchor for topbar doc button")
    return content.replace(TOPBAR_ANCHOR, TOPBAR_BTN + "\n        " + TOPBAR_ANCHOR.lstrip(), 1)


def _insert_sidebar_main(content: str) -> str:
    # Remove any previous documentation nav link
    content = re.sub(
        r'\n\s*<div class="nav-section" data-i18n="nav.sectionHelp">Help</div>\s*\n\s*<a data-page="documentation" class="hrmm-doc-nav">.*?</a>',
        "",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'\n\s*<a data-page="documentation" class="hrmm-doc-nav">.*?</a>',
        "",
        content,
        flags=re.DOTALL,
    )
    nav_block = content.split("sidebarNav", 1)[1].split("</nav>", 1)[0] if "sidebarNav" in content else ""
    if 'data-page="documentation"' in nav_block:
        return content
    if SIDEBAR_NAV_OPEN not in content:
        raise SystemExit("Could not find sidebar nav for documentation")
    return content.replace(
        SIDEBAR_NAV_OPEN,
        SIDEBAR_NAV_OPEN + SIDEBAR_HELP_BLOCK,
        1,
    )


def _insert_bottom_nav(content: str) -> str:
    if 'data-bnav="documentation" onclick' in content:
        return content
    if BOTTOM_NAV_OLD not in content:
        raise SystemExit("Could not find bottom nav menu button to patch")
    return content.replace(BOTTOM_NAV_OLD, BOTTOM_NAV_NEW, 1)


def _patch_core(content: str) -> str:
    if 'id="page-documentation"' not in content:
        content = content.replace(
            '      <div class="page" id="page-settings"></div>\n',
            '      <div class="page" id="page-settings"></div>\n' + PAGE_DIV,
            1,
        )

    if RENDER_MAP_OLD in content and "documentation:renderDocumentation" not in content:
        content = content.replace(RENDER_MAP_OLD, RENDER_MAP_NEW, 1)

    if "function renderDocumentation()" not in content:
        content = content.replace(
            "function renderPage(page) {",
            RENDER_FN + "\nfunction renderPage(page) {",
            1,
        )

    if TITLE_FN_OLD in content and "page === 'documentation'" not in content.split("function getPageTitleString", 1)[1][:250]:
        content = content.replace(TITLE_FN_OLD, TITLE_FN_NEW, 1)

    if RBAC_OLD in content:
        content = content.replace(RBAC_OLD, RBAC_NEW, 1)

    if "/* HRMM embedded documentation */" not in content:
        content = content.replace(
            "  </style>\n</head>",
            CSS + f"\n    /* {MARKER} */\n  </style>\n</head>",
            1,
        )

    if '"settings": "Settings"' in content and '"documentation": "Documentation"' not in content[:120000]:
        content = content.replace(
            '"settings": "Settings"',
            '"documentation": "Documentation",\n    "settings": "Settings"',
            1,
        )

    if '"sectionMain": "Main"' in content and '"sectionHelp"' not in content[:120000]:
        content = content.replace(
            '"sectionMain": "Main"',
            '"sectionHelp": "Help",\n    "sectionMain": "Main"',
            1,
        )

    if '"localization": "Localization"' in content:
        block = content.split('"topbar"', 1)[1][:800] if '"topbar"' in content else ""
        if '"documentationTitle"' not in block:
            content = content.replace(
                '"localization": "Localization"',
                '"localization": "Localization",\n    "documentation": "Documentation",\n    "documentationTitle": "Open help and user guide"',
                1,
            )

    if '"menu": "Menu"' in content and '"bnav"' in content:
        content = content.replace(
            '"menu": "Menu"\n  },\n  "dash":',
            '"menu": "Menu",\n    "documentation": "Docs"\n  },\n  "dash":',
            1,
        )

    if BNAV_KITCHEN_OLD in content:
        content = content.replace(BNAV_KITCHEN_OLD, BNAV_KITCHEN_NEW, 1)

    if BNAV_ACTIVE_OLD in content:
        content = content.replace(BNAV_ACTIVE_OLD, BNAV_ACTIVE_NEW, 1)

    login_anchor = 'id="btnFirstTimeSetup"'
    login_doc = (
        '<p class="hrmm-login-doc" style="text-align:center;margin:0.75rem 0 0;font-size:0.88rem;color:var(--text-muted,#64748b);" '
        'data-i18n="doc.loginHint">Help &amp; documentation available inside the app after sign-in (☰ Menu → Help).</p>\n        '
    )
    if login_anchor in content and "hrmm-login-doc" not in content:
        content = content.replace(
            '<button type="button" class="btn btn-outline" id="btnFirstTimeSetup"',
            login_doc + '<button type="button" class="btn btn-outline" id="btnFirstTimeSetup"',
            1,
        )

    return content


def patch(content: str) -> str:
    # Upgrade renderDocumentation to v6 (full in-app panel)
    old_render = re.search(
        r"function getDocUiLocale\(\)[\s\S]*?window\.openDocumentation = function\(\) \{ navToPage\('documentation'\); \};",
        content,
    )
    if old_render and "embed=1" not in old_render.group(0):
        content = content.replace(old_render.group(0), RENDER_FN.strip(), 1)
    elif "function renderDocumentation()" in content and "getDocUiLocale" not in content:
        content = content.replace(
            "function renderPage(page) {",
            RENDER_FN + "\nfunction renderPage(page) {",
            1,
        )

    if (
        MARKER in content
        and 'data-bnav="documentation" onclick' in content
        and 'id="topbarDocBtn"' in content
        and 'nav.sectionHelp' in content
        and 'embed=1' in content
    ):
        print("Already patched v6 — skipping")
        return content

    content = _patch_core(content)
    content = _insert_sidebar_main(content)
    content = _insert_topbar_btn(content)
    content = _insert_bottom_nav(content)

    if MARKER not in content:
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
    patched = patch(text)
    index.write_text(patched, encoding="utf-8")
    print(f"Patched {index} — documentation embedded inside app (Help menu, top bar, bottom nav)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
