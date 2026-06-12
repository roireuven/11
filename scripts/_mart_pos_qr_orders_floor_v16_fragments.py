"""Mini-Mart + POS — Room Service and QR order numbers 1–60 floor (like Restaurant)."""

MART_POS_STATE = r"""let martOrderType = 'Room Service';
let martOrderNum = '';
let martFocusAllOrderNums = true;
let posOrderType = 'Room Service';
let posOrderNum = '';
let posFocusAllOrderNums = true;
"""

MART_POS_HELPERS = r"""
function deptQrMartOrderIsOpen(o) {
  return o && rowDataVisible(o) && (o.status === 'Open' || !o.status);
}
function deptQrPosOrderIsOpen(o) {
  return o && rowDataVisible(o) && (o.status === 'Open' || !o.status);
}
function deptQrExtractSlotFromOrder(o) {
  if (typeof guestQrExtractOrderNum === 'function') {
    var ex = guestQrExtractOrderNum(o);
    if (ex != null) return ex;
  }
  var m = /^Order #(\d+)$/i.exec(String(o.guestName || '').trim());
  if (m) return parseInt(m[1], 10);
  m = /^Order #(\d+)$/i.exec(String(o.roomNumber || '').trim());
  if (m) return parseInt(m[1], 10);
  return null;
}
function martGetOrdersForOrderNum(slotNum) {
  var n = parseInt(slotNum, 10);
  if (isNaN(n) || n < 1 || n > 60) return [];
  try { martOpenOrders = load('martOpenOrders', martOpenOrders); } catch (e) {}
  return (martOpenOrders || []).filter(function(o) {
    if (!deptQrMartOrderIsOpen(o)) return false;
    return deptQrExtractSlotFromOrder(o) === n;
  });
}
function posGetOrdersForOrderNum(slotNum) {
  var n = parseInt(slotNum, 10);
  if (isNaN(n) || n < 1 || n > 60) return [];
  try { posOpenOrders = load('posOpenOrders', posOpenOrders); } catch (e) {}
  return (posOpenOrders || []).filter(function(o) {
    if (!deptQrPosOrderIsOpen(o)) return false;
    return deptQrExtractSlotFromOrder(o) === n;
  });
}
function martGetActiveOrderNumOrdersTotal(slotNum) {
  return Math.round(martGetOrdersForOrderNum(slotNum).reduce(function(s, o) { return s + (parseFloat(o && o.grandTotal) || 0); }, 0) * 100) / 100;
}
function posGetActiveOrderNumOrdersTotal(slotNum) {
  return Math.round(posGetOrdersForOrderNum(slotNum).reduce(function(s, o) { return s + (parseFloat(o && o.grandTotal) || 0); }, 0) * 100) / 100;
}
function martGetOrderNumFloorState(slotNum) {
  var active = martGetOrdersForOrderNum(slotNum);
  if (!active.length) return 'available';
  return 'pending';
}
function posGetOrderNumFloorState(slotNum) {
  var active = posGetOrdersForOrderNum(slotNum);
  if (!active.length) return 'available';
  return 'pending';
}
function guestMartRecalcOpenOrderTotals(order, taxRate) {
  var saleItems = (order.items || []).map(function(ci) {
    return { itemId: ci.storeItemId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice };
  });
  var totals = computeLineTotalsFromRawLineItems(saleItems, taxRate);
  order.subtotal = totals.subtotal;
  order.tax = totals.taxAmount;
  order.grandTotal = totals.grandTotal;
}
function guestMartMergeCartIntoOrder(order, newItems, taxRate) {
  newItems.forEach(function(ni) {
    var ex = (order.items || []).find(function(i) {
      return String(i.storeItemId || '') === String(ni.storeItemId || '') && (parseFloat(i.unitPrice) || 0) === (parseFloat(ni.unitPrice) || 0);
    });
    if (ex) ex.qty = (parseInt(ex.qty, 10) || 0) + (parseInt(ni.qty, 10) || 0);
    else {
      if (!order.items) order.items = [];
      order.items.push({ storeItemId: ni.storeItemId, name: ni.name, qty: ni.qty, unitPrice: ni.unitPrice });
    }
  });
  guestMartRecalcOpenOrderTotals(order, taxRate);
}
function guestMartFindOrderNumMergeTarget(orderNum) {
  var n = parseInt(String(orderNum || '').trim(), 10);
  if (isNaN(n)) return null;
  var list = martGetOrdersForOrderNum(n);
  if (!list.length) return null;
  list = list.slice().sort(function(a, b) {
    try { return new Date(b.timestamp) - new Date(a.timestamp); } catch (e) { return 0; }
  });
  return list[0] || null;
}
function guestPosRecalcOpenOrderTotals(order, taxRate) {
  var saleItems = (order.items || []).map(function(ci) {
    return { itemId: ci.inventoryId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice };
  });
  var totals = computeLineTotalsFromRawLineItems(saleItems, taxRate);
  order.subtotal = totals.subtotal;
  order.tax = totals.taxAmount;
  order.grandTotal = totals.grandTotal;
}
function guestPosMergeCartIntoOrder(order, newItems, taxRate) {
  newItems.forEach(function(ni) {
    var ex = (order.items || []).find(function(i) {
      return String(i.inventoryId || '') === String(ni.inventoryId || '') && (parseFloat(i.unitPrice) || 0) === (parseFloat(ni.unitPrice) || 0);
    });
    if (ex) ex.qty = (parseInt(ex.qty, 10) || 0) + (parseInt(ni.qty, 10) || 0);
    else {
      if (!order.items) order.items = [];
      order.items.push({ inventoryId: ni.inventoryId, name: ni.name, qty: ni.qty, unitPrice: ni.unitPrice, category: ni.category });
    }
  });
  guestPosRecalcOpenOrderTotals(order, taxRate);
}
function guestPosFindOrderNumMergeTarget(orderNum) {
  var n = parseInt(String(orderNum || '').trim(), 10);
  if (isNaN(n)) return null;
  var list = posGetOrdersForOrderNum(n);
  if (!list.length) return null;
  list = list.slice().sort(function(a, b) {
    try { return new Date(b.timestamp) - new Date(a.timestamp); } catch (e) { return 0; }
  });
  return list[0] || null;
}
function martNotifyOrderNumUpdate(orderNum) {
  try { window.dispatchEvent(new CustomEvent('hotel-sync-martOpenOrders')); } catch (e) {}
  try {
    var nav = document.querySelector('#sidebarNav a[data-page="minimart"]');
    if (!nav || !nav.classList.contains('active') || typeof renderMiniMart !== 'function') return;
    if (martOrderType === 'QR Orders') {
      if (martFocusAllOrderNums) { renderMiniMart(); return; }
      if (parseInt(String(martOrderNum || '').trim(), 10) === parseInt(String(orderNum || '').trim(), 10)) renderMiniMart();
    }
  } catch (e) {}
}
function posNotifyOrderNumUpdate(orderNum) {
  try { window.dispatchEvent(new CustomEvent('hotel-sync-posOpenOrders')); } catch (e) {}
  try {
    var nav = document.querySelector('#sidebarNav a[data-page="pos"]');
    if (!nav || !nav.classList.contains('active') || typeof renderPOS !== 'function') return;
    if (posOrderType === 'QR Orders') {
      if (posFocusAllOrderNums) { renderPOS(); return; }
      if (parseInt(String(posOrderNum || '').trim(), 10) === parseInt(String(orderNum || '').trim(), 10)) renderPOS();
    }
  } catch (e) {}
}
function renderDeptOrderNumFloorHtml(cfg) {
  var getState = cfg.getState;
  var getTotal = cfg.getTotal;
  var clickFn = cfg.clickFn;
  var focusAll = cfg.focusAll;
  var orderNum = cfg.orderNum;
  var nAvail = 0, nOcc = 0, nPend = 0;
  for (var i = 1; i <= 60; i++) {
    var s0 = getState(i);
    if (s0 === 'available') nAvail++;
    else if (s0 === 'pending') nPend++;
    else nOcc++;
  }
  var floorHtml = '<div class="rest-floor-wrap">';
  floorHtml += '<div class="rest-floor-head"><div class="rest-floor-title-actions"><h3>' + t('restaurant.orderNumFloorTitle') + '</h3></div>';
  floorHtml += '<div class="rest-floor-summary" role="status" aria-live="polite">';
  floorHtml += '<span class="rfs rfs-free"><strong>' + nAvail + '</strong> ' + t('restaurant.wordFree') + '</span>';
  floorHtml += '<span class="rfs rfs-busy"><strong>' + nOcc + '</strong> ' + t('restaurant.wordLive') + '</span>';
  floorHtml += '<span class="rfs rfs-due"><strong>' + nPend + '</strong> ' + t('restaurant.wordPay') + '</span>';
  floorHtml += '</div></div>';
  floorHtml += '<div class="rest-floor-legend">' +
    '<span><span class="rest-floor-dot avail" aria-hidden="true"></span>' + t('restaurant.legendFree') + '</span>' +
    '<span><span class="rest-floor-dot occ" aria-hidden="true"></span>' + t('restaurant.legendOpen') + '</span>' +
    '<span><span class="rest-floor-dot pend" aria-hidden="true"></span>' + t('restaurant.legendPay') + '</span>' +
    '</div>';
  floorHtml += '<div class="rest-order-num-floor" role="group" aria-label="' + String(t('restaurant.orderNumFloorGroup')).replace(/"/g, '&quot;') + '">';
  for (var n = 1; n <= 60; n++) {
    var st = getState(n);
    var tag = st === 'available' ? t('restaurant.tagOpen') : (st === 'pending' ? t('restaurant.tagPay') : t('restaurant.tagLive'));
    var sel = (!focusAll && parseInt(String(orderNum || '').trim(), 10) === n) ? ' selected' : '';
    var actSumStr = fmt$(getTotal(n));
    var title = (st === 'available' ? t('restaurant.tileTitleOrderAvail', { n: String(n) }) : (st === 'pending' ? t('restaurant.tileTitleOrderPay', { n: String(n) }) : t('restaurant.tileTitleOrderLive', { n: String(n) }))) + ' — ' + actSumStr;
    floorHtml += '<button type="button" class="rest-table-tile rest-order-num-tile ' + st + sel + '" onclick="' + clickFn + '(' + n + ')" title="' + title.replace(/"/g, '&quot;') + '">' +
      '<span class="rtt-num">#' + n + '</span>' +
      '<span class="rtt-sumline"><span class="rtt-slab">' + t('minimart.totalActiveLabel') + '</span> <span class="rtt-total">' + actSumStr + '</span></span>' +
      '<span class="rtt-tag">' + tag + '</span></button>';
  }
  floorHtml += '</div>';
  floorHtml += '<p style="font-size:0.76rem;color:var(--text-light);margin:0.45rem 0 0;line-height:1.45;">' + t('restaurant.orderNumFloorHelp', { free: '<strong style="color:#2e7d32;">' + t('restaurant.wordFree') + '</strong>', live: '<strong style="color:#c62828;">' + t('restaurant.wordLive') + '</strong>', pay: '<strong style="color:#e65100;">' + t('restaurant.wordPay') + '</strong>' }) + '</p></div>';
  return floorHtml;
}
function martRenderOrderNumFloorHtml() {
  return renderDeptOrderNumFloorHtml({
    getState: martGetOrderNumFloorState,
    getTotal: martGetActiveOrderNumOrdersTotal,
    clickFn: 'martOrderNumFloorClick',
    focusAll: martFocusAllOrderNums,
    orderNum: martOrderNum
  });
}
function posRenderOrderNumFloorHtml() {
  return renderDeptOrderNumFloorHtml({
    getState: posGetOrderNumFloorState,
    getTotal: posGetActiveOrderNumOrdersTotal,
    clickFn: 'posOrderNumFloorClick',
    focusAll: posFocusAllOrderNums,
    orderNum: posOrderNum
  });
}
window.martOrderNumFloorClick = function(slotNum) {
  martCrmGuest = null;
  martSelectedBooking = null;
  martIsWalkin = true;
  martFocusAllOrderNums = false;
  martOrderNum = String(slotNum);
  renderMiniMart();
  if (martGetOrderNumFloorState(slotNum) !== 'available') {
    setTimeout(function() { martOpenOrderNumBillModal(slotNum); }, 30);
  }
};
window.posOrderNumFloorClick = function(slotNum) {
  posCrmGuestId = null;
  posSelectedBooking = null;
  posFocusAllOrderNums = false;
  posOrderNum = String(slotNum);
  renderPOS();
  if (posGetOrderNumFloorState(slotNum) !== 'available') {
    setTimeout(function() { posOpenOrderNumBillModal(slotNum); }, 30);
  }
};
window.martOpenOrderNumBillModal = function(slotNum) {
  var orders = martGetOrdersForOrderNum(slotNum);
  if (!orders.length) return;
  var escM = function(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  var body = '';
  orders.forEach(function(o) {
    var itemsStr = (o.items || []).map(function(i) { return escM(i.name) + ' ×' + i.qty; }).join(', ');
    var idS = String(o.id || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    body += '<div style="border:1px solid var(--border);border-radius:10px;padding:0.75rem;margin-bottom:0.6rem;background:var(--card-bg);">';
    body += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.35rem;"><strong>' + escM(o.orderNumber) + '</strong>';
    body += '<span class="status status-new">' + escM(t('minimart.statusOpen')) + '</span></div>';
    body += '<div style="font-size:0.82rem;margin:0.35rem 0;">' + itemsStr + '</div>';
    body += '<div style="font-weight:700;">' + fmt$(o.grandTotal) + '</div>';
    body += '<div style="display:flex;flex-wrap:wrap;gap:0.35rem;margin-top:0.45rem;">';
    body += '<button type="button" class="btn btn-sm btn-outline" onclick="closeModal();if(window.martOpenBillSeeInvoice)martOpenBillSeeInvoice(\'' + idS + '\')">' + t('common.seeInvoice') + '</button>';
    body += '<button type="button" class="btn btn-sm btn-warning" onclick="closeModal();if(window.martVoidOpenBill)martVoidOpenBill(\'' + idS + '\')">' + t('minimart.voidOpenBill') + '</button>';
    body += '</div></div>';
  });
  var label = t('restaurant.orderNumWord') + ' ' + slotNum;
  openModal('<div class="modal-header"><h2>' + label + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div><div class="modal-body">' + body + '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.close') + '</button></div>');
};
window.posOpenOrderNumBillModal = function(slotNum) {
  var orders = posGetOrdersForOrderNum(slotNum);
  if (!orders.length) return;
  var escM = function(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  var body = '';
  orders.forEach(function(o) {
    var itemsStr = (o.items || []).map(function(i) { return escM(i.name) + ' ×' + i.qty; }).join(', ');
    var idS = String(o.id || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    body += '<div style="border:1px solid var(--border);border-radius:10px;padding:0.75rem;margin-bottom:0.6rem;background:var(--card-bg);">';
    body += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.35rem;"><strong>' + escM(o.orderNumber) + '</strong>';
    body += '<span class="status status-new">' + escM(t('minimart.statusOpen')) + '</span></div>';
    body += '<div style="font-size:0.82rem;margin:0.35rem 0;">' + itemsStr + '</div>';
    body += '<div style="font-weight:700;">' + fmt$(o.grandTotal) + '</div>';
    body += '<div style="display:flex;flex-wrap:wrap;gap:0.35rem;margin-top:0.45rem;">';
    body += '<button type="button" class="btn btn-sm btn-outline" onclick="closeModal();if(window.posOpenBillSeeInvoice)posOpenBillSeeInvoice(\'' + idS + '\')">' + t('common.seeInvoice') + '</button>';
    body += '<button type="button" class="btn btn-sm btn-warning" onclick="closeModal();if(window.posVoidOpenBill)posVoidOpenBill(\'' + idS + '\')">' + t('minimart.voidOpenBill') + '</button>';
    body += '</div></div>';
  });
  var label = t('restaurant.orderNumWord') + ' ' + slotNum;
  openModal('<div class="modal-header"><h2>' + label + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div><div class="modal-body">' + body + '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.close') + '</button></div>');
};
window.martSetOrderType = function(type) {
  martOrderType = type;
  if (type === 'Room Service') { martFocusAllOrderNums = true; martOrderNum = ''; }
  if (type === 'QR Orders') { martFocusAllOrderNums = true; martOrderNum = ''; martCrmGuest = null; martSelectedBooking = null; martIsWalkin = true; }
  renderMiniMart();
};
window.posSetOrderType = function(type) {
  posOrderType = type;
  if (type === 'Room Service') { posFocusAllOrderNums = true; posOrderNum = ''; }
  if (type === 'QR Orders') { posFocusAllOrderNums = true; posOrderNum = ''; posCrmGuestId = null; posSelectedBooking = null; }
  renderPOS();
};
"""

