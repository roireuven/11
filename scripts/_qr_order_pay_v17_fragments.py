# QR order pay — shared helpers and pay footers on bill modals + report slots

MARKER = "HRMM-QR-ORDER-PAY-v1"

QR_PAY_HELPERS = """
function guestQrSlotIsPayable(hit) {
  if (!hit) return false;
  var st = String(hit.status || '').toLowerCase();
  if (st === 'paid' || st === 'void') return false;
  if (String(hit.paidBy || '').toLowerCase() === 'paid') return false;
  return true;
}
window.guestQrPrepareRestSlotScope = function(slotNum) {
  restOrderType = 'QR Orders';
  restFocusAllOrderNums = false;
  restOrderNum = String(slotNum);
  restSelectedBooking = null;
  restCrmGuestId = null;
};
window.guestQrPrepareMartSlotScope = function(slotNum) {
  martOrderType = 'QR Orders';
  martFocusAllOrderNums = false;
  martOrderNum = String(slotNum);
  martIsWalkin = true;
  martCrmGuest = null;
  martSelectedBooking = null;
};
window.guestQrPreparePosSlotScope = function(slotNum) {
  posOrderType = 'QR Orders';
  posFocusAllOrderNums = false;
  posOrderNum = String(slotNum);
  posCrmGuestId = null;
  posSelectedBooking = null;
};
window.guestQrOpenSlotPayModal = function(dept, slotNum) {
  var n = parseInt(String(slotNum || '').trim(), 10);
  if (isNaN(n) || n < 1 || n > 60) return;
  var delay = 40;
  if (typeof closeModal === 'function') closeModal();
  dept = dept === 'restaurant' ? 'restaurant' : (dept === 'pos' ? 'pos' : 'minimart');
  if (dept === 'restaurant') {
    guestQrPrepareRestSlotScope(n);
    setTimeout(function() { if (window.restOpenOrderNumBillModal) restOpenOrderNumBillModal(n); }, delay);
  } else if (dept === 'pos') {
    guestQrPreparePosSlotScope(n);
    setTimeout(function() { if (window.posOpenOrderNumBillModal) posOpenOrderNumBillModal(n); }, delay);
  } else {
    guestQrPrepareMartSlotScope(n);
    setTimeout(function() { if (window.martOpenOrderNumBillModal) martOpenOrderNumBillModal(n); }, delay);
  }
};
window.guestQrPayMartOpenBill = function(orderId, paidBy) {
  if (paidBy === 'Room Charge') return;
  try { martOpenOrders = load('martOpenOrders', martOpenOrders); } catch (e) {}
  var o = (martOpenOrders || []).find(function(x) { return x && x.id === orderId; });
  if (!o) { if (typeof toast === 'function') toast(t('minimart.toastNoOpenBills')); return; }
  var slot = guestQrExtractOrderNum(o);
  if (slot != null) guestQrPrepareMartSlotScope(slot);
  var tr = parseFloat(settings.surcharge) || 7;
  var saleItems = (o.items || []).map(function(ci) {
    return { itemId: ci.storeItemId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice };
  });
  var roomNumber = String(o.roomNumber || '');
  var guestName = String(o.guestName || '');
  var bookingId = String(o.bookingId || '');
  var removeIds = [orderId];
  if (paidBy === 'Cash') {
    var gtot = computeLineTotalsFromRawLineItems(saleItems, tr).grandTotal;
    openCashPaymentModal({
      grandTotal: gtot,
      title: t('minimart.mmCashTitle'),
      onSeePrepaidInvoice: function() { if (window.martOpenBillSeeInvoice) martOpenBillSeeInvoice(orderId); },
      onValid: function(tender, change) {
        toast(t('msg.changeDue', { amount: fmt$(change) }));
        martCheckoutRun('Cash', roomNumber, guestName, bookingId, saleItems, tr, removeIds);
      }
    });
    return;
  }
  martCheckoutRun(paidBy, roomNumber, guestName, bookingId, saleItems, tr, removeIds);
};
window.guestQrPayPosOpenBill = function(orderId, paidBy) {
  if (paidBy === 'Room Charge') return;
  try { posOpenOrders = load('posOpenOrders', posOpenOrders); } catch (e) {}
  var o = (posOpenOrders || []).find(function(x) { return x && x.id === orderId; });
  if (!o) { if (typeof toast === 'function') toast(t('minimart.toastNoOpenBills')); return; }
  var slot = guestQrExtractOrderNum(o);
  if (slot != null) guestQrPreparePosSlotScope(slot);
  var tr = parseFloat(settings.surcharge) || 7;
  var saleItems = (o.items || []).map(function(ci) {
    return { itemId: ci.storeItemId, name: ci.name, qty: ci.qty, unitPrice: ci.unitPrice };
  });
  var roomNumber = String(o.roomNumber || '');
  var guestName = String(o.guestName || '');
  var bookingId = String(o.bookingId || '');
  var removeIds = [orderId];
  if (paidBy === 'Cash') {
    var gtot = computeLineTotalsFromRawLineItems(saleItems, tr).grandTotal;
    openCashPaymentModal({
      grandTotal: gtot,
      title: t('minimart.mmCashTitle'),
      onSeePrepaidInvoice: function() { if (window.posOpenBillSeeInvoice) posOpenBillSeeInvoice(orderId); },
      onValid: function(tender, change) {
        toast(t('msg.changeDue', { amount: fmt$(change) }));
        posCheckoutRun('Cash', roomNumber, guestName, bookingId, saleItems, tr, removeIds);
      }
    });
    return;
  }
  posCheckoutRun(paidBy, roomNumber, guestName, bookingId, saleItems, tr, removeIds);
};
function guestQrBuildOpenBillPayBarHtml(total, payCashOnclick, payCardOnclick, seeInvoiceOnclick) {
  if (!(parseFloat(total) > 0)) return '';
  return '<div class="rest-bill-table-actions" style="position:sticky;bottom:0;z-index:1;border:1px solid var(--border);border-radius:10px;padding:0.75rem 0.85rem;margin:0.35rem 0 0.25rem;background:linear-gradient(180deg, rgba(26,115,232,0.07) 0%, var(--card-bg) 55%);box-shadow:0 -4px 12px rgba(0,0,0,0.05);">' +
    '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem 0.75rem;margin-bottom:0.5rem;">' +
    '<span style="font-size:0.85rem;color:var(--text-light);">' + t('minimart.totalActiveOrder') + '</span>' +
    '<strong style="font-size:1.05rem;">' + fmt$(total) + '</strong></div>' +
    '<div style="display:flex;flex-direction:column;gap:0.45rem;">' +
    '<button type="button" class="btn btn-sm btn-success" style="width:100%;" onclick="' + payCashOnclick + '">' + t('minimart.payTotalCash') + '</button>' +
    '<button type="button" class="btn btn-sm btn-outline" style="width:100%;" onclick="' + payCardOnclick + '">' + t('minimart.payTotalCard') + '</button>' +
    (seeInvoiceOnclick ? '<button type="button" class="btn btn-sm btn-outline" style="width:100%;" onclick="' + seeInvoiceOnclick + '">' + t('common.seeInvoice') + '</button>' : '') +
    '</div></div>';
}
"""

