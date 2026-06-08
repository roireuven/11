#!/usr/bin/env python3
"""Guest QR scan → restaurant or mini-mart self-order screen."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _load_v4_fragments() -> tuple[str, str, str]:
    frag_path = Path(__file__).resolve().parent / "_guest_order_v4_fragments.py"
    spec = importlib.util.spec_from_file_location("_guest_order_v4_fragments", frag_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Missing guest order v4 fragments: {frag_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.GUEST_ORDER_PARSE_AND_BOOT_V4, mod.GUEST_ORDER_BOOT_V4, mod.RENDER_GUEST_MINIMART_ORDER_V8


GUEST_ORDER_PARSE_AND_BOOT_V4, GUEST_ORDER_BOOT_V4, RENDER_GUEST_MINIMART_ORDER_V8 = _load_v4_fragments()

MARKER = "HRMM-GUEST-QR-ORDER-v9"
INDEX = Path("public/index.html")

GET_INVOICE_QR_PAYLOAD_OLD = """function getInvoiceQrPayload(inv) {
  var base = (settings && settings.invoiceQrText) ? String(settings.invoiceQrText).trim() : '';
  var includeDetails = !(settings && (settings.invoiceQrIncludeDetails === false || settings.invoiceQrIncludeDetails === '0' || settings.invoiceQrIncludeDetails === 0));
  var parts = [];
  if (base) parts.push(base);
  if (includeDetails && inv) {
    if (inv.invoiceNumber) parts.push('INV:' + String(inv.invoiceNumber));
    if (inv.paymentTransactionId) parts.push('TXN:' + String(inv.paymentTransactionId));
    if (inv.grandTotal != null && inv.grandTotal !== '') parts.push('TOTAL:' + String(inv.grandTotal));
  }
  if (!parts.length) return '';
  return parts.join('|');
}"""

GET_INVOICE_QR_PAYLOAD_V1 = """function guestQrRestaurantOrderEnabled() {
  return !(settings && (settings.invoiceQrIncludeRestaurantOrder === false || settings.invoiceQrIncludeRestaurantOrder === '0' || settings.invoiceQrIncludeRestaurantOrder === 0));
}
function buildGuestRestaurantOrderUrl(inv) {
  var base = '';
  if (settings && settings.invoiceQrText) {
    var custom = String(settings.invoiceQrText).trim();
    if (/^https?:\\/\\//i.test(custom)) base = custom.split('#')[0];
  }
  if (!base) {
    try { base = location.origin + (location.pathname || '/'); } catch (e) { base = ''; }
  }
  if (!base) return '';
  var params = new URLSearchParams();
  params.set('guestOrder', 'restaurant');
  if (inv) {
    if (inv.roomNumber != null && String(inv.roomNumber).trim() !== '') params.set('room', String(inv.roomNumber).trim());
    if (inv.guestName != null && String(inv.guestName).trim() !== '' && String(inv.guestName).trim() !== '—') params.set('guest', String(inv.guestName).trim());
    if (inv.bookingId != null && String(inv.bookingId).trim() !== '') params.set('booking', String(inv.bookingId).trim());
  }
  var q = params.toString();
  if (base.indexOf('?') >= 0) {
    var parts = base.split('?');
    return parts[0] + '?' + q + (parts[1] ? '&' + parts[1] : '');
  }
  return base + '?' + q;
}
function getInvoiceQrPayload(inv) {
  if (guestQrRestaurantOrderEnabled()) {
    var orderUrl = buildGuestRestaurantOrderUrl(inv);
    if (orderUrl) return orderUrl;
  }
  var base = (settings && settings.invoiceQrText) ? String(settings.invoiceQrText).trim() : '';
  var includeDetails = !(settings && (settings.invoiceQrIncludeDetails === false || settings.invoiceQrIncludeDetails === '0' || settings.invoiceQrIncludeDetails === 0));
  var parts = [];
  if (base) parts.push(base);
  if (includeDetails && inv) {
    if (inv.invoiceNumber) parts.push('INV:' + String(inv.invoiceNumber));
    if (inv.paymentTransactionId) parts.push('TXN:' + String(inv.paymentTransactionId));
    if (inv.grandTotal != null && inv.grandTotal !== '') parts.push('TOTAL:' + String(inv.grandTotal));
  }
  if (!parts.length) return '';
  return parts.join('|');
}"""

GET_INVOICE_QR_PAYLOAD_V2 = """function guestQrRestaurantOrderEnabled() {
  return !(settings && (settings.invoiceQrIncludeRestaurantOrder === false || settings.invoiceQrIncludeRestaurantOrder === '0' || settings.invoiceQrIncludeRestaurantOrder === 0));
}
function isLegacyInvoiceQrPayload(text) {
  var s = String(text == null ? '' : text).trim();
  if (!s) return false;
  if (/^INV:/.test(s) || /\\|TXN:/.test(s) || /\\|TOTAL:/.test(s)) return true;
  if (/^TOTAL:/.test(s)) return true;
  return false;
}
function invoiceQrCaptionForPayload(payload) {
  var s = String(payload == null ? '' : payload).trim();
  if (!s) return '';
  if (s.indexOf('guestOrder=restaurant') >= 0) return (typeof t === 'function' ? t('invoice.qrScanRestaurant') : 'Scan to order from restaurant');
  if (s.indexOf('guestOrder=minimart') >= 0) return (typeof t === 'function' ? t('invoice.qrScanMinimart') : 'Scan to order from mini-mart');
  return s.length > 52 ? s.slice(0, 49) + '…' : s;
}
function buildGuestOrderUrl(dept, inv) {
  var deptKey = dept === 'minimart' ? 'minimart' : 'restaurant';
  var base = '';
  if (settings && settings.invoiceQrText) {
    var custom = String(settings.invoiceQrText).trim();
    if (/^https?:\\/\\//i.test(custom)) base = custom.split('#')[0].split('?')[0];
  }
  if (!base) {
    try { base = location.origin + (location.pathname || '/'); } catch (e) { base = ''; }
  }
  if (!base) return '';
  try { base = String(base).split('#')[0]; } catch (e) {}
  var params = new URLSearchParams();
  params.set('guestOrder', deptKey);
  if (inv) {
    var roomVal = inv.roomNumber != null ? String(inv.roomNumber).trim() : '';
    var tableVal = inv.tableNumber != null ? String(inv.tableNumber).trim() : '';
    if (!tableVal && roomVal && /^table\\b/i.test(roomVal)) tableVal = roomVal;
    if (tableVal && tableVal !== '—') params.set('table', tableVal);
    else if (roomVal && roomVal !== '—' && !/^table\\b/i.test(roomVal)) params.set('room', roomVal);
    if (inv.guestName != null && String(inv.guestName).trim() !== '' && String(inv.guestName).trim() !== '—') params.set('guest', String(inv.guestName).trim());
    if (inv.bookingId != null && String(inv.bookingId).trim() !== '') params.set('booking', String(inv.bookingId).trim());
  }
  var q = params.toString();
  if (base.indexOf('?') >= 0) {
    var parts = base.split('?');
    return parts[0] + '?' + q;
  }
  return base + '?' + q;
}
function buildGuestRestaurantOrderUrl(inv) {
  return buildGuestOrderUrl('restaurant', inv);
}
function getInvoiceQrPayload(inv) {
  if (guestQrRestaurantOrderEnabled()) {
    var orderUrl = buildGuestRestaurantOrderUrl(inv);
    if (orderUrl) return orderUrl;
  }
  var base = (settings && settings.invoiceQrText) ? String(settings.invoiceQrText).trim() : '';
  var includeDetails = !(settings && (settings.invoiceQrIncludeDetails === false || settings.invoiceQrIncludeDetails === '0' || settings.invoiceQrIncludeDetails === 0));
  if (guestQrRestaurantOrderEnabled()) includeDetails = false;
  var parts = [];
  if (base && !guestQrRestaurantOrderEnabled()) parts.push(base);
  if (includeDetails && inv) {
    if (inv.invoiceNumber) parts.push('INV:' + String(inv.invoiceNumber));
    if (inv.paymentTransactionId) parts.push('TXN:' + String(inv.paymentTransactionId));
    if (inv.grandTotal != null && inv.grandTotal !== '') parts.push('TOTAL:' + String(inv.grandTotal));
  }
  if (!parts.length) return '';
  return parts.join('|');
}"""

GET_INVOICE_QR_PAYLOAD_V3 = """function guestQrRestaurantOrderEnabled() {
  return !(settings && (settings.invoiceQrIncludeRestaurantOrder === false || settings.invoiceQrIncludeRestaurantOrder === '0' || settings.invoiceQrIncludeRestaurantOrder === 0));
}
function guestQrMinimartOrderEnabled() {
  return !(settings && (settings.invoiceQrIncludeMinimartOrder === false || settings.invoiceQrIncludeMinimartOrder === '0' || settings.invoiceQrIncludeMinimartOrder === 0));
}
function guestQrOrderOnInvoiceEnabled() {
  return guestQrRestaurantOrderEnabled() || guestQrMinimartOrderEnabled();
}
function isLegacyInvoiceQrPayload(text) {
  var s = String(text == null ? '' : text).trim();
  if (!s) return false;
  if (/^INV:/.test(s) || /\\|TXN:/.test(s) || /\\|TOTAL:/.test(s)) return true;
  if (/^TOTAL:/.test(s)) return true;
  return false;
}
function invoiceQrCaptionForPayload(payload) {
  var s = String(payload == null ? '' : payload).trim();
  if (!s) return '';
  if (s.indexOf('guestOrder=restaurant') >= 0) return (typeof t === 'function' ? t('invoice.qrScanRestaurant') : 'Scan to order from restaurant');
  if (s.indexOf('guestOrder=minimart') >= 0) return (typeof t === 'function' ? t('invoice.qrScanMinimart') : 'Scan to order from mini-mart');
  return s.length > 52 ? s.slice(0, 49) + '…' : s;
}
function buildGuestOrderUrl(dept, inv) {
  var deptKey = dept === 'minimart' ? 'minimart' : 'restaurant';
  var base = '';
  if (settings && settings.invoiceQrText) {
    var custom = String(settings.invoiceQrText).trim();
    if (/^https?:\\/\\//i.test(custom)) base = custom.split('#')[0].split('?')[0];
  }
  if (!base) {
    try { base = location.origin + (location.pathname || '/'); } catch (e) { base = ''; }
  }
  if (!base) return '';
  try { base = String(base).split('#')[0]; } catch (e) {}
  var params = new URLSearchParams();
  params.set('guestOrder', deptKey);
  if (inv) {
    var orderNumVal = inv.orderNum != null ? String(inv.orderNum).trim() : '';
    if (orderNumVal && orderNumVal !== '—') {
      params.set('orderNum', orderNumVal);
    } else {
      var roomVal = inv.roomNumber != null ? String(inv.roomNumber).trim() : '';
      var tableVal = inv.tableNumber != null ? String(inv.tableNumber).trim() : '';
      if (!tableVal && roomVal && /^table\\b/i.test(roomVal)) tableVal = roomVal;
      if (tableVal && tableVal !== '—') params.set('table', tableVal);
      else if (roomVal && roomVal !== '—' && !/^table\\b/i.test(roomVal)) params.set('room', roomVal);
      if (inv.guestName != null && String(inv.guestName).trim() !== '' && String(inv.guestName).trim() !== '—') params.set('guest', String(inv.guestName).trim());
      if (inv.bookingId != null && String(inv.bookingId).trim() !== '') params.set('booking', String(inv.bookingId).trim());
    }
  }
  var q = params.toString();
  if (base.indexOf('?') >= 0) {
    var parts = base.split('?');
    return parts[0] + '?' + q;
  }
  return base + '?' + q;
}
function buildGuestRestaurantOrderUrl(inv) {
  return buildGuestOrderUrl('restaurant', inv);
}
function buildInvoiceGuestOrderQrBlock(url, caption) {
  if (!url) return '';
  var cap = caption || '';
  return '<div class="invoice-qr-block invoice-guest-order-qr"><img src="' + escapeHtml(buildInvoiceQrImageUrl(url)) + '" alt="' + escapeHtml(cap) + '" class="invoice-qr-img"><div class="invoice-qr-caption">' + escapeHtml(cap) + '</div></div>';
}
function buildInvoiceGuestOrderQrsHtml(inv) {
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
}
function getInvoiceQrPayload(inv) {
  if (guestQrOrderOnInvoiceEnabled()) return '';
  var base = (settings && settings.invoiceQrText) ? String(settings.invoiceQrText).trim() : '';
  var includeDetails = !(settings && (settings.invoiceQrIncludeDetails === false || settings.invoiceQrIncludeDetails === '0' || settings.invoiceQrIncludeDetails === 0));
  var parts = [];
  if (base) parts.push(base);
  if (includeDetails && inv) {
    if (inv.invoiceNumber) parts.push('INV:' + String(inv.invoiceNumber));
    if (inv.paymentTransactionId) parts.push('TXN:' + String(inv.paymentTransactionId));
    if (inv.grandTotal != null && inv.grandTotal !== '') parts.push('TOTAL:' + String(inv.grandTotal));
  }
  if (!parts.length) return '';
  return parts.join('|');
}"""

BUILD_INVOICE_QR_HTML_HEAD_OLD = """function buildInvoiceQrHtml(inv, opts) {
  opts = opts || {};
  var custom = getEffectiveInvoiceQrImage(inv);
  var payload = custom ? '' : getEffectiveInvoiceQrPayload(inv);
  if (!custom && !payload) return opts.editable ? buildInvoiceQrEditorHtml(inv, getInvoiceQrPayload(inv)) : '';"""

BUILD_INVOICE_QR_HTML_HEAD_NEW = """function buildInvoiceQrHtml(inv, opts) {
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

REFRESH_INVOICE_QR_OLD = """function refreshInvoiceQrDisplay(inv) {
  if (!inv && window._activeInvoiceQrCtx) inv = window._activeInvoiceQrCtx.inv;
  if (!inv) return;
  var imgEl = document.getElementById('invoiceQrDisplayImg');"""

REFRESH_INVOICE_QR_NEW = """function refreshInvoiceQrDisplay(inv) {
  if (!inv && window._activeInvoiceQrCtx) inv = window._activeInvoiceQrCtx.inv;
  if (!inv) return;
  if (!getEffectiveInvoiceQrImage(inv) && typeof buildInvoiceGuestOrderQrsHtml === 'function' && buildInvoiceGuestOrderQrsHtml(inv)) return;
  var imgEl = document.getElementById('invoiceQrDisplayImg');"""

SETTINGS_QR_DETAILS_V3 = """        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
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

SAVE_SETTINGS_QR_V3 = """  if (document.getElementById('sInvoiceQrText')) settings.invoiceQrText = document.getElementById('sInvoiceQrText').value.trim();
  if (document.getElementById('sInvoiceQrGuestOrderRest')) settings.invoiceQrIncludeRestaurantOrder = document.getElementById('sInvoiceQrGuestOrderRest').checked;
  if (document.getElementById('sInvoiceQrGuestOrderMart')) settings.invoiceQrIncludeMinimartOrder = document.getElementById('sInvoiceQrGuestOrderMart').checked;
  if (document.getElementById('sInvoiceQrGuestOrder')) settings.invoiceQrIncludeRestaurantOrder = document.getElementById('sInvoiceQrGuestOrder').checked;
  if (document.getElementById('sInvoiceQrDetails')) settings.invoiceQrIncludeDetails = document.getElementById('sInvoiceQrDetails').checked;
  settings.maxGuests = parseInt(document.getElementById('sMaxG').value)||3;"""

ENSURE_GUEST_SETTING_V3 = """(function ensureGuestQrOrderSettingDefault() {
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

INIT_AUTOLOGIN_DUP_OLD = """  if (typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl()) { return; }
  if (typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl()) { return; }
  if (typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl()) { return; }
  if (typeof tryBootGuestRestaurantOrder === 'function' && tryBootGuestRestaurantOrder()) { return; }"""

INIT_AUTOLOGIN_DUP_ALT = """  if (typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl()) { return; }
  if (typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl()) { return; }
  if (typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl()) { return; }"""

INIT_AUTOLOGIN_DUP_NEW = """  if (typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl()) { return; }
  if (typeof tryBootGuestRestaurantOrder === 'function' && tryBootGuestRestaurantOrder()) { return; }"""

INVOICE_QR_URL_BUILD_OLD = """function invoiceQrCaptionForPayload(payload) {
  var s = String(payload == null ? '' : payload).trim();
  if (!s) return '';
  if (s.indexOf('guestOrder=restaurant') >= 0) return 'Scan to order from restaurant';
  return s.length > 52 ? s.slice(0, 49) + '…' : s;
}
function buildGuestRestaurantOrderUrl(inv) {
  var base = '';
  if (settings && settings.invoiceQrText) {
    var custom = String(settings.invoiceQrText).trim();
    if (/^https?:\\/\\//i.test(custom)) base = custom.split('#')[0].split('?')[0];
  }
  if (!base) {
    try { base = location.origin + (location.pathname || '/'); } catch (e) { base = ''; }
  }
  if (!base) return '';
  try { base = String(base).split('#')[0]; } catch (e) {}
  var params = new URLSearchParams();
  params.set('guestOrder', 'restaurant');
  if (inv) {
    var roomVal = inv.roomNumber != null ? String(inv.roomNumber).trim() : '';
    var tableVal = inv.tableNumber != null ? String(inv.tableNumber).trim() : '';
    if (!tableVal && roomVal && /^table\\b/i.test(roomVal)) tableVal = roomVal;
    if (tableVal && tableVal !== '—') params.set('table', tableVal);
    else if (roomVal && roomVal !== '—' && !/^table\\b/i.test(roomVal)) params.set('room', roomVal);
    if (inv.guestName != null && String(inv.guestName).trim() !== '' && String(inv.guestName).trim() !== '—') params.set('guest', String(inv.guestName).trim());
    if (inv.bookingId != null && String(inv.bookingId).trim() !== '') params.set('booking', String(inv.bookingId).trim());
  }
  var q = params.toString();
  if (base.indexOf('?') >= 0) {
    var parts = base.split('?');
    return parts[0] + '?' + q;
  }
  return base + '?' + q;
}"""

INVOICE_QR_CAPTION_LEGACY = """function invoiceQrCaptionForPayload(payload) {
  var s = String(payload == null ? '' : payload).trim();
  if (!s) return '';
  if (s.indexOf('guestOrder=restaurant') >= 0) return 'Scan to order from restaurant';
  if (s.indexOf('guestOrder=minimart') >= 0) return 'Scan to order from mini-mart';
  return s.length > 52 ? s.slice(0, 49) + '…' : s;
}"""

INVOICE_QR_CAPTION_I18N = """function invoiceQrCaptionForPayload(payload) {
  var s = String(payload == null ? '' : payload).trim();
  if (!s) return '';
  if (s.indexOf('guestOrder=restaurant') >= 0) return (typeof t === 'function' ? t('invoice.qrScanRestaurant') : 'Scan to order from restaurant');
  if (s.indexOf('guestOrder=minimart') >= 0) return (typeof t === 'function' ? t('invoice.qrScanMinimart') : 'Scan to order from mini-mart');
  return s.length > 52 ? s.slice(0, 49) + '…' : s;
}"""

INVOICE_QR_URL_BUILD_NEW = """function invoiceQrCaptionForPayload(payload) {
  var s = String(payload == null ? '' : payload).trim();
  if (!s) return '';
  if (s.indexOf('guestOrder=restaurant') >= 0) return (typeof t === 'function' ? t('invoice.qrScanRestaurant') : 'Scan to order from restaurant');
  if (s.indexOf('guestOrder=minimart') >= 0) return (typeof t === 'function' ? t('invoice.qrScanMinimart') : 'Scan to order from mini-mart');
  return s.length > 52 ? s.slice(0, 49) + '…' : s;
}
function buildGuestOrderUrl(dept, inv) {
  var deptKey = dept === 'minimart' ? 'minimart' : 'restaurant';
  var base = '';
  if (settings && settings.invoiceQrText) {
    var custom = String(settings.invoiceQrText).trim();
    if (/^https?:\\/\\//i.test(custom)) base = custom.split('#')[0].split('?')[0];
  }
  if (!base) {
    try { base = location.origin + (location.pathname || '/'); } catch (e) { base = ''; }
  }
  if (!base) return '';
  try { base = String(base).split('#')[0]; } catch (e) {}
  var params = new URLSearchParams();
  params.set('guestOrder', deptKey);
  if (inv) {
    var roomVal = inv.roomNumber != null ? String(inv.roomNumber).trim() : '';
    var tableVal = inv.tableNumber != null ? String(inv.tableNumber).trim() : '';
    if (!tableVal && roomVal && /^table\\b/i.test(roomVal)) tableVal = roomVal;
    if (tableVal && tableVal !== '—') params.set('table', tableVal);
    else if (roomVal && roomVal !== '—' && !/^table\\b/i.test(roomVal)) params.set('room', roomVal);
    if (inv.guestName != null && String(inv.guestName).trim() !== '' && String(inv.guestName).trim() !== '—') params.set('guest', String(inv.guestName).trim());
    if (inv.bookingId != null && String(inv.bookingId).trim() !== '') params.set('booking', String(inv.bookingId).trim());
  }
  var q = params.toString();
  if (base.indexOf('?') >= 0) {
    var parts = base.split('?');
    return parts[0] + '?' + q;
  }
  return base + '?' + q;
}
function buildGuestRestaurantOrderUrl(inv) {
  return buildGuestOrderUrl('restaurant', inv);
}"""

GET_EFFECTIVE_QR_PAYLOAD_OLD = """function getEffectiveInvoiceQrPayload(inv) {
  if (inv && inv.qrTextOverride != null && inv.qrTextOverride !== undefined) return String(inv.qrTextOverride).trim();
  return getInvoiceQrPayload(inv);
}"""

GET_EFFECTIVE_QR_PAYLOAD_NEW = """function getEffectiveInvoiceQrPayload(inv) {
  if (inv && inv.qrTextOverride != null && inv.qrTextOverride !== undefined) {
    var override = String(inv.qrTextOverride).trim();
    if (!(guestQrRestaurantOrderEnabled() && isLegacyInvoiceQrPayload(override))) return override;
  }
  return getInvoiceQrPayload(inv);
}"""

BUILD_QR_CAPTION_OLD = """  var cap = custom ? 'Custom QR image' : (payload.length > 52 ? payload.slice(0, 49) + '…' : payload);"""

BUILD_QR_CAPTION_NEW = """  var cap = custom ? (typeof invoiceT === 'function' ? invoiceT('invoice.qrCustomImage', 'Custom QR image') : 'Custom QR image') : invoiceQrCaptionForPayload(payload);"""

REFRESH_QR_CAPTION_OLD = """  if (capEl) capEl.textContent = custom ? 'Custom QR image' : (payload.length > 52 ? payload.slice(0, 49) + '…' : payload);"""

REFRESH_QR_CAPTION_NEW = """  if (capEl) capEl.textContent = custom ? (typeof invoiceT === 'function' ? invoiceT('invoice.qrCustomImage', 'Custom QR image') : 'Custom QR image') : invoiceQrCaptionForPayload(payload);"""

ENSURE_GUEST_SETTING_V1 = """(function ensureGuestQrOrderSettingDefault() {
  try {
    if (typeof settings !== 'undefined' && settings && settings.invoiceQrIncludeRestaurantOrder === undefined) {
      settings.invoiceQrIncludeRestaurantOrder = true;
      if (typeof save === 'function') save('settings', settings);
    }
  } catch (e) {}
})();"""

ENSURE_GUEST_SETTING_V2 = """(function ensureGuestQrOrderSettingDefault() {
  try {
    var mk = (typeof DB_KEY !== 'undefined' ? DB_KEY : 'hotel_mgr_') + 'guestQrOrderForceEnabledV2';
    var done = false;
    try { done = String(localStorage.getItem(mk) || '') === '1'; } catch (e) {}
    if (typeof settings !== 'undefined' && settings) {
      if (settings.invoiceQrIncludeRestaurantOrder === undefined || !done) {
        settings.invoiceQrIncludeRestaurantOrder = true;
        if (typeof save === 'function') save('settings', settings);
      }
      if (!done) {
        try { localStorage.setItem(mk, '1'); } catch (e) {}
        if (typeof isAndroid !== 'undefined' && isAndroid) {
          try { HotelDB.saveSetting('guestQrOrderForceEnabledV2', '1'); } catch (e) {}
        }
      }
    }
  } catch (e) {}
})();"""

UPDATE_QR_PREVIEW_OLD = """  var payload = getInvoiceQrPayload({ invoiceNumber: 'INV-PREVIEW', paymentTransactionId: 'TXN-PREVIEW', grandTotal: 0 });"""

UPDATE_QR_PREVIEW_NEW = """  var payload = getInvoiceQrPayload({ invoiceNumber: 'INV-PREVIEW', paymentTransactionId: 'TXN-PREVIEW', grandTotal: 0, roomNumber: '101', guestName: 'Guest', bookingId: 'BK-PREVIEW' });"""

SETTINGS_QR_DETAILS_OLD = """        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
          <input type="checkbox" id="sInvoiceQrDetails" ${(s.invoiceQrIncludeDetails===false||s.invoiceQrIncludeDetails==='0'||s.invoiceQrIncludeDetails===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          Include invoice number &amp; total in QR
        </label>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">Generated QR appears on each invoice. Upload a custom QR image below to override.</p>"""

SETTINGS_QR_DETAILS_V1 = """        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
          <input type="checkbox" id="sInvoiceQrGuestOrder" ${(s.invoiceQrIncludeRestaurantOrder===false||s.invoiceQrIncludeRestaurantOrder==='0'||s.invoiceQrIncludeRestaurantOrder===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          QR opens guest restaurant order (scan to order food)
        </label>
        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
          <input type="checkbox" id="sInvoiceQrDetails" ${(s.invoiceQrIncludeDetails===false||s.invoiceQrIncludeDetails==='0'||s.invoiceQrIncludeDetails===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          Include invoice number &amp; total in QR (when guest order QR is off)
        </label>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">When guest order is on, the QR links to the restaurant menu for room/table ordering. Optional custom URL above is used as the site base when it starts with http.</p>"""

SETTINGS_QR_DETAILS_V2 = """        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
          <input type="checkbox" id="sInvoiceQrGuestOrder" ${(s.invoiceQrIncludeRestaurantOrder===false||s.invoiceQrIncludeRestaurantOrder==='0'||s.invoiceQrIncludeRestaurantOrder===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          QR opens guest restaurant order (scan to order food)
        </label>
        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;opacity:0.85;">
          <input type="checkbox" id="sInvoiceQrDetails" ${(s.invoiceQrIncludeDetails===false||s.invoiceQrIncludeDetails==='0'||s.invoiceQrIncludeDetails===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          Include invoice number &amp; total in QR (only when guest order QR is off)
        </label>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">When guest order is on, invoice QR codes link to the restaurant menu (room/guest from the invoice). Press Ctrl+F5 after updates if the QR still shows old invoice text.</p>"""

SAVE_SETTINGS_QR_OLD = """  if (document.getElementById('sInvoiceQrText')) settings.invoiceQrText = document.getElementById('sInvoiceQrText').value.trim();
  if (document.getElementById('sInvoiceQrDetails')) settings.invoiceQrIncludeDetails = document.getElementById('sInvoiceQrDetails').checked;
  settings.maxGuests = parseInt(document.getElementById('sMaxG').value)||3;"""

SAVE_SETTINGS_QR_NEW = """  if (document.getElementById('sInvoiceQrText')) settings.invoiceQrText = document.getElementById('sInvoiceQrText').value.trim();
  if (document.getElementById('sInvoiceQrGuestOrder')) settings.invoiceQrIncludeRestaurantOrder = document.getElementById('sInvoiceQrGuestOrder').checked;
  if (document.getElementById('sInvoiceQrDetails')) settings.invoiceQrIncludeDetails = document.getElementById('sInvoiceQrDetails').checked;
  settings.maxGuests = parseInt(document.getElementById('sMaxG').value)||3;"""

LOGIN_OVERLAY_END = """    </div>
  </div>
  <script>
  /* Before nisha1. ?newsetup=1 = clear setup only (keeps data). If appDataEpoch in storage differs from app-setup-version meta, full wipe (upgrade deploy gate). If epoch was never set, only stamp epoch — do not wipe (first load / just after Create Account). */"""

GUEST_OVERLAY_HTML = """    </div>
  </div>

  <div id="guestRestOrderOverlay" class="guest-rest-order-overlay hidden" aria-hidden="true">
    <div class="guest-rest-order-shell">
      <header class="guest-rest-order-hd">
        <div>
          <h1 id="guestRestOrderTitle">Restaurant order</h1>
          <p id="guestRestOrderSub" class="guest-rest-order-sub"></p>
        </div>
        <button type="button" class="guest-rest-order-close" id="guestRestOrderCloseBtn" aria-label="Close">&times;</button>
      </header>
      <div id="guestRestOrderBody" class="guest-rest-order-body"></div>
    </div>
  </div>
  <script>
  /* Before nisha1. ?newsetup=1 = clear setup only (keeps data). If appDataEpoch in storage differs from app-setup-version meta, full wipe (upgrade deploy gate). If epoch was never set, only stamp epoch — do not wipe (first load / just after Create Account). */"""

INIT_AUTOLOGIN_OLD = """(function initAutologinIfSetupComplete() {
  if (typeof hotelIsSetupComplete === 'function' && !hotelIsSetupComplete()) { return; }"""

INIT_AUTOLOGIN_NEW = """(function initAutologinIfSetupComplete() {
  if (typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl()) { return; }
  if (typeof tryBootGuestRestaurantOrder === 'function' && tryBootGuestRestaurantOrder()) { return; }
  if (typeof hotelIsSetupComplete === 'function' && !hotelIsSetupComplete()) { return; }"""

GUEST_ORDER_JS = """
/* HRMM guest QR restaurant order */
var guestRestCart = [];
var guestRestMenuFilter = 'All';
var guestOrderMenuSearch = '';
var guestRestCtx = { room: '', guest: '', booking: '', table: '', orderNum: '' };
var guestRestSubmitted = false;
"""

GUEST_ORDER_MENU_HELPERS = """
function guestRestAttrEsc(s) {
  if (typeof escAttr === 'function') return escAttr(s);
  return guestRestEsc(s);
}
function guestRestProductImageUrl(item, isStore) {
  if (!item) return '';
  var imgU = item.imageUrl != null ? String(item.imageUrl).trim() : '';
  if (imgU) return imgU;
  if (!isStore && item.image != null && String(item.image).trim()) return String(item.image).trim();
  if (isStore && item.image != null && /^https?:\\/\\//i.test(String(item.image))) return String(item.image).trim();
  return '';
}
function guestRestItemImageBlock(item, isStore) {
  var imgU = guestRestProductImageUrl(item, !!isStore);
  var ico = isStore
    ? (typeof getStoreItemDisplayIcon === 'function' ? getStoreItemDisplayIcon(item) : '\\uD83D\\uDED2')
    : (typeof getMenuItemDisplayIcon === 'function' ? getMenuItemDisplayIcon(item) : '\\uD83C\\uDF7D\\uFE0F');
  if (imgU) {
    return '<div class="grmc-img" aria-hidden="true"><img src="' + guestRestAttrEsc(imgU) + '" alt="" loading="lazy" decoding="async" onerror="this.parentNode.classList.add(\\'grmc-img-err\\');this.remove();" /><span class="grmc-img-ico">' + ico + '</span></div>';
  }
  return '<div class="grmc-img grmc-img-ph" aria-hidden="true">' + ico + '</div>';
}
function guestRestMenuCardHtml(item, idEsc, addFn, isStore) {
  var desc = item.description && String(item.description).trim();
  var descHtml = desc ? '<span class="grmc-desc">' + guestRestEsc(desc.length > 52 ? desc.slice(0, 49) + '\\u2026' : desc) + '</span>' : '';
  return '<button type="button" class="guest-rest-menu-card" onclick="' + addFn + '(\\'' + idEsc + '\\')">' +
    guestRestItemImageBlock(item, isStore) +
    '<span class="grmc-body"><span class="grmc-name">' + guestRestEsc(item.name) + '</span>' +
    '<span class="grmc-meta">' + guestRestEsc(item.category || '') + '</span>' +
    descHtml +
    '<span class="grmc-price">' + fmt$(item.price) + '</span></span></button>';
}
function guestRestMenuMatchesSearch(item, q) {
  if (!q) return true;
  q = String(q).toLowerCase();
  var hay = (String(item.name || '') + ' ' + String(item.category || '') + ' ' + String(item.description || '')).toLowerCase();
  return hay.indexOf(q) >= 0;
}
window.guestRestScrollToCart = function() {
  var el = document.getElementById('guestRestCartPanel');
  if (el && el.scrollIntoView) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
};
function guestRestMobileBarHtml(cartLen, grandTotal, submitFn, submitLabel, canSubmit) {
  if (!cartLen) return '';
  return '<div class="guest-rest-mobile-bar">' +
    '<button type="button" class="guest-rest-mobile-bar-main" onclick="guestRestScrollToCart()">' +
      '<span class="guest-rest-mobile-bar-count">' + cartLen + ' item' + (cartLen === 1 ? '' : 's') + '</span>' +
      '<span class="guest-rest-mobile-bar-total">' + fmt$(grandTotal) + '</span>' +
      '<span class="guest-rest-mobile-bar-hint">View cart</span>' +
    '</button>' +
    '<button type="button" class="btn btn-primary guest-rest-mobile-bar-go" ' + (canSubmit ? '' : 'disabled') + ' onclick="' + submitFn + '()">' + submitLabel + '</button>' +
  '</div>';
}
"""

CSS = """
    /* HRMM guest QR restaurant order */
    .guest-rest-order-overlay { position: fixed; inset: 0; z-index: 10050; background: var(--bg, #f4f6f9); overflow: auto; -webkit-overflow-scrolling: touch; }
    .guest-rest-order-overlay.hidden { display: none; }
    body.guest-rest-order-mode { overflow: hidden; }
    body.guest-rest-order-mode #app,
    body.guest-rest-order-mode #sidebar,
    body.guest-rest-order-mode #topbar,
    body.guest-rest-order-mode #bottomNav { display: none !important; }
    .guest-rest-order-shell { max-width: 960px; margin: 0 auto; min-height: 100dvh; display: flex; flex-direction: column; padding: max(0.5rem, env(safe-area-inset-top, 0px)) 0.75rem max(1rem, env(safe-area-inset-bottom, 8px)); box-sizing: border-box; }
    .guest-rest-order-hd { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.75rem; padding: 0.5rem 0 0.75rem; border-bottom: 1px solid var(--border); margin-bottom: 0.75rem; }
    .guest-rest-order-hd h1 { margin: 0; font-size: 1.15rem; line-height: 1.25; }
    .guest-rest-order-sub { margin: 0.25rem 0 0; font-size: 0.82rem; color: var(--text-light); line-height: 1.35; }
    .guest-rest-order-close { border: none; background: transparent; font-size: 1.75rem; line-height: 1; cursor: pointer; color: var(--text-light); padding: 0.15rem 0.35rem; }
    .guest-rest-order-body { flex: 1; }
    .guest-rest-layout { display: grid; grid-template-columns: 1fr; gap: 0.85rem; }
    @media (min-width: 768px) { .guest-rest-layout { grid-template-columns: 1.2fr 0.8fr; align-items: start; } }
    .guest-rest-panel { background: var(--card-bg, #fff); border: 1px solid var(--border); border-radius: 12px; padding: 0.85rem; }
    .guest-rest-panel h2 { margin: 0 0 0.65rem; font-size: 1rem; display: flex; align-items: center; gap: 0.35rem; }
    .guest-rest-count { font-size: 0.75rem; background: var(--primary); color: #fff; border-radius: 999px; padding: 0.1rem 0.45rem; }
    .guest-rest-tabs { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.65rem; }
    .guest-rest-search { margin-bottom: 0.65rem; }
    .guest-rest-search input { width: 100%; min-height: 42px; border-radius: 10px; }
    .guest-rest-menu-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.55rem; }
    @media (min-width: 480px) { .guest-rest-menu-grid { grid-template-columns: repeat(3, 1fr); gap: 0.65rem; } }
    @media (min-width: 768px) { .guest-rest-menu-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (min-width: 900px) { .guest-rest-menu-grid { grid-template-columns: repeat(3, 1fr); } }
    .guest-rest-menu-card { display: flex; flex-direction: column; align-items: stretch; text-align: left; gap: 0; border: 1px solid var(--border); border-radius: 12px; padding: 0; background: var(--card-bg, #fff); cursor: pointer; overflow: hidden; min-height: 0; }
    .guest-rest-menu-card:active { transform: scale(0.98); }
    .guest-rest-menu-card .grmc-img { position: relative; width: 100%; aspect-ratio: 4 / 3; background: linear-gradient(180deg, #e8e8e8, #f5f5f5); display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .guest-rest-menu-card .grmc-img img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .guest-rest-menu-card .grmc-img .grmc-img-ico { position: absolute; right: 4px; bottom: 4px; font-size: 1.1rem; line-height: 1; z-index: 1; text-shadow: 0 0 4px #fff, 0 0 2px #fff; pointer-events: none; }
    .guest-rest-menu-card .grmc-img.grmc-img-ph { font-size: 2rem; }
    .guest-rest-menu-card .grmc-img.grmc-img-err { min-height: 72px; }
    .guest-rest-menu-card .grmc-body { display: flex; flex-direction: column; gap: 0.1rem; padding: 0.5rem 0.55rem 0.6rem; flex: 1; }
    .grmc-name { font-weight: 600; font-size: 0.82rem; line-height: 1.25; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .grmc-meta { font-size: 0.68rem; color: var(--text-light); }
    .grmc-desc { font-size: 0.68rem; color: var(--text-light); line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .grmc-price { font-size: 0.88rem; color: var(--primary); font-weight: 700; margin-top: auto; padding-top: 0.15rem; }
    .guest-rest-cart-panel { scroll-margin-top: 72px; }
    .guest-rest-mobile-bar { display: none; }
    @media (max-width: 767px) {
      .guest-rest-mobile-bar { display: flex; position: fixed; left: 0; right: 0; bottom: 0; z-index: 10060; gap: 0.5rem; padding: 0.55rem 0.75rem calc(0.55rem + env(safe-area-inset-bottom, 0px)); background: rgba(255,255,255,0.96); border-top: 1px solid var(--border); box-shadow: 0 -4px 16px rgba(0,0,0,0.08); backdrop-filter: blur(8px); }
      body.dark-mode .guest-rest-mobile-bar { background: rgba(26,32,44,0.96); }
      .guest-rest-mobile-bar-main { flex: 1; display: flex; flex-direction: column; align-items: flex-start; justify-content: center; min-height: 44px; border: 1px solid var(--border); border-radius: 10px; background: var(--card-bg, #fff); padding: 0.35rem 0.65rem; cursor: pointer; text-align: left; }
      .guest-rest-mobile-bar-count { font-size: 0.72rem; color: var(--text-light); }
      .guest-rest-mobile-bar-total { font-size: 1rem; font-weight: 700; color: var(--primary); line-height: 1.2; }
      .guest-rest-mobile-bar-hint { font-size: 0.68rem; color: var(--text-light); }
      .guest-rest-mobile-bar-go { flex: 0 0 auto; min-width: 110px; min-height: 44px; justify-content: center; }
      .guest-rest-order-shell { padding-bottom: calc(5.5rem + env(safe-area-inset-bottom, 0px)); }
    }
    .guest-rest-empty, .guest-rest-cart-empty { grid-column: 1 / -1; text-align: center; color: var(--text-light); padding: 1.5rem 0.5rem; font-size: 0.88rem; }
    .guest-rest-cart-items { max-height: 240px; overflow: auto; margin-bottom: 0.65rem; }
    .guest-rest-cart-row { display: grid; grid-template-columns: 1fr auto auto auto; gap: 0.35rem; align-items: center; padding: 0.35rem 0; border-bottom: 1px solid var(--border); font-size: 0.85rem; }
    .guest-rest-qty { display: inline-flex; align-items: center; gap: 0.2rem; }
    .guest-rest-qty button { width: 28px; height: 28px; border: 1px solid var(--border); border-radius: 6px; background: var(--card-bg, #fff); cursor: pointer; }
    .guest-rest-remove { border: none; background: transparent; color: var(--danger, #c62828); cursor: pointer; font-size: 1rem; }
    .guest-rest-totals { font-size: 0.85rem; margin-bottom: 0.65rem; }
    .guest-rest-totals > div { display: flex; justify-content: space-between; padding: 0.2rem 0; }
    .guest-rest-grand { font-weight: 700; font-size: 0.95rem; border-top: 1px solid var(--border); margin-top: 0.25rem; padding-top: 0.35rem !important; }
    .guest-rest-notes-label { display: block; font-size: 0.78rem; font-weight: 600; margin-bottom: 0.65rem; }
    .guest-rest-notes-label input { margin-top: 0.25rem; }
    .guest-rest-submit { width: 100%; justify-content: center; min-height: 44px; }
    .guest-rest-success { text-align: center; padding: 2.5rem 1rem; }
    .guest-rest-success-icon { width: 64px; height: 64px; border-radius: 50%; background: #e8f5e9; color: #2e7d32; font-size: 2rem; line-height: 64px; margin: 0 auto 1rem; }
    .guest-rest-success h2 { margin: 0 0 0.5rem; }
    .guest-rest-success p { color: var(--text-light); margin: 0 0 1rem; line-height: 1.45; }
    .bottom-nav-item[data-bnav="guestorder"] .bnav-label { max-width: 3.5rem; }
    .guest-order-qr-modal { max-width: 420px; }
    .guest-order-qr-lead { font-size: 0.85rem; color: var(--text-light); margin: 0 0 0.75rem; line-height: 1.45; }
    .guest-order-qr-preview { text-align: center; margin: 0.75rem 0 1rem; padding: 0.65rem; border: 1px dashed var(--border); border-radius: 10px; background: rgba(255,255,255,0.5); }
    body.dark-mode .guest-order-qr-preview { background: rgba(0,0,0,0.15); }
    .guest-order-qr-actions { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
    .guest-order-qr-actions .btn { flex: 1 1 140px; justify-content: center; min-height: 42px; }
    .invoice-guest-order-qrs { display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center; margin: 0.75rem 0 1rem; }
    .invoice-guest-order-qrs .invoice-guest-order-qr { flex: 1 1 140px; max-width: 220px; }
    /* __HRMM_GUEST_QR_MARKER__ */
"""

BOTTOM_NAV_DOCS_BTN = """    <button class="bottom-nav-item" data-bnav="documentation" onclick="bnav('documentation')"><span class="bnav-icon">&#128214;</span><span class="bnav-label" data-i18n="bnav.documentation">Docs</span></button>"""

BOTTOM_NAV_WITH_GUEST_ORDER = """    <button class="bottom-nav-item" data-bnav="guestorder-rest" onclick="openGuestOrderQrModal('restaurant')"><span class="bnav-icon">&#127869;</span><span class="bnav-label" data-i18n="bnav.guestOrderRest">RESTAURANT QR</span></button>
    <button class="bottom-nav-item" data-bnav="guestorder-mart" onclick="openGuestOrderQrModal('minimart')"><span class="bnav-icon">&#128722;</span><span class="bnav-label" data-i18n="bnav.guestOrderMart">MINIMart QR</span></button>
    <button class="bottom-nav-item" data-bnav="documentation" onclick="bnav('documentation')"><span class="bnav-icon">&#128214;</span><span class="bnav-label" data-i18n="bnav.documentation">Docs</span></button>"""

BOTTOM_NAV_SINGLE_GUEST_ORDER = """    <button class="bottom-nav-item" data-bnav="guestorder" onclick="openGuestOrderQrModal()"><span class="bnav-icon">&#128279;</span><span class="bnav-label" data-i18n="bnav.guestOrder">Order QR</span></button>
    <button class="bottom-nav-item" data-bnav="documentation" onclick="bnav('documentation')"><span class="bnav-icon">&#128214;</span><span class="bnav-label" data-i18n="bnav.documentation">Docs</span></button>"""

BNAV_FN_OLD = """window.bnav = function(page) {
  if (currentRole === 'Kitchen' && page !== 'restaurant' && page !== 'documentation') {"""

BNAV_FN_GUEST_SINGLE = """window.bnav = function(page) {
  if (page === 'guestorder') {
    if (typeof openGuestOrderQrModal === 'function') openGuestOrderQrModal();
    return;
  }
  if (currentRole === 'Kitchen' && page !== 'restaurant' && page !== 'documentation' && page !== 'guestorder') {"""

BNAV_FN_NEW = """window.bnav = function(page) {
  if (page === 'guestorder' || page === 'guestorder-rest') {
    if (typeof openGuestOrderQrModal === 'function') openGuestOrderQrModal('restaurant');
    return;
  }
  if (page === 'guestorder-mart') {
    if (typeof openGuestOrderQrModal === 'function') openGuestOrderQrModal('minimart');
    return;
  }
  if (currentRole === 'Kitchen' && page !== 'restaurant' && page !== 'documentation' && page !== 'guestorder' && page !== 'guestorder-rest' && page !== 'guestorder-mart') {"""

RBAC_BNAV_SETTINGS_TAIL = """  var bnavSettings = document.querySelector('#bottomNav [data-bnav="settings"]');
  if (bnavSettings) {
    bnavSettings.style.display = canSettings ? '' : 'none';
  }
}"""

RBAC_BNAV_SETTINGS_GUEST = """  var bnavSettings = document.querySelector('#bottomNav [data-bnav="settings"]');
  if (bnavSettings) {
    bnavSettings.style.display = canSettings ? '' : 'none';
  }
  var bnavGuestOrderRest = document.querySelector('#bottomNav [data-bnav="guestorder-rest"]');
  if (bnavGuestOrderRest) {
    var canRestQr = allowed === null || (Array.isArray(allowed) && allowed.indexOf('restaurant') >= 0);
    bnavGuestOrderRest.style.display = canRestQr ? '' : 'none';
  }
  var bnavGuestOrderMart = document.querySelector('#bottomNav [data-bnav="guestorder-mart"]');
  if (bnavGuestOrderMart) {
    var canMartQr = allowed === null || (Array.isArray(allowed) && allowed.indexOf('minimart') >= 0);
    bnavGuestOrderMart.style.display = canMartQr ? '' : 'none';
  }
  var bnavGuestOrder = document.querySelector('#bottomNav [data-bnav="guestorder"]');
  if (bnavGuestOrder) {
    var canGuestOrder = allowed === null || (Array.isArray(allowed) && (allowed.indexOf('restaurant') >= 0 || allowed.indexOf('minimart') >= 0));
    bnavGuestOrder.style.display = canGuestOrder ? '' : 'none';
  }
}"""

RBAC_BNAV_SETTINGS_GUEST_SINGLE = """  var bnavSettings = document.querySelector('#bottomNav [data-bnav="settings"]');
  if (bnavSettings) {
    bnavSettings.style.display = canSettings ? '' : 'none';
  }
  var bnavGuestOrder = document.querySelector('#bottomNav [data-bnav="guestorder"]');
  if (bnavGuestOrder) {
    var canGuestOrder = allowed === null || (Array.isArray(allowed) && (allowed.indexOf('restaurant') >= 0 || allowed.indexOf('minimart') >= 0));
    bnavGuestOrder.style.display = canGuestOrder ? '' : 'none';
  }
}"""

I18N_BNAV_OLD = """  "bnav": {
    "dashboard": "Dashboard",
    "pos": "POS",
    "bookings": "Bookings",
    "menu": "Menu",
    "documentation": "Docs"
  },"""

I18N_BNAV_NEW = """  "bnav": {
    "dashboard": "Dashboard",
    "pos": "POS",
    "bookings": "Bookings",
    "guestOrder": "Order QR",
    "guestOrderRest": "RESTAURANT QR",
    "guestOrderMart": "MINIMart QR",
    "menu": "Menu",
    "documentation": "Docs"
  },"""

GUEST_ORDER_STAFF_JS_V3 = """
var guestOrderQrStaffCtx = { mode: 'room', room: '', guest: '', booking: '', table: '' };
function guestOrderQrInvFromCtx(ctx) {
  ctx = ctx || guestOrderQrStaffCtx;
  return {
    roomNumber: ctx.room || '',
    guestName: ctx.guest || '',
    bookingId: ctx.booking || '',
    tableNumber: ctx.table || ''
  };
}
function guestOrderQrBuildUrl(ctx) {
  return buildGuestRestaurantOrderUrl(guestOrderQrInvFromCtx(ctx));
}
function guestOrderQrRefreshPreview() {
  var img = document.getElementById('guestOrderQrImg');
  var cap = document.getElementById('guestOrderQrCaption');
  var link = document.getElementById('guestOrderQrLink');
  var url = guestOrderQrBuildUrl(guestOrderQrStaffCtx);
  if (img) img.src = url ? buildInvoiceQrImageUrl(url) : '';
  if (cap) cap.textContent = url ? invoiceQrCaptionForPayload(url) : 'Add customer details';
  if (link) link.value = url || '';
}
window.guestOrderQrSetMode = function(mode) {
  guestOrderQrStaffCtx.mode = mode === 'walkin' ? 'walkin' : 'room';
  if (typeof openGuestOrderQrModal === 'function') openGuestOrderQrModal(true);
};
window.guestOrderQrPickBooking = function(val) {
  guestOrderQrStaffCtx.room = '';
  guestOrderQrStaffCtx.guest = '';
  guestOrderQrStaffCtx.booking = '';
  if (val) {
    var b = (bookings || []).find(function(x) { return x && x.id === val; });
    if (b) {
      guestOrderQrStaffCtx.room = String(b.roomNumber || '');
      guestOrderQrStaffCtx.guest = String(b.guestName || '');
      guestOrderQrStaffCtx.booking = String(b.bookingId || '');
    }
  }
  guestOrderQrRefreshPreview();
};
window.guestOrderQrApplyWalkin = function() {
  var nameEl = document.getElementById('guestOrderQrWalkName');
  var tableEl = document.getElementById('guestOrderQrWalkTable');
  guestOrderQrStaffCtx.guest = nameEl ? nameEl.value.trim() : '';
  guestOrderQrStaffCtx.table = tableEl ? tableEl.value.trim() : '';
  guestOrderQrStaffCtx.room = '';
  guestOrderQrStaffCtx.booking = '';
  guestOrderQrRefreshPreview();
};
window.openGuestOrderQrModal = function() {
  var pickable = typeof getBookingsForGuestPicker === 'function' ? getBookingsForGuestPicker() : [];
  var opts = '<option value="">— Select room / guest —</option>';
  pickable.forEach(function(b) {
    if (!b) return;
    var sel = '';
    if (guestOrderQrStaffCtx.booking && String(b.bookingId) === String(guestOrderQrStaffCtx.booking)) sel = ' selected';
    opts += '<option value="' + escapeHtml(String(b.id)) + '"' + sel + '>' + escapeHtml(String(b.roomNumber) + ' — ' + String(b.guestName)) + '</option>';
  });
  var mode = guestOrderQrStaffCtx.mode || 'room';
  var html = '<div class="modal-hd"><h2>Customer order QR</h2><button type="button" class="modal-close" onclick="closeModal()">&times;</button></div>' +
    '<div class="modal-body guest-order-qr-modal">' +
    '<p class="guest-order-qr-lead">Create a QR code so a customer can order from the restaurant themselves (scan with phone).</p>' +
    '<div class="rest-order-type" style="margin-bottom:0.75rem;">' +
      '<button type="button" class="btn ' + (mode === 'room' ? 'btn-primary' : 'btn-outline') + '" onclick="guestOrderQrSetMode(\\'room\\')">Room guest</button>' +
      '<button type="button" class="btn ' + (mode === 'walkin' ? 'btn-primary' : 'btn-outline') + '" onclick="guestOrderQrSetMode(\\'walkin\\')">Walk-in / table</button>' +
    '</div>';
  if (mode === 'room') {
    html += '<div class="form-group"><label>Guest / room</label><select class="form-control" id="guestOrderQrBookingPick" onchange="guestOrderQrPickBooking(this.value)">' + opts + '</select></div>';
  } else {
    html += '<div class="form-row"><div class="form-group"><label>Customer name</label><input type="text" class="form-control" id="guestOrderQrWalkName" value="' + escapeHtml(guestOrderQrStaffCtx.guest) + '" placeholder="Customer name" oninput="guestOrderQrApplyWalkin()"></div>' +
      '<div class="form-group"><label>Table</label><input type="text" class="form-control" id="guestOrderQrWalkTable" value="' + escapeHtml(guestOrderQrStaffCtx.table) + '" placeholder="Table 1" oninput="guestOrderQrApplyWalkin()"></div></div>';
  }
  html += '<div class="guest-order-qr-preview"><img id="guestOrderQrImg" class="invoice-qr-img" alt="Order QR code">' +
    '<div id="guestOrderQrCaption" class="invoice-qr-caption">Scan to order from restaurant</div></div>' +
    '<div class="form-group"><label>Order link</label><input type="text" class="form-control" id="guestOrderQrLink" readonly onclick="this.select()"></div>' +
    '<div class="guest-order-qr-actions">' +
      '<button type="button" class="btn btn-primary" onclick="guestOrderQrOpenCustomerScreen()">Open order screen</button>' +
      '<button type="button" class="btn btn-outline" onclick="guestOrderQrCopyLink()">Copy link</button>' +
    '</div></div>';
  openModal(html);
  guestOrderQrRefreshPreview();
};
window.guestOrderQrCopyLink = function() {
  var url = guestOrderQrBuildUrl(guestOrderQrStaffCtx);
  if (!url) { if (typeof toast === 'function') toast('Add customer details first'); return; }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url).then(function() { if (typeof toast === 'function') toast('Link copied'); }).catch(function() {
      var el = document.getElementById('guestOrderQrLink');
      if (el) { el.value = url; el.select(); try { document.execCommand('copy'); if (typeof toast === 'function') toast('Link copied'); } catch (e) {} }
    });
  } else {
    var el = document.getElementById('guestOrderQrLink');
    if (el) { el.value = url; el.select(); try { document.execCommand('copy'); if (typeof toast === 'function') toast('Link copied'); } catch (e) {} }
  }
};
window.guestOrderQrOpenCustomerScreen = function() {
  var url = guestOrderQrBuildUrl(guestOrderQrStaffCtx);
  if (!url) { if (typeof toast === 'function') toast('Add customer details first'); return; }
  closeModal();
  showGuestRestaurantOrderScreen({
    room: guestOrderQrStaffCtx.room || '',
    guest: guestOrderQrStaffCtx.guest || '',
    booking: guestOrderQrStaffCtx.booking || '',
    table: guestOrderQrStaffCtx.table || ''
  });
};
"""

GUEST_ORDER_STAFF_JS = """
var guestOrderQrStaffCtx = { dept: 'restaurant', mode: 'room', room: '', guest: '', booking: '', table: '', orderNum: '' };
function guestOrderQrInvFromCtx(ctx) {
  ctx = ctx || guestOrderQrStaffCtx;
  return { orderNum: ctx.orderNum || '' };
}
function guestOrderQrBuildUrl(ctx) {
  ctx = ctx || guestOrderQrStaffCtx;
  return buildGuestOrderUrl(ctx.dept === 'minimart' ? 'minimart' : 'restaurant', guestOrderQrInvFromCtx(ctx));
}
function guestOrderQrListRooms() {
  var pickable = typeof getBookingsForGuestPicker === 'function' ? getBookingsForGuestPicker() : [];
  var rooms = {};
  pickable.forEach(function(b) {
    if (!b) return;
    var r = String(b.roomNumber != null ? b.roomNumber : '').trim();
    if (r && r !== '—') rooms[r] = true;
  });
  return Object.keys(rooms).sort(function(a, b) {
    var na = parseInt(a, 10), nb = parseInt(b, 10);
    if (!isNaN(na) && !isNaN(nb) && String(na) === a && String(nb) === b) return na - nb;
    return a.localeCompare(b);
  });
}
function guestOrderQrListBookingsForRoom(room) {
  var pickable = typeof getBookingsForGuestPicker === 'function' ? getBookingsForGuestPicker() : [];
  room = String(room || '').trim();
  if (!room) return [];
  return pickable.filter(function(b) {
    if (!b) return false;
    return String(b.roomNumber != null ? b.roomNumber : '').trim() === room;
  });
}
function guestOrderQrListTables() {
  if (typeof restSortedTables === 'function') return restSortedTables();
  try { restaurantTables = load('restaurantTables', restaurantTables); } catch (e) {}
  if (!Array.isArray(restaurantTables)) return [];
  return restaurantTables.slice();
}
function guestOrderQrHasCustomerContext(ctx) {
  ctx = ctx || guestOrderQrStaffCtx;
  var n = parseInt(String(ctx.orderNum || '').trim(), 10);
  return n >= 1 && n <= 60;
}
function guestOrderQrMissingContextHint(ctx) {
  return 'Select order number first';
}
function guestOrderQrRefreshPreview() {
  var img = document.getElementById('guestOrderQrImg');
  var cap = document.getElementById('guestOrderQrCaption');
  var link = document.getElementById('guestOrderQrLink');
  var url = guestOrderQrHasCustomerContext() ? guestOrderQrBuildUrl(guestOrderQrStaffCtx) : '';
  if (img) img.src = url ? buildInvoiceQrImageUrl(url) : '';
  if (cap) cap.textContent = url ? invoiceQrCaptionForPayload(url) : 'Select order number';
  if (link) link.value = url || '';
}
window.guestOrderQrSetDept = function(dept) {
  guestOrderQrStaffCtx.dept = dept === 'minimart' ? 'minimart' : 'restaurant';
  guestOrderQrStaffCtx.mode = 'room';
  guestOrderQrStaffCtx.room = '';
  guestOrderQrStaffCtx.guest = '';
  guestOrderQrStaffCtx.booking = '';
  guestOrderQrStaffCtx.table = '';
  guestOrderQrStaffCtx.orderNum = '';
  if (typeof openGuestOrderQrModal === 'function') openGuestOrderQrModal(true);
};
window.guestOrderQrSetMode = function(mode) {
  guestOrderQrStaffCtx.mode = mode === 'walkin' ? 'walkin' : 'room';
  if (typeof openGuestOrderQrModal === 'function') openGuestOrderQrModal(true);
};
window.guestOrderQrPickRoom = function(room) {
  guestOrderQrStaffCtx.room = room ? String(room).trim() : '';
  guestOrderQrStaffCtx.guest = '';
  guestOrderQrStaffCtx.booking = '';
  var list = guestOrderQrListBookingsForRoom(guestOrderQrStaffCtx.room);
  if (list.length === 1) {
    guestOrderQrStaffCtx.guest = String(list[0].guestName || '');
    guestOrderQrStaffCtx.booking = String(list[0].bookingId || list[0].id || '');
  }
  if (typeof openGuestOrderQrModal === 'function') openGuestOrderQrModal(true);
  else guestOrderQrRefreshPreview();
};
window.guestOrderQrPickGuestBooking = function(bookingRowId) {
  guestOrderQrStaffCtx.guest = '';
  guestOrderQrStaffCtx.booking = '';
  if (bookingRowId) {
    var b = (bookings || []).find(function(x) { return x && x.id === bookingRowId; });
    if (b) {
      guestOrderQrStaffCtx.room = String(b.roomNumber || guestOrderQrStaffCtx.room || '');
      guestOrderQrStaffCtx.guest = String(b.guestName || '');
      guestOrderQrStaffCtx.booking = String(b.bookingId || b.id || '');
    }
  }
  guestOrderQrRefreshPreview();
};
window.guestOrderQrPickTable = function(val) {
  guestOrderQrStaffCtx.table = val ? String(val).trim() : '';
  guestOrderQrStaffCtx.room = '';
  guestOrderQrStaffCtx.booking = '';
  guestOrderQrRefreshPreview();
};
window.guestOrderQrApplyWalkin = function() {
  var nameEl = document.getElementById('guestOrderQrWalkName');
  guestOrderQrStaffCtx.guest = nameEl ? nameEl.value.trim() : '';
  guestOrderQrStaffCtx.room = '';
  guestOrderQrStaffCtx.booking = '';
  guestOrderQrRefreshPreview();
};
window.guestOrderQrPickOrderNum = function(val) {
  guestOrderQrStaffCtx.orderNum = val ? String(val).trim() : '';
  guestOrderQrRefreshPreview();
};
window.openGuestOrderQrModal = function(deptOrKeepState) {
  if (!guestOrderQrStaffCtx || typeof guestOrderQrStaffCtx !== 'object') {
    guestOrderQrStaffCtx = { dept: 'restaurant', mode: 'room', room: '', guest: '', booking: '', table: '', orderNum: '' };
  }
  if (deptOrKeepState === 'restaurant' || deptOrKeepState === 'minimart') {
    guestOrderQrStaffCtx.dept = deptOrKeepState;
    guestOrderQrStaffCtx.mode = 'room';
    guestOrderQrStaffCtx.room = '';
    guestOrderQrStaffCtx.guest = '';
    guestOrderQrStaffCtx.booking = '';
    guestOrderQrStaffCtx.table = '';
    guestOrderQrStaffCtx.orderNum = '';
  } else if (deptOrKeepState !== true) {
    guestOrderQrStaffCtx = { dept: guestOrderQrStaffCtx.dept || 'restaurant', mode: 'room', room: '', guest: '', booking: '', table: '', orderNum: '' };
  }
  var dept = guestOrderQrStaffCtx.dept === 'minimart' ? 'minimart' : 'restaurant';
  var mode = guestOrderQrStaffCtx.mode || 'room';
  var deptLabel = dept === 'minimart' ? 'Mini-Mart' : 'Restaurant';
  var rooms = guestOrderQrListRooms();
  var roomOpts = '<option value="">— Select room —</option>';
  rooms.forEach(function(r) {
    var sel = guestOrderQrStaffCtx.room === r ? ' selected' : '';
    roomOpts += '<option value="' + escapeHtml(r) + '"' + sel + '>' + escapeHtml(r) + '</option>';
  });
  var guestList = guestOrderQrStaffCtx.room ? guestOrderQrListBookingsForRoom(guestOrderQrStaffCtx.room) : [];
  var guestOpts = '<option value="">— Select guest —</option>';
  guestList.forEach(function(b) {
    var bid = String(b.bookingId || b.id || '');
    var sel = guestOrderQrStaffCtx.booking && bid === String(guestOrderQrStaffCtx.booking) ? ' selected' : '';
    guestOpts += '<option value="' + escapeHtml(String(b.id)) + '"' + sel + '>' + escapeHtml(String(b.guestName || 'Guest')) + '</option>';
  });
  var tables = guestOrderQrListTables();
  var tableOpts = '<option value="">— Select table —</option>';
  var knownTable = false;
  tables.forEach(function(t) {
    var lab = t && t.label ? String(t.label).trim() : '';
    if (!lab) return;
    if (guestOrderQrStaffCtx.table === lab) knownTable = true;
    var sel = guestOrderQrStaffCtx.table === lab ? ' selected' : '';
    tableOpts += '<option value="' + escapeHtml(lab) + '"' + sel + '>' + escapeHtml(lab) + '</option>';
  });
  if (guestOrderQrStaffCtx.table && !knownTable) {
    tableOpts += '<option value="' + escapeHtml(guestOrderQrStaffCtx.table) + '" selected>' + escapeHtml(guestOrderQrStaffCtx.table) + '</option>';
  }
  var orderNumOpts = '<option value="">— Select order number —</option>';
  for (var on = 1; on <= 60; on++) {
    var onSel = String(guestOrderQrStaffCtx.orderNum) === String(on) ? ' selected' : '';
    orderNumOpts += '<option value="' + on + '"' + onSel + '>Order number ' + on + '</option>';
  }
  var leadText = 'Scan this QR so the customer can self-order from the ' + deptLabel.toLowerCase() + '. Pick an order number (1–60) below.';
  var html = '<div class="modal-hd"><h2>' + deptLabel + ' order QR</h2><button type="button" class="modal-close" onclick="closeModal()">&times;</button></div>' +
    '<div class="modal-body guest-order-qr-modal">' +
    '<p class="guest-order-qr-lead">' + leadText + '</p>' +
    '<div class="rest-order-type" style="margin-bottom:0.65rem;">' +
      '<button type="button" class="btn ' + (dept === 'restaurant' ? 'btn-primary' : 'btn-outline') + '" onclick="guestOrderQrSetDept(\\'restaurant\\')">Restaurant QR</button>' +
      '<button type="button" class="btn ' + (dept === 'minimart' ? 'btn-primary' : 'btn-outline') + '" onclick="guestOrderQrSetDept(\\'minimart\\')">Mini-Mart QR</button>' +
    '</div>' +
    '<div class="form-group"><label>Order number</label><select class="form-control" id="guestOrderQrOrderNumPick" onchange="guestOrderQrPickOrderNum(this.value)">' + orderNumOpts + '</select></div>';
  html += '<div class="guest-order-qr-preview"><img id="guestOrderQrImg" class="invoice-qr-img" alt="Order QR code">' +
    '<div id="guestOrderQrCaption" class="invoice-qr-caption">Scan to order</div></div>' +
    '<div class="form-group"><label>Order link</label><input type="text" class="form-control" id="guestOrderQrLink" readonly onclick="this.select()"></div>' +
    '<div class="guest-order-qr-actions">' +
      '<button type="button" class="btn btn-primary" onclick="guestOrderQrOpenCustomerScreen()">Open order screen</button>' +
      '<button type="button" class="btn btn-outline" onclick="guestOrderQrCopyLink()">Copy link</button>' +
    '</div></div>';
  openModal(html);
  guestOrderQrRefreshPreview();
};
window.guestOrderQrCopyLink = function() {
  var url = guestOrderQrBuildUrl(guestOrderQrStaffCtx);
  if (!url || !guestOrderQrHasCustomerContext()) { if (typeof toast === 'function') toast(guestOrderQrMissingContextHint()); return; }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url).then(function() { if (typeof toast === 'function') toast('Link copied'); }).catch(function() {
      var el = document.getElementById('guestOrderQrLink');
      if (el) { el.value = url; el.select(); try { document.execCommand('copy'); if (typeof toast === 'function') toast('Link copied'); } catch (e) {} }
    });
  } else {
    var el = document.getElementById('guestOrderQrLink');
    if (el) { el.value = url; el.select(); try { document.execCommand('copy'); if (typeof toast === 'function') toast('Link copied'); } catch (e) {} }
  }
};
window.guestOrderQrOpenCustomerScreen = function() {
  if (!guestOrderQrHasCustomerContext()) { if (typeof toast === 'function') toast(guestOrderQrMissingContextHint()); return; }
  closeModal();
  showGuestOrderScreen(guestOrderQrStaffCtx.dept === 'minimart' ? 'minimart' : 'restaurant', {
    room: guestOrderQrStaffCtx.room || '',
    guest: guestOrderQrStaffCtx.guest || '',
    booking: guestOrderQrStaffCtx.booking || '',
    table: guestOrderQrStaffCtx.table || '',
    orderNum: guestOrderQrStaffCtx.orderNum || ''
  });
};
"""

GUEST_ORDER_JS_BODY_V3_TAIL = """
function parseGuestRestaurantOrderParams() {
  var sp = (typeof window.hotelBootUrlParams === 'function') ? window.hotelBootUrlParams() : new URLSearchParams(typeof location !== 'undefined' && location.search ? location.search : '');
  if (sp.get('guestOrder') !== 'restaurant') return null;
  return {
    room: sp.get('room') || '',
    guest: sp.get('guest') || '',
    booking: sp.get('booking') || '',
    table: sp.get('table') || ''
  };
}
"""

GUEST_ORDER_JS_BODY = ENSURE_GUEST_SETTING_V2 + """
function ensureGuestRestaurantMenuLoaded() {
  try {
    if (typeof load === 'function') menuItems = load('menuItems', menuItems);
  } catch (e) {}
  if (!Array.isArray(menuItems) || !menuItems.length) {
    if (typeof defaultMenuItems !== 'undefined' && Array.isArray(defaultMenuItems) && defaultMenuItems.length) menuItems = defaultMenuItems.slice();
    else menuItems = [];
  }
  if (!Array.isArray(restaurantOrders)) restaurantOrders = [];
}
function ensureGuestRestaurantWorkPeriod() {
  try {
    if (typeof load === 'function') {
      workPeriods = load('workPeriods', workPeriods);
      if (!Array.isArray(workPeriods)) workPeriods = [];
    }
  } catch (e) {}
  var wp = typeof getActiveWorkPeriod === 'function' ? getActiveWorkPeriod('Restaurant') : null;
  if (wp) return wp;
  wp = { id: genId(), dept: 'Restaurant', startTime: new Date().toISOString(), endTime: null, openingCash: 0, closingCash: null, cashVariance: null, status: 'Open', userId: '', userName: 'Guest QR', closedBy: '' };
  if (!Array.isArray(workPeriods)) workPeriods = [];
  workPeriods.push(wp);
  try { if (typeof save === 'function') save('workPeriods', workPeriods); } catch (e) {}
  return wp;
}
function guestRestEsc(s) {
  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
""" + GUEST_ORDER_MENU_HELPERS + """
function renderGuestRestaurantOrder() {
  var body = document.getElementById('guestRestOrderBody');
  var sub = document.getElementById('guestRestOrderSub');
  var title = document.getElementById('guestRestOrderTitle');
  if (!body) return;
  ensureGuestRestaurantMenuLoaded();
  var hn = (settings && settings.hotelName) ? String(settings.hotelName) : 'Restaurant';
  if (title) title.textContent = hn + ' — Order food';
  if (sub) {
    var bits = [];
    if (guestRestCtx.orderNum) bits.push('Order number ' + guestRestCtx.orderNum);
    else {
      if (guestRestCtx.guest) bits.push(guestRestCtx.guest);
      if (guestRestCtx.room) bits.push('Room ' + guestRestCtx.room);
      if (guestRestCtx.table) bits.push(String(guestRestCtx.table));
      if (guestRestCtx.booking) bits.push('Booking ' + guestRestCtx.booking);
    }
    sub.textContent = bits.length ? bits.join(' · ') : 'Browse the menu and send your order to the kitchen';
  }
  if (guestRestSubmitted) {
    body.innerHTML = '<div class="guest-rest-success"><div class="guest-rest-success-icon" aria-hidden="true">✓</div><h2>Order sent!</h2><p>Your order was submitted to the kitchen. Staff will prepare it shortly.</p><button type="button" class="btn btn-primary" onclick="guestRestStartNewOrder()">Order more</button></div>';
    return;
  }
  var taxRate = parseFloat(settings && (settings.serviceTax || settings.taxRate)) || 7;
  var categories = ['All'].concat(typeof getMenuCategories === 'function' ? getMenuCategories() : []);
  var searchQ = String(guestOrderMenuSearch || '').trim();
  var searchHtml = '<div class="guest-rest-search"><input type="search" class="form-control" placeholder="Search menu…" value="' + guestRestEsc(searchQ) + '" oninput="guestOrderMenuSearch=this.value;renderGuestOrderScreen()" autocomplete="off"></div>';
  var tabs = '<div class="guest-rest-tabs">' + categories.map(function(c) {
    var lab = c === 'All' ? 'All' : c;
    return '<button type="button" class="btn btn-sm ' + (guestRestMenuFilter === c ? 'btn-primary' : 'btn-outline') + '" onclick="guestRestMenuFilter=\\'' + String(c).replace(/'/g, "\\\\'") + '\\';renderGuestRestaurantOrder()">' + guestRestEsc(lab) + '</button>';
  }).join('') + '</div>';
  var filtered = (guestRestMenuFilter === 'All' ? menuItems : menuItems.filter(function(m) { return m && m.category === guestRestMenuFilter; })).filter(function(m) {
    return m && m.available !== false && (typeof rowDataVisible !== 'function' || rowDataVisible(m)) && guestRestMenuMatchesSearch(m, searchQ);
  });
  var menuHtml = '<div class="guest-rest-menu-grid">';
  filtered.forEach(function(m) {
    var idEsc = String(m.id).replace(/'/g, "\\\\'");
    menuHtml += guestRestMenuCardHtml(m, idEsc, 'guestRestAddToCart', false);
  });
  if (!filtered.length) menuHtml += '<div class="guest-rest-empty">No menu items available right now.</div>';
  menuHtml += '</div>';
  var cartHtml = '';
  var subtotal = 0;
  guestRestCart.forEach(function(ci, idx) {
    var line = (parseFloat(ci.unitPrice) || 0) * (parseInt(ci.qty, 10) || 0);
    subtotal += line;
    cartHtml += '<div class="guest-rest-cart-row"><span>' + guestRestEsc(ci.name) + '</span><div class="guest-rest-qty"><button type="button" onclick="guestRestCartQty(' + idx + ',-1)">−</button><span>' + ci.qty + '</span><button type="button" onclick="guestRestCartQty(' + idx + ',1)">+</button></div><span>' + fmt$(line) + '</span><button type="button" class="guest-rest-remove" onclick="guestRestCartRemove(' + idx + ')">✕</button></div>';
  });
  if (!cartHtml) cartHtml = '<div class="guest-rest-cart-empty">Tap menu items to add them to your cart</div>';
  var tax = Math.round((subtotal * (taxRate / 100)) * 100) / 100;
  var grandTotal = Math.round((subtotal + tax) * 100) / 100;
  var canSend = guestRestCart.length > 0;
  var mobileBar = guestRestMobileBarHtml(guestRestCart.length, grandTotal, 'guestRestSubmitOrder', 'Send order', canSend);
  body.innerHTML =
    '<div class="guest-rest-layout">' +
      '<section class="guest-rest-panel"><h2>Menu</h2>' + searchHtml + tabs + menuHtml + '</section>' +
      '<section class="guest-rest-panel guest-rest-cart-panel" id="guestRestCartPanel"><h2>Your order <span class="guest-rest-count">' + guestRestCart.length + '</span></h2>' +
        '<div class="guest-rest-cart-items">' + cartHtml + '</div>' +
        '<div class="guest-rest-totals"><div><span>Subtotal</span><span>' + fmt$(subtotal) + '</span></div><div><span>Tax (' + taxRate + '%)</span><span>' + fmt$(tax) + '</span></div><div class="guest-rest-grand"><span>Total</span><span>' + fmt$(grandTotal) + '</span></div></div>' +
        '<label class="guest-rest-notes-label">Notes (optional)<input type="text" class="form-control" id="guestRestOrderNotes" placeholder="Allergies, preferences…"></label>' +
        '<button type="button" class="btn btn-primary guest-rest-submit" ' + (canSend ? '' : 'disabled') + ' onclick="guestRestSubmitOrder()">Send to kitchen</button>' +
      '</section>' +
    '</div>' + mobileBar;
}
window.guestRestAddToCart = function(menuItemId) {
  ensureGuestRestaurantMenuLoaded();
  var m = menuItems.find(function(x) { return x && x.id === menuItemId; });
  if (!m || m.available === false) return;
  var existing = guestRestCart.find(function(c) { return c.menuItemId === menuItemId; });
  if (existing) existing.qty++;
  else guestRestCart.push({ menuItemId: menuItemId, name: m.name, unitPrice: m.price, qty: 1 });
  renderGuestRestaurantOrder();
};
window.guestRestCartQty = function(idx, delta) {
  var ci = guestRestCart[idx];
  if (!ci) return;
  var nq = ci.qty + delta;
  if (nq <= 0) guestRestCart.splice(idx, 1);
  else ci.qty = nq;
  renderGuestRestaurantOrder();
};
window.guestRestCartRemove = function(idx) {
  guestRestCart.splice(idx, 1);
  renderGuestRestaurantOrder();
};
window.guestRestStartNewOrder = function() {
  guestRestSubmitted = false;
  guestRestCart = [];
  renderGuestRestaurantOrder();
};
window.guestRestSubmitOrder = function() {
  if (!guestRestCart.length) return;
  ensureGuestRestaurantMenuLoaded();
  var wp = ensureGuestRestaurantWorkPeriod();
  if (!wp) { if (typeof toast === 'function') toast('Could not start restaurant shift'); return; }
  var taxRate = parseFloat(settings && (settings.serviceTax || settings.taxRate)) || 7;
  var items = guestRestCart.map(function(ci) {
    return { menuItemId: ci.menuItemId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice, total: (parseFloat(ci.unitPrice) || 0) * (parseInt(ci.qty, 10) || 0) };
  });
  var subtotal = items.reduce(function(s, i) { return s + i.total; }, 0);
  var tax = Math.round((subtotal * (taxRate / 100)) * 100) / 100;
  var grandTotal = Math.round((subtotal + tax) * 100) / 100;
  var notesEl = document.getElementById('guestRestOrderNotes');
  var notes = notesEl ? notesEl.value : '';
  var tableNumber = guestRestCtx.orderNum ? ('Order #' + guestRestCtx.orderNum) : (guestRestCtx.table ? String(guestRestCtx.table) : (guestRestCtx.room ? ('Room ' + guestRestCtx.room) : 'QR Guest'));
  var order = {
    id: genId(), timestamp: new Date().toISOString(), orderNumber: nextOrderNumber(),
    roomNumber: guestRestCtx.orderNum ? String(guestRestCtx.orderNum) : (guestRestCtx.room || ''),
    guestName: guestRestCtx.orderNum ? ('Order #' + guestRestCtx.orderNum) : (guestRestCtx.guest || 'Guest'),
    bookingId: guestRestCtx.booking || '', guestOrderNum: guestRestCtx.orderNum || '',
    tableNumber: tableNumber, items: items, subtotal: subtotal, tax: tax, grandTotal: grandTotal,
    status: 'Preparing', paidBy: 'Pending', staffName: 'Guest (QR scan)', notes: notes, workPeriodId: wp.id,
    diningFlow: 'kitchen', guestQrOrder: true, source: 'guestQr'
  };
  restaurantOrders.push(order);
  try { save('restaurantOrders', restaurantOrders); } catch (e) {}
  try { if (typeof logAudit === 'function') logAudit('New Order', 'Restaurant', order.orderNumber, 'Guest QR order: ' + fmt$(grandTotal) + ' (' + tableNumber + ')'); } catch (e) {}
  guestRestCart = [];
  guestRestSubmitted = true;
  renderGuestRestaurantOrder();
};
""" + GUEST_ORDER_PARSE_AND_BOOT_V4 + GUEST_ORDER_BOOT_V4


CSS_V4_MENU_OLD = """    .guest-rest-tabs { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.65rem; }
    .guest-rest-menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0.5rem; }
    .guest-rest-menu-card { display: flex; flex-direction: column; align-items: flex-start; text-align: left; gap: 0.15rem; border: 1px solid var(--border); border-radius: 10px; padding: 0.65rem; background: var(--card-bg, #fff); cursor: pointer; min-height: 88px; }
    .guest-rest-menu-card:active { transform: scale(0.98); }
    .grmc-name { font-weight: 600; font-size: 0.88rem; line-height: 1.25; }
    .grmc-meta { font-size: 0.72rem; color: var(--text-light); }
    .grmc-price { font-size: 0.85rem; color: var(--primary); font-weight: 700; margin-top: auto; }"""

CSS_V5_MENU_NEW = """    .guest-rest-tabs { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.65rem; }
    .guest-rest-search { margin-bottom: 0.65rem; }
    .guest-rest-search input { width: 100%; min-height: 42px; border-radius: 10px; }
    .guest-rest-menu-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.55rem; }
    @media (min-width: 480px) { .guest-rest-menu-grid { grid-template-columns: repeat(3, 1fr); gap: 0.65rem; } }
    @media (min-width: 768px) { .guest-rest-menu-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (min-width: 900px) { .guest-rest-menu-grid { grid-template-columns: repeat(3, 1fr); } }
    .guest-rest-menu-card { display: flex; flex-direction: column; align-items: stretch; text-align: left; gap: 0; border: 1px solid var(--border); border-radius: 12px; padding: 0; background: var(--card-bg, #fff); cursor: pointer; overflow: hidden; min-height: 0; }
    .guest-rest-menu-card:active { transform: scale(0.98); }
    .guest-rest-menu-card .grmc-img { position: relative; width: 100%; aspect-ratio: 4 / 3; background: linear-gradient(180deg, #e8e8e8, #f5f5f5); display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .guest-rest-menu-card .grmc-img img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .guest-rest-menu-card .grmc-img .grmc-img-ico { position: absolute; right: 4px; bottom: 4px; font-size: 1.1rem; line-height: 1; z-index: 1; text-shadow: 0 0 4px #fff, 0 0 2px #fff; pointer-events: none; }
    .guest-rest-menu-card .grmc-img.grmc-img-ph { font-size: 2rem; }
    .guest-rest-menu-card .grmc-img.grmc-img-err { min-height: 72px; }
    .guest-rest-menu-card .grmc-body { display: flex; flex-direction: column; gap: 0.1rem; padding: 0.5rem 0.55rem 0.6rem; flex: 1; }
    .grmc-name { font-weight: 600; font-size: 0.82rem; line-height: 1.25; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .grmc-meta { font-size: 0.68rem; color: var(--text-light); }
    .grmc-desc { font-size: 0.68rem; color: var(--text-light); line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .grmc-price { font-size: 0.88rem; color: var(--primary); font-weight: 700; margin-top: auto; padding-top: 0.15rem; }
    .guest-rest-cart-panel { scroll-margin-top: 72px; }
    .guest-rest-mobile-bar { display: none; }
    @media (max-width: 767px) {
      .guest-rest-mobile-bar { display: flex; position: fixed; left: 0; right: 0; bottom: 0; z-index: 10060; gap: 0.5rem; padding: 0.55rem 0.75rem calc(0.55rem + env(safe-area-inset-bottom, 0px)); background: rgba(255,255,255,0.96); border-top: 1px solid var(--border); box-shadow: 0 -4px 16px rgba(0,0,0,0.08); backdrop-filter: blur(8px); }
      body.dark-mode .guest-rest-mobile-bar { background: rgba(26,32,44,0.96); }
      .guest-rest-mobile-bar-main { flex: 1; display: flex; flex-direction: column; align-items: flex-start; justify-content: center; min-height: 44px; border: 1px solid var(--border); border-radius: 10px; background: var(--card-bg, #fff); padding: 0.35rem 0.65rem; cursor: pointer; text-align: left; }
      .guest-rest-mobile-bar-count { font-size: 0.72rem; color: var(--text-light); }
      .guest-rest-mobile-bar-total { font-size: 1rem; font-weight: 700; color: var(--primary); line-height: 1.2; }
      .guest-rest-mobile-bar-hint { font-size: 0.68rem; color: var(--text-light); }
      .guest-rest-mobile-bar-go { flex: 0 0 auto; min-width: 110px; min-height: 44px; justify-content: center; }
      .guest-rest-order-shell { padding-bottom: calc(5.5rem + env(safe-area-inset-bottom, 0px)); }
    }"""

GUEST_ORDER_JS_V4 = """var guestRestCart = [];
var guestRestMenuFilter = 'All';
var guestRestCtx = { room: '', guest: '', booking: '', table: '' };
var guestRestSubmitted = false;"""

GUEST_ORDER_JS_V5 = """var guestRestCart = [];
var guestRestMenuFilter = 'All';
var guestOrderMenuSearch = '';
var guestRestCtx = { room: '', guest: '', booking: '', table: '' };
var guestRestSubmitted = false;"""

REST_MENU_CARD_V4 = """    menuHtml += '<button type="button" class="guest-rest-menu-card" onclick="guestRestAddToCart(\\'' + idEsc + '\\')"><span class="grmc-name">' + guestRestEsc(m.name) + '</span><span class="grmc-meta">' + guestRestEsc(m.category || '') + '</span><span class="grmc-price">' + fmt$(m.price) + '</span></button>';"""

REST_MENU_CARD_V5 = """    menuHtml += guestRestMenuCardHtml(m, idEsc, 'guestRestAddToCart', false);"""

MART_MENU_CARD_V4 = """    menuHtml += '<button type="button" class="guest-rest-menu-card" onclick="guestMartAddToCart(\\'' + idEsc + '\\')"><span class="grmc-name">' + guestRestEsc(m.name) + '</span><span class="grmc-meta">' + guestRestEsc(m.category || '') + '</span><span class="grmc-price">' + fmt$(m.price) + '</span></button>';"""

MART_MENU_CARD_V5 = """    menuHtml += guestRestMenuCardHtml(m, idEsc, 'guestMartAddToCart', true);"""

REST_FILTER_V4 = """    return m && m.available !== false && (typeof rowDataVisible !== 'function' || rowDataVisible(m));
  });"""

REST_FILTER_V5 = """    return m && m.available !== false && (typeof rowDataVisible !== 'function' || rowDataVisible(m)) && guestRestMenuMatchesSearch(m, searchQ);
  });"""

MART_FILTER_V4 = """    return m && m.available !== false && (typeof rowDataVisible !== 'function' || rowDataVisible(m));
  });"""

MART_FILTER_V5 = """    return m && m.available !== false && (typeof rowDataVisible !== 'function' || rowDataVisible(m)) && guestRestMenuMatchesSearch(m, searchQ);
  });"""

STAFF_HANDLERS_START = "window.guestOrderQrSetMode = function(mode) {"

STALE_BOOT_BLOCK = """window.tryBootGuestRestaurantOrder = function() {
  var params = parseGuestRestaurantOrderParams();"""

INIT_AUTOLOGIN_BROKEN = """  if (typeof tryBootGuestRestaurantOrder === 'function' && tryBootGuestRestaurantOrder()) { return; }
  if (typeof hotelIsSetupComplete === 'function' && !hotelIsSetupComplete()) { return; }"""

INIT_AUTOLOGIN_FIXED = """  if (typeof tryBootGuestOrderFromUrl === 'function' && tryBootGuestOrderFromUrl()) { return; }
  if (typeof tryBootGuestRestaurantOrder === 'function' && tryBootGuestRestaurantOrder()) { return; }
  if (typeof hotelIsSetupComplete === 'function' && !hotelIsSetupComplete()) { return; }"""


def _apply_v7_upgrades(content: str) -> str:
    if GET_INVOICE_QR_PAYLOAD_V2 in content and "guestQrMinimartOrderEnabled" not in content:
        content = content.replace(GET_INVOICE_QR_PAYLOAD_V2, GET_INVOICE_QR_PAYLOAD_V3, 1)
    elif "function buildGuestOrderUrl" in content and "buildInvoiceGuestOrderQrsHtml" not in content:
        if GET_INVOICE_QR_PAYLOAD_V1 in content:
            content = content.replace(GET_INVOICE_QR_PAYLOAD_V1, GET_INVOICE_QR_PAYLOAD_V3, 1)

    if BUILD_INVOICE_QR_HTML_HEAD_OLD in content and "buildInvoiceGuestOrderQrsHtml" not in content.split("function buildInvoiceQrHtml", 1)[1][:400]:
        content = content.replace(BUILD_INVOICE_QR_HTML_HEAD_OLD, BUILD_INVOICE_QR_HTML_HEAD_NEW, 1)

    if REFRESH_INVOICE_QR_OLD in content and "buildInvoiceGuestOrderQrsHtml(inv)) return" not in content:
        content = content.replace(REFRESH_INVOICE_QR_OLD, REFRESH_INVOICE_QR_NEW, 1)

    if SETTINGS_QR_DETAILS_V2 in content and "sInvoiceQrGuestOrderMart" not in content:
        content = content.replace(SETTINGS_QR_DETAILS_V2, SETTINGS_QR_DETAILS_V3, 1)
    elif SETTINGS_QR_DETAILS_V1 in content and "sInvoiceQrGuestOrderMart" not in content:
        content = content.replace(SETTINGS_QR_DETAILS_V1, SETTINGS_QR_DETAILS_V3, 1)

    if SAVE_SETTINGS_QR_NEW in content and "sInvoiceQrGuestOrderMart" not in content:
        content = content.replace(SAVE_SETTINGS_QR_NEW, SAVE_SETTINGS_QR_V3, 1)

    if ENSURE_GUEST_SETTING_V2 in content and "invoiceQrIncludeMinimartOrder" not in content:
        content = content.replace(ENSURE_GUEST_SETTING_V2, ENSURE_GUEST_SETTING_V3, 1)

    if INIT_AUTOLOGIN_DUP_OLD in content:
        content = content.replace(INIT_AUTOLOGIN_DUP_OLD, INIT_AUTOLOGIN_DUP_NEW, 1)
    elif INIT_AUTOLOGIN_DUP_ALT in content:
        content = content.replace(INIT_AUTOLOGIN_DUP_ALT, INIT_AUTOLOGIN_DUP_NEW, 1)

    mart_fn = re.search(
        r"function renderGuestMiniMartOrder\(\) \{.*?\n\}\nwindow\.guestMartAddToCart",
        content,
        flags=re.DOTALL,
    )
    if mart_fn and "Search items" not in mart_fn.group(0):
        content = content.replace(
            mart_fn.group(0),
            RENDER_GUEST_MINIMART_ORDER_V8 + "\nwindow.guestMartAddToCart",
            1,
        )

    content = re.sub(r"HRMM-GUEST-QR-ORDER-v\d+", MARKER, content)
    return content


BUILD_GUEST_ORDER_URL_INV_OLD = """  if (inv) {
    var roomVal = inv.roomNumber != null ? String(inv.roomNumber).trim() : '';
    var tableVal = inv.tableNumber != null ? String(inv.tableNumber).trim() : '';
    if (!tableVal && roomVal && /^table\\b/i.test(roomVal)) tableVal = roomVal;
    if (tableVal && tableVal !== '—') params.set('table', tableVal);
    else if (roomVal && roomVal !== '—' && !/^table\\b/i.test(roomVal)) params.set('room', roomVal);
    if (inv.guestName != null && String(inv.guestName).trim() !== '' && String(inv.guestName).trim() !== '—') params.set('guest', String(inv.guestName).trim());
    if (inv.bookingId != null && String(inv.bookingId).trim() !== '') params.set('booking', String(inv.bookingId).trim());
  }"""

BUILD_GUEST_ORDER_URL_INV_V8 = """  if (inv) {
    if (deptKey === 'minimart') {
      var orderNumVal = inv.orderNum != null ? String(inv.orderNum).trim() : '';
      if (orderNumVal && orderNumVal !== '—') {
        params.set('orderNum', orderNumVal);
      } else {
        var roomVal = inv.roomNumber != null ? String(inv.roomNumber).trim() : '';
        var tableVal = inv.tableNumber != null ? String(inv.tableNumber).trim() : '';
        if (!tableVal && roomVal && /^table\\b/i.test(roomVal)) tableVal = roomVal;
        if (tableVal && tableVal !== '—') params.set('table', tableVal);
        else if (roomVal && roomVal !== '—' && !/^table\\b/i.test(roomVal)) params.set('room', roomVal);
        if (inv.guestName != null && String(inv.guestName).trim() !== '' && String(inv.guestName).trim() !== '—') params.set('guest', String(inv.guestName).trim());
        if (inv.bookingId != null && String(inv.bookingId).trim() !== '') params.set('booking', String(inv.bookingId).trim());
      }
    } else {
      var roomVal = inv.roomNumber != null ? String(inv.roomNumber).trim() : '';
      var tableVal = inv.tableNumber != null ? String(inv.tableNumber).trim() : '';
      if (!tableVal && roomVal && /^table\\b/i.test(roomVal)) tableVal = roomVal;
      if (tableVal && tableVal !== '—') params.set('table', tableVal);
      else if (roomVal && roomVal !== '—' && !/^table\\b/i.test(roomVal)) params.set('room', roomVal);
      if (inv.guestName != null && String(inv.guestName).trim() !== '' && String(inv.guestName).trim() !== '—') params.set('guest', String(inv.guestName).trim());
      if (inv.bookingId != null && String(inv.bookingId).trim() !== '') params.set('booking', String(inv.bookingId).trim());
    }
  }"""

BUILD_GUEST_ORDER_URL_INV_NEW = """  if (inv) {
    var orderNumVal = inv.orderNum != null ? String(inv.orderNum).trim() : '';
    if (orderNumVal && orderNumVal !== '—') {
      params.set('orderNum', orderNumVal);
    } else {
      var roomVal = inv.roomNumber != null ? String(inv.roomNumber).trim() : '';
      var tableVal = inv.tableNumber != null ? String(inv.tableNumber).trim() : '';
      if (!tableVal && roomVal && /^table\\b/i.test(roomVal)) tableVal = roomVal;
      if (tableVal && tableVal !== '—') params.set('table', tableVal);
      else if (roomVal && roomVal !== '—' && !/^table\\b/i.test(roomVal)) params.set('room', roomVal);
      if (inv.guestName != null && String(inv.guestName).trim() !== '' && String(inv.guestName).trim() !== '—') params.set('guest', String(inv.guestName).trim());
      if (inv.bookingId != null && String(inv.bookingId).trim() !== '') params.set('booking', String(inv.bookingId).trim());
    }
  }"""

PARSE_GUEST_ORDER_PARAMS_OLD = "return { dept: go, room: sp.get('room') || '', guest: sp.get('guest') || '', booking: sp.get('booking') || '', table: sp.get('table') || '' };"
PARSE_GUEST_ORDER_PARAMS_NEW = "return { dept: go, room: sp.get('room') || '', guest: sp.get('guest') || '', booking: sp.get('booking') || '', table: sp.get('table') || '', orderNum: sp.get('orderNum') || '' };"

GUEST_MART_CTX_OLD = "var guestMartCtx = { room: '', guest: '', booking: '', table: '' };"
GUEST_MART_CTX_NEW = "var guestMartCtx = { room: '', guest: '', booking: '', table: '', orderNum: '' };"

GUEST_REST_CTX_OLD = "var guestRestCtx = { room: '', guest: '', booking: '', table: '' };"
GUEST_REST_CTX_NEW = "var guestRestCtx = { room: '', guest: '', booking: '', table: '', orderNum: '' };"


def _replace_guest_order_staff_js(content: str) -> str:
    start = content.find("var guestOrderQrStaffCtx")
    if start < 0:
        return content
    end_marker = "window.guestOrderQrOpenCustomerScreen = function()"
    end = content.find(end_marker, start)
    if end < 0:
        return content
    end = content.find("\n};", end)
    if end < 0:
        return content
    return content[:start] + GUEST_ORDER_STAFF_JS.strip() + "\n" + content[end + 4 :]


def _apply_v8_upgrades(content: str) -> str:
    if "guestOrderQrPickOrderNum" not in content:
        content = _replace_guest_order_staff_js(content)

    if BUILD_GUEST_ORDER_URL_INV_OLD in content and "params.set('orderNum'" not in content.split("function buildGuestOrderUrl", 1)[1][:1200]:
        content = content.replace(BUILD_GUEST_ORDER_URL_INV_OLD, BUILD_GUEST_ORDER_URL_INV_NEW, 1)

    if PARSE_GUEST_ORDER_PARAMS_OLD in content:
        content = content.replace(PARSE_GUEST_ORDER_PARAMS_OLD, PARSE_GUEST_ORDER_PARAMS_NEW, 1)

    if GUEST_MART_CTX_OLD in content:
        content = content.replace(GUEST_MART_CTX_OLD, GUEST_MART_CTX_NEW, 1)

    mart_chunk = content.split("function renderGuestMiniMartOrder()", 1)
    if len(mart_chunk) > 1 and "guestMartCtx.orderNum" not in mart_chunk[1][:1200]:
        mart_fn = re.search(
            r"function renderGuestMiniMartOrder\(\) \{.*?\n\}\nwindow\.guestMartAddToCart",
            content,
            flags=re.DOTALL,
        )
        if mart_fn:
            content = content.replace(
                mart_fn.group(0),
                RENDER_GUEST_MINIMART_ORDER_V8 + "\nwindow.guestMartAddToCart",
                1,
            )

    if "guestMartCtx = { room: ctx.room" in content and "orderNum: ctx.orderNum" not in content:
        content = content.replace(
            "guestMartCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '' };",
            "guestMartCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '', orderNum: ctx.orderNum || '' };",
            1,
        )

    if "guestOrderNum: guestMartCtx.orderNum" not in content and "window.guestMartSubmitOrder = function()" in content:
        content = content.replace(
            "roomNumber: guestMartCtx.room || '—', guestName: guestMartCtx.guest || 'Walk-in', bookingId: guestMartCtx.booking || '',",
            "roomNumber: guestMartCtx.orderNum ? String(guestMartCtx.orderNum) : (guestMartCtx.room || '—'),\n    guestName: guestMartCtx.orderNum ? ('Order #' + guestMartCtx.orderNum) : (guestMartCtx.guest || 'Walk-in'),\n    bookingId: guestMartCtx.booking || '',\n    guestOrderNum: guestMartCtx.orderNum || '',",
            1,
        )

    content = re.sub(r"HRMM-GUEST-QR-ORDER-v\d+", MARKER, content)
    return content


def _apply_v9_upgrades(content: str) -> str:
    if "guest-order-qr-modal" in content and "Room guest</button>" in content:
        content = _replace_guest_order_staff_js(content)

    if BUILD_GUEST_ORDER_URL_INV_V8 in content:
        content = content.replace(BUILD_GUEST_ORDER_URL_INV_V8, BUILD_GUEST_ORDER_URL_INV_NEW, 1)
    elif BUILD_GUEST_ORDER_URL_INV_OLD in content and "params.set('orderNum'" not in content.split("function buildGuestOrderUrl", 1)[1][:1200]:
        content = content.replace(BUILD_GUEST_ORDER_URL_INV_OLD, BUILD_GUEST_ORDER_URL_INV_NEW, 1)

    if GUEST_REST_CTX_OLD in content:
        content = content.replace(GUEST_REST_CTX_OLD, GUEST_REST_CTX_NEW, 1)

    if "guestRestCtx.orderNum" not in content.split("function renderGuestRestaurantOrder()", 1)[1][:900]:
        content = content.replace(
            "    if (guestRestCtx.guest) bits.push(guestRestCtx.guest);\n    if (guestRestCtx.room) bits.push('Room ' + guestRestCtx.room);",
            "    if (guestRestCtx.orderNum) bits.push('Order number ' + guestRestCtx.orderNum);\n    else {\n      if (guestRestCtx.guest) bits.push(guestRestCtx.guest);\n      if (guestRestCtx.room) bits.push('Room ' + guestRestCtx.room);",
            1,
        )
        content = content.replace(
            "    if (guestRestCtx.booking) bits.push('Booking ' + guestRestCtx.booking);\n    sub.textContent = bits.length ? bits.join(' · ') : 'Browse the menu",
            "    if (guestRestCtx.booking) bits.push('Booking ' + guestRestCtx.booking);\n    }\n    sub.textContent = bits.length ? bits.join(' · ') : 'Browse the menu",
            1,
        )

    if "guestOrderNum: guestRestCtx.orderNum" not in content and "window.guestRestSubmitOrder = function()" in content:
        content = content.replace(
            "  var tableNumber = guestRestCtx.table ? String(guestRestCtx.table) : (guestRestCtx.room ? ('Room ' + guestRestCtx.room) : 'QR Guest');\n  var order = {\n    id: genId(), timestamp: new Date().toISOString(), orderNumber: nextOrderNumber(),\n    roomNumber: guestRestCtx.room || '', guestName: guestRestCtx.guest || 'Guest', bookingId: guestRestCtx.booking || '',",
            "  var tableNumber = guestRestCtx.orderNum ? ('Order #' + guestRestCtx.orderNum) : (guestRestCtx.table ? String(guestRestCtx.table) : (guestRestCtx.room ? ('Room ' + guestRestCtx.room) : 'QR Guest'));\n  var order = {\n    id: genId(), timestamp: new Date().toISOString(), orderNumber: nextOrderNumber(),\n    roomNumber: guestRestCtx.orderNum ? String(guestRestCtx.orderNum) : (guestRestCtx.room || ''),\n    guestName: guestRestCtx.orderNum ? ('Order #' + guestRestCtx.orderNum) : (guestRestCtx.guest || 'Guest'),\n    bookingId: guestRestCtx.booking || '', guestOrderNum: guestRestCtx.orderNum || '',",
            1,
        )
        content = content.replace(
            "diningFlow: 'kitchen', guestQrOrder: true\n  };",
            "diningFlow: 'kitchen', guestQrOrder: true, source: 'guestQr'\n  };",
            1,
        )

    if "guestRestCtx = { room: ctx.room" in content and "orderNum: ctx.orderNum" not in content.split("guestRestCtx = { room: ctx.room", 1)[1][:80]:
        content = content.replace(
            "guestRestCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '' };",
            "guestRestCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '', orderNum: ctx.orderNum || '' };",
            1,
        )

    content = re.sub(r"HRMM-GUEST-QR-ORDER-v\d+", MARKER, content)
    return content


I18N_BNAV_GUEST_PARTIAL_OLD = """    "guestOrder": "Order QR",
    "menu": "Menu","""

I18N_BNAV_GUEST_PARTIAL_NEW = """    "guestOrder": "Order QR",
    "guestOrderRest": "RESTAURANT QR",
    "guestOrderMart": "MINIMart QR",
    "menu": "Menu","""


def _apply_bnav_qr_labels(content: str) -> str:
    if I18N_BNAV_GUEST_PARTIAL_OLD in content:
        content = content.replace(I18N_BNAV_GUEST_PARTIAL_OLD, I18N_BNAV_GUEST_PARTIAL_NEW, 1)
    content = content.replace('"guestOrderRest": "Rest QR"', '"guestOrderRest": "RESTAURANT QR"')
    content = content.replace('"guestOrderMart": "Mart QR"', '"guestOrderMart": "MINIMart QR"')
    content = re.sub(
        r'("bnav": \{\s*"dashboard":[^\n]+\n\s*"pos":[^\n]+\n\s*"bookings":[^\n]+\n)(\s*"menu":)',
        r'\1    "guestOrderRest": "RESTAURANT QR",\n    "guestOrderMart": "MINIMart QR",\n\2',
        content,
    )
    content = content.replace(
        '<span class="bnav-label" data-i18n="bnav.guestOrderRest">Rest QR</span>',
        '<span class="bnav-label" data-i18n="bnav.guestOrderRest">RESTAURANT QR</span>',
    )
    content = content.replace(
        '<span class="bnav-label" data-i18n="bnav.guestOrderMart">Mart QR</span>',
        '<span class="bnav-label" data-i18n="bnav.guestOrderMart">MINIMart QR</span>',
    )
    return content


def _apply_invoice_qr_i18n(content: str) -> str:
    if INVOICE_QR_CAPTION_LEGACY in content and "invoice.qrScanRestaurant" not in content.split(INVOICE_QR_CAPTION_LEGACY, 1)[0][-200:]:
        content = content.replace(INVOICE_QR_CAPTION_LEGACY, INVOICE_QR_CAPTION_I18N, 1)
    legacy_single = """function invoiceQrCaptionForPayload(payload) {
  var s = String(payload == null ? '' : payload).trim();
  if (!s) return '';
  if (s.indexOf('guestOrder=restaurant') >= 0) return 'Scan to order from restaurant';
  return s.length > 52 ? s.slice(0, 49) + '…' : s;
}"""
    if legacy_single in content and "invoice.qrScanRestaurant" not in content:
        content = content.replace(legacy_single, INVOICE_QR_CAPTION_I18N, 1)
    if "custom ? 'Custom QR image' : invoiceQrCaptionForPayload" in content:
        content = content.replace(
            "custom ? 'Custom QR image' : invoiceQrCaptionForPayload",
            "custom ? (typeof invoiceT === 'function' ? invoiceT('invoice.qrCustomImage', 'Custom QR image') : 'Custom QR image') : invoiceQrCaptionForPayload",
        )
    return content


def _repair_order_qr(content: str) -> str:
    """Always run — fixes corrupted incremental upgrades (missing staff JS core, stale boot)."""
    if "function guestOrderQrBuildUrl" not in content and STAFF_HANDLERS_START in content:
        start = content.find(STAFF_HANDLERS_START)
        open_screen = content.find("window.guestOrderQrOpenCustomerScreen = function()", start)
        if open_screen >= 0:
            end = content.find("\n};", open_screen)
            if end >= 0:
                content = content[:start] + GUEST_ORDER_STAFF_JS.strip() + "\n" + content[end + 4 :]

    if STALE_BOOT_BLOCK in content and "window.tryBootGuestOrderFromUrl = function()" in content:
        idx = content.find(STALE_BOOT_BLOCK)
        end = content.find("\n};", idx)
        if end >= 0:
            content = content[:idx] + content[end + 4 :]

    if INIT_AUTOLOGIN_BROKEN in content:
        content = content.replace(INIT_AUTOLOGIN_BROKEN, INIT_AUTOLOGIN_FIXED, 1)

    if INIT_AUTOLOGIN_OLD in content and "tryBootGuestOrderFromUrl()" not in content.split(INIT_AUTOLOGIN_OLD, 1)[1][:200]:
        content = content.replace(INIT_AUTOLOGIN_OLD, INIT_AUTOLOGIN_NEW, 1)

    if BOTTOM_NAV_SINGLE_GUEST_ORDER in content and 'data-bnav="guestorder-rest"' not in content:
        content = content.replace(BOTTOM_NAV_SINGLE_GUEST_ORDER, BOTTOM_NAV_WITH_GUEST_ORDER, 1)

    if BNAV_FN_GUEST_SINGLE in content and "guestorder-mart" not in content.split("window.bnav = function(page)", 1)[1][:500]:
        content = content.replace(BNAV_FN_GUEST_SINGLE, BNAV_FN_NEW, 1)

    if RBAC_BNAV_SETTINGS_GUEST_SINGLE in content and "bnavGuestOrderRest" not in content:
        content = content.replace(RBAC_BNAV_SETTINGS_GUEST_SINGLE, RBAC_BNAV_SETTINGS_GUEST, 1)

    content = re.sub(r"HRMM-GUEST-QR-ORDER-v\d+", MARKER, content)
    if "<!-- HRMM-GUEST-QR-ORDER" not in content and MARKER not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )
    elif f"<!-- {MARKER} -->" not in content:
        content = re.sub(r"<!-- HRMM-GUEST-QR-ORDER-v\d+ -->", f"<!-- {MARKER} -->", content)

    return content


def _is_fully_patched(content: str) -> bool:
    return (
        MARKER in content
        and "function guestOrderQrBuildUrl" in content
        and "var guestOrderQrStaffCtx" in content
        and "guestRestMenuCardHtml" in content
        and "tryBootGuestOrderFromUrl" in content
        and "buildInvoiceGuestOrderQrsHtml" in content
        and "guestQrMinimartOrderEnabled" in content
        and 'data-bnav="guestorder-rest"' in content
        and 'data-bnav="guestorder-mart"' in content
        and STALE_BOOT_BLOCK not in content
        and "function renderGuestMiniMartOrder()" in content
        and "Search items" in content.split("function renderGuestMiniMartOrder()", 1)[1][:2500]
        and "guestOrderQrPickOrderNum" in content
    )


def _apply_v3_upgrades(content: str) -> str:
    if BOTTOM_NAV_DOCS_BTN in content and 'data-bnav="guestorder"' not in content:
        content = content.replace(BOTTOM_NAV_DOCS_BTN, BOTTOM_NAV_WITH_GUEST_ORDER, 1)

    if BNAV_FN_OLD in content and "page === 'guestorder'" not in content.split("window.bnav = function(page)", 1)[1][:400]:
        content = content.replace(BNAV_FN_OLD, BNAV_FN_NEW, 1)

    if RBAC_BNAV_SETTINGS_TAIL in content and "bnavGuestOrder" not in content:
        content = content.replace(RBAC_BNAV_SETTINGS_TAIL, RBAC_BNAV_SETTINGS_GUEST, 1)

    if I18N_BNAV_OLD in content and '"guestOrder"' not in content.split(I18N_BNAV_OLD, 1)[0][-80:]:
        content = content.replace(I18N_BNAV_OLD, I18N_BNAV_NEW, 1)

    if "guestOrderQrStaffCtx" not in content and "window.tryBootGuestRestaurantOrder = function()" in content:
        content = content.replace(
            "window.tryBootGuestRestaurantOrder = function() {",
            GUEST_ORDER_STAFF_JS + "\nwindow.tryBootGuestRestaurantOrder = function() {",
            1,
        )
    elif "guestOrderQrStaffCtx" not in content and "tryBootGuestRestaurantOrder" in content:
        anchor = "/* Autologin after all data and i18n helpers are ready. Never show login on top of the first-time setup overlay. */"
        if anchor in content:
            content = content.replace(anchor, GUEST_ORDER_STAFF_JS + anchor, 1)

    if "guest-order-qr-modal" not in content and "/* __HRMM_GUEST_QR_MARKER__ */" in content:
        content = content.replace(
            "    /* __HRMM_GUEST_QR_MARKER__ */",
            "    .bottom-nav-item[data-bnav=\"guestorder\"] .bnav-label { max-width: 3.5rem; }\n"
            "    .guest-order-qr-modal { max-width: 420px; }\n"
            "    .guest-order-qr-lead { font-size: 0.85rem; color: var(--text-light); margin: 0 0 0.75rem; line-height: 1.45; }\n"
            "    .guest-order-qr-preview { text-align: center; margin: 0.75rem 0 1rem; padding: 0.65rem; border: 1px dashed var(--border); border-radius: 10px; background: rgba(255,255,255,0.5); }\n"
            "    body.dark-mode .guest-order-qr-preview { background: rgba(0,0,0,0.15); }\n"
            "    .guest-order-qr-actions { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }\n"
            "    .guest-order-qr-actions .btn { flex: 1 1 140px; justify-content: center; min-height: 42px; }\n"
            "    /* __HRMM_GUEST_QR_MARKER__ */",
            1,
        )

    return content


def _apply_v5_upgrades(content: str) -> str:
    content = re.sub(r"HRMM-GUEST-QR-ORDER-v4", MARKER, content)

    if CSS_V4_MENU_OLD in content and ".guest-rest-search" not in content:
        content = content.replace(CSS_V4_MENU_OLD, CSS_V5_MENU_NEW, 1)

    if GUEST_ORDER_JS_V4 in content and "guestOrderMenuSearch" not in content:
        content = content.replace(GUEST_ORDER_JS_V4, GUEST_ORDER_JS_V5, 1)

    if "function guestRestMenuCardHtml" not in content and "function guestRestEsc(s)" in content:
        content = content.replace(
            "function guestRestEsc(s) {\n  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\"/g, '&quot;');\n}",
            "function guestRestEsc(s) {\n  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\"/g, '&quot;');\n}"
            + GUEST_ORDER_MENU_HELPERS,
            1,
        )

    if REST_MENU_CARD_V4 in content:
        content = content.replace(REST_MENU_CARD_V4, REST_MENU_CARD_V5, 1)

    if MART_MENU_CARD_V4 in content:
        content = content.replace(MART_MENU_CARD_V4, MART_MENU_CARD_V5, 1)

    if REST_FILTER_V4 in content and "guestRestMenuMatchesSearch" in content:
        content = content.replace(REST_FILTER_V4, REST_FILTER_V5, 1)

    if MART_FILTER_V4 in content and "guestRestMenuMatchesSearch" in content:
        content = content.replace(MART_FILTER_V4, MART_FILTER_V5, 1)

    if "var searchQ = String(guestOrderMenuSearch" not in content and "function renderGuestRestaurantOrder()" in content:
        content = content.replace(
            "  var categories = ['All'].concat(typeof getMenuCategories === 'function' ? getMenuCategories() : []);\n  var tabs = '<div class=\"guest-rest-tabs\">'",
            "  var categories = ['All'].concat(typeof getMenuCategories === 'function' ? getMenuCategories() : []);\n  var searchQ = String(guestOrderMenuSearch || '').trim();\n  var searchHtml = '<div class=\"guest-rest-search\"><input type=\"search\" class=\"form-control\" placeholder=\"Search menu…\" value=\"' + guestRestEsc(searchQ) + '\" oninput=\"guestOrderMenuSearch=this.value;renderGuestOrderScreen()\" autocomplete=\"off\"></div>';\n  var tabs = '<div class=\"guest-rest-tabs\">'",
            1,
        )
        content = content.replace(
            "      '<section class=\"guest-rest-panel\"><h2>Menu</h2>' + tabs + menuHtml + '</section>' +",
            "      '<section class=\"guest-rest-panel\"><h2>Menu</h2>' + searchHtml + tabs + menuHtml + '</section>' +",
            1,
        )
        content = content.replace(
            "      '<section class=\"guest-rest-panel guest-rest-cart-panel\"><h2>Your order",
            "      '<section class=\"guest-rest-panel guest-rest-cart-panel\" id=\"guestRestCartPanel\"><h2>Your order",
            1,
        )
        content = content.replace(
            "  var canSend = guestRestCart.length > 0;\n  body.innerHTML =",
            "  var canSend = guestRestCart.length > 0;\n  var mobileBar = guestRestMobileBarHtml(guestRestCart.length, grandTotal, 'guestRestSubmitOrder', 'Send order', canSend);\n  body.innerHTML =",
            1,
        )
        content = content.replace(
            "      '</section>' +\n    '</div>';\n}\nwindow.guestRestAddToCart = function(menuItemId) {",
            "      '</section>' +\n    '</div>' + mobileBar;\n}\nwindow.guestRestAddToCart = function(menuItemId) {",
            1,
        )

    if "var searchQ = String(guestOrderMenuSearch" not in content.split("function renderGuestMiniMartOrder()", 1)[1][:900] and "function renderGuestMiniMartOrder()" in content:
        content = content.replace(
            "  var categories = ['All'].concat(typeof getStoreCategories === 'function' ? getStoreCategories() : []);\n  var tabs = '<div class=\"guest-rest-tabs\">'",
            "  var categories = ['All'].concat(typeof getStoreCategories === 'function' ? getStoreCategories() : []);\n  var searchQ = String(guestOrderMenuSearch || '').trim();\n  var searchHtml = '<div class=\"guest-rest-search\"><input type=\"search\" class=\"form-control\" placeholder=\"Search items…\" value=\"' + guestRestEsc(searchQ) + '\" oninput=\"guestOrderMenuSearch=this.value;renderGuestOrderScreen()\" autocomplete=\"off\"></div>';\n  var tabs = '<div class=\"guest-rest-tabs\">'",
            1,
        )
        content = content.replace(
            "body.innerHTML = '<div class=\"guest-rest-layout\"><section class=\"guest-rest-panel\"><h2>Items</h2>' + tabs + menuHtml + '</section><section class=\"guest-rest-panel guest-rest-cart-panel\"><h2>Your cart",
            "  var mobileBar = guestRestMobileBarHtml(guestMartCart.length, grandTotal, 'guestMartSubmitOrder', 'Submit', guestMartCart.length > 0);\n  body.innerHTML = '<div class=\"guest-rest-layout\"><section class=\"guest-rest-panel\"><h2>Items</h2>' + searchHtml + tabs + menuHtml + '</section><section class=\"guest-rest-panel guest-rest-cart-panel\" id=\"guestRestCartPanel\"><h2>Your cart",
            1,
        )
        content = content.replace(
            "onclick=\"guestMartSubmitOrder()\">Submit order</button></section></div>';\n}\nwindow.guestMartAddToCart = function(id) {",
            "onclick=\"guestMartSubmitOrder()\">Submit order</button></section></div>' + mobileBar;\n}\nwindow.guestMartAddToCart = function(id) {",
            1,
        )

    return content


def _apply_v4_upgrades(content: str) -> str:
    content = re.sub(r"HRMM-GUEST-QR-ORDER-v3", MARKER, content)

    if INIT_AUTOLOGIN_OLD in content and "tryBootGuestOrderFromUrl()" not in content.split(INIT_AUTOLOGIN_OLD, 1)[1][:160]:
        content = content.replace(INIT_AUTOLOGIN_OLD, INIT_AUTOLOGIN_NEW, 1)

    if GUEST_ORDER_STAFF_JS_V3 in content and "guestOrderQrSetDept" not in content:
        content = content.replace(GUEST_ORDER_STAFF_JS_V3, GUEST_ORDER_STAFF_JS, 1)

    boot_anchor = "window.showGuestRestaurantOrderScreen = function(ctx) {"
    if boot_anchor in content and "tryBootGuestOrderFromUrl" not in content:
        start = content.find(boot_anchor)
        if start >= 0:
            end = content.find("\n};", start)
            if end >= 0:
                end = content.find("\n};", end + 3)
                if end >= 0:
                    content = content[:start] + GUEST_ORDER_PARSE_AND_BOOT_V4 + GUEST_ORDER_BOOT_V4 + content[end + 4 :]

    if "function parseGuestRestaurantOrderParams()" in content and "function parseGuestOrderParams()" not in content:
        content = content.replace(GUEST_ORDER_JS_BODY_V3_TAIL, "", 1)

    if INVOICE_QR_URL_BUILD_OLD in content and "buildGuestOrderUrl" not in content:
        content = content.replace(INVOICE_QR_URL_BUILD_OLD, INVOICE_QR_URL_BUILD_NEW, 1)
    elif "buildGuestOrderUrl" not in content:
        content = _apply_qr_payload_upgrade(content)

    return content


def _apply_qr_payload_upgrade(content: str) -> str:
    if GET_INVOICE_QR_PAYLOAD_V2 in content and "guestQrMinimartOrderEnabled" not in content:
        return content.replace(GET_INVOICE_QR_PAYLOAD_V2, GET_INVOICE_QR_PAYLOAD_V3, 1)
    if GET_INVOICE_QR_PAYLOAD_V1 in content:
        return content.replace(GET_INVOICE_QR_PAYLOAD_V1, GET_INVOICE_QR_PAYLOAD_V3, 1)
    if GET_INVOICE_QR_PAYLOAD_OLD in content:
        return content.replace(GET_INVOICE_QR_PAYLOAD_OLD, GET_INVOICE_QR_PAYLOAD_V2, 1)
    if "function guestQrRestaurantOrderEnabled()" in content and "isLegacyInvoiceQrPayload" not in content:
        raise SystemExit("Could not upgrade guest QR payload block")
    return content


def patch(content: str) -> str:
    if not _is_fully_patched(content):
        content = _apply_qr_payload_upgrade(content)

        if GET_EFFECTIVE_QR_PAYLOAD_OLD in content and "isLegacyInvoiceQrPayload" not in content.split(GET_EFFECTIVE_QR_PAYLOAD_OLD, 1)[0][-200:]:
            content = content.replace(GET_EFFECTIVE_QR_PAYLOAD_OLD, GET_EFFECTIVE_QR_PAYLOAD_NEW, 1)

        if BUILD_QR_CAPTION_OLD in content:
            content = content.replace(BUILD_QR_CAPTION_OLD, BUILD_QR_CAPTION_NEW, 1)

        if REFRESH_QR_CAPTION_OLD in content:
            content = content.replace(REFRESH_QR_CAPTION_OLD, REFRESH_QR_CAPTION_NEW, 1)

        if ENSURE_GUEST_SETTING_V1 in content:
            content = content.replace(ENSURE_GUEST_SETTING_V1, ENSURE_GUEST_SETTING_V2, 1)

        if UPDATE_QR_PREVIEW_OLD in content:
            content = content.replace(UPDATE_QR_PREVIEW_OLD, UPDATE_QR_PREVIEW_NEW, 1)

        if SETTINGS_QR_DETAILS_OLD in content:
            content = content.replace(SETTINGS_QR_DETAILS_OLD, SETTINGS_QR_DETAILS_V2, 1)
        elif SETTINGS_QR_DETAILS_V1 in content:
            content = content.replace(SETTINGS_QR_DETAILS_V1, SETTINGS_QR_DETAILS_V2, 1)

        if SAVE_SETTINGS_QR_OLD in content and "sInvoiceQrGuestOrder" not in content.split(SAVE_SETTINGS_QR_OLD, 1)[1][:120]:
            content = content.replace(SAVE_SETTINGS_QR_OLD, SAVE_SETTINGS_QR_NEW, 1)

        if LOGIN_OVERLAY_END in content and 'id="guestRestOrderOverlay"' not in content:
            content = content.replace(LOGIN_OVERLAY_END, GUEST_OVERLAY_HTML, 1)

        autologin_anchor = "/* Autologin after all data and i18n helpers are ready. Never show login on top of the first-time setup overlay. */"
        if autologin_anchor in content and "tryBootGuestRestaurantOrder" not in content:
            content = content.replace(
                autologin_anchor,
                GUEST_ORDER_JS + GUEST_ORDER_JS_BODY + GUEST_ORDER_STAFF_JS + autologin_anchor,
                1,
            )
        elif ENSURE_GUEST_SETTING_V1 in content and ENSURE_GUEST_SETTING_V2 not in content:
            content = content.replace(ENSURE_GUEST_SETTING_V1, ENSURE_GUEST_SETTING_V2, 1)

        if INIT_AUTOLOGIN_OLD in content and "tryBootGuestOrderFromUrl()" not in content.split(INIT_AUTOLOGIN_OLD, 1)[1][:160]:
            content = content.replace(INIT_AUTOLOGIN_OLD, INIT_AUTOLOGIN_NEW, 1)

        if "/* __HRMM_GUEST_QR_MARKER__ */" not in content:
            content = content.replace(
                "  </style>\n</head>",
                CSS + "\n  </style>\n</head>",
                1,
            )

        content = re.sub(r"<!-- HRMM-GUEST-QR-ORDER-v\d+ -->", f"<!-- {MARKER} -->", content)
        if MARKER not in content:
            content = content.replace(
                "<title>HotelRestaurantMini-MartManagement</title>",
                f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
                1,
            )

        content = _apply_v3_upgrades(content)
        content = _apply_v4_upgrades(content)
        content = _apply_v5_upgrades(content)
    else:
        print(f"Already patched {MARKER} — running integrity repair")

    content = _apply_v7_upgrades(content)
    content = _apply_v8_upgrades(content)
    content = _apply_v9_upgrades(content)
    content = _apply_bnav_qr_labels(content)
    content = _apply_invoice_qr_i18n(content)
    content = _repair_order_qr(content)
    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — guest QR restaurant & mini-mart self-order")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
