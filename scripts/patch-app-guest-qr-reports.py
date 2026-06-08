#!/usr/bin/env python3
"""QR order board (1–60) and report popup on Restaurant and Mini-Mart screens."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-GUEST-QR-REPORTS-v1"
INDEX = Path("public/index.html")

REST_BTN_OLD = (
    '<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">'
    '<button type="button" class="btn btn-sm btn-outline" onclick="restSelectedBooking=null;restCrmGuestId=null;restFocusAllTables=true;renderRestaurant()" title="'
)

REST_BTN_NEW = (
    '<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">'
    '<button type="button" class="btn btn-sm btn-primary" onclick="openGuestQrOrdersReport(\'restaurant\')">QR Orders 1–60</button>'
    '<button type="button" class="btn btn-sm btn-outline" onclick="restSelectedBooking=null;restCrmGuestId=null;restFocusAllTables=true;renderRestaurant()" title="'
)

MART_BTN_OLD = """'<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">' +
    (hasMmContact ? '<button type="button" class="btn btn-sm btn-outline" onclick="martCrmGuest=null;martIsWalkin=true;martSelectedBooking=null;renderMiniMart()" title="' + esc(t('minimart.clearGuestFilterTitle')) + '">' + t('minimart.showAll') + '</button>' : '') +
    '<button type="button" class="btn btn-sm btn-outline" onclick="toggleMartHistory()">▲ ' + t('minimart.pastOrders') + '</button>' +"""

MART_BTN_NEW = """'<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">' +
    '<button type="button" class="btn btn-sm btn-primary" onclick="openGuestQrOrdersReport(\\'minimart\\')">QR Orders 1–60</button>' +
    (hasMmContact ? '<button type="button" class="btn btn-sm btn-outline" onclick="martCrmGuest=null;martIsWalkin=true;martSelectedBooking=null;renderMiniMart()" title="' + esc(t('minimart.clearGuestFilterTitle')) + '">' + t('minimart.showAll') + '</button>' : '') +
    '<button type="button" class="btn btn-sm btn-outline" onclick="toggleMartHistory()">▲ ' + t('minimart.pastOrders') + '</button>' +"""

JS_ANCHOR = "// ===== MENU ITEMS CRUD ====="

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
  var title = dept === 'restaurant' ? 'Restaurant QR orders (1–60)' : 'Mini-Mart QR orders (1–60)';
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
    '<h3 class="guest-qr-report-subhd">Order numbers 1–60</h3>' +
    guestQrBuildSlotsHtml(dept, rows) +
    '<div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin:0.85rem 0 0.65rem;">' +
      '<button type="button" class="btn btn-outline btn-sm" onclick="exportGuestQrOrdersCsv(\'' + dept + '\')">Export CSV</button>' +
      '<button type="button" class="btn btn-outline btn-sm" onclick="openGuestQrOrdersReport(\'' + dept + '\')">Refresh</button>' +
    '</div>' +
    '<h3 class="guest-qr-report-subhd">All QR scan orders</h3>' +
    '<div id="guestQrReportGrid"></div></div>';
  openModal(html);
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
    .guest-qr-report-modal { max-width: min(960px, 96vw); }
    .guest-qr-report-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 0.5rem; margin-bottom: 0.85rem; }
    .guest-qr-report-stats > div { background: var(--card-bg, #fff); border: 1px solid var(--border); border-radius: 10px; padding: 0.55rem 0.65rem; text-align: center; }
    .guest-qr-stat-lbl { display: block; font-size: 0.68rem; color: var(--text-light); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.15rem; }
    .guest-qr-report-subhd { font-size: 0.92rem; margin: 0.65rem 0 0.45rem; font-weight: 700; }
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
    }
    /* __HRMM_GUEST_QR_REPORTS_MARKER__ */
"""


def _css_block() -> str:
    return GUEST_QR_REPORTS_CSS.replace("__HRMM_GUEST_QR_REPORTS_MARKER__", MARKER)


def patch(content: str) -> str:
    if MARKER in content and "openGuestQrOrdersReport" in content and REST_BTN_NEW.split("QR Orders")[0] in content:
        print(f"Guest QR reports already patched {MARKER} — skipping")
        return content

    if MARKER not in content:
        content = content.replace(
            "  </style>\n</head>",
            _css_block() + "  </style>\n</head>",
            1,
        )

    if JS_ANCHOR in content and "openGuestQrOrdersReport" not in content:
        content = content.replace(JS_ANCHOR, GUEST_QR_REPORTS_JS.strip() + "\n\n" + JS_ANCHOR, 1)

    if REST_BTN_OLD in content and "openGuestQrOrdersReport('restaurant')" not in content:
        content = content.replace(REST_BTN_OLD, REST_BTN_NEW, 1)

    if MART_BTN_OLD in content and "openGuestQrOrdersReport('minimart')" not in content:
        content = content.replace(MART_BTN_OLD, MART_BTN_NEW, 1)

    if MARKER not in content:
        content = content.replace(
            f"<!-- HRMM-GUEST-QR-ORDER-v9 -->",
            f"<!-- HRMM-GUEST-QR-ORDER-v9 -->\n  <!-- {MARKER} -->",
            1,
        )
        if f"<!-- {MARKER} -->" not in content:
            content = re.sub(
                r"(<!-- HRMM-GUEST-QR-ORDER-v\d+ -->)",
                r"\1\n  <!-- " + MARKER + " -->",
                content,
                count=1,
            )

    content = re.sub(r"HRMM-GUEST-QR-REPORTS-v\d+", MARKER, content)
    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — QR order board and report on Restaurant & Mini-Mart")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