MART_GET_OPEN_OLD = """function martGetOpenInScope() {
  try { martOpenOrders = load('martOpenOrders', martOpenOrders); } catch (e) {}
  var open = (martOpenOrders || []).filter(function(o) { return o && rowDataVisible(o) && (o.status === 'Open' || !o.status); });
  if (martSelectedBooking && !martIsWalkin) {"""

MART_GET_OPEN_NEW = """function martGetOpenInScope() {
  try { martOpenOrders = load('martOpenOrders', martOpenOrders); } catch (e) {}
  var open = (martOpenOrders || []).filter(function(o) { return o && rowDataVisible(o) && (o.status === 'Open' || !o.status); });
  if (martOrderType === 'QR Orders' && !martFocusAllOrderNums && martOrderNum) {
    var slotN = parseInt(String(martOrderNum).trim(), 10);
    if (!isNaN(slotN)) return martGetOrdersForOrderNum(slotN);
  }
  if (martSelectedBooking && !martIsWalkin) {"""

POS_GET_OPEN_OLD = """function posGetOpenInScope() {
  try { posOpenOrders = load('posOpenOrders', posOpenOrders); } catch (e) {}
  var open = (posOpenOrders || []).filter(function(o) { return o && rowDataVisible(o) && (o.status === 'Open' || !o.status); });
  if (posSelectedBooking) {"""

