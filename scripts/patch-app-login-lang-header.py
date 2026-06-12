#!/usr/bin/env python3
"""Prominent login/setup language dropdown (all 21 locales) + i18n for auth screens."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-LOGIN-LANG-HEADER-v1"
INDEX = Path("public/index.html")

CSS_ANCHOR = "    body.dark-mode #loginOverlay { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }"
CSS_BLOCK = """
    /* Auth screens — top language picker (21 locales) */
    .auth-language-header {
      position: sticky;
      top: 0;
      z-index: 3;
      width: 100%;
      max-width: min(460px, calc(100vw - 1.5rem));
      margin: 0 auto 0.45rem;
      display: flex;
      justify-content: flex-end;
      padding: 0 0.15rem;
      box-sizing: border-box;
      flex-shrink: 0;
    }
    [dir="rtl"] .auth-language-header { justify-content: flex-start; }
    .auth-language-header select.auth-locale-sel,
    #loginLocaleSelect.auth-locale-sel,
    #setupLocaleSelect.auth-locale-sel {
      padding: 0.55rem 0.85rem;
      font-size: 0.85rem;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,0.35);
      background: rgba(255,255,255,0.96);
      color: #1f2937;
      cursor: pointer;
      max-width: 100%;
      min-width: 0;
      min-height: 44px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    #setupOverlay .auth-language-header { max-width: min(440px, 92vw); }
    #setupOverlay {
      flex-direction: column;
      justify-content: flex-start;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
      padding: max(0.5rem, env(safe-area-inset-top, 0px)) 0.75rem max(1rem, env(safe-area-inset-bottom, 8px));
    }
    #setupOverlay .setup-card { margin: 0 auto 1rem; flex-shrink: 0; }"""

SETUP_OPEN = '  <div id="setupOverlay">'
SETUP_OPEN_NEW = """  <div id="setupOverlay">
    <div class="auth-language-header">
      <select id="setupLocaleSelect" class="form-control login-locale-sel auth-locale-sel" data-locale-select="1" data-native-select="1" data-i18n-aria-label="settings.appLanguage" aria-label="Interface language" onchange="setAppLocale(this.value)">
        <option value="en" selected>English</option>
      </select>
    </div>"""

LOGIN_OPEN = '  <div id="loginOverlay" class="hidden">'
LOGIN_OPEN_NEW = """  <div id="loginOverlay" class="hidden">
    <div class="auth-language-header">
      <select id="loginLocaleSelect" class="form-control login-locale-sel auth-locale-sel" data-locale-select="1" data-native-select="1" data-i18n-aria-label="settings.appLanguage" aria-label="Interface language" onchange="setAppLocale(this.value)">
        <option value="en" selected>English</option>
      </select>
    </div>"""

LOGIN_LANG_ROW_OLD = """      <div class="form-group" style="margin-top:0.5rem;" id="loginLangRow">
        <label for="loginLocaleSelect" data-i18n="settings.appLanguage" style="font-size:0.9rem;font-weight:700;color:var(--text);">Interface language</label>
        <select id="loginLocaleSelect" class="form-control login-locale-sel" data-locale-select="1" data-native-select="1" onchange="setAppLocale(this.value)">
          <option value="en" selected>English</option>
        </select>
        <p style="font-size:0.7rem;color:#999;margin:0.35rem 0 0;line-height:1.35;" data-i18n="settings.languageHint">Applies to labels on this screen and the app after sign in.</p>
      </div>"""

LOGIN_LANG_ROW_NEW = """      <p class="login-lang-hint" style="font-size:0.7rem;color:#999;margin:0.35rem 0 0;line-height:1.35;text-align:center;" data-i18n="settings.languageHintLogin">Applies to labels on this screen and the app after sign in.</p>"""

BACK_SIGNIN_OLD = """      <p class="login-tap-hint" style="text-align:center;margin:1rem 0 0;font-size:0.7rem;color:#6c757d;line-height:1.4;">Already have access? <button type="button" class="btn btn-sm btn-outline" style="min-height:36px;vertical-align:middle;" id="linkBackToSignIn" onclick="(function(){var s=document.getElementById('setupOverlay');var l=document.getElementById('loginOverlay');if(s){s.classList.add('hidden');}if(l){l.classList.remove('hidden');}})()">Back to sign in (demo)</button></p>"""

BACK_SIGNIN_NEW = """      <p class="login-tap-hint" style="text-align:center;margin:1rem 0 0;font-size:0.7rem;color:#6c757d;line-height:1.4;"><span data-i18n="login.alreadyHaveAccess">Already have access?</span> <button type="button" class="btn btn-sm btn-outline" style="min-height:36px;vertical-align:middle;" id="linkBackToSignIn" onclick="(function(){var s=document.getElementById('setupOverlay');var l=document.getElementById('loginOverlay');if(s){s.classList.add('hidden');}if(l){l.classList.remove('hidden');}})()"><span data-i18n="login.backToSignIn">Back to sign in (demo)</span></button></p>"""

FIRST_SETUP_OLD = """        <button type="button" class="btn btn-outline" id="btnFirstTimeSetup" style="width:100%;max-width:100%;min-height:44px;font-size:0.9rem;" onclick="(function(){try{var u=new URL(window.location.href);u.searchParams.set('newsetup','1');location.replace(u.toString());}catch(e){location.href=(location.pathname||'/')+'?newsetup=1'+(location.hash||'');}})()">Start first-time setup (email + password)</button>"""

