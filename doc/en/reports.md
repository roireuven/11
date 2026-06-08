# Reports

**Path:** Sidebar → **Reports**

Available to **Admin** and **Manager**. **Manager** lands on Reports by default after login.

---

## Dashboard vs Reports module

| View | Who | Content |
|------|-----|---------|
| **Dashboard** | Roles with dashboard access | Live KPIs, shift status, date-filtered charts |
| **Reports** | Admin, Manager | Department sales, occupancy trends, shift summaries |

![Dashboard analytics and shift panels](assets/screenshots/02-dashboard.png)

---

## Dashboard analytics (all roles with access)

Open **Dashboard** from the sidebar or bottom nav.

### Date filtering

| Control | Effect |
|---------|--------|
| **From Date / To Date** | Custom range for charts and tables |
| **LAST 30 DAYS** | Quick preset |

### Metrics typically shown

- **Shift status** — Restaurant, Mini-Mart, Hotel (open/closed)
- **Room availability vs occupied**
- **Bookings** count for selected range
- **Invoices** summary
- **Daily overview** table

> Room charges use **calendar day** logic; F&B and mini-mart sales use **timestamps** (see Dashboard help text in app).

---

## Reports module (Manager focus)

### Sales by department

| Department | Includes |
|------------|----------|
| **Hotel (PMS)** | Room revenue, services on folio |
| **Restaurant** | Dine-in, room service, table orders |
| **Mini-Mart** | Shop sales, walk-in and room charges |
| **POS** | Aggregated till activity where applicable |

Use Reports for **end-of-day** and **period** reviews.

### QR Orders Report (Restaurant & Mini-Mart)

Separate from the sidebar **Reports** module — opened from **Restaurant** or **Mini-Mart** screens:

| Feature | Description |
|---------|-------------|
| **QR Orders Report** button | On New Order card and Active Orders toolbar |
| Summary | QR order count, slots used (of 60), open orders, revenue |
| Charts | Status donut, revenue by order #, orders by hour |
| Slot board | Visual grid of order numbers **1–60** |
| Spreadsheet | Filterable XGrid of all QR scan orders |
| **Export Excel (CSV)** | Download for Excel or Google Sheets |

See [Guest QR orders](guest-qr-orders.md).

### Occupancy and revenue

- Occupancy trends over selected dates
- Revenue comparison by department
- Manager sign-off workflows (property-specific process)

---

## Work periods (shifts)

POS and F&B **work periods** tie transactions to an open shift:

| Concept | Use |
|---------|-----|
| **Open shift** | Start of cashier/restaurant/hotel shift on Dashboard |
| **Close shift** | End shift — enables variance review |
| **Cash variance** | Compare expected vs actual cash |
| **Shift-bound summaries** | Transactions tagged to active period |

Exported in backup as **`Work periods`** table.

### Shift workflow (recommended)

1. **OPEN SHIFT** on Dashboard for each department at start of day.
2. Run operations (POS, restaurant, bookings).
3. **CLOSE SHIFT** at handover.
4. Manager reviews Reports + exported CSV if needed.

---

## Export for Excel / BI

| Method | Output |
|--------|--------|
| **Settings → Export all data (CSV ZIP)** | Full database snapshot |
| **Per-table CSV buttons** | Single table (bookings, transactions, restaurant, etc.) |

Import ZIP into Excel, Google Sheets, or Power BI for custom charts.

---

## Role summary

| Role | Dashboard | Reports |
|------|:---------:|:-------:|
| Admin | ✓ | ✓ |
| Manager | ✓ | ✓ (default landing) |
| Reception | ✓ | — |
| Others | If in RBAC list | — |

See [User roles & permissions](user-roles-and-permissions.md).

---

## Related

- [Settings & configuration](settings-and-configuration.md)
- [Backup, restore & data](backup-restore-and-data.md)
- [Mini-mart & POS](minimart-and-pos.md)
- [Restaurant & kitchen](restaurant-and-kitchen.md)
- [Visual guide](visual-guide.md)
