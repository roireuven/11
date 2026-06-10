#!/usr/bin/env python3
"""Only Admin may edit invoices after creation (grid, modal, QR overrides, import)."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "HRMM-INVOICE-ADMIN-EDIT-v1"
INDEX = Path("public/index.html")

HELPERS = """
window.canEditInvoiceRecords = function() {
  return typeof currentRole !== 'undefined' && currentRole === 'Admin';
};
window.requireAdminInvoiceEdit = function() {
  if (window.canEditInvoiceRecords()) return true;
  if (typeof toast === 'function') {
    toast(typeof t === 'function' ? t('msg.adminOnlyInvoiceEdit') : 'Only Admin can edit invoices');
  }
  return false;
};
"""

INVOICES_ANCHOR = "// ===== INVOICES ====="

RENDER_OLD = """  invoiceGrid = new XGrid('invoiceGrid', {
    columns: [
      {field:'invoiceNumber',label:t('g.invoiceNumber'),filterable:true,width:'100px'},
      {field:'date',label:t('g.date'),format:v=>fmtDate(v),editable:true,editType:'date',filterable:true},
      {field:'guestName',label:t('g.guest'),editable:true,filterable:true},
      {field:'roomNumber',label:t('g.roomNumber'),editable:true,filterable:true,width:'70px'},
      {field:'subtotal',label:t('g.subtotal'),format:v=>fmt$(v),editable:true,editType:'number'},
      {field:'discountAmount',label:t('g.discount'),format:v=>fmt$(v),editable:true,editType:'number'},
      {field:'taxTotal',label:t('g.tax'),format:v=>fmt$(v),editable:true,editType:'number'},
      {field:'grandTotal',label:t('g.grandTotal'),format:v=>'<strong>'+fmt$(v)+'</strong>'},
      {field:'paymentStatus',label:t('g.paymentStatus'),format:v=>{const cls=v==='Fully Paid'?'paid':v==='Partially Paid'?'pending':'maintenance';return `<span class="status status-${cls}">${v}</span>`;},editable:true,editType:'select',editOptions:getInvoiceStatuses(),filterable:true},
      {field:'currency',label:t('g.currency'),editable:true,editType:'select',editOptions:getCurrencies(),width:'75px'},
    ],
    data: invoices,
    showSearch: true,
    emptyMessage: t('empty.noInvoices'),
    rowClass: function(row) {
      if (row.paymentStatus === 'Fully Paid') return 'row-status-success';
      if (row.paymentStatus === 'Partially Paid') return 'row-status-warning';
      if (row.paymentStatus === 'Unpaid') return 'row-status-error';
      return '';
    },
    summaryRow: {invoiceNumber:'label', subtotal:'sum', taxTotal:'sum', grandTotal:'sum'},
    hideExport: currentRole === 'Receptionist' || currentRole === 'Housekeeper',
    onAdd: () => showAddInvoice(),
    onImport: (rows) => { rows.forEach(r=>{if(!invoices.find(i=>i.id===r.id))invoices.push(r);}); save('invoices',invoices); logAudit('Import','Invoice','Imported '+rows.length+' rows'); renderInvoices(); },
    onEdit: (row, field, val) => {
      const inv = invoices.find(x=>x.id===row.id); if(!inv) return;
      inv[field]=val;
      if(field==='subtotal'||field==='discountAmount'||field==='taxTotal'){
        inv.grandTotal = (parseFloat(inv.subtotal)||0) - (parseFloat(inv.discountAmount)||0) + (parseFloat(inv.taxTotal)||0);
      }
      save('invoices',invoices); logAudit('Update','Invoice','Updated '+inv.invoiceNumber); toast(t('msg.invoiceUpdated')); renderInvoices();
    },
    actions: [
      {name:'seeInv',labelKey:'common.seeInvoice',cls:'btn-outline',handler:function(id) { const inv0 = (invoices || []).find(i => i.id === id); if (!inv0) return; if (inv0.paymentStatus === 'Fully Paid' && typeof openPostPaymentInvoiceFullScreen === 'function') openPostPaymentInvoiceFullScreen(inv0, null); else if (typeof openPostPaymentInvoiceFullScreen === 'function') openPostPaymentInvoiceFullScreen(inv0, { prepaidInvoice: true }); }},
      {name:'pay',labelKey:'common.pay',cls:'btn-success',condition:r=>r.paymentStatus!=='Fully Paid',handler:id=>{ payInvoice(id); }},
      {name:'edit',labelKey:'common.edit',cls:'btn-outline',handler:id=>showEditInvoice(id)},
      {name:'view',labelKey:'common.view',cls:'btn-outline',handler:id=>showInvoiceDetail(id)},
      {name:'delete',label:'✕',cls:'btn-danger',handler:id=>deleteInvoice(id)},
    ]
  });"""

RENDER_NEW = """  var invCanEdit = typeof canEditInvoiceRecords === 'function' && canEditInvoiceRecords();
  invoiceGrid = new XGrid('invoiceGrid', {
    columns: [
      {field:'invoiceNumber',label:t('g.invoiceNumber'),filterable:true,width:'100px'},
      {field:'date',label:t('g.date'),format:v=>fmtDate(v),editable:invCanEdit,editType:'date',filterable:true},
      {field:'guestName',label:t('g.guest'),editable:invCanEdit,filterable:true},
      {field:'roomNumber',label:t('g.roomNumber'),editable:invCanEdit,filterable:true,width:'70px'},
      {field:'subtotal',label:t('g.subtotal'),format:v=>fmt$(v),editable:invCanEdit,editType:'number'},
      {field:'discountAmount',label:t('g.discount'),format:v=>fmt$(v),editable:invCanEdit,editType:'number'},
      {field:'taxTotal',label:t('g.tax'),format:v=>fmt$(v),editable:invCanEdit,editType:'number'},
      {field:'grandTotal',label:t('g.grandTotal'),format:v=>'<strong>'+fmt$(v)+'</strong>'},
      {field:'paymentStatus',label:t('g.paymentStatus'),format:v=>{const cls=v==='Fully Paid'?'paid':v==='Partially Paid'?'pending':'maintenance';return `<span class="status status-${cls}">${v}</span>`;},editable:invCanEdit,editType:'select',editOptions:getInvoiceStatuses(),filterable:true},
      {field:'currency',label:t('g.currency'),editable:invCanEdit,editType:'select',editOptions:getCurrencies(),width:'75px'},
    ],
    data: invoices,
    showSearch: true,
    emptyMessage: t('empty.noInvoices'),
    rowClass: function(row) {
      if (row.paymentStatus === 'Fully Paid') return 'row-status-success';
      if (row.paymentStatus === 'Partially Paid') return 'row-status-warning';
      if (row.paymentStatus === 'Unpaid') return 'row-status-error';
      return '';
    },
    summaryRow: {invoiceNumber:'label', subtotal:'sum', taxTotal:'sum', grandTotal:'sum'},
    hideExport: currentRole === 'Receptionist' || currentRole === 'Housekeeper',
    onAdd: () => showAddInvoice(),
    onImport: invCanEdit ? (rows) => { rows.forEach(r=>{if(!invoices.find(i=>i.id===r.id))invoices.push(r);}); save('invoices',invoices); logAudit('Import','Invoice','Imported '+rows.length+' rows'); renderInvoices(); } : null,
    onEdit: invCanEdit ? (row, field, val) => {
      if (!requireAdminInvoiceEdit()) return;
      const inv = invoices.find(x=>x.id===row.id); if(!inv) return;
      inv[field]=val;
      if(field==='subtotal'||field==='discountAmount'||field==='taxTotal'){
        inv.grandTotal = (parseFloat(inv.subtotal)||0) - (parseFloat(inv.discountAmount)||0) + (parseFloat(inv.taxTotal)||0);
      }
      save('invoices',invoices); logAudit('Update','Invoice','Updated '+inv.invoiceNumber); toast(t('msg.invoiceUpdated')); renderInvoices();
    } : null,
    actions: [
      {name:'seeInv',labelKey:'common.seeInvoice',cls:'btn-outline',handler:function(id) { const inv0 = (invoices || []).find(i => i.id === id); if (!inv0) return; if (inv0.paymentStatus === 'Fully Paid' && typeof openPostPaymentInvoiceFullScreen === 'function') openPostPaymentInvoiceFullScreen(inv0, null); else if (typeof openPostPaymentInvoiceFullScreen === 'function') openPostPaymentInvoiceFullScreen(inv0, { prepaidInvoice: true }); }},
      {name:'pay',labelKey:'common.pay',cls:'btn-success',condition:r=>r.paymentStatus!=='Fully Paid',handler:id=>{ payInvoice(id); }},
      {name:'edit',labelKey:'common.edit',cls:'btn-outline',condition:function(){return invCanEdit;},handler:id=>showEditInvoice(id)},
      {name:'view',labelKey:'common.view',cls:'btn-outline',handler:id=>showInvoiceDetail(id)},
      {name:'delete',label:'✕',cls:'btn-danger',condition:function(){return invCanEdit;},handler:id=>deleteInvoice(id)},
    ]
  });"""

DELETE_OLD = "window.deleteInvoice = function(id) { if(!confirm(t('msg.deleteInvoice'))) return;"
DELETE_NEW = "window.deleteInvoice = function(id) { if (!requireAdminInvoiceEdit()) return; if(!confirm(t('msg.deleteInvoice'))) return;"

SHOW_EDIT_OLD = "window.showEditInvoice = function(id) {\n  const inv = invoices.find(i=>i.id===id); if(!inv) return;"
SHOW_EDIT_NEW = "window.showEditInvoice = function(id) {\n  if (!requireAdminInvoiceEdit()) return;\n  const inv = invoices.find(i=>i.id===id); if(!inv) return;"

UPDATE_OLD = "window.updateInvoice = function(id) {\n  const inv = invoices.find(i=>i.id===id); if(!inv) return;"
UPDATE_NEW = "window.updateInvoice = function(id) {\n  if (!requireAdminInvoiceEdit()) return;\n  const inv = invoices.find(i=>i.id===id); if(!inv) return;"

BODY_HTML_OLD = "  return pre + buildInvoiceBrandHeaderHtml(inv) + buildInvoiceQrHtml(inv, { editable: true }) +"
BODY_HTML_NEW = "  var invEditable = typeof canEditInvoiceRecords === 'function' && canEditInvoiceRecords() && inv && inv.id;\n  return pre + buildInvoiceBrandHeaderHtml(inv) + buildInvoiceQrHtml(inv, { editable: !!invEditable }) +"

APPLY_QR_OLD = "window.applyInvoiceQrEdit = function() {\n  var ctx = window._activeInvoiceQrCtx;\n  if (!ctx || !ctx.inv) return;"
APPLY_QR_NEW = "window.applyInvoiceQrEdit = function() {\n  if (!requireAdminInvoiceEdit()) return;\n  var ctx = window._activeInvoiceQrCtx;\n  if (!ctx || !ctx.inv) return;"

RESET_QR_OLD = "window.resetInvoiceQrEdit = function() {\n  var ctx = window._activeInvoiceQrCtx;\n  if (!ctx || !ctx.inv) return;"
RESET_QR_NEW = "window.resetInvoiceQrEdit = function() {\n  if (!requireAdminInvoiceEdit()) return;\n  var ctx = window._activeInvoiceQrCtx;\n  if (!ctx || !ctx.inv) return;"

MODAL_QR_OLD = "window.invoiceModalQrBrowseChanged = function(input) {\n  var ctx = window._activeInvoiceQrCtx;\n  if (!ctx || !ctx.inv) return;"
MODAL_QR_NEW = "window.invoiceModalQrBrowseChanged = function(input) {\n  if (!requireAdminInvoiceEdit()) return;\n  var ctx = window._activeInvoiceQrCtx;\n  if (!ctx || !ctx.inv) return;"

MODAL_LOGO_OLD = "window.invoiceModalLogoBrowseChanged = function(input) {"
MODAL_LOGO_NEW = "window.invoiceModalLogoBrowseChanged = function(input) {\n  if (!requireAdminInvoiceEdit()) return;"

LOCALE_SNIPPET = '"invoiceUpdated": "Invoice updated",'
LOCALE_INSERT = '"invoiceUpdated": "Invoice updated",\n    "adminOnlyInvoiceEdit": "Only Admin can edit invoices after they are created",'

VIEWPORT_OLD = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
VIEWPORT_NEW = '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">'


def patch(content: str) -> str:
    if MARKER in content and "canEditInvoiceRecords" in content:
        print(f"Already patched {MARKER} — skipping")
        return content

    if INVOICES_ANCHOR in content and "canEditInvoiceRecords" not in content:
        content = content.replace(INVOICES_ANCHOR, HELPERS + INVOICES_ANCHOR, 1)

    if RENDER_OLD in content:
        content = content.replace(RENDER_OLD, RENDER_NEW, 1)

    content = content.replace(DELETE_OLD, DELETE_NEW, 1)
    content = content.replace(SHOW_EDIT_OLD, SHOW_EDIT_NEW, 1)
    content = content.replace(UPDATE_OLD, UPDATE_NEW, 1)
    content = content.replace(BODY_HTML_OLD, BODY_HTML_NEW, 1)
    content = content.replace(APPLY_QR_OLD, APPLY_QR_NEW, 1)
    content = content.replace(RESET_QR_OLD, RESET_QR_NEW, 1)
    content = content.replace(MODAL_QR_OLD, MODAL_QR_NEW, 1)

    if "window.invoiceModalLogoBrowseChanged = function(input) {\n  if (!requireAdminInvoiceEdit())" not in content:
        content = content.replace(MODAL_LOGO_OLD, MODAL_LOGO_NEW, 1)

    if '"adminOnlyInvoiceEdit"' not in content and LOCALE_SNIPPET in content:
        content = content.replace(LOCALE_SNIPPET, LOCALE_INSERT)

    if VIEWPORT_OLD in content and "viewport-fit=cover" not in content:
        content = content.replace(VIEWPORT_OLD, VIEWPORT_NEW, 1)

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
    out = patch(index.read_text(encoding="utf-8"))
    if "canEditInvoiceRecords" not in out:
        print("Invoice admin edit patch failed", file=sys.stderr)
        return 1
    index.write_text(out, encoding="utf-8")
    print(f"patched {index} ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
