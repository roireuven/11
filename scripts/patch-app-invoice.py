#!/usr/bin/env python3
"""Invoice: items table, logo, and QR code on payment receipts."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-INVOICE-v4"
INDEX = Path("public/index.html")

CSS = """
    /* HRMM invoice items table, logo, and QR */
    .invoice-brand-block { text-align: center; margin-bottom: 1rem; }
    .invoice-brand-block img { max-height: 80px; max-width: 240px; object-fit: contain; }
    .invoice-brand-name { font-size: 1.15rem; font-weight: 700; margin: 0.35rem 0 0; }
    .invoice-qr-block { text-align: center; margin: 0.75rem 0 1rem; }
    .invoice-qr-img { width: 132px; height: 132px; object-fit: contain; border: 1px solid var(--border); border-radius: 8px; padding: 0.35rem; background: #fff; }
    .invoice-qr-caption { font-size: 0.72rem; color: var(--text-light); margin-top: 0.35rem; word-break: break-word; max-width: 220px; margin-left: auto; margin-right: auto; }
    .invoice-qr-editor { margin: 0.5rem auto 1rem; max-width: 300px; padding: 0.65rem; border: 1px dashed var(--border); border-radius: 8px; background: rgba(255,255,255,0.65); }
    body.dark-mode .invoice-qr-editor { background: rgba(0,0,0,0.18); }
    .invoice-qr-editor-label { font-size: 0.78rem; font-weight: 600; margin-bottom: 0.35rem; text-align: left; }
    .invoice-qr-edit-input { font-size: 0.82rem; margin-bottom: 0.5rem; width: 100%; box-sizing: border-box; }
    .invoice-qr-editor-actions { display: flex; flex-wrap: wrap; gap: 0.35rem; justify-content: center; }
    .invoice-qr-editor-hint { font-size: 0.72rem; color: var(--text-light); margin: 0.45rem 0 0; text-align: left; }
    .invoice-qr-browse-row { display: flex; flex-wrap: wrap; align-items: center; gap: 0.35rem; margin-top: 0.35rem; }
    .invoice-items-table { width: 100%; border-collapse: collapse; margin: 0.75rem 0; font-size: 0.85rem; }
    .invoice-items-table th, .invoice-items-table td { padding: 0.45rem 0.35rem; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }
    .invoice-items-table th:last-child, .invoice-items-table td:last-child { text-align: right; }
    .invoice-items-table th:nth-child(2), .invoice-items-table td:nth-child(2),
    .invoice-items-table th:nth-child(3), .invoice-items-table td:nth-child(3) { text-align: center; }
    .invoice-items-table thead th { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--text-light); border-bottom: 2px solid var(--border); }
    .invoice-items-table tbody tr:last-child td { border-bottom: none; }
    /* __HRMM_INVOICE_MARKER__ */
