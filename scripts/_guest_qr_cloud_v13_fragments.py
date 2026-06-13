# Guest QR cloud sync — Firestore push from guest phone, staff ingest to local orders.

FIREBASE_SDK_SCRIPTS = """  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore-compat.js"></script>"""

GUEST_QR_CLOUD_JS_V13 = r"""
/* HRMM guest QR cloud sync v13 */
var guestQrCloudDb = null;
var guestQrCloudInitPromise = null;
var guestQrCloudStaffUnsub = null;
var guestQrCloudPollTimer = null;

function guestQrCloudEmailNamespace(email) {
  var s = String(email || '').toLowerCase().trim();
  var h = 0;
  for (var i = 0; i < s.length; i++) { h = ((h << 5) - h) + s.charCodeAt(i); h |= 0; }
  return 'ns' + (h >>> 0).toString(36);
}
window.guestQrCloudEmailNamespace = guestQrCloudEmailNamespace;

function guestQrCloudResolvePropertyNs(ctx) {
  ctx = ctx || {};
  if (ctx.propertyNs) return String(ctx.propertyNs).trim();
  try {
    var p = typeof parseGuestOrderParams === 'function' ? parseGuestOrderParams() : null;
    if (p && p.propertyNs) return String(p.propertyNs).trim();
  } catch (e) {}
  try {
    var ns = localStorage.getItem('hotel_mgr_dataNamespace');
    if (ns && String(ns).trim().length >= 2) return String(ns).trim();
  } catch (e2) {}
  try {
    if (typeof settings !== 'undefined' && settings && settings.setupEmail) {
      return guestQrCloudEmailNamespace(settings.setupEmail);
    }
    var em = localStorage.getItem((typeof DB_KEY !== 'undefined' ? DB_KEY : 'hotel_mgr_') + 'setupEmail');
    if (em) return guestQrCloudEmailNamespace(em);
  } catch (e3) {}
  return '';
}

function guestQrCloudIsGuestOnlySession() {
  try { return document.body && document.body.classList.contains('guest-rest-order-mode'); } catch (e) { return false; }
}

function guestQrCloudInit() {
  if (guestQrCloudInitPromise) return guestQrCloudInitPromise;
  guestQrCloudInitPromise = new Promise(function(resolve, reject) {
    if (typeof firebase === 'undefined') { reject(new Error('Firebase SDK not loaded')); return; }
    var done = function(db) { guestQrCloudDb = db; resolve(db); };
    try {
      if (firebase.apps && firebase.apps.length) {
        done(firebase.firestore());
        return;
      }
    } catch (e0) {}
    fetch('/__/firebase/init.json').then(function(r) { return r.json(); }).then(function(cfg) {
      if (!firebase.apps.length) firebase.initializeApp(cfg);
      done(firebase.firestore());
    }).catch(reject);
  });
  return guestQrCloudInitPromise;
}

function guestQrCloudOrdersCol(propertyNs) {
  return guestQrCloudDb.collection('guestQrOrders').doc(String(propertyNs)).collection('orders');
}

function guestQrCloudPushPayload(propertyNs, dept, payload) {
  return guestQrCloudInit().then(function() {
    var id = payload.orderId || (typeof genId === 'function' ? genId() : String(Date.now()));
    var doc = Object.assign({}, payload, {
      propertyNs: propertyNs,
      dept: dept,
      status: 'pending',
      orderId: id,
      createdAt: new Date().toISOString()
    });
    return guestQrCloudOrdersCol(propertyNs).doc(id).set(doc).then(function() { return id; });
  });
}

function guestQrCloudPushRestaurantOrder(order, tableLabel, mergeMode) {
  var propertyNs = guestQrCloudResolvePropertyNs(typeof guestRestCtx !== 'undefined' ? guestRestCtx : {});
  if (!propertyNs) return Promise.reject(new Error('missing propertyNs'));
  var payload = {
    orderId: order.id,
    table: tableLabel || order.guestQrTable || order.tableNumber || '',
    orderNum: order.guestOrderNum || '',
    room: order.roomNumber || '',
    guest: order.guestName || '',
    booking: order.bookingId || '',
    items: order.items || [],
    subtotal: order.subtotal,
    tax: order.tax,
    grandTotal: order.grandTotal,
    notes: order.notes || '',
    mergeMode: mergeMode || 'new',
    order: order
  };
  return guestQrCloudPushPayload(propertyNs, 'restaurant', payload);
}

function guestQrCloudPushMartOrder(order) {
  var propertyNs = guestQrCloudResolvePropertyNs(typeof guestMartCtx !== 'undefined' ? guestMartCtx : {});
  if (!propertyNs) return Promise.reject(new Error('missing propertyNs'));
  var payload = {
    orderId: order.id,
    orderNum: order.guestOrderNum || '',
    room: order.roomNumber || '',
    guest: order.guestName || '',
    booking: order.bookingId || '',
    items: order.items || [],
    subtotal: order.subtotal,
    tax: order.tax,
    grandTotal: order.grandTotal,
    order: order
  };
  return guestQrCloudPushPayload(propertyNs, 'minimart', payload);
}

function guestQrCloudMarkSynced(propertyNs, orderId) {
  return guestQrCloudInit().then(function() {
    return guestQrCloudOrdersCol(propertyNs).doc(orderId).update({
      status: 'synced',
      syncedAt: new Date().toISOString(),
      syncedBy: (typeof currentUser !== 'undefined' && currentUser && currentUser.name) ? currentUser.name : 'Staff'
    });
  });
}

function guestQrCloudBuildRestaurantOrderFromCloud(data) {
  var taxRate = parseFloat(settings && (settings.serviceTax || settings.taxRate)) || 7;
  var items = (data.items || []).map(function(ci) {
    return {
      menuItemId: ci.menuItemId || ci.storeItemId || ci.itemId || '',
      name: ci.name,
      qty: ci.qty,
      unitPrice: ci.unitPrice,
      total: (parseFloat(ci.unitPrice) || 0) * (parseInt(ci.qty, 10) || 0)
    };
  });
  var subtotal = data.subtotal != null ? data.subtotal : items.reduce(function(s, i) { return s + i.total; }, 0);
  var tax = data.tax != null ? data.tax : Math.round((subtotal * (taxRate / 100)) * 100) / 100;
  var grandTotal = data.grandTotal != null ? data.grandTotal : Math.round((subtotal + tax) * 100) / 100;
  var tableLabel = String(data.table || '').trim();
  var orderNum = String(data.orderNum || '').trim();
  var tableNumber;
  if (tableLabel) tableNumber = tableLabel;
  else if (orderNum) tableNumber = 'Order #' + orderNum;
  else if (data.room) tableNumber = 'Room ' + data.room;
  else tableNumber = 'QR Guest';
  var wp = typeof getActiveWorkPeriod === 'function' ? getActiveWorkPeriod('Restaurant') : null;
  if (!wp && typeof ensureGuestRestaurantWorkPeriod === 'function') wp = ensureGuestRestaurantWorkPeriod();
  var orderId = data.orderId || (typeof genId === 'function' ? genId() : String(Date.now()));
  return {
    id: orderId,
    timestamp: data.createdAt || new Date().toISOString(),
    orderNumber: typeof nextOrderNumber === 'function' ? nextOrderNumber() : ('RO-' + Date.now()),
    roomNumber: orderNum ? String(orderNum) : (data.room || ''),
    guestName: orderNum ? ('Order #' + orderNum) : (data.guest || (tableLabel ? 'Guest (Table QR)' : 'Guest')),
    bookingId: data.booking || '',
    guestOrderNum: orderNum || '',
    guestQrTable: tableLabel || '',
    tableNumber: tableNumber,
    items: items,
    subtotal: subtotal,
    tax: tax,
    grandTotal: grandTotal,
    status: 'Preparing',
    paidBy: 'Pending',
    staffName: 'Guest (QR scan)',
    notes: data.notes || '',
    workPeriodId: wp ? wp.id : '',
    diningFlow: 'kitchen',
    guestQrOrder: true,
    source: 'guestQr',
    guestQrCloud: true
  };
}

function guestQrCloudIngestRestaurantDoc(docSnap) {
  var data = docSnap.data();
  if (!data || data.status !== 'pending' || data.dept !== 'restaurant') return Promise.resolve();
  var propertyNs = guestQrCloudResolvePropertyNs();
  if (!propertyNs || data.propertyNs !== propertyNs) return Promise.resolve();
  try { restaurantOrders = load('restaurantOrders', restaurantOrders); } catch (e) { restaurantOrders = restaurantOrders || []; }
  if (!Array.isArray(restaurantOrders)) restaurantOrders = [];
  var orderId = data.orderId || docSnap.id;
  if (restaurantOrders.some(function(o) { return o && o.id === orderId; })) {
    return guestQrCloudMarkSynced(propertyNs, docSnap.id);
  }
  var tableLabel = String(data.table || '').trim();
  var items = (data.items || []).map(function(ci) {
    return {
      menuItemId: ci.menuItemId || ci.itemId || '',
      name: ci.name,
      qty: ci.qty,
      unitPrice: ci.unitPrice,
      total: (parseFloat(ci.unitPrice) || 0) * (parseInt(ci.qty, 10) || 0)
    };
  });
  var taxRate = parseFloat(settings && (settings.serviceTax || settings.taxRate)) || 7;
  var mergeTarget = tableLabel && typeof guestRestFindTableMergeTarget === 'function' ? guestRestFindTableMergeTarget(tableLabel) : null;
  if (data.mergeMode === 'merge' && mergeTarget && items.length) {
    if (typeof guestRestMergeCartIntoOrder === 'function') {
      guestRestMergeCartIntoOrder(mergeTarget, items, data.notes || '', taxRate);
    }
    mergeTarget.guestQrOrder = true;
    mergeTarget.source = mergeTarget.source || 'guestQr';
    mergeTarget.guestQrTable = tableLabel;
    mergeTarget.guestQrCloud = true;
  } else {
    var order = guestQrCloudBuildRestaurantOrderFromCloud(data);
    order.id = orderId;
    restaurantOrders.push(order);
  }
  try { save('restaurantOrders', restaurantOrders); } catch (e) {}
  try {
    if (typeof logAudit === 'function') {
      logAudit('New Order', 'Restaurant', orderId, 'Guest QR cloud order ingested' + (tableLabel ? (' (' + tableLabel + ')') : ''));
    }
  } catch (e2) {}
  if (tableLabel && typeof guestRestNotifyTableOrderUpdate === 'function') guestRestNotifyTableOrderUpdate(tableLabel);
  return guestQrCloudMarkSynced(propertyNs, docSnap.id);
}

function guestQrCloudIngestMartDoc(docSnap) {
  var data = docSnap.data();
  if (!data || data.status !== 'pending' || data.dept !== 'minimart') return Promise.resolve();
  var propertyNs = guestQrCloudResolvePropertyNs();
  if (!propertyNs || data.propertyNs !== propertyNs) return Promise.resolve();
  try { martOpenOrders = load('martOpenOrders', martOpenOrders); } catch (e) { martOpenOrders = martOpenOrders || []; }
  if (!Array.isArray(martOpenOrders)) martOpenOrders = [];
  var orderId = data.orderId || docSnap.id;
  if (martOpenOrders.some(function(o) { return o && o.id === orderId; })) {
    return guestQrCloudMarkSynced(propertyNs, docSnap.id);
  }
  var order = data.order || {};
  order.id = orderId;
  order.timestamp = data.createdAt || order.timestamp || new Date().toISOString();
  order.guestQrOrder = true;
  order.source = 'guestQr';
  order.guestQrCloud = true;
  if (!order.orderNumber && typeof martNextMiniMartOrderNumber === 'function') {
    order.orderNumber = martNextMiniMartOrderNumber();
  }
  martOpenOrders.push(order);
  try { save('martOpenOrders', martOpenOrders); } catch (e) {}
  return guestQrCloudMarkSynced(propertyNs, docSnap.id);
}

function guestQrCloudIngestDoc(docSnap) {
  var data = docSnap.data();
  if (!data) return Promise.resolve();
  if (data.dept === 'minimart') return guestQrCloudIngestMartDoc(docSnap);
  return guestQrCloudIngestRestaurantDoc(docSnap);
}

function guestQrCloudPullPendingOnce() {
  var propertyNs = guestQrCloudResolvePropertyNs();
  if (!propertyNs || guestQrCloudIsGuestOnlySession()) return Promise.resolve();
  return guestQrCloudInit().then(function() {
    return guestQrCloudOrdersCol(propertyNs).where('status', '==', 'pending').limit(40).get();
  }).then(function(snap) {
    var chain = Promise.resolve();
    snap.forEach(function(doc) {
      chain = chain.then(function() { return guestQrCloudIngestDoc(doc); });
    });
    return chain;
  }).catch(function(err) {
    try { console.warn('guestQrCloud pull', err); } catch (e) {}
  });
}

function guestQrCloudStartStaffSync() {
  if (guestQrCloudIsGuestOnlySession()) return;
  var propertyNs = guestQrCloudResolvePropertyNs();
  if (!propertyNs) return;
  guestQrCloudPullPendingOnce();
  if (guestQrCloudStaffUnsub) {
    try { guestQrCloudStaffUnsub(); } catch (e) {}
    guestQrCloudStaffUnsub = null;
  }
  guestQrCloudInit().then(function() {
    guestQrCloudStaffUnsub = guestQrCloudOrdersCol(propertyNs)
      .where('status', '==', 'pending')
      .onSnapshot(function(snap) {
        snap.docChanges().forEach(function(chg) {
          if (chg.type === 'added' || chg.type === 'modified') {
            guestQrCloudIngestDoc(chg.doc);
          }
        });
      }, function(err) {
        try { console.warn('guestQrCloud snapshot', err); } catch (e) {}
      });
  }).catch(function() {});
  if (!guestQrCloudPollTimer) {
    guestQrCloudPollTimer = setInterval(function() {
      if (typeof currentUser !== 'undefined' && currentUser) guestQrCloudPullPendingOnce();
    }, 20000);
  }
}

function guestQrCloudStopStaffSync() {
  if (guestQrCloudStaffUnsub) {
    try { guestQrCloudStaffUnsub(); } catch (e) {}
    guestQrCloudStaffUnsub = null;
  }
}
window.guestQrCloudStartStaffSync = guestQrCloudStartStaffSync;
window.guestQrCloudPullPendingOnce = guestQrCloudPullPendingOnce;
"""

