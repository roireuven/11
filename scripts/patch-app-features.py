#!/usr/bin/env python3
"""Patch HotelRestaurantMini-MartManagement: sell flows, audit log, inventory POS nav."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-FEATURES-v2"
INDEX = Path("public/index.html")

REST_ORDER_TYPE_OLD = "let restOrderType = 'Room Service';"
REST_ORDER_TYPE_NEW = "let restOrderType = 'Table';"

NO_AUTO_AUDIT_OLD = "const _noAutoAudit = {auditLog:1,bookingLog:1,inventoryLog:1,settings:1};"
NO_AUTO_AUDIT_NEW = (
    "const _noAutoAudit = {auditLog:1,bookingLog:1,inventoryLog:1,settings:1,"
    "transactions:1,invoices:1,serviceRequests:1,bookings:1};"
)

AUDIT_CAP_OLD = "if (auditLog.length > 2000) auditLog = auditLog.slice(-2000);"
AUDIT_CAP_NEW = "if (auditLog.length > 5000) auditLog = auditLog.slice(-5000);"

MINIMART_NAV = '      <a data-page="minimart"><span class="icon">&#128722;</span><span class="nav-txt" data-i18n="nav.minimart">Mini-Mart</span></a>'
POS_NAV = MINIMART_NAV + """
      <a data-page="pos"><span class="icon">&#128181;</span><span class="nav-txt" data-i18n="nav.pos">Inventory POS</span></a>"""

RBAC_OLD = """    'Manager': ['dashboard','rooms','bookings','guests','housekeeping','maintenance','services','invoices','reports','inventory','guestportal','restaurant','minimart','menuitems','storeitems','orderhistory','documentation'],
    'Receptionist': ['dashboard','rooms','bookings','guests','services','invoices','guestportal','restaurant','minimart','menuitems','inventory','documentation'],"""

RBAC_NEW = """    'Manager': ['dashboard','rooms','bookings','guests','housekeeping','maintenance','services','invoices','reports','inventory','guestportal','restaurant','minimart','pos','menuitems','storeitems','orderhistory','documentation'],
    'Receptionist': ['dashboard','rooms','bookings','guests','services','invoices','guestportal','restaurant','minimart','pos','menuitems','inventory','documentation'],"""

BNAV_OLD = """window.bnav = function(page) {
  if (currentRole === 'Kitchen' && page !== 'restaurant' && page !== 'documentation') {
    toast(t('msg.kitchenSidebarHint'));
    toggleSidebarFromNav();
    return;
  }
  if (page === 'pos') {
    window.__bnavPosToMinimart = true;
    page = 'minimart';
  }
  const link = document.querySelector('#sidebarNav a[data-page="' + page + '"]');
  if (link) link.click();
};"""

BNAV_NEW = """window.bnav = function(page) {
  if (currentRole === 'Kitchen' && page !== 'restaurant' && page !== 'documentation') {
    toast(t('msg.kitchenSidebarHint'));
    toggleSidebarFromNav();
    return;
  }
  if (page === 'pos') {
    var posLink = document.querySelector('#sidebarNav a[data-page="pos"]');
    if (posLink && posLink.style.display !== 'none') {
      posLink.click();
      return;
    }
    window.__bnavPosToMinimart = true;
    page = 'minimart';
  }
  const link = document.querySelector('#sidebarNav a[data-page="' + page + '"]');
  if (link) link.click();
};"""

BNAV_ACTIVE_OLD = "const match = p === page || (p === 'pos' && page === 'minimart') || (p === 'documentation' && page === 'documentation');"
BNAV_ACTIVE_NEW = "const match = p === page || (p === 'pos' && (page === 'minimart' || page === 'pos')) || (p === 'documentation' && page === 'documentation');"

