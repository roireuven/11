#!/usr/bin/env python3
"""Wire setup screen hardcoded strings to i18n (all 21 locales via locale JSON)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-SETUP-I18N-v1"
INDEX = Path("public/index.html")

BANNER_OLD = """      <div style="margin:0.6rem auto 0.2rem;max-width:520px;padding:0.6rem 0.75rem;border-radius:12px;background:rgba(26,115,232,0.12);border:1px solid rgba(26,115,232,0.35);color:#0a2a4a;font-weight:700;font-size:0.85rem;line-height:1.35;text-align:center;">
        Setup not done yet — please create your system email and password below.
      </div>"""

BANNER_NEW = """      <div style="margin:0.6rem auto 0.2rem;max-width:520px;padding:0.6rem 0.75rem;border-radius:12px;background:rgba(26,115,232,0.12);border:1px solid rgba(26,115,232,0.35);color:#0a2a4a;font-weight:700;font-size:0.85rem;line-height:1.35;text-align:center;" data-i18n="setup.notDoneBanner">
        Setup not done yet — please create your system email and password below.
      </div>"""

SETUP_SUBTITLE_ANCHOR = '      <div class="setup-ver" data-i18n="setup.version">v2.0 — First-Time Setup</div>'
SETUP_SUBTITLE_NEW = """      <div class="setup-ver" data-i18n="setup.version">v2.0 — First-Time Setup</div>
      <p class="setup-subtitle" data-i18n="setup.subtitle" style="color:#6b7280;font-size:0.88rem;margin:0.15rem 0 0.6rem;line-height:1.4;text-align:center;">Configure your business settings to start</p>"""

BTN_SETUP_OLD = 'id="btnCompleteSetup" aria-label="Create account and get started"'
BTN_SETUP_NEW = 'id="btnCompleteSetup" data-i18n-aria-label="setup.createBtnAria" aria-label="Create account and get started"'

EARLY_REPLACEMENTS = [
    (
        "if (!e0 || !p0) { if (err0) err0.textContent = 'Form not ready. Refresh the page (Ctrl+F5).'; return; }",
        "if (!e0 || !p0) { if (err0) err0.textContent = (typeof t === 'function' ? t('setup.formNotReady') : 'Form not ready. Refresh the page (Ctrl+F5).'); return; }",
    ),
    (
        "if (!email0 || email0.indexOf('@') < 0) { if (err0) err0.textContent = 'Please enter a valid email address'; return; }",
        "if (!email0 || email0.indexOf('@') < 0) { if (err0) err0.textContent = (typeof t === 'function' ? t('setup.invalidEmail') : 'Please enter a valid email address'); return; }",
    ),
    (
        "if (!pass0 || pass0.length < 4) { if (err0) err0.textContent = 'Password must be at least 4 characters'; return; }",
        "if (!pass0 || pass0.length < 4) { if (err0) err0.textContent = (typeof t === 'function' ? t('setup.passwordMin') : 'Password must be at least 4 characters'); return; }",
    ),
    (
        "if (err0) err0.textContent = 'Storage blocked. Allow site data (cookies) for this site, then try again.';",
        "if (err0) err0.textContent = (typeof t === 'function' ? t('setup.storageBlockedSetup') : 'Storage blocked. Allow site data (cookies) for this site, then try again.');",
    ),
    (
        "if (err0) err0.textContent = 'Could not save. Try again, or go Back to sign in and use a demo user.';",
        "if (err0) err0.textContent = (typeof t === 'function' ? t('setup.saveFailedSetup') : 'Could not save. Try again, or go Back to sign in and use a demo user.');",
    ),
]

MAIN_REPLACEMENTS = [
    (
        "if (err) err.textContent = 'Please enter a valid email address';",
        "if (err) err.textContent = (typeof t === 'function' ? t('setup.invalidEmail') : 'Please enter a valid email address');",
    ),
    (
        "if (err) err.textContent = 'Password must be at least 4 characters';",
        "if (err) err.textContent = (typeof t === 'function' ? t('setup.passwordMin') : 'Password must be at least 4 characters');",
    ),
    (
        "if (err) err.textContent = (ex && ex.message) ? String(ex.message) : 'Could not complete setup. Try again.';",
        "if (err) err.textContent = (ex && ex.message) ? String(ex.message) : (typeof t === 'function' ? t('setup.setupFailed') : 'Could not complete setup. Try again.');",
    ),
]


def patch(content: str) -> str:
    if MARKER in content and 'data-i18n="setup.notDoneBanner"' in content:
        content = re.sub(r"HRMM-SETUP-I18N-v\d+", MARKER, content)
        return content

    if SETUP_SUBTITLE_ANCHOR in content and 'class="setup-subtitle"' not in content:
        content = content.replace(SETUP_SUBTITLE_ANCHOR, SETUP_SUBTITLE_NEW, 1)

    if BANNER_OLD in content:
        content = content.replace(BANNER_OLD, BANNER_NEW, 1)

    if BTN_SETUP_OLD in content and "data-i18n-aria-label=\"setup.createBtnAria\"" not in content:
        content = content.replace(BTN_SETUP_OLD, BTN_SETUP_NEW, 1)

    for old, new in EARLY_REPLACEMENTS + MAIN_REPLACEMENTS:
        if old in content and new not in content:
            content = content.replace(old, new, 1)

    if f"<!-- {MARKER} -->" not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )
    else:
        content = re.sub(r"HRMM-SETUP-I18N-v\d+", MARKER, content)

    return content


def main() -> int:
    path = INDEX
    if not path.is_file():
        print(f"Missing {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    path.write_text(patch(text), encoding="utf-8")
    print(f"Patched {path} — {MARKER} (setup screen i18n wiring)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
