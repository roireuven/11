"""Double-height top/bottom bars on small phones — overflow icons in dropdown menus."""

DOUBLE_BARS_CSS = """
    /* HRMM mobile double bars — tall top/bottom + overflow menus */
    .topbar-more-btn,
    .topbar-more-menu,
    .topbar-more-backdrop,
    .bnav-more-menu,
    .bnav-more-backdrop,
    .mobile-locale-backdrop,
    .mobile-locale-sheet { display: none; }
    @media (max-width: 600px) {
      .topbar {
        display: grid;
        grid-template-columns: auto 1fr auto;
        grid-template-rows: 44px 34px;
        min-height: 88px;
        height: auto;
        align-items: center;
        padding: 0.2rem 0.35rem 0.15rem;
        padding-top: max(0.2rem, env(safe-area-inset-top, 0px));
      }
      .topbar-left,
      .topbar-right { display: contents; }
      .topbar-left .menu-toggle,
      .topbar-left .btn-back { grid-column: 1; grid-row: 1; }
      .topbar-more-btn {
        display: inline-flex !important;
        grid-column: 3;
        grid-row: 1;
        justify-self: end;
        align-self: center;
        min-width: 44px;
        min-height: 44px;
        font-size: 1.35rem;
        line-height: 1;
        padding: 0.15rem 0.4rem;
      }
      .topbar-left #topbarLangMenuWrap,
      .topbar-left #topbarSettingsBtn,
      .topbar-left #topbarDocBtn,
      .topbar-right .topbar-locale-pick,
      .topbar-right .dark-toggle,
      .topbar-right .topbar-user,
      .topbar-right .btn-logout { display: none !important; }
      #pageTitle {
        grid-column: 1 / -1;
        grid-row: 2;
        display: block !important;
        font-size: 0.86rem;
        text-align: center;
        margin: 0;
        padding: 0 0.35rem 0.1rem;
        line-height: 1.2;
      }
      .topbar-more-menu {
        display: none;
        position: fixed;
        right: max(0.45rem, env(safe-area-inset-right, 0px));
        top: calc(88px + env(safe-area-inset-top, 0px));
        min-width: 11.5rem;
        max-width: min(18rem, 92vw);
        background: var(--card-bg, #fff);
        border: 1px solid var(--border, #ddd);
        border-radius: 12px;
        box-shadow: 0 12px 32px rgba(0,0,0,0.22);
        z-index: 10060;
        padding: 0.35rem 0;
        max-height: min(58vh, 360px);
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
      }
      .topbar-more-menu.open { display: block; }
      .topbar-more-backdrop {
        display: none;
        position: fixed;
        inset: 0;
        z-index: 10055;
        background: rgba(0,0,0,0.32);
      }
      .topbar-more-backdrop.open { display: block; }
      .topbar-more-opt {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        width: 100%;
        border: none;
        background: none;
        font: inherit;
        font-size: 0.88rem;
        font-weight: 600;
        text-align: start;
        padding: 0.65rem 0.85rem;
        color: var(--text, #1c1e21);
        cursor: pointer;
        touch-action: manipulation;
      }
      .topbar-more-opt:hover,
      .topbar-more-opt:focus { background: rgba(26,115,232,0.08); }
      .topbar-more-opt .tmo-ico { font-size: 1.1rem; width: 1.35rem; text-align: center; flex-shrink: 0; }
      .mobile-locale-backdrop {
        display: none;
        position: fixed;
        inset: 0;
        z-index: 10150;
        background: rgba(0,0,0,0.45);
      }
      .mobile-locale-backdrop.open { display: block; }
      .mobile-locale-sheet {
        display: none;
        position: fixed;
        left: max(0.5rem, env(safe-area-inset-left, 0px));
        right: max(0.5rem, env(safe-area-inset-right, 0px));
        top: 50%;
        transform: translateY(-50%);
        max-height: min(72vh, 520px);
        background: var(--card-bg, #fff);
        border: 1px solid var(--border, #ddd);
        border-radius: 14px;
        box-shadow: 0 16px 48px rgba(0,0,0,0.3);
        z-index: 10160;
        flex-direction: column;
        overflow: hidden;
      }
      .mobile-locale-sheet.open { display: flex; }
      .mobile-locale-sheet-hd {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        padding: 0.85rem 1rem;
        font-weight: 700;
        font-size: 0.95rem;
        border-bottom: 1px solid var(--border, #ddd);
        flex-shrink: 0;
      }
      .mobile-locale-sheet-hd button {
        border: none;
        background: none;
        font-size: 1.35rem;
        line-height: 1;
        padding: 0.2rem 0.35rem;
        cursor: pointer;
        color: var(--text-light, #666);
      }
      .mobile-locale-list {
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
        padding: 0.35rem 0;
        flex: 1 1 auto;
        min-height: 0;
      }
      .mobile-locale-opt {
        display: block;
        width: 100%;
        border: none;
        background: none;
        font: inherit;
        font-size: 0.92rem;
        font-weight: 600;
        text-align: start;
        padding: 0.72rem 1rem;
        color: var(--text, #1c1e21);
        cursor: pointer;
        touch-action: manipulation;
      }
      .mobile-locale-opt:hover,
      .mobile-locale-opt:focus { background: rgba(26,115,232,0.08); }
      .mobile-locale-opt.selected {
        background: rgba(26,115,232,0.12);
        color: #1a73e8;
        font-weight: 800;
      }
      .bottom-nav {
        height: calc(76px + env(safe-area-inset-bottom, 0px)) !important;
        min-height: calc(76px + env(safe-area-inset-bottom, 0px));
        padding-bottom: env(safe-area-inset-bottom, 0px);
        align-items: stretch;
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
        min-width: 50px;
        max-width: 68px;
        min-height: 58px !important;
        padding: 0.38rem 0.15rem 0.28rem !important;
        justify-content: center;
        gap: 0.18rem !important;
        scroll-snap-align: start;
      }
      .bottom-nav-item .bnav-icon { font-size: 1.15rem !important; line-height: 1; }
      .bottom-nav-item .bnav-label { font-size: 0.5rem !important; line-height: 1.1; max-width: 4rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .bottom-nav-item.bnav-mobile-more-item { display: none !important; }
      .bottom-nav-item.bottom-nav-more { display: flex !important; min-width: 46px; }
      .bnav-more-menu {
        display: none;
        position: fixed;
        right: max(0.45rem, env(safe-area-inset-right, 0px));
        bottom: calc(76px + env(safe-area-inset-bottom, 0px) + 0.35rem);
        min-width: 11.5rem;
        max-width: min(18rem, 92vw);
        background: var(--card-bg, #fff);
        border: 1px solid var(--border, #ddd);
        border-radius: 12px;
        box-shadow: 0 -8px 28px rgba(0,0,0,0.2);
        z-index: 160;
        padding: 0.35rem 0;
        max-height: min(50vh, 320px);
        overflow-y: auto;
      }
      .bnav-more-menu.open { display: block; }
      .bnav-more-backdrop {
        display: none;
        position: fixed;
        inset: 0;
        z-index: 155;
        background: rgba(0,0,0,0.28);
      }
      .bnav-more-backdrop.open { display: block; }
      .bnav-more-opt {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        width: 100%;
        border: none;
        background: none;
        font: inherit;
        font-size: 0.86rem;
        font-weight: 600;
        text-align: start;
        padding: 0.62rem 0.85rem;
        color: var(--text, #1c1e21);
        cursor: pointer;
        touch-action: manipulation;
      }
      .bnav-more-opt:hover,
      .bnav-more-opt:focus { background: rgba(26,115,232,0.08); }
      .bnav-more-opt .bmo-ico { font-size: 1.1rem; width: 1.35rem; text-align: center; flex-shrink: 0; }
      .content {
        padding-bottom: calc(80px + env(safe-area-inset-bottom, 0px)) !important;
      }
      .toast { bottom: calc(80px + env(safe-area-inset-bottom, 0px)) !important; }
      .fab { bottom: calc(88px + env(safe-area-inset-bottom, 0px)) !important; }
    }
    @media (max-width: 380px) {
      .topbar { grid-template-rows: 42px 32px; min-height: 84px; }
      .topbar-more-menu { top: calc(84px + env(safe-area-inset-top, 0px)); }
      #pageTitle { font-size: 0.8rem; }
      .bottom-nav-item { min-width: 46px; max-width: 62px; }
      .bottom-nav-item .bnav-label { font-size: 0.46rem !important; max-width: 3.5rem; }
    }
    /* HRMM-MOBILE-DOUBLE-BARS-v2 */
"""