SELL_SERVICE_FN = """
window.sellServiceWalkIn = function(serviceId) {
  var svc = services.find(function(x) { return x.id === serviceId; });
  if (!svc) return;
  var qty = 1;
  var price = parseFloat(svc.unitPrice) || 0;
  if (price <= 0) { toast(t('msg.enterValidPrice')); return; }
  var lineItems = [{ itemId: svc.id, name: svc.name, qty: qty, unitPrice: price }];
  var taxR = parseFloat(settings.serviceTax || settings.taxRate) || 7;
  var gtot = computeLineTotalsFromRawLineItems(lineItems, taxR).grandTotal;
  openCashPaymentModal({
    grandTotal: gtot,
    title: (typeof t === 'function' ? t('msg.serviceReqCashTitle', { name: svc.name }) : ('Service — ' + svc.name)),
    onValid: function(tender, change) {
      if (change > 0) toast(t('msg.changeDue', { amount: fmt$(change) }));
      var txn = processSale({
        source: 'Service', paymentMethod: 'Cash',
        roomNumber: '', guestName: 'Walk-in', bookingId: '',
        items: lineItems, taxRate: taxR
      });
      if (!txn) return;
      logAudit('Sale', 'Service', svc.id, 'Walk-in sale: ' + svc.name + ' ' + fmt$(gtot), svc.name + ' x1');
      toast(t('msg.saleCompleted'));
      renderServices();
    }
  });
};
"""

SERVICE_ACTIONS_OLD = """    actions: [
      {name:'edit',labelKey:'common.edit',cls:'btn-outline',handler:id=>showEditService(id)},
      {name:'delete',label:'✕',cls:'btn-danger',handler:id=>deleteService(id)},
    ]
  });
  new XGrid('svcReqGrid',"""

SERVICE_ACTIONS_NEW = """    actions: [
      {name:'sell',labelKey:'common.pay',cls:'btn-success',condition:function(r){return currentRole!=='Housekeeper'&&(parseFloat(r.unitPrice)||0)>0;},handler:function(id){sellServiceWalkIn(id);}},
      {name:'edit',labelKey:'common.edit',cls:'btn-outline',handler:id=>showEditService(id)},
      {name:'delete',label:'✕',cls:'btn-danger',handler:id=>deleteService(id)},
    ]
  });
  new XGrid('svcReqGrid',"""

PAY_INVOICE_OLD = """window.payInvoice = function(id) {
  const inv = invoices.find(i => i.id === id);
  if (!inv || inv.paymentStatus === 'Fully Paid') return;
  const gt = Math.round((parseFloat(inv.grandTotal) || 0) * 100) / 100;
  if (gt <= 0) {
    inv.paymentStatus = 'Fully Paid';
    save('invoices', invoices);
    logAudit('Payment', 'Invoice', inv.invoiceNumber + ' marked as Fully Paid');
    renderInvoices();
    toast(t('msg.invoicePaid'));
    setTimeout(function() { if (typeof openPostPaymentInvoiceFullScreen === 'function') openPostPaymentInvoiceFullScreen(inv, null); }, 0);
    return;
  }
  const payInvId = inv.id;
  openCashPaymentModal({
    grandTotal: gt,
    title: t('msg.invoiceCashTitle', { n: inv.invoiceNumber || '' }),
    onSeePrepaidInvoice: function() { if (typeof seeInvoiceFromGridDetail === 'function') seeInvoiceFromGridDetail(payInvId); },
    onValid: function(tender, change) {
      if (change > 0) toast(t('msg.changeDue', { amount: fmt$(change) }));
      inv.paymentStatus = 'Fully Paid';
      if (!inv.paymentTransactionId) inv.paymentTransactionId = nextTransactionId();
      save('invoices', invoices);
      logAudit('Payment', 'Invoice', inv.invoiceNumber + ' marked as Fully Paid (Cash)');
      renderInvoices();
      toast(t('msg.invoicePaid'));
      setTimeout(function() { if (typeof openPostPaymentInvoiceFullScreen === 'function') openPostPaymentInvoiceFullScreen(inv, null); }, 0);
    }
  });
};"""