POS_GET_OPEN_NEW = """function posGetOpenInScope() {
  try { posOpenOrders = load('posOpenOrders', posOpenOrders); } catch (e) {}
  var open = (posOpenOrders || []).filter(function(o) { return o && rowDataVisible(o) && (o.status === 'Open' || !o.status); });
  if (posOrderType === 'QR Orders' && !posFocusAllOrderNums && posOrderNum) {
    var slotN2 = parseInt(String(posOrderNum).trim(), 10);
    if (!isNaN(slotN2)) return posGetOrdersForOrderNum(slotN2);
  }
  if (posSelectedBooking) {"""

MART_NEW_ORDER_CARD_OLD = """  const newOrderCard = '<div class="card"><div class="card-header" style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0.5rem;"><h2 style="margin:0;">' + t('minimart.newOrder') + '</h2><button type="button" class="btn btn-sm btn-primary guest-qr-report-btn" onclick="openGuestQrOrdersReport(\\'minimart\\')">&#128202; QR Orders Report</button></div><div class="card-body">' + selHtml + '</div></div>';"""

MART_NEW_ORDER_CARD_NEW = """  const martOrderTypeHtml = '<div class="rest-order-type">' +
    '<button class="btn ' + (martOrderType === 'Room Service' ? 'btn-primary' : 'btn-outline') + '" onclick="martSetOrderType(\\'Room Service\\')">' + t('restaurant.orderTypeRoom') + '</button>' +
    '<button class="btn ' + (martOrderType === 'QR Orders' ? 'btn-primary' : 'btn-outline') + '" onclick="martSetOrderType(\\'QR Orders\\')">' + t('restaurant.orderTypeQrOrders') + '</button></div>';
  const martSelPanel = martOrderType === 'QR Orders'
    ? (typeof martRenderOrderNumFloorHtml === 'function' ? martRenderOrderNumFloorHtml() : '')
    : selHtml;
  const newOrderCard = '<div class="card"><div class="card-header" style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0.5rem;"><h2 style="margin:0;">' + t('minimart.newOrder') + '</h2><button type="button" class="btn btn-sm btn-primary guest-qr-report-btn" onclick="openGuestQrOrdersReport(\\'minimart\\')">&#128202; QR Orders Report</button></div><div class="card-body">' + martOrderTypeHtml + martSelPanel + '</div></div>';"""

