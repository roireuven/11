#!/usr/bin/env python3
"""Keep setup/login language in sync: shared storage + refresh when switching auth screens."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-AUTH-LOCALE-SYNC-v1"
INDEX = Path("public/index.html")

GET_LOCALE_OLD = """function getCurrentUiLocale() {
  try {
    var v = localStorage.getItem(I18N_KEY) || 'en';
    if (!isValidI18nCode(v)) return 'en';
    return v;
  } catch (e) { return 'en'; }
}"""

GET_LOCALE_NEW = """function getCurrentUiLocale() {
  try {
    var v = localStorage.getItem(I18N_KEY) || localStorage.getItem('hotel_mgr_uiLocale') || 'en';
    if (!isValidI18nCode(v)) return 'en';
    return v;
  } catch (e) { return 'en'; }
}
/** Refresh login + setup labels and language dropdowns after switching auth screens. */
window.syncAuthScreensLocale = function() {
  var lang = (typeof getCurrentUiLocale === 'function') ? getCurrentUiLocale() : 'en';
  if (typeof applyDocumentLocale === 'function') applyDocumentLocale(lang);
  if (typeof ensureLocalePicks === 'function') ensureLocalePicks();
  if (typeof applyShellI18n === 'function' && i18nData) applyShellI18n();
};"""

SET_LOCALE_OLD = """window.setAppLocale = function(lang) {
  if (!isValidI18nCode(lang)) return;
  try { localStorage.setItem(I18N_KEY, lang); } catch (e) {}
  applyDocumentLocale(lang);"""

SET_LOCALE_NEW = """window.setAppLocale = function(lang) {
  if (!isValidI18nCode(lang)) return;
  try { localStorage.setItem(I18N_KEY, lang); } catch (e) {}
  try { localStorage.setItem('hotel_mgr_uiLocale', lang); } catch (e) {}
  applyDocumentLocale(lang);"""

FINISH_LOCALE_OLD = """  applyShellI18n();
  syncLangMenuHighlight();
  var lo = document.getElementById('loginOverlay');"""

FINISH_LOCALE_NEW = """  applyShellI18n();
  syncLangMenuHighlight();
  if (typeof window.syncAuthScreensLocale === 'function') window.syncAuthScreensLocale();
  var lo = document.getElementById('loginOverlay');"""

BACK_SIGNIN_OLD = (
    "id=\"linkBackToSignIn\" onclick=\"(function(){var s=document.getElementById('setupOverlay');"
    "var l=document.getElementById('loginOverlay');if(s){s.classList.add('hidden');}"
    "if(l){l.classList.remove('hidden');}})()\""
)

BACK_SIGNIN_NEW = (
    "id=\"linkBackToSignIn\" onclick=\"(function(){var s=document.getElementById('setupOverlay');"
    "var l=document.getElementById('loginOverlay');if(s){s.classList.add('hidden');}"
    "if(l){l.classList.remove('hidden');}"
    "if(typeof window.syncAuthScreensLocale==='function'){window.syncAuthScreensLocale();}})()\""
)

# hotelCompleteSetupEarly runs before main bundle I18N_KEY — use global key only there
SETUP_NS_EARLY_OLD = """      K = 'hotel_mgr_' + ns0 + '_';
      try {
        localStorage.setItem(K + 'setupEmail', email0);"""

SETUP_NS_EARLY_NEW = """      K = 'hotel_mgr_' + ns0 + '_';
      try {
        var _locE = localStorage.getItem('hotel_mgr_uiLocale');
        if (_locE) localStorage.setItem(K + 'uiLocale', _locE);
      } catch (e) {}
      try {
        localStorage.setItem(K + 'setupEmail', email0);"""

COMPLETE_SETUP_SHOW_LOGIN_OLD = """  document.getElementById('setupOverlay').classList.add('hidden');
  document.getElementById('loginOverlay').classList.remove('hidden');
  document.getElementById('loginUsername').value = email;"""

COMPLETE_SETUP_SHOW_LOGIN_NEW = """  document.getElementById('setupOverlay').classList.add('hidden');
  document.getElementById('loginOverlay').classList.remove('hidden');
  if (typeof window.syncAuthScreensLocale === 'function') window.syncAuthScreensLocale();
  document.getElementById('loginUsername').value = email;"""


def patch(content: str) -> str:
    if MARKER in content and "syncAuthScreensLocale" in content:
        content = re.sub(r"HRMM-AUTH-LOCALE-SYNC-v\d+", MARKER, content)
        return content

    if GET_LOCALE_OLD in content:
        content = content.replace(GET_LOCALE_OLD, GET_LOCALE_NEW, 1)
    elif "syncAuthScreensLocale" not in content and "function getCurrentUiLocale" in content:
        content = content.replace(
            "var v = localStorage.getItem(I18N_KEY) || 'en';",
            "var v = localStorage.getItem(I18N_KEY) || localStorage.getItem('hotel_mgr_uiLocale') || 'en';",
            1,
        )

    if SET_LOCALE_OLD in content:
        content = content.replace(SET_LOCALE_OLD, SET_LOCALE_NEW, 1)
    elif "hotel_mgr_uiLocale', lang)" not in content and "window.setAppLocale = function" in content:
        content = content.replace(
            "  try { localStorage.setItem(I18N_KEY, lang); } catch (e) {}\n  applyDocumentLocale(lang);",
            "  try { localStorage.setItem(I18N_KEY, lang); } catch (e) {}\n  try { localStorage.setItem('hotel_mgr_uiLocale', lang); } catch (e) {}\n  applyDocumentLocale(lang);",
            1,
        )

    if "window.syncAuthScreensLocale" not in content and "function ensureLocalePicks" in content:
        content = content.replace(
            "function ensureLocalePicks() {",
            "window.syncAuthScreensLocale = function() {\n  var lang = (typeof getCurrentUiLocale === 'function') ? getCurrentUiLocale() : 'en';\n  if (typeof applyDocumentLocale === 'function') applyDocumentLocale(lang);\n  if (typeof ensureLocalePicks === 'function') ensureLocalePicks();\n  if (typeof applyShellI18n === 'function' && typeof i18nData !== 'undefined' && i18nData) applyShellI18n();\n};\nfunction ensureLocalePicks() {",
            1,
        )

    if FINISH_LOCALE_OLD in content and "syncAuthScreensLocale" not in content.split(FINISH_LOCALE_OLD, 1)[1][:120]:
        content = content.replace(FINISH_LOCALE_OLD, FINISH_LOCALE_NEW, 1)

    if BACK_SIGNIN_OLD in content:
        content = content.replace(BACK_SIGNIN_OLD, BACK_SIGNIN_NEW, 1)

    # Early setup handler (before main bundle I18N_KEY)
    if SETUP_NS_EARLY_OLD in content and "_locE = localStorage.getItem('hotel_mgr_uiLocale')" not in content:
        content = content.replace(SETUP_NS_EARLY_OLD, SETUP_NS_EARLY_NEW, 1)

    if COMPLETE_SETUP_SHOW_LOGIN_OLD in content and "syncAuthScreensLocale" not in content.split(COMPLETE_SETUP_SHOW_LOGIN_OLD, 1)[1][:200]:
        content = content.replace(COMPLETE_SETUP_SHOW_LOGIN_OLD, COMPLETE_SETUP_SHOW_LOGIN_NEW, 1)

    if f"<!-- {MARKER} -->" not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )
    else:
        content = re.sub(r"HRMM-AUTH-LOCALE-SYNC-v\d+", MARKER, content)

    return content


def main() -> int:
    path = INDEX
    if not path.is_file():
        print(f"Missing {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    path.write_text(patch(text), encoding="utf-8")
    print(f"Patched {path} — {MARKER} (setup/login locale sync)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