PAY_INVOICE_NEW = """window.payInvoice = function(id) {
  const inv = invoices.find(i => i.id === id);
  if (!inv || inv.paymentStatus === 'Fully Paid') return;
  const gt = Math.round((parseFloat(inv.grandTotal) || 0) * 100) / 100;
  if (gt <= 0) {
    inv.paymentStatus = 'Fully Paid';
    save('invoices', invoices);
    logAudit('Payment', 'Invoice', inv.invoiceNumber, 'Marked as Fully Paid (zero balance)', '');
    renderInvoices();
    toast(t('msg.invoicePaid'));
    setTimeout(function() { if (typeof openPostPaymentInvoiceFullScreen === 'function') openPostPaymentInvoiceFullScreen(inv, null); }, 0);
    return;
  }
  const payInvId = inv.id;
  openCashPaymentModal({
    grandTotal: gt,
    title: t('msg.invoiceCashTitle', { n: inv.invoiceNumber || '' }),
    onSeePrepaidInvoice: function() { if (typeof seeInvoiceFromGridDetail === 'function') seeInvoiceFromGridDetail(payInvId); },
    onValid: function(tender, change) {
      if (change > 0) toast(t('msg.changeDue', { amount: fmt$(change) }));
      var wp = ensureWorkPeriodForSales('Hotel');
      if (!wp) return;
      var txnId = nextTransactionId();
      var lineItems = (inv.services || []).map(function(s) {
        return { itemId: '', name: s.name, qty: parseInt(s.quantity, 10) || 1, unitPrice: parseFloat(s.unitPrice) || 0 };
      });
      if (!lineItems.length && (parseFloat(inv.subtotal) || 0) > 0) {
        lineItems.push({ itemId: '', name: 'Invoice ' + (inv.invoiceNumber || ''), qty: 1, unitPrice: parseFloat(inv.subtotal) || gt });
      }
      var txn = {
        id: genId(), transactionId: txnId, timestamp: new Date().toISOString(),
        source: 'Hotel', orderId: inv.invoiceNumber || '',
        roomNumber: inv.roomNumber || '', guestName: inv.guestName || '',
        bookingId: inv.bookingId || '', workPeriodId: wp.id,
        items: lineItems.map(function(i) {
          return { itemId: i.itemId, name: i.name, qty: i.qty, unitPrice: i.unitPrice,
            total: (parseFloat(i.unitPrice) || 0) * (parseInt(i.qty, 10) || 0), inventoryDeducted: false };
        }),
        subtotal: parseFloat(inv.subtotal) || gt, taxRate: parseFloat(settings.taxRate) || 7,
        taxAmount: parseFloat(inv.taxTotal) || 0, grandTotal: gt,
        status: 'Completed', paymentMethod: 'Cash', invoiceId: inv.invoiceNumber || '', staffName: currentUser ? currentUser.name : currentRole
      };
      transactions.push(txn);
      save('transactions', transactions);
      inv.paymentStatus = 'Fully Paid';
      inv.paymentTransactionId = txnId;
      save('invoices', invoices);
      var itemsLine = lineItems.map(function(i) { return i.name + ' x' + i.qty; }).join(', ');
      logAudit('Payment', 'Invoice', inv.invoiceNumber, 'Paid ' + fmt$(gt) + ' (Cash)', txnId + (itemsLine ? ' | ' + itemsLine : ''));
      renderInvoices();
      toast(t('msg.invoicePaid'));
      setTimeout(function() { if (typeof openPostPaymentInvoiceFullScreen === 'function') openPostPaymentInvoiceFullScreen(inv, null); }, 0);
    }
  });
};"""

