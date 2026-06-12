# HotelRestaurantMini-MartManagement — Documentation

Complete documentation for **HotelRestaurantMini-MartManagement** (**v2.4** — current production), an all-in-one property management system for **hotel**, **restaurant**, **mini-mart**, **POS**, and **vehicle rental** — including **guest QR self-order**, **QR Orders Report**, and **21-language** staff UI.

> **Browse online (Firebase):** [https://hotel-restaurant-minimart2-4.web.app/doc/](https://hotel-restaurant-minimart2-4.web.app/doc/)  
> **Inside the app:** Sidebar → **Help → Documentation** (all roles) — embedded help  
> **Mirror (GitHub Pages):** [https://roireuven.github.io/11/doc/](https://roireuven.github.io/11/doc/)

## Live application

| Platform | URL |
|----------|-----|
| **Web — stable v2.4 (production)** | [https://hotel-restaurant-minimart2-4.web.app/](https://hotel-restaurant-minimart2-4.web.app/) |
| **Alternate domain** | [https://hotel-restaurant-minimart2-4.firebaseapp.com/](https://hotel-restaurant-minimart2-4.firebaseapp.com/) |
| **Stable v2.3 (legacy snapshot)** | [https://hotel-restaurant-minimart2-3.web.app/](https://hotel-restaurant-minimart2-3.web.app/) |
| **Development (manual deploy only)** | [https://hotel-restaurant-minimart.web.app/](https://hotel-restaurant-minimart.web.app/) |
| **Android APK (related)** | [Hotel Manager landing page](https://roireuven.github.io/11/) |

Routine releases deploy to **v2.4 only** (`npm run deploy`). See [Deployment](deployment.md).

## Documentation index

### Getting started

| Document | Description |
|----------|-------------|
| [What's new in v2.4](whats-new-v2.md) | Current release: vehicle rental, mobile UI, 21 languages |
| [Overview](overview.md) | What the system is, who it is for, key capabilities |
| [Getting started](getting-started.md) | Quick start for owners and staff |
| [Visual guide (screenshots)](visual-guide.md) | Illustrated UI tour with screenshots |
| [Installation](installation.md) | Web, Android, and local development |
| [First-time setup](first-time-setup.md) | Create your system account and initial configuration |
| [Demo credentials](demo-credentials.md) | Built-in demo users for testing |

### Using the system

| Document | Description |
|----------|-------------|
| [User roles & permissions](user-roles-and-permissions.md) | Admin, Manager, Reception, Housekeeper, Restaurant, Kitchen |
| [Navigation & UI](navigation-and-ui.md) | Sidebar, mobile bottom nav, double-height bars, languages |
| [Hotel operations](hotel-operations.md) | Rooms, bookings, guests, housekeeping, maintenance |
| [Services & billing](services-and-billing.md) | Guest services, invoices, check-in/out |
| [Restaurant & kitchen](restaurant-and-kitchen.md) | Orders, tables, room service, kitchen queue |
| [Mini-mart & POS](minimart-and-pos.md) | Shop sales, room charges, till |
| [Vehicle rental](vehicle-rental.md) | Cars & motorbikes — fleet floor, checkout, return, reports |
| [Guest QR orders](guest-qr-orders.md) | Scan-to-order, order # 1–60, QR report, 21-language guest UI |
| [Inventory & catalog](inventory-and-catalog.md) | Stock, menu items, store items |
| [Guest portal](guest-portal.md) | Guest-facing features |
| [Reports](reports.md) | Sales, occupancy, and operational reports |
| [Accounts & audit](accounts-and-audit.md) | Users, messages, audit trail |

### Administration

| Document | Description |
|----------|-------------|
| [Settings & configuration](settings-and-configuration.md) | Hotel profile, taxes, seasons, dropdown lists |
| [Backup, restore & data](backup-restore-and-data.md) | Export/import, storage backends, factory reset |
| [Localization](localization.md) | Supported languages and RTL |
| [Data model](data-model.md) | Tables, entities, and change logs |

### Technical

| Document | Description |
|----------|-------------|
| [Architecture](architecture.md) | SPA design, storage, sync model |
| [Deployment](deployment.md) | Firebase Hosting — v2.4 production deploy |
| [Development](development.md) | Local dev environment and sync from production |
| [Troubleshooting & FAQ](troubleshooting-faq.md) | Common issues and fixes |
| [Glossary](glossary.md) | Terms used in the app |

## Version

- **App version:** **v2.4** (stable production)
- **Production URL:** `hotel-restaurant-minimart2-4.web.app`
- **Deploy policy:** `npm run deploy` uploads to **v2.4 only**
- **Documentation:** 31 English guides, 21 locales (Docsify site at `/doc/`)

## Support workflow

1. Read [Getting started](getting-started.md) and [First-time setup](first-time-setup.md).
2. Assign roles using [User roles & permissions](user-roles-and-permissions.md).
3. Configure the property in [Settings & configuration](settings-and-configuration.md).
4. Train staff using the module guides (hotel, restaurant, mini-mart, vehicle rental).
5. Set up [Backup, restore & data](backup-restore-and-data.md) before going live.
