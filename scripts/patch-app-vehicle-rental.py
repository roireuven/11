#!/usr/bin/env python3
"""Vehicle rental module — boutique fleet v2 with calendar, messaging, contract, P&L."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

MARKER = "HRMM-VEHICLE-RENTAL-v2"
INDEX = Path("public/index.html")
ROOT = Path(__file__).resolve().parents[1]
V2_MODULE = ROOT / "scripts" / "_vehicle_rental_v2_module.js"

NAV_ANCHOR = (
    '      <a data-page="pos"><span class="icon">&#128181;</span>'
    '<span class="nav-txt" data-i18n="nav.pos">Inventory POS</span></a>'
)
NAV_NEW = (
    '      <a data-page="pos"><span class="icon">&#128181;</span>'
    '<span class="nav-txt" data-i18n="nav.pos">Inventory POS</span></a>\n'
    '      <a data-page="vehiclerental"><span class="icon">&#128663;</span>'
    '<span class="nav-txt" data-i18n="nav.vehiclerental">Vehicle Rental</span></a>'
)

PAGE_ANCHOR = '      <div class="page" id="page-pos"></div>'
PAGE_NEW = (
    '      <div class="page" id="page-pos"></div>\n'
    '      <div class="page" id="page-vehiclerental"></div>'
)

DATA_ANCHOR = "let storeItems = load('storeItems', null);"
VEHICLE_DATA_ANCHOR = "let rentCrmGuestId = null;"

RENDER_PAGE_OLD = (
    "const fn = {dashboard:renderDashboard,rooms:renderRooms,bookings:renderBookings,"
    "guests:renderGuests,housekeeping:renderHousekeeping,maintenance:renderMaintenance,"
    "services:renderServices,invoices:renderInvoices,guestportal:renderGuestPortal,"
    "reports:renderReports,accounts:renderAccounts,auditlog:renderAuditLog,"
    "settings:renderSettings,inventory:renderInventory,pos:renderPOS,"
    "restaurant:renderRestaurant,minimart:renderMiniMart,menuitems:renderMenuItems,"
    "storeitems:renderStoreItems,orderhistory:renderOrderHistory,"
    "alltransactions:renderAllTransactions,messagelog:renderMessageLog,"
    "dropdowns:renderDropdowns,documentation:renderDocumentation};"
)
RENDER_PAGE_NEW = (
    "const fn = {dashboard:renderDashboard,rooms:renderRooms,bookings:renderBookings,"
    "guests:renderGuests,housekeeping:renderHousekeeping,maintenance:renderMaintenance,"
    "services:renderServices,invoices:renderInvoices,guestportal:renderGuestPortal,"
    "reports:renderReports,accounts:renderAccounts,auditlog:renderAuditLog,"
    "settings:renderSettings,inventory:renderInventory,pos:renderPOS,"
    "restaurant:renderRestaurant,minimart:renderMiniMart,vehiclerental:renderVehicleRental,"
    "menuitems:renderMenuItems,storeitems:renderStoreItems,orderhistory:renderOrderHistory,"
    "alltransactions:renderAllTransactions,messagelog:renderMessageLog,"
    "dropdowns:renderDropdowns,documentation:renderDocumentation};"
)

PAGE_TITLES_OLD = (
    "orderhistory:'Order History',alltransactions:'Transactions',messagelog:'Messages',"
    "dropdowns:'Dropdown Lists'};"
)
PAGE_TITLES_NEW = (
    "orderhistory:'Order History',alltransactions:'Transactions',messagelog:'Messages',"
    "dropdowns:'Dropdown Lists',vehiclerental:'Vehicle Rental'};"
)

RBAC_MANAGER_OLD = (
    "'Manager': ['dashboard','rooms','bookings','guests','housekeeping','maintenance',"
    "'services','invoices','reports','inventory','guestportal','restaurant','minimart',"
    "'pos','menuitems','storeitems','orderhistory','documentation'],"
)
RBAC_MANAGER_NEW = (
    "'Manager': ['dashboard','rooms','bookings','guests','housekeeping','maintenance',"
    "'services','invoices','reports','inventory','guestportal','restaurant','minimart',"
    "'pos','vehiclerental','menuitems','storeitems','orderhistory','documentation'],"
)

RBAC_RECEPTION_OLD = (
    "'Receptionist': ['dashboard','rooms','bookings','guests','services','invoices',"
    "'guestportal','restaurant','minimart','pos','menuitems','inventory','documentation'],"
)
RBAC_RECEPTION_NEW = (
    "'Receptionist': ['dashboard','rooms','bookings','guests','services','invoices',"
    "'guestportal','restaurant','minimart','pos','vehiclerental','menuitems',"
    "'inventory','documentation'],"
)

NORMALIZE_OLD = (
    "  if (s.indexOf('hotel') >= 0) return 'Hotel';\n"
    "  // PMS / room services, etc. (processSale source \"Service\")\n"
    "  if (s.indexOf('service') >= 0) return 'Hotel';"
)
NORMALIZE_NEW = (
    "  if (s.indexOf('hotel') >= 0) return 'Hotel';\n"
    "  if (s.indexOf('vehicle') >= 0 || s.indexOf('rental') >= 0) return 'Hotel';\n"
    "  // PMS / room services, etc. (processSale source \"Service\")\n"
    "  if (s.indexOf('service') >= 0) return 'Hotel';"
)

DASH_ROW_OLD = (
    "  var invSum = 0;\n"
    "  (invoices || []).forEach(function(inv) { if (rowDataVisible(inv) && inv.date === ymd) "
    "invSum += parseFloat(inv.grandTotal) || 0; });\n"
    "  var hotel = (filterShift === 'TOTAL') ? invSum : invSum / 3;\n"
    "  var rest = 0, mm = 0;"
)
DASH_ROW_NEW = (
    "  var invSum = 0;\n"
    "  (invoices || []).forEach(function(inv) { if (rowDataVisible(inv) && inv.date === ymd) "
    "invSum += parseFloat(inv.grandTotal) || 0; });\n"
    "  var rentalRev = 0;\n"
    "  (transactions || []).forEach(function(tx) {\n"
    "    if (!rowDataVisible(tx) || tx.source !== 'Vehicle Rental') return;\n"
    "    var d = dashTimestampDay(tx.timestamp);\n"
    "    if (d !== ymd) return;\n"
    "    if (!dashFnBMatchesShift(tx.timestamp, filterShift)) return;\n"
    "    rentalRev += parseFloat(tx.grandTotal) || 0;\n"
    "  });\n"
    "  var hotel = (filterShift === 'TOTAL') ? invSum + rentalRev : invSum / 3 + rentalRev;\n"
    "  var rest = 0, mm = 0;"
)

DASH_SHIFT_OLD = (
    "  (posTransactions || []).forEach(function(p) {\n"
    "    if (!rowDataVisible(p)) return;\n"
    "    var d = dashTimestampDay(p.timestamp);\n"
    "    if (!d || d < from || d > to) return;\n"
    "    var s = dashShiftNameFromTimestamp(p.timestamp);\n"
    "    sums[s] = (sums[s] || 0) + (parseFloat(p.grandTotal) || 0);\n"
    "  });\n"
    "  return sums;"
)
DASH_SHIFT_NEW = (
    "  (posTransactions || []).forEach(function(p) {\n"
    "    if (!rowDataVisible(p)) return;\n"
    "    var d = dashTimestampDay(p.timestamp);\n"
    "    if (!d || d < from || d > to) return;\n"
    "    var s = dashShiftNameFromTimestamp(p.timestamp);\n"
    "    sums[s] = (sums[s] || 0) + (parseFloat(p.grandTotal) || 0);\n"
    "  });\n"
    "  (transactions || []).forEach(function(tx) {\n"
    "    if (!rowDataVisible(tx) || tx.source !== 'Vehicle Rental') return;\n"
    "    var d = dashTimestampDay(tx.timestamp);\n"
    "    if (!d || d < from || d > to) return;\n"
    "    var s = dashShiftNameFromTimestamp(tx.timestamp);\n"
    "    sums[s] = (sums[s] || 0) + (parseFloat(tx.grandTotal) || 0);\n"
    "  });\n"
    "  return sums;"
)

EXPORT_TABLES_OLD = "    {name:'work_periods.csv', data:workPeriods},\n  ];"
EXPORT_TABLES_NEW = (
    "    {name:'work_periods.csv', data:workPeriods},\n"
    "    {name:'vehicles.csv', data:vehicles},\n"
    "    {name:'vehicle_rentals.csv', data:vehicleRentals},\n"
    "    {name:'vehicle_expenses.csv', data:vehicleExpenses},\n"
    "    {name:'vehicle_maint_blocks.csv', data:vehicleMaintBlocks},\n"
    "  ];"
)

BACKUP_DATA_OLD = (
    "restaurantTables,storeItems,serviceRequests,transactions,workPeriods};"
)
BACKUP_DATA_NEW = (
    "restaurantTables,storeItems,serviceRequests,transactions,workPeriods,"
    "vehicles,vehicleRentals,vehicleExpenses,vehicleMaintBlocks,rentLocations};"
)

RESTORE_OLD = (
    "  r = takeArr('workPeriods'); if (r) { workPeriods = r; save('workPeriods', workPeriods); }\n"
    "  r = takeArr('auditLog');"
)
RESTORE_NEW = (
    "  r = takeArr('workPeriods'); if (r) { workPeriods = r; save('workPeriods', workPeriods); }\n"
    "  r = takeArr('vehicles'); if (r) { vehicles = r; save('vehicles', vehicles); }\n"
    "  r = takeArr('vehicleRentals'); if (r) { vehicleRentals = r; save('vehicleRentals', vehicleRentals); }\n"
    "  r = takeArr('vehicleExpenses'); if (r) { vehicleExpenses = r; save('vehicleExpenses', vehicleExpenses); }\n"
    "  r = takeArr('vehicleMaintBlocks'); if (r) { vehicleMaintBlocks = r; save('vehicleMaintBlocks', vehicleMaintBlocks); }\n"
    "  r = takeArr('rentLocations'); if (r) { rentLocations = r; save('rentLocations', rentLocations); }\n"
    "  r = takeArr('auditLog');"
)

ASSEMBLE_MAP_OLD = (
    "    'work_periods.csv': ['workPeriods', []]\n"
    "  };"
)
ASSEMBLE_MAP_NEW = (
    "    'work_periods.csv': ['workPeriods', []],\n"
    "    'vehicles.csv': ['vehicles', []],\n"
    "    'vehicle_rentals.csv': ['vehicleRentals', []],\n"
    "    'vehicle_expenses.csv': ['vehicleExpenses', []],\n"
    "    'vehicle_maint_blocks.csv': ['vehicleMaintBlocks', []]\n"
    "  };"
)

CSV_DEF_OLD = (
    "    { k: 'workPeriods', tr: 'settings.csvBtnWorkPeriods' },\n"
    "    { k: 'auditLog', tr: 'settings.csvBtnAudit' },"
)
CSV_DEF_NEW = (
    "    { k: 'workPeriods', tr: 'settings.csvBtnWorkPeriods' },\n"
    "    { k: 'vehicles', tr: 'settings.csvBtnVehicles' },\n"
    "    { k: 'vehicleRentals', tr: 'settings.csvBtnVehicleRentals' },\n"
    "    { k: 'vehicleExpenses', tr: 'settings.csvBtnVehicleExpenses' },\n"
    "    { k: 'auditLog', tr: 'settings.csvBtnAudit' },"
)

EXPORT_SINGLE_OLD = (
    "restaurantTables,serviceRequests,messages,workPeriods,auditLog,bookingLog,inventoryLog};"
)
EXPORT_SINGLE_NEW = (
    "restaurantTables,serviceRequests,messages,workPeriods,vehicles,vehicleRentals,"
    "vehicleExpenses,vehicleMaintBlocks,rentLocations,auditLog,bookingLog,inventoryLog};"
)

MODULE_RE = re.compile(
    r"function rentVehicleIcon\([^)]*\)[\s\S]*?\nfunction renderRestaurant\(\)",
    re.MULTILINE,
)


def _load_v1_fragments():
    frag_path = Path(__file__).resolve().parent / "_vehicle_rental_v1_fragments.py"
    spec = importlib.util.spec_from_file_location("_vehicle_rental_v1_fragments", frag_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Missing fragments: {frag_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_v2_boutique():
    frag_path = Path(__file__).resolve().parent / "_vehicle_rental_v2_boutique.py"
    spec = importlib.util.spec_from_file_location("_vehicle_rental_v2_boutique", frag_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Missing boutique fragments: {frag_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_v2_module() -> str:
    if not V2_MODULE.is_file():
        raise SystemExit(f"Missing {V2_MODULE}")
    return V2_MODULE.read_text(encoding="utf-8").strip()


def _replace(content: str, old: str, new: str, label: str) -> str:
    if old not in content:
        if new.split("\n", 1)[0] in content:
            return content
        raise SystemExit(f"Could not apply {label}")
    return content.replace(old, new, 1)


def patch(content: str) -> str:
    v1 = _load_v1_fragments()
    v2 = _load_v2_boutique()
    module_js = _load_v2_module()

    content = re.sub(r"<!-- HRMM-VEHICLE-RENTAL-v\d+ -->", f"<!-- {MARKER} -->", content)
    if MARKER not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )

    if "/* HRMM vehicle rental floor */" not in content:
        content = content.replace(
            "    /* HRMM guest QR restaurant order */",
            "    /* HRMM vehicle rental floor */" + v1.VEHICLE_CSS + "\n"
            "    /* HRMM guest QR restaurant order */",
            1,
        )

    if "/* HRMM vehicle rental boutique v2 */" not in content:
        content = content.replace(
            "    /* HRMM guest QR restaurant order */",
            "    /* HRMM vehicle rental boutique v2 */" + v2.VEHICLE_V2_CSS + "\n"
            "    /* HRMM guest QR restaurant order */",
            1,
        )

    if "let vehicles = load('vehicles'" not in content:
        content = content.replace(
            DATA_ANCHOR,
            v1.VEHICLE_DATA_INIT.strip() + "\n" + DATA_ANCHOR,
            1,
        )

    if "let vehicleExpenses = load('vehicleExpenses'" not in content:
        if VEHICLE_DATA_ANCHOR in content:
            content = content.replace(
                VEHICLE_DATA_ANCHOR,
                VEHICLE_DATA_ANCHOR + "\n" + v2.VEHICLE_V2_DATA.strip(),
                1,
            )
        else:
            content = content.replace(
                DATA_ANCHOR,
                v2.VEHICLE_V2_DATA.strip() + "\n" + DATA_ANCHOR,
                1,
            )

    if MODULE_RE.search(content):
        content = MODULE_RE.sub(lambda _m: module_js + "\n\nfunction renderRestaurant()", content, count=1)
    elif "function renderVehicleRental()" not in content:
        content = content.replace(
            "function renderRestaurant() {",
            module_js + "\n\nfunction renderRestaurant() {",
            1,
        )

    if 'data-page="vehiclerental"' not in content:
        content = _replace(content, NAV_ANCHOR, NAV_NEW, "sidebar nav")

    if 'id="page-vehiclerental"' not in content:
        content = _replace(content, PAGE_ANCHOR, PAGE_NEW, "page container")

    if "vehiclerental:renderVehicleRental" not in content:
        content = _replace(content, RENDER_PAGE_OLD, RENDER_PAGE_NEW, "renderPage map")

    if "vehiclerental:'Vehicle Rental'" not in content:
        content = _replace(content, PAGE_TITLES_OLD, PAGE_TITLES_NEW, "pageTitles")

    if "'vehiclerental'" not in content.split("applyRBAC")[1].split("};")[0]:
        if RBAC_MANAGER_OLD in content:
            content = content.replace(RBAC_MANAGER_OLD, RBAC_MANAGER_NEW, 1)
        if RBAC_RECEPTION_OLD in content:
            content = content.replace(RBAC_RECEPTION_OLD, RBAC_RECEPTION_NEW, 1)

    if "s.indexOf('vehicle')" not in content:
        content = _replace(content, NORMALIZE_OLD, NORMALIZE_NEW, "normalizeDeptKey")

    if "tx.source !== 'Vehicle Rental'" not in content.split("dashComputeRowForDay")[1][:800]:
        content = _replace(content, DASH_ROW_OLD, DASH_ROW_NEW, "dashComputeRowForDay")

    if "tx.source !== 'Vehicle Rental'" not in content.split("dashShiftSumsInRange")[1][:600]:
        content = _replace(content, DASH_SHIFT_OLD, DASH_SHIFT_NEW, "dashShiftSumsInRange")

    if "vehicles.csv" not in content:
        content = content.replace(EXPORT_TABLES_OLD, EXPORT_TABLES_NEW, 1)
        content = content.replace(BACKUP_DATA_OLD, BACKUP_DATA_NEW)
        if EXPORT_SINGLE_OLD in content:
            content = content.replace(EXPORT_SINGLE_OLD, EXPORT_SINGLE_NEW, 1)
        if RESTORE_OLD in content and "vehicleExpenses" not in content.split("restoreFromJson")[1][:1200]:
            content = _replace(content, RESTORE_OLD, RESTORE_NEW, "restoreFromJson")
        if ASSEMBLE_MAP_OLD in content:
            content = _replace(content, ASSEMBLE_MAP_OLD, ASSEMBLE_MAP_NEW, "assembleBackupFromZipEntries")
        if CSV_DEF_OLD in content and "vehicleExpenses" not in content:
            content = content.replace(CSV_DEF_OLD, CSV_DEF_NEW, 1)
    elif "vehicle_expenses.csv" not in content:
        content = content.replace(
            "    {name:'vehicle_rentals.csv', data:vehicleRentals},\n  ];",
            "    {name:'vehicle_rentals.csv', data:vehicleRentals},\n"
            "    {name:'vehicle_expenses.csv', data:vehicleExpenses},\n"
            "    {name:'vehicle_maint_blocks.csv', data:vehicleMaintBlocks},\n  ];",
            1,
        )

    return content


def main() -> int:
    index = ROOT / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — boutique vehicle rental v2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
