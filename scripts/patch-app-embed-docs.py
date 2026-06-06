#!/usr/bin/env python3
"""Embed combined documentation into HotelRestaurantMini-MartManagement (public/index.html)."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "HRMM-DOCS-EMBED-v2"
INDEX = Path("public/index.html")

SIDEBAR_LINK = """
      <a data-page="documentation" class="hrmm-doc-nav"><span class="icon">&#128214;</span><span class="nav-txt" data-i18n="nav.documentation">Documentation</span></a>"""

TOPBAR_BTN = """
        <button type="button" class="btn-lang" id="topbarDocBtn" onclick="navToPage('documentation')" data-i18n-title="topbar.documentationTitle" title="Documentation" aria-label="Documentation">
          <span class="lang-btn-ico" aria-hidden="true">&#128214;</span>
          <span data-i18n="topbar.documentation">Documentation</span>
        </button>"""

PAGE_DIV = '      <div class="page" id="page-documentation"></div>\n'

CSS = """
    /* HRMM embedded documentation */
    .doc-embed-wrap { display: flex; flex-direction: column; height: calc(100vh - 4.5rem); min-height: 420px; margin: -0.5rem -0.75rem 0; }
    .doc-embed-toolbar { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; padding: 0.5rem 0.75rem; background: var(--card-bg); border-bottom: 1px solid var(--border); }
    .doc-embed-toolbar a { font-size: 0.82rem; font-weight: 600; color: var(--primary); text-decoration: none; }
    .doc-embed-toolbar a:hover { text-decoration: underline; }
    .doc-embed-frame { flex: 1; width: 100%; border: none; background: #fff; min-height: 360px; }
    body.dark-mode .doc-embed-frame { background: #1a1a2e; }
    #topbarDocBtn { flex-shrink: 0; }
"""

RENDER_FN = """
function renderDocumentation() {
  var el = document.getElementById('page-documentation');
  if (!el) return;
  var docBase = 'doc/';
  var home = docBase + '#/README';
  el.innerHTML =
    '<div class="doc-embed-wrap">' +
      '<div class="doc-embed-toolbar">' +
        '<span style="font-weight:700;color:var(--text);">HotelRestaurantMini-MartManagement — Documentation</span>' +
        '<a href="' + docBase + '" target="_blank" rel="noopener">Open in new tab ↗</a>' +
      '</div>' +
      '<iframe class="doc-embed-frame" title="Documentation" src="' + home + '" loading="lazy"></iframe>' +
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

# Also patch if v1 RBAC already applied
RBAC_OLD_V1 = RBAC_NEW

RENDER_MAP_OLD = "dropdowns:renderDropdowns};"
RENDER_MAP_NEW = "dropdowns:renderDropdowns,documentation:renderDocumentation};"

TITLE_FN_OLD = "function getPageTitleString(page) {"
TITLE_FN_NEW = """function getPageTitleString(page) {
  if (page === 'documentation') return (typeof t === 'function' && t('nav.documentation') !== 'nav.documentation') ? t('nav.documentation') : 'Documentation';"""

TOPBAR_ANCHOR = '        <h1 id="pageTitle">Dashboard</h1>'


def _insert_topbar_btn(content: str) -> str:
    if 'id="topbarDocBtn"' in content:
        return content
    if TOPBAR_ANCHOR not in content:
        raise SystemExit("Could not find pageTitle anchor for topbar doc button")
    return content.replace(TOPBAR_ANCHOR, TOPBAR_BTN + "\n        " + TOPBAR_ANCHOR.lstrip(), 1)


def patch(content: str) -> str:
    fully_patched = MARKER in content and 'id="topbarDocBtn"' in content
    if fully_patched:
        print("Already patched — skipping embed")
        return content

    if MARKER not in content:
        if '<a data-page="settings">' not in content:
            raise SystemExit("Could not find settings nav anchor")

        content = content.replace(
            '<a data-page="settings">',
            SIDEBAR_LINK + '\n      <a data-page="settings">',
            1,
        )

        if 'id="page-settings"' not in content:
            raise SystemExit("Could not find page-settings div")
        content = content.replace(
            '      <div class="page" id="page-settings"></div>\n',
            '      <div class="page" id="page-settings"></div>\n' + PAGE_DIV,
            1,
        )

        if "function renderPage(page)" not in content:
            raise SystemExit("Could not find renderPage")
        if RENDER_MAP_OLD in content:
            content = content.replace(RENDER_MAP_OLD, RENDER_MAP_NEW, 1)
        if "function renderDocumentation()" not in content:
            content = content.replace(
                "function renderPage(page) {",
                RENDER_FN + "\nfunction renderPage(page) {",
                1,
            )

        if TITLE_FN_OLD in content and "page === 'documentation'" not in content.split("function getPageTitleString")[1][:200]:
            content = content.replace(TITLE_FN_OLD, TITLE_FN_NEW, 1)

        if RBAC_OLD in content:
            content = content.replace(RBAC_OLD, RBAC_NEW, 1)
        elif RBAC_OLD_V1 in content:
            pass  # already has documentation in RBAC

        if "/* HRMM embedded documentation */" not in content:
            content = content.replace(
                "  </style>\n</head>",
                CSS + f"\n    /* {MARKER} */\n  </style>\n</head>",
                1,
            )

        if '"documentation":' not in content.split('"nav"')[1][:800] if '"nav"' in content else True:
            if '"settings": "Settings"' in content:
                content = content.replace(
                    '"settings": "Settings"',
                    '"documentation": "Documentation",\n    "settings": "Settings"',
                    1,
                )

        if '"localization": "Localization"' in content and '"documentation": "Documentation"' not in content.split('"topbar"')[1][:600] if '"topbar"' in content else True:
            content = content.replace(
                '"localization": "Localization"',
                '"localization": "Localization",\n    "documentation": "Documentation",\n    "documentationTitle": "Open help and user guide"',
                1,
            )

        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )

        login_anchor = 'id="btnFirstTimeSetup"'
        login_doc = (
            '<p class="hrmm-login-doc" style="text-align:center;margin:0.75rem 0 0;">'
            '<a href="doc/" target="_blank" rel="noopener" style="font-weight:600;color:var(--primary);">'
            'Documentation ↗</a></p>\n        '
        )
        if login_anchor in content and "hrmm-login-doc" not in content:
            content = content.replace(
                '<button type="button" class="btn btn-outline" id="btnFirstTimeSetup"',
                login_doc + '<button type="button" class="btn btn-outline" id="btnFirstTimeSetup"',
                1,
            )

    content = _insert_topbar_btn(content)

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
    print(f"Patched {index} — documentation button in top bar + sidebar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