MART_PUT_BILL_START_OLD = """window.martPutBillOnCustomer = function() {
  if (martCart.length === 0) { toast(t('minimart.toastCartEmpty')); return; }
  try { martOpenOrders = load('martOpenOrders', martOpenOrders); } catch (e) {}
  var tr0 = parseFloat(settings.surcharge) || 7;"""

MART_PUT_BILL_START_NEW = """window.martPutBillOnCustomer = function() {
  if (martCart.length === 0) { toast(t('minimart.toastCartEmpty')); return; }
  try { martOpenOrders = load('martOpenOrders', martOpenOrders); } catch (e) {}
  var tr0 = parseFloat(settings.surcharge) || 7;
  if (martOrderType === 'QR Orders') {
    var onMm = String(martOrderNum || '1').trim();
    var linesQr = martCart.map(function(ci) { return { storeItemId: ci.storeItemId, name: ci.name, unitPrice: ci.unitPrice, qty: ci.qty }; });
    var saleQr = linesQr.map(function(ci) { return { itemId: ci.storeItemId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice }; });
    var totalsQr = computeLineTotalsFromRawLineItems(saleQr, tr0);
    var mergeMm = typeof guestMartFindOrderNumMergeTarget === 'function' ? guestMartFindOrderNumMergeTarget(onMm) : null;
    if (mergeMm) {
      guestMartMergeCartIntoOrder(mergeMm, linesQr, tr0);
      mergeMm.guestOrderNum = onMm;
      mergeMm.source = mergeMm.source || 'staffQr';
    } else {
      martOpenOrders.push({
        id: genId(), orderNumber: martNextMiniMartOrderNumber(), timestamp: new Date().toISOString(),
        roomNumber: onMm, guestName: 'Order #' + onMm, bookingId: '', guestOrderNum: onMm,
        source: 'staffQr', items: linesQr, subtotal: totalsQr.subtotal, tax: totalsQr.taxAmount,
        grandTotal: totalsQr.grandTotal, status: 'Open', paidBy: 'Pending'
      });
    }
    save('martOpenOrders', martOpenOrders);
    martCart = [];
    toast(t('minimart.toastBillOnCustomer', { n: 'Order #' + onMm }));
    renderMiniMart();
    return;
  }"""

