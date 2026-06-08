#!/usr/bin/env python3
"""Mobile phone UI: hamburger sidebar, localization, bottom nav, touch targets."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-MOBILE-MENU-v4"
INDEX = Path("public/index.html")

MENU_OLD = (
    ".menu-toggle { display: block; background: rgba(255,255,255,0.15); border: none; "
    "font-size: 1.3rem; cursor: pointer; padding: 0.4rem 0.6rem; border-radius: 8px; "
    "color: #fff; flex-shrink: 0; }"
)

MENU_NEW = (
    ".menu-toggle { display: flex; align-items: center; justify-content: center; "
    "background: rgba(255,255,255,0.15); border: none; font-size: 0.95rem; line-height: 1; "
    "cursor: pointer; padding: 0.25rem 0.4rem; border-radius: 7px; color: #fff; "
    "flex-shrink: 0; min-width: 44px; min-height: 44px; touch-action: manipulation; "
    "-webkit-tap-highlight-color: transparent; }"
)

LANG_WRAP_Z_OLD = ".lang-menu-wrap { position: relative; z-index: 1; flex-shrink: 0; }"
LANG_WRAP_Z_NEW = (
    ".lang-menu-wrap { position: relative; z-index: 1; flex-shrink: 0; }\n"
    "    .topbar .topbar-locale-wrap { z-index: 320; }"
)

MOBILE_CSS = """
    /* HRMM mobile hamburger menu — phones: sidebar, locale, bottom nav */
    @media (max-width: 600px) {
      .topbar { padding: 0 0.35rem; height: 50px; padding-top: env(safe-area-inset-top, 0px); }
      .topbar-left { gap: 0.25rem; min-width: 0; overflow: visible; flex: 0 1 auto; }
      .topbar h1 { display: none; }
      #topbarSettingsBtn, #topbarDocBtn { display: none !important; }
      .menu-toggle { font-size: 0.88rem; min-width: 44px; min-height: 44px; padding: 0.2rem 0.38rem; border-radius: 6px; }
      .topbar .btn-back { min-width: 44px; min-height: 44px; padding: 0.15rem 0.35rem; font-size: 0.95rem; }
      .topbar .btn-lang { min-height: 44px; min-width: 44px; padding: 0.2rem 0.42rem; font-size: 0.72rem; gap: 0; touch-action: manipulation; }
      .topbar .btn-lang span:not(.lang-btn-ico) { display: none !important; }
      .topbar-right { gap: 0.22rem; flex-shrink: 0; min-width: 0; }
      .topbar-user > div:first-child { display: none; }
      .topbar .avatar { width: 30px; height: 30px; font-size: 0.72rem; border-width: 1px; }
      .topbar .btn-logout { padding: 0.22rem 0.42rem; font-size: 0.65rem; min-height: 44px; min-width: 44px; letter-spacing: 0; touch-action: manipulation; }
      .topbar .dark-toggle { width: 44px; height: 44px; min-width: 44px; padding: 0; font-size: 0.95rem; flex-shrink: 0; border: none; background: rgba(255,255,255,0.15); border-radius: 7px; color: #fff; cursor: pointer; touch-action: manipulation; }
      .topbar .topbar-locale-wrap .lang-menu.open {
        position: fixed;
        left: max(0.5rem, env(safe-area-inset-left, 0px));
        right: max(0.5rem, env(safe-area-inset-right, 0px));
        top: calc(50px + env(safe-area-inset-top, 0px));
        width: auto;
        min-width: 0;
        max-height: min(62vh, 380px);
        margin-top: 0;
        z-index: 10050;
        box-shadow: 0 12px 32px rgba(0,0,0,0.28);
        -webkit-overflow-scrolling: touch;
      }
      .lang-menu-backdrop {
        display: none;
        position: fixed;
        inset: 0;
        z-index: 10040;
        background: rgba(0,0,0,0.35);
        -webkit-tap-highlight-color: transparent;
      }
      .lang-menu-backdrop.open { display: block; }
      .lang-menu .lang-opt { min-height: 44px; padding: 0.65rem 0.75rem; touch-action: manipulation; }
      .content { height: calc(100dvh - 50px - env(safe-area-inset-top, 0px)); }
      .sidebar {
        width: min(272px, 90vw);
        max-width: 100vw;
        -webkit-overflow-scrolling: touch;
        overscroll-behavior: contain;
        padding-bottom: calc(3.75rem + env(safe-area-inset-bottom, 0px));
      }
      .sidebar.open { z-index: 220; }
      .sidebar-overlay.open { z-index: 215; }
      .sidebar-header { padding: 0.7rem 0.65rem; gap: 0.4rem; align-items: flex-start; }
      .sidebar-header h2 { font-size: 0.82rem; line-height: 1.15; word-break: break-word; hyphens: auto; }
      .sidebar-header span { font-size: 0.58rem; line-height: 1.2; }
      .sidebar-header .logo { width: 30px !important; height: 30px !important; font-size: 1rem !important; flex-shrink: 0; }
      .sidebar-nav {
        padding-bottom: calc(4.5rem + env(safe-area-inset-bottom, 0px));
      }
      .sidebar-nav a { padding: 0.44rem 0.7rem; gap: 0.42rem; font-size: 0.74rem; min-height: 44px; touch-action: manipulation; }
      .sidebar-nav a .icon { font-size: 0.92rem; width: 20px; flex-shrink: 0; }
      .sidebar-nav a .nav-txt { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .sidebar-nav .nav-section { padding: 0.28rem 0.7rem 0.08rem; font-size: 0.56rem; margin-top: 0.24rem; }
      .bottom-nav {
        height: calc(50px + env(safe-area-inset-bottom, 0px));
        padding-bottom: env(safe-area-inset-bottom, 0px);
        overflow-x: auto;
        overflow-y: hidden;
        -webkit-overflow-scrolling: touch;
        justify-content: flex-start;
        scroll-snap-type: x proximity;
        scrollbar-width: none;
      }
      .bottom-nav::-webkit-scrollbar { display: none; }
      .bottom-nav-item {
        flex: 0 0 auto;
        min-width: 54px;
        max-width: 76px;
        font-size: 0.54rem;
        gap: 1px;
        padding: 0 3px;
        scroll-snap-align: start;
        min-height: 44px;
      }
      .bottom-nav-item .bnav-icon { font-size: 1.05rem; }
      .bottom-nav-item .bnav-label { max-width: 3.4rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .content { padding-bottom: calc(58px + env(safe-area-inset-bottom, 0px)); }
      .toast { bottom: calc(58px + env(safe-area-inset-bottom, 0px)); }
      .fab { bottom: calc(66px + env(safe-area-inset-bottom, 0px)); }
    }
    @media (max-width: 380px) {
      .topbar { padding: 0 0.25rem; height: 48px; }
      .topbar .topbar-locale-wrap .lang-menu.open { top: calc(48px + env(safe-area-inset-top, 0px)); }
      .menu-toggle { font-size: 0.82rem; min-width: 42px; min-height: 42px; padding: 0.15rem 0.32rem; }
      .sidebar { width: min(255px, 92vw); }
      .sidebar-nav a { padding: 0.4rem 0.62rem; font-size: 0.7rem; }
      .bottom-nav-item { min-width: 50px; font-size: 0.5rem; }
      .bottom-nav-item .bnav-label { max-width: 3rem; }
    }
    /* __HRMM_MOBILE_MARKER__ */
"""

TOGGLE_LANG_OLD = """window.toggleLangMenu = function(e) {
  e.stopPropagation();
  var m = document.getElementById('langMenu');
  var btn = document.getElementById('langMenuBtn');
  if (!m) return;
  var open = m.classList.contains('open');
  if (open) { m.style.display = 'none'; m.classList.remove('open'); if (btn) btn.setAttribute('aria-expanded', 'false'); }
  else { m.style.display = 'block'; m.classList.add('open'); if (btn) btn.setAttribute('aria-expanded', 'true'); }
};"""

TOGGLE_LANG_NEW = """window.closeLangMenu = function() {
  var m = document.getElementById('langMenu');
  var btn = document.getElementById('langMenuBtn');
  var bd = document.getElementById('langMenuBackdrop');
  if (m) { m.style.display = 'none'; m.classList.remove('open'); }
  if (btn) btn.setAttribute('aria-expanded', 'false');
  if (bd) bd.classList.remove('open');
};
window.toggleLangMenu = function(e) {
  if (e) {
    if (e.preventDefault) e.preventDefault();
    if (e.stopPropagation) e.stopPropagation();
  }
  var m = document.getElementById('langMenu');
  var btn = document.getElementById('langMenuBtn');
  var bd = document.getElementById('langMenuBackdrop');
  if (!m) return;
  var open = m.classList.contains('open');
  if (open) { window.closeLangMenu(); }
  else {
    m.style.display = 'block';
    m.classList.add('open');
    if (btn) btn.setAttribute('aria-expanded', 'true');
    if (bd) bd.classList.add('open');
  }
};"""

FINISH_LOCALE_OLD = """  var m = document.getElementById('langMenu');
  if (m) { m.style.display = 'none'; m.classList.remove('open'); }
  var b = document.getElementById('langMenuBtn');
  if (b) b.setAttribute('aria-expanded', 'false');"""

FINISH_LOCALE_NEW = """  if (typeof window.closeLangMenu === 'function') window.closeLangMenu();
  else {
    var m = document.getElementById('langMenu');
    if (m) { m.style.display = 'none'; m.classList.remove('open'); }
    var b = document.getElementById('langMenuBtn');
    if (b) b.setAttribute('aria-expanded', 'false');
  }"""

INIT_I18N_CLICK_OLD = """  document.addEventListener('click', function(ev) {
    var m = document.getElementById('langMenu');
    var w = document.getElementById('topbarLangMenuWrap');
    if (m && m.classList.contains('open') && w && !w.contains(ev.target)) { m.style.display = 'none'; m.classList.remove('open'); var b2 = document.getElementById('langMenuBtn'); if (b2) b2.setAttribute('aria-expanded', 'false'); }
  });"""

INIT_I18N_CLICK_NEW = """  document.addEventListener('click', function(ev) {
    var m = document.getElementById('langMenu');
    var w = document.getElementById('topbarLangMenuWrap');
    var bd = document.getElementById('langMenuBackdrop');
    if (m && m.classList.contains('open') && w && !w.contains(ev.target) && (!bd || ev.target === bd)) {
      if (typeof window.closeLangMenu === 'function') window.closeLangMenu();
    }
  });
  document.addEventListener('touchend', function(ev) {
    var m = document.getElementById('langMenu');
    var w = document.getElementById('topbarLangMenuWrap');
    var bd = document.getElementById('langMenuBackdrop');
    if (m && m.classList.contains('open') && w && !w.contains(ev.target) && (!bd || ev.target === bd)) {
      if (typeof window.closeLangMenu === 'function') window.closeLangMenu();
    }
  }, { passive: true });"""

LANG_BACKDROP_HTML = """  <div class="lang-menu-backdrop" id="langMenuBackdrop" onclick="closeLangMenu()" aria-hidden="true"></div>
  <div class="sidebar-overlay" id="sidebarOverlay"></div>"""

SIDEBAR_OVERLAY_ONLY = '  <div class="sidebar-overlay" id="sidebarOverlay"></div>'

MENU_TOGGLE_OLD = """document.getElementById('menuToggle').addEventListener('click', () => { document.getElementById('sidebar').classList.toggle('open'); document.getElementById('sidebarOverlay').classList.toggle('open'); });
document.getElementById('sidebarOverlay').addEventListener('click', () => { document.getElementById('sidebar').classList.remove('open'); document.getElementById('sidebarOverlay').classList.remove('open'); });"""

MENU_TOGGLE_NEW = """function hrmmToggleSidebar(open) {
  var sb = document.getElementById('sidebar');
  var ov = document.getElementById('sidebarOverlay');
  if (!sb || !ov) return;
  var want = typeof open === 'boolean' ? open : !sb.classList.contains('open');
  sb.classList.toggle('open', want);
  ov.classList.toggle('open', want);
}
document.getElementById('menuToggle').addEventListener('click', function(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  hrmmToggleSidebar();
});
document.getElementById('menuToggle').addEventListener('touchend', function(e) {
  e.preventDefault();
  hrmmToggleSidebar();
});
document.getElementById('sidebarOverlay').addEventListener('click', function() { hrmmToggleSidebar(false); });
document.getElementById('sidebarOverlay').addEventListener('touchend', function(e) { e.preventDefault(); hrmmToggleSidebar(false); });"""

TOGGLE_SIDEBAR_NAV_OLD = """window.toggleSidebarFromNav = function() {
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('sidebarOverlay').classList.toggle('open');
};"""

TOGGLE_SIDEBAR_NAV_NEW = """window.toggleSidebarFromNav = function() {
  if (typeof hrmmToggleSidebar === 'function') hrmmToggleSidebar();
  else {
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('sidebarOverlay').classList.toggle('open');
  }
};"""


def _mobile_css() -> str:
    return MOBILE_CSS.replace("__HRMM_MOBILE_MARKER__", MARKER)


def _strip_old_mobile_css(content: str) -> str:
    content = re.sub(
        r"\n\s*/\* HRMM mobile hamburger menu[^\n]*\*/[\s\S]*?/\* HRMM-MOBILE-MENU-v\d+ \*/\n",
        "\n",
        content,
    )
    content = re.sub(
        r"\n\s*/\* HRMM mobile hamburger menu \*/\n\s*@media \(max-width: 600px\)[\s\S]*?/\* HRMM-MOBILE-MENU-v1 \*/\n",
        "\n",
        content,
    )
    return content


def _apply_js_upgrades(content: str) -> str:
    if TOGGLE_LANG_OLD in content:
        content = content.replace(TOGGLE_LANG_OLD, TOGGLE_LANG_NEW, 1)
    elif "window.closeLangMenu" not in content and "window.toggleLangMenu = function" in content:
        content = content.replace(
            "window.toggleLangMenu = function",
            "window.closeLangMenu = function() {\n"
            "  var m = document.getElementById('langMenu');\n"
            "  var btn = document.getElementById('langMenuBtn');\n"
            "  var bd = document.getElementById('langMenuBackdrop');\n"
            "  if (m) { m.style.display = 'none'; m.classList.remove('open'); }\n"
            "  if (btn) btn.setAttribute('aria-expanded', 'false');\n"
            "  if (bd) bd.classList.remove('open');\n"
            "};\nwindow.toggleLangMenu = function",
            1,
        )

    if FINISH_LOCALE_OLD in content:
        content = content.replace(FINISH_LOCALE_OLD, FINISH_LOCALE_NEW, 1)

    if INIT_I18N_CLICK_OLD in content:
        content = content.replace(INIT_I18N_CLICK_OLD, INIT_I18N_CLICK_NEW, 1)

    if SIDEBAR_OVERLAY_ONLY in content and 'id="langMenuBackdrop"' not in content:
        content = content.replace(SIDEBAR_OVERLAY_ONLY, LANG_BACKDROP_HTML, 1)

    if MENU_TOGGLE_OLD in content:
        content = content.replace(MENU_TOGGLE_OLD, MENU_TOGGLE_NEW, 1)

    if TOGGLE_SIDEBAR_NAV_OLD in content:
        content = content.replace(TOGGLE_SIDEBAR_NAV_OLD, TOGGLE_SIDEBAR_NAV_NEW, 1)

    return content


def _is_fully_patched(content: str) -> bool:
    return (
        MARKER in content
        and "window.closeLangMenu" in content
        and 'id="langMenuBackdrop"' in content
        and "overflow: visible" in content.split(MARKER, 1)[0][-2500:]
        and "lang-menu-backdrop" in content
        and "hrmmToggleSidebar" in content
    )


def patch(content: str) -> str:
    if _is_fully_patched(content):
        print(f"Mobile menu already patched {MARKER} — skipping")
        return content

    content = _strip_old_mobile_css(content)

    if MENU_OLD in content:
        content = content.replace(MENU_OLD, MENU_NEW, 1)
    elif ".menu-toggle {" in content and "min-width: 44px; min-height: 44px; touch-action" not in content:
        content = re.sub(
            r"\.menu-toggle \{ display: flex;[\s\S]*?min-height: 34px; \}",
            MENU_NEW.strip(),
            content,
            count=1,
        )

    if LANG_WRAP_Z_OLD in content and ".topbar .topbar-locale-wrap { z-index: 320; }" not in content:
        content = content.replace(LANG_WRAP_Z_OLD, LANG_WRAP_Z_NEW, 1)

    if MARKER not in content:
        content = content.replace(
            "  </style>\n</head>",
            _mobile_css() + "  </style>\n</head>",
            1,
        )

    content = _apply_js_upgrades(content)
    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — mobile phone hamburger, locale, and bottom nav")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