FIRST_SETUP_NEW = """        <button type="button" class="btn btn-outline" id="btnFirstTimeSetup" style="width:100%;max-width:100%;min-height:44px;font-size:0.9rem;" onclick="(function(){try{var u=new URL(window.location.href);u.searchParams.set('newsetup','1');location.replace(u.toString());}catch(e){location.href=(location.pathname||'/')+'?newsetup=1'+(location.hash||'');}})()"><span data-i18n="login.startFirstTimeSetup">Start first-time setup (email + password)</span></button>"""

NEW_SETUP_OLD = """          <a href="?newsetup=1" id="linkFirstTimeSetup" data-newsetup="1" style="color:#1a73e8;font-weight:600;">New setup</a> (system email + password) &mdash; one browser only. You can also add <code style="font-size:0.6rem;">?newsetup=1</code> to the address bar."""

NEW_SETUP_NEW = """          <a href="?newsetup=1" id="linkFirstTimeSetup" data-newsetup="1" style="color:#1a73e8;font-weight:600;" data-i18n="login.newSetup">New setup</a> <span data-i18n="login.newSetupHint">(system email + password) — one browser only. You can also add ?newsetup=1 to the address bar.</span>"""

ENSURE_LOCALE_OLD = "  ['topbarLocaleSelect', 'loginLocaleSelect'].forEach(function(id) {"
ENSURE_LOCALE_NEW = "  ['topbarLocaleSelect', 'loginLocaleSelect', 'setupLocaleSelect'].forEach(function(id) {"

IS_LOCALE_OLD = "  if (sel.id === 'settingsLocaleSelect' || sel.id === 'topbarLocaleSelect' || sel.id === 'loginLocaleSelect' || sel.getAttribute('data-locale-select') === '1' || sel.getAttribute('data-native-select') === '1') return true;"
IS_LOCALE_NEW = "  if (sel.id === 'settingsLocaleSelect' || sel.id === 'topbarLocaleSelect' || sel.id === 'loginLocaleSelect' || sel.id === 'setupLocaleSelect' || sel.getAttribute('data-locale-select') === '1' || sel.getAttribute('data-native-select') === '1') return true;"

APPLY_SHELL_OLD = """  var tls = document.getElementById('topbarLocaleSelect');
  if (tls) { tls.setAttribute('aria-label', t('topbar.localePicker')); tls.setAttribute('title', t('topbar.localizationTitle')); }
  ensureLocalePicks();"""

APPLY_SHELL_NEW = """  var tls = document.getElementById('topbarLocaleSelect');
  if (tls) { tls.setAttribute('aria-label', t('topbar.localePicker')); tls.setAttribute('title', t('topbar.localizationTitle')); }
  ['loginLocaleSelect', 'setupLocaleSelect'].forEach(function(id) {
    var als = document.getElementById(id);
    if (als) { als.setAttribute('aria-label', t('settings.appLanguage')); als.setAttribute('title', t('topbar.localizationTitle')); }
  });
  ensureLocalePicks();"""


def patch(content: str) -> str:
    if MARKER in content and "auth-language-header" in content and "setupLocaleSelect" in content:
        content = re.sub(r"HRMM-LOGIN-LANG-HEADER-v\d+", MARKER, content)
        return content

    if CSS_ANCHOR in content and ".auth-language-header" not in content:
        content = content.replace(CSS_ANCHOR, CSS_ANCHOR + CSS_BLOCK, 1)

    if SETUP_OPEN in content and 'id="setupLocaleSelect"' not in content:
        content = content.replace(SETUP_OPEN, SETUP_OPEN_NEW, 1)

    if LOGIN_OPEN in content and content.count('id="loginLocaleSelect"') < 2:
        # Only patch if select is still inside card (not yet in header)
        if LOGIN_LANG_ROW_OLD.split("loginLocaleSelect")[0] in content:
            content = content.replace(LOGIN_OPEN, LOGIN_OPEN_NEW, 1)
            content = content.replace(LOGIN_LANG_ROW_OLD, LOGIN_LANG_ROW_NEW, 1)
        elif 'class="auth-language-header"' not in content.split(LOGIN_OPEN, 1)[1].split("login-card", 1)[0]:
            content = content.replace(LOGIN_OPEN, LOGIN_OPEN_NEW, 1)

    if BACK_SIGNIN_OLD in content:
        content = content.replace(BACK_SIGNIN_OLD, BACK_SIGNIN_NEW, 1)
    if FIRST_SETUP_OLD in content:
        content = content.replace(FIRST_SETUP_OLD, FIRST_SETUP_NEW, 1)
    if NEW_SETUP_OLD in content:
        content = content.replace(NEW_SETUP_OLD, NEW_SETUP_NEW, 1)

    if ENSURE_LOCALE_OLD in content:
        content = content.replace(ENSURE_LOCALE_OLD, ENSURE_LOCALE_NEW, 1)

    if IS_LOCALE_OLD in content and "setupLocaleSelect" not in content.split(IS_LOCALE_OLD, 1)[0][-200:] + IS_LOCALE_OLD:
        content = content.replace(IS_LOCALE_OLD, IS_LOCALE_NEW, 1)

    if APPLY_SHELL_OLD in content:
        content = content.replace(APPLY_SHELL_OLD, APPLY_SHELL_NEW, 1)

    if f"<!-- {MARKER} -->" not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )
    else:
        content = re.sub(r"HRMM-LOGIN-LANG-HEADER-v\d+", MARKER, content)

    return content


def main() -> int:
    path = INDEX
    if not path.is_file():
        print(f"Missing {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    out = patch(text)
    path.write_text(out, encoding="utf-8")
    print(f"Patched {path} — {MARKER} (auth language dropdown, 21 locales)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
