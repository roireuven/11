#!/usr/bin/env python3
"""Dashboard vehicle rental — fleet card, shift bar, backup/restore, day drill-down."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-DASHBOARD-RENTAL-v2"
INDEX = Path("public/index.html")

PMS_OPEN_RENTAL_BTN = (
    "'<button type=\"button\" class=\"btn btn-primary pms-mod-btn\" "
    "onclick=\"showPage(\\'vehiclerental\\')\">' + t('pms.btnOpenRental') + '</button>' +\n      "
)

PMS_BTN_ANCHOR = (
    "'<button type=\"button\" class=\"btn btn-primary pms-mod-btn\" "
    "onclick=\"if(window.showAddAccount)showAddAccount()\">+ ' + t('pms.btnAddUsr') + '</button>' +\n"
    "      '</div></div></div>';"
)
PMS_BTN_NEW = (
    "'<button type=\"button\" class=\"btn btn-primary pms-mod-btn\" "
    "onclick=\"if(window.showAddAccount)showAddAccount()\">+ ' + t('pms.btnAddUsr') + '</button>' +\n"
    "      '<button type=\"button\" class=\"btn btn-primary pms-mod-btn\" "
    "onclick=\"if(window.showAddVehicle)showAddVehicle()\">+ ' + t('pms.btnAddVehicle') + '</button>' +\n"
    "      '</div></div></div>';"
)

WPBAR_TITLE_OLD = (
    "    const title = dept === 'Restaurant' ? 'Restaurant shift' : "
    "(dept === 'Hotel' ? 'Hotel shift' : 'Mini‑mart shift');"
)
WPBAR_TITLE_NEW = (
    "    const title = dept === 'Restaurant' ? 'Restaurant shift' : "
    "(dept === 'Hotel' ? 'Hotel shift' : (dept === 'Vehicle Rental' ? 'Vehicle rental shift' : 'Mini‑mart shift'));"
)

WPBAR_OLD = (
    "  const wpBar = !isHK ? (_wpBarFor('Restaurant') + _wpBarFor('Mini-Mart') + _wpBarFor('Hotel')) : '';"
)
WPBAR_NEW = (
    "  const wpBar = !isHK ? (_wpBarFor('Restaurant') + _wpBarFor('Mini-Mart') + "
    "_wpBarFor('Hotel') + _wpBarFor('Vehicle Rental')) : '';"
)

NORMALIZE_RENTAL_HOTEL = (
    "  if (s.indexOf('vehicle') >= 0 || s.indexOf('rental') >= 0) return 'Hotel';\n"
)
NORMALIZE_RENTAL_DEPT = (
    "  if (s.indexOf('vehicle') >= 0 || s.indexOf('rental') >= 0) return 'Vehicle Rental';\n"
)

WP_REPORT_OLD = (
    "  var byPay = {}, bySource = { 'Restaurant': 0, 'Mini-Mart': 0, 'POS': 0, 'Service': 0, 'Other': 0 };"
)
WP_REPORT_NEW = (
    "  var byPay = {}, bySource = { 'Restaurant': 0, 'Mini-Mart': 0, 'POS': 0, 'Service': 0, "
    "'Vehicle Rental': 0, 'Other': 0 };"
)

DASH_CARD_ANCHOR = "    bodyHtml += wpBar;"
DASH_CARD_NEW = (
    "    bodyHtml += wpBar;\n"
    "    if (typeof rentRenderDashboardCardHtml === 'function') bodyHtml += rentRenderDashboardCardHtml();"
)

DAY_DETAIL_ANCHOR = (
    "  } else { html += '<p style=\"color:var(--text-light);font-size:0.85rem;\">—</p>'; }\n"
    "\n"
    "  html += '</div>';"
)
DAY_DETAIL_NEW = (
    "  } else { html += '<p style=\"color:var(--text-light);font-size:0.85rem;\">—</p>'; }\n"
    "\n"
    "  if (typeof rentRenderDayDetailSection === 'function') html += rentRenderDayDetailSection(dateStr);\n"
    "\n"
    "  html += '</div>';"
)

EXPORT_SINGLE_OLD = (
    "restaurantTables,serviceRequests,messages,workPeriods,vehicles,vehicleRentals,auditLog,bookingLog,inventoryLog};"
)
EXPORT_SINGLE_NEW = (
    "restaurantTables,serviceRequests,messages,workPeriods,vehicles,vehicleRentals,"
    "vehicleExpenses,vehicleMaintBlocks,rentLocations,auditLog,bookingLog,inventoryLog};"
)

BACKUP_ZIP_OLD = (
    "vehicles,vehicleRentals};\n"
    "  files.push({name:'settings.json'"
)
BACKUP_ZIP_NEW = (
    "vehicles,vehicleRentals,vehicleExpenses,vehicleMaintBlocks,rentLocations};\n"
    "  files.push({name:'settings.json'"
)

EXPORT_JSON_OLD = (
    "workPeriods,vehicles,vehicleRentals};\n"
    "  const json = JSON.stringify(data, null, 2);"
)
EXPORT_JSON_NEW = (
    "workPeriods,vehicles,vehicleRentals,vehicleExpenses,vehicleMaintBlocks,rentLocations};\n"
    "  const json = JSON.stringify(data, null, 2);"
)

RESTORE_ANCHOR = (
    "  r = takeArr('workPeriods'); if (r) { workPeriods = r; save('workPeriods', workPeriods); }\n"
    "  if (data.settings && typeof data.settings === 'object' && !Array.isArray(data.settings)) { settings = data.settings; save('settings',settings); }\n"
    "  r = takeArr('auditLog');"
)
RESTORE_NEW = (
    "  r = takeArr('workPeriods'); if (r) { workPeriods = r; save('workPeriods', workPeriods); }\n"
    "  r = takeArr('vehicles'); if (r) { vehicles = r; save('vehicles', vehicles); }\n"
    "  r = takeArr('vehicleRentals'); if (r) { vehicleRentals = r; save('vehicleRentals', vehicleRentals); }\n"
    "  r = takeArr('vehicleExpenses'); if (r) { vehicleExpenses = r; save('vehicleExpenses', vehicleExpenses); }\n"
    "  r = takeArr('vehicleMaintBlocks'); if (r) { vehicleMaintBlocks = r; save('vehicleMaintBlocks', vehicleMaintBlocks); }\n"
    "  r = takeArr('rentLocations'); if (r) { rentLocations = r; save('rentLocations', rentLocations); }\n"
    "  if (data.settings && typeof data.settings === 'object' && !Array.isArray(data.settings)) { settings = data.settings; save('settings',settings); }\n"
    "  r = takeArr('auditLog');"
)

ASSEMBLE_OLD = (
    "    'vehicle_rentals.csv': ['vehicleRentals', []]\n"
    "  };"
)
ASSEMBLE_NEW = (
    "    'vehicle_rentals.csv': ['vehicleRentals', []],\n"
    "    'vehicle_expenses.csv': ['vehicleExpenses', []],\n"
    "    'vehicle_maint_blocks.csv': ['vehicleMaintBlocks', []]\n"
    "  };"
)


def _replace(content: str, old: str, new: str, label: str) -> str:
    if old not in content:
        if new.split("\n", 1)[0] in content:
            return content
        raise SystemExit(f"Could not apply {label}")
    return content.replace(old, new, 1)


def patch(content: str) -> str:
    content = re.sub(r"HRMM-DASHBOARD-RENTAL-v\d+", MARKER, content)
    if MARKER not in content:
        content = content.replace("</head>", f"  <!-- {MARKER} -->\n</head>", 1)

    if PMS_OPEN_RENTAL_BTN in content:
        content = content.replace(PMS_OPEN_RENTAL_BTN, "", 1)

    if "pms.btnAddVehicle" not in content and PMS_BTN_ANCHOR in content:
        content = _replace(content, PMS_BTN_ANCHOR, PMS_BTN_NEW, "PMS add vehicle button")

    if "_wpBarFor('Vehicle Rental')" not in content:
        if WPBAR_TITLE_OLD in content:
            content = content.replace(WPBAR_TITLE_OLD, WPBAR_TITLE_NEW, 1)
        if WPBAR_OLD in content:
            content = content.replace(WPBAR_OLD, WPBAR_NEW, 1)

    if NORMALIZE_RENTAL_HOTEL in content:
        content = content.replace(NORMALIZE_RENTAL_HOTEL, NORMALIZE_RENTAL_DEPT, 1)
    elif "return 'Vehicle Rental';" not in content.split("normalizeDeptKey")[1][:400]:
        pass  # vehicle-rental patch handles fresh installs

    if "'Vehicle Rental': 0" not in content.split("workPeriodBuildReport")[1][:300]:
        if WP_REPORT_OLD in content:
            content = content.replace(WP_REPORT_OLD, WP_REPORT_NEW, 1)

    if "rentRenderDashboardCardHtml" not in content.split("renderDashboard")[1][:2500]:
        content = _replace(content, DASH_CARD_ANCHOR, DASH_CARD_NEW, "dashboard fleet card")

    if "rentRenderDayDetailSection" not in content:
        content = _replace(content, DAY_DETAIL_ANCHOR, DAY_DETAIL_NEW, "showDayDetail rentals")

    if "vehicleExpenses,vehicleMaintBlocks,rentLocations,auditLog" not in content:
        if EXPORT_SINGLE_OLD in content:
            content = content.replace(EXPORT_SINGLE_OLD, EXPORT_SINGLE_NEW, 1)
        if BACKUP_ZIP_OLD in content:
            content = content.replace(BACKUP_ZIP_OLD, BACKUP_ZIP_NEW, 1)
        if EXPORT_JSON_OLD in content:
            content = content.replace(EXPORT_JSON_OLD, EXPORT_JSON_NEW, 1)

    if "takeArr('vehicleExpenses')" not in content:
        content = _replace(content, RESTORE_ANCHOR, RESTORE_NEW, "restoreFromJson fleet")

    if "'vehicle_expenses.csv': ['vehicleExpenses'" not in content:
        content = _replace(content, ASSEMBLE_OLD, ASSEMBLE_NEW, "assembleBackupFromZipEntries")

    return content


def main() -> int:
    if not INDEX.is_file():
        print(f"Missing {INDEX}", file=sys.stderr)
        return 1
    text = INDEX.read_text(encoding="utf-8")
    patched = patch(text)
    INDEX.write_text(patched, encoding="utf-8")
    print(f"Patched {INDEX} ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
