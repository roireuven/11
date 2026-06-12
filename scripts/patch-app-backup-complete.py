#!/usr/bin/env python3
"""Complete backup/export/import — all tables in CSV ZIP + JSON, import confirm, CSV fallback."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-BACKUP-COMPLETE-v1"
INDEX = Path("public/index.html")

CSV_DEF_OLD = """  const csvDef = [
    { k: 'rooms', tr: 'settings.csvBtnRooms' },
    { k: 'guests', tr: 'settings.csvBtnGuests' },
    { k: 'bookings', tr: 'settings.csvBtnBookings' },
    { k: 'services', tr: 'settings.csvBtnServices' },
    { k: 'invoices', tr: 'settings.csvBtnInvoices' },
    { k: 'inventory', tr: 'settings.csvBtnInv' },
    { k: 'menuItems', tr: 'settings.csvBtnMenu' },
    { k: 'storeItems', tr: 'settings.csvBtnStore' },
    { k: 'tickets', tr: 'settings.csvBtnTickets' },
    { k: 'accounts', tr: 'settings.csvBtnAccounts' },
    { k: 'transactions', tr: 'settings.csvBtnTxn' },
    { k: 'posTransactions', tr: 'settings.csvBtnPos' },
    { k: 'restaurantOrders', tr: 'settings.csvBtnRest' },
    { k: 'martOpenOrders', tr: 'settings.csvBtnMartOpen' },
    { k: 'restaurantTables', tr: 'settings.csvBtnRestTables' },
    { k: 'serviceRequests', tr: 'settings.csvBtnSvcReq' },
    { k: 'messages', tr: 'settings.csvBtnMsg' },
    { k: 'workPeriods', tr: 'settings.csvBtnWorkPeriods' }
  ];"""

CSV_DEF_NEW = """  const csvDef = [
    { k: 'rooms', tr: 'settings.csvBtnRooms' },
    { k: 'guests', tr: 'settings.csvBtnGuests' },
    { k: 'bookings', tr: 'settings.csvBtnBookings' },
    { k: 'services', tr: 'settings.csvBtnServices' },
    { k: 'invoices', tr: 'settings.csvBtnInvoices' },
    { k: 'inventory', tr: 'settings.csvBtnInv' },
    { k: 'menuItems', tr: 'settings.csvBtnMenu' },
    { k: 'storeItems', tr: 'settings.csvBtnStore' },
    { k: 'tickets', tr: 'settings.csvBtnTickets' },
    { k: 'accounts', tr: 'settings.csvBtnAccounts' },
    { k: 'transactions', tr: 'settings.csvBtnTxn' },
    { k: 'posTransactions', tr: 'settings.csvBtnPos' },
    { k: 'restaurantOrders', tr: 'settings.csvBtnRest' },
    { k: 'martOpenOrders', tr: 'settings.csvBtnMartOpen' },
    { k: 'posOpenOrders', tr: 'settings.csvBtnPosOpen' },
    { k: 'restaurantTables', tr: 'settings.csvBtnRestTables' },
    { k: 'serviceRequests', tr: 'settings.csvBtnSvcReq' },
    { k: 'messages', tr: 'settings.csvBtnMsg' },
    { k: 'workPeriods', tr: 'settings.csvBtnWorkPeriods' },
    { k: 'auditLog', tr: 'settings.csvBtnAudit' },
    { k: 'bookingLog', tr: 'settings.csvBtnBookingLog' },
    { k: 'inventoryLog', tr: 'settings.csvBtnInventoryLog' }
  ];"""

EXPORT_BUTTONS_OLD = """        <button class="btn btn-primary" style="width:100%;justify-content:center;padding:0.75rem;" onclick="exportAllCSV()">◆ ${t('settings.exportAll')}</button>
        <button class="btn btn-outline" style="width:100%;justify-content:center;padding:0.75rem;" onclick="reloadBuiltInSampleData()">◆ ${t('settings.reloadDemo')}</button>"""

EXPORT_BUTTONS_NEW = """        <button class="btn btn-primary" style="width:100%;justify-content:center;padding:0.75rem;" onclick="exportAllCSV()">◆ ${t('settings.exportAll')}</button>
        <button class="btn btn-outline" style="width:100%;justify-content:center;padding:0.75rem;" onclick="exportAllData()">◆ ${t('settings.exportJson')}</button>
        <button class="btn btn-outline" style="width:100%;justify-content:center;padding:0.75rem;" onclick="reloadBuiltInSampleData()">◆ ${t('settings.reloadDemo')}</button>"""

BACKUP_P_OLD = '"backupP": "Export all data as a ZIP file of CSV files plus a full JSON backup for restore.",'
BACKUP_P_NEW = (
    '"backupP": "Export all data as a ZIP (every table CSV + settings.json + _backup.json) '
    'or download JSON only. Import accepts ZIP or JSON.",'
)

EXPORT_SINGLE_OLD = (
    "  const dataMap = {rooms,guests,bookings,services,invoices,inventory,menuItems,storeItems,"
    "tickets,accounts,transactions,posTransactions,restaurantOrders,martOpenOrders,posOpenOrders,"
    "restaurantTables,serviceRequests,messages,workPeriods};"
)

EXPORT_SINGLE_NEW = (
    "  const dataMap = {rooms,guests,bookings,services,invoices,inventory,menuItems,storeItems,"
    "tickets,accounts,transactions,posTransactions,restaurantOrders,martOpenOrders,posOpenOrders,"
    "restaurantTables,serviceRequests,messages,workPeriods,auditLog,bookingLog,inventoryLog};"
)

EXPORT_ALL_CSV_OLD = """window.exportAllCSV = function() {
  const tables = [
    {name:'rooms.csv', data:rooms},
    {name:'guests.csv', data:guests},
    {name:'bookings.csv', data:bookings.map(b=>({...b,services:JSON.stringify(b.services||[])}))},
    {name:'services.csv', data:services},
    {name:'invoices.csv', data:invoices.map(i=>({...i,services:JSON.stringify(i.services||[])}))},
    {name:'accounts.csv', data:accounts.map(a=>{const c={...a};delete c.password;return c;})},
    {name:'inventory.csv', data:inventory},
    {name:'tickets.csv', data:tickets},
    {name:'audit_log.csv', data:auditLog},
    {name:'booking_log.csv', data:bookingLog},
    {name:'inventory_log.csv', data:inventoryLog},
    {name:'pos_transactions.csv', data:posTransactions.map(p=>({...p,items:JSON.stringify(p.items||[])}))},
    {name:'menu_items.csv', data:menuItems},
    {name:'restaurant_orders.csv', data:restaurantOrders.map(o=>({...o,items:JSON.stringify(o.items||[])}))},
    {name:'mart_open_orders.csv', data:(martOpenOrders || []).map(o=>({...o,items:JSON.stringify(o.items||[])}))},
    {name:'pos_open_orders.csv', data:(posOpenOrders || []).map(o=>({...o,items:JSON.stringify(o.items||[])}))},
    {name:'restaurant_tables.csv', data:restaurantTables},
    {name:'store_items.csv', data:storeItems},
    {name:'service_requests.csv', data:serviceRequests},
    {name:'transactions.csv', data:transactions.map(t=>({...t,items:JSON.stringify(t.items||[])}))},
    {name:'work_periods.csv', data:workPeriods},
  ];
  const files = tables.filter(t=>t.data&&t.data.length).map(t=>({name:t.name, content:tableToCsv(t.data)}));
  const backupData = {rooms,guests,bookings,services,invoices,accounts,auditLog,settings,tickets,messages,inventory,bookingLog,inventoryLog,posTransactions,menuItems,restaurantOrders,martOpenOrders,posOpenOrders,restaurantTables,storeItems,serviceRequests,transactions,workPeriods};
  files.push({name:'_backup.json', content:JSON.stringify(backupData)});
  const zip = buildZip(files);
  let binStr = '';
  for (let i = 0; i < zip.length; i++) binStr += String.fromCharCode(zip[i]);
  const b64 = btoa(binStr);
  const a = document.createElement('a');
  a.href = 'data:application/zip;base64,' + b64;
  a.download = 'hotel_database_export_'+today()+'.zip';
  a.style.display = 'none';
  document.body.appendChild(a); a.click();
  setTimeout(()=>document.body.removeChild(a),500);
  logAudit('Export','System','Exported all data as CSV ZIP');
  toast(t('msg.csvZipStarted'));
};"""

EXPORT_ALL_CSV_NEW = """window.exportAllCSV = function() {
  const tables = [
    {name:'rooms.csv', data:rooms},
    {name:'guests.csv', data:guests},
    {name:'bookings.csv', data:bookings.map(b=>({...b,services:JSON.stringify(b.services||[])}))},
    {name:'services.csv', data:services},
    {name:'invoices.csv', data:invoices.map(i=>({...i,services:JSON.stringify(i.services||[])}))},
    {name:'accounts.csv', data:accounts.map(a=>{const c={...a};delete c.password;return c;})},
    {name:'inventory.csv', data:inventory},
    {name:'tickets.csv', data:tickets},
    {name:'messages.csv', data:messages},
    {name:'audit_log.csv', data:auditLog},
    {name:'booking_log.csv', data:bookingLog},
    {name:'inventory_log.csv', data:inventoryLog},
    {name:'pos_transactions.csv', data:posTransactions.map(p=>({...p,items:JSON.stringify(p.items||[])}))},
    {name:'menu_items.csv', data:menuItems},
    {name:'restaurant_orders.csv', data:restaurantOrders.map(o=>({...o,items:JSON.stringify(o.items||[])}))},
    {name:'mart_open_orders.csv', data:(martOpenOrders || []).map(o=>({...o,items:JSON.stringify(o.items||[])}))},
    {name:'pos_open_orders.csv', data:(posOpenOrders || []).map(o=>({...o,items:JSON.stringify(o.items||[])}))},
    {name:'restaurant_tables.csv', data:restaurantTables},
    {name:'store_items.csv', data:storeItems},
    {name:'service_requests.csv', data:serviceRequests},
    {name:'transactions.csv', data:transactions.map(t=>({...t,items:JSON.stringify(t.items||[])}))},
    {name:'work_periods.csv', data:workPeriods},
  ];
  const files = tables.map(function(t) {
    return { name: t.name, content: (t.data && t.data.length) ? tableToCsv(t.data) : '\\uFEFF' };
  });
  const backupData = {rooms,guests,bookings,services,invoices,accounts,auditLog,settings,tickets,messages,inventory,bookingLog,inventoryLog,posTransactions,menuItems,restaurantOrders,martOpenOrders,posOpenOrders,restaurantTables,storeItems,serviceRequests,transactions,workPeriods};
  files.push({name:'settings.json', content:JSON.stringify(settings || {}, null, 2)});
  files.push({name:'_backup.json', content:JSON.stringify(backupData)});
  const zip = buildZip(files);
  let binStr = '';
  for (let i = 0; i < zip.length; i++) binStr += String.fromCharCode(zip[i]);
  const b64 = btoa(binStr);
  const a = document.createElement('a');
  a.href = 'data:application/zip;base64,' + b64;
  a.download = 'hotel_database_export_'+today()+'.zip';
  a.style.display = 'none';
  document.body.appendChild(a); a.click();
  setTimeout(()=>document.body.removeChild(a),500);
  logAudit('Export','System','Exported all data as CSV ZIP');
  toast(t('msg.csvZipStarted'));
};"""

ZIP_HELPERS_OLD = """function extractJsonFromZip(arrayBuffer) {
  const view = new DataView(arrayBuffer);
  let offset = 0;
  while (offset < arrayBuffer.byteLength - 4) {
    if (view.getUint32(offset, true) !== 0x04034b50) break;
    const nameLen = view.getUint16(offset + 26, true);
    const extraLen = view.getUint16(offset + 28, true);
    const dataLen = view.getUint32(offset + 18, true);
    const nameBytes = new Uint8Array(arrayBuffer, offset + 30, nameLen);
    const name = new TextDecoder().decode(nameBytes);
    const dataStart = offset + 30 + nameLen + extraLen;
    if (name === '_backup.json') {
      const jsonBytes = new Uint8Array(arrayBuffer, dataStart, dataLen);
      return new TextDecoder().decode(jsonBytes);
    }
    offset = dataStart + dataLen;
  }
  return null;
}"""

ZIP_HELPERS_NEW = """function extractZipEntries(arrayBuffer) {
  const view = new DataView(arrayBuffer);
  const entries = {};
  let offset = 0;
  while (offset < arrayBuffer.byteLength - 4) {
    if (view.getUint32(offset, true) !== 0x04034b50) break;
    const nameLen = view.getUint16(offset + 26, true);
    const extraLen = view.getUint16(offset + 28, true);
    const dataLen = view.getUint32(offset + 18, true);
    const nameBytes = new Uint8Array(arrayBuffer, offset + 30, nameLen);
    const name = new TextDecoder().decode(nameBytes);
    const dataStart = offset + 30 + nameLen + extraLen;
    const dataBytes = new Uint8Array(arrayBuffer, dataStart, dataLen);
    entries[name] = new TextDecoder().decode(dataBytes);
    offset = dataStart + dataLen;
  }
  return entries;
}
function extractJsonFromZip(arrayBuffer) {
  const entries = extractZipEntries(arrayBuffer);
  if (entries['_backup.json']) return entries['_backup.json'];
  return null;
}
function parseCsvText(text) {
  if (!text) return [];
  if (text.charCodeAt(0) === 0xFEFF) text = text.substring(1);
  const lines = text.split('\\n').filter(function(l) { return l.trim(); });
  if (lines.length < 2) return [];
  function parseLine(line) {
    const result = []; let current = ''; let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (inQuotes) {
        if (ch === '"' && line[i + 1] === '"') { current += '"'; i++; }
        else if (ch === '"') { inQuotes = false; }
        else { current += ch; }
      } else {
        if (ch === '"') { inQuotes = true; }
        else if (ch === ',') { result.push(current); current = ''; }
        else { current += ch; }
      }
    }
    result.push(current);
    return result;
  }
  const headers = parseLine(lines[0]);
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const vals = parseLine(lines[i]);
    const obj = {};
    headers.forEach(function(h, idx) { obj[h] = vals[idx] != null ? vals[idx] : ''; });
    rows.push(obj);
  }
  return rows;
}
function reviveBackupJsonFields(rows, jsonFields) {
  if (!rows || !rows.length) return rows || [];
  return rows.map(function(row) {
    const copy = Object.assign({}, row);
    jsonFields.forEach(function(field) {
      if (typeof copy[field] === 'string' && copy[field].length > 1 && (copy[field][0] === '[' || copy[field][0] === '{')) {
        try { copy[field] = JSON.parse(copy[field]); } catch (e) {}
      }
    });
    return copy;
  });
}
function assembleBackupFromZipEntries(entries) {
  const map = {
    'rooms.csv': ['rooms', []],
    'guests.csv': ['guests', []],
    'bookings.csv': ['bookings', ['services']],
    'services.csv': ['services', []],
    'invoices.csv': ['invoices', ['services']],
    'accounts.csv': ['accounts', []],
    'inventory.csv': ['inventory', []],
    'tickets.csv': ['tickets', []],
    'messages.csv': ['messages', []],
    'audit_log.csv': ['auditLog', []],
    'booking_log.csv': ['bookingLog', []],
    'inventory_log.csv': ['inventoryLog', []],
    'pos_transactions.csv': ['posTransactions', ['items']],
    'menu_items.csv': ['menuItems', []],
    'restaurant_orders.csv': ['restaurantOrders', ['items']],
    'mart_open_orders.csv': ['martOpenOrders', ['items']],
    'pos_open_orders.csv': ['posOpenOrders', ['items']],
    'restaurant_tables.csv': ['restaurantTables', []],
    'store_items.csv': ['storeItems', []],
    'service_requests.csv': ['serviceRequests', []],
    'transactions.csv': ['transactions', ['items']],
    'work_periods.csv': ['workPeriods', []]
  };
  const out = {};
  Object.keys(map).forEach(function(fileName) {
    const spec = map[fileName];
    const key = spec[0];
    const jsonFields = spec[1];
    if (!entries[fileName]) return;
    out[key] = reviveBackupJsonFields(parseCsvText(entries[fileName]), jsonFields);
  });
  if (entries['settings.json']) {
    try { out.settings = JSON.parse(entries['settings.json']); } catch (e) {}
  }
  return out;
}"""

IMPORT_OLD = """window.importData = function(input) {
  const file = input.files[0]; if(!file) return;
  if (file.name.endsWith('.zip')) {
    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const jsonStr = extractJsonFromZip(e.target.result);
        if (!jsonStr) { toast(t('msg.zipNoData')); return; }
        const data = JSON.parse(jsonStr);
        restoreFromJson(data);
      } catch(err) { toast(t('msg.zipReadError', { message: String(err && err.message != null ? err.message : err) })); }
    };
    reader.readAsArrayBuffer(file);
  } else {
    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const data = JSON.parse(e.target.result);
        restoreFromJson(data);
      } catch(err) { toast(t('msg.invalidFile')); }
    };
    reader.readAsText(file);
  }
  input.value = '';
};"""

IMPORT_NEW = """window.importData = function(input) {
  const file = input.files[0]; if(!file) return;
  if (typeof t === 'function' && !confirm(t('settings.importConfirm'))) { input.value = ''; return; }
  if (file.name.endsWith('.zip')) {
    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const entries = extractZipEntries(e.target.result);
        let data = null;
        if (entries['_backup.json']) {
          data = JSON.parse(entries['_backup.json']);
        } else {
          data = assembleBackupFromZipEntries(entries);
          if (!data || !Object.keys(data).length) { toast(t('msg.zipNoData')); return; }
        }
        restoreFromJson(data);
      } catch(err) { toast(t('msg.zipReadError', { message: String(err && err.message != null ? err.message : err) })); }
    };
    reader.readAsArrayBuffer(file);
  } else {
    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const data = JSON.parse(e.target.result);
        restoreFromJson(data);
      } catch(err) { toast(t('msg.invalidFile')); }
    };
    reader.readAsText(file);
  }
  input.value = '';
};"""


def _add_locale_keys(content: str) -> str:
    if '"exportJson"' not in content:
        content = content.replace(
            '"exportAll": "Export all data (CSV ZIP)",',
            '"exportAll": "Export all data (CSV ZIP)",\n    "exportJson": "Export all data (JSON)",\n    "importConfirm": "Import will replace matching data in this browser. Export a backup first. Continue?",',
        )
    insert = (
        ',\n    "csvBtnMartOpen": "Mini-mart open bills",\n'
        '    "csvBtnPosOpen": "POS open bills",\n'
        '    "csvBtnAudit": "Audit log",\n'
        '    "csvBtnBookingLog": "Booking log",\n'
        '    "csvBtnInventoryLog": "Inventory log"'
    )
    if '"csvBtnMartOpen"' not in content:
        content = content.replace(
            '"csvBtnWorkPeriods": "Work periods"',
            '"csvBtnWorkPeriods": "Work periods"' + insert,
        )
    content = content.replace(BACKUP_P_OLD, BACKUP_P_NEW)
    return content


def patch(content: str) -> str:
    if MARKER in content and "assembleBackupFromZipEntries" in content:
        print(f"Already patched {MARKER} — skipping")
        return content

    content = _add_locale_keys(content)
    if CSV_DEF_OLD in content:
        content = content.replace(CSV_DEF_OLD, CSV_DEF_NEW, 1)
    if EXPORT_BUTTONS_OLD in content:
        content = content.replace(EXPORT_BUTTONS_OLD, EXPORT_BUTTONS_NEW, 1)
    if EXPORT_SINGLE_OLD in content:
        content = content.replace(EXPORT_SINGLE_OLD, EXPORT_SINGLE_NEW, 1)
    if EXPORT_ALL_CSV_OLD in content:
        content = content.replace(EXPORT_ALL_CSV_OLD, EXPORT_ALL_CSV_NEW, 1)
    if ZIP_HELPERS_OLD in content:
        content = content.replace(ZIP_HELPERS_OLD, ZIP_HELPERS_NEW, 1)
    if IMPORT_OLD in content:
        content = content.replace(IMPORT_OLD, IMPORT_NEW, 1)

    if MARKER not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )

    if "assembleBackupFromZipEntries" not in content:
        print("Backup patch failed — missing assembleBackupFromZipEntries", file=sys.stderr)
        return content

    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    patched = patch(text)
    if MARKER not in patched or "messages.csv" not in patched:
        print("Backup patch failed — verify exportAllCSV includes messages.csv", file=sys.stderr)
        return 1
    if "assembleBackupFromZipEntries" not in patched:
        print("Backup patch failed — missing CSV fallback import helpers", file=sys.stderr)
        return 1
    index.write_text(patched, encoding="utf-8")
    print(f"patched {index} ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
