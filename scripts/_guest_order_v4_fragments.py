# Fragment strings injected into patch-app-guest-qr-order.py — do not import at runtime.

GUEST_ORDER_PARSE_AND_BOOT_V4 = r"""
function parseGuestOrderParams() {
  var sp = (typeof window.hotelBootUrlParams === 'function') ? window.hotelBootUrlParams() : new URLSearchParams(typeof location !== 'undefined' && location.search ? location.search : '');
  var go = sp.get('guestOrder');
  if (go !== 'restaurant' && go !== 'minimart') return null;
  return { dept: go, room: sp.get('room') || '', guest: sp.get('guest') || '', booking: sp.get('booking') || '', table: sp.get('table') || '' };
}
function parseGuestRestaurantOrderParams() {
  var p = parseGuestOrderParams();
  if (!p || p.dept !== 'restaurant') return null;
  return p;
}
window._guestOrderDept = 'restaurant';
var guestMartCart = [];
var guestMartMenuFilter = 'All';
var guestMartCtx = { room: '', guest: '', booking: '', table: '' };
var guestMartSubmitted = false;
function ensureGuestMiniMartStoreLoaded() {
  try { if (typeof load === 'function') storeItems = load('storeItems', storeItems); } catch (e) {}
  if (!Array.isArray(storeItems) || !storeItems.length) {
    if (typeof defaultStoreItems !== 'undefined' && Array.isArray(defaultStoreItems) && defaultStoreItems.length) storeItems = defaultStoreItems.slice();
    else storeItems = [];
  }
  if (!Array.isArray(martOpenOrders)) martOpenOrders = [];
}
function ensureGuestMiniMartWorkPeriod() {
  try {
    if (typeof load === 'function') { workPeriods = load('workPeriods', workPeriods); if (!Array.isArray(workPeriods)) workPeriods = []; }
  } catch (e) {}
  var wp = typeof getActiveWorkPeriod === 'function' ? getActiveWorkPeriod('Mini-Mart') : null;
  if (wp) return wp;
  wp = { id: genId(), dept: 'Mini-Mart', startTime: new Date().toISOString(), endTime: null, openingCash: 0, closingCash: null, cashVariance: null, status: 'Open', userId: '', userName: 'Guest QR', closedBy: '' };
  if (!Array.isArray(workPeriods)) workPeriods = [];
  workPeriods.push(wp);
  try { if (typeof save === 'function') save('workPeriods', workPeriods); } catch (e) {}
  return wp;
}
function renderGuestMiniMartOrder() {
  var body = document.getElementById('guestRestOrderBody');
  var sub = document.getElementById('guestRestOrderSub');
  var title = document.getElementById('guestRestOrderTitle');
  if (!body) return;
  ensureGuestMiniMartStoreLoaded();
  var hn = (settings && settings.hotelName) ? String(settings.hotelName) : 'Mini-Mart';
  if (title) title.textContent = hn + ' — Shop';
  if (sub) {
    var bits = [];
    if (guestMartCtx.guest) bits.push(guestMartCtx.guest);
    if (guestMartCtx.room) bits.push('Room ' + guestMartCtx.room);
    if (guestMartCtx.table) bits.push(String(guestMartCtx.table));
    if (guestMartCtx.booking) bits.push('Booking ' + guestMartCtx.booking);
    sub.textContent = bits.length ? bits.join(' · ') : 'Browse items and submit your order';
  }
  if (guestMartSubmitted) {
    body.innerHTML = '<div class="guest-rest-success"><div class="guest-rest-success-icon" aria-hidden="true">✓</div><h2>Order submitted!</h2><p>Your mini-mart order was sent. Staff will prepare it for pickup or delivery.</p><button type="button" class="btn btn-primary" onclick="guestMartStartNewOrder()">Order more</button></div>';
    return;
  }
  var taxRate = parseFloat(settings && (settings.surcharge || settings.taxRate)) || 7;
  var categories = ['All'].concat(typeof getStoreCategories === 'function' ? getStoreCategories() : []);
  var searchQ = String(guestOrderMenuSearch || '').trim();
  var searchHtml = '<div class="guest-rest-search"><input type="search" class="form-control" placeholder="Search items…" value="' + guestRestEsc(searchQ) + '" oninput="guestOrderMenuSearch=this.value;renderGuestOrderScreen()" autocomplete="off"></div>';
  var tabs = '<div class="guest-rest-tabs">' + categories.map(function(c) {
    return '<button type="button" class="btn btn-sm ' + (guestMartMenuFilter === c ? 'btn-primary' : 'btn-outline') + '" onclick="guestMartMenuFilter=\'' + String(c).replace(/'/g, "\\'") + '\';renderGuestOrderScreen()">' + guestRestEsc(c === 'All' ? 'All' : c) + '</button>';
  }).join('') + '</div>';
  var filtered = (guestMartMenuFilter === 'All' ? storeItems : storeItems.filter(function(m) { return m && m.category === guestMartMenuFilter; })).filter(function(m) {
    return m && m.available !== false && (typeof rowDataVisible !== 'function' || rowDataVisible(m)) && guestRestMenuMatchesSearch(m, searchQ);
  });
  var menuHtml = '<div class="guest-rest-menu-grid">';
  filtered.forEach(function(m) {
    var idEsc = String(m.id).replace(/'/g, "\\'");
    menuHtml += guestRestMenuCardHtml(m, idEsc, 'guestMartAddToCart', true);
  });
  if (!filtered.length) menuHtml += '<div class="guest-rest-empty">No items available right now.</div>';
  menuHtml += '</div>';
  var cartHtml = '', subtotal = 0;
  guestMartCart.forEach(function(ci, idx) {
    var line = (parseFloat(ci.unitPrice) || 0) * (parseInt(ci.qty, 10) || 0);
    subtotal += line;
    cartHtml += '<div class="guest-rest-cart-row"><span>' + guestRestEsc(ci.name) + '</span><div class="guest-rest-qty"><button type="button" onclick="guestMartCartQty(' + idx + ',-1)">−</button><span>' + ci.qty + '</span><button type="button" onclick="guestMartCartQty(' + idx + ',1)">+</button></div><span>' + fmt$(line) + '</span><button type="button" class="guest-rest-remove" onclick="guestMartCartRemove(' + idx + ')">✕</button></div>';
  });
  if (!cartHtml) cartHtml = '<div class="guest-rest-cart-empty">Tap items to add them to your cart</div>';
  var tax = Math.round((subtotal * (taxRate / 100)) * 100) / 100;
  var grandTotal = Math.round((subtotal + tax) * 100) / 100;
  var canSubmit = guestMartCart.length > 0;
  var mobileBar = guestRestMobileBarHtml(guestMartCart.length, grandTotal, 'guestMartSubmitOrder', 'Submit order', canSubmit);
  body.innerHTML =
    '<div class="guest-rest-layout">' +
      '<section class="guest-rest-panel"><h2>Shop</h2>' + searchHtml + tabs + menuHtml + '</section>' +
      '<section class="guest-rest-panel guest-rest-cart-panel" id="guestRestCartPanel"><h2>Your cart <span class="guest-rest-count">' + guestMartCart.length + '</span></h2>' +
        '<div class="guest-rest-cart-items">' + cartHtml + '</div>' +
        '<div class="guest-rest-totals"><div><span>Subtotal</span><span>' + fmt$(subtotal) + '</span></div><div><span>Tax (' + taxRate + '%)</span><span>' + fmt$(tax) + '</span></div><div class="guest-rest-grand"><span>Total</span><span>' + fmt$(grandTotal) + '</span></div></div>' +
        '<button type="button" class="btn btn-primary guest-rest-submit" ' + (canSubmit ? '' : 'disabled') + ' onclick="guestMartSubmitOrder()">Submit order</button>' +
      '</section>' +
    '</div>' + mobileBar;
}
window.guestMartAddToCart = function(id) {
  ensureGuestMiniMartStoreLoaded();
  var it = storeItems.find(function(x) { return x && x.id === id; });
  if (!it || it.available === false) return;
  var ex = guestMartCart.find(function(c) { return c.storeItemId === id; });
  if (ex) ex.qty++; else guestMartCart.push({ storeItemId: id, name: it.name, unitPrice: it.price, qty: 1 });
  renderGuestMiniMartOrder();
};
window.guestMartCartQty = function(idx, delta) {
  var ci = guestMartCart[idx]; if (!ci) return;
  ci.qty += delta; if (ci.qty <= 0) guestMartCart.splice(idx, 1);
  renderGuestMiniMartOrder();
};
window.guestMartCartRemove = function(idx) { guestMartCart.splice(idx, 1); renderGuestMiniMartOrder(); };
window.guestMartStartNewOrder = function() { guestMartSubmitted = false; guestMartCart = []; renderGuestMiniMartOrder(); };
window.guestMartSubmitOrder = function() {
  if (!guestMartCart.length) return;
  ensureGuestMiniMartStoreLoaded();
  ensureGuestMiniMartWorkPeriod();
  var tr = parseFloat(settings && (settings.surcharge || settings.taxRate)) || 7;
  var lines = guestMartCart.map(function(ci) { return { storeItemId: ci.storeItemId, name: ci.name, unitPrice: ci.unitPrice, qty: ci.qty }; });
  var saleItems = lines.map(function(ci) { return { itemId: ci.storeItemId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice }; });
  var totals = computeLineTotalsFromRawLineItems(saleItems, tr);
  var orderNum = typeof martNextMiniMartOrderNumber === 'function' ? martNextMiniMartOrderNumber() : ('MM-' + Date.now());
  var order = {
    id: genId(), orderNumber: orderNum, timestamp: new Date().toISOString(),
    roomNumber: guestMartCtx.room || '—', guestName: guestMartCtx.guest || 'Walk-in', bookingId: guestMartCtx.booking || '',
    source: 'guestQr', items: lines, subtotal: totals.subtotal, tax: totals.taxAmount, grandTotal: totals.grandTotal,
    status: 'Open', paidBy: 'Pending', staffName: 'Guest (QR scan)', guestQrOrder: true
  };
  martOpenOrders.push(order);
  try { save('martOpenOrders', martOpenOrders); } catch (e) {}
  try { if (typeof logAudit === 'function') logAudit('Insert', 'martOpenOrders', order.id, 'Guest QR mini-mart order ' + orderNum); } catch (e) {}
  guestMartCart = []; guestMartSubmitted = true; renderGuestMiniMartOrder();
};
function renderGuestOrderScreen() {
  if (window._guestOrderDept === 'minimart') renderGuestMiniMartOrder();
  else renderGuestRestaurantOrder();
}
function bindGuestOrderCloseOnce() {
  var closeBtn = document.getElementById('guestRestOrderCloseBtn');
  if (closeBtn && !closeBtn._guestRestBound) {
    closeBtn._guestRestBound = true;
    closeBtn.addEventListener('click', function() {
      try { history.replaceState(null, '', location.pathname || '/'); } catch (e) {}
      location.reload();
    });
  }
}
window.showGuestOrderScreen = function(dept, ctx) {
  window._guestOrderDept = dept === 'minimart' ? 'minimart' : 'restaurant';
  ctx = ctx || {};
  if (window._guestOrderDept === 'minimart') {
    guestMartCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '' };
    guestMartSubmitted = false;
  } else {
    guestRestCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '' };
    guestRestSubmitted = false;
  }
  var ov = document.getElementById('guestRestOrderOverlay');
  var lo = document.getElementById('loginOverlay');
  var so = document.getElementById('setupOverlay');
  var app = document.getElementById('app');
  if (lo) lo.classList.add('hidden');
  if (so) so.classList.add('hidden');
  if (app) app.style.display = 'none';
  if (typeof showBottomNav === 'function') showBottomNav(false);
  if (ov) { ov.classList.remove('hidden'); ov.setAttribute('aria-hidden', 'false'); }
  document.body.classList.add('guest-rest-order-mode');
  renderGuestOrderScreen();
  bindGuestOrderCloseOnce();
};
"""

