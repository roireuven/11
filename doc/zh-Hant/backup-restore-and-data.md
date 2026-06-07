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
| POS | Till transactions |
| Menu | Restaurant menu and recipes |
| Restaurant | Orders, tables, kitchen status |
| Mini-mart open bills | Unpaid room charges |
| Restaurant tables | Table floor labels |
| Store | Mini-mart items, stock, barcodes |
| Service requests | Guest/room service requests |
| Transactions | All POS, restaurant, mini-mart, room charges |
| Work periods | POS/F&B shifts |
| Settings | Hotel and system key/value config |
| Audit | Compliance change history |

## Export

### Export all data (CSV ZIP)

Full archive: CSV files per table **plus** JSON backup for restore.

### Per-table CSV

Buttons for individual exports: Rooms, Guests, Bookings, Services, Invoices, Inventory, Menu, Store, Tickets, Accounts, Transactions, POS, Restaurant, Mini-mart open bills, Restaurant tables, Service requests, Messages, Work periods.

## Import

**Import data (ZIP or JSON)** — restore from prior export.

Always export before importing on a live system.

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

1. **Export all data** on source browser
2. Transfer ZIP/JSON file securely
3. **Import** on target browser (same or new setup)

## Android notes

SQLite file remains on device until app data cleared or uninstalled. Use export before device replacement.

## Data namespace

Each setup uses a prefix derived from the system email (`hotel_mgr_dataNamespace`). Multiple properties on one browser require separate setups or separate browsers/profiles.

## Related

- [First-time setup](first-time-setup.md)
- [Architecture](architecture.md)
- [Troubleshooting & FAQ](troubleshooting-faq.md)