BUILD_GUEST_ORDER_URL_PROPERTY_NS_OLD = """  if (inv) {
    var orderNumVal = inv.orderNum != null ? String(inv.orderNum).trim() : '';
    if (orderNumVal && orderNumVal !== '—') {
      params.set('orderNum', orderNumVal);
    } else {"""

BUILD_GUEST_ORDER_URL_PROPERTY_NS_NEW = """  var propertyNsVal = typeof guestQrCloudResolvePropertyNs === 'function' ? guestQrCloudResolvePropertyNs({}) : '';
  if (!propertyNsVal) {
    try {
      var nsL = localStorage.getItem('hotel_mgr_dataNamespace');
      if (nsL && String(nsL).trim().length >= 2) propertyNsVal = String(nsL).trim();
    } catch (eNs) {}
  }
  if (propertyNsVal) params.set('propertyNs', propertyNsVal);
  if (inv) {
    var orderNumVal = inv.orderNum != null ? String(inv.orderNum).trim() : '';
    if (orderNumVal && orderNumVal !== '—') {
      params.set('orderNum', orderNumVal);
    } else {"""

PARSE_GUEST_ORDER_PARAMS_PROPERTY_NS_OLD = "return { dept: go, room: sp.get('room') || '', guest: sp.get('guest') || '', booking: sp.get('booking') || '', table: sp.get('table') || '', orderNum: sp.get('orderNum') || '' };"

