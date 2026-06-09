# Accounts & audit

Staff access control, messaging, and compliance logging — **Admin** modules.

**Paths:** Sidebar → **Accounts** · **Messages** · **Audit Log**

---

## Accounts (user management)

**Path:** Sidebar → **Accounts** — **Admin only**

![Accounts — create staff logins and roles](../en/assets/screenshots/13-accounts.png)

| Field | Description |
|-------|-------------|
| **Name** | Display name in top bar |
| **Email** | Sign-in username |
| **Role** | Admin, Manager, Reception, Housekeeper, Restaurant, Kitchen |
| **Password** | Set or reset staff password |
| **Status** | Active / inactive |

### Recommended setup

1. Complete [First-time setup](first-time-setup.md) as property owner (Admin).
2. Create one account per staff member — **do not share** the admin password.
3. Assign **least privilege** role (see [User roles & permissions](user-roles-and-permissions.md)).
4. Deactivate accounts when staff leave.

---

## Messages

**Path:** Sidebar → **Messages** — **Admin only**

Communication log for guest and internal messages. Surfaces on Dashboard as **Communication Log** / **Recent Activity**.

---

## Audit log (master trail)

**Path:** Sidebar → **Audit Log** — **Admin only**

System-wide compliance trail — who changed what and when. The master log now includes:

| Feature | Description |
|---------|-------------|
| **Module filter** | Focus on Hotel, Service, Invoice, Inventory, Mini-Mart, etc. |
| **Action filter** | Sale, Payment, Insert, Update, Delete, Export, … |
| **Date range** | From / To date pickers |
| **Search** | Full-text search across all columns |
| **Export CSV** | Download filtered rows for compliance archive |
| **5,000 row cap** | Older entries roll off automatically (export monthly) |

### What gets logged

| Event type | Example module | Example action |
|------------|----------------|----------------|
| **POS / till sales** | Mini-Mart, POS, Service | `Sale` with transaction id in **Items** column |
| **Invoice payment** | Invoice | `Payment` with cash total and transaction id |
| **Catalog edits** | Service, Inventory | `Update`, `Insert`, `Delete` |
| **Booking changes** | Booking | `Update`, `Service`, `Override` |
| **Staff accounts** | Account | `Update`, `Toggle`, `Delete` |
| **Audit export** | Audit | `Export` when CSV downloaded |

Sales from **Mini-Mart**, **Inventory POS**, **Restaurant**, **Services (walk-in)**, and **invoice cash payment** all create transaction records linked in the audit **Items** column.

### Export for compliance

1. Open **Audit Log**
2. Set filters (module, dates) if needed
3. Click **Export** — downloads `audit-log-YYYY-MM-DD.csv`
4. For full database archive: **Settings → Export all data (CSV ZIP)**

---

## Per-module change logs

Most modules include a **Change Log** panel at the bottom of the page:

| Module | Log key |
|--------|---------|
| Rooms | Rooms change log |
| Bookings | Bookings change log |
| Services | Services change log |
| Invoices | Invoices change log |
| Inventory | Inventory audit |
| Restaurant | Restaurant change log |
| All Transactions | Transactions change log |

These complement the master **Audit Log** — use master log for compliance, module logs for day-to-day operations.

---

## Security practices

1. **Disable** inactive accounts — never share one login across shifts
2. **Kitchen / Housekeeper** roles — no access to rates or settings
3. **Export audit** monthly for properties with compliance requirements
4. Change owner password after install if it was shared during setup
5. **Documentation** access is allowed for all roles — train staff using in-app **Help**

---

## Related

- [User roles & permissions](user-roles-and-permissions.md)
- [Services & billing](services-and-billing.md) — sell and payment flows
- [Mini-mart & POS](minimart-and-pos.md)
- [Backup, restore & data](backup-restore-and-data.md)