REST_BILL_MODAL_OLD = """window.restOpenOrderNumBillModal = function(slotNum) {
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
    if (o.status === 'New') body += '<button class="btn btn-sm btn-warning" onclick="closeModal();restUpdateStatus(\\'' + o.id + '\\',\\'Preparing\\')">' + t('restaurant.actPrep') + '</button>';
    if (o.status === 'Preparing') body += '<button class="btn btn-sm btn-success" onclick="closeModal();restUpdateStatus(\\'' + o.id + '\\',\\'Ready\\')">' + t('restaurant.actReady') + '</button>';
    if (o.status === 'Ready') body += '<button class="btn btn-sm btn-outline" onclick="closeModal();restUpdateStatus(\\'' + o.id + '\\',\\'Served\\')">' + t('restaurant.actServed') + '</button>';
    if (floorSt !== 'occupied' && restOrderIsPayableLine(o)) {
      body += '<button class="btn btn-sm btn-success" onclick="closeModal();restPayOrder(\\'' + o.id + '\\',\\'Cash\\')">' + t('minimart.cash') + '</button>';
      body += '<button class="btn btn-sm btn-outline" onclick="closeModal();restPayOrder(\\'' + o.id + '\\',\\'Credit Card\\')">' + t('restaurant.creditCard') + '</button>';
    }
    body += '</div></div>';
  });
  openModal('<div class="modal-header"><h2>' + label + '</h2><button class="modal-close" onclick="closeModal()">×</button></div><div class="modal-body">' + body + '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.close') + '</button></div>');
};"""

