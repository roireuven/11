"""Restaurant POS — QR order numbers 1–60 floor (like table floor)."""

REST_ORDER_NUM_STATE = r"""/** QR order slot 1–60 — focus like table floor. */
let restOrderNum = '';
let restFocusAllOrderNums = true;
"""

REST_ORDER_NUM_HELPERS = r"""
function restGetOrdersForOrderNum(slotNum) {
  var n = parseInt(slotNum, 10);
  if (isNaN(n) || n < 1 || n > 60) return [];
  return restaurantOrders.filter(function(o) {
    if (!restOrderIsActive(o)) return false;
    if (typeof guestQrExtractOrderNum === 'function') {
      var ex = guestQrExtractOrderNum(o);
      if (ex === n) return true;
    }
    var m = /^Order #(\d+)$/i.exec(String(o.tableNumber || '').trim());
    return m && parseInt(m[1], 10) === n;
  });
}
function restGetActiveOrderNumOrdersTotal(slotNum) {
  var list = restGetOrdersForOrderNum(slotNum);
  return Math.round(list.reduce(function(s, o) { return s + (parseFloat(o && o.grandTotal) || 0); }, 0) * 100) / 100;
}
function restGetOrderNumFloorState(slotNum) {
  var active = restGetOrdersForOrderNum(slotNum);
  if (!active.length) return 'available';
  if (active.some(function(o) { return restOrderIsPayableLine(o); })) return 'pending';
  return 'occupied';
}
function guestRestFindOrderNumMergeTarget(orderNum) {
  var n = parseInt(String(orderNum || '').trim(), 10);
  if (isNaN(n)) return null;
  try { restaurantOrders = load('restaurantOrders', restaurantOrders); } catch (e) {}
  var list = typeof restGetOrdersForOrderNum === 'function' ? restGetOrdersForOrderNum(n) : [];
  if (!list.length) return null;
  list = list.slice().sort(function(a, b) {
    try { return new Date(b.timestamp) - new Date(a.timestamp); } catch (e) { return 0; }
  });
  for (var i = 0; i < list.length; i++) {
    var o = list[i];
    if (o && typeof restOrderIsActive === 'function' && restOrderIsActive(o) && o.status !== 'Served' && o.status !== 'Paid') return o;
  }
  return null;
}
function guestRestNotifyOrderNumOrderUpdate(orderNum) {
  try { window.dispatchEvent(new CustomEvent('hotel-sync-restaurantOrders')); } catch (e) {}
  try {
    var nav = document.querySelector('#sidebarNav a[data-page="restaurant"]');
    if (!nav || !nav.classList.contains('active') || typeof renderRestaurant !== 'function') return;
    if (typeof restOrderType !== 'undefined' && restOrderType === 'QR Orders') {
      if (typeof restFocusAllOrderNums !== 'undefined' && restFocusAllOrderNums) { renderRestaurant(); return; }
      var n = parseInt(String(orderNum || '').trim(), 10);
      if (!isNaN(n) && parseInt(String(restOrderNum || '').trim(), 10) === n) renderRestaurant();
    }
  } catch (e) {}
}
function restRenderOrderNumFloorHtml() {
  var esc = function(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); };
  var nAvail = 0, nOcc = 0, nPend = 0;
  for (var i = 1; i <= 60; i++) {
    var s0 = restGetOrderNumFloorState(i);
    if (s0 === 'available') nAvail++;
    else if (s0 === 'pending') nPend++;
    else nOcc++;
  }
  var floorHtml = '<div class="rest-floor-wrap">';
  floorHtml += '<div class="rest-floor-head">';
  floorHtml += '<div class="rest-floor-title-actions"><h3>' + t('restaurant.orderNumFloorTitle') + '</h3></div>';
  floorHtml += '<div class="rest-floor-summary" role="status" aria-live="polite">';
  floorHtml += '<span class="rfs rfs-free" title="' + String(t('restaurant.ttFree')).replace(/"/g, '&quot;') + '"><strong>' + nAvail + '</strong> ' + t('restaurant.wordFree') + '</span>';
  floorHtml += '<span class="rfs rfs-busy" title="' + String(t('restaurant.ttBusy')).replace(/"/g, '&quot;') + '"><strong>' + nOcc + '</strong> ' + t('restaurant.wordLive') + '</span>';
  floorHtml += '<span class="rfs rfs-due" title="' + String(t('restaurant.ttDue')).replace(/"/g, '&quot;') + '"><strong>' + nPend + '</strong> ' + t('restaurant.wordPay') + '</span>';
  floorHtml += '</div></div>';
  floorHtml += '<div class="rest-floor-legend">' +
    '<span><span class="rest-floor-dot avail" aria-hidden="true"></span>' + t('restaurant.legendFree') + '</span>' +
    '<span><span class="rest-floor-dot occ" aria-hidden="true"></span>' + t('restaurant.legendOpen') + '</span>' +
    '<span><span class="rest-floor-dot pend" aria-hidden="true"></span>' + t('restaurant.legendPay') + '</span>' +
    '</div>';
  floorHtml += '<div class="rest-order-num-floor" role="group" aria-label="' + String(t('restaurant.orderNumFloorGroup')).replace(/"/g, '&quot;') + '">';
  for (var n = 1; n <= 60; n++) {
    var st = restGetOrderNumFloorState(n);
    var tag, hint, title;
    if (st === 'available') {
      tag = t('restaurant.tagOpen');
      hint = t('restaurant.hintSeatGuests');
      title = t('restaurant.tileTitleOrderAvail', { n: String(n) });
    } else if (st === 'pending') {
      tag = t('restaurant.tagPay');
      hint = t('restaurant.hintBillDue');
      title = t('restaurant.tileTitleOrderPay', { n: String(n) });
    } else {
      tag = t('restaurant.tagLive');
      hint = t('restaurant.hintOrderOnTab');
      title = t('restaurant.tileTitleOrderLive', { n: String(n) });
    }
    var sel = (!restFocusAllOrderNums && parseInt(String(restOrderNum || '').trim(), 10) === n) ? ' selected' : '';
    var actOrderSum = restGetActiveOrderNumOrdersTotal(n);
    var actSumStr = fmt$(actOrderSum);
    var titleWithTotal = title + ' — ' + actSumStr;
    floorHtml += '<button type="button" class="rest-table-tile rest-order-num-tile ' + st + sel + '" onclick="restOrderNumFloorClick(' + n + ')" title="' + titleWithTotal.replace(/"/g, '&quot;') + '" aria-label="' + (title + ' — ' + t('minimart.totalActiveLabel') + ' ' + actSumStr).replace(/"/g, '&quot;') + '">' +
      '<span class="rtt-num">#' + n + '</span>' +
      '<span class="rtt-sumline"><span class="rtt-slab">' + t('minimart.totalActiveLabel') + '</span> <span class="rtt-total">' + actSumStr + '</span></span>' +
      '<span class="rtt-tag">' + tag + '</span>' +
      '<span class="rtt-sub">' + hint + '</span>' +
      '</button>';
  }
  floorHtml += '</div>';
  floorHtml += '<p style="font-size:0.76rem;color:var(--text-light);margin:0.45rem 0 0;line-height:1.45;">' + t('restaurant.orderNumFloorHelp', { free: '<strong style="color:#2e7d32;">' + t('restaurant.wordFree') + '</strong>', live: '<strong style="color:#c62828;">' + t('restaurant.wordLive') + '</strong>', pay: '<strong style="color:#e65100;">' + t('restaurant.wordPay') + '</strong>' }) + '</p></div>';
  return floorHtml;
}
window.restOrderNumFloorClick = function(slotNum) {
  restSelectedBooking = null;
  restCrmGuestId = null;
  restFocusAllOrderNums = false;
  restOrderNum = String(slotNum);
  var st = restGetOrderNumFloorState(slotNum);
  renderRestaurant();
  if (st !== 'available') {
    setTimeout(function() { restOpenOrderNumBillModal(slotNum); }, 30);
  }
};
window.restOpenOrderNumBillModal = function(slotNum) {
  var orders = restGetOrdersForOrderNum(slotNum);
  if (!orders.length) return;
  var floorSt = restGetOrderNumFloorState(slotNum);
  var label = t('restaurant.orderNumWord') + ' ' + slotNum;
  var body = '';
  orders.forEach(function(o) {
    var itemsStr = (o.items || []).map(function(i) { return i.name + ' ×' + i.qty; }).join(', ');
    var stCls = restStatusClassForTile(o.status);
    body += '<div style="border:1px solid var(--border);border-radius:10px;padding:0.75rem;margin-bottom:0.6rem;background:var(--card-bg);">';
    body += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.35rem;"><strong>' + o.orderNumber + '</strong>';
    body += '<span class="status status-' + stCls + '">' + restI18nOrderStatus(o.status) + '</span></div>';
    body += '<div style="font-size:0.82rem;margin:0.35rem 0;color:var(--text);">' + itemsStr + '</div>';
    body += '<div style="font-weight:700;margin:0.25rem 0;">' + fmt$(o.grandTotal) + '</div>';
    if (o.notes) body += '<div style="font-size:0.78rem;color:var(--text-light);margin-bottom:0.35rem;">' + o.notes + '</div>';
    body += '<div style="display:flex;flex-wrap:wrap;gap:0.35rem;margin-top:0.45rem;">';
    if (o.status === 'New') body += '<button class="btn btn-sm btn-warning" onclick="closeModal();restUpdateStatus(\'' + o.id + '\',\'Preparing\')">' + t('restaurant.actPrep') + '</button>';
    if (o.status === 'Preparing') body += '<button class="btn btn-sm btn-success" onclick="closeModal();restUpdateStatus(\'' + o.id + '\',\'Ready\')">' + t('restaurant.actReady') + '</button>';
    if (o.status === 'Ready') body += '<button class="btn btn-sm btn-outline" onclick="closeModal();restUpdateStatus(\'' + o.id + '\',\'Served\')">' + t('restaurant.actServed') + '</button>';
    if (floorSt !== 'occupied' && restOrderIsPayableLine(o)) {
      body += '<button class="btn btn-sm btn-success" onclick="closeModal();restPayOrder(\'' + o.id + '\',\'Cash\')">' + t('minimart.cash') + '</button>';
      body += '<button class="btn btn-sm btn-outline" onclick="closeModal();restPayOrder(\'' + o.id + '\',\'Credit Card\')">' + t('restaurant.creditCard') + '</button>';
    }
    body += '</div></div>';
  });
  openModal('<div class="modal-header"><h2>' + label + '</h2><button class="modal-close" onclick="closeModal()">×</button></div><div class="modal-body">' + body + '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.close') + '</button></div>');
};
"""

