#!/usr/bin/env python3
"""Paid/trial licensing for Firebase hosted app (no backend).

Creates /paid.html that boots the same SPA in "paid" mode, and injects
trial/license gating into the login flow.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "HRMM-LICENSE-v1"
GUARD_MARKER = "HRMM-LICENSE-GUARD-v1"
INDEX = Path("public/index.html")
PAID = Path("public/paid.html")
BILLING = Path("config/hrmm-billing.json")

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
  var price = parseInt(window.HRMM_LICENSE_PRICE, 10) || 100;
  var seed = em + '|hrmm|annual|' + String(price);
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
function hrmmAccountLicenseOk(account) {
  if (!window.HRMM_LICENSE_MODE) return true;
  if (!account || !account.email) return false;
  return (!hrmmIsTrialExpired()) || hrmmLicenseOkForEmail(account.email, hrmmGetLicenseKey());
}
function hrmmLoginLicenseGate(account, errEl) {
  if (!window.HRMM_LICENSE_MODE) return true;
  hrmmEnsureTrialStarted();
  hrmmMaybeInjectLicenseField();
  var licEl = document.getElementById('loginLicenseKey');
  var licKey = licEl ? String(licEl.value || '').trim() : hrmmGetLicenseKey();
  if (licKey) hrmmSetLicenseKey(licKey);
  if (hrmmAccountLicenseOk(account)) return true;
  if (errEl) {
    errEl.textContent = (typeof t === 'function' ? t('login.trialExpired') : 'Trial expired. Please enter a valid license key.');
    errEl.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }
  return false;
}
"""

LOGIN_GUARD_ANCHOR = "  currentUser = { id: account.id, name: account.name, email: account.email, role: account.role };"
LOGIN_GUARD_SINGLE = (
    "  // <!-- HRMM-LICENSE-GUARD-v1 -->\n"
    "  if (!hrmmLoginLicenseGate(account, errEl)) return;\n"
    "  currentUser = { id: account.id, name: account.name, email: account.email, role: account.role };"
)

LOGIN_OVERLAY_ANCHOR = '<div class="form-group"><label data-i18n="login.password">'
LOGIN_OVERLAY_INSERT = (
    '<div id="loginFormExtra"></div>\n      ' + LOGIN_OVERLAY_ANCHOR
)

AUTOLOGIN_ANCHOR = (
    "      if (account) {\n"
    "        currentUser = { id: account.id, name: account.name, email: account.email, role: account.role };"
)
AUTOLOGIN_NEW = (
    "      if (account) {\n"
    "        if (window.HRMM_LICENSE_MODE && !hrmmAccountLicenseOk(account)) {\n"
    "          hrmmMaybeInjectLicenseField();\n"
    "          return;\n"
    "        }\n"
    "        currentUser = { id: account.id, name: account.name, email: account.email, role: account.role };"
)

DUPLICATE_GUARD_RE = re.compile(
    r"(?:  hrmmEnsureTrialStarted\(\);\n"
    r"  hrmmMaybeInjectLicenseField\(\);\n"
    r"  if \(window\.HRMM_LICENSE_MODE\) \{[\s\S]*?      return;\n"
    r"    \}\n"
    r"  \}\n)+",
    re.MULTILINE,
)

AUTOLOGIN_DUP_RE = re.compile(
    r"(?:  if \(typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl\(\)\) \{ return; \}\n)+"
)

LICENSE_BLOCK_RE = re.compile(
    r"// ===== LOGIN / LOGOUT =====\n// <!-- HRMM-LICENSE-v1 -->[\s\S]*?"
    r"(?=\nfunction readStoredCurrentUser)",
    re.MULTILINE,
)


def load_billing() -> dict:
    path = Path(__file__).resolve().parents[1] / BILLING
    if not path.is_file():
        return {"paypalUrl": "", "licensePriceUsd": 100, "trialDays": 30}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {"paypalUrl": "", "licensePriceUsd": 100, "trialDays": 30}


