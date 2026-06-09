"""Guest QR staff modal JS v11 — order number OR table pick (restaurant)."""

GUEST_QR_STAFF_JS_V11 = r"""
var guestOrderQrStaffCtx = { dept: 'restaurant', pickMode: 'orderNum', mode: 'room', room: '', guest: '', booking: '', table: '', orderNum: '' };
function guestOrderQrInvFromCtx(ctx) {
  ctx = ctx || guestOrderQrStaffCtx;
  if (ctx.dept !== 'minimart' && ctx.pickMode === 'table') {
    var tbl = String(ctx.table || '').trim();
    if (tbl) return { tableNumber: tbl };
    return {};
  }
  var on = String(ctx.orderNum || '').trim();
  if (on) return { orderNum: on };
  return {};
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
  if (ctx.dept !== 'minimart' && ctx.pickMode === 'table') {
    return String(ctx.table || '').trim() !== '';
  }
  var n = parseInt(String(ctx.orderNum || '').trim(), 10);
  return n >= 1 && n <= 60;
}
function guestOrderQrMissingContextHint(ctx) {
  ctx = ctx || guestOrderQrStaffCtx;
  if (ctx.dept !== 'minimart' && ctx.pickMode === 'table') {
    return (typeof uiT === 'function' ? uiT('guestOrder.selectTableFirst', 'Select a table first') : 'Select a table first');
  }
  return (typeof uiT === 'function' ? uiT('guestOrder.selectOrderNumFirst', 'Select order number first') : 'Select order number first');
}
function guestOrderQrRefreshPreview() {
  var img = document.getElementById('guestOrderQrImg');
  var cap = document.getElementById('guestOrderQrCaption');
  var link = document.getElementById('guestOrderQrLink');
  var url = guestOrderQrHasCustomerContext() ? guestOrderQrBuildUrl(guestOrderQrStaffCtx) : '';
  if (img) img.src = url ? buildInvoiceQrImageUrl(url) : '';
  if (cap) {
    if (url) cap.textContent = invoiceQrCaptionForPayload(url);
    else if (guestOrderQrStaffCtx.dept !== 'minimart' && guestOrderQrStaffCtx.pickMode === 'table') {
      cap.textContent = (typeof uiT === 'function' ? uiT('guestOrder.selectTableHint', 'Select table') : 'Select table');
    } else {
      cap.textContent = (typeof uiT === 'function' ? uiT('guestOrder.selectOrderNumHint', 'Select order number') : 'Select order number');
    }
  }
  if (link) link.value = url || '';
}
window.guestOrderQrSetDept = function(dept) {
  guestOrderQrStaffCtx.dept = dept === 'minimart' ? 'minimart' : 'restaurant';
  guestOrderQrStaffCtx.pickMode = 'orderNum';
  guestOrderQrStaffCtx.mode = 'room';
  guestOrderQrStaffCtx.room = '';
  guestOrderQrStaffCtx.guest = '';
  guestOrderQrStaffCtx.booking = '';
  guestOrderQrStaffCtx.table = '';
  guestOrderQrStaffCtx.orderNum = '';
  if (typeof openGuestOrderQrModal === 'function') openGuestOrderQrModal(true);
};
window.guestOrderQrSetPickMode = function(mode) {
  guestOrderQrStaffCtx.pickMode = mode === 'table' ? 'table' : 'orderNum';
  if (guestOrderQrStaffCtx.pickMode === 'table') guestOrderQrStaffCtx.orderNum = '';
  else guestOrderQrStaffCtx.table = '';
  if (typeof openGuestOrderQrModal === 'function') openGuestOrderQrModal(true);
  else guestOrderQrRefreshPreview();
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
  guestOrderQrStaffCtx.pickMode = 'table';
  guestOrderQrStaffCtx.table = val ? String(val).trim() : '';
  guestOrderQrStaffCtx.orderNum = '';
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
  guestOrderQrStaffCtx.pickMode = 'orderNum';
  guestOrderQrStaffCtx.orderNum = val ? String(val).trim() : '';
  guestOrderQrStaffCtx.table = '';
  guestOrderQrRefreshPreview();
};
window.openGuestOrderQrModal = function(deptOrKeepState) {
  if (!guestOrderQrStaffCtx || typeof guestOrderQrStaffCtx !== 'object') {
    guestOrderQrStaffCtx = { dept: 'restaurant', pickMode: 'orderNum', mode: 'room', room: '', guest: '', booking: '', table: '', orderNum: '' };
  }
  if (!guestOrderQrStaffCtx.pickMode) guestOrderQrStaffCtx.pickMode = 'orderNum';
  if (deptOrKeepState === 'restaurant' || deptOrKeepState === 'minimart') {
    guestOrderQrStaffCtx.dept = deptOrKeepState;
    guestOrderQrStaffCtx.pickMode = 'orderNum';
    guestOrderQrStaffCtx.mode = 'room';
    guestOrderQrStaffCtx.room = '';
    guestOrderQrStaffCtx.guest = '';
    guestOrderQrStaffCtx.booking = '';
    guestOrderQrStaffCtx.table = '';
    guestOrderQrStaffCtx.orderNum = '';
  } else if (deptOrKeepState !== true) {
    guestOrderQrStaffCtx = { dept: guestOrderQrStaffCtx.dept || 'restaurant', pickMode: 'orderNum', mode: 'room', room: '', guest: '', booking: '', table: '', orderNum: '' };
  }
  var dept = guestOrderQrStaffCtx.dept === 'minimart' ? 'minimart' : 'restaurant';
  if (dept === 'minimart') guestOrderQrStaffCtx.pickMode = 'orderNum';
  var pickMode = guestOrderQrStaffCtx.pickMode || 'orderNum';
  var tables = guestOrderQrListTables();
  var tableOpts = '<option value="">' + (typeof uiT === 'function' ? uiT('guestOrder.selectTable', '— Select table —') : '— Select table —') + '</option>';
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
  var orderNumOpts = '<option value="">' + (typeof uiT === 'function' ? uiT('guestOrder.selectOrderNum', '— Select order number —') : '— Select order number —') + '</option>';
  for (var on = 1; on <= 60; on++) {
    var onSel = String(guestOrderQrStaffCtx.orderNum) === String(on) ? ' selected' : '';
    var onLab = (typeof uiT === 'function' ? uiT('guestOrder.orderNumOption', 'Order number {n}', { n: on }) : 'Order number ' + on);
    orderNumOpts += '<option value="' + on + '"' + onSel + '>' + onLab + '</option>';
  }
  var leadText;
  if (dept === 'minimart') {
    leadText = (typeof uiT === 'function' ? uiT('guestOrder.leadMart', 'Scan this QR so the customer can self-order from the mini-mart. Pick an order number (1–60) below.') : 'Scan this QR so the customer can self-order from the mini-mart. Pick an order number (1–60) below.');
  } else if (pickMode === 'table') {
    leadText = (typeof uiT === 'function' ? uiT('guestOrder.leadRestTable', 'Scan this QR so the customer can self-order from the restaurant. Pick a table below — orders are linked to that table.') : 'Scan this QR so the customer can self-order from the restaurant. Pick a table below — orders are linked to that table.');
  } else {
    leadText = (typeof uiT === 'function' ? uiT('guestOrder.leadRest', 'Scan this QR so the customer can self-order from the restaurant. Pick an order number (1–60) below.') : 'Scan this QR so the customer can self-order from the restaurant. Pick an order number (1–60) below.');
  }
  var modalTitle = dept === 'minimart' ? (typeof uiT === 'function' ? uiT('guestOrder.modalTitleMart', 'Mini-Mart order QR') : 'Mini-Mart order QR') : (typeof uiT === 'function' ? uiT('guestOrder.modalTitleRest', 'Restaurant order QR') : 'Restaurant order QR');
  var html = '<div class="modal-hd"><h2>' + modalTitle + '</h2><button type="button" class="modal-close" onclick="closeModal()">&times;</button></div>' +
    '<div class="modal-body guest-order-qr-modal">' +
    '<p class="guest-order-qr-lead">' + leadText + '</p>' +
    '<div class="rest-order-type" style="margin-bottom:0.65rem;">' +
      '<button type="button" class="btn ' + (dept === 'restaurant' ? 'btn-primary' : 'btn-outline') + '" onclick="guestOrderQrSetDept(\'restaurant\')">' + (typeof uiT === 'function' ? uiT('guestOrder.restaurantQr', 'Restaurant QR') : 'Restaurant QR') + '</button>' +
      '<button type="button" class="btn ' + (dept === 'minimart' ? 'btn-primary' : 'btn-outline') + '" onclick="guestOrderQrSetDept(\'minimart\')">' + (typeof uiT === 'function' ? uiT('guestOrder.minimartQr', 'Mini-Mart QR') : 'Mini-Mart QR') + '</button>' +
    '</div>';
  if (dept === 'restaurant') {
    html += '<div class="rest-order-type guest-qr-pick-mode" style="margin-bottom:0.65rem;">' +
      '<button type="button" class="btn ' + (pickMode === 'orderNum' ? 'btn-primary' : 'btn-outline') + '" onclick="guestOrderQrSetPickMode(\'orderNum\')">' + (typeof uiT === 'function' ? uiT('guestOrder.pickByOrderNum', 'Order number') : 'Order number') + '</button>' +
      '<button type="button" class="btn ' + (pickMode === 'table' ? 'btn-primary' : 'btn-outline') + '" onclick="guestOrderQrSetPickMode(\'table\')">' + (typeof uiT === 'function' ? uiT('guestOrder.pickByTable', 'Table') : 'Table') + '</button>' +
    '</div>';
    if (pickMode === 'table') {
      html += '<div class="form-group"><label>' + (typeof uiT === 'function' ? uiT('guestOrder.table', 'Table') : 'Table') + '</label><select class="form-control" id="guestOrderQrTablePick" data-native-select="1" onchange="guestOrderQrPickTable(this.value)">' + tableOpts + '</select></div>';
    } else {
      html += '<div class="form-group"><label>' + (typeof uiT === 'function' ? uiT('guestOrder.orderNumber', 'Order number') : 'Order number') + '</label><select class="form-control" id="guestOrderQrOrderNumPick" data-native-select="1" onchange="guestOrderQrPickOrderNum(this.value)">' + orderNumOpts + '</select></div>';
    }
  } else {
    html += '<div class="form-group"><label>' + (typeof uiT === 'function' ? uiT('guestOrder.orderNumber', 'Order number') : 'Order number') + '</label><select class="form-control" id="guestOrderQrOrderNumPick" data-native-select="1" onchange="guestOrderQrPickOrderNum(this.value)">' + orderNumOpts + '</select></div>';
  }
  html += '<div class="guest-order-qr-preview"><img id="guestOrderQrImg" class="invoice-qr-img" alt="' + (typeof uiT === 'function' ? uiT('guestOrder.qrAlt', 'Order QR code') : 'Order QR code') + '">' +
    '<div id="guestOrderQrCaption" class="invoice-qr-caption">' + (typeof uiT === 'function' ? uiT('guestOrder.scanToOrder', 'Scan to order') : 'Scan to order') + '</div></div>' +
    '<div class="form-group"><label>' + (typeof uiT === 'function' ? uiT('guestOrder.orderLink', 'Order link') : 'Order link') + '</label><input type="text" class="form-control" id="guestOrderQrLink" readonly onclick="this.select()"></div>' +
    '<div class="guest-order-qr-actions">' +
      '<button type="button" class="btn btn-primary" onclick="guestOrderQrOpenCustomerScreen()">' + (typeof uiT === 'function' ? uiT('guestOrder.openOrderScreen', 'Open order screen') : 'Open order screen') + '</button>' +
      '<button type="button" class="btn btn-outline" onclick="guestOrderQrCopyLink()">' + (typeof uiT === 'function' ? uiT('guestOrder.copyLink', 'Copy link') : 'Copy link') + '</button>' +
    '</div></div>';
  openShellModal(html);
  guestOrderQrRefreshPreview();
};
window.guestOrderQrCopyLink = function() {
  var url = guestOrderQrBuildUrl(guestOrderQrStaffCtx);
  if (!url || !guestOrderQrHasCustomerContext()) { if (typeof toast === 'function') toast(guestOrderQrMissingContextHint()); return; }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url).then(function() { if (typeof toast === 'function') toast(typeof uiT === 'function' ? uiT('guestOrder.linkCopied', 'Link copied') : 'Link copied'); }).catch(function() {
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