REST_ORDER_NUM_CSS = r"""
    /* HRMM rest QR order numbers floor */
    .rest-order-num-floor { display: grid; grid-template-columns: repeat(10, 1fr); gap: 0.45rem; margin-bottom: 0.5rem; padding: 0.5rem; border-radius: 14px; background: linear-gradient(180deg, rgba(26,115,232,0.04) 0%, rgba(0,0,0,0.02) 100%); border: 1px solid rgba(26,115,232,0.12); }
    body.dark-mode .rest-order-num-floor { background: rgba(0,0,0,0.2); border-color: rgba(255,255,255,0.08); }
    .rest-order-num-tile .rtt-num { font-size: 0.95rem; }
    .rest-order-num-tile .rtt-sub { display: none; }
    @media (max-width: 900px) { .rest-order-num-floor { grid-template-columns: repeat(6, 1fr); } }
    @media (max-width: 600px) { .rest-order-num-floor { grid-template-columns: repeat(5, 1fr); } }
"""

ORDER_TYPE_HTML_OLD = (
    "  let orderTypeHtml = '<div class=\"rest-order-type\">' +\n"
    "    '<button class=\"btn ' + (restOrderType === 'Room Service' ? 'btn-primary' : 'btn-outline') + '\" onclick=\"restSetOrderType(\\'Room Service\\')\">' + t('restaurant.orderTypeRoom') + '</button>' +\n"
    "    '<button class=\"btn ' + (restOrderType === 'Table' ? 'btn-primary' : 'btn-outline') + '\" onclick=\"restSetOrderType(\\'Table\\')\">' + t('restaurant.orderTypeTable') + '</button></div>';"
)

