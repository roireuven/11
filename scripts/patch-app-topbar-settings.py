#!/usr/bin/env python3
"""Add Settings shortcut icon to the top menu bar (Admin)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-TOPBAR-SETTINGS-v1"
INDEX = Path("public/index.html")

TOPBAR_BTN = """
        <button type="button" class="btn-lang" id="topbarSettingsBtn" onclick="navToPage('settings')" data-i18n-title="nav.settings" title="Settings" aria-label="Settings">
          <span class="lang-btn-ico" aria-hidden="true">&#9881;</span>
          <span data-i18n="nav.settings">Settings</span>
        </button>"""

CSS = """
    /* HRMM top bar Settings shortcut */
    #topbarSettingsBtn { flex-shrink: 0; }
    /* """ + MARKER + """ */
"""

RBAC_TAIL_OLD = """  const restNav = document.querySelector('#sidebarNav a[data-page="restaurant"]');
  if (restNav) {
    if (currentRole === 'Kitchen') restNav.innerHTML = '<span class="icon">&#127859;</span><span class="nav-txt" data-i18n="nav.kitchen">' + (i18nEn ? t('nav.kitchen') : 'Kitchen') + '</span>';
    else restNav.innerHTML = '<span class="icon">&#127860;</span><span class="nav-txt" data-i18n="nav.restaurant">' + (i18nEn ? t('nav.restaurant') : 'Restaurant') + '</span>';
  }
}"""

RBAC_TAIL_NEW = """  const restNav = document.querySelector('#sidebarNav a[data-page="restaurant"]');
  if (restNav) {
    if (currentRole === 'Kitchen') restNav.innerHTML = '<span class="icon">&#127859;</span><span class="nav-txt" data-i18n="nav.kitchen">' + (i18nEn ? t('nav.kitchen') : 'Kitchen') + '</span>';
    else restNav.innerHTML = '<span class="icon">&#127860;</span><span class="nav-txt" data-i18n="nav.restaurant">' + (i18nEn ? t('nav.restaurant') : 'Restaurant') + '</span>';
  }
  var settingsBtn = document.getElementById('topbarSettingsBtn');
  if (settingsBtn) {
    settingsBtn.style.display = (allowed === null || (Array.isArray(allowed) && allowed.indexOf('settings') >= 0)) ? '' : 'none';
  }
}"""


def patch(content: str) -> str:
    if MARKER in content and 'id="topbarSettingsBtn"' in content:
        print(f"Already patched {MARKER} — skipping")
        return content

    anchor = '        <button type="button" class="btn-lang" id="topbarDocBtn"'
    if 'id="topbarSettingsBtn"' not in content:
        if anchor not in content:
            raise SystemExit("Could not find topbarDocBtn anchor for Settings button")
        # Insert Settings button immediately before Documentation button
        content = content.replace(anchor, TOPBAR_BTN + "\n" + anchor, 1)

    if RBAC_TAIL_OLD in content and "topbarSettingsBtn" not in content.split("function applyRBAC", 1)[1][:2500]:
        content = content.replace(RBAC_TAIL_OLD, RBAC_TAIL_NEW, 1)

    if MARKER not in content:
        content = content.replace(
            "  </style>\n</head>",
            CSS + "\n  </style>\n</head>",
            1,
        )
        content = re.sub(
            r"/\* HRMM-TOPBAR-SETTINGS-v\d+ \*/",
            f"/* {MARKER} */",
            content,
        )

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
    print(f"Patched {index} — Settings icon in top menu bar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
