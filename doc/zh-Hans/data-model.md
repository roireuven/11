# Data model

Logical data entities used by HotelRestaurantMini-MartManagement. Stored as JSON in `localStorage` (web) or SQLite tables (Android) with equivalent names.

## Core hotel

### Rooms
Room number, floor, type, bed config, max guests, price/night, amenities, housekeeping status, occupancy status, maintenance logs.

### Guests
Name, passport, nationality, contact, DOB, notes, VIP/frequent/blacklist flags, visit count.

### Bookings
Guest link, room, check-in/out dates and times, arrival status, booking source, status, linked invoice IDs.

### Services
Catalog of chargeable services (category, price, description).

### Invoices
Line items, taxes, payments, status, links to booking/guest.

## Operations

### Tickets
Maintenance/housekeeping issues: room, description, priority, status.

### Service requests
Guest/room service requests from portal or front desk.

### Messages
Staff/guest message log with type and channel.

## F&B and retail

### Menu items
Restaurant dishes: name, category, price, image, inventory link.

### Store items
Mini-mart SKUs: name, category, price, barcode, stock.

### Inventory
Stock items shared across F&B and retail.

### Restaurant orders
Order header: type (table/room), table label, guest link, status, lines, kitchen state.

### Restaurant tables
Table floor configuration and labels.

### Mini-mart open bills
Unpaid guest room charges from shop.

### POS open bills
Unpaid walk-in POS tabs (Inventory POS).

## Financial

### POS transactions
Till sales, items, payment method.

### All transactions
Unified ledger: POS + restaurant + mini-mart + room service charges.

### Work periods
Shift open/close for cash reporting.

## Administration

### Accounts
User id, name, email, role, status.

### Settings
Key/value store for hotel config, setup flags, dark mode, locale.

### Audit
System-wide audit entries.

## Setup keys (per namespace)

| Key | Purpose |
|-----|---------|
| `setupDone` | First-time setup complete |
| `setupEmail` | System admin email |
| `setupPassword` | Login password |
| `setupVersion` | Setup schema version |
| `hotel_mgr_dataNamespace` | Isolation prefix |
| `appDataEpoch` | Data migration epoch |
| `currentUser` | Active session |

## Change logs

Each major module maintains an append-only **change log** in UI for operational audit (separate from central Audit table).

## ID generation

Entities use generated IDs (`hotelGenIdEarly()` and related helpers) for cross-table references.

## Related

- [Backup, restore & data](backup-restore-and-data.md)
- [Architecture](architecture.md)