ORDER_TYPE_HTML_NEW = (
    "  let orderTypeHtml = '<div class=\"rest-order-type\">' +\n"
    "    '<button class=\"btn ' + (restOrderType === 'Room Service' ? 'btn-primary' : 'btn-outline') + '\" onclick=\"restSetOrderType(\\'Room Service\\')\">' + t('restaurant.orderTypeRoom') + '</button>' +\n"
    "    '<button class=\"btn ' + (restOrderType === 'Table' ? 'btn-primary' : 'btn-outline') + '\" onclick=\"restSetOrderType(\\'Table\\')\">' + t('restaurant.orderTypeTable') + '</button>' +\n"
    "    '<button class=\"btn ' + (restOrderType === 'QR Orders' ? 'btn-primary' : 'btn-outline') + '\" onclick=\"restSetOrderType(\\'QR Orders\\')\">' + t('restaurant.orderTypeQrOrders') + '</button></div>';"
)

SEL_HTML_BRANCH_OLD = """      '</div>';
  } else {
    const tablesSorted = restSortedTables();"""

SEL_HTML_BRANCH_NEW = """      '</div>';
  } else if (restOrderType === 'QR Orders') {
    selHtml = typeof restRenderOrderNumFloorHtml === 'function' ? restRenderOrderNumFloorHtml() : '';
  } else {
    const tablesSorted = restSortedTables();"""

