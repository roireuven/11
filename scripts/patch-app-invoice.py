#!/usr/bin/env python3
"""Invoice: items table, logo, and QR code on payment receipts."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-INVOICE-v2"
INDEX = Path("public/index.html")

CSS = """
    /* HRMM invoice items table, logo, and QR */
    .invoice-brand-block { text-align: center; margin-bottom: 1rem; }
    .invoice-brand-block img { max-height: 80px; max-width: 240px; object-fit: contain; }
    .invoice-brand-name { font-size: 1.15rem; font-weight: 700; margin: 0.35rem 0 0; }
    .invoice-qr-block { text-align: center; margin: 0.75rem 0 1rem; }
    .invoice-qr-img { width: 132px; height: 132px; object-fit: contain; border: 1px solid var(--border); border-radius: 8px; padding: 0.35rem; background: #fff; }
    .invoice-qr-caption { font-size: 0.72rem; color: var(--text-light); margin-top: 0.35rem; word-break: break-word; max-width: 220px; margin-left: auto; margin-right: auto; }
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
function buildInvoiceQrHtml(inv) {
  var custom = (settings && settings.invoiceQrImage) ? String(settings.invoiceQrImage).trim() : '';
  if (custom) {
    return '<div class="invoice-qr-block"><img src="' + escapeHtml(custom) + '" alt="QR code" class="invoice-qr-img"><div class="invoice-qr-caption">Scan QR</div></div>';
  }
  var payload = getInvoiceQrPayload(inv);
  if (!payload) return '';
  var url = 'https://api.qrserver.com/v1/create-qr-code/?size=140x140&margin=10&data=' + encodeURIComponent(payload);
  var cap = payload.length > 52 ? payload.slice(0, 49) + '…' : payload;
  return '<div class="invoice-qr-block"><img src="' + escapeHtml(url) + '" alt="QR code" class="invoice-qr-img"><div class="invoice-qr-caption">' + escapeHtml(cap) + '</div></div>';
}
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
    "return pre + buildInvoiceBrandHeaderHtml() + buildInvoiceQrHtml(inv) +",
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
        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" class="form-control" id="sInvoiceQrFile" onchange="invoiceQrFileChanged(this)">
        <div id="sInvoiceQrPreview" style="margin-top:0.5rem;"></div>
        <button type="button" class="btn btn-sm btn-outline" style="margin-top:0.35rem;" onclick="clearInvoiceQrImage()">Remove QR image</button>
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
function buildInvoiceQrHtml(inv) {
  var custom = (settings && settings.invoiceQrImage) ? String(settings.invoiceQrImage).trim() : '';
  if (custom) {
    return '<div class="invoice-qr-block"><img src="' + escapeHtml(custom) + '" alt="QR code" class="invoice-qr-img"><div class="invoice-qr-caption">Scan QR</div></div>';
  }
  var payload = getInvoiceQrPayload(inv);
  if (!payload) return '';
  var url = 'https://api.qrserver.com/v1/create-qr-code/?size=140x140&margin=10&data=' + encodeURIComponent(payload);
  var cap = payload.length > 52 ? payload.slice(0, 49) + '…' : payload;
  return '<div class="invoice-qr-block"><img src="' + escapeHtml(url) + '" alt="QR code" class="invoice-qr-img"><div class="invoice-qr-caption">' + escapeHtml(cap) + '</div></div>';
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
        r"\n\s*/\* HRMM invoice[^\n]*\*/\n.*?\n\s*/\* HRMM-INVOICE-v\d+ \*/\n",
        "\n",
        content,
        flags=re.DOTALL,
    )


def _is_fully_patched(content: str) -> bool:
    return (
        MARKER in content
        and "buildInvoiceQrHtml" in content
        and "sInvoiceQrText" in content
        and f"/* {MARKER} */" in content
    )


def patch(content: str) -> str:
    if _is_fully_patched(content):
        print(f"Already patched {MARKER} — skipping")
        return content

    if "function getInvoiceLineItems" not in content:
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

    if BUILD_INVOICE_OLD in content:
        content = content.replace(BUILD_INVOICE_OLD, BUILD_INVOICE_V2, 1)
    elif BUILD_INVOICE_V1 in content:
        content = content.replace(BUILD_INVOICE_V1, BUILD_INVOICE_V2, 1)
    elif "buildInvoiceQrHtml(inv)" not in content and BUILD_INVOICE_V2 not in content:
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
    print(f"Patched {index} — invoice items table, logo, and QR code")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