AUDIT_LOG_OLD = """function renderAuditLog() {
  document.getElementById('page-auditlog').innerHTML = `
    <div class="card"><div class="card-header"><h2>${t('ui.changeLogChit', { title: t('ui.masterAuditLog') })}</h2><button class="btn btn-danger btn-sm" onclick="clearAuditLog()">${t('common.clearLog')}</button></div><div class="card-body"><div id="masterLogGrid"></div></div></div>`;
  new XGrid('masterLogGrid', {
    columns: [
      {field:'timestamp',label:t('g.timestamp'),format:v=>{try{const d=new Date(v);return d.toLocaleDateString('en-US',{month:'short',day:'numeric'})+' '+d.toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit',second:'2-digit'});}catch(e){return v;}},filterable:true,width:'150px'},
      {field:'module',label:t('g.module'),filterable:true,width:'90px'},
      {field:'user',label:t('g.user'),filterable:true,width:'80px'},
      {field:'action',label:t('g.action'),filterable:true,width:'80px'},
      {field:'itemId',label:t('g.itemId'),filterable:true,width:'100px'},
      {field:'items',label:t('g.items'),filterable:true,width:'160px'},
      {field:'details',label:t('g.details'),filterable:true},
    ],
    data: auditLog.slice(),
    showSearch: true,
    emptyMessage: t('empty.noAudit'),
    trackVisible: false
  });
}"""

AUDIT_LOG_NEW = """function getAuditLogFiltered() {
  var mod = (document.getElementById('auditFilterModule') || {}).value || '';
  var act = (document.getElementById('auditFilterAction') || {}).value || '';
  var from = (document.getElementById('auditFilterFrom') || {}).value || '';
  var to = (document.getElementById('auditFilterTo') || {}).value || '';
  return auditLog.filter(function(row) {
    if (mod && String(row.module || '').toLowerCase().indexOf(mod.toLowerCase()) < 0) return false;
    if (act && String(row.action || '').toLowerCase() !== act.toLowerCase()) return false;
    if (from) { try { if (new Date(row.timestamp) < new Date(from + 'T00:00:00')) return false; } catch (e) {} }
    if (to) { try { if (new Date(row.timestamp) > new Date(to + 'T23:59:59')) return false; } catch (e) {} }
    return true;
  });
}
window.exportAuditLogCsv = function() {
  var rows = getAuditLogFiltered();
  if (!rows.length) { toast(t('empty.noAudit')); return; }
  var hdr = ['timestamp','module','user','action','itemId','items','details'];
  var lines = [hdr.join(',')];
  rows.forEach(function(r) {
    lines.push(hdr.map(function(k) {
      var v = String(r[k] == null ? '' : r[k]).replace(/"/g, '""');
      return '"' + v + '"';
    }).join(','));
  });
  var blob = new Blob([lines.join('\\n')], { type: 'text/csv;charset=utf-8' });
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'audit-log-' + (new Date().toISOString().slice(0, 10)) + '.csv';
  a.click();
  URL.revokeObjectURL(a.href);
  logAudit('Export', 'Audit', 'CSV', 'Exported ' + rows.length + ' audit rows', '');
};
function renderAuditLog() {
  var modules = [];
  auditLog.forEach(function(r) { if (r.module && modules.indexOf(r.module) < 0) modules.push(r.module); });
  modules.sort();
  var actions = [];
  auditLog.forEach(function(r) { if (r.action && actions.indexOf(r.action) < 0) actions.push(r.action); });
  actions.sort();
  document.getElementById('page-auditlog').innerHTML = `
    <div class="card"><div class="card-header"><h2>${t('ui.changeLogChit', { title: t('ui.masterAuditLog') })}</h2>
      <div style="display:flex;gap:0.35rem;flex-wrap:wrap;align-items:center;">
        <button class="btn btn-outline btn-sm" onclick="exportAuditLogCsv()">${t('common.export') || 'Export'}</button>
        <button class="btn btn-danger btn-sm" onclick="clearAuditLog()">${t('common.clearLog')}</button>
      </div>
    </div>
    <div class="card-body">
      <div class="form-row" style="margin-bottom:0.75rem;gap:0.5rem;flex-wrap:wrap;">
        <div class="form-group" style="min-width:120px;margin:0;"><label style="font-size:0.75rem;">${t('g.module')}</label>
          <select class="form-control" id="auditFilterModule" onchange="renderAuditLog()"><option value="">All</option>${modules.map(function(m){var s=String(m==null?'':m).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');return '<option value="'+s+'">'+s+'</option>';}).join('')}</select></div>
        <div class="form-group" style="min-width:120px;margin:0;"><label style="font-size:0.75rem;">${t('g.action')}</label>
          <select class="form-control" id="auditFilterAction" onchange="renderAuditLog()"><option value="">All</option>${actions.map(function(a){var s=String(a==null?'':a).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');return '<option value="'+s+'">'+s+'</option>';}).join('')}</select></div>
        <div class="form-group" style="min-width:120px;margin:0;"><label style="font-size:0.75rem;">From</label>
          <input type="date" class="form-control" id="auditFilterFrom" onchange="renderAuditLog()"></div>
        <div class="form-group" style="min-width:120px;margin:0;"><label style="font-size:0.75rem;">To</label>
          <input type="date" class="form-control" id="auditFilterTo" onchange="renderAuditLog()"></div>
      </div>
      <div id="masterLogGrid"></div>
    </div></div>`;
  new XGrid('masterLogGrid', {
    columns: [
      {field:'timestamp',label:t('g.timestamp'),format:v=>{try{const d=new Date(v);return d.toLocaleDateString('en-US',{month:'short',day:'numeric'})+' '+d.toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit',second:'2-digit'});}catch(e){return v;}},filterable:true,width:'150px'},
      {field:'module',label:t('g.module'),filterable:true,width:'90px'},
      {field:'user',label:t('g.user'),filterable:true,width:'80px'},
      {field:'action',label:t('g.action'),filterable:true,width:'80px'},
      {field:'itemId',label:t('g.itemId'),filterable:true,width:'100px'},
      {field:'items',label:t('g.items'),filterable:true,width:'160px'},
      {field:'details',label:t('g.details'),filterable:true},
    ],
    data: getAuditLogFiltered().slice().reverse(),
    showSearch: true,
    emptyMessage: t('empty.noAudit'),
    trackVisible: false
  });
}"""