PARSE_GUEST_ORDER_PARAMS_PROPERTY_NS_NEW = "return { dept: go, room: sp.get('room') || '', guest: sp.get('guest') || '', booking: sp.get('booking') || '', table: sp.get('table') || '', orderNum: sp.get('orderNum') || '', propertyNs: sp.get('propertyNs') || '' };"

GUEST_CTX_PROPERTY_NS_OLD = "var guestRestCtx = { room: '', guest: '', booking: '', table: '', orderNum: '' };"
GUEST_CTX_PROPERTY_NS_NEW = "var guestRestCtx = { room: '', guest: '', booking: '', table: '', orderNum: '', propertyNs: '' };"

GUEST_MART_CTX_PROPERTY_NS_OLD = "var guestMartCtx = { room: '', guest: '', booking: '', table: '', orderNum: '' };"
GUEST_MART_CTX_PROPERTY_NS_NEW = "var guestMartCtx = { room: '', guest: '', booking: '', table: '', orderNum: '', propertyNs: '' };"

SHOW_GUEST_ORDER_CTX_OLD = """    guestMartCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '', orderNum: ctx.orderNum || '' };
    guestMartSubmitted = false;
  } else {
    guestRestCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '', orderNum: ctx.orderNum || '' };"""

SHOW_GUEST_ORDER_CTX_NEW = """    guestMartCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '', orderNum: ctx.orderNum || '', propertyNs: ctx.propertyNs || '' };
    guestMartSubmitted = false;
  } else {
    guestRestCtx = { room: ctx.room || '', guest: ctx.guest || '', booking: ctx.booking || '', table: ctx.table || '', orderNum: ctx.orderNum || '', propertyNs: ctx.propertyNs || '' };"""