TOPBAR_MORE_HTML = """
    <button type="button" class="btn-lang topbar-more-btn" id="topbarMoreBtn" onclick="toggleTopbarMoreMenu(event)" aria-haspopup="true" aria-expanded="false" data-i18n-title="topbar.more" title="More" aria-label="More">&#8942;</button>
    <div class="topbar-more-backdrop" id="topbarMoreBackdrop" onclick="closeTopbarMoreMenu()" aria-hidden="true"></div>
    <div class="topbar-more-menu" id="topbarMoreMenu" role="menu" aria-label="More actions">
      <button type="button" class="topbar-more-opt" onclick="openMobileLocalePopup()"><span class="tmo-ico">&#127760;</span><span data-i18n="topbar.localization">Localization</span></button>
      <button type="button" class="topbar-more-opt" onclick="closeTopbarMoreMenu();navToPage('settings')"><span class="tmo-ico">&#9881;</span><span data-i18n="nav.settings">Settings</span></button>
      <button type="button" class="topbar-more-opt" onclick="closeTopbarMoreMenu();navToPage('documentation')"><span class="tmo-ico">&#128214;</span><span data-i18n="topbar.documentation">Documentation</span></button>
      <button type="button" class="topbar-more-opt" onclick="closeTopbarMoreMenu();toggleDarkMode()"><span class="tmo-ico">&#127769;</span><span data-i18n="topbar.toggleDark">Dark mode</span></button>
      <button type="button" class="topbar-more-opt" onclick="closeTopbarMoreMenu();doLogout()"><span class="tmo-ico">&#10140;</span><span data-i18n="topbar.logout">Logout</span></button>
    </div>
    <div class="mobile-locale-backdrop" id="mobileLocaleBackdrop" onclick="closeMobileLocalePopup()" aria-hidden="true"></div>
    <div class="mobile-locale-sheet" id="mobileLocaleSheet" role="dialog" aria-labelledby="mobileLocaleTitle" aria-modal="true">
      <div class="mobile-locale-sheet-hd">
        <span id="mobileLocaleTitle" data-i18n="topbar.chooseLanguage">Choose language</span>
        <button type="button" onclick="closeMobileLocalePopup()" aria-label="Close">&times;</button>
      </div>
      <div class="mobile-locale-list" id="mobileLocaleList"></div>
    </div>"""