REST_APPLY_FILTER_OLD = """  } else if (restOrderType === 'Table' && !restFocusAllTables && restTableNumber) {
    const tn = String(restTableNumber).trim();
    list = list.filter(function(o) { return typeof restTableLabelsMatch === 'function' ? restTableLabelsMatch(o.tableNumber, tn) : String(o.tableNumber || '').trim() === tn; });
  }
  return list;"""

REST_APPLY_FILTER_NEW = """  } else if (restOrderType === 'Table' && !restFocusAllTables && restTableNumber) {
    const tn = String(restTableNumber).trim();
    list = list.filter(function(o) { return typeof restTableLabelsMatch === 'function' ? restTableLabelsMatch(o.tableNumber, tn) : String(o.tableNumber || '').trim() === tn; });
  } else if (restOrderType === 'QR Orders' && !restFocusAllOrderNums && restOrderNum) {
    const slotN = parseInt(String(restOrderNum).trim(), 10);
    if (!isNaN(slotN)) list = list.filter(function(o) { return typeof restGetOrdersForOrderNum === 'function' ? restGetOrdersForOrderNum(slotN).some(function(x) { return x && x.id === o.id; }) : false; });
  }
  return list;"""

REST_SET_ORDER_TYPE_OLD = """window.restSetOrderType = function(type) {
  restOrderType = type;
  restSelectedBooking = null;
  restCrmGuestId = null;
  if (type === 'Table') restFocusAllTables = true;
  renderRestaurant();
};"""

REST_SET_ORDER_TYPE_NEW = """window.restSetOrderType = function(type) {
  restOrderType = type;
  restSelectedBooking = null;
  restCrmGuestId = null;
  if (type === 'Table') { restFocusAllTables = true; restFocusAllOrderNums = true; restOrderNum = ''; }
  if (type === 'QR Orders') { restFocusAllOrderNums = true; restFocusAllTables = true; restOrderNum = ''; }
  if (type === 'Room Service') { restFocusAllTables = true; restFocusAllOrderNums = true; restOrderNum = ''; }
  renderRestaurant();
};"""

REST_SEND_KITCHEN_ELSE_OLD = """  } else {
    tableNumber = restTableNumber || 'Table 1';
  }

  const items = restCart.map(ci => ({menuItemId: ci.menuItemId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice, total: ci.unitPrice * ci.qty}));
  const subtotal = items.reduce((s, i) => s + i.total, 0);
  const tax = Math.round((subtotal * (taxRate / 100)) * 100) / 100;
  const grandTotal = Math.round((subtotal + tax) * 100) / 100;
  const notes = document.getElementById('restOrderNotes') ? document.getElementById('restOrderNotes').value : '';

  const order = {
    id: genId(), timestamp: new Date().toISOString(), orderNumber: nextOrderNumber(),
    roomNumber: roomNumber, guestName: guestName, bookingId: bookingId, tableNumber: tableNumber,
    items: items, subtotal: subtotal, tax: tax, grandTotal: grandTotal,
    status: 'Preparing', paidBy: 'Pending', staffName: staffName, notes: notes, workPeriodId: getActiveWorkPeriod('Restaurant').id,
    diningFlow: 'kitchen'
  };"""