# Patch guestRestSubmitOrder tail — after local save, cloud push; guest-only relies on cloud.
GUEST_REST_SUBMIT_CLOUD_TAIL_OLD = """  if (tableLabel) guestRestNotifyTableOrderUpdate(tableLabel);
  guestRestCart = [];
  guestRestSubmitted = true;
  renderGuestRestaurantOrder();
};"""

GUEST_REST_SUBMIT_CLOUD_TAIL_NEW = """  if (tableLabel) guestRestNotifyTableOrderUpdate(tableLabel);
  var propertyNs = guestQrCloudResolvePropertyNs(guestRestCtx);
  var cloudPayload = {
    id: mergeTarget ? mergeTarget.id : (typeof genId === 'function' ? genId() : String(Date.now())),
    items: items,
    notes: notes,
    subtotal: subtotal,
    tax: tax,
    grandTotal: grandTotal,
    guestQrTable: tableLabel,
    tableNumber: tableNumber,
    guestOrderNum: orderNum,
    roomNumber: orderNum ? String(orderNum) : (guestRestCtx.room || ''),
    guestName: orderNum ? ('Order #' + orderNum) : (guestRestCtx.guest || (tableLabel ? 'Guest (Table QR)' : 'Guest')),
    bookingId: guestRestCtx.booking || ''
  };
  var finishGuest = function() {
    guestRestCart = [];
    guestRestSubmitted = true;
    renderGuestRestaurantOrder();
  };
  if (propertyNs) {
    guestQrCloudPushRestaurantOrder(cloudPayload, tableLabel, mergeTarget ? 'merge' : 'new').then(function() {
      finishGuest();
    }).catch(function(err) {
      if (guestQrCloudIsGuestOnlySession()) {
        if (typeof toast === 'function') toast('Could not send order. Check internet and try again.');
        try { console.warn('guest QR cloud push', err); } catch (e) {}
        return;
      }
      finishGuest();
    });
    return;
  }
  if (guestQrCloudIsGuestOnlySession()) {
    if (typeof toast === 'function') toast('Order link is outdated — ask staff for a new QR code.');
    return;
  }
  finishGuest();
};"""