MART_CHECKOUT_CTX_OLD = """  let roomNumber = '', guestName = '', bookingId = '';
  if (martCrmGuest) {
    guestName = guestDisplayNameFromProfile(martCrmGuest);
  } else if (martSelectedBooking && !martIsWalkin) {"""

MART_CHECKOUT_CTX_NEW = """  let roomNumber = '', guestName = '', bookingId = '';
  if (martOrderType === 'QR Orders') {
    var onPay = String(martOrderNum || '1').trim();
    roomNumber = onPay;
    guestName = 'Order #' + onPay;
  } else if (martCrmGuest) {
    guestName = guestDisplayNameFromProfile(martCrmGuest);
  } else if (martSelectedBooking && !martIsWalkin) {"""

MART_FILTER_LABEL_OLD = """  const martFilterLabel = (martSelectedBooking && !martIsWalkin) ? (function() { const bk = bookings.find(function(b) { return b.id === martSelectedBooking; }); return bk ? t('minimart.roomGuestFmt', { room: String(bk.roomNumber), name: String(bk.guestName) }) : t('minimart.selectedGuest'); })() : (martIsWalkin && martCrmGuest ? String(guestDisplayNameFromProfile(martCrmGuest) || '') : t('minimart.allCustomers'));"""

MART_FILTER_LABEL_NEW = """  const martFilterLabel = (martOrderType === 'QR Orders')
    ? (martFocusAllOrderNums ? t('restaurant.allOrderNums') : (t('restaurant.orderNumWord') + ' ' + String(martOrderNum || '')))
    : ((martSelectedBooking && !martIsWalkin) ? (function() { const bk = bookings.find(function(b) { return b.id === martSelectedBooking; }); return bk ? t('minimart.roomGuestFmt', { room: String(bk.roomNumber), name: String(bk.guestName) }) : t('minimart.selectedGuest'); })() : (martIsWalkin && martCrmGuest ? String(guestDisplayNameFromProfile(martCrmGuest) || '') : t('minimart.allCustomers')));"""