REST_SEND_KITCHEN_ELSE_NEW = """  } else if (restOrderType === 'QR Orders') {
    const on = String(restOrderNum || '1').trim();
    tableNumber = 'Order #' + on;
    roomNumber = on;
    guestName = 'Order #' + on;
  } else {
    tableNumber = restTableNumber || 'Table 1';
  }

  const items = restCart.map(ci => ({menuItemId: ci.menuItemId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice, total: ci.unitPrice * ci.qty}));
  const subtotal = items.reduce((s, i) => s + i.total, 0);
  const tax = Math.round((subtotal * (taxRate / 100)) * 100) / 100;
  const grandTotal = Math.round((subtotal + tax) * 100) / 100;
  const notes = document.getElementById('restOrderNotes') ? document.getElementById('restOrderNotes').value : '';
  const guestOrderNumVal = restOrderType === 'QR Orders' ? String(restOrderNum || '1').trim() : '';

  const order = {
    id: genId(), timestamp: new Date().toISOString(), orderNumber: nextOrderNumber(),
    roomNumber: roomNumber, guestName: guestName, bookingId: bookingId, tableNumber: tableNumber,
    guestOrderNum: guestOrderNumVal,
    items: items, subtotal: subtotal, tax: tax, grandTotal: grandTotal,
    status: 'Preparing', paidBy: 'Pending', staffName: staffName, notes: notes, workPeriodId: getActiveWorkPeriod('Restaurant').id,
    diningFlow: 'kitchen'
  };"""

SHOW_ALL_OLD = "restSelectedBooking=null;restCrmGuestId=null;restFocusAllTables=true;renderRestaurant()"
SHOW_ALL_NEW = "restSelectedBooking=null;restCrmGuestId=null;restFocusAllTables=true;restFocusAllOrderNums=true;restOrderNum='';renderRestaurant()"

FILTER_LABEL_TABLE_OLD = """    if (restOrderType === 'Table') { return restFocusAllTables ? t('restaurant.allTables') : (restTableNumber || t('restaurant.tableWord')); }
    if (restOrderType === 'Room Service' && restSelectedBooking) {"""

FILTER_LABEL_TABLE_NEW = """    if (restOrderType === 'Table') { return restFocusAllTables ? t('restaurant.allTables') : (restTableNumber || t('restaurant.tableWord')); }
    if (restOrderType === 'QR Orders') { return restFocusAllOrderNums ? t('restaurant.allOrderNums') : (t('restaurant.orderNumWord') + ' ' + String(restOrderNum || '')); }
    if (restOrderType === 'Room Service' && restSelectedBooking) {"""

SCOPE_HINT_TABLE_OLD = """    if (restOrderType === 'Table') {
      return restFocusAllTables ? t('restaurant.allTables') : (restTableNumber || t('restaurant.tableWord'));
    }
    return t('restaurant.allRoomsUnfiltered');"""

SCOPE_HINT_TABLE_NEW = """    if (restOrderType === 'Table') {
      return restFocusAllTables ? t('restaurant.allTables') : (restTableNumber || t('restaurant.tableWord'));
    }
    if (restOrderType === 'QR Orders') {
      return restFocusAllOrderNums ? t('restaurant.allOrderNums') : (t('restaurant.orderNumWord') + ' ' + String(restOrderNum || ''));
    }
    return t('restaurant.allRoomsUnfiltered');"""

EMPTY_ACT_TABLE_OLD = """  else if (restOrderType === 'Table' && !restFocusAllTables) emptyActMsg = t('restaurant.emptyActiveForTable', { table: (restTableNumber || t('restaurant.tableWord')) });
  else if (restOrderType === 'Table') emptyActMsg = t('restaurant.emptyActiveAnyTable');"""

EMPTY_ACT_TABLE_NEW = """  else if (restOrderType === 'Table' && !restFocusAllTables) emptyActMsg = t('restaurant.emptyActiveForTable', { table: (restTableNumber || t('restaurant.tableWord')) });
  else if (restOrderType === 'Table') emptyActMsg = t('restaurant.emptyActiveAnyTable');
  else if (restOrderType === 'QR Orders' && !restFocusAllOrderNums) emptyActMsg = t('restaurant.emptyActiveForOrderNum', { n: String(restOrderNum || '') });
  else if (restOrderType === 'QR Orders') emptyActMsg = t('restaurant.emptyActiveAnyOrderNum');"""

GUEST_MERGE_TARGET_OLD = "  var mergeTarget = tableLabel ? guestRestFindTableMergeTarget(tableLabel) : null;"
GUEST_MERGE_TARGET_NEW = "  var mergeTarget = tableLabel ? guestRestFindTableMergeTarget(tableLabel) : (orderNum ? guestRestFindOrderNumMergeTarget(orderNum) : null);"

