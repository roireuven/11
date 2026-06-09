# Settings & configuration

**Path:** Sidebar → **Settings** — **Admin only**

![Settings — property name, currency, taxes, seasons](assets/screenshots/11-settings.png)

## Hotel settings

| Setting | Description |
|---------|-------------|
| Hotel name | Property name on invoices and UI |
| Contact email / phone | Display and correspondence |
| Address | Property address |
| Currency | Reporting currency (see LAK hint for Laos) |
| Default tax rate (%) | Applied to invoices |
| Service tax (%) | F&B / service charge |
| Check-in / check-out time | Default times for bookings |
| Max guests per room | Capacity rule |
| Surcharge rate (%) | Extra fees |

### Seasonal pricing

| Field | Description |
|-------|-------------|
| Peak season multiplier | Rate multiplier |
| Off season multiplier | Rate multiplier |
| Peak season start / end | Date range |

Click **Save settings** after changes.

## App language

**Interface language** — same as top-bar locale control. Applies to menus and labels app-wide (including guest QR modal, guest self-order screens, and QR Orders Report in all **21 locales**).

For Lao operations, Settings may suggest **Use LAK for hotel currency** when interface is Lao.

## Invoice payment QR (Settings)

Under **Settings → Hotel settings**:

| Option | Purpose |
|--------|---------|
| Invoice logo / picture | Shown at top of printed and on-screen invoices |
| Payment QR text or URL | Bank payment link or QR payload |
| Payment QR image (Browse) | Upload bank QR image |
| Include invoice number & total in payment QR | Adds INV/TOTAL to payment payload |

**Invoices do not include guest-order QRs.** Restaurant and mini-mart self-order links are on the bottom nav (**Restaurant QR**, **Mini-Mart QR**). See [Guest QR orders](guest-qr-orders.md).

## Regulations

Free-text or structured **regulations** field for property policies (display/reference).

## System configuration

Additional key/value **system configuration** stored with settings.

## Room rates and pricing

Dedicated section for rate tables linked to room types and seasons.

## Dropdown lists

**Path:** Sidebar → **Dropdown Lists** (Admin) — or configure lists referenced by Settings

Editable lists include:

- Room types, bed configurations
- Currencies and currency labels
- Booking sources, arrival statuses
- Payment methods / payment types
- Service categories, invoice statuses
- Ticket priorities / statuses
- Inventory, menu, store categories
- Order statuses, user roles
- Housekeeping / occupancy statuses
- Cancellation policies
- Message types / channels
- Transaction statuses

Use **Manage {label}** editor: add, edit, remove values, then Save.

## Danger zone

See [Backup, restore & data](backup-restore-and-data.md) for:

- Clear all data
- Factory reset
- Full wipe and new setup

## Related

- [Guest QR orders](guest-qr-orders.md)
- [Localization](localization.md)
- [Backup, restore & data](backup-restore-and-data.md)
- [Data model](data-model.md)