MART_SCOPE_HINT_OLD = """  let martScopeHint = t('minimart.allCustomersScope');
  if (martSelectedBooking && !martIsWalkin) {"""

MART_SCOPE_HINT_NEW = """  let martScopeHint = t('minimart.allCustomersScope');
  if (martOrderType === 'QR Orders') {
    martScopeHint = martFocusAllOrderNums ? t('restaurant.allOrderNums') : (t('restaurant.orderNumWord') + ' ' + String(martOrderNum || ''));
  } else if (martSelectedBooking && !martIsWalkin) {"""

MART_SHOW_ALL_OLD = "martCrmGuest=null;martIsWalkin=true;martSelectedBooking=null;renderMiniMart()"
MART_SHOW_ALL_NEW = "martCrmGuest=null;martIsWalkin=true;martSelectedBooking=null;martFocusAllOrderNums=true;martOrderNum=\\'\\';renderMiniMart()"

MART_CAN_CHARGE_OLD = "const canChargeRoom = (martIsWalkin && martCrmGuest) || (!martIsWalkin && martSelectedBooking);"
MART_CAN_CHARGE_NEW = "const canChargeRoom = martOrderType === 'QR Orders' ? !!martOrderNum : ((martIsWalkin && martCrmGuest) || (!martIsWalkin && martSelectedBooking));"

MART_EMPTY_ACT_OLD = "const emptyActMsg = hasMmContact ? t('minimart.emptyActiveForContact') : t('minimart.emptyActiveSelectContact');"
MART_EMPTY_ACT_NEW = """const emptyActMsg = (martOrderType === 'QR Orders' && !martFocusAllOrderNums)
    ? t('restaurant.emptyActiveForOrderNum', { n: String(martOrderNum || '') })
    : (martOrderType === 'QR Orders' ? t('restaurant.emptyActiveAnyOrderNum') : (hasMmContact ? t('minimart.emptyActiveForContact') : t('minimart.emptyActiveSelectContact')));"""

POS_TOP_OLD = """  let html = '<div class="pos-top"><div class="form-group" style="margin-bottom:0;"><label style="font-weight:700;font-size:0.85rem;">Active Room / Guest</label><select class="form-control" id="posRoomSelect" onchange="posSelectBooking(this.value)">' + selHtml + '</select></div>' + guestInfoHtml + '</div>';"""

POS_TOP_NEW = """  const posOrderTypeHtml = '<div class="rest-order-type" style="margin-bottom:0.65rem;">' +
    '<button class="btn ' + (posOrderType === 'Room Service' ? 'btn-primary' : 'btn-outline') + '" onclick="posSetOrderType(\\'Room Service\\')">' + t('restaurant.orderTypeRoom') + '</button>' +
    '<button class="btn ' + (posOrderType === 'QR Orders' ? 'btn-primary' : 'btn-outline') + '" onclick="posSetOrderType(\\'QR Orders\\')">' + t('restaurant.orderTypeQrOrders') + '</button></div>';
  const posGuestPanel = posOrderType === 'QR Orders'
    ? (typeof posRenderOrderNumFloorHtml === 'function' ? posRenderOrderNumFloorHtml() : '')
    : ('<div class="form-group" style="margin-bottom:0;"><label style="font-weight:700;font-size:0.85rem;">Active Room / Guest</label><select class="form-control" id="posRoomSelect" onchange="posSelectBooking(this.value)">' + selHtml + '</select></div>' + guestInfoHtml);
  let html = '<div class="pos-top">' + posOrderTypeHtml + posGuestPanel + '</div>';"""

POS_PUT_BILL_START_OLD = """window.posPutBillOnRoom = function() {
  if (posCart.length === 0) { toast(t('msg.cartEmpty')); return; }
  if (!posSelectedBooking && !posCrmGuestId) { toast(t('msg.selectRoomFirst')); return; }
  try { posOpenOrders = load('posOpenOrders', posOpenOrders); } catch (e) {}"""