GUEST_MERGE_META_OLD = """    mergeTarget.guestQrTable = tableLabel;
    mergeTarget.staffName = mergeTarget.staffName || 'Guest (QR scan)';
    try { save('restaurantOrders', restaurantOrders); } catch (e) {}
    try { if (typeof logAudit === 'function') logAudit('Update', 'Restaurant', mergeTarget.orderNumber, 'Guest QR added items to table ' + tableLabel + ': ' + fmt$(mergeTarget.grandTotal)); } catch (e) {}"""

GUEST_MERGE_META_NEW = """    mergeTarget.guestQrTable = tableLabel;
    if (orderNum) mergeTarget.guestOrderNum = orderNum;
    mergeTarget.staffName = mergeTarget.staffName || 'Guest (QR scan)';
    try { save('restaurantOrders', restaurantOrders); } catch (e) {}
    try { if (typeof logAudit === 'function') logAudit('Update', 'Restaurant', mergeTarget.orderNumber, 'Guest QR added items' + (tableLabel ? (' to table ' + tableLabel) : (' to order #' + orderNum)) + ': ' + fmt$(mergeTarget.grandTotal)); } catch (e) {}"""

GUEST_NOTIFY_OLD = """  if (tableLabel) guestRestNotifyTableOrderUpdate(tableLabel);
  guestRestCart = [];"""

GUEST_NOTIFY_NEW = """  if (tableLabel) guestRestNotifyTableOrderUpdate(tableLabel);
  if (orderNum) guestRestNotifyOrderNumOrderUpdate(orderNum);
  guestRestCart = [];"""

REST_SEND_ROOM_ELSE_OLD = """  } else {
    tableNumber = restTableNumber || 'Table 1';
  }

  const items = restCart.map(ci => ({menuItemId: ci.menuItemId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice, total: ci.unitPrice * ci.qty}));
  const subtotal = items.reduce((s, i) => s + i.total, 0);
  const tax = Math.round((subtotal * (taxRate / 100)) * 100) / 100;
  const grandTotal = Math.round((subtotal + tax) * 100) / 100;
  const notes = document.getElementById('restOrderNotes') ? document.getElementById('restOrderNotes').value : '';

  const order = {
    id: genId(), timestamp: new Date().toISOString(), orderNumber: nextOrderNumber(),
    roomNumber: roomNumber, guestName: guestName, bookingId: bookingId, tableNumber: tableNumber,
    items: items, subtotal: subtotal, tax: tax, grandTotal: grandTotal,
    status: 'Ready', paidBy: 'Pending', staffName: staffName, notes: notes, workPeriodId: getActiveWorkPeriod('Restaurant').id,
    diningFlow: 'room'
  };"""

REST_SEND_ROOM_ELSE_NEW = """  } else if (restOrderType === 'QR Orders') {
    const on = String(restOrderNum || '1').trim();
    tableNumber = 'Order #' + on;
    roomNumber = on;
    guestName = 'Order #' + on;
  } else {
    tableNumber = restTableNumber || 'Table 1';
  }

  const items = restCart.map(ci => ({menuItemId: ci.menuItemId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice, total: ci.unitPrice * ci.qty}));
  const subtotal = items.reduce((s, i) => s + i.total, 0);
  const tax = Math.round((subtotal * (taxRate / 100)) * 100) / 100;
  const grandTotal = Math.round((subtotal + tax) * 100) / 100;
  const notes = document.getElementById('restOrderNotes') ? document.getElementById('restOrderNotes').value : '';
  const guestOrderNumVal2 = restOrderType === 'QR Orders' ? String(restOrderNum || '1').trim() : '';

  const order = {
    id: genId(), timestamp: new Date().toISOString(), orderNumber: nextOrderNumber(),
    roomNumber: roomNumber, guestName: guestName, bookingId: bookingId, tableNumber: tableNumber,
    guestOrderNum: guestOrderNumVal2,
    items: items, subtotal: subtotal, tax: tax, grandTotal: grandTotal,
    status: 'Ready', paidBy: 'Pending', staffName: staffName, notes: notes, workPeriodId: getActiveWorkPeriod('Restaurant').id,
    diningFlow: 'room'
  };"""

FOCUS_ALL_TABLES_OLD = "let restFocusAllTables = true;"
FOCUS_ALL_TABLES_NEW = FOCUS_ALL_TABLES_OLD + "\n" + REST_ORDER_NUM_STATE.strip()
