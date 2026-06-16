#!/usr/bin/env python3
"""Work periods (shifts): open by default (no auto-close)."""
from __future__ import annotations

import sys
import re
from pathlib import Path

MARKER = "HRMM-SHIFTS-v2"
INDEX = Path("public/index.html")

AUTO_OPEN_OLD = """if (!Array.isArray(workPeriods)) workPeriods = [];
if (workPeriods.length === 0) {
  workPeriods.push({ id: genId(), dept: 'Mini-Mart', startTime: new Date().toISOString(), endTime: null, openingCash: 0, closingCash: null, cashVariance: null, status: 'Open', userId: '', userName: '—', closedBy: '' });
  save('workPeriods', workPeriods);
}"""

AUTO_OPEN_NEW = """if (!Array.isArray(workPeriods)) workPeriods = [];
// Ensure initial sample shifts are OPEN by default.
if (workPeriods.length === 0) {
  var now = new Date().toISOString();
  var mk = function(dept, who) {
    return { id: genId(), dept: dept, startTime: now, endTime: null, openingCash: 0, closingCash: null, cashVariance: null, status: 'Open', userId: '', userName: who || '—', closedBy: '' };
  };
  workPeriods.push(mk('Restaurant', '—'));
  workPeriods.push(mk('Mini-Mart', '—'));
  workPeriods.push(mk('Hotel', '—'));
  workPeriods.push(mk('Vehicle Rental', '—'));
  save('workPeriods', workPeriods);
}"""


def _is_fully_patched(content: str) -> bool:
    return MARKER in content and "Vehicle Rental" in content and AUTO_OPEN_OLD not in content


def patch(content: str) -> str:
    if _is_fully_patched(content):
        print(f"Already patched {MARKER} — skipping")
        return content

    if AUTO_OPEN_OLD in content:
        content = content.replace(AUTO_OPEN_OLD, AUTO_OPEN_NEW, 1)
    else:
        # Upgrade from HRMM-SHIFTS-v1 (migrateShiftsClosedByDefault) to v2
        m = re.search(r"if\s*\(!Array\.isArray\(workPeriods\)\)\s*workPeriods\s*=\s*\[\];\n\(\s*function\s+migrateShiftsClosedByDefault\(\)[\s\S]*?\}\)\(\);\s*", content)
        if m:
            content = content[: m.start()] + AUTO_OPEN_NEW + content[m.end() :]
        else:
            raise SystemExit("Could not find workPeriods shift init block")

    content = re.sub(r"<!-- HRMM-SHIFTS-v\d+ -->", f"<!-- {MARKER} -->", content)
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
    print(f"Patched {index} — shifts open by default (no auto-close)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
