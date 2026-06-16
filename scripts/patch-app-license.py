#!/usr/bin/env python3
"""Paid/trial licensing for Firebase hosted app (no backend).

Creates /paid.html that boots the same SPA in "paid" mode, and injects
trial/license gating into the login flow.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-LICENSE-v1"
INDEX = Path("public/index.html")
PAID = Path("public/paid.html")

LOGIN_ANCHOR = "// ===== LOGIN / LOGOUT ====="
LOGIN_INJECT = r"""
// ===== LOGIN / LOGOUT =====
// <!-- HRMM-LICENSE-v1 -->
window.HRMM_LICENSE_MODE = window.HRMM_LICENSE_MODE || ''; // '', 'paid'
window.HRMM_PAYPAL_URL = window.HRMM_PAYPAL_URL || ''; // optional
window.HRMM_LICENSE_PRICE = window.HRMM_LICENSE_PRICE || 100;
window.HRMM_LICENSE_TRIAL_DAYS = window.HRMM_LICENSE_TRIAL_DAYS || 30;
function hrmmLsGet(k) { try { return localStorage.getItem(DB_KEY + k); } catch (e) { return null; } }
function hrmmLsSet(k, v) { try { localStorage.setItem(DB_KEY + k, String(v)); } catch (e) {} }
function hrmmNowMs() { return (new Date()).getTime(); }
function hrmmTrialMs() { return (parseInt(window.HRMM_LICENSE_TRIAL_DAYS, 10) || 30) * 86400000; }
function hrmmTrialStart() {
  var v = hrmmLsGet('trialStartMs');
  var n = v ? parseInt(v, 10) : 0;
  return n > 0 ? n : 0;
}
function hrmmEnsureTrialStarted() {
  if (!window.HRMM_LICENSE_MODE) return;
  if (hrmmTrialStart()) return;
  hrmmLsSet('trialStartMs', String(hrmmNowMs()));
}
function hrmmGetLicenseKey() { return hrmmLsGet('licenseKey') || ''; }
function hrmmSetLicenseKey(k) { if (!k) return; hrmmLsSet('licenseKey', String(k).trim()); }
function hrmmIsTrialExpired() {
  if (!window.HRMM_LICENSE_MODE) return false;
  var s = hrmmTrialStart();
  if (!s) return false;
  return (hrmmNowMs() - s) > hrmmTrialMs();
}
function hrmmCrc32(str) {
  var crc = 0 ^ (-1);
  for (var i = 0; i < str.length; i++) {
    var c = str.charCodeAt(i);
    crc = (crc >>> 8) ^ hrmmCrcTable[(crc ^ c) & 0xFF];
  }
  return (crc ^ (-1)) >>> 0;
}
var hrmmCrcTable = (function() {
  var t = new Array(256);
  for (var n = 0; n < 256; n++) {
    var c = n;
    for (var k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    t[n] = c >>> 0;
  }
  return t;
})();
function hrmmExpectedLicenseKey(email) {
  var em = String(email || '').trim().toLowerCase();
  if (!em) return '';
  var seed = em + '|hrmm|annual|100';
  var n = hrmmCrc32(seed);
  return ('HRMM-' + n.toString(36).toUpperCase()).replace(/[^A-Z0-9\-]/g, '');
}
function hrmmLicenseOkForEmail(email, key) {
  if (!window.HRMM_LICENSE_MODE) return true;
  var k = String(key || '').trim().toUpperCase();
  if (!k) return false;
  return k === hrmmExpectedLicenseKey(email);
}
function hrmmRenderLicensePayHintHtml() {
  var u = window.HRMM_PAYPAL_URL ? String(window.HRMM_PAYPAL_URL) : '';
  var price = window.HRMM_LICENSE_PRICE || 100;
  var html = '<div style="margin-top:0.65rem;padding:0.6rem 0.75rem;border:1px solid var(--border);border-radius:10px;background:var(--card-bg);font-size:0.82rem;color:var(--text-light);">' +
    '<div style="font-weight:800;color:var(--text);margin-bottom:0.15rem;">License: $' + String(price) + ' / year</div>' +
    '<div>' + (typeof t === 'function' ? t('login.licenseHint') : 'After payment you receive an email + license key. Enter it below to continue.') + '</div>' +
    (u ? ('<div style="margin-top:0.45rem;"><a class="btn btn-sm btn-primary" style="display:inline-flex;gap:0.35rem;align-items:center;" href="' + escAttr(u) + '" target="_blank" rel="noopener noreferrer">Pay with PayPal</a></div>') : '') +
    '</div>';
  return html;
}
function hrmmMaybeInjectLicenseField() {
  if (!window.HRMM_LICENSE_MODE) return;
  try {
    var box = document.getElementById('loginFormExtra');
    if (!box) return;
    if (box._hrmmLicReady) return;
    box._hrmmLicReady = true;
    box.innerHTML =
      '<div class="form-group" style="margin-top:0.5rem;">' +
      '<label>' + (typeof t === 'function' ? t('login.licenseKey') : 'License key') + '</label>' +
      '<input type="text" class="form-control" id="loginLicenseKey" placeholder="HRMM-XXXXX" value="' + escAttr(hrmmGetLicenseKey()) + '" style="text-transform:uppercase;letter-spacing:0.03em;">' +
      '</div>' + hrmmRenderLicensePayHintHtml();
  } catch (e) {}
}
"""

LOGIN_GUARD_ANCHOR = "  currentUser = { id: account.id, name: account.name, email: account.email, role: account.role };"
LOGIN_GUARD_NEW = (
    "  hrmmEnsureTrialStarted();\n"
    "  hrmmMaybeInjectLicenseField();\n"
    "  if (window.HRMM_LICENSE_MODE) {\n"
    "    var licEl = document.getElementById('loginLicenseKey');\n"
    "    var licKey = licEl ? String(licEl.value || '').trim() : hrmmGetLicenseKey();\n"
    "    if (licKey) hrmmSetLicenseKey(licKey);\n"
    "    var ok = (!hrmmIsTrialExpired()) || hrmmLicenseOkForEmail(account.email, hrmmGetLicenseKey());\n"
    "    if (!ok) {\n"
    "      errEl.textContent = (typeof t === 'function' ? t('login.trialExpired') : 'Trial expired. Please enter a valid license key.');\n"
    "      errEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' });\n"
    "      return;\n"
    "    }\n"
    "  }\n"
    "  currentUser = { id: account.id, name: account.name, email: account.email, role: account.role };"
)

LOGIN_OVERLAY_ANCHOR = '<div class="form-group"><label data-i18n="login.password">'
LOGIN_OVERLAY_INSERT = (
    '<div id="loginFormExtra"></div>\n      ' + LOGIN_OVERLAY_ANCHOR
)


def patch_index(text: str) -> str:
    if MARKER not in text:
        text = text.replace("</head>", f"  <!-- {MARKER} -->\n</head>", 1)
    else:
        text = re.sub(r"HRMM-LICENSE-v\d+", MARKER, text)

    if LOGIN_ANCHOR in text and "hrmmExpectedLicenseKey" not in text:
        text = text.replace(LOGIN_ANCHOR, LOGIN_INJECT.strip("\n"), 1)

    if LOGIN_GUARD_ANCHOR in text and "hrmmIsTrialExpired" not in text.split("window.doLogin")[1][:1200]:
        text = text.replace(LOGIN_GUARD_ANCHOR, LOGIN_GUARD_NEW, 1)

    if "loginFormExtra" not in text and LOGIN_OVERLAY_ANCHOR in text:
        text = text.replace(LOGIN_OVERLAY_ANCHOR, LOGIN_OVERLAY_INSERT, 1)

    return text


def build_paid_html(index_html: str) -> str:
    # Use same SPA, but set license mode + optional PayPal URL in head.
    inject = (
        "<script>\n"
        "  window.HRMM_LICENSE_MODE = 'paid';\n"
        "  // Set your PayPal link here (paypal.me or a hosted button URL)\n"
        "  window.HRMM_PAYPAL_URL = window.HRMM_PAYPAL_URL || '';\n"
        "  window.HRMM_LICENSE_PRICE = 100;\n"
        "  window.HRMM_LICENSE_TRIAL_DAYS = 30;\n"
        "</script>\n"
    )
    out = index_html
    # Some upstream patching may leave multiple <title> tags; collapse to one.
    out = re.sub(r"<title>[\s\S]*?</title>\s*", "", out)
    if "HRMM-PAID-BOOT-v1" not in out:
        out = re.sub(
            r'(<meta name="app-setup-version"[^>]*>\s*)',
            r'\1  <title>HotelRestaurantMini‑Mart — Licensed</title>\n  <!-- HRMM-PAID-BOOT-v1 -->\n',
            out,
            count=1,
        )
    if "</head>" in out and "window.HRMM_LICENSE_MODE = 'paid'" not in out:
        out = out.replace("</head>", inject + "</head>", 1)
    return out


def main() -> int:
    if not INDEX.is_file():
        print(f"Missing {INDEX}", file=sys.stderr)
        return 1
    index_html = INDEX.read_text(encoding="utf-8")
    patched = patch_index(index_html)
    INDEX.write_text(patched, encoding="utf-8")
    paid_html = build_paid_html(patched)
    PAID.write_text(paid_html, encoding="utf-8")
    print(f"Patched {INDEX} and wrote {PAID} ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