POS_PUT_BILL_START_NEW = """window.posPutBillOnRoom = function() {
  if (posCart.length === 0) { toast(t('msg.cartEmpty')); return; }
  if (posOrderType === 'QR Orders') {
    if (!posOrderNum) { toast(t('restaurant.emptyActiveForOrderNum', { n: '?' })); return; }
    try { posOpenOrders = load('posOpenOrders', posOpenOrders); } catch (e) {}
    var trP = parseFloat(settings.surcharge) || 7;
    var onP = String(posOrderNum || '1').trim();
    var linesP = posCart.map(function(ci) { return { inventoryId: ci.inventoryId, name: ci.name, unitPrice: ci.unitPrice, qty: ci.qty, category: ci.category }; });
    var saleP = linesP.map(function(ci) { return { itemId: ci.inventoryId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice }; });
    var totalsP = computeLineTotalsFromRawLineItems(saleP, trP);
    var mergeP = typeof guestPosFindOrderNumMergeTarget === 'function' ? guestPosFindOrderNumMergeTarget(onP) : null;
    if (mergeP) {
      guestPosMergeCartIntoOrder(mergeP, linesP, trP);
      mergeP.guestOrderNum = onP;
      mergeP.source = mergeP.source || 'staffQr';
    } else {
      posOpenOrders.push({
        id: genId(), orderNumber: posNextPosOpenOrderNumber(), timestamp: new Date().toISOString(),
        roomNumber: onP, guestName: 'Order #' + onP, bookingId: '', guestOrderNum: onP,
        source: 'staffQr', items: linesP, subtotal: totalsP.subtotal, tax: totalsP.taxAmount,
        grandTotal: totalsP.grandTotal, status: 'Open', paidBy: 'Pending'
      });
    }
    save('posOpenOrders', posOpenOrders);
    posCart = [];
    toast(t('minimart.toastBillOnCustomer', { n: 'Order #' + onP }));
    renderPOS();
    return;
  }
  if (!posSelectedBooking && !posCrmGuestId) { toast(t('msg.selectRoomFirst')); return; }
  try { posOpenOrders = load('posOpenOrders', posOpenOrders); } catch (e) {}"""

POS_CHECKOUT_CTX_OLD = """  let roomNumber = '', guestName = '', bookingId = '';
  if (posCrmGuestId) {"""

POS_CHECKOUT_CTX_NEW = """  let roomNumber = '', guestName = '', bookingId = '';
  if (posOrderType === 'QR Orders') {
    var onPos = String(posOrderNum || '1').trim();
    roomNumber = onPos;
    guestName = 'Order #' + onPos;
  } else if (posCrmGuestId) {"""

POS_NAME_PART_OLD = """  const posNamePart = posSelectedBooking ? (function() { const bk = bookings.find(function(b) { return b.id === posSelectedBooking; }); return bk ? t('minimart.roomGuestFmt', { room: String(bk.roomNumber), name: String(bk.guestName) }) : t('minimart.selectedGuest'); })() : (posCrmGuestId ? (function() { const gc = (guests || []).find(function(x) { return x.id === posCrmGuestId; }); return gc ? String(guestDisplayNameFromProfile(gc) || '') : t('minimart.allCustomers'); })() : t('minimart.allCustomers'));"""

POS_NAME_PART_NEW = """  const posNamePart = (posOrderType === 'QR Orders')
    ? (posFocusAllOrderNums ? t('restaurant.allOrderNums') : (t('restaurant.orderNumWord') + ' ' + String(posOrderNum || '')))
    : (posSelectedBooking ? (function() { const bk = bookings.find(function(b) { return b.id === posSelectedBooking; }); return bk ? t('minimart.roomGuestFmt', { room: String(bk.roomNumber), name: String(bk.guestName) }) : t('minimart.selectedGuest'); })() : (posCrmGuestId ? (function() { const gc = (guests || []).find(function(x) { return x.id === posCrmGuestId; }); return gc ? String(guestDisplayNameFromProfile(gc) || '') : t('minimart.allCustomers'); })() : t('minimart.allCustomers')));"""

POS_SCOPE_HINT_OLD = """  var posScopeHint = t('minimart.allCustomersScope');
  if (posSelectedBooking) {"""

POS_SCOPE_HINT_NEW = """  var posScopeHint = t('minimart.allCustomersScope');
  if (posOrderType === 'QR Orders') {
    posScopeHint = posFocusAllOrderNums ? t('restaurant.allOrderNums') : (t('restaurant.orderNumWord') + ' ' + String(posOrderNum || ''));
  } else if (posSelectedBooking) {"""

POS_SHOW_ALL_OLD = "posSelectedBooking=null;posCrmGuestId=null;renderPOS()"
POS_SHOW_ALL_NEW = "posSelectedBooking=null;posCrmGuestId=null;posFocusAllOrderNums=true;posOrderNum=\\'\\';renderPOS()"

POS_CAN_CHARGE_OLD = "const canChargeRoom = !!(posCrmGuestId || posSelectedBooking);"
POS_CAN_CHARGE_NEW = "const canChargeRoom = posOrderType === 'QR Orders' ? !!posOrderNum : !!(posCrmGuestId || posSelectedBooking);"

POS_HAS_CONTACT_OLD = "const hasPosContact = !!(posSelectedBooking || posCrmGuestId);"
POS_HAS_CONTACT_NEW = "const hasPosContact = posOrderType === 'QR Orders' ? !posFocusAllOrderNums : !!(posSelectedBooking || posCrmGuestId);"

POS_EMPTY_ACT_OLD = "const emptyPosActMsg = hasPosContact ? t('minimart.emptyActiveForContact') : t('minimart.emptyActiveSelectContact');"
POS_EMPTY_ACT_NEW = """const emptyPosActMsg = (posOrderType === 'QR Orders' && !posFocusAllOrderNums)
    ? t('restaurant.emptyActiveForOrderNum', { n: String(posOrderNum || '') })
    : (posOrderType === 'QR Orders' ? t('restaurant.emptyActiveAnyOrderNum') : (hasPosContact ? t('minimart.emptyActiveForContact') : t('minimart.emptyActiveSelectContact')));"""

