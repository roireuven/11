#!/usr/bin/env node
/** Static check: export keys match restore keys for full backup round-trip. */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const INDEX = join(ROOT, "public/index.html");

const REQUIRED_EXPORT_KEYS = [
  "rooms", "guests", "bookings", "bookingLog", "services", "invoices", "accounts",
  "auditLog", "settings", "tickets", "messages", "inventory", "inventoryLog",
  "posTransactions", "menuItems", "restaurantOrders", "martOpenOrders", "posOpenOrders",
  "restaurantTables", "storeItems", "serviceRequests", "transactions", "workPeriods",
  "vehicles", "vehicleRentals", "vehicleExpenses", "vehicleMaintBlocks", "rentLocations",
];

const REQUIRED_CSV_FILES = [
  "rooms.csv", "guests.csv", "bookings.csv", "services.csv", "invoices.csv",
  "accounts.csv", "inventory.csv", "tickets.csv", "messages.csv", "audit_log.csv",
  "booking_log.csv", "inventory_log.csv", "pos_transactions.csv", "menu_items.csv",
  "restaurant_orders.csv", "mart_open_orders.csv", "pos_open_orders.csv",
  "restaurant_tables.csv", "store_items.csv", "service_requests.csv",
  "transactions.csv", "work_periods.csv", "vehicles.csv", "vehicle_rentals.csv",
  "vehicle_expenses.csv", "vehicle_maint_blocks.csv", "rent_locations.csv",
  "settings.json", "_backup.json",
];

function fail(msg) {
  console.error("verify-backup-roundtrip:", msg);
  process.exit(1);
}

const html = readFileSync(INDEX, "utf8");

const exportJsonMatch = html.match(/window\.exportAllData = function\(\) \{([\s\S]*?)\n\};/);
const exportCsvMatch = html.match(/window\.exportAllCSV = function\(\) \{([\s\S]*?)\n\};/);
const restoreMatch = html.match(/function restoreFromJson\(data\) \{([\s\S]*?)\n\}/);
const assembleMatch = html.match(/function assembleBackupFromZipEntries\(entries\) \{([\s\S]*?)\n\}/);

const exportJsonChunk = exportJsonMatch?.[1] || "";
const exportCsvChunk = exportCsvMatch?.[1] || "";
const restoreChunk = restoreMatch?.[1] || "";
const assembleChunk = assembleMatch?.[1] || "";

if (!exportJsonChunk) fail("missing exportAllData()");
if (!exportCsvChunk) fail("missing exportAllCSV()");
if (!restoreChunk) fail("missing restoreFromJson()");

for (const key of REQUIRED_EXPORT_KEYS) {
  if (!exportJsonChunk.includes(key)) {
    fail(`exportAllData() missing key: ${key}`);
  }
  if (key !== "settings" && !restoreChunk.includes(`takeArr('${key}')`)) {
    fail(`restoreFromJson() missing takeArr('${key}')`);
  }
}

for (const file of REQUIRED_CSV_FILES) {
  if (!exportCsvChunk.includes(file)) {
    fail(`exportAllCSV() missing file: ${file}`);
  }
}

if (!assembleChunk.includes("'rent_locations.csv': ['rentLocations'")) {
  fail("assembleBackupFromZipEntries missing rent_locations.csv");
}

if (!html.includes('id="loginFormExtra"')) {
  fail("login form missing #loginFormExtra for license key on /paid");
}

if (!html.includes("hrmmLoginLicenseGate")) {
  fail("missing hrmmLoginLicenseGate for trial/license check");
}

const guardCount = (html.match(/HRMM-LICENSE-GUARD-v1/g) || []).length;
if (guardCount !== 1) {
  fail(`expected exactly 1 license guard, found ${guardCount}`);
}

console.log("verify-backup-roundtrip: OK (export/restore keys aligned)");