REST_BILL_MODAL_NEW = """window.restOpenOrderNumBillModal = function(slotNum) {
  if (typeof guestQrPrepareRestSlotScope === 'function') guestQrPrepareRestSlotScope(slotNum);
  var orders = restGetOrdersForOrderNum(slotNum);
  if (!orders.length) return;
  var floorSt = restGetOrderNumFloorState(slotNum);
  var label = t('restaurant.orderNumWord') + ' ' + slotNum;
  var body = '';
  var unpaid = orders.filter(function(o) { return o && !o.transactionId && o.status !== 'Void' && o.status !== 'Paid'; });
  var sumUnpaid = Math.round(unpaid.reduce(function(s, o) { return s + (parseFloat(o.grandTotal) || 0); }, 0) * 100) / 100;
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
    if (o.status === 'New') body += '<button class="btn btn-sm btn-warning" onclick="closeModal();restUpdateStatus(\\'' + o.id + '\\',\\'Preparing\\')">' + t('restaurant.actPrep') + '</button>';
    if (o.status === 'Preparing') body += '<button class="btn btn-sm btn-success" onclick="closeModal();restUpdateStatus(\\'' + o.id + '\\',\\'Ready\\')">' + t('restaurant.actReady') + '</button>';
    if (o.status === 'Ready') body += '<button class="btn btn-sm btn-outline" onclick="closeModal();restUpdateStatus(\\'' + o.id + '\\',\\'Served\\')">' + t('restaurant.actServed') + '</button>';
    if (restOrderIsPayableLine(o)) {
      body += '<button class="btn btn-sm btn-success" onclick="closeModal();restPayOrder(\\'' + o.id + '\\',\\'Cash\\')">' + t('minimart.cash') + '</button>';
      body += '<button class="btn btn-sm btn-outline" onclick="closeModal();restPayOrder(\\'' + o.id + '\\',\\'Credit Card\\')">' + t('restaurant.creditCard') + '</button>';
    } else if (!o.transactionId && o.status !== 'Void' && o.status !== 'Paid' && currentRole !== 'Kitchen') {
      body += '<button class="btn btn-sm btn-success" onclick="closeModal();restPayOrder(\\'' + o.id + '\\',\\'Cash\\')">' + t('minimart.cash') + '</button>';
      body += '<button class="btn btn-sm btn-outline" onclick="closeModal();restPayOrder(\\'' + o.id + '\\',\\'Credit Card\\')">' + t('restaurant.creditCard') + '</button>';
    }
    if (!o.transactionId && o.status !== 'Void' && o.status !== 'Paid' && parseFloat(o.grandTotal) > 0) {
      body += '<button type="button" class="btn btn-sm btn-outline" onclick="closeModal();if(window.seeRestaurantOrderPrepaidInvoice)seeRestaurantOrderPrepaidInvoice(\\'' + o.id + '\\')">' + t('common.seeInvoice') + '</button>';
    }
    body += '</div></div>';
  });
  if (sumUnpaid > 0 && currentRole !== 'Kitchen') {
    body += guestQrBuildOpenBillPayBarHtml(sumUnpaid,
      'closeModal();if(window.restPayActiveOrdersTotal)restPayActiveOrdersTotal(\\'Cash\\')',
      'closeModal();if(window.restPayActiveOrdersTotal)restPayActiveOrdersTotal(\\'Credit Card\\')',
      'closeModal();if(window.restActivePayableSeeInvoice)restActivePayableSeeInvoice()');
  }
  openModal('<div class="modal-header"><h2>' + label + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div><div class="modal-body" style="max-height:70vh;overflow-y:auto;">' + body + '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.close') + '</button></div>');
};"""