GUEST_MART_SUBMIT_OLD = """  var orderNum = typeof martNextMiniMartOrderNumber === 'function' ? martNextMiniMartOrderNumber() : ('MM-' + Date.now());
  var order = {
    id: genId(), orderNumber: orderNum, timestamp: new Date().toISOString(),
    roomNumber: guestMartCtx.orderNum ? String(guestMartCtx.orderNum) : (guestMartCtx.room || '—'),
    guestName: guestMartCtx.orderNum ? ('Order #' + guestMartCtx.orderNum) : (guestMartCtx.guest || 'Walk-in'),
    bookingId: guestMartCtx.booking || '',
    guestOrderNum: guestMartCtx.orderNum || '',
    source: 'guestQr', items: lines, subtotal: totals.subtotal, tax: totals.taxAmount, grandTotal: totals.grandTotal,
    status: 'Open', paidBy: 'Pending', staffName: 'Guest (QR scan)', guestQrOrder: true
  };
  var propertyNsMart = guestQrCloudResolvePropertyNs(guestMartCtx);
  var finishMart = function() {
    guestMartCart = []; guestMartSubmitted = true; renderGuestMiniMartOrder();
  };
  var saveMartLocal = function() {
    martOpenOrders.push(order);"""

GUEST_MART_SUBMIT_NEW = """  var slotNum = String(guestMartCtx.orderNum || '').trim();
  var mergeMart = slotNum && typeof guestMartFindOrderNumMergeTarget === 'function' ? guestMartFindOrderNumMergeTarget(slotNum) : null;
  var orderNum = typeof martNextMiniMartOrderNumber === 'function' ? martNextMiniMartOrderNumber() : ('MM-' + Date.now());
  var order = {
    id: genId(), orderNumber: orderNum, timestamp: new Date().toISOString(),
    roomNumber: slotNum ? String(slotNum) : (guestMartCtx.room || '—'),
    guestName: slotNum ? ('Order #' + slotNum) : (guestMartCtx.guest || 'Walk-in'),
    bookingId: guestMartCtx.booking || '',
    guestOrderNum: slotNum || '',
    source: 'guestQr', items: lines, subtotal: totals.subtotal, tax: totals.taxAmount, grandTotal: totals.grandTotal,
    status: 'Open', paidBy: 'Pending', staffName: 'Guest (QR scan)', guestQrOrder: true
  };
  var propertyNsMart = guestQrCloudResolvePropertyNs(guestMartCtx);
  var finishMart = function() {
    if (slotNum && typeof martNotifyOrderNumUpdate === 'function') martNotifyOrderNumUpdate(slotNum);
    guestMartCart = []; guestMartSubmitted = true; renderGuestMiniMartOrder();
  };
  var saveMartLocal = function() {
    if (mergeMart) {
      guestMartMergeCartIntoOrder(mergeMart, lines, tr);
      mergeMart.guestQrOrder = true;
      mergeMart.source = mergeMart.source || 'guestQr';
      mergeMart.guestOrderNum = slotNum || mergeMart.guestOrderNum || '';
    } else {
      martOpenOrders.push(order);
    }"""

GUEST_MART_CTX_SHOW_OLD = "guestMartCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '' };"
GUEST_MART_CTX_SHOW_NEW = "guestMartCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '', orderNum: ctx.orderNum || '', propertyNs: ctx.propertyNs || '' };"

CLOUD_INGEST_MART_OLD = """  martOpenOrders.push(order);
  try { save('martOpenOrders', martOpenOrders); } catch (e) {}
  return guestQrCloudMarkSynced(propertyNs, docSnap.id);
}"""

CLOUD_INGEST_MART_NEW = """  martOpenOrders.push(order);
  try { save('martOpenOrders', martOpenOrders); } catch (e) {}
  if (order.guestOrderNum && typeof martNotifyOrderNumUpdate === 'function') martNotifyOrderNumUpdate(order.guestOrderNum);
  return guestQrCloudMarkSynced(propertyNs, docSnap.id);
}"""

MART_CART_ROW_TABLE_OLD = "tableNumber: t('minimart.roomPrefix', { n: o.roomNumber }),"
MART_CART_ROW_TABLE_NEW = "tableNumber: (o.guestOrderNum ? (t('restaurant.orderNumWord') + ' ' + o.guestOrderNum) : t('minimart.roomPrefix', { n: o.roomNumber })),"

POS_CART_ROW_TABLE_OLD = "tableNumber: t('minimart.roomPrefix', { n: o.roomNumber }),"
POS_CART_ROW_TABLE_NEW_POS = "tableNumber: (o.guestOrderNum ? (t('restaurant.orderNumWord') + ' ' + o.guestOrderNum) : t('minimart.roomPrefix', { n: o.roomNumber })),"
