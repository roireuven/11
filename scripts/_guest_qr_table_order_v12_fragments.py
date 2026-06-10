"""Guest QR v12 — table QR orders merge into restaurant table active orders."""

GUEST_REST_TABLE_ORDER_HELPERS_V12 = r"""
function guestRestRecalcOrderTotals(order, taxRate) {
  var items = order.items || [];
  var subtotal = items.reduce(function(s, i) { return s + (parseFloat(i.total) || 0); }, 0);
  order.subtotal = Math.round(subtotal * 100) / 100;
  order.tax = Math.round((order.subtotal * (parseFloat(taxRate) || 0) / 100) * 100) / 100;
  order.grandTotal = Math.round((order.subtotal + order.tax) * 100) / 100;
}
function guestRestMergeCartIntoOrder(order, newItems, extraNotes, taxRate) {
  newItems.forEach(function(ni) {
    var ex = (order.items || []).find(function(i) {
      return String(i.menuItemId || '') === String(ni.menuItemId || '') && (parseFloat(i.unitPrice) || 0) === (parseFloat(ni.unitPrice) || 0);
    });
    if (ex) {
      ex.qty = (parseInt(ex.qty, 10) || 0) + (parseInt(ni.qty, 10) || 0);
      ex.total = (parseFloat(ex.unitPrice) || 0) * ex.qty;
    } else {
      if (!order.items) order.items = [];
      order.items.push({ menuItemId: ni.menuItemId, name: ni.name, qty: ni.qty, unitPrice: ni.unitPrice, total: ni.total });
    }
  });
  if (extraNotes) order.notes = order.notes ? (order.notes + '; ' + extraNotes) : extraNotes;
  guestRestRecalcOrderTotals(order, taxRate);
}
function guestRestFindTableMergeTarget(tableLabel) {
  if (!tableLabel) return null;
  try { restaurantOrders = load('restaurantOrders', restaurantOrders); } catch (e) {}
  var list = typeof restGetOrdersForPhysicalTable === 'function' ? restGetOrdersForPhysicalTable(tableLabel) : [];
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
function guestRestNotifyTableOrderUpdate(tableLabel) {
  try { window.dispatchEvent(new CustomEvent('hotel-sync-restaurantOrders')); } catch (e) {}
  try {
    var nav = document.querySelector('#sidebarNav a[data-page="restaurant"]');
    if (!nav || !nav.classList.contains('active') || typeof renderRestaurant !== 'function') return;
    if (typeof restOrderType !== 'undefined' && restOrderType === 'Table') {
      if (typeof restFocusAllTables !== 'undefined' && restFocusAllTables) { renderRestaurant(); return; }
      if (tableLabel && typeof restTableNumber !== 'undefined' && typeof restTableLabelsMatch === 'function' && restTableLabelsMatch(restTableNumber, tableLabel)) {
        renderRestaurant();
      }
    }
  } catch (e) {}
}
"""

GUEST_REST_SUBMIT_ORDER_V12 = r"""window.guestRestSubmitOrder = function() {
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
  var tableLabel = String(guestRestCtx.table || '').trim();
  var orderNum = String(guestRestCtx.orderNum || '').trim();
  var tableNumber;
  if (tableLabel) tableNumber = tableLabel;
  else if (orderNum) tableNumber = 'Order #' + orderNum;
  else if (guestRestCtx.room) tableNumber = 'Room ' + guestRestCtx.room;
  else tableNumber = 'QR Guest';
  var mergeTarget = tableLabel ? guestRestFindTableMergeTarget(tableLabel) : null;
  if (mergeTarget) {
    guestRestMergeCartIntoOrder(mergeTarget, items, notes, taxRate);
    mergeTarget.guestQrOrder = true;
    mergeTarget.source = mergeTarget.source || 'guestQr';
    mergeTarget.guestQrTable = tableLabel;
    mergeTarget.staffName = mergeTarget.staffName || 'Guest (QR scan)';
    try { save('restaurantOrders', restaurantOrders); } catch (e) {}
    try { if (typeof logAudit === 'function') logAudit('Update', 'Restaurant', mergeTarget.orderNumber, 'Guest QR added items to table ' + tableLabel + ': ' + fmt$(mergeTarget.grandTotal)); } catch (e) {}
  } else {
    var order = {
      id: genId(), timestamp: new Date().toISOString(), orderNumber: nextOrderNumber(),
      roomNumber: orderNum ? String(orderNum) : (guestRestCtx.room || ''),
      guestName: orderNum ? ('Order #' + orderNum) : (guestRestCtx.guest || (tableLabel ? 'Guest (Table QR)' : 'Guest')),
      bookingId: guestRestCtx.booking || '', guestOrderNum: orderNum || '',
      guestQrTable: tableLabel || '',
      tableNumber: tableNumber, items: items, subtotal: subtotal, tax: tax, grandTotal: grandTotal,
      status: 'Preparing', paidBy: 'Pending', staffName: 'Guest (QR scan)', notes: notes, workPeriodId: wp.id,
      diningFlow: 'kitchen', guestQrOrder: true, source: 'guestQr'
    };
    restaurantOrders.push(order);
    try { save('restaurantOrders', restaurantOrders); } catch (e) {}
    try { if (typeof logAudit === 'function') logAudit('New Order', 'Restaurant', order.orderNumber, 'Guest QR order: ' + fmt$(grandTotal) + ' (' + tableNumber + ')'); } catch (e) {}
  }
  if (tableLabel) guestRestNotifyTableOrderUpdate(tableLabel);
  guestRestCart = [];
  guestRestSubmitted = true;
  renderGuestRestaurantOrder();
};"""

REST_TABLE_LABEL_MATCH_V12 = r"""function restTableLabelsMatch(a, b) {
  return String(a != null ? a : '').trim().toLowerCase() === String(b != null ? b : '').trim().toLowerCase();
}
function restGetOrdersForPhysicalTable(tableLabel) {
  return restaurantOrders.filter(function(o) {
    return restOrderIsActive(o) && restTableLabelsMatch(o.tableNumber, tableLabel);
  });
}"""

REST_APPLY_FILTER_TABLE_MATCH_OLD = """  } else if (restOrderType === 'Table' && !restFocusAllTables && restTableNumber) {
    const tn = String(restTableNumber).trim();
    list = list.filter(function(o) { return String(o.tableNumber || '').trim() === tn; });
  }"""

REST_APPLY_FILTER_TABLE_MATCH_NEW = """  } else if (restOrderType === 'Table' && !restFocusAllTables && restTableNumber) {
    const tn = String(restTableNumber).trim();
    list = list.filter(function(o) { return typeof restTableLabelsMatch === 'function' ? restTableLabelsMatch(o.tableNumber, tn) : String(o.tableNumber || '').trim() === tn; });
  }"""

REST_GET_ORDERS_TABLE_OLD = """function restGetOrdersForPhysicalTable(tableLabel) {
  return restaurantOrders.filter(function(o) {
    return restOrderIsActive(o) && String(o.tableNumber || '').trim() === String(tableLabel).trim();
  });
}"""