"""

HELPERS = """
function getInvoiceLineItems(inv) {
  if (!inv) return [];
  var rows = [];
  if (Array.isArray(inv.items) && inv.items.length) {
    inv.items.forEach(function(i) {
      if (!i) return;
      var qty = parseInt(i.qty != null ? i.qty : i.quantity, 10) || 1;
      var unit = parseFloat(i.unitPrice) || 0;
      rows.push({ name: i.name || i.itemName || 'Item', qty: qty, unitPrice: unit, lineTotal: parseFloat(i.total) || (unit * qty), category: i.category || i.serviceCategory || '' });
    });
  }
  if (!rows.length && Array.isArray(inv.services) && inv.services.length) {
    inv.services.forEach(function(s) {
      if (!s) return;
      var qty = parseInt(s.quantity, 10) || 1;
      var unit = parseFloat(s.unitPrice) || 0;
      rows.push({ name: s.name || 'Service', qty: qty, unitPrice: unit, lineTotal: unit * qty, category: s.serviceCategory || '' });
    });
  }
  if (!rows.length && inv.paymentTransactionId) {
    try {
      if (typeof load === 'function') transactions = load('transactions', transactions);
      var txn = (transactions || []).find(function(x) { return x && String(x.transactionId || '') === String(inv.paymentTransactionId); });
      if (txn && Array.isArray(txn.items)) {
        txn.items.forEach(function(i) {
          if (!i) return;
          var qty = parseInt(i.qty, 10) || 1;
          var unit = parseFloat(i.unitPrice) || 0;
          rows.push({ name: i.name || 'Item', qty: qty, unitPrice: unit, lineTotal: parseFloat(i.total) || (unit * qty), category: txn.source || '' });
        });
      }
    } catch (e) {}
  }
  return rows;
}
function buildInvoiceBrandHeaderHtml() {
  var hn = (settings && settings.hotelName) ? String(settings.hotelName) : '';
  var logo = (settings && settings.invoiceLogo) ? String(settings.invoiceLogo).trim() : '';
  var addr = (settings && settings.address) ? String(settings.address) : '';
  var phone = (settings && settings.phone) ? String(settings.phone) : '';
  var email = (settings && settings.email) ? String(settings.email) : '';
  if (!logo && !hn && !addr && !phone && !email) return '';
  var html = '<div class="invoice-brand-block">';
  if (logo) html += '<img src="' + escapeHtml(logo) + '" alt="' + escapeHtml(hn || 'Logo') + '">';
  if (hn) html += '<div class="invoice-brand-name">' + escapeHtml(hn) + '</div>';
  if (addr) html += '<div style="font-size:0.8rem;color:var(--text-light);margin-top:0.2rem;">' + escapeHtml(addr) + '</div>';
  if (phone || email) html += '<div style="font-size:0.78rem;color:var(--text-light);">' + escapeHtml([phone, email].filter(Boolean).join(' · ')) + '</div>';
  html += '</div>';
  return html;
}
function getInvoiceQrPayload(inv) {
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
}
function buildInvoiceQrHtml(inv, opts) {
  opts = opts || {};
  var custom = getEffectiveInvoiceQrImage(inv);
  var payload = custom ? '' : getEffectiveInvoiceQrPayload(inv);
  if (!custom && !payload) return opts.editable ? buildInvoiceQrEditorHtml(inv, getInvoiceQrPayload(inv)) : '';
  var imgSrc = custom || buildInvoiceQrImageUrl(payload);
  var cap = custom ? 'Custom QR image' : (payload.length > 52 ? payload.slice(0, 49) + '…' : payload);
  var html = '<div class="invoice-qr-block" id="invoiceQrDisplayBlock">' +
    '<img src="' + escapeHtml(imgSrc) + '" alt="QR code" class="invoice-qr-img" id="invoiceQrDisplayImg">' +
    '<div class="invoice-qr-caption" id="invoiceQrDisplayCaption">' + escapeHtml(cap) + '</div></div>';
  if (opts.editable) html += buildInvoiceQrEditorHtml(inv, payload);
  return html;
}
function getEffectiveInvoiceQrPayload(inv) {
  if (inv && inv.qrTextOverride != null && inv.qrTextOverride !== undefined) return String(inv.qrTextOverride).trim();
  return getInvoiceQrPayload(inv);
}
function getEffectiveInvoiceQrImage(inv) {
  if (inv && inv.qrImageOverride) return String(inv.qrImageOverride).trim();
  if (settings && settings.invoiceQrImage) return String(settings.invoiceQrImage).trim();
  return '';
}
function buildInvoiceQrImageUrl(payload) {
  if (!payload) return '';
  return 'https://api.qrserver.com/v1/create-qr-code/?size=140x140&margin=10&data=' + encodeURIComponent(payload);
}
function buildInvoiceQrEditorHtml(inv, payload) {
  var editVal = (inv && inv.qrTextOverride != null && inv.qrTextOverride !== undefined) ? String(inv.qrTextOverride) : (payload || '');
  return '<div class="invoice-qr-editor post-payment-no-print" id="invoiceQrEditor">' +
    '<div class="invoice-qr-editor-label">Edit QR</div>' +
    '<input type="text" class="form-control invoice-qr-edit-input" id="invoiceQrEditText" value="' + escapeHtml(editVal) + '" placeholder="URL or text for QR code">' +
    '<div class="invoice-qr-editor-actions">' +
    '<input type="file" accept="image/png,image/jpeg,image/webp,image/gif" id="invoiceQrBrowseFile" style="display:none" onchange="invoiceModalQrBrowseChanged(this)">' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById(\'invoiceQrBrowseFile\').click()">Browse…</button>' +
    '<button type="button" class="btn btn-sm btn-primary" onclick="applyInvoiceQrEdit()">Apply</button>' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="resetInvoiceQrEdit()">Reset</button>' +
    '</div>' +
    '<p class="invoice-qr-editor-hint">Override QR for this invoice only. Defaults come from Settings.</p>' +
    '</div>';
}
function persistInvoiceQrOverrides(inv) {
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
}
function refreshInvoiceQrDisplay(inv) {
  if (!inv && window._activeInvoiceQrCtx) inv = window._activeInvoiceQrCtx.inv;
  if (!inv) return;
  var imgEl = document.getElementById('invoiceQrDisplayImg');
  var capEl = document.getElementById('invoiceQrDisplayCaption');
  var blockEl = document.getElementById('invoiceQrDisplayBlock');
  var custom = getEffectiveInvoiceQrImage(inv);
  var payload = custom ? '' : getEffectiveInvoiceQrPayload(inv);
  if (!custom && !payload) {
    if (blockEl) blockEl.style.display = 'none';
    return;
  }
  if (blockEl) blockEl.style.display = '';
  if (imgEl) imgEl.src = custom || buildInvoiceQrImageUrl(payload);
  if (capEl) capEl.textContent = custom ? 'Custom QR image' : (payload.length > 52 ? payload.slice(0, 49) + '…' : payload);
}
function initInvoiceQrEditor(inv) {
  if (!inv) return;
  var txtEl = document.getElementById('invoiceQrEditText');
  if (!txtEl) return;
  if (inv.qrTextOverride != null && inv.qrTextOverride !== undefined) txtEl.value = String(inv.qrTextOverride);
  else txtEl.value = getInvoiceQrPayload(inv);
}
window._activeInvoiceQrCtx = null;
window.applyInvoiceQrEdit = function() {
  var ctx = window._activeInvoiceQrCtx;
  if (!ctx || !ctx.inv) return;
  var inv = ctx.inv;
  var txtEl = document.getElementById('invoiceQrEditText');
  var val = txtEl ? txtEl.value.trim() : '';
  if (val) inv.qrTextOverride = val;
  else delete inv.qrTextOverride;
  delete inv.qrImageOverride;
  var fi = document.getElementById('invoiceQrBrowseFile');
  if (fi) fi.value = '';
  persistInvoiceQrOverrides(inv);
  refreshInvoiceQrDisplay(inv);
  if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'QR updated');
};
window.resetInvoiceQrEdit = function() {
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
};
window.invoiceModalQrBrowseChanged = function(input) {
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
    inv.qrImageOverride = reader.result;
    delete inv.qrTextOverride;
    var txtEl = document.getElementById('invoiceQrEditText');
    if (txtEl) txtEl.value = '';
    persistInvoiceQrOverrides(inv);
    refreshInvoiceQrDisplay(inv);
    if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'QR image updated');
  };
  reader.readAsDataURL(f);
};
function buildInvoiceItemsTableHtml(inv) {
  var rows = getInvoiceLineItems(inv);
  if (!rows.length) return '';
  var itemL = (typeof t === 'function' ? t('g.itemName') : 'Item');
  var qtyL = (typeof t === 'function' ? t('g.quantity') : 'Qty');
  var priceL = (typeof t === 'function' ? t('g.unitPrice') : 'Unit price');
  var totalL = (typeof t === 'function' ? t('g.subtotal') : 'Amount');
  var html = '<table class="invoice-items-table"><thead><tr><th>' + escapeHtml(itemL) + '</th><th>' + escapeHtml(qtyL) + '</th><th>' + escapeHtml(priceL) + '</th><th>' + escapeHtml(totalL) + '</th></tr></thead><tbody>';
  rows.forEach(function(r) {
    html += '<tr><td>' + escapeHtml(String(r.name)) + (r.category ? ' <span style="font-size:0.72rem;color:var(--text-light);">(' + escapeHtml(String(r.category)) + ')</span>' : '') + '</td>';
    html += '<td>' + r.qty + '</td><td>' + fmt$(r.unitPrice) + '</td><td>' + fmt$(r.lineTotal) + '</td></tr>';
  });
  html += '</tbody></table>';
  return html;
}
function updateInvoiceLogoPreview() {
  var el = document.getElementById('sInvoiceLogoPreview');
  if (!el) return;
  var logo = (settings && settings.invoiceLogo) ? String(settings.invoiceLogo) : '';
  el.innerHTML = logo
    ? '<img src="' + escapeHtml(logo) + '" alt="Logo" style="max-height:64px;max-width:180px;object-fit:contain;border:1px solid var(--border);border-radius:6px;padding:0.25rem;background:#fff;">'
    : '<span style="font-size:0.8rem;color:var(--text-light);">No logo uploaded</span>';
}
function updateInvoiceQrPreview() {
  var el = document.getElementById('sInvoiceQrPreview');
  if (!el) return;
  var custom = (settings && settings.invoiceQrImage) ? String(settings.invoiceQrImage).trim() : '';
  if (custom) {
    el.innerHTML = '<img src="' + escapeHtml(custom) + '" alt="QR preview" style="width:96px;height:96px;object-fit:contain;border:1px solid var(--border);border-radius:6px;padding:0.25rem;background:#fff;">';
    return;
  }
  var txtEl = document.getElementById('sInvoiceQrText');
  if (txtEl) settings.invoiceQrText = txtEl.value.trim();
  var payload = getInvoiceQrPayload({ invoiceNumber: 'INV-PREVIEW', paymentTransactionId: 'TXN-PREVIEW', grandTotal: 0 });
  if (!payload) {
    el.innerHTML = '<span style="font-size:0.8rem;color:var(--text-light);">Enter QR text/URL or upload a QR image</span>';
    return;
  }
  var url = 'https://api.qrserver.com/v1/create-qr-code/?size=96x96&margin=8&data=' + encodeURIComponent(payload);
  el.innerHTML = '<img src="' + escapeHtml(url) + '" alt="QR preview" style="width:96px;height:96px;object-fit:contain;border:1px solid var(--border);border-radius:6px;padding:0.25rem;background:#fff;">';
}
window.invoiceLogoFileChanged = function(input) {
  var f = input && input.files && input.files[0];
  if (!f) return;
  if (f.size > 512000) {
    if (typeof toast === 'function') toast('Image too large (max 512 KB)');
    input.value = '';
    return;
  }
  var reader = new FileReader();
  reader.onload = function() {
    settings.invoiceLogo = reader.result;
    save('settings', settings);
    updateInvoiceLogoPreview();
    if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'Settings saved');
  };
  reader.readAsDataURL(f);
};
window.clearInvoiceLogo = function() {
  settings.invoiceLogo = '';
  save('settings', settings);
  var fi = document.getElementById('sInvoiceLogoFile');
  if (fi) fi.value = '';
  updateInvoiceLogoPreview();
  if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'Settings saved');
};
window.invoiceQrFileChanged = function(input) {
  var f = input && input.files && input.files[0];
  if (!f) return;
  if (f.size > 512000) {
    if (typeof toast === 'function') toast('Image too large (max 512 KB)');
    input.value = '';
    return;
  }
  var reader = new FileReader();
  reader.onload = function() {
    settings.invoiceQrImage = reader.result;
    save('settings', settings);
    updateInvoiceQrPreview();
    if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'Settings saved');
  };
  reader.readAsDataURL(f);
};
window.clearInvoiceQrImage = function() {
  settings.invoiceQrImage = '';
  save('settings', settings);
  var fi = document.getElementById('sInvoiceQrFile');
  if (fi) fi.value = '';
  updateInvoiceQrPreview();
  if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'Settings saved');
};
"""

BUILD_INVOICE_OLD = """function buildInvoiceFullScreenBodyHtml(inv, bodyMeta) {
  if (!inv) return '';
  var g = String(inv.guestName || '—');
  var r = String(inv.roomNumber || '—');
  var pre = '';
  if (bodyMeta && bodyMeta.prepaidMode) {
    pre = '<div class="prepaid-invoice-banner" role="note"><strong>' + (typeof t === 'function' ? t('msg.prepaidInvoiceTag') : 'PREPAID INVOICE') + '</strong><br><span class="prepaid-invoice-sub">' + (typeof t === 'function' ? t('msg.prepaidInvoiceNote') : 'Payment pending; print as pro forma if needed.') + '</span></div>';
  }
  return pre + '<p><strong>Guest:</strong> ' + escapeHtml(g) + '</p><p><strong>Room:</strong> ' + escapeHtml(r) + '</p><p><strong>Date:</strong> ' + escapeHtml(String(fmtDate(inv.date))) + '</p><p><strong>Currency:</strong> ' + escapeHtml(String(inv.currency || 'USD')) + '</p>' +
    (inv.billingAddress ? '<p><strong>Billing:</strong> ' + escapeHtml(String(inv.billingAddress)) + '</p>' : '') +
    (inv.bookingId ? '<p><strong>Booking:</strong> ' + escapeHtml(String(inv.bookingId)) + '</p>' : '') +
    '<hr style="margin:1rem 0;border:none;border-top:1px solid var(--border);">' +
    '<p>Subtotal: <strong>' + fmt$(inv.subtotal) + '</strong></p>' +
    ((inv.services || []).length
      ? '<p style="margin-top:0.5rem;font-weight:600;">Services:</p><ul style="list-style:none;margin:0.25rem 0;">' + (inv.services || []).map(function(s) {
        return '<li style="padding:0.2rem 0;">' + (s.icon || '◈') + ' ' + escapeHtml(String(s.name)) + ' x' + (parseInt(s.quantity, 10) || 1) + ' — ' + fmt$((parseFloat(s.unitPrice) || 0) * (parseInt(s.quantity, 10) || 1)) + '</li>';
      }).join('') + '</ul>'
      : '') +
    '<p>Discount: <strong>-' + fmt$(inv.discountAmount) + '</strong></p>' +
    '<p>Tax: <strong>' + fmt$(inv.taxTotal) + '</strong></p>' +
    '<hr style="margin:1rem 0;border:none;border-top:2px solid var(--text);">' +
    '<p style="font-size:1.1rem;"><strong>Grand Total: ' + fmt$(inv.grandTotal) + '</strong></p>' +
    '<p>Status: <span class="status status-' + (inv.paymentStatus === 'Fully Paid' ? 'paid' : inv.paymentStatus === 'Partially Paid' ? 'pending' : 'maintenance') + '">' + escapeHtml(String(inv.paymentStatus || '—')) + '</span></p>' +
    (inv.paymentTransactionId ? '<p style="margin-top:0.5rem;font-size:0.8rem;color:var(--text-light);">Transaction: ' + escapeHtml(String(inv.paymentTransactionId)) + '</p>' : '');
}"""

BUILD_INVOICE_V1 = """function buildInvoiceFullScreenBodyHtml(inv, bodyMeta) {
  if (!inv) return '';
  var g = String(inv.guestName || '—');
  var r = String(inv.roomNumber || '—');
  var pre = '';
  if (bodyMeta && bodyMeta.prepaidMode) {
    pre = '<div class="prepaid-invoice-banner" role="note"><strong>' + (typeof t === 'function' ? t('msg.prepaidInvoiceTag') : 'PREPAID INVOICE') + '</strong><br><span class="prepaid-invoice-sub">' + (typeof t === 'function' ? t('msg.prepaidInvoiceNote') : 'Payment pending; print as pro forma if needed.') + '</span></div>';
  }
  var itemsHtml = buildInvoiceItemsTableHtml(inv);
  return pre + buildInvoiceBrandHeaderHtml() +
    '<p><strong>Guest:</strong> ' + escapeHtml(g) + '</p><p><strong>Room:</strong> ' + escapeHtml(r) + '</p><p><strong>Date:</strong> ' + escapeHtml(String(fmtDate(inv.date))) + '</p><p><strong>Currency:</strong> ' + escapeHtml(String(inv.currency || 'USD')) + '</p>' +
    (inv.billingAddress ? '<p><strong>Billing:</strong> ' + escapeHtml(String(inv.billingAddress)) + '</p>' : '') +
    (inv.bookingId ? '<p><strong>Booking:</strong> ' + escapeHtml(String(inv.bookingId)) + '</p>' : '') +
    (itemsHtml ? '<hr style="margin:1rem 0;border:none;border-top:1px solid var(--border);">' + itemsHtml : '') +
    '<hr style="margin:1rem 0;border:none;border-top:1px solid var(--border);">' +
    '<p>Subtotal: <strong>' + fmt$(inv.subtotal) + '</strong></p>' +
    '<p>Discount: <strong>-' + fmt$(inv.discountAmount) + '</strong></p>' +
    '<p>Tax: <strong>' + fmt$(inv.taxTotal) + '</strong></p>' +
    '<hr style="margin:1rem 0;border:none;border-top:2px solid var(--text);">' +
    '<p style="font-size:1.1rem;"><strong>Grand Total: ' + fmt$(inv.grandTotal) + '</strong></p>' +
    '<p>Status: <span class="status status-' + (inv.paymentStatus === 'Fully Paid' ? 'paid' : inv.paymentStatus === 'Partially Paid' ? 'pending' : 'maintenance') + '">' + escapeHtml(String(inv.paymentStatus || '—')) + '</span></p>' +
    (inv.paymentTransactionId ? '<p style="margin-top:0.5rem;font-size:0.8rem;color:var(--text-light);">Transaction: ' + escapeHtml(String(inv.paymentTransactionId)) + '</p>' : '');
}"""

BUILD_INVOICE_V2 = BUILD_INVOICE_V1.replace(
    "return pre + buildInvoiceBrandHeaderHtml() +",
    "return pre + buildInvoiceBrandHeaderHtml() + buildInvoiceQrHtml(inv, { editable: true }) +",
    1,
)

SHOW_DETAIL_OLD = """    <hr style="margin:1rem 0;border:none;border-top:1px solid var(--border);">
    <p>Subtotal: <strong>${fmt$(inv.subtotal)}</strong></p>
    ${(inv.services||[]).length?'<p style="margin-top:0.5rem;font-weight:600;">Services:</p><ul style="list-style:none;margin:0.25rem 0;">'+inv.services.map(s=>`<li style="padding:0.2rem 0;">${s.icon||'◈'} ${s.name} x${s.quantity||1} — ${fmt$((parseFloat(s.unitPrice)||0)*(parseInt(s.quantity)||1))}</li>`).join('')+'</ul>':''}"""

SHOW_DETAIL_V1 = """    ${buildInvoiceBrandHeaderHtml()}
    ${buildInvoiceItemsTableHtml(inv)}
    <hr style="margin:1rem 0;border:none;border-top:1px solid var(--border);">
    <p>Subtotal: <strong>${fmt$(inv.subtotal)}</strong></p>"""

SHOW_DETAIL_V2 = """    ${buildInvoiceBrandHeaderHtml()}
    ${buildInvoiceQrHtml(inv)}
    ${buildInvoiceItemsTableHtml(inv)}
    <hr style="margin:1rem 0;border:none;border-top:1px solid var(--border);">
    <p>Subtotal: <strong>${fmt$(inv.subtotal)}</strong></p>"""

SETTINGS_ADDR_OLD = """      <div class="form-group"><label>${t('settings.address')}</label><input type="text" class="form-control" id="sAddr" value="${s.address}"></div>
      <h3 style="margin:1.5rem 0 1rem;font-size:1rem;">${t('settings.regulations')}</h3>"""

SETTINGS_INVOICE_V1 = """      <h3 style="margin:1.25rem 0 0.75rem;font-size:1rem;">Invoice</h3>
      <div class="form-group">
        <label>Invoice logo / picture</label>
        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" class="form-control" id="sInvoiceLogoFile" onchange="invoiceLogoFileChanged(this)">
        <div id="sInvoiceLogoPreview" style="margin-top:0.5rem;"></div>
        <button type="button" class="btn btn-sm btn-outline" style="margin-top:0.35rem;" onclick="clearInvoiceLogo()">Remove logo</button>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">Shown at the top of payment and printed invoices (PNG/JPG, max 512 KB).</p>
      </div>
      <h3 style="margin:1.5rem 0 1rem;font-size:1rem;">${t('settings.regulations')}</h3>"""

SETTINGS_INVOICE_V2 = """      <h3 style="margin:1.25rem 0 0.75rem;font-size:1rem;">Invoice</h3>
      <div class="form-group">
        <label>Invoice logo / picture</label>
        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" class="form-control" id="sInvoiceLogoFile" onchange="invoiceLogoFileChanged(this)">
        <div id="sInvoiceLogoPreview" style="margin-top:0.5rem;"></div>
        <button type="button" class="btn btn-sm btn-outline" style="margin-top:0.35rem;" onclick="clearInvoiceLogo()">Remove logo</button>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">Shown at the top of payment and printed invoices (PNG/JPG, max 512 KB).</p>
      </div>
      <div class="form-group" style="margin-top:1rem;">
        <label>Invoice QR code — text or URL</label>
        <input type="text" class="form-control" id="sInvoiceQrText" value="${s.invoiceQrText||''}" placeholder="https://your-hotel.com or payment link" oninput="updateInvoiceQrPreview()">
        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
          <input type="checkbox" id="sInvoiceQrDetails" ${(s.invoiceQrIncludeDetails===false||s.invoiceQrIncludeDetails==='0'||s.invoiceQrIncludeDetails===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          Include invoice number &amp; total in QR
        </label>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">Generated QR appears on each invoice. Upload a custom QR image below to override.</p>
      </div>
      <div class="form-group">
        <label>Custom QR image (optional)</label>
        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" id="sInvoiceQrFile" style="display:none" onchange="invoiceQrFileChanged(this)">
        <div class="invoice-qr-browse-row">
          <button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById('sInvoiceQrFile').click()">Browse…</button>
          <button type="button" class="btn btn-sm btn-outline" onclick="clearInvoiceQrImage()">Remove QR image</button>
        </div>
        <div id="sInvoiceQrPreview" style="margin-top:0.5rem;"></div>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">Default QR for all invoices. Override on a single invoice from the payment receipt screen.</p>
      </div>
      <h3 style="margin:1.5rem 0 1rem;font-size:1rem;">${t('settings.regulations')}</h3>"""

SETTINGS_ADDR_NEW = """      <div class="form-group"><label>${t('settings.address')}</label><input type="text" class="form-control" id="sAddr" value="${s.address}"></div>
""" + SETTINGS_INVOICE_V2

RENDER_SETTINGS_TAIL_OLD = """    </div></div>`;
}
window.saveSettings = function() {"""

RENDER_SETTINGS_TAIL_V1 = """    </div></div>`;
  if (typeof updateInvoiceLogoPreview === 'function') updateInvoiceLogoPreview();
}
window.saveSettings = function() {"""

RENDER_SETTINGS_TAIL_V2 = """    </div></div>`;
  if (typeof updateInvoiceLogoPreview === 'function') updateInvoiceLogoPreview();
  if (typeof updateInvoiceQrPreview === 'function') updateInvoiceQrPreview();
}
window.saveSettings = function() {"""

SAVE_SETTINGS_OLD = """  settings.address = document.getElementById('sAddr').value;
  settings.maxGuests = parseInt(document.getElementById('sMaxG').value)||3;"""

SAVE_SETTINGS_NEW = """  settings.address = document.getElementById('sAddr').value;
  if (document.getElementById('sInvoiceQrText')) settings.invoiceQrText = document.getElementById('sInvoiceQrText').value.trim();
  if (document.getElementById('sInvoiceQrDetails')) settings.invoiceQrIncludeDetails = document.getElementById('sInvoiceQrDetails').checked;
  settings.maxGuests = parseInt(document.getElementById('sMaxG').value)||3;"""

DEFAULT_SETTINGS_OLD = "address:'88 Harbor View Road, Bay City',maxGuests:3"
DEFAULT_SETTINGS_V1 = "address:'88 Harbor View Road, Bay City',invoiceLogo:'',maxGuests:3"
DEFAULT_SETTINGS_V2 = "address:'88 Harbor View Road, Bay City',invoiceLogo:'',invoiceQrText:'',invoiceQrImage:'',invoiceQrIncludeDetails:true,maxGuests:3"

SYNTHETIC_TXN_OLD = """    services: items.map(function(i) {
      return { name: i.name, unitPrice: i.unitPrice, quantity: i.qty, icon: '◆' };
    })
  };
}"""

SYNTHETIC_TXN_NEW = """    services: items.map(function(i) {
      return { name: i.name, unitPrice: i.unitPrice, quantity: i.qty, icon: '◆' };
    }),
    items: items.map(function(i) {
      return { name: i.name, qty: i.qty, unitPrice: i.unitPrice, total: (parseFloat(i.unitPrice) || 0) * (parseInt(i.qty, 10) || 0) };
    })
  };
}"""

V2_BUILD_QR_FN = """function buildInvoiceQrHtml(inv) {
  var custom = (settings && settings.invoiceQrImage) ? String(settings.invoiceQrImage).trim() : '';
  if (custom) {
    return '<div class="invoice-qr-block"><img src="' + escapeHtml(custom) + '" alt="QR code" class="invoice-qr-img"><div class="invoice-qr-caption">Scan QR</div></div>';
  }
  var payload = getInvoiceQrPayload(inv);
  if (!payload) return '';
  var url = 'https://api.qrserver.com/v1/create-qr-code/?size=140x140&margin=10&data=' + encodeURIComponent(payload);
  var cap = payload.length > 52 ? payload.slice(0, 49) + '…' : payload;
  return '<div class="invoice-qr-block"><img src="' + escapeHtml(url) + '" alt="QR code" class="invoice-qr-img"><div class="invoice-qr-caption">' + escapeHtml(cap) + '</div></div>';
}"""

V3_QR_FN_BLOCK = """function buildInvoiceQrHtml(inv, opts) {
  opts = opts || {};
  var custom = getEffectiveInvoiceQrImage(inv);
  var payload = custom ? '' : getEffectiveInvoiceQrPayload(inv);
  if (!custom && !payload) return opts.editable ? buildInvoiceQrEditorHtml(inv, getInvoiceQrPayload(inv)) : '';
  var imgSrc = custom || buildInvoiceQrImageUrl(payload);
  var cap = custom ? 'Custom QR image' : (payload.length > 52 ? payload.slice(0, 49) + '…' : payload);
  var html = '<div class="invoice-qr-block" id="invoiceQrDisplayBlock">' +
    '<img src="' + escapeHtml(imgSrc) + '" alt="QR code" class="invoice-qr-img" id="invoiceQrDisplayImg">' +
    '<div class="invoice-qr-caption" id="invoiceQrDisplayCaption">' + escapeHtml(cap) + '</div></div>';
  if (opts.editable) html += buildInvoiceQrEditorHtml(inv, payload);
  return html;
}
function getEffectiveInvoiceQrPayload(inv) {
  if (inv && inv.qrTextOverride != null && inv.qrTextOverride !== undefined) return String(inv.qrTextOverride).trim();
  return getInvoiceQrPayload(inv);
}
function getEffectiveInvoiceQrImage(inv) {
  if (inv && inv.qrImageOverride) return String(inv.qrImageOverride).trim();
  if (settings && settings.invoiceQrImage) return String(settings.invoiceQrImage).trim();
  return '';
}
function buildInvoiceQrImageUrl(payload) {
  if (!payload) return '';
  return 'https://api.qrserver.com/v1/create-qr-code/?size=140x140&margin=10&data=' + encodeURIComponent(payload);
}
function buildInvoiceQrEditorHtml(inv, payload) {
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
}
function persistInvoiceQrOverrides(inv) {
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
}
function refreshInvoiceQrDisplay(inv) {
  if (!inv && window._activeInvoiceQrCtx) inv = window._activeInvoiceQrCtx.inv;
  if (!inv) return;
  var imgEl = document.getElementById('invoiceQrDisplayImg');
  var capEl = document.getElementById('invoiceQrDisplayCaption');
  var blockEl = document.getElementById('invoiceQrDisplayBlock');
  var custom = getEffectiveInvoiceQrImage(inv);
  var payload = custom ? '' : getEffectiveInvoiceQrPayload(inv);
  if (!custom && !payload) {
    if (blockEl) blockEl.style.display = 'none';
    return;
  }
  if (blockEl) blockEl.style.display = '';
  if (imgEl) imgEl.src = custom || buildInvoiceQrImageUrl(payload);
  if (capEl) capEl.textContent = custom ? 'Custom QR image' : (payload.length > 52 ? payload.slice(0, 49) + '…' : payload);
}
function initInvoiceQrEditor(inv) {
  if (!inv) return;
  var txtEl = document.getElementById('invoiceQrEditText');
  if (!txtEl) return;
  if (inv.qrTextOverride != null && inv.qrTextOverride !== undefined) txtEl.value = String(inv.qrTextOverride);
  else txtEl.value = getInvoiceQrPayload(inv);
}
window._activeInvoiceQrCtx = null;
window.applyInvoiceQrEdit = function() {
  var ctx = window._activeInvoiceQrCtx;
  if (!ctx || !ctx.inv) return;
  var inv = ctx.inv;
  var txtEl = document.getElementById('invoiceQrEditText');
  var val = txtEl ? txtEl.value.trim() : '';
  if (val) inv.qrTextOverride = val;
  else delete inv.qrTextOverride;
  delete inv.qrImageOverride;
  var fi = document.getElementById('invoiceQrBrowseFile');
  if (fi) fi.value = '';
  persistInvoiceQrOverrides(inv);
  refreshInvoiceQrDisplay(inv);
  if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'QR updated');
};
window.resetInvoiceQrEdit = function() {
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
};
window.invoiceModalQrBrowseChanged = function(input) {
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
    inv.qrImageOverride = reader.result;
    delete inv.qrTextOverride;
    var txtEl = document.getElementById('invoiceQrEditText');
    if (txtEl) txtEl.value = '';
    persistInvoiceQrOverrides(inv);
    refreshInvoiceQrDisplay(inv);
    if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'QR image updated');
  };
  reader.readAsDataURL(f);
};"""

OPEN_POST_PAYMENT_OLD = """  body.innerHTML = buildInvoiceFullScreenBodyHtml(useInv, (isPre ? { prepaidMode: true } : null));
  var printL = typeof t === 'function' ? t('msg.postPaymentPrint') : 'Print';"""

OPEN_POST_PAYMENT_NEW = """  window._activeInvoiceQrCtx = { inv: useInv, batchMeta: batchMeta, isPre: !!isPre };
  body.innerHTML = buildInvoiceFullScreenBodyHtml(useInv, (isPre ? { prepaidMode: true } : null));
  if (typeof initInvoiceQrEditor === 'function') initInvoiceQrEditor(useInv);
  var printL = typeof t === 'function' ? t('msg.postPaymentPrint') : 'Print';"""

OPEN_POST_PAYMENT_V2_OLD = """  window._activeInvoiceQrCtx = { inv: useInv };
  body.innerHTML = buildInvoiceFullScreenBodyHtml(useInv, (isPre ? { prepaidMode: true } : null));
  if (typeof initInvoiceQrEditor === 'function') initInvoiceQrEditor(useInv);
  var printL = typeof t === 'function' ? t('msg.postPaymentPrint') : 'Print';"""

PRINT_IFRAME_FN = """window.printPostPaymentInvoice = function() {
  var ctx = window._activeInvoiceQrCtx;
  if (!ctx || !ctx.inv) {
    if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.postPaymentPrint') : 'Nothing to print');
    return;
  }
  var html = buildInvoicePrintDocumentHtml(ctx.inv, ctx.batchMeta || (ctx.isPre ? { prepaidInvoice: true } : null));
  var frame = document.getElementById('hrmmInvoicePrintFrame');
  if (!frame) {
    frame = document.createElement('iframe');
    frame.id = 'hrmmInvoicePrintFrame';
    frame.setAttribute('title', 'Invoice print');
    frame.style.cssText = 'position:fixed;width:0;height:0;border:0;opacity:0;pointer-events:none;left:-9999px;top:0;';
    document.body.appendChild(frame);
  }
  var win = frame.contentWindow;
  var doc = win.document;
  doc.open();
  doc.write(html);
  doc.close();
  function runPrint() {
    try { win.focus(); win.print(); } catch (e) {
      if (typeof toast === 'function') toast('Print failed');
    }
  }
  setTimeout(function() {
    var imgs = doc.querySelectorAll('img');
    if (!imgs.length) { runPrint(); return; }
    var left = imgs.length;
    var fired = false;
    function done() {
      left--;
      if (left <= 0 && !fired) { fired = true; setTimeout(runPrint, 80); }
    }
    for (var i = 0; i < imgs.length; i++) {
      if (imgs[i].complete) done();
      else { imgs[i].addEventListener('load', done); imgs[i].addEventListener('error', done); }
    }
    setTimeout(function() { if (!fired) { fired = true; runPrint(); } }, 2500);
  }, 100);
};"""

PRINT_FN_POPUP_OLD = """window.printPostPaymentInvoice = function() {
  var ctx = window._activeInvoiceQrCtx;
  if (!ctx || !ctx.inv) { window.print(); return; }
  var html = buildInvoicePrintDocumentHtml(ctx.inv, ctx.batchMeta || (ctx.isPre ? { prepaidInvoice: true } : null));
  var w = window.open('', '_blank', 'noopener,noreferrer');
  if (!w) { window.print(); return; }
  w.document.open();
  w.document.write(html);
  w.document.close();
  w.focus();
  setTimeout(function() {
    try { w.print(); } catch (e) { window.print(); }
    setTimeout(function() { try { w.close(); } catch (e2) {} }, 600);
  }, 350);
};"""

PRINT_ONCLICK_OLD = """  document.getElementById('postPaymentInvoicePrint').onclick = function() { window.print(); };"""
PRINT_ONCLICK_V1 = """  document.getElementById('postPaymentInvoicePrint').onclick = function() { if (typeof printPostPaymentInvoice === 'function') printPostPaymentInvoice(); else window.print(); };"""
PRINT_ONCLICK_NEW = """  document.getElementById('postPaymentInvoicePrint').onclick = function() { if (typeof printPostPaymentInvoice === 'function') printPostPaymentInvoice(); };"""

PRINT_JS_ANCHOR = "function getPostPaymentInvoiceOverlayEl() {"
PRINT_JS_BLOCK = """
function buildInvoicePrintBodyHtml(inv, bodyMeta) {
  if (!inv) return '';
  var g = String(inv.guestName || '—');
  var r = String(inv.roomNumber || '—');
  var pre = '';
  if (bodyMeta && bodyMeta.prepaidMode) {
    pre = '<div class="prepaid-invoice-banner" role="note"><strong>' + (typeof t === 'function' ? t('msg.prepaidInvoiceTag') : 'PREPAID INVOICE') + '</strong><br><span class="prepaid-invoice-sub">' + (typeof t === 'function' ? t('msg.prepaidInvoiceNote') : 'Payment pending; print as pro forma if needed.') + '</span></div>';
  }
  var itemsHtml = buildInvoiceItemsTableHtml(inv);
  return pre + buildInvoiceBrandHeaderHtml() + buildInvoiceQrHtml(inv) +
    '<p><strong>Guest:</strong> ' + escapeHtml(g) + '</p><p><strong>Room:</strong> ' + escapeHtml(r) + '</p><p><strong>Date:</strong> ' + escapeHtml(String(fmtDate(inv.date))) + '</p><p><strong>Currency:</strong> ' + escapeHtml(String(inv.currency || 'USD')) + '</p>' +
    (inv.billingAddress ? '<p><strong>Billing:</strong> ' + escapeHtml(String(inv.billingAddress)) + '</p>' : '') +
    (inv.bookingId ? '<p><strong>Booking:</strong> ' + escapeHtml(String(inv.bookingId)) + '</p>' : '') +
    (itemsHtml ? '<hr style="margin:1rem 0;border:none;border-top:1px solid #ccc;">' + itemsHtml : '') +
    '<hr style="margin:1rem 0;border:none;border-top:1px solid #ccc;">' +
    '<p>Subtotal: <strong>' + fmt$(inv.subtotal) + '</strong></p>' +
    '<p>Discount: <strong>-' + fmt$(inv.discountAmount) + '</strong></p>' +
    '<p>Tax: <strong>' + fmt$(inv.taxTotal) + '</strong></p>' +
    '<hr style="margin:1rem 0;border:none;border-top:2px solid #111;">' +
    '<p style="font-size:1.1rem;"><strong>Grand Total: ' + fmt$(inv.grandTotal) + '</strong></p>' +
    '<p>Status: <strong>' + escapeHtml(String(inv.paymentStatus || '—')) + '</strong></p>' +
    (inv.paymentTransactionId ? '<p style="margin-top:0.5rem;font-size:0.8rem;color:#555;">Transaction: ' + escapeHtml(String(inv.paymentTransactionId)) + '</p>' : '');
}
function buildInvoicePrintDocumentHtml(inv, batchMeta) {
  var isPre = batchMeta && batchMeta.prepaidInvoice;
  var title = isPre
    ? (typeof t === 'function' ? t('msg.prepaidInvoiceTitle') : 'Prepaid invoice')
    : (typeof t === 'function' ? t('msg.postPaymentInvoiceTitle') : 'Payment complete');
  var bodyHtml = buildInvoicePrintBodyHtml(inv, (isPre ? { prepaidMode: true } : null));
  var css = 'body{font-family:system-ui,-apple-system,Segoe UI,sans-serif;margin:0;padding:12mm;color:#111;background:#fff;line-height:1.45;}' +
    'h1{font-size:1.15rem;margin:0 0 12px;padding-bottom:8px;border-bottom:2px solid #1a73e8;}' +
    '.invoice-brand-block{text-align:center;margin-bottom:12px;}.invoice-brand-block img{max-height:80px;max-width:240px;object-fit:contain;}' +
    '.invoice-brand-name{font-size:1.15rem;font-weight:700;margin:0.35rem 0 0;}' +
    '.invoice-qr-block{text-align:center;margin:12px 0;}.invoice-qr-img{width:132px;height:132px;object-fit:contain;}' +
    '.invoice-qr-caption{font-size:0.72rem;color:#555;margin-top:4px;word-break:break-word;}' +
    '.invoice-items-table{width:100%;border-collapse:collapse;margin:12px 0;font-size:0.85rem;}' +
    '.invoice-items-table th,.invoice-items-table td{padding:6px;border-bottom:1px solid #ccc;text-align:left;}' +
    '.invoice-items-table th:last-child,.invoice-items-table td:last-child{text-align:right;}' +
    '.invoice-items-table th:nth-child(2),.invoice-items-table td:nth-child(2),.invoice-items-table th:nth-child(3),.invoice-items-table td:nth-child(3){text-align:center;}' +
    '.prepaid-invoice-banner{background:#fff8e1;border:1px solid #e6b800;border-radius:8px;padding:10px;margin-bottom:12px;}' +
    'p{margin:0.35rem 0;} strong{color:#111;} img{-webkit-print-color-adjust:exact;print-color-adjust:exact;}';
  return '<!DOCTYPE html><html><head><meta charset="utf-8"><title>' + escapeHtml(title) + ' · ' + escapeHtml(String(inv.invoiceNumber || '—')) + '</title><style>' + css + '</style></head><body>' +
    '<h1>' + escapeHtml(title) + ' · ' + escapeHtml(String(inv.invoiceNumber || '—')) + '</h1>' + bodyHtml + '</body></html>';
}
""" + PRINT_IFRAME_FN + """
"""

SETTINGS_QR_FILE_OLD = """        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" class="form-control" id="sInvoiceQrFile" onchange="invoiceQrFileChanged(this)">
        <div id="sInvoiceQrPreview" style="margin-top:0.5rem;"></div>
        <button type="button" class="btn btn-sm btn-outline" style="margin-top:0.35rem;" onclick="clearInvoiceQrImage()">Remove QR image</button>"""

SETTINGS_QR_FILE_NEW = """        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" id="sInvoiceQrFile" style="display:none" onchange="invoiceQrFileChanged(this)">
        <div class="invoice-qr-browse-row">
          <button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById('sInvoiceQrFile').click()">Browse…</button>
          <button type="button" class="btn btn-sm btn-outline" onclick="clearInvoiceQrImage()">Remove QR image</button>
        </div>
        <div id="sInvoiceQrPreview" style="margin-top:0.5rem;"></div>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">Default QR for all invoices. Override on a single invoice from the payment receipt screen.</p>"""

BUILD_QR_EDITABLE_OLD = "buildInvoiceBrandHeaderHtml() + buildInvoiceQrHtml(inv) +"
BUILD_QR_EDITABLE_NEW = "buildInvoiceBrandHeaderHtml() + buildInvoiceQrHtml(inv, { editable: true }) +"

PRINT_MEDIA_OLD = """    @media print { .post-payment-invoice-hd, .post-payment-invoice-ft, .prepaid-invoice-banner { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body * { visibility: hidden; } .post-payment-invoice-overlay, .post-payment-invoice-overlay * { visibility: visible; } .post-payment-invoice-overlay { position: absolute; inset: 0; display: block !important; background: #fff; backdrop-filter: none; padding: 0; } .post-payment-invoice-card { max-width: none; box-shadow: none; border: none; } .post-payment-no-print { display: none !important; } }"""

PRINT_MEDIA_NEW = """    @media print {
      /* HRMM-INVOICE-PRINT-v6 — hidden iframe print (no popup blocker blank page) */
      .post-payment-invoice-hd, .prepaid-invoice-banner, .invoice-brand-block, .invoice-qr-block {
        -webkit-print-color-adjust: exact; print-color-adjust: exact;
      }
      body * { visibility: hidden; }
      .post-payment-invoice-overlay, .post-payment-invoice-overlay * { visibility: visible; }
      .post-payment-invoice-overlay {
        position: static !important; inset: auto !important; display: block !important;
        background: #fff !important; backdrop-filter: none !important; padding: 0 !important;
        height: auto !important; max-height: none !important; overflow: visible !important;
      }
      .post-payment-invoice-card {
        max-width: none !important; max-height: none !important; height: auto !important;
        box-shadow: none !important; border: none !important; overflow: visible !important;
        display: block !important; width: 100% !important;
      }
      .post-payment-invoice-body {
        overflow: visible !important; flex: none !important; min-height: auto !important;
        max-height: none !important; height: auto !important; background: #fff !important;
      }
      .post-payment-invoice-ft, .post-payment-no-print, .invoice-qr-editor { display: none !important; }
      .invoice-items-table { break-inside: avoid; page-break-inside: avoid; }
    }"""

PRINT_FIX_MARKER = "HRMM-INVOICE-PRINT-v6"

QR_HELPERS_ANCHOR = "window.clearInvoiceLogo = function() {"
QR_HELPERS_INSERT = """
function getInvoiceQrPayload(inv) {
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
}
function buildInvoiceQrHtml(inv, opts) {
  opts = opts || {};
  var custom = getEffectiveInvoiceQrImage(inv);
  var payload = custom ? '' : getEffectiveInvoiceQrPayload(inv);
  if (!custom && !payload) return opts.editable ? buildInvoiceQrEditorHtml(inv, getInvoiceQrPayload(inv)) : '';
  var imgSrc = custom || buildInvoiceQrImageUrl(payload);
  var cap = custom ? 'Custom QR image' : (payload.length > 52 ? payload.slice(0, 49) + '…' : payload);
  var html = '<div class="invoice-qr-block" id="invoiceQrDisplayBlock">' +
    '<img src="' + escapeHtml(imgSrc) + '" alt="QR code" class="invoice-qr-img" id="invoiceQrDisplayImg">' +
    '<div class="invoice-qr-caption" id="invoiceQrDisplayCaption">' + escapeHtml(cap) + '</div></div>';
  if (opts.editable) html += buildInvoiceQrEditorHtml(inv, payload);
  return html;
}
function getEffectiveInvoiceQrPayload(inv) {
  if (inv && inv.qrTextOverride != null && inv.qrTextOverride !== undefined) return String(inv.qrTextOverride).trim();
  return getInvoiceQrPayload(inv);
}
function getEffectiveInvoiceQrImage(inv) {
  if (inv && inv.qrImageOverride) return String(inv.qrImageOverride).trim();
  if (settings && settings.invoiceQrImage) return String(settings.invoiceQrImage).trim();
  return '';
}
function buildInvoiceQrImageUrl(payload) {
  if (!payload) return '';
  return 'https://api.qrserver.com/v1/create-qr-code/?size=140x140&margin=10&data=' + encodeURIComponent(payload);
}
function buildInvoiceQrEditorHtml(inv, payload) {
  var editVal = (inv && inv.qrTextOverride != null && inv.qrTextOverride !== undefined) ? String(inv.qrTextOverride) : (payload || '');
  return '<div class="invoice-qr-editor post-payment-no-print" id="invoiceQrEditor">' +
    '<div class="invoice-qr-editor-label">Edit QR</div>' +
    '<input type="text" class="form-control invoice-qr-edit-input" id="invoiceQrEditText" value="' + escapeHtml(editVal) + '" placeholder="URL or text for QR code">' +
    '<div class="invoice-qr-editor-actions">' +
    '<input type="file" accept="image/png,image/jpeg,image/webp,image/gif" id="invoiceQrBrowseFile" style="display:none" onchange="invoiceModalQrBrowseChanged(this)">' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById(\'invoiceQrBrowseFile\').click()">Browse…</button>' +
    '<button type="button" class="btn btn-sm btn-primary" onclick="applyInvoiceQrEdit()">Apply</button>' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="resetInvoiceQrEdit()">Reset</button>' +
    '</div>' +
    '<p class="invoice-qr-editor-hint">Override QR for this invoice only. Defaults come from Settings.</p>' +
    '</div>';
}
function persistInvoiceQrOverrides(inv) {
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
}
function refreshInvoiceQrDisplay(inv) {
  if (!inv && window._activeInvoiceQrCtx) inv = window._activeInvoiceQrCtx.inv;
  if (!inv) return;
  var imgEl = document.getElementById('invoiceQrDisplayImg');
  var capEl = document.getElementById('invoiceQrDisplayCaption');
  var blockEl = document.getElementById('invoiceQrDisplayBlock');
  var custom = getEffectiveInvoiceQrImage(inv);
  var payload = custom ? '' : getEffectiveInvoiceQrPayload(inv);
  if (!custom && !payload) {
    if (blockEl) blockEl.style.display = 'none';
    return;
  }
  if (blockEl) blockEl.style.display = '';
  if (imgEl) imgEl.src = custom || buildInvoiceQrImageUrl(payload);
  if (capEl) capEl.textContent = custom ? 'Custom QR image' : (payload.length > 52 ? payload.slice(0, 49) + '…' : payload);
}
function initInvoiceQrEditor(inv) {
  if (!inv) return;
  var txtEl = document.getElementById('invoiceQrEditText');
  if (!txtEl) return;
  if (inv.qrTextOverride != null && inv.qrTextOverride !== undefined) txtEl.value = String(inv.qrTextOverride);
  else txtEl.value = getInvoiceQrPayload(inv);
}
window._activeInvoiceQrCtx = null;
window.applyInvoiceQrEdit = function() {
  var ctx = window._activeInvoiceQrCtx;
  if (!ctx || !ctx.inv) return;
  var inv = ctx.inv;
  var txtEl = document.getElementById('invoiceQrEditText');
  var val = txtEl ? txtEl.value.trim() : '';
  if (val) inv.qrTextOverride = val;
  else delete inv.qrTextOverride;
  delete inv.qrImageOverride;
  var fi = document.getElementById('invoiceQrBrowseFile');
  if (fi) fi.value = '';
  persistInvoiceQrOverrides(inv);
  refreshInvoiceQrDisplay(inv);
  if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'QR updated');
};
window.resetInvoiceQrEdit = function() {
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
};
window.invoiceModalQrBrowseChanged = function(input) {
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
    inv.qrImageOverride = reader.result;
    delete inv.qrTextOverride;
    var txtEl = document.getElementById('invoiceQrEditText');
    if (txtEl) txtEl.value = '';
    persistInvoiceQrOverrides(inv);
    refreshInvoiceQrDisplay(inv);
    if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'QR image updated');
  };
  reader.readAsDataURL(f);
};
function updateInvoiceQrPreview() {
  var el = document.getElementById('sInvoiceQrPreview');
  if (!el) return;
  var custom = (settings && settings.invoiceQrImage) ? String(settings.invoiceQrImage).trim() : '';
  if (custom) {
    el.innerHTML = '<img src="' + escapeHtml(custom) + '" alt="QR preview" style="width:96px;height:96px;object-fit:contain;border:1px solid var(--border);border-radius:6px;padding:0.25rem;background:#fff;">';
    return;
  }
  var txtEl = document.getElementById('sInvoiceQrText');
  if (txtEl) settings.invoiceQrText = txtEl.value.trim();
  var payload = getInvoiceQrPayload({ invoiceNumber: 'INV-PREVIEW', paymentTransactionId: 'TXN-PREVIEW', grandTotal: 0 });
  if (!payload) {
    el.innerHTML = '<span style="font-size:0.8rem;color:var(--text-light);">Enter QR text/URL or upload a QR image</span>';
    return;
  }
  var url = 'https://api.qrserver.com/v1/create-qr-code/?size=96x96&margin=8&data=' + encodeURIComponent(payload);
  el.innerHTML = '<img src="' + escapeHtml(url) + '" alt="QR preview" style="width:96px;height:96px;object-fit:contain;border:1px solid var(--border);border-radius:6px;padding:0.25rem;background:#fff;">';
}
window.invoiceQrFileChanged = function(input) {
  var f = input && input.files && input.files[0];
  if (!f) return;
  if (f.size > 512000) {
    if (typeof toast === 'function') toast('Image too large (max 512 KB)');
    input.value = '';
    return;
  }
  var reader = new FileReader();
  reader.onload = function() {
    settings.invoiceQrImage = reader.result;
    save('settings', settings);
    updateInvoiceQrPreview();
    if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'Settings saved');
  };
  reader.readAsDataURL(f);
};
window.clearInvoiceQrImage = function() {
  settings.invoiceQrImage = '';
  save('settings', settings);
  var fi = document.getElementById('sInvoiceQrFile');
  if (fi) fi.value = '';
  updateInvoiceQrPreview();
  if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.settingsSaved') : 'Settings saved');
};
"""


def _css_block() -> str:
    return CSS.replace("__HRMM_INVOICE_MARKER__", MARKER)


def _strip_old_invoice_css(content: str) -> str:
    return re.sub(
        r"\n\s*/\* HRMM invoice items table[^\n]*\*/\n.*?\n\s*/\* HRMM-INVOICE-v\d+ \*/\n",
        "\n",
        content,
        flags=re.DOTALL,
    )


def _is_fully_patched(content: str) -> bool:
    return (
        MARKER in content
        and "refreshInvoiceQrDisplay" in content
        and "invoiceModalQrBrowseChanged" in content
        and "buildInvoiceQrHtml(inv, { editable: true })" in content
        and "hrmmInvoicePrintFrame" in content
        and PRINT_FIX_MARKER in content
        and "buildInvoicePrintBodyHtml" in content
        and f"/* {MARKER} */" in content
    )


def _apply_print_fix(content: str) -> str:
    if PRINT_MEDIA_OLD in content:
        content = content.replace(PRINT_MEDIA_OLD, PRINT_MEDIA_NEW, 1)
    elif PRINT_FIX_MARKER not in content:
        for old_tag in (
            "/* HRMM-INVOICE-PRINT-v4 — expand body instead of clipping scroll area */",
            "/* HRMM-INVOICE-PRINT-v5 — dedicated print window; keep overlay rules as fallback */",
        ):
            if old_tag in content:
                content = content.replace(
                    old_tag,
                    "/* HRMM-INVOICE-PRINT-v6 — hidden iframe print (no popup blocker blank page) */",
                    1,
                )
                break
    return content


def _apply_print_window(content: str) -> str:
    if PRINT_FN_POPUP_OLD in content:
        content = content.replace(PRINT_FN_POPUP_OLD, PRINT_IFRAME_FN, 1)
    if PRINT_JS_ANCHOR in content and "function buildInvoicePrintBodyHtml" not in content:
        content = content.replace(PRINT_JS_ANCHOR, PRINT_JS_BLOCK + PRINT_JS_ANCHOR, 1)
    if OPEN_POST_PAYMENT_V2_OLD in content:
        content = content.replace(OPEN_POST_PAYMENT_V2_OLD, OPEN_POST_PAYMENT_NEW, 1)
    if PRINT_ONCLICK_V1 in content:
        content = content.replace(PRINT_ONCLICK_V1, PRINT_ONCLICK_NEW, 1)
    elif PRINT_ONCLICK_OLD in content:
        content = content.replace(PRINT_ONCLICK_OLD, PRINT_ONCLICK_NEW, 1)
    return content


def _apply_v3_upgrades(content: str) -> str:
    if V2_BUILD_QR_FN in content and "function buildInvoiceQrHtml(inv, opts)" not in content:
        content = content.replace(V2_BUILD_QR_FN, V3_QR_FN_BLOCK, 1)
    if BUILD_QR_EDITABLE_OLD in content:
        content = content.replace(BUILD_QR_EDITABLE_OLD, BUILD_QR_EDITABLE_NEW, 1)
    if OPEN_POST_PAYMENT_OLD in content:
        content = content.replace(OPEN_POST_PAYMENT_OLD, OPEN_POST_PAYMENT_NEW, 1)
    if SETTINGS_QR_FILE_OLD in content:
        content = content.replace(SETTINGS_QR_FILE_OLD, SETTINGS_QR_FILE_NEW, 1)
    return content


def patch(content: str) -> str:
    content = _apply_print_fix(content)
    content = _apply_print_window(content)

    if _is_fully_patched(content):
        print(f"Already patched {MARKER} — skipping")
        return content

    is_partial = "function getInvoiceLineItems" in content or "buildInvoiceQrHtml" in content

    if not is_partial:
        anchor = "function buildInvoiceFullScreenBodyHtml"
        if anchor not in content:
            raise SystemExit("Could not find buildInvoiceFullScreenBodyHtml anchor")
        content = content.replace(anchor, HELPERS + anchor, 1)
    elif "buildInvoiceQrHtml" not in content and QR_HELPERS_ANCHOR in content:
        content = content.replace(
            QR_HELPERS_ANCHOR,
            QR_HELPERS_INSERT + QR_HELPERS_ANCHOR,
            1,
        )

    content = _apply_v3_upgrades(content)

    if not is_partial or BUILD_INVOICE_OLD in content:
        if BUILD_INVOICE_OLD in content:
            content = content.replace(BUILD_INVOICE_OLD, BUILD_INVOICE_V2, 1)
        elif BUILD_INVOICE_V1 in content and BUILD_QR_EDITABLE_NEW not in content:
            content = content.replace(BUILD_INVOICE_V1, BUILD_INVOICE_V2, 1)
        elif "buildInvoiceQrHtml(inv, { editable: true })" not in content and BUILD_INVOICE_V2 not in content:
            if "buildInvoiceBrandHeaderHtml()" in content:
                pass
            else:
                raise SystemExit("Could not patch buildInvoiceFullScreenBodyHtml for QR")

    if SHOW_DETAIL_OLD in content:
        content = content.replace(SHOW_DETAIL_OLD, SHOW_DETAIL_V2, 1)
    elif SHOW_DETAIL_V1 in content:
        content = content.replace(SHOW_DETAIL_V1, SHOW_DETAIL_V2, 1)

    if SETTINGS_ADDR_OLD in content:
        content = content.replace(SETTINGS_ADDR_OLD, SETTINGS_ADDR_NEW, 1)
    elif SETTINGS_INVOICE_V1 in content:
        content = content.replace(SETTINGS_INVOICE_V1, SETTINGS_INVOICE_V2, 1)

    if RENDER_SETTINGS_TAIL_OLD in content:
        content = content.replace(RENDER_SETTINGS_TAIL_OLD, RENDER_SETTINGS_TAIL_V2, 1)
    elif RENDER_SETTINGS_TAIL_V1 in content:
        content = content.replace(RENDER_SETTINGS_TAIL_V1, RENDER_SETTINGS_TAIL_V2, 1)

    if SAVE_SETTINGS_OLD in content and "sInvoiceQrText" not in content.split(SAVE_SETTINGS_OLD, 1)[1][:200]:
        content = content.replace(SAVE_SETTINGS_OLD, SAVE_SETTINGS_NEW, 1)

    if DEFAULT_SETTINGS_V2.split("invoiceQrText")[0] in content and "invoiceQrText" not in content:
        if DEFAULT_SETTINGS_V1 in content:
            content = content.replace(DEFAULT_SETTINGS_V1, DEFAULT_SETTINGS_V2, 1)
        elif DEFAULT_SETTINGS_OLD in content:
            content = content.replace(DEFAULT_SETTINGS_OLD, DEFAULT_SETTINGS_V2, 1)

    if SYNTHETIC_TXN_OLD in content:
        content = content.replace(SYNTHETIC_TXN_OLD, SYNTHETIC_TXN_NEW, 1)

    content = _strip_old_invoice_css(content)
    if f"/* {MARKER} */" not in content:
        content = content.replace(
            "  </style>\n</head>",
            _css_block() + "\n  </style>\n</head>",
            1,
        )

    content = re.sub(r"<!-- HRMM-INVOICE-v\d+ -->", f"<!-- {MARKER} -->", content)
    if MARKER not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )

    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — invoice items table, logo, QR editor, and print layout fix")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