MART_BILL_MODAL_OLD = """window.martOpenOrderNumBillModal = function(slotNum) {
  var orders = martGetOrdersForOrderNum(slotNum);
  if (!orders.length) return;
  var escM = function(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  var body = '';
  orders.forEach(function(o) {
    var itemsStr = (o.items || []).map(function(i) { return escM(i.name) + ' ×' + i.qty; }).join(', ');
    var idS = String(o.id || '').replace(/\\\\/g, '\\\\\\\\').replace(/'/g, "\\\\'");
    body += '<div style="border:1px solid var(--border);border-radius:10px;padding:0.75rem;margin-bottom:0.6rem;background:var(--card-bg);">';
    body += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.35rem;"><strong>' + escM(o.orderNumber) + '</strong>';
    body += '<span class="status status-new">' + escM(t('minimart.statusOpen')) + '</span></div>';
    body += '<div style="font-size:0.82rem;margin:0.35rem 0;">' + itemsStr + '</div>';
    body += '<div style="font-weight:700;">' + fmt$(o.grandTotal) + '</div>';
    body += '<div style="display:flex;flex-wrap:wrap;gap:0.35rem;margin-top:0.45rem;">';
    body += '<button type="button" class="btn btn-sm btn-outline" onclick="closeModal();if(window.martOpenBillSeeInvoice)martOpenBillSeeInvoice(\\'' + idS + '\\')">' + t('common.seeInvoice') + '</button>';
    body += '<button type="button" class="btn btn-sm btn-warning" onclick="closeModal();if(window.martVoidOpenBill)martVoidOpenBill(\\'' + idS + '\\')">' + t('minimart.voidOpenBill') + '</button>';
    body += '</div></div>';
  });
  var label = t('restaurant.orderNumWord') + ' ' + slotNum;
  openModal('<div class="modal-header"><h2>' + label + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div><div class="modal-body">' + body + '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.close') + '</button></div>');
};"""

