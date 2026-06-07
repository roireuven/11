# Glossary

| Term | Definition |
|------|------------|
| **PMS** | Property Management System — hotel rooms and bookings |
| **F&B** | Food and beverage — restaurant and kitchen operations |
| **POS** | Point of sale — cash/card till transactions |
| **Mini-mart** | On-site retail shop module |
| **Folio** | Guest bill combining room, restaurant, and shop charges |
| **Room charge** | Posting F&B or shop sale to guest room instead of immediate payment |
| **Put bill on customer** | Mini-mart action to add unpaid charges to guest active orders |
| **Kitchen queue** | Live list of orders at New / Preparing / Ready status |
| **Table floor** | Restaurant grid showing table free/busy/pay-due state |
| **Housekeeping board** | Room cleaning status workflow UI |
| **OOS** | Out of service — room not available for sale |
| **RBAC** | Role-based access control — menu visibility by staff role |
| **Data namespace** | Storage key prefix isolating one property setup from another |
| **Work period** | POS/F&B shift window for cash reporting |
| **Factory reset** | Wipe operational data while keeping or removing setup depending on option |
| **Setup email** | Primary admin email created at first-time setup |
| **Demo credentials** | Built-in test accounts (`*@hotel.com` / `1234`) |
| **SPA** | Single-page application — one HTML file drives all screens |
| **Firebase Hosting** | Static file CDN for the web app (not cloud database) |
| **HotelDB** | Android SQLite bridge API for persistent storage |
| **Locale** | Language code (e.g. `en`, `lo`, `zh-Hans`) for UI strings |
| **RTL** | Right-to-left layout for Arabic and Hebrew |
| **Audit log** | Record of system changes for compliance |
| **Change log** | Per-module edit history in the UI |
| **Dropdown lists** | Admin-configurable enums (room types, payment methods, etc.) |
| **LAK** | Lao kip — currency code (₭) |
| **Check-in / Check-out** | Guest arrival and departure processing with room status updates |

## Abbreviations in reports

| Abbrev | Meaning |
|--------|---------|
| PMS | Hotel department sales in combined reports |
| POS | Point-of-sale till totals |
| F&B | Food and beverage revenue |

## Role names

| UI label | Internal code |
|----------|---------------|
| Reception | `Receptionist` |
| All others | Same as UI (Admin, Manager, etc.) |
