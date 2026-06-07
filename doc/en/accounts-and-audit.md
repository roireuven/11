# Accounts & audit

Staff access control, messaging, and compliance logging — **Admin** modules.

**Paths:** Sidebar → **Accounts** · **Messages** · **Audit Log**

---

## Accounts (user management)

**Path:** Sidebar → **Accounts** — **Admin only**

![Accounts — create staff logins and roles](assets/screenshots/13-accounts.png)

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

### Demo vs production accounts

| Mode | Use |
|------|-----|
| **Demo logins** | Training only — see [Demo credentials](demo-credentials.md) |
| **Production accounts** | Real staff — created in **Accounts** |

Run **Factory reset** in Settings before go-live if you used demo data.

---

## Messages

**Path:** Sidebar → **Messages** — **Admin only**

Communication log for guest and internal messages. Surfaces on Dashboard as **Communication Log** / **Recent Activity**.

Use with **Guest Portal** and **Services** for guest-facing workflows.

---

## Audit log

**Path:** Sidebar → **Audit Log** — **Admin only**

System-wide compliance trail — who changed what and when. Complements per-module change logs below.

### Export for compliance

**Settings → Export all data (CSV ZIP)** includes audit tables for external archive.

---

## Per-module change logs

Most modules include a **Change Log** panel:

| Module | Log key |
|--------|---------|
| Rooms | Rooms change log |
| Bookings | Bookings change log |
| Guests | Guests change log |
| Housekeeping | Housekeeping change log |
| Invoices | Invoices change log |
| Inventory | Inventory audit |
| Restaurant | Restaurant change log |
| Order History | Order history change log |
| Accounts | Accounts change log |
| Dropdown Lists | Dropdowns change log |
| Guest Portal | `guestportal` in audit export |
| All Transactions | Transactions change log |

Empty logs show: *"No changes recorded yet"*

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
- [Demo credentials](demo-credentials.md)
- [Backup, restore & data](backup-restore-and-data.md)
- [Guest portal](guest-portal.md)
