#!/usr/bin/env python3
"""Guest QR scan → restaurant self-order screen (restaurant only, not mini-mart)."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "HRMM-GUEST-QR-ORDER-v1"
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

GET_INVOICE_QR_PAYLOAD_NEW = """function guestQrRestaurantOrderEnabled() {
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

UPDATE_QR_PREVIEW_OLD = """  var payload = getInvoiceQrPayload({ invoiceNumber: 'INV-PREVIEW', paymentTransactionId: 'TXN-PREVIEW', grandTotal: 0 });"""

UPDATE_QR_PREVIEW_NEW = """  var payload = getInvoiceQrPayload({ invoiceNumber: 'INV-PREVIEW', paymentTransactionId: 'TXN-PREVIEW', grandTotal: 0, roomNumber: '101', guestName: 'Guest', bookingId: 'BK-PREVIEW' });"""

SETTINGS_QR_DETAILS_OLD = """        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
          <input type="checkbox" id="sInvoiceQrDetails" ${(s.invoiceQrIncludeDetails===false||s.invoiceQrIncludeDetails==='0'||s.invoiceQrIncludeDetails===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          Include invoice number &amp; total in QR
        </label>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">Generated QR appears on each invoice. Upload a custom QR image below to override.</p>"""

SETTINGS_QR_DETAILS_NEW = """        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
          <input type="checkbox" id="sInvoiceQrGuestOrder" ${(s.invoiceQrIncludeRestaurantOrder===false||s.invoiceQrIncludeRestaurantOrder==='0'||s.invoiceQrIncludeRestaurantOrder===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          QR opens guest restaurant order (scan to order food)
        </label>
        <label style="margin-top:0.5rem;display:flex;align-items:center;gap:0.35rem;font-weight:500;font-size:0.88rem;">
          <input type="checkbox" id="sInvoiceQrDetails" ${(s.invoiceQrIncludeDetails===false||s.invoiceQrIncludeDetails==='0'||s.invoiceQrIncludeDetails===0)?'':'checked'} onchange="updateInvoiceQrPreview()">
          Include invoice number &amp; total in QR (when guest order QR is off)
        </label>
        <p style="font-size:0.78rem;color:var(--text-light);margin:0.35rem 0 0;">When guest order is on, the QR links to the restaurant menu for room/table ordering. Optional custom URL above is used as the site base when it starts with http.</p>"""

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
  if (typeof tryBootGuestRestaurantOrder === 'function' && tryBootGuestRestaurantOrder()) { return; }
  if (typeof hotelIsSetupComplete === 'function' && !hotelIsSetupComplete()) { return; }"""

GUEST_ORDER_JS = """
/* HRMM guest QR restaurant order */
var guestRestCart = [];
var guestRestMenuFilter = 'All';
var guestRestCtx = { room: '', guest: '', booking: '', table: '' };
var guestRestSubmitted = false;
(function ensureGuestQrOrderSettingDefault() {
  try {
    if (typeof settings !== 'undefined' && settings && settings.invoiceQrIncludeRestaurantOrder === undefined) {
      settings.invoiceQrIncludeRestaurantOrder = true;
      if (typeof save === 'function') save('settings', settings);
    }
  } catch (e) {}
})();
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
    if (guestRestCtx.guest) bits.push(guestRestCtx.guest);
    if (guestRestCtx.room) bits.push('Room ' + guestRestCtx.room);
    if (guestRestCtx.table) bits.push(String(guestRestCtx.table));
    if (guestRestCtx.booking) bits.push('Booking ' + guestRestCtx.booking);
    sub.textContent = bits.length ? bits.join(' · ') : 'Browse the menu and send your order to the kitchen';
  }
  if (guestRestSubmitted) {
    body.innerHTML = '<div class="guest-rest-success"><div class="guest-rest-success-icon" aria-hidden="true">✓</div><h2>Order sent!</h2><p>Your order was submitted to the kitchen. Staff will prepare it shortly.</p><button type="button" class="btn btn-primary" onclick="guestRestStartNewOrder()">Order more</button></div>';
    return;
  }
  var taxRate = parseFloat(settings && (settings.serviceTax || settings.taxRate)) || 7;
  var categories = ['All'].concat(typeof getMenuCategories === 'function' ? getMenuCategories() : []);
  var tabs = '<div class="guest-rest-tabs">' + categories.map(function(c) {
    var lab = c === 'All' ? 'All' : c;
    return '<button type="button" class="btn btn-sm ' + (guestRestMenuFilter === c ? 'btn-primary' : 'btn-outline') + '" onclick="guestRestMenuFilter=\\'' + String(c).replace(/'/g, "\\\\'") + '\\';renderGuestRestaurantOrder()">' + guestRestEsc(lab) + '</button>';
  }).join('') + '</div>';
  var filtered = (guestRestMenuFilter === 'All' ? menuItems : menuItems.filter(function(m) { return m && m.category === guestRestMenuFilter; })).filter(function(m) {
    return m && m.available !== false && (typeof rowDataVisible !== 'function' || rowDataVisible(m));
  });
  var menuHtml = '<div class="guest-rest-menu-grid">';
  filtered.forEach(function(m) {
    var idEsc = String(m.id).replace(/'/g, "\\\\'");
    menuHtml += '<button type="button" class="guest-rest-menu-card" onclick="guestRestAddToCart(\\'' + idEsc + '\\')"><span class="grmc-name">' + guestRestEsc(m.name) + '</span><span class="grmc-meta">' + guestRestEsc(m.category || '') + '</span><span class="grmc-price">' + fmt$(m.price) + '</span></button>';
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
  body.innerHTML =
    '<div class="guest-rest-layout">' +
      '<section class="guest-rest-panel"><h2>Menu</h2>' + tabs + menuHtml + '</section>' +
      '<section class="guest-rest-panel guest-rest-cart-panel"><h2>Your order <span class="guest-rest-count">' + guestRestCart.length + '</span></h2>' +
        '<div class="guest-rest-cart-items">' + cartHtml + '</div>' +
        '<div class="guest-rest-totals"><div><span>Subtotal</span><span>' + fmt$(subtotal) + '</span></div><div><span>Tax (' + taxRate + '%)</span><span>' + fmt$(tax) + '</span></div><div class="guest-rest-grand"><span>Total</span><span>' + fmt$(grandTotal) + '</span></div></div>' +
        '<label class="guest-rest-notes-label">Notes (optional)<input type="text" class="form-control" id="guestRestOrderNotes" placeholder="Allergies, preferences…"></label>' +
        '<button type="button" class="btn btn-primary guest-rest-submit" ' + (canSend ? '' : 'disabled') + ' onclick="guestRestSubmitOrder()">Send to kitchen</button>' +
      '</section>' +
    '</div>';
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
  var tableNumber = guestRestCtx.table ? String(guestRestCtx.table) : (guestRestCtx.room ? ('Room ' + guestRestCtx.room) : 'QR Guest');
  var order = {
    id: genId(), timestamp: new Date().toISOString(), orderNumber: nextOrderNumber(),
    roomNumber: guestRestCtx.room || '', guestName: guestRestCtx.guest || 'Guest', bookingId: guestRestCtx.booking || '',
    tableNumber: tableNumber, items: items, subtotal: subtotal, tax: tax, grandTotal: grandTotal,
    status: 'Preparing', paidBy: 'Pending', staffName: 'Guest (QR scan)', notes: notes, workPeriodId: wp.id,
    diningFlow: 'kitchen', guestQrOrder: true
  };
  restaurantOrders.push(order);
  try { save('restaurantOrders', restaurantOrders); } catch (e) {}
  try { if (typeof logAudit === 'function') logAudit('New Order', 'Restaurant', order.orderNumber, 'Guest QR order: ' + fmt$(grandTotal) + ' (' + tableNumber + ')'); } catch (e) {}
  guestRestCart = [];
  guestRestSubmitted = true;
  renderGuestRestaurantOrder();
};
window.showGuestRestaurantOrderScreen = function(ctx) {
  guestRestCtx = ctx || guestRestCtx || { room: '', guest: '', booking: '', table: '' };
  guestRestSubmitted = false;
  var ov = document.getElementById('guestRestOrderOverlay');
  var lo = document.getElementById('loginOverlay');
  var so = document.getElementById('setupOverlay');
  var app = document.getElementById('app');
  if (lo) lo.classList.add('hidden');
  if (so) so.classList.add('hidden');
  if (app) app.style.display = 'none';
  if (typeof showBottomNav === 'function') showBottomNav(false);
  if (ov) {
    ov.classList.remove('hidden');
    ov.setAttribute('aria-hidden', 'false');
  }
  document.body.classList.add('guest-rest-order-mode');
  renderGuestRestaurantOrder();
};
window.tryBootGuestRestaurantOrder = function() {
  var params = parseGuestRestaurantOrderParams();
  if (!params) return false;
  guestRestCtx = params;
  try {
    showGuestRestaurantOrderScreen(params);
    var closeBtn = document.getElementById('guestRestOrderCloseBtn');
    if (closeBtn && !closeBtn._guestRestBound) {
      closeBtn._guestRestBound = true;
      closeBtn.addEventListener('click', function() {
        try { history.replaceState(null, '', location.pathname || '/'); } catch (e) {}
        location.reload();
      });
    }
  } catch (e) {
    try { console.warn('guest QR boot', e); } catch (e2) {}
    return false;
  }
  return true;
};
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
    .guest-rest-menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0.5rem; }
    .guest-rest-menu-card { display: flex; flex-direction: column; align-items: flex-start; text-align: left; gap: 0.15rem; border: 1px solid var(--border); border-radius: 10px; padding: 0.65rem; background: var(--card-bg, #fff); cursor: pointer; min-height: 88px; }
    .guest-rest-menu-card:active { transform: scale(0.98); }
    .grmc-name { font-weight: 600; font-size: 0.88rem; line-height: 1.25; }
    .grmc-meta { font-size: 0.72rem; color: var(--text-light); }
    .grmc-price { font-size: 0.85rem; color: var(--primary); font-weight: 700; margin-top: auto; }
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
    /* __HRMM_GUEST_QR_MARKER__ */
"""


def _is_fully_patched(content: str) -> bool:
    return MARKER in content and "tryBootGuestRestaurantOrder" in content and "buildGuestRestaurantOrderUrl" in content


def patch(content: str) -> str:
    if _is_fully_patched(content):
        print(f"Already patched {MARKER} — skipping")
        return content

    if GET_INVOICE_QR_PAYLOAD_OLD not in content and "buildGuestRestaurantOrderUrl" not in content:
        raise SystemExit("Could not find getInvoiceQrPayload anchor")

    if GET_INVOICE_QR_PAYLOAD_OLD in content:
        content = content.replace(GET_INVOICE_QR_PAYLOAD_OLD, GET_INVOICE_QR_PAYLOAD_NEW, 1)

    if UPDATE_QR_PREVIEW_OLD in content:
        content = content.replace(UPDATE_QR_PREVIEW_OLD, UPDATE_QR_PREVIEW_NEW, 1)

    if SETTINGS_QR_DETAILS_OLD in content:
        content = content.replace(SETTINGS_QR_DETAILS_OLD, SETTINGS_QR_DETAILS_NEW, 1)

    if SAVE_SETTINGS_QR_OLD in content:
        content = content.replace(SAVE_SETTINGS_QR_OLD, SAVE_SETTINGS_QR_NEW, 1)

    if LOGIN_OVERLAY_END in content and 'id="guestRestOrderOverlay"' not in content:
        content = content.replace(LOGIN_OVERLAY_END, GUEST_OVERLAY_HTML, 1)

    autologin_anchor = "/* Autologin after all data and i18n helpers are ready. Never show login on top of the first-time setup overlay. */"
    if autologin_anchor in content and "tryBootGuestRestaurantOrder" not in content:
        content = content.replace(autologin_anchor, GUEST_ORDER_JS + autologin_anchor, 1)

    if INIT_AUTOLOGIN_OLD in content:
        content = content.replace(INIT_AUTOLOGIN_OLD, INIT_AUTOLOGIN_NEW, 1)

    if f"/* {MARKER} */" not in content and "/* __HRMM_GUEST_QR_MARKER__ */" not in content:
        content = content.replace(
            "  </style>\n</head>",
            CSS + "\n  </style>\n</head>",
            1,
        )

    if f"<!-- {MARKER} -->" not in content:
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
    print(f"Patched {index} — guest QR restaurant self-order")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