def patch(content: str) -> str:
    if MARKER in content and "sellServiceWalkIn" in content and "exportAuditLogCsv" in content and REST_ORDER_TYPE_OLD not in content:
        print(f"Already patched {MARKER} — skipping")
        return content

    if REST_ORDER_TYPE_OLD in content:
        content = content.replace(REST_ORDER_TYPE_OLD, REST_ORDER_TYPE_NEW, 1)

    if NO_AUTO_AUDIT_OLD in content:
        content = content.replace(NO_AUTO_AUDIT_OLD, NO_AUTO_AUDIT_NEW, 1)

    content = content.replace(AUDIT_CAP_OLD, AUDIT_CAP_NEW)

    if MINIMART_NAV in content and 'data-page="pos"' not in content.split(MINIMART_NAV, 1)[1][:200]:
        content = content.replace(MINIMART_NAV, POS_NAV, 1)

    if RBAC_OLD in content:
        content = content.replace(RBAC_OLD, RBAC_NEW, 1)

    if BNAV_OLD in content:
        content = content.replace(BNAV_OLD, BNAV_NEW, 1)

    if BNAV_ACTIVE_OLD in content:
        content = content.replace(BNAV_ACTIVE_OLD, BNAV_ACTIVE_NEW, 1)

    if "function sellServiceWalkIn" not in content:
        content = content.replace(
            "// ===== SERVICES =====",
            SELL_SERVICE_FN + "\n// ===== SERVICES =====",
            1,
        )

    if SERVICE_ACTIONS_OLD in content:
        content = content.replace(SERVICE_ACTIONS_OLD, SERVICE_ACTIONS_NEW, 1)

    if PAY_INVOICE_OLD in content:
        content = content.replace(PAY_INVOICE_OLD, PAY_INVOICE_NEW, 1)

    if AUDIT_LOG_OLD in content:
        content = content.replace(AUDIT_LOG_OLD, AUDIT_LOG_NEW, 1)

    if MARKER not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )
    content = re.sub(r"<!-- HRMM-FEATURES-v\d+ -->", f"<!-- {MARKER} -->", content)

    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    patched = patch(text)
    index.write_text(patched, encoding="utf-8")
    print(f"Patched {index} — sell flows, audit log, inventory POS, restaurant table default")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