GUEST_MART_SUBMIT_CLOUD_OLD = """  martOpenOrders.push(order);
  try { save('martOpenOrders', martOpenOrders); } catch (e) {}
  try { if (typeof logAudit === 'function') logAudit('Insert', 'martOpenOrders', order.id, 'Guest QR mini-mart order ' + orderNum); } catch (e) {}
  guestMartCart = []; guestMartSubmitted = true; renderGuestMiniMartOrder();
};"""

GUEST_MART_SUBMIT_CLOUD_NEW = """  var propertyNsMart = guestQrCloudResolvePropertyNs(guestMartCtx);
  var finishMart = function() {
    guestMartCart = []; guestMartSubmitted = true; renderGuestMiniMartOrder();
  };
  var saveMartLocal = function() {
    martOpenOrders.push(order);
    try { save('martOpenOrders', martOpenOrders); } catch (e) {}
    try { if (typeof logAudit === 'function') logAudit('Insert', 'martOpenOrders', order.id, 'Guest QR mini-mart order ' + orderNum); } catch (e) {}
  };
  if (!guestQrCloudIsGuestOnlySession()) saveMartLocal();
  if (propertyNsMart) {
    guestQrCloudPushMartOrder(order).then(function() { finishMart(); }).catch(function(err) {
      if (guestQrCloudIsGuestOnlySession()) {
        if (typeof toast === 'function') toast('Could not send order. Check internet and try again.');
        try { console.warn('guest QR cloud mart', err); } catch (e) {}
        return;
      }
      finishMart();
    });
    return;
  }
  if (guestQrCloudIsGuestOnlySession()) {
    if (typeof toast === 'function') toast('Order link is outdated — ask staff for a new QR code.');
    return;
  }
  finishMart();
};"""

LOGIN_SUCCESS_CLOUD_HOOK_OLD = """  applyRBAC();
  navigateToDefaultPage();"""

LOGIN_SUCCESS_CLOUD_HOOK_NEW = """  applyRBAC();
  if (typeof guestQrCloudStartStaffSync === 'function') guestQrCloudStartStaffSync();
  navigateToDefaultPage();"""

AUTOLOGIN_UI_CLOUD_HOOK_OLD = """          applyRBAC();
          navigateToDefaultPage();"""

AUTOLOGIN_UI_CLOUD_HOOK_NEW = """          applyRBAC();
          if (typeof guestQrCloudStartStaffSync === 'function') guestQrCloudStartStaffSync();
          navigateToDefaultPage();"""

GUEST_QR_OPEN_CUSTOMER_PROPERTY_NS_OLD = """    orderNum: guestOrderQrStaffCtx.orderNum || ''
  });
};"""

GUEST_QR_OPEN_CUSTOMER_PROPERTY_NS_NEW = """    orderNum: guestOrderQrStaffCtx.orderNum || '',
    propertyNs: guestOrderQrStaffCtx.propertyNs || (typeof guestQrCloudResolvePropertyNs === 'function' ? guestQrCloudResolvePropertyNs({}) : '')
  });
};"""

