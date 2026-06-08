#!/usr/bin/env python3
"""QR order board (1–60), charts, Excel grid, and report popup on Restaurant and Mini-Mart."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-GUEST-QR-REPORTS-v3"
INDEX = Path("public/index.html")
JS_START = "/* HRMM guest QR orders board + report */"
JS_ANCHOR = "// ===== MENU ITEMS CRUD ====="

REST_BTN_OLD = (
    '<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">'
    '<button type="button" class="btn btn-sm btn-outline" onclick="restSelectedBooking=null;restCrmGuestId=null;restFocusAllTables=true;renderRestaurant()" title="'
)

REST_BTN_NEW = (
    '<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">'
    '<button type="button" class="btn btn-sm btn-primary guest-qr-report-btn" onclick="openGuestQrOrdersReport(\\\'restaurant\\\')">&#128202; QR Orders Report</button>'
    '<button type="button" class="btn btn-sm btn-outline" onclick="restSelectedBooking=null;restCrmGuestId=null;restFocusAllTables=true;renderRestaurant()" title="'
)

REST_BTN_BROKEN = (
    '<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">'
    '<button type="button" class="btn btn-sm btn-primary" onclick="openGuestQrOrdersReport(\'restaurant\')">QR Orders 1–60</button>'
    '<button type="button" class="btn btn-sm btn-outline" onclick="restSelectedBooking=null;restCrmGuestId=null;restFocusAllTables=true;renderRestaurant()" title="'
)

REST_BTN_V1 = (
    '<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">'
    '<button type="button" class="btn btn-sm btn-primary" onclick="openGuestQrOrdersReport(\\\'restaurant\\\')">QR Orders 1–60</button>'
    '<button type="button" class="btn btn-sm btn-outline" onclick="restSelectedBooking=null;restCrmGuestId=null;restFocusAllTables=true;renderRestaurant()" title="'
)

REST_NEW_ORDER_OLD = (
    "let html = '<div class=\"card\"><div class=\"card-header\"><h2>' + t('minimart.newOrder') + '</h2></div><div class=\"card-body\">' + orderTypeHtml + selHtml + '</div></div>';"
)

REST_NEW_ORDER_NEW = (
    "let html = '<div class=\"card\"><div class=\"card-header\" style=\"display:flex;flex-wrap:wrap;align-items:center;"
    "justify-content:space-between;gap:0.5rem;\"><h2 style=\"margin:0;\">' + t('minimart.newOrder') + '</h2>"
    "<button type=\"button\" class=\"btn btn-sm btn-primary guest-qr-report-btn\" onclick=\"openGuestQrOrdersReport(\\'restaurant\\')\">"
    "&#128202; QR Orders Report</button></div><div class=\"card-body\">' + orderTypeHtml + selHtml + '</div></div>';"
)

MART_BTN_OLD = """'<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">' +
    (hasMmContact ? '<button type="button" class="btn btn-sm btn-outline" onclick="martCrmGuest=null;martIsWalkin=true;martSelectedBooking=null;renderMiniMart()" title="' + esc(t('minimart.clearGuestFilterTitle')) + '">' + t('minimart.showAll') + '</button>' : '') +
    '<button type="button" class="btn btn-sm btn-outline" onclick="toggleMartHistory()">▲ ' + t('minimart.pastOrders') + '</button>' +"""

MART_BTN_NEW = """'<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">' +
    '<button type="button" class="btn btn-sm btn-primary guest-qr-report-btn" onclick="openGuestQrOrdersReport(\\'minimart\\')">&#128202; QR Orders Report</button>' +
    (hasMmContact ? '<button type="button" class="btn btn-sm btn-outline" onclick="martCrmGuest=null;martIsWalkin=true;martSelectedBooking=null;renderMiniMart()" title="' + esc(t('minimart.clearGuestFilterTitle')) + '">' + t('minimart.showAll') + '</button>' : '') +
    '<button type="button" class="btn btn-sm btn-outline" onclick="toggleMartHistory()">▲ ' + t('minimart.pastOrders') + '</button>' +"""

MART_BTN_V1 = """'<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">' +
    '<button type="button" class="btn btn-sm btn-primary" onclick="openGuestQrOrdersReport(\\'minimart\\')">QR Orders 1–60</button>' +
    (hasMmContact ? '<button type="button" class="btn btn-sm btn-outline" onclick="martCrmGuest=null;martIsWalkin=true;martSelectedBooking=null;renderMiniMart()" title="' + esc(t('minimart.clearGuestFilterTitle')) + '">' + t('minimart.showAll') + '</button>' : '') +
    '<button type="button" class="btn btn-sm btn-outline" onclick="toggleMartHistory()">▲ ' + t('minimart.pastOrders') + '</button>' +"""

MART_NEW_ORDER_OLD = (
    "const newOrderCard = '<div class=\"card\"><div class=\"card-header\"><h2>' + t('minimart.newOrder') + '</h2></div><div class=\"card-body\">' + selHtml + '</div></div>';"
)

MART_NEW_ORDER_NEW = (
    "const newOrderCard = '<div class=\"card\"><div class=\"card-header\" style=\"display:flex;flex-wrap:wrap;align-items:center;"
    "justify-content:space-between;gap:0.5rem;\"><h2 style=\"margin:0;\">' + t('minimart.newOrder') + '</h2>"
    "<button type=\"button\" class=\"btn btn-sm btn-primary guest-qr-report-btn\" onclick=\"openGuestQrOrdersReport(\\'minimart\\')\">"
    "&#128202; QR Orders Report</button></div><div class=\"card-body\">' + selHtml + '</div></div>';"
)

GUEST_QR_REPORTS_JS = r"""
/* HRMM guest QR orders board + report */
function guestQrIsQrOrder(o) {
  if (!o) return false;
  if (o.guestQrOrder === true || o.source === 'guestQr') return true;
  if (o.guestOrderNum != null && String(o.guestOrderNum).trim() !== '') return true;
  var gn = String(o.guestName || '');
  if (/^Order #\d+$/i.test(gn)) return true;
  return false;
}
function guestQrExtractOrderNum(o) {
  if (!o) return null;
  var n = parseInt(String(o.guestOrderNum != null ? o.guestOrderNum : '').trim(), 10);
  if (!isNaN(n) && n >= 1 && n <= 60) return n;
  n = parseInt(String(o.roomNumber != null ? o.roomNumber : '').trim(), 10);
  if (!isNaN(n) && n >= 1 && n <= 60 && guestQrIsQrOrder(o)) return n;
  var m = /^Order #(\d+)$/i.exec(String(o.guestName || '').trim());
  if (m) {
    n = parseInt(m[1], 10);
    if (!isNaN(n) && n >= 1 && n <= 60) return n;
  }
  return null;
}
function guestQrCollectOrders(dept) {
  var rows = [];
  if (dept === 'restaurant') {
    try { restaurantOrders = load('restaurantOrders', restaurantOrders); } catch (e) {}
    (restaurantOrders || []).forEach(function(o) {
      if (!o || !guestQrIsQrOrder(o)) return;
      if (typeof rowDataVisible === 'function' && !rowDataVisible(o)) return;
      var slot = guestQrExtractOrderNum(o);
      var items = Array.isArray(o.items) ? o.items.map(function(i) { return i.name + ' x' + i.qty; }).join(', ') : '';
      rows.push({
        id: o.id,
        slotNum: slot != null ? slot : '—',
        orderNumber: o.orderNumber || '—',
        timestamp: o.timestamp || '',
        status: o.status || '—',
        items: items,
        subtotal: o.subtotal != null ? o.subtotal : 0,
        tax: o.tax != null ? o.tax : 0,
        grandTotal: o.grandTotal != null ? o.grandTotal : 0,
        paidBy: o.paidBy || '—',
        guestLabel: o.guestName || '—',
        tableOrRoom: o.tableNumber || o.roomNumber || '—',
        _raw: o
      });
    });
  } else {
    try { martOpenOrders = load('martOpenOrders', martOpenOrders); } catch (e) {}
    try { posTransactions = load('posTransactions', posTransactions); } catch (e) {}
    (martOpenOrders || []).forEach(function(o) {
      if (!o || !guestQrIsQrOrder(o)) return;
      if (typeof rowDataVisible === 'function' && !rowDataVisible(o)) return;
      var slot = guestQrExtractOrderNum(o);
      var items = Array.isArray(o.items) ? o.items.map(function(i) { return i.name + ' x' + i.qty; }).join(', ') : '';
      rows.push({
        id: o.id,
        slotNum: slot != null ? slot : '—',
        orderNumber: o.orderNumber || '—',
        timestamp: o.timestamp || '',
        status: o.status || 'Open',
        items: items,
        subtotal: o.subtotal != null ? o.subtotal : 0,
        tax: o.tax != null ? o.tax : 0,
        grandTotal: o.grandTotal != null ? o.grandTotal : 0,
        paidBy: o.paidBy || 'Pending',
        guestLabel: o.guestName || '—',
        tableOrRoom: o.roomNumber || '—',
        _raw: o,
        _open: true
      });
    });
    (posTransactions || []).forEach(function(o) {
      if (!o || String(o.source || '') !== 'Mini-Mart') return;
      if (!guestQrIsQrOrder(o)) return;
      if (typeof rowDataVisible === 'function' && !rowDataVisible(o)) return;
      var slot = guestQrExtractOrderNum(o);
      var items = Array.isArray(o.items) ? o.items.map(function(i) { return i.name + ' x' + i.qty; }).join(', ') : '';
      rows.push({
        id: o.id,
        slotNum: slot != null ? slot : '—',
        orderNumber: o.transactionId || o.id || '—',
        timestamp: o.timestamp || '',
        status: 'Paid',
        items: items,
        subtotal: o.subtotal != null ? o.subtotal : 0,
        tax: o.tax != null ? o.tax : 0,
        grandTotal: o.grandTotal != null ? o.grandTotal : 0,
        paidBy: o.paidBy || '—',
        guestLabel: o.guestName || '—',
        tableOrRoom: o.roomNumber || '—',
        _raw: o,
        _open: false
      });
    });
  }
  rows.sort(function(a, b) {
    var sa = a.slotNum === '—' ? 999 : parseInt(a.slotNum, 10);
    var sb = b.slotNum === '—' ? 999 : parseInt(b.slotNum, 10);
    if (sa !== sb) return sa - sb;
    try { return new Date(b.timestamp) - new Date(a.timestamp); } catch (e) { return 0; }
  });
  return rows;
}
function guestQrBuildSlotsHtml(dept, rows) {
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
    var sub = hit ? ('<span class="guest-qr-slot-amt">' + (typeof fmt$ === 'function' ? fmt$(hit.grandTotal) : hit.grandTotal) + '</span><span class="guest-qr-slot-st">' + guestRestEsc(String(hit.status)) + '</span>') : '<span class="guest-qr-slot-free">Free</span>';
    html += '<div class="' + cls + '"><span class="guest-qr-slot-num">' + i + '</span>' + sub + '</div>';
  }
  html += '</div>';
  return html;
}
function guestQrReportSummary(rows) {
  var total = 0, open = 0, paid = 0, slots = {};
  rows.forEach(function(r) {
    total += parseFloat(r.grandTotal) || 0;
    if (String(r.status).toLowerCase() === 'paid' || String(r.paidBy).toLowerCase() === 'paid') paid++;
    else if (String(r.status).toLowerCase() !== 'void') open++;
    if (r.slotNum !== '—') slots[String(r.slotNum)] = true;
  });
  return { count: rows.length, total: total, open: open, paid: paid, slotsUsed: Object.keys(slots).length };
}
function guestQrBuildChartsHtml(rows) {
  var status = { Open: 0, Paid: 0, Other: 0 };
  var slotRev = {};
  var hours = {};
  (rows || []).forEach(function(r) {
    var st = String(r.status || '').toLowerCase();
    if (st === 'paid' || String(r.paidBy || '').toLowerCase() === 'paid') status.Paid++;
    else if (st === 'open' || st === 'pending' || st === 'new') status.Open++;
    else status.Other++;
    if (r.slotNum !== '—') {
      var s = String(r.slotNum);
      slotRev[s] = (slotRev[s] || 0) + (parseFloat(r.grandTotal) || 0);
    }
    try {
      var h = new Date(r.timestamp).getHours();
      if (!isNaN(h)) hours[h] = (hours[h] || 0) + 1;
    } catch (e) {}
  });
  var totalSt = status.Open + status.Paid + status.Other;
  if (!totalSt) totalSt = 1;
  var pPaid = Math.round(status.Paid / totalSt * 100);
  var pOpen = Math.round(status.Open / totalSt * 100);
  var pOther = Math.max(0, 100 - pPaid - pOpen);
  var donutStyle = 'background:conic-gradient(#42b72a 0 ' + pPaid + '%, #f5a623 ' + pPaid + '% ' + (pPaid + pOpen) + '%, #9aa0a6 ' + (pPaid + pOpen) + '% 100%)';
  var slotKeys = Object.keys(slotRev).sort(function(a, b) { return slotRev[b] - slotRev[a]; }).slice(0, 12);
  var maxRev = slotKeys.length ? slotRev[slotKeys[0]] : 1;
  var bars = slotKeys.map(function(k) {
    var pct = Math.max(6, Math.round((slotRev[k] / maxRev) * 100));
    return '<div class="guest-qr-bar-row"><span class="guest-qr-bar-lbl">#' + k + '</span><div class="guest-qr-bar-track"><div class="guest-qr-bar-fill" style="width:' + pct + '%"></div></div><span class="guest-qr-bar-val">' + (typeof fmt$ === 'function' ? fmt$(slotRev[k]) : slotRev[k]) + '</span></div>';
  }).join('');
  if (!bars) bars = '<p class="guest-qr-chart-empty">No slot revenue yet</p>';
  var hourKeys = Object.keys(hours).map(Number).sort(function(a, b) { return a - b; });
  var maxH = hourKeys.length ? Math.max.apply(null, hourKeys.map(function(h) { return hours[h]; })) : 1;
  var hourBars = hourKeys.map(function(h) {
    var pct = Math.max(8, Math.round((hours[h] / maxH) * 100));
    return '<div class="guest-qr-hbar" title="' + h + ':00 — ' + hours[h] + ' orders" style="height:' + pct + '%"><span>' + h + '</span></div>';
  }).join('');
  if (!hourBars) hourBars = '<p class="guest-qr-chart-empty">No time data yet</p>';
  return '<div class="guest-qr-charts">' +
    '<div class="guest-qr-chart-card"><h4>Status breakdown</h4><div class="guest-qr-donut-wrap"><div class="guest-qr-donut" style="' + donutStyle + '"></div><ul class="guest-qr-legend"><li><span class="dot paid"></span>Paid ' + status.Paid + ' (' + pPaid + '%)</li><li><span class="dot open"></span>Open ' + status.Open + ' (' + pOpen + '%)</li><li><span class="dot other"></span>Other ' + status.Other + ' (' + pOther + '%)</li></ul></div></div>' +
    '<div class="guest-qr-chart-card"><h4>Revenue by order # (top slots)</h4>' + bars + '</div>' +
    '<div class="guest-qr-chart-card guest-qr-chart-wide"><h4>Orders by hour of day</h4><div class="guest-qr-hour-chart">' + hourBars + '</div></div>' +
    '</div>';
}
window.exportGuestQrOrdersCsv = function(dept) {
  var rows = guestQrCollectOrders(dept);
  var head = ['Order #','System ID','Time','Status','Items','Subtotal','Tax','Total','Payment','Guest'];
  var lines = [head.join(',')];
  rows.forEach(function(r) {
    var esc = function(v) {
      var s = String(v == null ? '' : v);
      if (s.indexOf(',') >= 0 || s.indexOf('"') >= 0) return '"' + s.replace(/"/g, '""') + '"';
      return s;
    };
    lines.push([
      r.slotNum, r.orderNumber, r.timestamp, r.status, r.items,
      r.subtotal, r.tax, r.grandTotal, r.paidBy, r.guestLabel
    ].map(esc).join(','));
  });
  var blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8' });
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = (dept === 'restaurant' ? 'restaurant' : 'minimart') + '-qr-orders.csv';
  document.body.appendChild(a);
  a.click();
  setTimeout(function() { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  if (typeof toast === 'function') toast('CSV downloaded');
};
window.openGuestQrOrdersReport = function(dept) {
  dept = dept === 'minimart' ? 'minimart' : 'restaurant';
  var title = dept === 'restaurant' ? 'Restaurant QR orders report' : 'Mini-Mart QR orders report';
  var rows = guestQrCollectOrders(dept);
  var sum = guestQrReportSummary(rows);
  var html = '<div class="modal-hd"><h2>' + title + '</h2><button type="button" class="modal-close" onclick="closeModal()">&times;</button></div>' +
    '<div class="modal-body guest-qr-report-modal">' +
    '<div class="guest-qr-report-stats">' +
      '<div><span class="guest-qr-stat-lbl">QR orders</span><strong>' + sum.count + '</strong></div>' +
      '<div><span class="guest-qr-stat-lbl">Slots used</span><strong>' + sum.slotsUsed + ' / 60</strong></div>' +
      '<div><span class="guest-qr-stat-lbl">Open</span><strong>' + sum.open + '</strong></div>' +
      '<div><span class="guest-qr-stat-lbl">Revenue</span><strong>' + (typeof fmt$ === 'function' ? fmt$(sum.total) : sum.total) + '</strong></div>' +
    '</div>' +
    '<h3 class="guest-qr-report-subhd">Charts &amp; graphs</h3>' +
    guestQrBuildChartsHtml(rows) +
    '<h3 class="guest-qr-report-subhd">Order numbers 1–60</h3>' +
    guestQrBuildSlotsHtml(dept, rows) +
    '<div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin:0.85rem 0 0.65rem;">' +
      '<button type="button" class="btn btn-outline btn-sm" onclick="exportGuestQrOrdersCsv(\'' + dept + '\')">Export Excel (CSV)</button>' +
      '<button type="button" class="btn btn-outline btn-sm" onclick="openGuestQrOrdersReport(\'' + dept + '\')">Refresh</button>' +
    '</div>' +
    '<h3 class="guest-qr-report-subhd">All QR scan orders (spreadsheet)</h3>' +
    '<div id="guestQrReportGrid"></div></div>';
  openShellModal(html, { wide: true });
  if (typeof XGrid !== 'undefined') {
    new XGrid('guestQrReportGrid', {
      columns: [
        { field: 'slotNum', label: 'Order #', filterable: true, width: '72px' },
        { field: 'orderNumber', label: 'Ticket', filterable: true, width: '90px' },
        { field: 'timestamp', label: 'Time', format: function(v) { try { return new Date(v).toLocaleString(); } catch (e) { return v; } }, width: '130px' },
        { field: 'status', label: 'Status', filterable: true, width: '88px' },
        { field: 'items', label: 'Items' },
        { field: 'grandTotal', label: 'Total', format: function(v) { return typeof fmt$ === 'function' ? fmt$(v) : v; }, width: '80px' },
        { field: 'paidBy', label: 'Payment', filterable: true, width: '90px' },
        { field: 'guestLabel', label: 'Guest', filterable: true, width: '100px' }
      ],
      data: rows,
      summaryRow: { slotNum: 'label', grandTotal: 'sum' },
      emptyMessage: 'No QR scan orders yet'
    });
  }
};
"""

GUEST_QR_REPORTS_CSS = """
    /* HRMM guest QR orders report */
    .guest-qr-report-btn { white-space: nowrap; }
    .guest-qr-report-modal { max-width: min(1024px, 96vw); }
    .guest-qr-report-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 0.5rem; margin-bottom: 0.85rem; }
    .guest-qr-report-stats > div { background: var(--card-bg, #fff); border: 1px solid var(--border); border-radius: 10px; padding: 0.55rem 0.65rem; text-align: center; }
    .guest-qr-stat-lbl { display: block; font-size: 0.68rem; color: var(--text-light); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.15rem; }
    .guest-qr-report-subhd { font-size: 0.92rem; margin: 0.65rem 0 0.45rem; font-weight: 700; }
    .guest-qr-charts { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.65rem; margin-bottom: 0.75rem; }
    .guest-qr-chart-card { background: var(--card-bg, #fff); border: 1px solid var(--border); border-radius: 10px; padding: 0.65rem; }
    .guest-qr-chart-card h4 { font-size: 0.78rem; margin: 0 0 0.5rem; color: var(--text-light); text-transform: uppercase; letter-spacing: 0.04em; }
    .guest-qr-chart-wide { grid-column: 1 / -1; }
    .guest-qr-chart-empty { font-size: 0.78rem; color: var(--text-light); margin: 0.35rem 0; }
    .guest-qr-donut-wrap { display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }
    .guest-qr-donut { width: 88px; height: 88px; border-radius: 50%; flex-shrink: 0; box-shadow: inset 0 0 0 14px var(--card-bg, #fff); }
    .guest-qr-legend { list-style: none; margin: 0; padding: 0; font-size: 0.75rem; }
    .guest-qr-legend li { margin: 0.2rem 0; display: flex; align-items: center; gap: 0.35rem; }
    .guest-qr-legend .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
    .guest-qr-legend .dot.paid { background: #42b72a; }
    .guest-qr-legend .dot.open { background: #f5a623; }
    .guest-qr-legend .dot.other { background: #9aa0a6; }
    .guest-qr-bar-row { display: grid; grid-template-columns: 2rem 1fr auto; gap: 0.35rem; align-items: center; margin-bottom: 0.3rem; font-size: 0.72rem; }
    .guest-qr-bar-lbl { font-weight: 700; color: var(--primary); }
    .guest-qr-bar-track { height: 10px; background: rgba(0,0,0,0.06); border-radius: 6px; overflow: hidden; }
    body.dark-mode .guest-qr-bar-track { background: rgba(255,255,255,0.08); }
    .guest-qr-bar-fill { height: 100%; background: linear-gradient(90deg, #1a73e8, #42b72a); border-radius: 6px; min-width: 4px; }
    .guest-qr-bar-val { font-weight: 600; white-space: nowrap; }
    .guest-qr-hour-chart { display: flex; align-items: flex-end; gap: 0.35rem; min-height: 120px; padding: 0.25rem 0; }
    .guest-qr-hbar { flex: 1; min-width: 18px; max-width: 36px; background: linear-gradient(180deg, #1a73e8, #1557b0); border-radius: 6px 6px 2px 2px; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 0.15rem; font-size: 0.58rem; color: #fff; font-weight: 700; }
    .guest-qr-slots-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(72px, 1fr)); gap: 0.35rem; max-height: 220px; overflow-y: auto; padding: 0.15rem; border: 1px solid var(--border); border-radius: 10px; background: rgba(0,0,0,0.02); }
    body.dark-mode .guest-qr-slots-grid { background: rgba(255,255,255,0.03); }
    .guest-qr-slot { border: 1px solid var(--border); border-radius: 8px; padding: 0.35rem 0.25rem; text-align: center; min-height: 54px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.1rem; font-size: 0.62rem; background: var(--card-bg, #fff); }
    .guest-qr-slot.occupied { border-color: #1a73e8; background: rgba(26,115,232,0.08); }
    .guest-qr-slot-num { font-weight: 800; font-size: 0.82rem; line-height: 1.1; }
    .guest-qr-slot-amt { font-weight: 700; color: var(--primary); font-size: 0.6rem; }
    .guest-qr-slot-st { color: var(--text-light); font-size: 0.58rem; }
    .guest-qr-slot-free { color: var(--text-light); font-size: 0.58rem; }
    @media (max-width: 600px) {
      .guest-qr-slots-grid { grid-template-columns: repeat(5, 1fr); max-height: 200px; }
      .guest-qr-report-modal { max-width: 100%; }
      .guest-qr-charts { grid-template-columns: 1fr; }
    }
    /* __HRMM_GUEST_QR_REPORTS_MARKER__ */
"""


def _css_block() -> str:
    return GUEST_QR_REPORTS_CSS.replace("__HRMM_GUEST_QR_REPORTS_MARKER__", MARKER)


def _rest_btn_ok(content: str) -> bool:
    return "openGuestQrOrdersReport(\\'restaurant\\')" in content


def _is_fully_patched(content: str) -> bool:
    return (
        MARKER in content
        and "guestQrBuildChartsHtml" in content
        and "guest-qr-report-btn" in content
        and _rest_btn_ok(content)
        and REST_NEW_ORDER_NEW.split("guest-qr-report-btn")[0] in content
    )


def _upgrade_js_block(content: str) -> str:
    if JS_START not in content:
        return content
    if "guestQrBuildChartsHtml" in content:
        return content
    i0 = content.index(JS_START)
    i1 = content.find(JS_ANCHOR, i0)
    if i1 < 0:
        return content
    return content[:i0] + GUEST_QR_REPORTS_JS.strip() + "\n\n" + content[i1:]


def _upgrade_css_block(content: str) -> str:
    if MARKER in content and "guest-qr-charts" in content:
        return content
    old = re.search(
        r"\n\s*/\* HRMM guest QR orders report \*/\n.*?\n\s*/\* HRMM-GUEST-QR-REPORTS-v\d+ \*/\n",
        content,
        flags=re.DOTALL,
    )
    if old:
        return content[: old.start()] + "\n" + _css_block() + content[old.end() :]
    if f"/* {MARKER} */" not in content:
        content = content.replace("  </style>\n</head>", _css_block() + "  </style>\n</head>", 1)
    return content


def _apply_i18n_v3(content: str) -> str:
    """Wire QR report UI to uiT()."""
    if "uiT('guestQrReport.titleRest'" in content:
        return content

    pairs = [
        ("&#128202; QR Orders Report</button>", "&#128202; ' + (typeof uiT === 'function' ? uiT('guestOrder.qrReportBtn', 'QR Orders Report') : 'QR Orders Report') + '</button>"),
        ("'<span class=\"guest-qr-slot-free\">Free</span>'", "'<span class=\"guest-qr-slot-free\">' + (typeof uiT === 'function' ? uiT('guestQrReport.free', 'Free') : 'Free') + '</span>'"),
        ("bars = '<p class=\"guest-qr-chart-empty\">No slot revenue yet</p>'", "bars = '<p class=\"guest-qr-chart-empty\">' + (typeof uiT === 'function' ? uiT('guestQrReport.noSlotRevenue', 'No slot revenue yet') : 'No slot revenue yet') + '</p>'"),
        ("hourBars = '<p class=\"guest-qr-chart-empty\">No time data yet</p>'", "hourBars = '<p class=\"guest-qr-chart-empty\">' + (typeof uiT === 'function' ? uiT('guestQrReport.noTimeData', 'No time data yet') : 'No time data yet') + '</p>'"),
        ("<h4>Status breakdown</h4>", "<h4>' + (typeof uiT === 'function' ? uiT('guestQrReport.statusBreakdown', 'Status breakdown') : 'Status breakdown') + '</h4>"),
        ("<li><span class=\"dot paid\"></span>Paid ' + status.Paid", "<li><span class=\"dot paid\"></span>' + (typeof uiT === 'function' ? uiT('guestQrReport.paid', 'Paid') : 'Paid') + ' ' + status.Paid"),
        ("<li><span class=\"dot open\"></span>Open ' + status.Open", "<li><span class=\"dot open\"></span>' + (typeof uiT === 'function' ? uiT('guestQrReport.open', 'Open') : 'Open') + ' ' + status.Open"),
        ("<li><span class=\"dot other\"></span>Other ' + status.Other", "<li><span class=\"dot other\"></span>' + (typeof uiT === 'function' ? uiT('guestQrReport.other', 'Other') : 'Other') + ' ' + status.Other"),
        ("<h4>Revenue by order # (top slots)</h4>", "<h4>' + (typeof uiT === 'function' ? uiT('guestQrReport.revenueBySlot', 'Revenue by order # (top slots)') : 'Revenue by order # (top slots)') + '</h4>"),
        ("<h4>Orders by hour of day</h4>", "<h4>' + (typeof uiT === 'function' ? uiT('guestQrReport.ordersByHour', 'Orders by hour of day') : 'Orders by hour of day') + '</h4>"),
        ("toast('CSV downloaded')", "toast(typeof uiT === 'function' ? uiT('guestQrReport.csvDownloaded', 'CSV downloaded') : 'CSV downloaded')"),
        (
            "  var title = dept === 'restaurant' ? 'Restaurant QR orders report' : 'Mini-Mart QR orders report';",
            "  var title = dept === 'restaurant' ? (typeof uiT === 'function' ? uiT('guestQrReport.titleRest', 'Restaurant QR orders report') : 'Restaurant QR orders report') : (typeof uiT === 'function' ? uiT('guestQrReport.titleMart', 'Mini-Mart QR orders report') : 'Mini-Mart QR orders report');",
        ),
        ("<span class=\"guest-qr-stat-lbl\">QR orders</span>", "<span class=\"guest-qr-stat-lbl\">' + (typeof uiT === 'function' ? uiT('guestQrReport.qrOrders', 'QR orders') : 'QR orders') + '</span>"),
        ("<span class=\"guest-qr-stat-lbl\">Slots used</span>", "<span class=\"guest-qr-stat-lbl\">' + (typeof uiT === 'function' ? uiT('guestQrReport.slotsUsed', 'Slots used') : 'Slots used') + '</span>"),
        ("<span class=\"guest-qr-stat-lbl\">Open</span><strong>' + sum.open", "<span class=\"guest-qr-stat-lbl\">' + (typeof uiT === 'function' ? uiT('guestQrReport.open', 'Open') : 'Open') + '</span><strong>' + sum.open"),
        ("<span class=\"guest-qr-stat-lbl\">Revenue</span>", "<span class=\"guest-qr-stat-lbl\">' + (typeof uiT === 'function' ? uiT('guestQrReport.revenue', 'Revenue') : 'Revenue') + '</span>"),
        ("<h3 class=\"guest-qr-report-subhd\">Charts &amp; graphs</h3>", "<h3 class=\"guest-qr-report-subhd\">' + (typeof uiT === 'function' ? uiT('guestQrReport.charts', 'Charts & graphs') : 'Charts & graphs') + '</h3>"),
        ("<h3 class=\"guest-qr-report-subhd\">Order numbers 1–60</h3>", "<h3 class=\"guest-qr-report-subhd\">' + (typeof uiT === 'function' ? uiT('guestQrReport.orderNums', 'Order numbers 1–60') : 'Order numbers 1–60') + '</h3>"),
        (">Export Excel (CSV)</button>' +", ">' + (typeof uiT === 'function' ? uiT('guestQrReport.exportCsv', 'Export Excel (CSV)') : 'Export Excel (CSV)') + '</button>' +"),
        (">Refresh</button>' +", ">' + (typeof uiT === 'function' ? uiT('guestQrReport.refresh', 'Refresh') : 'Refresh') + '</button>' +"),
        ("<h3 class=\"guest-qr-report-subhd\">All QR scan orders (spreadsheet)</h3>", "<h3 class=\"guest-qr-report-subhd\">' + (typeof uiT === 'function' ? uiT('guestQrReport.spreadsheet', 'All QR scan orders (spreadsheet)') : 'All QR scan orders (spreadsheet)') + '</h3>"),
        ("{ field: 'slotNum', label: 'Order #'", "{ field: 'slotNum', label: (typeof uiT === 'function' ? uiT('guestQrReport.colOrderNum', 'Order #') : 'Order #')"),
        ("{ field: 'orderNumber', label: 'Ticket'", "{ field: 'orderNumber', label: (typeof uiT === 'function' ? uiT('guestQrReport.colTicket', 'Ticket') : 'Ticket')"),
        ("{ field: 'timestamp', label: 'Time'", "{ field: 'timestamp', label: (typeof uiT === 'function' ? uiT('guestQrReport.colTime', 'Time') : 'Time')"),
        ("{ field: 'status', label: 'Status'", "{ field: 'status', label: (typeof uiT === 'function' ? uiT('guestQrReport.colStatus', 'Status') : 'Status')"),
        ("{ field: 'items', label: 'Items'", "{ field: 'items', label: (typeof uiT === 'function' ? uiT('guestQrReport.colItems', 'Items') : 'Items')"),
        ("{ field: 'grandTotal', label: 'Total'", "{ field: 'grandTotal', label: (typeof uiT === 'function' ? uiT('guestQrReport.colTotal', 'Total') : 'Total')"),
        ("{ field: 'paidBy', label: 'Payment'", "{ field: 'paidBy', label: (typeof uiT === 'function' ? uiT('guestQrReport.colPayment', 'Payment') : 'Payment')"),
        ("{ field: 'guestLabel', label: 'Guest'", "{ field: 'guestLabel', label: (typeof uiT === 'function' ? uiT('guestQrReport.colGuest', 'Guest') : 'Guest')"),
        ("emptyMessage: 'No QR scan orders yet'", "emptyMessage: (typeof uiT === 'function' ? uiT('guestQrReport.noOrders', 'No QR scan orders yet') : 'No QR scan orders yet')"),
    ]
    for old, new in pairs:
        if old in content:
            content = content.replace(old, new, 1)
    content = re.sub(r"HRMM-GUEST-QR-REPORTS-v\d+", MARKER, content)
    return content


def _fix_button_labels(content: str) -> str:
    if REST_BTN_BROKEN in content:
        content = content.replace(REST_BTN_BROKEN, REST_BTN_NEW, 1)
    if REST_BTN_V1 in content:
        content = content.replace(REST_BTN_V1, REST_BTN_NEW, 1)
    if MART_BTN_V1 in content:
        content = content.replace(MART_BTN_V1, MART_BTN_NEW, 1)
    return content


def patch(content: str) -> str:
    content = _fix_button_labels(content)
    content = _upgrade_js_block(content)
    content = _upgrade_css_block(content)
    content = _apply_i18n_v3(content)

    if _is_fully_patched(content):
        print(f"Guest QR reports already patched {MARKER} — skipping")
        return content

    if REST_BTN_OLD in content and not _rest_btn_ok(content):
        content = content.replace(REST_BTN_OLD, REST_BTN_NEW, 1)

    if MART_BTN_OLD in content and "guest-qr-report-btn" not in content.split("function renderMiniMart")[1][:8000]:
        content = content.replace(MART_BTN_OLD, MART_BTN_NEW, 1)

    if REST_NEW_ORDER_OLD in content and REST_NEW_ORDER_NEW.split("guest-qr-report-btn")[0] not in content:
        content = content.replace(REST_NEW_ORDER_OLD, REST_NEW_ORDER_NEW, 1)

    mart_chunk = content.split("const newOrderCard", 1)
    if len(mart_chunk) > 1 and MART_NEW_ORDER_OLD in content and "guest-qr-report-btn" not in mart_chunk[1][:1500]:
        content = content.replace(MART_NEW_ORDER_OLD, MART_NEW_ORDER_NEW, 1)

    if JS_ANCHOR in content and "openGuestQrOrdersReport" not in content:
        content = content.replace(JS_ANCHOR, GUEST_QR_REPORTS_JS.strip() + "\n\n" + JS_ANCHOR, 1)

    content = re.sub(r"HRMM-GUEST-QR-REPORTS-v\d+", MARKER, content)
    if f"<!-- {MARKER} -->" not in content:
        content = re.sub(
            r"(<!-- HRMM-GUEST-QR-ORDER-v\d+ -->)",
            r"\1\n  <!-- " + MARKER + " -->",
            content,
            count=1,
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
    print(f"Patched {index} — QR report buttons, charts, and spreadsheet on Restaurant & Mini-Mart")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