DOUBLE_BARS_JS = r"""
window.closeTopbarMoreMenu = function() {
  var m = document.getElementById('topbarMoreMenu');
  var b = document.getElementById('topbarMoreBackdrop');
  var btn = document.getElementById('topbarMoreBtn');
  if (m) m.classList.remove('open');
  if (b) b.classList.remove('open');
  if (btn) btn.setAttribute('aria-expanded', 'false');
};
window.toggleTopbarMoreMenu = function(e) {
  if (e) { if (e.preventDefault) e.preventDefault(); if (e.stopPropagation) e.stopPropagation(); }
  var m = document.getElementById('topbarMoreMenu');
  var b = document.getElementById('topbarMoreBackdrop');
  var btn = document.getElementById('topbarMoreBtn');
  if (!m) return;
  var open = m.classList.contains('open');
  if (open) { window.closeTopbarMoreMenu(); return; }
  if (typeof window.closeLangMenu === 'function') window.closeLangMenu();
  if (typeof window.closeBnavMoreMenu === 'function') window.closeBnavMoreMenu();
  if (typeof window.closeMobileLocalePopup === 'function') window.closeMobileLocalePopup();
  m.classList.add('open');
  if (b) b.classList.add('open');
  if (btn) btn.setAttribute('aria-expanded', 'true');
};
window.closeMobileLocalePopup = function() {
  var s = document.getElementById('mobileLocaleSheet');
  var b = document.getElementById('mobileLocaleBackdrop');
  if (s) s.classList.remove('open');
  if (b) b.classList.remove('open');
};
window.renderMobileLocaleList = function() {
  var list = document.getElementById('mobileLocaleList');
  if (!list || typeof I18N_LOCALE_LIST === 'undefined') return;
  var cur = (typeof getCurrentUiLocale === 'function') ? getCurrentUiLocale() : 'en';
  list.innerHTML = I18N_LOCALE_LIST.map(function(o) {
    var code = String(o.code || 'en');
    var lab = String(o.label || code);
    var sel = code === cur ? ' selected' : '';
    return '<button type="button" class="mobile-locale-opt' + sel + '" data-lang="' + code.replace(/"/g, '&quot;') + '" onclick="setAppLocale(this.getAttribute(\'data-lang\'));closeMobileLocalePopup();closeTopbarMoreMenu();">' + lab.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</button>';
  }).join('');
};
window.openMobileLocalePopup = function() {
  if (typeof window.closeTopbarMoreMenu === 'function') window.closeTopbarMoreMenu();
  if (typeof window.closeLangMenu === 'function') window.closeLangMenu();
  if (typeof window.renderMobileLocaleList === 'function') window.renderMobileLocaleList();
  var s = document.getElementById('mobileLocaleSheet');
  var b = document.getElementById('mobileLocaleBackdrop');
  if (s) s.classList.add('open');
  if (b) b.classList.add('open');
  if (typeof applyShellI18n === 'function') applyShellI18n();
};
window.closeBnavMoreMenu = function() {
  var m = document.getElementById('bnavMoreMenu');
  var b = document.getElementById('bnavMoreBackdrop');
  if (m) m.classList.remove('open');
  if (b) b.classList.remove('open');
};
window.toggleBnavMoreMenu = function(e) {
  if (e) { if (e.preventDefault) e.preventDefault(); if (e.stopPropagation) e.stopPropagation(); }
  var m = document.getElementById('bnavMoreMenu');
  var b = document.getElementById('bnavMoreBackdrop');
  if (!m) return;
  var open = m.classList.contains('open');
  if (open) { window.closeBnavMoreMenu(); return; }
  if (typeof window.closeTopbarMoreMenu === 'function') window.closeTopbarMoreMenu();
  if (typeof window.closeLangMenu === 'function') window.closeLangMenu();
  if (typeof window.closeMobileLocalePopup === 'function') window.closeMobileLocalePopup();
  m.classList.add('open');
  if (b) b.classList.add('open');
};
(function hrmmInitMobileDoubleBars_() {
  function wireBnavMore() {
    var nav = document.getElementById('bottomNav');
    if (!nav) return;
    ['guestorder-rest', 'guestorder-mart'].forEach(function(key) {
      var el = nav.querySelector('[data-bnav="' + key + '"]');
      if (el) el.classList.remove('bnav-mobile-more-item');
    });
    ['documentation', 'settings'].forEach(function(key) {
      var el = nav.querySelector('[data-bnav="' + key + '"]');
      if (el) el.classList.add('bnav-mobile-more-item');
    });
    if (!document.getElementById('bnavMoreMenu')) {
      var moreBtn = document.createElement('button');
      moreBtn.type = 'button';
      moreBtn.className = 'bottom-nav-item bottom-nav-more';
      moreBtn.setAttribute('data-bnav', 'more');
      moreBtn.onclick = function(ev) { toggleBnavMoreMenu(ev); };
      moreBtn.innerHTML = '<span class="bnav-icon">&#8942;</span><span class="bnav-label" data-i18n="bnav.more">More</span>';
      nav.appendChild(moreBtn);
      var backdrop = document.createElement('div');
      backdrop.className = 'bnav-more-backdrop';
      backdrop.id = 'bnavMoreBackdrop';
      backdrop.onclick = function() { closeBnavMoreMenu(); };
      var menu = document.createElement('div');
      menu.className = 'bnav-more-menu';
      menu.id = 'bnavMoreMenu';
      menu.setAttribute('role', 'menu');
      menu.innerHTML =
        '<button type="button" class="bnav-more-opt" onclick="closeBnavMoreMenu();bnav(\'documentation\')"><span class="bmo-ico">&#128214;</span><span data-i18n="bnav.documentation">Docs</span></button>' +
        '<button type="button" class="bnav-more-opt" onclick="closeBnavMoreMenu();bnav(\'settings\')"><span class="bmo-ico">&#9881;</span><span data-i18n="nav.settings">Settings</span></button>';
      document.body.appendChild(backdrop);
      document.body.appendChild(menu);
    } else {
      var menu = document.getElementById('bnavMoreMenu');
      if (menu) {
        menu.innerHTML =
          '<button type="button" class="bnav-more-opt" onclick="closeBnavMoreMenu();bnav(\'documentation\')"><span class="bmo-ico">&#128214;</span><span data-i18n="bnav.documentation">Docs</span></button>' +
          '<button type="button" class="bnav-more-opt" onclick="closeBnavMoreMenu();bnav(\'settings\')"><span class="bmo-ico">&#9881;</span><span data-i18n="nav.settings">Settings</span></button>';
      }
    }
    if (typeof applyShellI18n === 'function') applyShellI18n();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wireBnavMore);
  else wireBnavMore();
  document.addEventListener('click', function(ev) {
    var tm = document.getElementById('topbarMoreMenu');
    var tb = document.getElementById('topbarMoreBtn');
    if (tm && tm.classList.contains('open') && tb && !tb.contains(ev.target) && !tm.contains(ev.target)) {
      var tbd = document.getElementById('topbarMoreBackdrop');
      if (!tbd || ev.target === tbd) closeTopbarMoreMenu();
    }
  });
})();
"""
