# Backup, restore & data

**Path:** Settings → **Backup and restore** / **Storage overview**

## Storage backends

| Platform | Backend | Description |
|----------|---------|-------------|
| **Web** | Browser `localStorage` | Data stays in **this browser only** — not synced to other devices |
| **Android** | SQLite `hotel_manager.db` | Persists on device across app restarts |

Settings shows row counts per table in **Storage overview**.

## Data tables

| Table | Contents |
|-------|----------|
| Rooms | Room list, type, floor, price, status |
| Guests | Guest directory and history |
| Bookings | Reservations and stay details |
| Services | Service catalog and pricing |
| Invoices | Invoices, taxes, payments |
| Accounts | Users, roles, sign-in |
| Tickets | Maintenance / housekeeping tickets |
| Messages | Message log |
| Inventory | F&B, mini-mart, hotel supplies |
| POS transactions | Till sales (completed) |
| POS open bills | Unpaid POS tabs |
| Menu | Restaurant menu and recipes |
| Restaurant orders | Orders, tables, kitchen status |
| Mini-mart open bills | Unpaid room charges |
| Restaurant tables | Table floor labels |
| Store | Mini-mart items, stock, barcodes |
| Service requests | Guest/room service requests |
| Transactions | All POS, restaurant, mini-mart, room charges |
| Work periods | POS/F&B shifts |
| Settings | Hotel and system key/value config |
| Audit log | Compliance change history |
| Booking log | Booking module change log |
| Inventory log | Inventory module change log |

## Export

### Export all data (CSV ZIP)

Downloads a ZIP archive with **every table**, including empty ones:

| File | Contents |
|------|----------|
| `rooms.csv` … `work_periods.csv` | One CSV per business table (nested arrays stored as JSON strings in cells) |
| `messages.csv` | Message log |
| `audit_log.csv`, `booking_log.csv`, `inventory_log.csv` | Change logs |
| `pos_open_orders.csv` | Open POS bills |
| `settings.json` | Full settings object |
| `_backup.json` | Complete JSON snapshot used for restore |

**Accounts CSV:** passwords are omitted from CSV for security; `_backup.json` retains full account records from the export moment.

### Export all data (JSON)

Separate button downloads `hotel_backup_YYYY-MM-DD.json` — same payload as `_backup.json` inside the ZIP. Use for quick restore or scripted backups.

### Per-table CSV

Buttons export one table at a time: Rooms, Guests, Bookings, Services, Invoices, Inventory, Menu, Store, Tickets, Accounts, Transactions, POS, Restaurant, Mini-mart open bills, **POS open bills**, Restaurant tables, Service requests, Messages, Work periods, **Audit log**, **Booking log**, **Inventory log**.

## Import

**Import data (ZIP or JSON)** — restores from a prior export.

| File type | Behavior |
|-----------|----------|
| **JSON** | Full restore via `exportAllData()` or `_backup.json` |
| **ZIP** | Prefers `_backup.json`; if missing, rebuilds from CSV files + `settings.json` in the archive |

Import shows a **confirmation** prompt — export before importing on a live system.

Import replaces matching arrays and settings in the current browser namespace; it does **not** change setup email/password unless you import an embedded-sample bundle separately.

## Reload demo sample

| Option | Effect |
|--------|--------|
| **Reload built-in demo sample** | Clears saved data and loads bundled demo (rooms, bookings, restaurant, POS, mini-mart) |
| **Reload sample data (keep menu & store products)** | Softer reset preserving catalog |

Same impact as factory reset for operational data — **back up first**.

## Danger zone actions

| Action | Effect |
|--------|--------|
| **Clear all data** | Removes business records |
| **Factory reset** | Wipe operational data |
| **Full wipe and new setup** | Deletes **all** data **and** system email/password — returns to first-time setup |

Full wipe requires **two confirmations**.

## Moving data between devices (web)

Web localStorage does not auto-sync. To move property data:

1. **Export all data** (ZIP or JSON) on source browser
2. Transfer file securely
3. **Import** on target browser (same or new setup)

## Android notes

SQLite file remains on device until app data cleared or uninstalled. Use export before device replacement.

## Data namespace

Each setup uses a prefix derived from the system email (`hotel_mgr_dataNamespace`). Multiple properties on one browser require separate setups or separate browsers/profiles.

## Related

- [First-time setup](first-time-setup.md)
- [Architecture](architecture.md)
- [Troubleshooting & FAQ](troubleshooting-faq.md)
