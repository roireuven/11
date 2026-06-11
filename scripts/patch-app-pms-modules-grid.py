#!/usr/bin/env python3
"""Dashboard PMS quick-action module grid wired to pms.* i18n (21 locales)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-PMS-MODULES-GRID-v2"
INDEX = Path("public/index.html")

CSS_ANCHOR = "    .setup-card .setup-welcome strong { color: #1a73e8; }"
CSS_NEW = """    .setup-card .setup-welcome strong { color: #1a73e8; }
    .pms-modules-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(10.5rem, 1fr));
      gap: 0.55rem;
    }
    .pms-mod-btn {
      width: 100%;
      text-align: center;
      white-space: normal;
      line-height: 1.25;
      min-height: 2.6rem;
      padding: 0.55rem 0.45rem;
      font-size: 0.82rem;
    }
    @media (max-width: 480px) {
      .pms-modules-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .pms-mod-btn { font-size: 0.76rem; min-height: 2.45rem; }
    }"""

DASH_ANCHOR = "    bodyHtml += wpBar;"
DASH_INSERT = """    bodyHtml += '<div class="card pms-modules-card" style="margin-bottom:0.85rem;"><div class="card-header" style="flex-direction:column;align-items:flex-start;"><h2 data-i18n="pms.sysTitle">' + t('pms.sysTitle') + '</h2></div><div class="card-body"><div class="pms-modules-grid">' +
      '<button type="button" class="btn btn-primary pms-mod-btn" onclick="if(window.showAddRoom)showAddRoom()">+ ' + t('pms.btnAddRoom') + '</button>' +
      '<button type="button" class="btn btn-primary pms-mod-btn" onclick="if(window.showAddBooking)showAddBooking()">+ ' + t('pms.btnAddBk') + '</button>' +
      '<button type="button" class="btn btn-primary pms-mod-btn" onclick="if(window.showAddGuest)showAddGuest()">+ ' + t('pms.btnAddGst') + '</button>' +
      '<button type="button" class="btn btn-primary pms-mod-btn" onclick="if(window.showAddTicket)showAddTicket()">+ ' + t('pms.btnAddTask') + '</button>' +
      '<button type="button" class="btn btn-primary pms-mod-btn" onclick="if(window.showAddService)showAddService()">+ ' + t('pms.btnAddSvc') + '</button>' +
      '<button type="button" class="btn btn-primary pms-mod-btn" onclick="if(window.showAddInvoice)showAddInvoice()">+ ' + t('pms.btnAddInv') + '</button>' +
      '<button type="button" class="btn btn-primary pms-mod-btn" onclick="if(window.showAddInventory)showAddInventory()">+ ' + t('pms.btnAddStk') + '</button>' +
      '<button type="button" class="btn btn-primary pms-mod-btn" onclick="if(window.showAddMenuItem)showAddMenuItem()">+ ' + t('pms.btnAddMenu') + '</button>' +
      '<button type="button" class="btn btn-primary pms-mod-btn" onclick="if(window.showAddStoreItem)showAddStoreItem()">+ ' + t('pms.btnAddShop') + '</button>' +
      '<button type="button" class="btn btn-primary pms-mod-btn" onclick="if(window.showAddAccount)showAddAccount()">+ ' + t('pms.btnAddUsr') + '</button>' +
      '</div></div></div>';
    bodyHtml += wpBar;"""


REMOVALS = [
    "'<button type=\"button\" class=\"btn btn-primary pms-mod-btn\" onclick=\"showPage(\\'housekeeping\\')\">+ ' + t('pms.btnAddCln') + '</button>' +\n      ",
    "'<button type=\"button\" class=\"btn btn-primary pms-mod-btn\" onclick=\"showPage(\\'alltransactions\\')\">+ ' + t('pms.btnAddTx') + '</button>' +\n      ",
]


def patch(content: str) -> str:
    changed = False
    for old in REMOVALS:
        if old in content:
            content = content.replace(old, "", 1)
            changed = True

    if MARKER in content and "pms-modules-grid" in content:
        content = re.sub(r"HRMM-PMS-MODULES-GRID-v\d+", MARKER, content)
        if changed:
            print("Removed cleaning/transaction buttons from PMS dashboard grid")
        return content

    if CSS_ANCHOR in content and ".pms-modules-grid" not in content:
        content = content.replace(CSS_ANCHOR, CSS_NEW, 1)

    if DASH_ANCHOR in content and "pms-modules-card" not in content:
        content = content.replace(DASH_ANCHOR, DASH_INSERT, 1)

    if MARKER not in content:
        content = content.replace("</head>", f"  <!-- {MARKER} -->\n</head>", 1)

    return content


def main() -> int:
    if not INDEX.is_file():
        print(f"Missing {INDEX}", file=sys.stderr)
        return 1
    text = INDEX.read_text(encoding="utf-8")
    patched = patch(text)
    if patched == text:
        print("No PMS modules grid changes applied.")
        return 0
    INDEX.write_text(patched, encoding="utf-8")
    print(f"Patched {INDEX} ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
