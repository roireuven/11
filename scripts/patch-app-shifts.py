#!/usr/bin/env python3
"""Work periods (shifts): closed by default until staff opens them."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "HRMM-SHIFTS-v1"
INDEX = Path("public/index.html")

AUTO_OPEN_OLD = """if (!Array.isArray(workPeriods)) workPeriods = [];
if (workPeriods.length === 0) {
  workPeriods.push({ id: genId(), dept: 'Mini-Mart', startTime: new Date().toISOString(), endTime: null, openingCash: 0, closingCash: null, cashVariance: null, status: 'Open', userId: '', userName: '—', closedBy: '' });
  save('workPeriods', workPeriods);
}"""

AUTO_OPEN_NEW = """if (!Array.isArray(workPeriods)) workPeriods = [];
(function migrateShiftsClosedByDefault() {
  var MK = DB_KEY + 'shiftsClosedByDefaultV1';
  try { if (String(localStorage.getItem(MK) || '') === '1') return; } catch (e) { return; }
  if (isAndroid) {
    try { if (String(HotelDB.getSetting('shiftsClosedByDefaultV1') || '') === '1') return; } catch (e) {}
  }
  if (!Array.isArray(workPeriods)) return;
  var changed = false;
  workPeriods.forEach(function(wp) {
    if (!wp || wp.status !== 'Open') return;
    var hasTx = Array.isArray(transactions) && transactions.some(function(tx) { return tx && tx.workPeriodId === wp.id; });
    if (hasTx) return;
    wp.status = 'Closed';
    wp.endTime = wp.endTime || new Date().toISOString();
    wp.closingCash = wp.closingCash != null ? wp.closingCash : (parseFloat(wp.openingCash) || 0);
    wp.cashVariance = wp.cashVariance != null ? wp.cashVariance : 0;
    wp.closedBy = wp.closedBy || 'System';
    changed = true;
  });
  if (changed) save('workPeriods', workPeriods);
  try { localStorage.setItem(MK, '1'); } catch (e) {}
  if (isAndroid) { try { HotelDB.saveSetting('shiftsClosedByDefaultV1', '1'); } catch (e) {} }
})();"""


def _is_fully_patched(content: str) -> bool:
    return MARKER in content and "migrateShiftsClosedByDefault" in content and AUTO_OPEN_OLD not in content


def patch(content: str) -> str:
    if _is_fully_patched(content):
        print(f"Already patched {MARKER} — skipping")
        return content

    if AUTO_OPEN_OLD not in content:
        if "migrateShiftsClosedByDefault" in content:
            print(f"Already patched {MARKER} — skipping")
            return content
        raise SystemExit("Could not find workPeriods auto-open block")

    content = content.replace(AUTO_OPEN_OLD, AUTO_OPEN_NEW, 1)

    if f"<!-- {MARKER} -->" not in content:
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
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — shifts closed by default until opened on dashboard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