def _dedupe_license_guards(text: str) -> str:
    text = DUPLICATE_GUARD_RE.sub("", text)
    text = re.sub(
        r"(?:  // <!-- HRMM-LICENSE-GUARD-v1 -->\n  if \(!hrmmLoginLicenseGate\(account, errEl\)\) return;\n)+",
        "  // <!-- HRMM-LICENSE-GUARD-v1 -->\n  if (!hrmmLoginLicenseGate(account, errEl)) return;\n",
        text,
    )
    return text


def patch_index(text: str) -> str:
    if MARKER not in text:
        text = text.replace("</head>", f"  <!-- {MARKER} -->\n</head>", 1)
    else:
        text = re.sub(r"HRMM-LICENSE-v\d+", MARKER, text)

    license_block = LOGIN_INJECT.strip("\n") + "\n"
    if LICENSE_BLOCK_RE.search(text):
        text = LICENSE_BLOCK_RE.sub(license_block, text, count=1)
    elif LOGIN_ANCHOR in text and "hrmmLoginLicenseGate" not in text:
        text = text.replace(LOGIN_ANCHOR, license_block, 1)

    text = _dedupe_license_guards(text)

    if GUARD_MARKER not in text and LOGIN_GUARD_ANCHOR in text:
        text = text.replace(LOGIN_GUARD_ANCHOR, LOGIN_GUARD_SINGLE, 1)

    if 'id="loginFormExtra"' not in text and LOGIN_OVERLAY_ANCHOR in text:
        text = text.replace(LOGIN_OVERLAY_ANCHOR, LOGIN_OVERLAY_INSERT, 1)

    if "hrmmAccountLicenseOk(account)" not in text.split("initAutologinIfSetupComplete")[1][:2500]:
        if AUTOLOGIN_ANCHOR in text:
            text = text.replace(AUTOLOGIN_ANCHOR, AUTOLOGIN_NEW, 1)

    text = AUTOLOGIN_DUP_RE.sub(
        "  if (typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl()) { return; }\n",
        text,
    )

    return text


def build_paid_html(index_html: str, billing: dict) -> str:
    paypal = str(billing.get("paypalUrl") or "").strip()
    price = int(billing.get("licensePriceUsd") or 100)
    trial = int(billing.get("trialDays") or 30)
    inject = (
        "<script>\n"
        "  window.HRMM_LICENSE_MODE = 'paid';\n"
        f"  window.HRMM_PAYPAL_URL = {json.dumps(paypal)};\n"
        f"  window.HRMM_LICENSE_PRICE = {price};\n"
        f"  window.HRMM_LICENSE_TRIAL_DAYS = {trial};\n"
        "</script>\n"
    )
    out = index_html
    out = re.sub(r"<title>[\s\S]*?</title>\s*", "", out)
    if "HRMM-PAID-BOOT-v1" not in out:
        out = re.sub(
            r'(<meta name="app-setup-version"[^>]*>\s*)',
            r'\1  <title>HotelRestaurantMini‑Mart — Licensed</title>\n  <!-- HRMM-PAID-BOOT-v1 -->\n',
            out,
            count=1,
        )
    out = re.sub(
        r"<script>\s*window\.HRMM_LICENSE_MODE = 'paid';[\s\S]*?</script>\s*",
        "",
        out,
    )
    if "</head>" in out:
        out = out.replace("</head>", inject + "</head>", 1)
    return out


def main() -> int:
    if not INDEX.is_file():
        print(f"Missing {INDEX}", file=sys.stderr)
        return 1
    billing = load_billing()
    index_html = INDEX.read_text(encoding="utf-8")
    patched = patch_index(index_html)
    INDEX.write_text(patched, encoding="utf-8")
    paid_html = build_paid_html(patched, billing)
    PAID.write_text(paid_html, encoding="utf-8")
    paypal = str(billing.get("paypalUrl") or "").strip()
    if paypal:
        print(f"Patched {INDEX} and wrote {PAID} ({MARKER}, PayPal configured)")
    else:
        print(f"Patched {INDEX} and wrote {PAID} ({MARKER}, PayPal URL empty — set config/hrmm-billing.json)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