MART_BILL_MODAL_NEW = """window.martOpenOrderNumBillModal = function(slotNum) {
  if (typeof guestQrPrepareMartSlotScope === 'function') guestQrPrepareMartSlotScope(slotNum);
  var orders = martGetOrdersForOrderNum(slotNum);
  if (!orders.length) return;
  var escM = function(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  var body = '';
  var sumOpen = Math.round(orders.reduce(function(s, o) { return s + (parseFloat(o.grandTotal) || 0); }, 0) * 100) / 100;
  orders.forEach(function(o) {
    var itemsStr = (o.items || []).map(function(i) { return escM(i.name) + ' ×' + i.qty; }).join(', ');
    var idS = String(o.id || '').replace(/\\\\/g, '\\\\\\\\').replace(/'/g, "\\\\'");
    body += '<div style="border:1px solid var(--border);border-radius:10px;padding:0.75rem;margin-bottom:0.6rem;background:var(--card-bg);">';
    body += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.35rem;"><strong>' + escM(o.orderNumber) + '</strong>';
    body += '<span class="status status-new">' + escM(t('minimart.statusOpen')) + '</span></div>';
    body += '<div style="font-size:0.82rem;margin:0.35rem 0;">' + itemsStr + '</div>';
    body += '<div style="font-weight:700;">' + fmt$(o.grandTotal) + '</div>';
    body += '<div style="display:flex;flex-wrap:wrap;gap:0.35rem;margin-top:0.45rem;">';
    body += '<button type="button" class="btn btn-sm btn-success" onclick="closeModal();if(window.guestQrPayMartOpenBill)guestQrPayMartOpenBill(\\'' + idS + '\\',\\'Cash\\')">' + t('minimart.cash') + '</button>';
    body += '<button type="button" class="btn btn-sm btn-outline" onclick="closeModal();if(window.guestQrPayMartOpenBill)guestQrPayMartOpenBill(\\'' + idS + '\\',\\'Credit Card\\')">' + t('minimart.payTotalCard') + '</button>';
    body += '<button type="button" class="btn btn-sm btn-outline" onclick="closeModal();if(window.martOpenBillSeeInvoice)martOpenBillSeeInvoice(\\'' + idS + '\\')">' + t('common.seeInvoice') + '</button>';
    body += '<button type="button" class="btn btn-sm btn-warning" onclick="closeModal();if(window.martVoidOpenBill)martVoidOpenBill(\\'' + idS + '\\')">' + t('minimart.voidOpenBill') + '</button>';
    body += '</div></div>';
  });
  if (sumOpen > 0) {
    body += guestQrBuildOpenBillPayBarHtml(sumOpen,
      'closeModal();if(window.martPayTotalBar)martPayTotalBar(\\'Cash\\')',
      'closeModal();if(window.martPayTotalBar)martPayTotalBar(\\'Credit Card\\')',
      'closeModal();if(window.martPayTotalBarSeeInvoice)martPayTotalBarSeeInvoice()');
  }
  var label = t('restaurant.orderNumWord') + ' ' + slotNum;
  openModal('<div class="modal-header"><h2>' + label + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div><div class="modal-body" style="max-height:70vh;overflow-y:auto;">' + body + '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.close') + '</button></div>');
};"""

POS_BILL_MODAL_OLD = """window.posOpenOrderNumBillModal = function(slotNum) {
  var orders = posGetOrdersForOrderNum(slotNum);
  if (!orders.length) return;
  var escM = function(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  var body = '';
  orders.forEach(function(o) {
    var itemsStr = (o.items || []).map(function(i) { return escM(i.name) + ' ×' + i.qty; }).join(', ');
    var idS = String(o.id || '').replace(/\\\\/g, '\\\\\\\\').replace(/'/g, "\\\\'");
    body += '<div style="border:1px solid var(--border);border-radius:10px;padding:0.75rem;margin-bottom:0.6rem;background:var(--card-bg);">';
    body += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.35rem;"><strong>' + escM(o.orderNumber) + '</strong>';
    body += '<span class="status status-new">' + escM(t('minimart.statusOpen')) + '</span></div>';
    body += '<div style="font-size:0.82rem;margin:0.35rem 0;">' + itemsStr + '</div>';
    body += '<div style="font-weight:700;">' + fmt$(o.grandTotal) + '</div>';
    body += '<div style="display:flex;flex-wrap:wrap;gap:0.35rem;margin-top:0.45rem;">';
    body += '<button type="button" class="btn btn-sm btn-outline" onclick="closeModal();if(window.posOpenBillSeeInvoice)posOpenBillSeeInvoice(\\'' + idS + '\\')">' + t('common.seeInvoice') + '</button>';
    body += '<button type="button" class="btn btn-sm btn-warning" onclick="closeModal();if(window.posVoidOpenBill)posVoidOpenBill(\\'' + idS + '\\')">' + t('minimart.voidOpenBill') + '</button>';
    body += '</div></div>';
  });
  var label = t('restaurant.orderNumWord') + ' ' + slotNum;
  openModal('<div class="modal-header"><h2>' + label + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div><div class="modal-body">' + body + '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.close') + '</button></div>');
};"""

