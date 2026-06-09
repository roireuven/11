#!/usr/bin/env python3
"""Invoice bills: bank payment QR + logo only (no guest order QRs on invoices)."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "HRMM-INVOICE-PAYMENT-QR-ONLY-v1"
INDEX = Path("public/index.html")

BUILD_INVOICE_QR_HTML_GUEST = """function buildInvoiceQrHtml(inv, opts) {
  opts = opts || {};
  var custom = getEffectiveInvoiceQrImage(inv);
  if (!custom && typeof buildInvoiceGuestOrderQrsHtml === 'function') {
    var guestQrs = buildInvoiceGuestOrderQrsHtml(inv);
    if (guestQrs) {
      var ghtml = guestQrs;
      if (opts.editable) ghtml += buildInvoiceQrEditorHtml(inv, getInvoiceQrPayload(inv));
      return ghtml;
    }
  }
  var payload = custom ? '' : getEffectiveInvoiceQrPayload(inv);
  if (!custom && !payload) return opts.editable ? buildInvoiceQrEditorHtml(inv, getInvoiceQrPayload(inv)) : '';"""

BUILD_INVOICE_QR_HTML_PAYMENT = """function buildInvoiceQrHtml(inv, opts) {
  opts = opts || {};
  var custom = getEffectiveInvoiceQrImage(inv);
  var payload = custom ? '' : getEffectiveInvoiceQrPayload(inv);
  if (!custom && !payload) return opts.editable ? buildInvoiceQrEditorHtml(inv, getInvoiceQrPayload(inv)) : '';"""

REFRESH_INVOICE_QR_GUEST = """function refreshInvoiceQrDisplay(inv) {
  if (!inv && window._activeInvoiceQrCtx) inv = window._activeInvoiceQrCtx.inv;
  if (!inv) return;
  if (!getEffectiveInvoiceQrImage(inv) && typeof buildInvoiceGuestOrderQrsHtml === 'function' && buildInvoiceGuestOrderQrsHtml(inv)) return;
  var imgEl = document.getElementById('invoiceQrDisplayImg');"""

REFRESH_INVOICE_QR_PAYMENT = """function refreshInvoiceQrDisplay(inv) {
  if (!inv && window._activeInvoiceQrCtx) inv = window._activeInvoiceQrCtx.inv;
  if (!inv) return;
  var imgEl = document.getElementById('invoiceQrDisplayImg');"""

GET_INVOICE_QR_PAYLOAD_GUEST = """function getInvoiceQrPayload(inv) {
  if (guestQrOrderOnInvoiceEnabled()) return '';
  var base = (settings && settings.invoiceQrText) ? String(settings.invoiceQrText).trim() : '';"""

GET_INVOICE_QR_PAYLOAD_PAYMENT = """function getInvoiceQrPayload(inv) {
  var base = (settings && settings.invoiceQrText) ? String(settings.invoiceQrText).trim() : '';"""

BUILD_GUEST_ORDER_QRS_OLD = """function buildInvoiceGuestOrderQrsHtml(inv) {
  if (!guestQrOrderOnInvoiceEnabled()) return '';
  if (inv && inv.qrTextOverride != null && inv.qrTextOverride !== undefined && String(inv.qrTextOverride).trim()) return '';
  if (inv && inv.qrImageOverride) return '';
  var html = '<div class="invoice-guest-order-qrs" id="invoiceQrDisplayBlock">';
  if (guestQrRestaurantOrderEnabled()) {
    var u1 = buildGuestOrderUrl('restaurant', inv);
    var c1 = typeof t === 'function' ? t('invoice.qrScanRestaurant') : 'Scan to order from restaurant';
    if (u1) html += buildInvoiceGuestOrderQrBlock(u1, c1);
  }
  if (guestQrMinimartOrderEnabled()) {
    var u2 = buildGuestOrderUrl('minimart', inv);
    var c2 = typeof t === 'function' ? t('invoice.qrScanMinimart') : 'Scan to order from mini-mart';
    if (u2) html += buildInvoiceGuestOrderQrBlock(u2, c2);
  }
  html += '</div>';
  return html.indexOf('invoice-guest-order-qr') >= 0 ? html : '';
}"""

BUILD_GUEST_ORDER_QRS_PAYMENT = """function buildInvoiceGuestOrderQrsHtml(inv) {
  return '';
}"""

BUILD_BRAND_HEADER_OLD = """function buildInvoiceBrandHeaderHtml() {
  var hn = (settings && settings.hotelName) ? String(settings.hotelName) : '';
  var logo = (settings && settings.invoiceLogo) ? String(settings.invoiceLogo).trim() : '';"""

BUILD_BRAND_HEADER_NEW = """function buildInvoiceBrandHeaderHtml(inv) {
  inv = inv || null;
  var hn = (settings && settings.hotelName) ? String(settings.hotelName) : '';
  var logo = '';
  if (inv && inv.logoOverride) logo = String(inv.logoOverride).trim();
  if (!logo) logo = (settings && settings.invoiceLogo) ? String(settings.invoiceLogo).trim() : '';"""

BUILD_BRAND_HEADER_CALL_OLD = "buildInvoiceBrandHeaderHtml() + buildInvoiceQrHtml"
BUILD_BRAND_HEADER_CALL_NEW = "buildInvoiceBrandHeaderHtml(inv) + buildInvoiceQrHtml"

BUILD_QR_EDITOR_OLD = """function buildInvoiceQrEditorHtml(inv, payload) {
  var editVal = (inv && inv.qrTextOverride != null && inv.qrTextOverride !== undefined) ? String(inv.qrTextOverride) : (payload || '');
  return '<div class="invoice-qr-editor post-payment-no-print" id="invoiceQrEditor">' +
    '<div class="invoice-qr-editor-label">Edit QR</div>' +
    '<input type="text" class="form-control invoice-qr-edit-input" id="invoiceQrEditText" value="' + escapeHtml(editVal) + '" placeholder="URL or text for QR code">' +
    '<div class="invoice-qr-editor-actions">' +
    '<input type="file" accept="image/png,image/jpeg,image/webp,image/gif" id="invoiceQrBrowseFile" style="display:none" onchange="invoiceModalQrBrowseChanged(this)">' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById(\\'invoiceQrBrowseFile\\').click()">Browse…</button>' +
    '<button type="button" class="btn btn-sm btn-primary" onclick="applyInvoiceQrEdit()">Apply</button>' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="resetInvoiceQrEdit()">Reset</button>' +
    '</div>' +
    '<p class="invoice-qr-editor-hint">Override QR for this invoice only. Defaults come from Settings.</p>' +
    '</div>';
}"""

BUILD_QR_EDITOR_NEW = """function buildInvoiceQrEditorHtml(inv, payload) {
  var editVal = (inv && inv.qrTextOverride != null && inv.qrTextOverride !== undefined) ? String(inv.qrTextOverride) : (payload || '');
  return '<div class="invoice-qr-editor post-payment-no-print" id="invoiceQrEditor">' +
    '<div class="invoice-qr-editor-label">Invoice logo</div>' +
    '<div class="invoice-qr-editor-actions">' +
    '<input type="file" accept="image/png,image/jpeg,image/webp,image/gif" id="invoiceLogoBrowseFile" style="display:none" onchange="invoiceModalLogoBrowseChanged(this)">' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById(\\'invoiceLogoBrowseFile\\').click()">Browse logo…</button>' +
    '</div>' +
    '<div class="invoice-qr-editor-label" style="margin-top:0.65rem;">Payment QR (from bank)</div>' +
    '<input type="text" class="form-control invoice-qr-edit-input" id="invoiceQrEditText" value="' + escapeHtml(editVal) + '" placeholder="Bank payment URL or text">' +
    '<div class="invoice-qr-editor-actions">' +
    '<input type="file" accept="image/png,image/jpeg,image/webp,image/gif" id="invoiceQrBrowseFile" style="display:none" onchange="invoiceModalQrBrowseChanged(this)">' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById(\\'invoiceQrBrowseFile\\').click()">Browse payment QR…</button>' +
    '<button type="button" class="btn btn-sm btn-primary" onclick="applyInvoiceQrEdit()">Apply</button>' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="resetInvoiceQrEdit()">Reset</button>' +
    '</div>' +
    '<p class="invoice-qr-editor-hint">Payment QR and logo for this bill only. Guest order QRs stay on the bottom nav shortcuts.</p>' +
    '</div>';
}"""

PERSIST_QR_OVERRIDES_OLD = """function persistInvoiceQrOverrides(inv) {
  if (!inv || !inv.id) return;
  try {
    if (typeof load === 'function') invoices = load('invoices', invoices);
    var idx = (invoices || []).findIndex(function(i) { return i && i.id === inv.id; });
    if (idx < 0) return;
    if (inv.qrTextOverride != null && inv.qrTextOverride !== undefined) invoices[idx].qrTextOverride = inv.qrTextOverride;
    else delete invoices[idx].qrTextOverride;
    if (inv.qrImageOverride) invoices[idx].qrImageOverride = inv.qrImageOverride;
    else delete invoices[idx].qrImageOverride;
    save('invoices', invoices);
  } catch (e) {}
}"""

PERSIST_QR_OVERRIDES_NEW = """function persistInvoiceQrOverrides(inv) {
  if (!inv || !inv.id) return;
  try {
    if (typeof load === 'function') invoices = load('invoices', invoices);
    var idx = (invoices || []).findIndex(function(i) { return i && i.id === inv.id; });
    if (idx < 0) return;
    if (inv.qrTextOverride != null && inv.qrTextOverride !== undefined) invoices[idx].qrTextOverride = inv.qrTextOverride;
    else delete invoices[idx].qrTextOverride;
    if (inv.qrImageOverride) invoices[idx].qrImageOverride = inv.qrImageOverride;
    else delete invoices[idx].qrImageOverride;
    if (inv.logoOverride) invoices[idx].logoOverride = inv.logoOverride;
    else delete invoices[idx].logoOverride;
    save('invoices', invoices);
  } catch (e) {}
}
function refreshInvoiceBrandDisplay(inv) {
  if (!inv && window._activeInvoiceQrCtx) inv = window._activeInvoiceQrCtx.inv;
  if (!inv) return;
  var block = document.querySelector('.invoice-brand-block');
  if (!block) return;
  var logo = '';
  if (inv.logoOverride) logo = String(inv.logoOverride).trim();
  if (!logo && settings && settings.invoiceLogo) logo = String(settings.invoiceLogo).trim();
  var img = block.querySelector('img');
  if (logo) {
    if (img) img.src = logo;
    else {
      var hn = (settings && settings.hotelName) ? String(settings.hotelName) : '';
      block.insertAdjacentHTML('afterbegin', '<img src="' + escapeHtml(logo) + '" alt="' + escapeHtml(hn || 'Logo') + '">');
    }
  } else if (img) img.remove();
}
window.invoiceModalLogoBrowseChanged = function(input) {
  var ctx = window._activeInvoiceQrCtx;
  if (!ctx || !ctx.inv) return;
  var f = input && input.files && input.files[0];
  if (!f) return;
  if (f.size > 512000) {
    if (typeof toast === 'function') toast('Image too large (max 512 KB)');
    input.value = '';
    return;
  }
  var inv = ctx.inv;
  var reader = new FileReader();
  reader.onload = function() {
    inv.logoOverride = reader.result;
    persistInvoiceQrOverrides(inv);
    refreshInvoiceBrandDisplay(inv);
    if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'Logo updated');
  };
  reader.readAsDataURL(f);
};"""

RESET_QR_EDIT_OLD = """window.resetInvoiceQrEdit = function() {
  var ctx = window._activeInvoiceQrCtx;
  if (!ctx || !ctx.inv) return;
  var inv = ctx.inv;
  delete inv.qrTextOverride;
  delete inv.qrImageOverride;
  var fi = document.getElementById('invoiceQrBrowseFile');
  if (fi) fi.value = '';
  persistInvoiceQrOverrides(inv);
  initInvoiceQrEditor(inv);
  refreshInvoiceQrDisplay(inv);
  if (typeof toast === 'function') toast('QR reset to default');
};"""

RESET_QR_EDIT_NEW = """window.resetInvoiceQrEdit = function() {
  var ctx = window._activeInvoiceQrCtx;
  if (!ctx || !ctx.inv) return;
  var inv = ctx.inv;
  delete inv.qrTextOverride;
  delete inv.qrImageOverride;
  delete inv.logoOverride;
  var fi = document.getElementById('invoiceQrBrowseFile');
  if (fi) fi.value = '';
  var lf = document.getElementById('invoiceLogoBrowseFile');
  if (lf) lf.value = '';
  persistInvoiceQrOverrides(inv);
  initInvoiceQrEditor(inv);
  refreshInvoiceQrDisplay(inv);
  refreshInvoiceBrandDisplay(inv);
  if (typeof toast === 'function') toast('Bill QR reset to default');
};"""

SETTINGS_QR_GUEST = """        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
          <input type="checkbox" id="sInvoiceQrGuestOrderRest" ${(s.invoiceQrIncludeRestaurantOrder===false||s.invoiceQrIncludeRestaurantOrder==='0'||s.invoiceQrIncludeRestaurantOrder===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          Invoice QR — restaurant order (scan to order food)
        </label>
        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
          <input type="checkbox" id="sInvoiceQrGuestOrderMart" ${(s.invoiceQrIncludeMinimartOrder===false||s.invoiceQrIncludeMinimartOrder==='0'||s.invoiceQrIncludeMinimartOrder===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          Invoice QR — mini-mart order (scan to shop)
        </label>
        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;opacity:0.85;">
          <input type="checkbox" id="sInvoiceQrDetails" ${(s.invoiceQrIncludeDetails===false||s.invoiceQrIncludeDetails==='0'||s.invoiceQrIncludeDetails===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          Include invoice number &amp; total in QR (only when guest order QR is off)
        </label>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">When guest order QR is on, invoices show scan-to-order codes for restaurant and/or mini-mart (room/guest from the invoice). Staff can also print Mart QR from the bottom nav.</p>"""

SETTINGS_QR_PAYMENT = """        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;opacity:0.85;">
          <input type="checkbox" id="sInvoiceQrDetails" ${(s.invoiceQrIncludeDetails===false||s.invoiceQrIncludeDetails==='0'||s.invoiceQrIncludeDetails===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          Include invoice number &amp; total in payment QR
        </label>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">Invoices show your bank payment QR only. Restaurant and mini-mart order QRs are on the bottom nav — not on bills.</p>"""

SETTINGS_QR_LABEL_OLD = """        <label>Invoice QR code — text or URL</label>
        <input type="text" class="form-control" id="sInvoiceQrText" value="${s.invoiceQrText||''}" placeholder="https://your-hotel.com or payment link" oninput="updateInvoiceQrPreview()">"""

SETTINGS_QR_LABEL_NEW = """        <label>Payment QR — text or URL (from bank)</label>
        <input type="text" class="form-control" id="sInvoiceQrText" value="${s.invoiceQrText||''}" placeholder="Bank payment link or QR payload" oninput="updateInvoiceQrPreview()">"""

SETTINGS_QR_IMAGE_OLD = """        <label>Custom QR image (optional)</label>
        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" id="sInvoiceQrFile" style="display:none" onchange="invoiceQrFileChanged(this)">
        <div class="invoice-qr-browse-row">
          <button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById('sInvoiceQrFile').click()">Browse…</button>"""

SETTINGS_QR_IMAGE_NEW = """        <label>Payment QR image (from bank)</label>
        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" id="sInvoiceQrFile" style="display:none" onchange="invoiceQrFileChanged(this)">
        <div class="invoice-qr-browse-row">
          <button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById('sInvoiceQrFile').click()">Browse payment QR…</button>"""

SAVE_SETTINGS_QR_GUEST = """  if (document.getElementById('sInvoiceQrText')) settings.invoiceQrText = document.getElementById('sInvoiceQrText').value.trim();
  if (document.getElementById('sInvoiceQrGuestOrderRest')) settings.invoiceQrIncludeRestaurantOrder = document.getElementById('sInvoiceQrGuestOrderRest').checked;
  if (document.getElementById('sInvoiceQrGuestOrderMart')) settings.invoiceQrIncludeMinimartOrder = document.getElementById('sInvoiceQrGuestOrderMart').checked;
  if (document.getElementById('sInvoiceQrGuestOrder')) settings.invoiceQrIncludeRestaurantOrder = document.getElementById('sInvoiceQrGuestOrder').checked;
  if (document.getElementById('sInvoiceQrDetails')) settings.invoiceQrIncludeDetails = document.getElementById('sInvoiceQrDetails').checked;
  settings.maxGuests = parseInt(document.getElementById('sMaxG').value)||3;"""

SAVE_SETTINGS_QR_PAYMENT = """  if (document.getElementById('sInvoiceQrText')) settings.invoiceQrText = document.getElementById('sInvoiceQrText').value.trim();
  if (document.getElementById('sInvoiceQrDetails')) settings.invoiceQrIncludeDetails = document.getElementById('sInvoiceQrDetails').checked;
  settings.invoiceQrIncludeRestaurantOrder = false;
  settings.invoiceQrIncludeMinimartOrder = false;
  settings.maxGuests = parseInt(document.getElementById('sMaxG').value)||3;"""

ENSURE_GUEST_SETTING_OLD = """(function ensureGuestQrOrderSettingDefault() {
  try {
    var mk = (typeof DB_KEY !== 'undefined' ? DB_KEY : 'hotel_mgr_') + 'guestQrOrderForceEnabledV3';
    var done = false;
    try {
      if (typeof settings !== 'undefined' && settings && settings.invoiceQrIncludeRestaurantOrder === undefined) {
        settings.invoiceQrIncludeRestaurantOrder = true;
        if (typeof save === 'function') save('settings', settings);
      }
      if (typeof settings !== 'undefined' && settings && settings.invoiceQrIncludeMinimartOrder === undefined) {
        settings.invoiceQrIncludeMinimartOrder = true;
        if (typeof save === 'function') save('settings', settings);
      }
      if (typeof HotelDB !== 'undefined' && HotelDB && typeof HotelDB.loadSetting === 'function') {
        done = HotelDB.loadSetting('guestQrOrderForceEnabledV3') === '1';
      }
      if (!done && typeof settings !== 'undefined' && settings) {
        settings.invoiceQrIncludeRestaurantOrder = true;
        settings.invoiceQrIncludeMinimartOrder = true;
        if (typeof save === 'function') save('settings', settings);
        if (typeof HotelDB !== 'undefined' && HotelDB && typeof HotelDB.saveSetting === 'function') {
          try { HotelDB.saveSetting('guestQrOrderForceEnabledV3', '1'); } catch (e) {}
        }
      }
    } catch (e) {}
  } catch (e) {}
})();"""

ENSURE_GUEST_SETTING_PAYMENT = """(function ensureInvoicePaymentQrOnly() {
  try {
    var mk = (typeof DB_KEY !== 'undefined' ? DB_KEY : 'hotel_mgr_') + 'invoicePaymentQrOnlyV1';
    var done = false;
    try {
      if (typeof HotelDB !== 'undefined' && HotelDB && typeof HotelDB.loadSetting === 'function') {
        done = HotelDB.loadSetting('invoicePaymentQrOnlyV1') === '1';
      }
      if (!done && typeof settings !== 'undefined' && settings) {
        settings.invoiceQrIncludeRestaurantOrder = false;
        settings.invoiceQrIncludeMinimartOrder = false;
        if (typeof save === 'function') save('settings', settings);
        if (typeof HotelDB !== 'undefined' && HotelDB && typeof HotelDB.saveSetting === 'function') {
          try { HotelDB.saveSetting('invoicePaymentQrOnlyV1', '1'); } catch (e) {}
        }
      }
    } catch (e) {}
  } catch (e) {}
})();"""

MARKER_COMMENT = f"    /* {MARKER} */\n"


def _replace(content: str, old: str, new: str, label: str) -> str:
    if old not in content:
        return content
    return content.replace(old, new, 1)


def patch(content: str) -> str:
    if MARKER in content:
        return content

    content = _replace(content, BUILD_INVOICE_QR_HTML_GUEST, BUILD_INVOICE_QR_HTML_PAYMENT, "buildInvoiceQrHtml")
    content = _replace(content, REFRESH_INVOICE_QR_GUEST, REFRESH_INVOICE_QR_PAYMENT, "refreshInvoiceQrDisplay")
    content = _replace(content, GET_INVOICE_QR_PAYLOAD_GUEST, GET_INVOICE_QR_PAYLOAD_PAYMENT, "getInvoiceQrPayload")
    content = _replace(content, BUILD_GUEST_ORDER_QRS_OLD, BUILD_GUEST_ORDER_QRS_PAYMENT, "buildInvoiceGuestOrderQrsHtml")
    content = _replace(content, BUILD_BRAND_HEADER_OLD, BUILD_BRAND_HEADER_NEW, "buildInvoiceBrandHeaderHtml")
    content = content.replace(BUILD_BRAND_HEADER_CALL_OLD, BUILD_BRAND_HEADER_CALL_NEW)
    content = content.replace("${buildInvoiceBrandHeaderHtml()}", "${buildInvoiceBrandHeaderHtml(inv)}", 1)
    content = _replace(content, BUILD_QR_EDITOR_OLD, BUILD_QR_EDITOR_NEW, "buildInvoiceQrEditorHtml")
    content = _replace(content, PERSIST_QR_OVERRIDES_OLD, PERSIST_QR_OVERRIDES_NEW, "persistInvoiceQrOverrides")
    content = _replace(content, RESET_QR_EDIT_OLD, RESET_QR_EDIT_NEW, "resetInvoiceQrEdit")
    content = _replace(content, SETTINGS_QR_GUEST, SETTINGS_QR_PAYMENT, "settings guest QR")
    content = _replace(content, SETTINGS_QR_LABEL_OLD, SETTINGS_QR_LABEL_NEW, "settings QR label")
    content = _replace(content, SETTINGS_QR_IMAGE_OLD, SETTINGS_QR_IMAGE_NEW, "settings QR image")
    content = _replace(content, SAVE_SETTINGS_QR_GUEST, SAVE_SETTINGS_QR_PAYMENT, "saveSettings QR")
    content = _replace(content, ENSURE_GUEST_SETTING_OLD, ENSURE_GUEST_SETTING_PAYMENT, "ensureGuestQrOrderSettingDefault")

    if MARKER not in content:
        if "/* HRMM invoice items table, logo, and QR */" in content:
            content = content.replace(
                "/* HRMM invoice items table, logo, and QR */",
                "/* HRMM invoice items table, logo, and QR */\n" + MARKER_COMMENT.strip(),
                1,
            )
        else:
            content = content.replace("</style>", MARKER_COMMENT + "</style>", 1)

    return content


def main() -> int:
    if not INDEX.is_file():
        print(f"error: {INDEX} not found — run sync/build first", file=sys.stderr)
        return 1
    content = INDEX.read_text(encoding="utf-8")
    patched = patch(content)
    if patched == content and MARKER not in content:
        print("warn: invoice payment QR patch made no changes", file=sys.stderr)
    INDEX.write_text(patched, encoding="utf-8")
    print(f"patched {INDEX} ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
