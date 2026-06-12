#!/usr/bin/env python3
"""Generate vehicle-rental i18n keys for all 21 locales."""
from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "doc" / "i18n" / "vehicle-rental-keys.json"
LOCALES = [
    "ar", "de", "en", "es", "fr", "he", "hi", "id", "it", "ja", "ko", "lo",
    "nl", "pl", "pt-BR", "ru", "th", "tr", "vi", "zh-Hans", "zh-Hant",
]
TARGETS = {
    "ar": "ar", "de": "de", "es": "es", "fr": "fr", "he": "iw", "hi": "hi",
    "id": "id", "it": "it", "ja": "ja", "ko": "ko", "lo": "lo", "nl": "nl",
    "pl": "pl", "pt-BR": "pt", "ru": "ru", "th": "th", "tr": "tr", "vi": "vi",
    "zh-Hans": "zh-CN", "zh-Hant": "zh-TW",
}


def main() -> int:
    from deep_translator import GoogleTranslator

    en = {
        "nav.vehiclerental": "Vehicle Rental",
        "pageTitle.vehiclerental": "Vehicle Rental",
        "rental.addVehicle": "Add vehicle",
        "rental.addVehicleTitle": "Add vehicle",
        "rental.type": "Type",
        "rental.plate": "Plate number",
        "rental.brand": "Brand",
        "rental.model": "Model",
        "rental.dailyRate": "Daily rate ($)",
        "rental.hourlyRate": "Hourly rate ($)",
        "rental.perDay": "day",
        "rental.checkoutTitle": "Check out vehicle",
        "rental.returnTitle": "Return vehicle",
        "rental.checkoutBtn": "Check out",
        "rental.returnBtn": "Return",
        "rental.startDate": "Start",
        "rental.endDate": "Due back",
        "rental.returnDate": "Actual return",
        "rental.fuelOut": "Fuel out",
        "rental.fuelIn": "Fuel in",
        "rental.mileageOut": "Mileage out",
        "rental.mileageIn": "Mileage in",
        "rental.bookingRef": "Booking ref",
        "rental.phGuest": "Guest name",
        "rental.payPending": "Pending",
        "rental.payRoom": "Charge to room",
        "rental.payPaid": "Paid",
        "rental.stAvailable": "Available",
        "rental.stOut": "Out",
        "rental.stDue": "Due / unpaid",
        "rental.stMaint": "Maintenance",
        "rental.linkBooking": "In-house booking",
        "rental.linkGuest": "Guest directory",
        "rental.pickBooking": "Select booking…",
        "rental.pickGuest": "Select guest…",
        "rental.floorHint": "Tap a tile to check out or return. Green = available, red = out, amber = due or payment pending.",
        "rental.noVehicles": "No vehicles in fleet. Add a car or motorbike.",
        "rental.activeRentals": "Active rentals",
        "rental.reportTitle": "Rental history & revenue",
        "rental.rentalNum": "Rental #",
        "rental.vehicle": "Vehicle",
        "rental.noActive": "No active rentals",
        "rental.noHistory": "No rental history yet",
        "rental.needGuest": "Enter guest name",
        "rental.needPlate": "Enter plate number",
        "rental.inMaintenance": "Vehicle is in maintenance",
        "rental.checkedOut": "Rental {num} checked out",
        "rental.returned": "Rental {num} returned",
        "rental.vehicleAdded": "Vehicle added to fleet",
        "settings.csvBtnVehicles": "Vehicles",
        "settings.csvBtnVehicleRentals": "Vehicle rentals",
    }
    data: dict = {"en": en}
    for code in LOCALES:
        if code == "en":
            continue
        block = {}
        tgt = TARGETS.get(code, code)
        tr = GoogleTranslator(source="en", target=tgt)
        for k, v in en.items():
            for attempt in range(4):
                try:
                    block[k] = tr.translate(v)
                    break
                except Exception:
                    time.sleep(1.2 * (attempt + 1))
            else:
                block[k] = v
            time.sleep(0.05)
        data[code] = block
        print(f"Translated {code}")
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