POS_BILL_MODAL_NEW = """window.posOpenOrderNumBillModal = function(slotNum) {
  if (typeof guestQrPreparePosSlotScope === 'function') guestQrPreparePosSlotScope(slotNum);
  var orders = posGetOrdersForOrderNum(slotNum);
  if (!orders.length) return;
  var escM = function(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); };
  var body = '';
  var sumOpen = Math.round(orders.reduce(function(s, o) { return s + (parseFloat(o.grandTotal) || 0); }, 0) * 100) / 100;
  orders.forEach(function(o) {
    var itemsStr = (o.items || []).map(function(i) { return escM(i.name) + ' ×' + i.qty; }).join(', ');
    var idS = String(o.id || '').replace(/\\\\/g, '\\\\\\\\').replace(/'/g, "\\\\'");
    body += '<div style="border:1px solid var(--border);border-radius:10px;padding:0.75rem;margin-bottom:0.6rem;background:var(--card-bg);">';
    body += '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.35rem;"><strong>' + escM(o.orderNumber) + '</strong>';
    body += '<span class="status status-new">' + escM(t('minimart.statusOpen')) + '</span></div>';
    body += '<div style="font-size:0.82rem;margin:0.35rem 0;">' + itemsStr + '</div>';
    body += '<div style="font-weight:700;">' + fmt$(o.grandTotal) + '</div>';
    body += '<div style="display:flex;flex-wrap:wrap;gap:0.35rem;margin-top:0.45rem;">';
    body += '<button type="button" class="btn btn-sm btn-success" onclick="closeModal();if(window.guestQrPayPosOpenBill)guestQrPayPosOpenBill(\\'' + idS + '\\',\\'Cash\\')">' + t('minimart.cash') + '</button>';
    body += '<button type="button" class="btn btn-sm btn-outline" onclick="closeModal();if(window.guestQrPayPosOpenBill)guestQrPayPosOpenBill(\\'' + idS + '\\',\\'Credit Card\\')">' + t('minimart.payTotalCard') + '</button>';
    body += '<button type="button" class="btn btn-sm btn-outline" onclick="closeModal();if(window.posOpenBillSeeInvoice)posOpenBillSeeInvoice(\\'' + idS + '\\')">' + t('common.seeInvoice') + '</button>';
    body += '<button type="button" class="btn btn-sm btn-warning" onclick="closeModal();if(window.posVoidOpenBill)posVoidOpenBill(\\'' + idS + '\\')">' + t('minimart.voidOpenBill') + '</button>';
    body += '</div></div>';
  });
  if (sumOpen > 0) {
    body += guestQrBuildOpenBillPayBarHtml(sumOpen,
      'closeModal();if(window.posPayTotalBar)posPayTotalBar(\\'Cash\\')',
      'closeModal();if(window.posPayTotalBar)posPayTotalBar(\\'Credit Card\\')',
      'closeModal();if(window.posPayTotalBarSeeInvoice)posPayTotalBarSeeInvoice()');
  }
  var label = t('restaurant.orderNumWord') + ' ' + slotNum;
  openModal('<div class="modal-header"><h2>' + label + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div><div class="modal-body" style="max-height:70vh;overflow-y:auto;">' + body + '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.close') + '</button></div>');
};"""

GUEST_QR_SLOTS_OLD = """function guestQrBuildSlotsHtml(dept, rows) {
  var bySlot = {};
  rows.forEach(function(r) {
    if (r.slotNum === '—') return;
    var s = String(r.slotNum);
    if (!bySlot[s]) bySlot[s] = r;
  });
  var html = '<div class="guest-qr-slots-grid">';
  for (var i = 1; i <= 60; i++) {
    var hit = bySlot[String(i)];
    var cls = 'guest-qr-slot' + (hit ? ' occupied' : '');
    var sub = hit ? ('<span class="guest-qr-slot-amt">' + (typeof fmt$ === 'function' ? fmt$(hit.grandTotal) : hit.grandTotal) + '</span><span class="guest-qr-slot-st">' + guestRestEsc(String(hit.status)) + '</span>') : '<span class="guest-qr-slot-free">' + (typeof uiT === 'function' ? uiT('guestQrReport.free', 'Free') : 'Free') + '</span>';
    html += '<div class="' + cls + '"><span class="guest-qr-slot-num">' + i + '</span>' + sub + '</div>';
  }
  html += '</div>';
  return html;
}"""

