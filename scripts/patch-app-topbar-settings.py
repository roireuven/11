#!/usr/bin/env python3
"""Add Settings shortcut to top bar and bottom navigation (Admin)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-TOPBAR-SETTINGS-v3"
INDEX = Path("public/index.html")

TOPBAR_BTN = """
        <button type="button" class="btn-lang" id="topbarSettingsBtn" onclick="navToPage('settings')" data-i18n-title="nav.settings" title="Settings" aria-label="Settings">
          <span class="lang-btn-ico" aria-hidden="true">&#9881;</span>
          <span data-i18n="nav.settings">Settings</span>
        </button>"""

CSS = """
    /* HRMM Settings shortcuts — top bar + bottom nav */
    #topbarSettingsBtn { flex-shrink: 0; }
    .bottom-nav-item[data-bnav="settings"] .bnav-label { max-width: 3.5rem; }
    /* __HRMM_SETTINGS_MARKER__ */
"""

BOTTOM_NAV_MENU_BTN = """    <button class="bottom-nav-item" data-bnav="menu" onclick="toggleSidebarFromNav()"><span class="bnav-icon">&#9776;</span><span class="bnav-label" data-i18n="bnav.menu">Menu</span></button>
  `;"""

BOTTOM_NAV_WITH_SETTINGS = """    <button class="bottom-nav-item" data-bnav="settings" onclick="bnav('settings')"><span class="bnav-icon">&#9881;</span><span class="bnav-label" data-i18n="nav.settings">Settings</span></button>
    <button class="bottom-nav-item" data-bnav="menu" onclick="toggleSidebarFromNav()"><span class="bnav-icon">&#9776;</span><span class="bnav-label" data-i18n="bnav.menu">Menu</span></button>
  `;"""

BNAV_ACTIVE_OLD = "const match = p === page || (p === 'pos' && (page === 'minimart' || page === 'pos')) || (p === 'documentation' && page === 'documentation');"
BNAV_ACTIVE_NEW = "const match = p === page || (p === 'pos' && (page === 'minimart' || page === 'pos')) || (p === 'documentation' && page === 'documentation') || (p === 'settings' && page === 'settings');"

RBAC_REST_NAV = """  const restNav = document.querySelector('#sidebarNav a[data-page="restaurant"]');
  if (restNav) {
    if (currentRole === 'Kitchen') restNav.innerHTML = '<span class="icon">&#127859;</span><span class="nav-txt" data-i18n="nav.kitchen">' + (i18nEn ? t('nav.kitchen') : 'Kitchen') + '</span>';
    else restNav.innerHTML = '<span class="icon">&#127860;</span><span class="nav-txt" data-i18n="nav.restaurant">' + (i18nEn ? t('nav.restaurant') : 'Restaurant') + '</span>';
  }
"""

RBAC_TAIL_OLD = RBAC_REST_NAV + "}"

RBAC_TAIL_WITH_TOPBAR = RBAC_REST_NAV + """  var settingsBtn = document.getElementById('topbarSettingsBtn');
  if (settingsBtn) {
    settingsBtn.style.display = (allowed === null || (Array.isArray(allowed) && allowed.indexOf('settings') >= 0)) ? '' : 'none';
  }
}"""

RBAC_SETTINGS_TAIL = """  var canSettings = allowed === null || (Array.isArray(allowed) && allowed.indexOf('settings') >= 0);
  var settingsBtn = document.getElementById('topbarSettingsBtn');
  if (settingsBtn) {
    settingsBtn.style.display = canSettings ? '' : 'none';
  }
  var bnavSettings = document.querySelector('#bottomNav [data-bnav="settings"]');
  if (bnavSettings) {
    bnavSettings.style.display = canSettings ? '' : 'none';
  }
}"""

RBAC_TAIL_FULL = RBAC_REST_NAV + RBAC_SETTINGS_TAIL

# v2 bug: bnavSettings block was appended after applyRBAC's closing brace (breaks login JS)
RBAC_BROKEN_V2 = RBAC_SETTINGS_TAIL.replace(
    "  var bnavSettings = document.querySelector('#bottomNav [data-bnav=\"settings\"]');",
    "}\n  var bnavSettings = document.querySelector('#bottomNav [data-bnav=\"settings\"]');",
    1,
)


def _rbac_is_broken(content: str) -> bool:
    return RBAC_BROKEN_V2 in content or "}\n  var bnavSettings = document.querySelector('#bottomNav [data-bnav=\"settings\"]');" in content


def _fix_rbac_tail(content: str) -> str:
    if RBAC_BROKEN_V2 in content:
        return content.replace(RBAC_BROKEN_V2, RBAC_SETTINGS_TAIL, 1)
    if RBAC_TAIL_WITH_TOPBAR in content:
        return content.replace(RBAC_TAIL_WITH_TOPBAR, RBAC_TAIL_FULL, 1)
    if RBAC_TAIL_OLD in content:
        return content.replace(RBAC_TAIL_OLD, RBAC_TAIL_FULL, 1)
    return content


def _css_block() -> str:
    return CSS.replace("__HRMM_SETTINGS_MARKER__", MARKER)


def _strip_old_settings_css(content: str) -> str:
    content = re.sub(
        r"\n\s*/\* HRMM (?:Settings shortcuts — top bar \+ bottom nav|top bar Settings shortcut) \*/\n"
        r".*?\n\s*/\* HRMM-TOPBAR-SETTINGS-v\d+ \*/\n",
        "\n",
        content,
        flags=re.DOTALL,
    )
    return content


def _is_fully_patched(content: str) -> bool:
    if _rbac_is_broken(content):
        return False
    return (
        MARKER in content
        and 'data-bnav="settings"' in content
        and RBAC_SETTINGS_TAIL in content
        and f"/* {MARKER} */" in content
    )


def patch(content: str) -> str:
    if _is_fully_patched(content):
        print(f"Already patched {MARKER} — skipping")
        return content

    anchor = '        <button type="button" class="btn-lang" id="topbarDocBtn"'
    if 'id="topbarSettingsBtn"' not in content:
        if anchor not in content:
            raise SystemExit("Could not find topbarDocBtn anchor for Settings button")
        content = content.replace(anchor, TOPBAR_BTN + "\n" + anchor, 1)

    if BOTTOM_NAV_MENU_BTN in content and 'data-bnav="settings"' not in content:
        content = content.replace(BOTTOM_NAV_MENU_BTN, BOTTOM_NAV_WITH_SETTINGS, 1)

    if BNAV_ACTIVE_OLD in content:
        content = content.replace(BNAV_ACTIVE_OLD, BNAV_ACTIVE_NEW, 1)
    elif BNAV_ACTIVE_NEW not in content and "p === 'settings'" not in content:
        content = content.replace(BNAV_ACTIVE_OLD, BNAV_ACTIVE_NEW, 1)

    content = _fix_rbac_tail(content)

    content = _strip_old_settings_css(content)
    if f"/* {MARKER} */" not in content:
        content = content.replace(
            "  </style>\n</head>",
            _css_block() + "\n  </style>\n</head>",
            1,
        )
    content = re.sub(r"<!-- HRMM-TOPBAR-SETTINGS-v\d+ -->", f"<!-- {MARKER} -->", content)

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
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — Settings icon in top bar and bottom nav")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