# Standalone repair block — must match renderGuestMiniMartOrder() inside GUEST_ORDER_PARSE_AND_BOOT_V4.
RENDER_GUEST_MINIMART_ORDER_V7 = r"""function renderGuestMiniMartOrder() {
  var body = document.getElementById('guestRestOrderBody');
  var sub = document.getElementById('guestRestOrderSub');
  var title = document.getElementById('guestRestOrderTitle');
  if (!body) return;
  ensureGuestMiniMartStoreLoaded();
  var hn = (settings && settings.hotelName) ? String(settings.hotelName) : 'Mini-Mart';
  if (title) title.textContent = hn + ' — Shop';
  if (sub) {
    var bits = [];
    if (guestMartCtx.guest) bits.push(guestMartCtx.guest);
    if (guestMartCtx.room) bits.push('Room ' + guestMartCtx.room);
    if (guestMartCtx.table) bits.push(String(guestMartCtx.table));
    if (guestMartCtx.booking) bits.push('Booking ' + guestMartCtx.booking);
    sub.textContent = bits.length ? bits.join(' · ') : 'Browse items and submit your order';
  }
  if (guestMartSubmitted) {
    body.innerHTML = '<div class="guest-rest-success"><div class="guest-rest-success-icon" aria-hidden="true">✓</div><h2>Order submitted!</h2><p>Your mini-mart order was sent. Staff will prepare it for pickup or delivery.</p><button type="button" class="btn btn-primary" onclick="guestMartStartNewOrder()">Order more</button></div>';
    return;
  }
  var taxRate = parseFloat(settings && (settings.surcharge || settings.taxRate)) || 7;
  var categories = ['All'].concat(typeof getStoreCategories === 'function' ? getStoreCategories() : []);
  var searchQ = String(guestOrderMenuSearch || '').trim();
  var searchHtml = '<div class="guest-rest-search"><input type="search" class="form-control" placeholder="Search items…" value="' + guestRestEsc(searchQ) + '" oninput="guestOrderMenuSearch=this.value;renderGuestOrderScreen()" autocomplete="off"></div>';
  var tabs = '<div class="guest-rest-tabs">' + categories.map(function(c) {
    return '<button type="button" class="btn btn-sm ' + (guestMartMenuFilter === c ? 'btn-primary' : 'btn-outline') + '" onclick="guestMartMenuFilter=\'' + String(c).replace(/'/g, "\\'") + '\';renderGuestOrderScreen()">' + guestRestEsc(c === 'All' ? 'All' : c) + '</button>';
  }).join('') + '</div>';
  var filtered = (guestMartMenuFilter === 'All' ? storeItems : storeItems.filter(function(m) { return m && m.category === guestMartMenuFilter; })).filter(function(m) {
    return m && m.available !== false && (typeof rowDataVisible !== 'function' || rowDataVisible(m)) && guestRestMenuMatchesSearch(m, searchQ);
  });
  var menuHtml = '<div class="guest-rest-menu-grid">';
  filtered.forEach(function(m) {
    var idEsc = String(m.id).replace(/'/g, "\\'");
    menuHtml += guestRestMenuCardHtml(m, idEsc, 'guestMartAddToCart', true);
  });
  if (!filtered.length) menuHtml += '<div class="guest-rest-empty">No items available right now.</div>';
  menuHtml += '</div>';
  var cartHtml = '', subtotal = 0;
  guestMartCart.forEach(function(ci, idx) {
    var line = (parseFloat(ci.unitPrice) || 0) * (parseInt(ci.qty, 10) || 0);
    subtotal += line;
    cartHtml += '<div class="guest-rest-cart-row"><span>' + guestRestEsc(ci.name) + '</span><div class="guest-rest-qty"><button type="button" onclick="guestMartCartQty(' + idx + ',-1)">−</button><span>' + ci.qty + '</span><button type="button" onclick="guestMartCartQty(' + idx + ',1)">+</button></div><span>' + fmt$(line) + '</span><button type="button" class="guest-rest-remove" onclick="guestMartCartRemove(' + idx + ')">✕</button></div>';
  });
  if (!cartHtml) cartHtml = '<div class="guest-rest-cart-empty">Tap items to add them to your cart</div>';
  var tax = Math.round((subtotal * (taxRate / 100)) * 100) / 100;
  var grandTotal = Math.round((subtotal + tax) * 100) / 100;
  var canSubmit = guestMartCart.length > 0;
  var mobileBar = guestRestMobileBarHtml(guestMartCart.length, grandTotal, 'guestMartSubmitOrder', 'Submit order', canSubmit);
  body.innerHTML =
    '<div class="guest-rest-layout">' +
      '<section class="guest-rest-panel"><h2>Shop</h2>' + searchHtml + tabs + menuHtml + '</section>' +
      '<section class="guest-rest-panel guest-rest-cart-panel" id="guestRestCartPanel"><h2>Your cart <span class="guest-rest-count">' + guestMartCart.length + '</span></h2>' +
        '<div class="guest-rest-cart-items">' + cartHtml + '</div>' +
        '<div class="guest-rest-totals"><div><span>Subtotal</span><span>' + fmt$(subtotal) + '</span></div><div><span>Tax (' + taxRate + '%)</span><span>' + fmt$(tax) + '</span></div><div class="guest-rest-grand"><span>Total</span><span>' + fmt$(grandTotal) + '</span></div></div>' +
        '<button type="button" class="btn btn-primary guest-rest-submit" ' + (canSubmit ? '' : 'disabled') + ' onclick="guestMartSubmitOrder()">Submit order</button>' +
      '</section>' +
    '</div>' + mobileBar;
}"""

GUEST_ORDER_BOOT_V4 = r"""
window.showGuestRestaurantOrderScreen = function(ctx) {
  showGuestOrderScreen('restaurant', ctx);
};
window.tryBootGuestOrderFromUrl = function() {
  var params = parseGuestOrderParams();
  if (!params) return false;
  try {
    showGuestOrderScreen(params.dept || 'restaurant', params);
    bindGuestOrderCloseOnce();
  } catch (e) {
    try { console.warn('guest QR boot', e); } catch (e2) {}
    return false;
  }
  return true;
};
window.tryBootGuestRestaurantOrder = window.tryBootGuestOrderFromUrl;
"""