GUEST_QR_SLOTS_NEW = """function guestQrBuildSlotsHtml(dept, rows) {
  var bySlot = {};
  rows.forEach(function(r) {
    if (r.slotNum === '—') return;
    var s = String(r.slotNum);
    if (!bySlot[s]) bySlot[s] = r;
  });
  var html = '<div class="guest-qr-slots-grid">';
  for (var i = 1; i <= 60; i++) {
    var hit = bySlot[String(i)];
    var cls = 'guest-qr-slot' + (hit ? ' occupied' : '');
    var payCls = hit && typeof guestQrSlotIsPayable === 'function' && guestQrSlotIsPayable(hit) ? ' guest-qr-slot-payable' : '';
    var sub = hit ? ('<span class="guest-qr-slot-amt">' + (typeof fmt$ === 'function' ? fmt$(hit.grandTotal) : hit.grandTotal) + '</span><span class="guest-qr-slot-st">' + guestRestEsc(String(hit.status)) + '</span>') : '<span class="guest-qr-slot-free">' + (typeof uiT === 'function' ? uiT('guestQrReport.free', 'Free') : 'Free') + '</span>';
    var clickAttr = '';
    if (hit && typeof guestQrSlotIsPayable === 'function' && guestQrSlotIsPayable(hit)) {
      clickAttr = ' role="button" tabindex="0" title="' + (typeof uiT === 'function' ? uiT('guestQrReport.tapToPay', 'Tap to pay') : 'Tap to pay') + '" onclick="guestQrOpenSlotPayModal(\\'' + dept + '\\',' + i + ')"';
    }
    html += '<div class="' + cls + payCls + '"' + clickAttr + '><span class="guest-qr-slot-num">' + i + '</span>' + sub + '</div>';
  }
  html += '</div>';
  return html;
}"""

GUEST_QR_GRID_COL_OLD = """        { field: 'guestLabel', label: (typeof uiT === 'function' ? uiT('guestQrReport.colGuest', 'Guest') : 'Guest'), filterable: true, width: '100px' }
      ],"""

GUEST_QR_GRID_COL_NEW = """        { field: 'guestLabel', label: (typeof uiT === 'function' ? uiT('guestQrReport.colGuest', 'Guest') : 'Guest'), filterable: true, width: '100px' },
        { field: 'id', label: (typeof uiT === 'function' ? uiT('guestQrReport.colPay', 'Pay') : 'Pay'), width: '72px', format: function(v, row) {
          if (!row || typeof guestQrSlotIsPayable !== 'function' || !guestQrSlotIsPayable(row)) return '—';
          var slot = row.slotNum;
          if (slot === '—' || slot == null || isNaN(parseInt(String(slot), 10))) return '—';
          return '<button type="button" class="btn btn-sm btn-success" onclick="guestQrOpenSlotPayModal(\\'' + dept + '\\',' + parseInt(String(slot), 10) + ')">' + (typeof uiT === 'function' ? uiT('guestQrReport.payBtn', 'Pay') : 'Pay') + '</button>';
        } }
      ],"""

QR_PAY_CSS = """
    /* HRMM QR order pay */
    .guest-qr-slot-payable { cursor: pointer; }
    .guest-qr-slot-payable:hover { box-shadow: 0 0 0 2px rgba(26,115,232,0.35); transform: translateY(-1px); }
    /* __HRMM_QR_ORDER_PAY_MARKER__ */
"""
